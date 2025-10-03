"""
Clarifier Agent Module

Genera preguntas de aclaración para refinar consultas del usuario
y mejorar la precisión de las respuestas del agente de CV.
"""

import os
import json
import re
from typing import List, Dict, Any, Optional
import logging
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
logger = logging.getLogger(__name__)

# Cliente OpenAI
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
MODEL = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")

CLARIFIER_SYSTEM = """
Genera EXACTAMENTE 3 preguntas de aclaración, cortas y concretas, 
que ayuden a refinar la consulta del usuario para un agente-CV profesional.

Las preguntas deben ser:
- Específicas y actionables
- Relevantes para la experiencia profesional
- Que ayuden a dar respuestas más precisas

Devuelve un JSON con la forma: {"questions": ["pregunta1", "pregunta2", "pregunta3"]}

Ejemplos de buenas preguntas de aclaración:
- "¿Te interesa algún sector específico como fintech o e-commerce?"
- "¿Buscas información sobre tecnologías específicas o arquitectura general?"
- "¿Prefieres ejemplos de proyectos recientes o experiencia general?"
"""

class ClarifierAgent:
    """Agente especializado en generar preguntas de aclaración"""
    
    def __init__(self):
        """Inicializar el agente clarificador"""
        self.client = client
        self.model = MODEL
        self.stats = {
            "total_clarifications": 0,
            "successful_clarifications": 0,
            "failed_clarifications": 0
        }
    
    def generate_clarifying_questions(self, user_query: str, context: str = "") -> List[str]:
        """
        Genera 3 preguntas de aclaración para refinar la consulta
        
        Args:
            user_query: Consulta original del usuario
            context: Contexto adicional para refinar las preguntas
            
        Returns:
            Lista de preguntas de aclaración
        """
        try:
            self.stats["total_clarifications"] += 1
            
            # Incluir contexto si se proporciona
            user_content = f"Consulta: {user_query}"
            if context:
                user_content += f"\nContexto: {context}"
            
            messages = [
                {"role": "system", "content": CLARIFIER_SYSTEM},
                {"role": "user", "content": user_content}
            ]
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.7,
                max_tokens=300
            )
            
            content = response.choices[0].message.content
            questions_data = self._safe_json_parse(content)
            
            if questions_data.get("questions") and len(questions_data["questions"]) > 0:
                self.stats["successful_clarifications"] += 1
                return questions_data["questions"][:3]  # Máximo 3 preguntas
            else:
                logger.warning("No se generaron preguntas válidas")
                return self._get_fallback_questions(user_query)
                
        except Exception as e:
            logger.error(f"Error generando preguntas de aclaración: {e}")
            self.stats["failed_clarifications"] += 1
            return self._get_fallback_questions(user_query)
    
    def _safe_json_parse(self, text: str) -> Dict[str, Any]:
        """
        Parsea JSON de manera segura con fallbacks
        
        Args:
            text: Texto que contiene JSON
            
        Returns:
            Dict parseado o con fallback
        """
        try:
            # Intentar parseo directo
            return json.loads(text)
        except json.JSONDecodeError:
            try:
                # Intentar extraer JSON del texto
                json_start = text.find('{')
                json_end = text.rfind('}') + 1
                
                if json_start >= 0 and json_end > json_start:
                    json_str = text[json_start:json_end]
                    return json.loads(json_str)
            except:
                pass
            
            # Fallback: extraer preguntas con regex
            questions = []
            
            # Buscar patrones de lista
            patterns = [
                r'"([^"]+\?)"',  # Preguntas entre comillas
                r'[-*•]\s*(.+\?)',  # Lista con viñetas
                r'\d+\.\s*(.+\?)',  # Lista numerada
            ]
            
            for pattern in patterns:
                matches = re.findall(pattern, text)
                if matches:
                    questions.extend([q.strip() for q in matches])
                    break
            
            return {"questions": questions[:3]}
    
    def _get_fallback_questions(self, user_query: str) -> List[str]:
        """
        Genera preguntas de fallback cuando falla la generación automática
        
        Args:
            user_query: Consulta original
            
        Returns:
            Lista de preguntas de fallback
        """
        # Preguntas genéricas pero útiles basadas en patrones comunes
        fallback_questions = [
            "¿Te interesa información sobre alguna tecnología específica?",
            "¿Buscas detalles sobre proyectos particulares o experiencia general?",
            "¿Hay algún sector o industria que te interese más?"
        ]
        
        # Personalizar según palabras clave en la consulta
        query_lower = user_query.lower()
        
        if "proyecto" in query_lower or "experiencia" in query_lower:
            fallback_questions[1] = "¿Prefieres ejemplos de proyectos recientes (últimos 2 años) o experiencia histórica?"
        
        if "tecnolog" in query_lower or "stack" in query_lower:
            fallback_questions[0] = "¿Te interesa el stack backend, frontend, o arquitectura completa?"
        
        if "sector" in query_lower or "industria" in query_lower:
            fallback_questions[2] = "¿Buscas experiencia en fintech, e-commerce, o algún otro sector específico?"
        
        return fallback_questions
    
    def refine_query_with_assumptions(self, original_query: str, clarifying_questions: List[str]) -> str:
        """
        Refina la consulta original agregando supuestos explícitos
        
        Args:
            original_query: Consulta original del usuario
            clarifying_questions: Lista de preguntas de aclaración
            
        Returns:
            Consulta refinada con supuestos
        """
        if not clarifying_questions:
            return original_query
        
        assumptions = " | ".join([
            f"Supuesto: {q} = (no especificado)" 
            for q in clarifying_questions
        ])
        
        refined = f"{original_query}\n\nAclaraciones necesarias: {assumptions}"
        
        logger.info(f"Consulta refinada con {len(clarifying_questions)} supuestos")
        
        return refined
    
    def refine_query_with_answers(
        self, 
        original_query: str, 
        qa_pairs: List[Dict[str, str]]
    ) -> str:
        """
        Refina la consulta con respuestas específicas del usuario
        
        Args:
            original_query: Consulta original
            qa_pairs: Lista de {"question": "...", "answer": "..."}
            
        Returns:
            Consulta refinada con respuestas
        """
        if not qa_pairs:
            return original_query
        
        clarifications = []
        for qa in qa_pairs:
            if qa.get("answer") and qa["answer"].strip().lower() not in ["no", "ninguno", "no especificado"]:
                clarifications.append(f"{qa['question']} → {qa['answer']}")
        
        if clarifications:
            clarification_text = " | ".join(clarifications)
            refined = f"{original_query}\n\nEspecificaciones: {clarification_text}"
        else:
            refined = original_query
        
        logger.info(f"Consulta refinada con {len(clarifications)} respuestas específicas")
        
        return refined
    
    def get_stats(self) -> Dict[str, Any]:
        """Obtener estadísticas del agente clarificador"""
        total = self.stats["total_clarifications"]
        success_rate = (self.stats["successful_clarifications"] / max(total, 1)) * 100
        
        return {
            **self.stats,
            "success_rate": round(success_rate, 2)
        }

# Función de conveniencia para uso directo
def generate_clarifying_questions(user_query: str) -> Dict[str, Any]:
    """
    Función de conveniencia para generar preguntas de aclaración
    
    Args:
        user_query: Consulta del usuario
        
    Returns:
        Dict con preguntas generadas
    """
    clarifier = ClarifierAgent()
    return clarifier.generate_clarifying_questions(user_query)

# Instancia global para uso en el orquestador
_clarifier_instance = None

def get_clarifier() -> ClarifierAgent:
    """Obtener instancia singleton del clarificador"""
    global _clarifier_instance
    if _clarifier_instance is None:
        _clarifier_instance = ClarifierAgent()
    return _clarifier_instance