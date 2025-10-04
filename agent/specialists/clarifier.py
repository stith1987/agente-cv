"""
Clarifier Agent Module

Agente especializado refactorizado para generar preguntas de aclaración
inteligentes que mejoren la precisión de las respuestas.
"""

import json
import time
from typing import List, Dict, Any, Optional
from openai import OpenAI

from ..utils.config import AgentConfig
from ..utils.logger import AgentLogger
from ..utils.prompts import PromptManager, PromptType


class ClarifierAgent:
    """Agente especializado en generar preguntas de aclaración"""
    
    def __init__(self, config: AgentConfig, logger: AgentLogger = None):
        """
        Inicializar agente clarificador
        
        Args:
            config: Configuración del agente
            logger: Logger para registrar actividad
        """
        self.config = config
        self.logger = logger or AgentLogger("clarifier_agent")
        self.prompt_manager = PromptManager()
        
        # Cliente OpenAI
        self.openai_client = OpenAI(api_key=config.openai.api_key)
        
        # Estadísticas
        self.stats = {
            "total_clarifications": 0,
            "successful_clarifications": 0,
            "failed_clarifications": 0,
            "average_questions_per_clarification": 0.0
        }
        
        self.logger.info("ClarifierAgent initialized successfully")
    
    def generate_clarifications(self, query: str, context: Dict[str, Any] = None) -> List[str]:
        """
        Generar preguntas de aclaración para refinar la consulta
        
        Args:
            query: Consulta original del usuario
            context: Contexto adicional de la conversación
            
        Returns:
            Lista de preguntas de aclaración
        """
        start_time = time.time()
        context = context or {}
        
        try:
            self.logger.debug(f"Generating clarifications for query: {query}")
            
            # Generar prompt de aclaración
            clarification_prompt = self.prompt_manager.format_clarification_prompt(query)
            
            # Llamada a OpenAI
            response = self.openai_client.chat.completions.create(
                model=self.config.openai.model,
                messages=[
                    {"role": "system", "content": "Eres un experto en generar preguntas de aclaración para consultas sobre CV profesional."},
                    {"role": "user", "content": clarification_prompt}
                ],
                temperature=0.7,  # Permitir algo de creatividad
                max_tokens=400
            )
            
            # Parsear respuesta
            response_text = response.choices[0].message.content.strip()
            
            try:
                clarification_data = json.loads(response_text)
                questions = clarification_data.get("questions", [])
            except json.JSONDecodeError:
                # Intentar extraer preguntas de texto plano
                questions = self._extract_questions_from_text(response_text)
            
            # Validar y filtrar preguntas
            questions = self._validate_questions(questions)
            
            # Aplicar reglas de mejora
            questions = self._improve_questions(questions, query, context)
            
            # Actualizar estadísticas
            self._update_stats(questions, True)
            
            execution_time = time.time() - start_time
            self.logger.log_tool_usage(
                "clarification_generation",
                {"query": query, "questions_count": len(questions)},
                True,
                execution_time
            )
            
            return questions
            
        except Exception as e:
            self.logger.error("Error generating clarifications", exception=e)
            self._update_stats([], False)
            
            # Preguntas por defecto en caso de error
            return self._get_default_questions(query)
    
    def _extract_questions_from_text(self, text: str) -> List[str]:
        """Extraer preguntas de texto plano"""
        questions = []
        
        # Buscar líneas que terminen con '?'
        lines = text.split('\n')
        for line in lines:
            line = line.strip()
            if line.endswith('?') and len(line) > 10:
                # Limpiar numeración y símbolos
                clean_line = line.lstrip('1234567890.-*• ').strip()
                if clean_line:
                    questions.append(clean_line)
        
        return questions[:3]  # Máximo 3 preguntas
    
    def _validate_questions(self, questions: List[str]) -> List[str]:
        """Validar y filtrar preguntas"""
        if not questions:
            return []
        
        valid_questions = []
        
        for question in questions:
            if not isinstance(question, str):
                continue
            
            question = question.strip()
            
            # Filtros de validación
            if not question:
                continue
            
            if not question.endswith('?'):
                question += '?'
            
            if len(question) < 15:  # Muy corta
                continue
                
            if len(question) > 200:  # Muy larga
                continue
            
            # Evitar preguntas duplicadas
            if question not in valid_questions:
                valid_questions.append(question)
        
        return valid_questions[:3]  # Máximo 3 preguntas
    
    def _improve_questions(self, questions: List[str], query: str, context: Dict[str, Any]) -> List[str]:
        """Mejorar preguntas basándose en el contexto"""
        if not questions:
            return self._get_default_questions(query)
        
        improved_questions = []
        query_lower = query.lower()
        
        # Agregar preguntas específicas basadas en palabras clave
        if "proyecto" in query_lower and len(questions) < 3:
            improved_questions.append("¿Te interesa algún proyecto específico o tipo de industria?")
        
        if "tecnología" in query_lower and len(questions) < 3:
            improved_questions.append("¿Buscas información sobre tecnologías específicas o arquitectura general?")
        
        if "experiencia" in query_lower and len(questions) < 3:
            improved_questions.append("¿Prefieres información sobre roles específicos o experiencia general?")
        
        # Combinar preguntas originales con mejoradas
        all_questions = questions + improved_questions
        
        # Eliminar duplicados y limitar a 3
        unique_questions = []
        for q in all_questions:
            if q not in unique_questions:
                unique_questions.append(q)
        
        return unique_questions[:3]
    
    def _get_default_questions(self, query: str) -> List[str]:
        """Obtener preguntas por defecto basadas en la consulta"""
        query_lower = query.lower()
        
        default_questions = [
            "¿Podrías ser más específico sobre qué aspecto te interesa más?",
            "¿Buscas información técnica detallada o un resumen general?",
            "¿Hay algún período de tiempo o proyecto específico que te interese?"
        ]
        
        # Personalizar basándose en palabras clave
        if "tecnología" in query_lower:
            default_questions[0] = "¿Te interesa alguna tecnología o stack específico?"
        elif "proyecto" in query_lower:
            default_questions[0] = "¿Hay algún tipo de proyecto o industria específica que te interese?"
        elif "experiencia" in query_lower:
            default_questions[0] = "¿Buscas información sobre algún rol o responsabilidad específica?"
        
        return default_questions
    
    def _update_stats(self, questions: List[str], success: bool):
        """Actualizar estadísticas"""
        self.stats["total_clarifications"] += 1
        
        if success:
            self.stats["successful_clarifications"] += 1
            
            # Actualizar promedio de preguntas
            total_successful = self.stats["successful_clarifications"]
            current_avg = self.stats["average_questions_per_clarification"]
            
            if total_successful > 0:
                self.stats["average_questions_per_clarification"] = (
                    (current_avg * (total_successful - 1) + len(questions)) / total_successful
                )
        else:
            self.stats["failed_clarifications"] += 1
    
    def analyze_clarification_need(self, query: str, classification: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Analizar si una consulta necesita aclaración
        
        Args:
            query: Consulta a analizar
            classification: Clasificación previa de la consulta
            
        Returns:
            Análisis de necesidad de aclaración
        """
        classification = classification or {}
        
        analysis = {
            "needs_clarification": False,
            "confidence": 100,
            "reasons": [],
            "urgency": "low"
        }
        
        query_words = query.split()
        query_lower = query.lower()
        
        # Regla 1: Consultas muy cortas
        if len(query_words) <= 3:
            analysis["needs_clarification"] = True
            analysis["confidence"] -= 30
            analysis["reasons"].append("Consulta muy breve")
            analysis["urgency"] = "high"
        
        # Regla 2: Palabras vagas
        vague_words = ["qué", "cuál", "cómo", "dime", "información", "algo", "todo"]
        vague_count = sum(1 for word in vague_words if word in query_lower)
        
        if vague_count >= 2:
            analysis["needs_clarification"] = True
            analysis["confidence"] -= 20
            analysis["reasons"].append("Contiene palabras vagas")
        
        # Regla 3: Múltiples temas
        topics = ["proyecto", "experiencia", "tecnología", "educación", "contacto"]
        topic_count = sum(1 for topic in topics if topic in query_lower)
        
        if topic_count >= 3:
            analysis["needs_clarification"] = True
            analysis["confidence"] -= 15
            analysis["reasons"].append("Múltiples temas en una consulta")
            analysis["urgency"] = "medium"
        
        # Regla 4: Clasificación de baja confianza
        if classification.get("confidence", 100) < 60:
            analysis["needs_clarification"] = True
            analysis["confidence"] -= 25
            analysis["reasons"].append("Clasificación de baja confianza")
        
        # Ajustar confianza final
        analysis["confidence"] = max(0, analysis["confidence"])
        
        return analysis
    
    def get_stats(self) -> Dict[str, Any]:
        """Obtener estadísticas del agente"""
        success_rate = 0
        if self.stats["total_clarifications"] > 0:
            success_rate = (self.stats["successful_clarifications"] / 
                          self.stats["total_clarifications"]) * 100
        
        return {
            **self.stats,
            "success_rate": round(success_rate, 2)
        }
    
    def reset_stats(self):
        """Reiniciar estadísticas"""
        self.stats = {
            "total_clarifications": 0,
            "successful_clarifications": 0,
            "failed_clarifications": 0,
            "average_questions_per_clarification": 0.0
        }
        self.logger.info("Clarifier stats reset")