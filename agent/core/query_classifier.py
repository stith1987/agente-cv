"""
Query Classifier Module

Sistema de clasificación inteligente de consultas para determinar
la mejor estrategia de respuesta y herramientas a utilizar.
"""

import json
from typing import Dict, Any, List, Optional, Tuple
from dataclasses import dataclass
from enum import Enum
from openai import OpenAI

from ..utils.config import AgentConfig
from ..utils.logger import AgentLogger
from ..utils.prompts import PromptManager, PromptType


class QueryCategory(Enum):
    """Categorías de consultas"""
    BASIC = "BASIC"           # Información general, datos básicos
    TECHNICAL = "TECHNICAL"   # Tecnologías específicas, arquitecturas
    EXPERIENCE = "EXPERIENCE" # Experiencia laboral, roles
    PROJECTS = "PROJECTS"     # Detalles de proyectos específicos
    COMPLEX = "COMPLEX"       # Consultas multifacéticas


class RecommendedTool(Enum):
    """Herramientas recomendadas"""
    FAQ = "FAQ"               # Base de datos FAQ
    RAG = "RAG"               # Búsqueda semántica
    COMBINED = "COMBINED"     # Búsqueda combinada
    CLARIFY = "CLARIFY"       # Necesita aclaración


class ComplexityLevel(Enum):
    """Niveles de complejidad"""
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"


@dataclass
class QueryClassification:
    """Resultado de clasificación de consulta"""
    category: QueryCategory
    confidence: float
    recommended_tool: RecommendedTool
    reasoning: str
    search_terms: List[str]
    expected_complexity: ComplexityLevel
    
    def __post_init__(self):
        """Validación post-inicialización"""
        if not 0 <= self.confidence <= 100:
            raise ValueError("Confidence debe estar entre 0 y 100")
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'QueryClassification':
        """Crear desde diccionario"""
        return cls(
            category=QueryCategory(data.get("category", "COMPLEX")),
            confidence=float(data.get("confidence", 50)),
            recommended_tool=RecommendedTool(data.get("recommended_tool", "COMBINED")),
            reasoning=data.get("reasoning", ""),
            search_terms=data.get("search_terms", []),
            expected_complexity=ComplexityLevel(data.get("expected_complexity", "MEDIUM"))
        )
    
    def to_dict(self) -> Dict[str, Any]:
        """Convertir a diccionario"""
        return {
            "category": self.category.value,
            "confidence": self.confidence,
            "recommended_tool": self.recommended_tool.value,
            "reasoning": self.reasoning,
            "search_terms": self.search_terms,
            "expected_complexity": self.expected_complexity.value
        }
    
    def is_high_confidence(self, threshold: float = 80.0) -> bool:
        """Verificar si la clasificación tiene alta confianza"""
        return self.confidence >= threshold
    
    def needs_clarification(self) -> bool:
        """Verificar si necesita aclaración"""
        return (self.recommended_tool == RecommendedTool.CLARIFY or 
                self.confidence < 60 or 
                self.expected_complexity == ComplexityLevel.HIGH)


class QueryClassifier:
    """Clasificador inteligente de consultas"""
    
    def __init__(self, config: AgentConfig, logger: AgentLogger = None):
        """
        Inicializar clasificador
        
        Args:
            config: Configuración del agente
            logger: Logger para registrar actividad
        """
        self.config = config
        self.logger = logger or AgentLogger("query_classifier")
        self.prompt_manager = PromptManager()
        
        # Cliente OpenAI
        self.openai_client = OpenAI(api_key=config.openai.api_key)
        
        # Estadísticas
        self.stats = {
            "total_classifications": 0,
            "successful_classifications": 0,
            "failed_classifications": 0,
            "category_distribution": {cat.value: 0 for cat in QueryCategory},
            "tool_recommendations": {tool.value: 0 for tool in RecommendedTool}
        }
        
        self.logger.info("QueryClassifier initialized successfully")
    
    def classify(self, query: str, context: Dict[str, Any] = None) -> QueryClassification:
        """
        Clasificar consulta
        
        Args:
            query: Consulta del usuario
            context: Contexto adicional
            
        Returns:
            Clasificación de la consulta
        """
        start_time = time.time()
        context = context or {}
        
        try:
            self.logger.debug(f"Classifying query: {query}")
            
            # Generar prompt de clasificación
            classification_prompt = self.prompt_manager.format_classification_prompt(query)
            
            # Llamada a OpenAI
            response = self.openai_client.chat.completions.create(
                model=self.config.openai.model,
                messages=[
                    {"role": "system", "content": "Eres un clasificador experto de consultas sobre CV profesional."},
                    {"role": "user", "content": classification_prompt}
                ],
                temperature=0.3,  # Baja temperatura para consistencia
                max_tokens=500
            )
            
            # Parsear respuesta
            response_text = response.choices[0].message.content.strip()
            
            try:
                classification_data = json.loads(response_text)
            except json.JSONDecodeError:
                # Intentar extraer JSON de la respuesta
                classification_data = self._extract_json_from_response(response_text)
            
            # Crear clasificación
            classification = QueryClassification.from_dict(classification_data)
            
            # Aplicar reglas de negocio
            classification = self._apply_business_rules(classification, query, context)
            
            # Actualizar estadísticas
            self._update_stats(classification, True)
            
            execution_time = time.time() - start_time
            self.logger.log_tool_usage(
                "query_classification", 
                {"query": query, "category": classification.category.value},
                True, 
                execution_time
            )
            
            return classification
            
        except Exception as e:
            self.logger.error("Error in query classification", exception=e)
            self._update_stats(success=False)
            
            # Clasificación por defecto en caso de error
            return self._get_default_classification(query)
    
    def _extract_json_from_response(self, response_text: str) -> Dict[str, Any]:
        """Extraer JSON de respuesta que puede contener texto adicional"""
        try:
            # Buscar JSON en la respuesta
            start_idx = response_text.find('{')
            end_idx = response_text.rfind('}') + 1
            
            if start_idx != -1 and end_idx != -1:
                json_str = response_text[start_idx:end_idx]
                return json.loads(json_str)
            else:
                raise ValueError("No JSON found in response")
                
        except Exception as e:
            self.logger.warning(f"Failed to extract JSON from response: {e}")
            # Clasificación básica por defecto
            return {
                "category": "COMPLEX",
                "confidence": 50,
                "recommended_tool": "COMBINED",
                "reasoning": "Error parsing classification response",
                "search_terms": [query],
                "expected_complexity": "MEDIUM"
            }
    
    def _apply_business_rules(self, classification: QueryClassification, 
                            query: str, context: Dict[str, Any]) -> QueryClassification:
        """Aplicar reglas de negocio para mejorar la clasificación"""
        
        # Regla 1: Consultas muy cortas o vagas necesitan aclaración
        if len(query.split()) <= 3 or any(word in query.lower() for word in ["qué", "cuál", "cómo", "dime"]):
            if classification.confidence < 70:
                classification.recommended_tool = RecommendedTool.CLARIFY
                classification.reasoning += " (Query too vague, needs clarification)"
        
        # Regla 2: Palabras clave específicas determinan herramienta
        query_lower = query.lower()
        
        # FAQ keywords
        faq_keywords = ["contacto", "email", "teléfono", "nombre", "edad", "ubicación", "estudios", "universidad"]
        if any(keyword in query_lower for keyword in faq_keywords):
            classification.recommended_tool = RecommendedTool.FAQ
            classification.category = QueryCategory.BASIC
        
        # RAG keywords
        rag_keywords = ["proyecto", "experiencia", "tecnología", "arquitectura", "implementación", "desarrollo"]
        if any(keyword in query_lower for keyword in rag_keywords):
            classification.recommended_tool = RecommendedTool.RAG
            if "proyecto" in query_lower:
                classification.category = QueryCategory.PROJECTS
            elif "tecnología" in query_lower or "arquitectura" in query_lower:
                classification.category = QueryCategory.TECHNICAL
        
        # Regla 3: Ajustar confianza basada en contexto
        if context.get("previous_queries", 0) > 0:
            # Incrementar confianza si hay contexto previo
            classification.confidence = min(100, classification.confidence + 10)
        
        # Regla 4: Consultas complejas necesitan herramientas combinadas
        if len(query.split()) > 15 or "y" in query_lower or "también" in query_lower:
            classification.recommended_tool = RecommendedTool.COMBINED
            classification.expected_complexity = ComplexityLevel.HIGH
        
        return classification
    
    def _get_default_classification(self, query: str) -> QueryClassification:
        """Obtener clasificación por defecto en caso de error"""
        return QueryClassification(
            category=QueryCategory.COMPLEX,
            confidence=50.0,
            recommended_tool=RecommendedTool.COMBINED,
            reasoning="Default classification due to processing error",
            search_terms=[query],
            expected_complexity=ComplexityLevel.MEDIUM
        )
    
    def _update_stats(self, classification: QueryClassification = None, success: bool = True):
        """Actualizar estadísticas"""
        self.stats["total_classifications"] += 1
        
        if success and classification:
            self.stats["successful_classifications"] += 1
            self.stats["category_distribution"][classification.category.value] += 1
            self.stats["tool_recommendations"][classification.recommended_tool.value] += 1
        else:
            self.stats["failed_classifications"] += 1
    
    def get_stats(self) -> Dict[str, Any]:
        """Obtener estadísticas del clasificador"""
        success_rate = 0
        if self.stats["total_classifications"] > 0:
            success_rate = (self.stats["successful_classifications"] / 
                          self.stats["total_classifications"]) * 100
        
        return {
            **self.stats,
            "success_rate": round(success_rate, 2)
        }
    
    def batch_classify(self, queries: List[str]) -> List[QueryClassification]:
        """Clasificar múltiples consultas en lote"""
        results = []
        
        for query in queries:
            try:
                classification = self.classify(query)
                results.append(classification)
            except Exception as e:
                self.logger.error(f"Error classifying query '{query}'", exception=e)
                results.append(self._get_default_classification(query))
        
        return results
    
    def reset_stats(self):
        """Reiniciar estadísticas"""
        self.stats = {
            "total_classifications": 0,
            "successful_classifications": 0,
            "failed_classifications": 0,
            "category_distribution": {cat.value: 0 for cat in QueryCategory},
            "tool_recommendations": {tool.value: 0 for tool in RecommendedTool}
        }
        self.logger.info("Classification stats reset")


# Importar time que faltaba
import time