"""
Response Evaluator Module

Sistema de evaluación inteligente de respuestas para medir calidad,
precisión y completitud de las respuestas del agente de CV.
"""

import json
import time
from typing import Dict, Any, List, Optional, Tuple
from dataclasses import dataclass
from enum import Enum
from openai import OpenAI

from ..utils.config import AgentConfig
from ..utils.logger import AgentLogger
from ..utils.prompts import PromptManager, PromptType


class EvaluationCriteria(Enum):
    """Criterios de evaluación"""
    PRECISION = "precision"         # Información correcta y respaldada
    COMPLETENESS = "completeness"   # Respuesta completa y detallada
    RELEVANCE = "relevance"         # Relacionada con la consulta
    CLARITY = "clarity"             # Fácil de entender
    PROFESSIONALISM = "professionalism"  # Tono apropiado


@dataclass
class EvaluationScores:
    """Puntuaciones detalladas de evaluación"""
    precision: float
    completeness: float
    relevance: float
    clarity: float
    professionalism: float
    
    def __post_init__(self):
        """Validar puntuaciones"""
        for score in [self.precision, self.completeness, self.relevance, 
                     self.clarity, self.professionalism]:
            if not 0 <= score <= 10:
                raise ValueError("All scores must be between 0 and 10")
    
    @property
    def overall_score(self) -> float:
        """Calcular puntuación general ponderada"""
        weights = {
            'precision': 0.30,
            'completeness': 0.25,
            'relevance': 0.20,
            'clarity': 0.15,
            'professionalism': 0.10
        }
        
        return (
            self.precision * weights['precision'] +
            self.completeness * weights['completeness'] +
            self.relevance * weights['relevance'] +
            self.clarity * weights['clarity'] +
            self.professionalism * weights['professionalism']
        )
    
    def to_dict(self) -> Dict[str, float]:
        """Convertir a diccionario"""
        return {
            "precision": self.precision,
            "completeness": self.completeness,
            "relevance": self.relevance,
            "clarity": self.clarity,
            "professionalism": self.professionalism,
            "overall_score": self.overall_score
        }


@dataclass
class EvaluationResult:
    """Resultado completo de evaluación"""
    scores: EvaluationScores
    confidence: float
    strengths: List[str]
    weaknesses: List[str]
    suggestions: List[str]
    
    def __post_init__(self):
        """Validación post-inicialización"""
        if not 0 <= self.confidence <= 100:
            raise ValueError("Confidence must be between 0 and 100")
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'EvaluationResult':
        """Crear desde diccionario"""
        scores_data = data.get("scores", {})
        scores = EvaluationScores(
            precision=float(scores_data.get("precision", 5.0)),
            completeness=float(scores_data.get("completeness", 5.0)),
            relevance=float(scores_data.get("relevance", 5.0)),
            clarity=float(scores_data.get("clarity", 5.0)),
            professionalism=float(scores_data.get("professionalism", 5.0))
        )
        
        return cls(
            scores=scores,
            confidence=float(data.get("confidence", 50)),
            strengths=data.get("strengths", []),
            weaknesses=data.get("weaknesses", []),
            suggestions=data.get("suggestions", [])
        )
    
    def to_dict(self) -> Dict[str, Any]:
        """Convertir a diccionario"""
        return {
            "overall_score": self.scores.overall_score,
            "scores": self.scores.to_dict(),
            "confidence": self.confidence,
            "strengths": self.strengths,
            "weaknesses": self.weaknesses,
            "suggestions": self.suggestions
        }
    
    def is_high_quality(self, threshold: float = 7.0) -> bool:
        """Verificar si es de alta calidad"""
        return self.scores.overall_score >= threshold
    
    def get_summary(self) -> str:
        """Obtener resumen de la evaluación"""
        score = self.scores.overall_score
        quality = "Excelente" if score >= 8.5 else "Buena" if score >= 7.0 else "Regular" if score >= 5.0 else "Deficiente"
        
        return f"Calidad: {quality} (Score: {score:.1f}/10, Confianza: {self.confidence:.0f}%)"


class ResponseEvaluator:
    """Evaluador inteligente de respuestas"""
    
    def __init__(self, config: AgentConfig, logger: AgentLogger = None):
        """
        Inicializar evaluador
        
        Args:
            config: Configuración del agente
            logger: Logger para registrar actividad
        """
        self.config = config
        self.logger = logger or AgentLogger("response_evaluator")
        self.prompt_manager = PromptManager()
        
        # Cliente OpenAI
        self.openai_client = OpenAI(api_key=config.openai.api_key)
        
        # Estadísticas
        self.stats = {
            "total_evaluations": 0,
            "successful_evaluations": 0,
            "failed_evaluations": 0,
            "average_score": 0.0,
            "high_quality_responses": 0,
            "score_distribution": {
                "excellent": 0,  # 8.5-10
                "good": 0,       # 7.0-8.4
                "regular": 0,    # 5.0-6.9
                "poor": 0        # 0-4.9
            }
        }
        
        self.logger.info("ResponseEvaluator initialized successfully")
    
    def evaluate_response(self, 
                         query: str, 
                         response: str, 
                         context: str = "", 
                         metadata: Optional[Dict[str, Any]] = None) -> EvaluationResult:
        """
        Evaluar calidad de respuesta
        
        Args:
            query: Consulta original
            response: Respuesta a evaluar
            context: Contexto utilizado
            metadata: Metadatos adicionales
            
        Returns:
            Resultado de evaluación
        """
        start_time = time.time()
        metadata = metadata or {}
        
        try:
            self.logger.debug(f"Evaluating response for query: {query[:100]}...")
            
            # Generar prompt de evaluación
            evaluation_prompt = self.prompt_manager.format_evaluation_prompt(
                query=query,
                response=response,
                context=context
            )
            
            # Llamada a OpenAI
            response_obj = self.openai_client.chat.completions.create(
                model=self.config.openai.model,
                messages=[
                    {"role": "system", "content": "Eres un evaluador experto de respuestas sobre CV profesional."},
                    {"role": "user", "content": evaluation_prompt}
                ],
                temperature=0.2,  # Baja temperatura para consistencia
                max_tokens=800
            )
            
            # Parsear respuesta
            response_text = response_obj.choices[0].message.content.strip()
            
            try:
                evaluation_data = json.loads(response_text)
            except json.JSONDecodeError:
                # Intentar extraer JSON de la respuesta
                evaluation_data = self._extract_json_from_response(response_text)
            
            # Crear resultado de evaluación
            evaluation_result = EvaluationResult.from_dict(evaluation_data)
            
            # Aplicar reglas de validación
            evaluation_result = self._apply_validation_rules(
                evaluation_result, query, response, context, metadata
            )
            
            # Actualizar estadísticas
            self._update_stats(evaluation_result, True)
            
            execution_time = time.time() - start_time
            self.logger.log_tool_usage(
                "response_evaluation",
                {"score": evaluation_result.scores.overall_score},
                True,
                execution_time
            )
            
            return evaluation_result
            
        except Exception as e:
            self.logger.error("Error in response evaluation", exception=e)
            self._update_stats(success=False)
            
            # Evaluación por defecto en caso de error
            return self._get_default_evaluation()
    
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
            # Evaluación básica por defecto
            return {
                "overall_score": 6.0,
                "scores": {
                    "precision": 6.0,
                    "completeness": 6.0,
                    "relevance": 6.0,
                    "clarity": 6.0,
                    "professionalism": 6.0
                },
                "confidence": 60,
                "strengths": ["Response provided"],
                "weaknesses": ["Unable to properly evaluate"],
                "suggestions": ["Improve evaluation system"]
            }
    
    def _apply_validation_rules(self, 
                              evaluation: EvaluationResult,
                              query: str,
                              response: str,
                              context: str,
                              metadata: Dict[str, Any]) -> EvaluationResult:
        """Aplicar reglas de validación para mejorar la evaluación"""
        
        # Regla 1: Respuestas muy cortas generalmente tienen menor completitud
        if len(response.split()) < 20:
            evaluation.scores.completeness = min(evaluation.scores.completeness, 6.0)
            if "Respuesta muy breve" not in evaluation.weaknesses:
                evaluation.weaknesses.append("Respuesta muy breve")
        
        # Regla 2: Respuestas que no responden directamente la pregunta
        query_keywords = set(query.lower().split())
        response_keywords = set(response.lower().split())
        overlap = len(query_keywords.intersection(response_keywords))
        overlap_ratio = overlap / len(query_keywords) if query_keywords else 0
        
        if overlap_ratio < 0.3:
            evaluation.scores.relevance = min(evaluation.scores.relevance, 5.0)
            if "Baja relevancia con la consulta" not in evaluation.weaknesses:
                evaluation.weaknesses.append("Baja relevancia con la consulta")
        
        # Regla 3: Presencia de contexto mejora la precisión
        if context and len(context) > 100:
            evaluation.scores.precision = min(10.0, evaluation.scores.precision + 0.5)
            if "Respuesta basada en contexto específico" not in evaluation.strengths:
                evaluation.strengths.append("Respuesta basada en contexto específico")
        
        # Regla 4: Metadatos de herramientas usadas
        tools_used = metadata.get("tools_used", [])
        if "rag_search" in tools_used and "faq_query" in tools_used:
            evaluation.scores.completeness = min(10.0, evaluation.scores.completeness + 0.5)
            if "Búsqueda combinada utilizada" not in evaluation.strengths:
                evaluation.strengths.append("Búsqueda combinada utilizada")
        
        # Regla 5: Ajustar confianza basada en consistencia de scores
        scores_list = [
            evaluation.scores.precision,
            evaluation.scores.completeness,
            evaluation.scores.relevance,
            evaluation.scores.clarity,
            evaluation.scores.professionalism
        ]
        
        variance = sum((score - evaluation.scores.overall_score) ** 2 for score in scores_list) / len(scores_list)
        if variance > 2.0:  # Alta varianza indica inconsistencia
            evaluation.confidence = max(30, evaluation.confidence - 20)
        
        return evaluation
    
    def _get_default_evaluation(self) -> EvaluationResult:
        """Obtener evaluación por defecto en caso de error"""
        scores = EvaluationScores(
            precision=6.0,
            completeness=6.0,
            relevance=6.0,
            clarity=6.0,
            professionalism=6.0
        )
        
        return EvaluationResult(
            scores=scores,
            confidence=50.0,
            strengths=["Response was generated"],
            weaknesses=["Unable to properly evaluate"],
            suggestions=["Improve evaluation system"]
        )
    
    def _update_stats(self, evaluation: EvaluationResult = None, success: bool = True):
        """Actualizar estadísticas"""
        self.stats["total_evaluations"] += 1
        
        if success and evaluation:
            self.stats["successful_evaluations"] += 1
            
            score = evaluation.scores.overall_score
            
            # Actualizar promedio
            total_successful = self.stats["successful_evaluations"]
            current_avg = self.stats["average_score"]
            self.stats["average_score"] = ((current_avg * (total_successful - 1)) + score) / total_successful
            
            # Actualizar distribución
            if score >= 8.5:
                self.stats["score_distribution"]["excellent"] += 1
            elif score >= 7.0:
                self.stats["score_distribution"]["good"] += 1
            elif score >= 5.0:
                self.stats["score_distribution"]["regular"] += 1
            else:
                self.stats["score_distribution"]["poor"] += 1
            
            # Contar respuestas de alta calidad
            if evaluation.is_high_quality(self.config.evaluation_min_score):
                self.stats["high_quality_responses"] += 1
        else:
            self.stats["failed_evaluations"] += 1
    
    def self_critique(self, 
                     query: str, 
                     response: str, 
                     tools_used: List[str], 
                     context_quality: str = "unknown") -> Dict[str, Any]:
        """
        Auto-crítica del sistema de respuesta
        
        Args:
            query: Consulta original
            response: Respuesta generada
            tools_used: Herramientas utilizadas
            context_quality: Calidad del contexto
            
        Returns:
            Análisis de auto-crítica
        """
        try:
            evaluation = self.evaluate_response(query, response)
            
            critique = {
                "success": True,
                "overall_score": evaluation.scores.overall_score,
                "is_high_quality": evaluation.is_high_quality(),
                "critique": evaluation.get_summary(),
                "insights": {
                    "tools_effectiveness": self._analyze_tools_effectiveness(tools_used, evaluation),
                    "response_quality": self._analyze_response_quality(evaluation),
                    "context_impact": self._analyze_context_impact(context_quality, evaluation)
                },
                "recommendations": self._generate_recommendations(evaluation, tools_used)
            }
            
            return critique
            
        except Exception as e:
            self.logger.error("Error in self critique", exception=e)
            return {
                "success": False,
                "critique": "Unable to perform self-critique",
                "insights": {},
                "recommendations": ["Improve evaluation system"]
            }
    
    def _analyze_tools_effectiveness(self, tools_used: List[str], evaluation: EvaluationResult) -> Dict[str, Any]:
        """Analizar efectividad de herramientas utilizadas"""
        return {
            "tools_used": tools_used,
            "effectiveness_score": evaluation.scores.precision,
            "recommendation": "optimal" if evaluation.scores.precision >= 7.5 else "needs_improvement"
        }
    
    def _analyze_response_quality(self, evaluation: EvaluationResult) -> Dict[str, Any]:
        """Analizar calidad general de la respuesta"""
        return {
            "overall_quality": "high" if evaluation.is_high_quality() else "moderate",
            "strongest_aspect": max(evaluation.scores.to_dict().items(), key=lambda x: x[1])[0],
            "weakest_aspect": min(evaluation.scores.to_dict().items(), key=lambda x: x[1])[0]
        }
    
    def _analyze_context_impact(self, context_quality: str, evaluation: EvaluationResult) -> Dict[str, Any]:
        """Analizar impacto del contexto en la respuesta"""
        return {
            "context_quality": context_quality,
            "precision_impact": "positive" if evaluation.scores.precision >= 7.0 else "negative",
            "completeness_impact": "positive" if evaluation.scores.completeness >= 7.0 else "negative"
        }
    
    def _generate_recommendations(self, evaluation: EvaluationResult, tools_used: List[str]) -> List[str]:
        """Generar recomendaciones basadas en la evaluación"""
        recommendations = []
        
        if evaluation.scores.precision < 7.0:
            recommendations.append("Mejorar precisión usando más contexto específico")
        
        if evaluation.scores.completeness < 7.0:
            recommendations.append("Proporcionar respuestas más detalladas")
        
        if evaluation.scores.relevance < 7.0:
            recommendations.append("Mejorar relevancia enfocándose en palabras clave de la consulta")
        
        if len(tools_used) == 1:
            recommendations.append("Considerar usar múltiples herramientas para respuestas más completas")
        
        return recommendations
    
    def get_stats(self) -> Dict[str, Any]:
        """Obtener estadísticas del evaluador"""
        success_rate = 0
        quality_rate = 0
        
        if self.stats["total_evaluations"] > 0:
            success_rate = (self.stats["successful_evaluations"] / 
                          self.stats["total_evaluations"]) * 100
        
        if self.stats["successful_evaluations"] > 0:
            quality_rate = (self.stats["high_quality_responses"] / 
                          self.stats["successful_evaluations"]) * 100
        
        return {
            **self.stats,
            "success_rate": round(success_rate, 2),
            "quality_rate": round(quality_rate, 2)
        }
    
    def reset_stats(self):
        """Reiniciar estadísticas"""
        self.stats = {
            "total_evaluations": 0,
            "successful_evaluations": 0,
            "failed_evaluations": 0,
            "average_score": 0.0,
            "high_quality_responses": 0,
            "score_distribution": {
                "excellent": 0,
                "good": 0,
                "regular": 0,  
                "poor": 0
            }
        }
        self.logger.info("Evaluation stats reset")