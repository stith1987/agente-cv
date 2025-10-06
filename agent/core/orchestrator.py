"""
Orchestrator Module

Orquestador principal refactorizado que gestiona la lógica de negocio,
coordina agentes especializados y proporciona respuestas inteligentes.
"""

import time
from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime
from openai import OpenAI

# Imports locales
from rag.retriever import SemanticRetriever
from tools.faq_sql import FAQSQLTool
from tools.notify import NotificationManager

from ..utils.config import AgentConfig
from ..utils.logger import AgentLogger
from ..utils.prompts import PromptManager
from ..utils.multi_llm_client import MultiLLMClient
from .query_classifier import QueryClassifier, QueryClassification, RecommendedTool
from .response_evaluator import ResponseEvaluator, EvaluationResult
from ..specialists.clarifier import ClarifierAgent
from ..specialists.email_handler import EmailAgent


class CVOrchestrator:
    """Orquestador principal del sistema de agentes de CV"""
    
    def __init__(self, config: Optional[AgentConfig] = None):
        """
        Inicializar orquestador
        
        Args:
            config: Configuración del agente, si no se proporciona se carga desde env
        """
        # Configuración
        self.config = config or AgentConfig.from_env()
        self.logger = AgentLogger("cv_orchestrator", 
                                self.config.log_level,
                                self.config.log_to_file,
                                self.config.log_file_path)
        
        # Managers
        self.prompt_manager = PromptManager()
        
        # Cliente Multi-LLM (compatible con OpenAI y otros proveedores)
        self.llm_client = MultiLLMClient(self.config.openai, self.logger)
        # Mantener compatibilidad con código legacy
        self.openai_client = self.llm_client.client
        
        # Inicializar componentes principales
        self._initialize_tools()
        self._initialize_agents()
        
        # Estadísticas de sesión
        self.session_stats = {
            "total_queries": 0,
            "successful_queries": 0,
            "failed_queries": 0,
            "rag_searches": 0,
            "faq_queries": 0,
            "combined_searches": 0,
            "clarifications_requested": 0,
            "emails_sent": 0,
            "start_time": datetime.now(),
            "average_response_time": 0.0
        }
        
        # Log de consultas para análisis
        self.query_log = []
        
        # Metadata del último LLM usado (para incluir en respuestas)
        self._last_llm_metadata = {}
        
        self.logger.info("CVOrchestrator initialized successfully")
    
    def _initialize_tools(self):
        """Inicializar herramientas del sistema"""
        try:
            self.retriever = SemanticRetriever()
            self.faq_tool = FAQSQLTool()
            self.notification_manager = NotificationManager()
            
            self.logger.info("Tools initialized successfully")
        except Exception as e:
            self.logger.error("Error initializing tools", exception=e)
            raise
    
    def _initialize_agents(self):
        """Inicializar agentes especializados"""
        try:
            self.query_classifier = QueryClassifier(self.config, self.logger)
            self.response_evaluator = ResponseEvaluator(self.config, self.logger)
            self.clarifier_agent = ClarifierAgent(self.config, self.logger)
            self.email_agent = EmailAgent(self.config, self.logger)
            
            self.logger.info("Specialized agents initialized successfully")
        except Exception as e:
            self.logger.error("Error initializing agents", exception=e)
            raise
    
    def process_query(self, 
                     query: str, 
                     context: Optional[Dict[str, Any]] = None,
                     user_preferences: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Procesar consulta principal
        
        Args:
            query: Consulta del usuario
            context: Contexto adicional de la conversación
            user_preferences: Preferencias del usuario
            
        Returns:
            Respuesta completa con metadatos
        """
        start_time = time.time()
        context = context or {}
        user_preferences = user_preferences or {}
        
        try:
            self.logger.info(f"Processing query: {query[:100]}...")
            
            # 1. Clasificar consulta
            classification = self.query_classifier.classify(query, context)
            self.logger.debug(f"Query classified as: {classification.category.value}")
            
            # 2. Determinar estrategia de respuesta
            response_strategy = self._determine_response_strategy(classification, user_preferences)
            
            # 3. Ejecutar estrategia
            response_data = self._execute_response_strategy(query, classification, response_strategy, context)
            
            # 4. Evaluar respuesta
            evaluation = self.response_evaluator.evaluate_response(
                query=query,
                response=response_data["response"],
                context=response_data.get("context", ""),
                metadata=response_data.get("metadata", {})
            )
            
            # 5. Post-procesamiento
            final_response = self._post_process_response(
                query, response_data, evaluation, classification
            )
            
            # 6. Actualizar estadísticas
            execution_time = time.time() - start_time
            self._update_session_stats(classification, execution_time, True)
            
            # 7. Log de la consulta
            self._log_query(query, final_response, classification, evaluation, execution_time)
            
            self.logger.log_query(query, classification.category.value, execution_time, True)
            
            return final_response
            
        except Exception as e:
            execution_time = time.time() - start_time
            self.logger.error("Error processing query", exception=e)
            
            # Respuesta de error
            error_response = self._generate_error_response(query, str(e))
            self._update_session_stats(None, execution_time, False)
            
            return error_response
    
    def _determine_response_strategy(self, 
                                   classification: QueryClassification,
                                   user_preferences: Dict[str, Any]) -> Dict[str, Any]:
        """Determinar estrategia de respuesta basada en clasificación"""
        strategy = {
            "primary_tool": classification.recommended_tool,
            "fallback_tools": [],
            "needs_clarification": classification.needs_clarification(),
            "complexity": classification.expected_complexity,
            "search_params": {
                "terms": classification.search_terms,
                "top_k": user_preferences.get("detail_level", self.config.rag_top_k),
                "similarity_threshold": self.config.rag_similarity_threshold
            }
        }
        
        # Agregar herramientas de fallback basadas en la clasificación
        if classification.recommended_tool == RecommendedTool.RAG:
            strategy["fallback_tools"].append(RecommendedTool.FAQ)
        elif classification.recommended_tool == RecommendedTool.FAQ:
            strategy["fallback_tools"].append(RecommendedTool.RAG)
        
        return strategy
    
    def _execute_response_strategy(self, 
                                 query: str,
                                 classification: QueryClassification,
                                 strategy: Dict[str, Any],
                                 context: Dict[str, Any]) -> Dict[str, Any]:
        """Ejecutar la estrategia de respuesta seleccionada"""
        
        # Si necesita aclaración, generar preguntas
        if strategy["needs_clarification"]:
            return self._handle_clarification_request(query, classification)
        
        # Ejecutar herramienta principal
        primary_tool = strategy["primary_tool"]
        
        if primary_tool == RecommendedTool.RAG:
            return self._execute_rag_search(query, strategy["search_params"])
        elif primary_tool == RecommendedTool.FAQ:
            return self._execute_faq_query(query)
        elif primary_tool == RecommendedTool.COMBINED:
            return self._execute_combined_search(query, strategy["search_params"])
        else:
            # Fallback a búsqueda combinada
            return self._execute_combined_search(query, strategy["search_params"])
    
    def _execute_rag_search(self, query: str, search_params: Dict[str, Any]) -> Dict[str, Any]:
        """Ejecutar búsqueda RAG"""
        try:
            results = self.retriever.search(
                query=query,
                top_k=search_params["top_k"]
            )
            
            if not results:
                return self._handle_no_results(query, "RAG")
            
            # Generar respuesta con contexto
            context = self._format_rag_context(results)
            response = self._generate_response_with_context(query, context, "RAG")
            
            self.session_stats["rag_searches"] += 1
            
            return {
                "response": response,
                "context": context,
                "source": "RAG",
                "metadata": {
                    "results_count": len(results),
                    "tools_used": ["rag_search"],
                    "search_params": search_params,
                    # Agregar metadata del LLM usado
                    **self._last_llm_metadata
                }
            }
            
        except Exception as e:
            self.logger.error("Error in RAG search", exception=e)
            return self._handle_tool_error(query, "RAG", str(e))
    
    def _execute_faq_query(self, query: str) -> Dict[str, Any]:
        """Ejecutar consulta FAQ"""
        try:
            results = self.faq_tool.query(query, limit=self.config.faq_limit)
            
            if not results:
                return self._handle_no_results(query, "FAQ")
            
            # Formatear respuesta FAQ
            response = self._format_faq_response(results)
            
            self.session_stats["faq_queries"] += 1
            
            return {
                "response": response,
                "context": str(results),
                "source": "FAQ",
                "metadata": {
                    "results_count": len(results),
                    "tools_used": ["faq_query"],
                    # Agregar metadata del LLM usado
                    **self._last_llm_metadata
                }
            }
            
        except Exception as e:
            self.logger.error("Error in FAQ query", exception=e)
            return self._handle_tool_error(query, "FAQ", str(e))
    
    def _execute_combined_search(self, query: str, search_params: Dict[str, Any]) -> Dict[str, Any]:
        """Ejecutar búsqueda combinada RAG + FAQ"""
        try:
            # Ejecutar ambas búsquedas en paralelo
            rag_results = self.retriever.search(
                query=query,
                top_k=search_params["top_k"] // 2  # Dividir espacio
            )
            
            faq_results = self.faq_tool.query(query, limit=self.config.faq_limit // 2)
            
            # Combinar resultados
            combined_context = self._combine_search_results(rag_results, faq_results)
            
            if not combined_context:
                return self._handle_no_results(query, "COMBINED")
            
            # Generar respuesta combinada
            response = self._generate_response_with_context(query, combined_context, "COMBINED")
            
            self.session_stats["combined_searches"] += 1
            
            return {
                "response": response,
                "context": combined_context,
                "source": "COMBINED",
                "metadata": {
                    "rag_results": len(rag_results) if rag_results else 0,
                    "faq_results": len(faq_results) if faq_results else 0,
                    "tools_used": ["rag_search", "faq_query"],
                    # Agregar metadata del LLM usado
                    **self._last_llm_metadata
                }
            }
            
        except Exception as e:
            self.logger.error("Error in combined search", exception=e)
            return self._handle_tool_error(query, "COMBINED", str(e))
    
    def _handle_clarification_request(self, query: str, classification: QueryClassification) -> Dict[str, Any]:
        """Manejar solicitud de aclaración"""
        try:
            clarification_questions = self.clarifier_agent.generate_clarifications(query)
            
            self.session_stats["clarifications_requested"] += 1
            
            return {
                "response": "Para poder ayudarte mejor, me gustaría hacer algunas preguntas de aclaración:",
                "clarification_questions": clarification_questions,
                "source": "CLARIFICATION",
                "metadata": {
                    "needs_clarification": True,
                    "classification": classification.to_dict(),
                    "tools_used": ["clarifier"]
                }
            }
            
        except Exception as e:
            self.logger.error("Error generating clarifications", exception=e)
            # Fallback a respuesta general
            return self._execute_combined_search(query, {"terms": [query], "top_k": 3, "similarity_threshold": 0.6})
    
    def _generate_response_with_context(self, query: str, context: str, source: str) -> str:
        """Generar respuesta usando contexto y LLM"""
        try:
            system_prompt = self.prompt_manager.format_system_prompt([source.lower()])
            
            user_prompt = f"""
            Consulta: {query}
            
            Contexto disponible:
            {context}
            
            Por favor, proporciona una respuesta completa y profesional basada en el contexto disponible.
            Si el contexto no es suficiente para responder completamente, indícalo claramente.
            """
            
            # Usar MultiLLMClient.generate() para capturar metadata
            llm_response = self.llm_client.generate(
                prompt=user_prompt,
                system_prompt=system_prompt,
                temperature=self.config.openai.temperature,
                max_tokens=self.config.openai.max_tokens
            )
            
            # Guardar metadata de la generación para usarlo en respuesta
            self._last_llm_metadata = {
                "provider": llm_response.provider,
                "model": llm_response.model,
                "tokens": llm_response.usage.total_tokens if llm_response.usage else None,
                "cost": llm_response.cost
            }
            
            return llm_response.content
            
        except Exception as e:
            self.logger.error("Error generating response with context", exception=e)
            return f"He encontrado información relevante pero tengo dificultades técnicas para procesarla completamente. Contexto disponible: {context[:200]}..."
    
    def _format_rag_context(self, results: List[Dict[str, Any]]) -> str:
        """Formatear resultados RAG en contexto"""
        if not results:
            return ""
        
        context_parts = []
        for i, result in enumerate(results[:5], 1):  # Limitar a 5 resultados
            content = result.get("content", "")
            source = result.get("source", "documento")
            similarity = result.get("similarity", 0)
            
            context_parts.append(f"[Fuente {i} - {source} (relevancia: {similarity:.2f})]:\n{content}\n")
        
        return "\n".join(context_parts)
    
    def _format_faq_response(self, results: List[Dict[str, Any]]) -> str:
        """Formatear respuesta FAQ directa"""
        if not results:
            return "No encontré información específica en las preguntas frecuentes."
        
        # Tomar la respuesta con mayor puntuación
        best_result = max(results, key=lambda x: x.get("score", 0))
        return best_result.get("answer", "Respuesta no disponible")
    
    def _combine_search_results(self, rag_results: List[Dict], faq_results: List[Dict]) -> str:
        """Combinar resultados de RAG y FAQ"""
        context_parts = []
        
        # Agregar resultados FAQ primero (más directos)
        if faq_results:
            context_parts.append("=== INFORMACIÓN GENERAL ===")
            for result in faq_results[:2]:
                context_parts.append(f"P: {result.get('question', '')}")
                context_parts.append(f"R: {result.get('answer', '')}\n")
        
        # Agregar resultados RAG (más detallados)
        if rag_results:
            context_parts.append("=== INFORMACIÓN DETALLADA ===")
            context_parts.append(self._format_rag_context(rag_results))
        
        return "\n".join(context_parts)
    
    def _handle_no_results(self, query: str, source: str) -> Dict[str, Any]:
        """Manejar caso sin resultados"""
        response = f"No encontré información específica para tu consulta en {source}. "
        response += "¿Podrías reformular la pregunta o ser más específico sobre qué aspecto te interesa?"
        
        return {
            "response": response,
            "context": "",
            "source": source,
            "metadata": {
                "no_results": True,
                "tools_used": [source.lower()],
                # Incluir metadata LLM si está disponible
                **self._last_llm_metadata
            }
        }
    
    def _handle_tool_error(self, query: str, tool: str, error_msg: str) -> Dict[str, Any]:
        """Manejar errores de herramientas"""
        response = f"Disculpa, he tenido dificultades técnicas con la herramienta {tool}. "
        response += "Intentemos con un enfoque diferente o intenta reformular tu consulta."
        
        return {
            "response": response,
            "context": "",
            "source": "ERROR",
            "metadata": {
                "error": True,
                "error_tool": tool,
                "error_message": error_msg,
                "tools_used": [],
                # Incluir metadata LLM si está disponible
                **self._last_llm_metadata
            }
        }
    
    def _post_process_response(self, 
                             query: str,
                             response_data: Dict[str, Any],
                             evaluation: EvaluationResult,
                             classification: QueryClassification) -> Dict[str, Any]:
        """Post-procesar respuesta final"""
        
        # Agregar información de evaluación
        response_data["evaluation"] = evaluation.to_dict()
        response_data["classification"] = classification.to_dict()
        
        # Enviar notificación si es necesario
        if self._should_send_notification(evaluation, classification):
            try:
                self.notification_manager.send_notification(
                    message=f"Consulta importante procesada: {query[:100]}",
                    title="Consulta CV Importante",
                    priority="normal"
                )
            except Exception as e:
                self.logger.warning("Failed to send notification", exception=e)
        
        # Agregar timestamp
        response_data["timestamp"] = datetime.now().isoformat()
        
        return response_data
    
    def _should_send_notification(self, evaluation: EvaluationResult, classification: QueryClassification) -> bool:
        """Determinar si se debe enviar notificación"""
        return (
            evaluation.scores.overall_score < 5.0 or  # Respuesta de baja calidad
            classification.expected_complexity.value == "HIGH" or  # Consulta compleja
            not evaluation.is_high_quality()  # No es de alta calidad
        )
    
    def _generate_error_response(self, query: str, error_msg: str) -> Dict[str, Any]:
        """Generar respuesta de error"""
        try:
            error_response = self.prompt_manager.format_error_response(
                error_type="ProcessingError",
                error_message=error_msg,
                query=query
            )
        except:
            error_response = "Disculpa, he tenido dificultades técnicas para procesar tu consulta. Por favor, intenta de nuevo más tarde."
        
        return {
            "response": error_response,
            "context": "",
            "source": "ERROR",
            "metadata": {
                "error": True,
                "error_message": error_msg,
                "tools_used": []
            },
            "timestamp": datetime.now().isoformat()
        }
    
    def _update_session_stats(self, classification: Optional[QueryClassification], 
                            execution_time: float, success: bool):
        """Actualizar estadísticas de sesión"""
        self.session_stats["total_queries"] += 1
        
        if success:
            self.session_stats["successful_queries"] += 1
        else:
            self.session_stats["failed_queries"] += 1
        
        # Actualizar tiempo promedio de respuesta
        total_queries = self.session_stats["total_queries"]
        current_avg = self.session_stats["average_response_time"]
        self.session_stats["average_response_time"] = ((current_avg * (total_queries - 1)) + execution_time) / total_queries
    
    def _log_query(self, query: str, response_data: Dict[str, Any], 
                  classification: QueryClassification, evaluation: EvaluationResult,
                  execution_time: float):
        """Registrar consulta en el log"""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "query": query,
            "classification": classification.to_dict(),
            "response_source": response_data.get("source", "UNKNOWN"),
            "evaluation_score": evaluation.scores.overall_score,
            "execution_time": execution_time,
            "success": True
        }
        
        self.query_log.append(log_entry)
        
        # Mantener solo las últimas 100 consultas
        if len(self.query_log) > 100:
            self.query_log = self.query_log[-100:]
    
    def get_session_stats(self) -> Dict[str, Any]:
        """Obtener estadísticas de la sesión"""
        return {
            **self.session_stats,
            "session_duration": str(datetime.now() - self.session_stats["start_time"]),
            "classifier_stats": self.query_classifier.get_stats(),
            "evaluator_stats": self.response_evaluator.get_stats()
        }
    
    def send_summary_email(self, recipient: Optional[str] = None) -> bool:
        """Enviar email con resumen de actividad"""
        try:
            if not self.config.email.is_configured():
                self.logger.warning("Email not configured, cannot send summary")
                return False
            
            recipient = recipient or self.config.email.default_recipient
            if not recipient:
                self.logger.warning("No recipient specified for summary email")
                return False
            
            # Generar resumen
            stats = self.get_session_stats()
            recent_queries = self.query_log[-5:] if len(self.query_log) >= 5 else self.query_log
            
            summary_content = f"""
            Resumen de Actividad del Agente CV
            
            Estadísticas de Sesión:
            - Total de consultas: {stats['total_queries']}
            - Consultas exitosas: {stats['successful_queries']}
            - Tiempo promedio de respuesta: {stats['average_response_time']:.2f}s
            
            Consultas Recientes:
            """
            
            for entry in recent_queries:
                summary_content += f"- {entry['query'][:50]}... (Score: {entry['evaluation_score']:.1f})\n"
            
            # Enviar email
            success = self.email_agent.send_summary_email(
                recipient=recipient,
                query="Resumen de Actividad",
                response=summary_content
            )
            
            if success:
                self.session_stats["emails_sent"] += 1
            
            return success
            
        except Exception as e:
            self.logger.error("Error sending summary email", exception=e)
            return False