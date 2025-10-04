"""
Prompts Manager Module

Sistema centralizado de gestión de prompts para el agente de CV.
"""

from typing import Dict, Any, List, Optional
from datetime import datetime
import json
from enum import Enum


class PromptType(Enum):
    """Tipos de prompts disponibles"""
    SYSTEM = "system"
    CLASSIFICATION = "classification"
    PLANNING = "planning"
    EVALUATION = "evaluation"
    CLARIFICATION = "clarification"
    EMAIL = "email"
    ERROR = "error"


class PromptManager:
    """Gestor centralizado de prompts"""
    
    def __init__(self):
        """Inicializar gestor de prompts"""
        self.prompts = self._load_prompts()
    
    def _load_prompts(self) -> Dict[str, str]:
        """Cargar todos los prompts"""
        return {
            PromptType.SYSTEM.value: self._get_system_prompt(),
            PromptType.CLASSIFICATION.value: self._get_classification_prompt(),
            PromptType.PLANNING.value: self._get_planning_prompt(),
            PromptType.EVALUATION.value: self._get_evaluation_prompt(),
            PromptType.CLARIFICATION.value: self._get_clarification_prompt(),
            PromptType.EMAIL.value: self._get_email_prompt(),
            PromptType.ERROR.value: self._get_error_prompt()
        }
    
    def _get_system_prompt(self) -> str:
        """Prompt del sistema principal"""
        return """
        Eres un asistente de IA especializado en representar la experiencia profesional de un Arquitecto de Soluciones Senior con más de 10 años de experiencia.

        ## Contexto del Profesional
        **Perfil:** Arquitecto de Soluciones Senior con más de 10 años de experiencia
        **Especialización:** Transformación digital, arquitecturas empresariales, microservicios, cloud-native
        **Sectores:** Principalmente financiero (banca digital, pagos), también e-commerce y tech empresarial
        **Tecnologías principales:** Java/Spring, Python, React, AWS, Docker, Kubernetes, PostgreSQL

        ## Instrucciones de Comportamiento
        1. **Precisión:** Responde solo con información respaldada por documentos
        2. **Profesionalismo:** Mantén un tono profesional pero accesible
        3. **Contexto:** Proporciona contexto relevante para cada respuesta
        4. **Claridad:** Explica conceptos técnicos cuando sea necesario
        5. **Honestidad:** Si no tienes información específica, dilo claramente

        ## Formato de Respuesta
        - Respuesta directa al inicio
        - Detalles y contexto específico
        - Ejemplos concretos cuando aplique
        - Referencias a proyectos o experiencias relevantes
        """
    
    def _get_classification_prompt(self) -> str:
        """Prompt para clasificación de consultas"""
        return """
        Clasifica la siguiente consulta sobre el CV profesional según estos criterios:

        ## Categorías:
        - **BASIC**: Información general, datos básicos, contacto
        - **TECHNICAL**: Tecnologías específicas, arquitecturas, proyectos técnicos
        - **EXPERIENCE**: Experiencia laboral, roles, responsabilidades
        - **PROJECTS**: Detalles de proyectos específicos, logros, resultados
        - **COMPLEX**: Consultas que requieren análisis combinado

        ## Herramientas recomendadas:
        - **FAQ**: Para consultas básicas y rápidas
        - **RAG**: Para detalles específicos de proyectos y experiencia
        - **COMBINED**: Para consultas complejas o multifacéticas

        Responde en JSON con la estructura:
        {
            "category": "CATEGORIA",
            "confidence": 85,
            "recommended_tool": "HERRAMIENTA",
            "reasoning": "explicación breve",
            "search_terms": ["término1", "término2"],
            "expected_complexity": "LOW|MEDIUM|HIGH"
        }

        Consulta a clasificar: {query}
        """
    
    def _get_planning_prompt(self) -> str:
        """Prompt para planificación de respuestas"""
        return """
        Planifica la estrategia para responder la siguiente consulta:

        ## Información disponible:
        - Clasificación: {classification}
        - Herramientas disponibles: {available_tools}
        - Contexto previo: {context}

        ## Genera un plan que incluya:
        1. **Estrategia**: Qué herramientas usar y en qué orden
        2. **Términos de búsqueda**: Palabras clave optimizadas
        3. **Filtros**: Qué tipo de información priorizar
        4. **Validación**: Cómo verificar la calidad de la respuesta

        Consulta: {query}
        """
    
    def _get_evaluation_prompt(self) -> str:
        """Prompt para evaluación de respuestas"""
        return """
        Evalúa la calidad de la siguiente respuesta sobre el CV profesional:

        ## Criterios de Evaluación (0-10):
        1. **Precisión** (30%): Información correcta y respaldada
        2. **Completitud** (25%): Respuesta completa y detallada
        3. **Relevancia** (20%): Directamente relacionada con la consulta
        4. **Claridad** (15%): Fácil de entender y bien estructurada
        5. **Profesionalismo** (10%): Tono y presentación apropiados

        ## Responde en JSON:
        {
            "overall_score": 8.5,
            "scores": {
                "precision": 9.0,
                "completeness": 8.0,
                "relevance": 9.0,
                "clarity": 8.5,
                "professionalism": 8.0
            },
            "confidence": 85,
            "strengths": ["punto fuerte 1", "punto fuerte 2"],
            "weaknesses": ["área de mejora 1"],
            "suggestions": ["sugerencia 1", "sugerencia 2"]
        }

        Consulta original: {query}
        Respuesta a evaluar: {response}
        Contexto usado: {context}
        """
    
    def _get_clarification_prompt(self) -> str:
        """Prompt para preguntas de aclaración"""
        return """
        Genera EXACTAMENTE 3 preguntas de aclaración para refinar esta consulta sobre el CV profesional.

        ## Criterios para las preguntas:
        - Específicas y actionables
        - Relevantes para la experiencia profesional
        - Que ayuden a dar respuestas más precisas
        - Cortas y directas

        ## Responde en JSON:
        {
            "questions": [
                "¿Te interesa algún sector específico como fintech o e-commerce?",
                "¿Buscas información sobre tecnologías específicas o arquitectura general?",
                "¿Prefieres ejemplos de proyectos recientes o experiencia general?"
            ]
        }

        Consulta original: {query}
        """
    
    def _get_email_prompt(self) -> str:
        """Prompt para generación de emails"""
        return """
        Genera un email profesional con el resumen de la consulta y respuesta del agente CV.

        ## Estructura del email:
        - **Asunto**: Claro y profesional
        - **Saludo**: Formal pero amigable
        - **Resumen**: Consulta realizada
        - **Respuesta**: Información proporcionada (resumida)
        - **Próximos pasos**: Si aplica
        - **Cierre**: Profesional

        ## Datos:
        - Consulta: {query}
        - Respuesta: {response}
        - Fecha: {timestamp}
        - Destinatario: {recipient}
        """
    
    def _get_error_prompt(self) -> str:
        """Prompt para manejo de errores"""
        return """
        Se ha producido un error al procesar la consulta sobre el CV profesional.

        ## Información del error:
        - Tipo: {error_type}
        - Mensaje: {error_message}
        - Consulta original: {query}

        ## Genera una respuesta que:
        1. Reconozca el problema de manera profesional
        2. Ofrezca alternativas cuando sea posible
        3. Proporcione información útil relacionada
        4. Mantenga un tono positivo y servicial

        ## Ejemplo de respuesta:
        "Disculpa, he tenido dificultades técnicas para procesar tu consulta específica sobre [tema]. 
        Sin embargo, puedo ayudarte con información general sobre [área relacionada]..."
        """
    
    def get_prompt(self, prompt_type: PromptType, **kwargs) -> str:
        """
        Obtener prompt formateado
        
        Args:
            prompt_type: Tipo de prompt
            **kwargs: Variables para formatear el prompt
            
        Returns:
            Prompt formateado
        """
        if prompt_type not in PromptType:
            raise ValueError(f"Tipo de prompt no válido: {prompt_type}")
        
        prompt_template = self.prompts[prompt_type.value]
        
        try:
            return prompt_template.format(**kwargs)
        except KeyError as e:
            raise ValueError(f"Variable requerida faltante en el prompt: {e}")
    
    def format_system_prompt(self, tools_available: List[str] = None) -> str:
        """Formatear prompt del sistema con herramientas disponibles"""
        base_prompt = self.get_prompt(PromptType.SYSTEM)
        
        if tools_available:
            tools_section = "\n\n## Herramientas Disponibles:\n"
            for tool in tools_available:
                tools_section += f"- {tool}\n"
            return base_prompt + tools_section
        
        return base_prompt
    
    def format_classification_prompt(self, query: str) -> str:
        """Formatear prompt de clasificación"""
        return self.get_prompt(PromptType.CLASSIFICATION, query=query)
    
    def format_planning_prompt(self, query: str, classification: dict, 
                             available_tools: List[str], context: str = "") -> str:
        """Formatear prompt de planificación"""
        return self.get_prompt(
            PromptType.PLANNING,
            query=query,
            classification=json.dumps(classification, indent=2),
            available_tools=", ".join(available_tools),
            context=context
        )
    
    def format_evaluation_prompt(self, query: str, response: str, context: str = "") -> str:
        """Formatear prompt de evaluación"""
        return self.get_prompt(
            PromptType.EVALUATION,
            query=query,
            response=response,
            context=context
        )
    
    def format_clarification_prompt(self, query: str) -> str:
        """Formatear prompt de aclaración"""
        return self.get_prompt(PromptType.CLARIFICATION, query=query)
    
    def format_email_prompt(self, query: str, response: str, 
                          recipient: str = "", timestamp: str = None) -> str:
        """Formatear prompt de email"""
        if timestamp is None:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        return self.get_prompt(
            PromptType.EMAIL,
            query=query,
            response=response,
            recipient=recipient,
            timestamp=timestamp
        )
    
    def format_error_response(self, error_type: str, error_message: str, query: str) -> str:
        """Formatear respuesta de error"""
        return self.get_prompt(
            PromptType.ERROR,
            error_type=error_type,
            error_message=error_message,
            query=query
        )