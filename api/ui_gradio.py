"""
Gradio UI Module

Interfaz web opcional usando Gradio para interactuar con el agente de CV
de manera visual y amigable.
"""

import os
import json
from typing import Dict, Any, List, Tuple, Optional
import logging
from datetime import datetime
from dotenv import load_dotenv

import gradio as gr
import requests

# Imports locales (para modo standalone)
try:
    from agent.orchestrator import CVOrchestrator
    from agent.evaluator import ResponseEvaluator
    STANDALONE_MODE = True
except ImportError:
    STANDALONE_MODE = False

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

# ==================== Configuration ====================

API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")
GRADIO_PORT = int(os.getenv("GRADIO_PORT", "7860"))
GRADIO_SHARE = os.getenv("GRADIO_SHARE", "false").lower() == "true"

# ==================== Gradio Interface Class ====================

class CVAgentUI:
    """Interfaz Gradio para el agente de CV"""
    
    def __init__(self, use_api: bool = True):
        """
        Inicializar interfaz
        
        Args:
            use_api: Si usar API REST o componentes directos
        """
        self.use_api = use_api
        self.chat_history = []
        self.session_id = f"gradio_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        if not use_api and STANDALONE_MODE:
            # Modo standalone - usar componentes directamente
            try:
                self.orchestrator = CVOrchestrator()
                self.evaluator = ResponseEvaluator()
                logger.info("Modo standalone inicializado")
            except Exception as e:
                logger.error(f"Error en modo standalone: {e}")
                self.use_api = True
        
        logger.info(f"UI inicializada - Modo: {'API' if self.use_api else 'Standalone'}")
    
    def chat_with_agent(
        self,
        message: str,
        history: List[List[str]],
        enable_evaluation: bool = False
    ) -> Tuple[str, List[List[str]], str]:
        """
        Chat con el agente
        
        Args:
            message: Mensaje del usuario
            history: Historial de chat
            enable_evaluation: Si evaluar la respuesta
            
        Returns:
            Tupla de (respuesta, historial_actualizado, metadata)
        """
        if not message.strip():
            return "", history, "❌ Mensaje vacío"
        
        try:
            if self.use_api:
                response_data = self._call_api(message, enable_evaluation)
            else:
                response_data = self._call_direct(message, enable_evaluation)
            
            if response_data.get("success", False):
                agent_response = response_data["response"]
                metadata = response_data.get("metadata", {})
                
                # Actualizar historial
                history.append([message, agent_response])
                
                # Formatear metadata
                metadata_text = self._format_metadata(metadata, response_data.get("evaluation"))
                
                return "", history, metadata_text
            else:
                error_msg = response_data.get("error", "Error desconocido")
                history.append([message, f"❌ Error: {error_msg}"])
                return "", history, f"❌ Error: {error_msg}"
        
        except Exception as e:
            logger.error(f"Error en chat: {e}")
            error_response = f"❌ Error procesando mensaje: {str(e)}"
            history.append([message, error_response])
            return "", history, error_response
    
    def _call_api(self, message: str, enable_evaluation: bool) -> Dict[str, Any]:
        """Llamar API REST"""
        try:
            payload = {
                "message": message,
                "session_id": self.session_id,
                "notify_important": True,
                "evaluate_response": enable_evaluation
            }
            
            response = requests.post(
                f"{API_BASE_URL}/chat",
                json=payload,
                timeout=30,
                headers={"Content-Type": "application/json"}
            )
            
            response.raise_for_status()
            return response.json()
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Error en API call: {e}")
            return {
                "success": False,
                "error": f"Error de conexión con API: {str(e)}"
            }
    
    def chat_with_clarification(
        self, 
        message: str, 
        history: List[List[str]]
    ) -> Tuple[str, List[List[str]], str]:
        """
        Chat con capacidad de clarificación automática
        
        Args:
            message: Mensaje del usuario
            history: Historial de chat
            
        Returns:
            Tupla con (entrada_limpia, historial_actualizado, metadata)
        """
        if not message.strip():
            return "", history, ""
        
        try:
            if self.use_api:
                # Llamar endpoint de clarificación
                payload = {
                    "message": message,
                    "session_id": self.session_id
                }
                
                response = requests.post(
                    f"{API_BASE_URL}/chat/clarify",
                    json=payload,
                    timeout=30,
                    headers={"Content-Type": "application/json"}
                )
                
                response.raise_for_status()
                response_data = response.json()
                
                if response_data["needs_clarification"]:
                    # Mostrar preguntas de aclaración
                    questions = response_data["clarifying_questions"]
                    clarification_text = "🤔 Para darte una mejor respuesta, ¿podrías aclarar:\n\n"
                    for i, question in enumerate(questions, 1):
                        clarification_text += f"{i}. {question}\n"
                    
                    history.append([message, clarification_text])
                    return "", history, f"🔍 Se generaron {len(questions)} preguntas de aclaración"
                else:
                    # Procesar normalmente
                    return self.chat(message, history, enable_evaluation=False)
            else:
                # Modo directo
                result = self.orchestrator.process_query_with_clarification(
                    query=message,
                    session_id=self.session_id,
                    enable_clarification=True
                )
                
                if result.get("needs_clarification", False):
                    questions = result.get("clarifying_questions", [])
                    clarification_text = "🤔 Para darte una mejor respuesta, ¿podrías aclarar:\n\n"
                    for i, question in enumerate(questions, 1):
                        clarification_text += f"{i}. {question}\n"
                    
                    history.append([message, clarification_text])
                    return "", history, f"🔍 Se generaron {len(questions)} preguntas de aclaración"
                else:
                    # Si no necesita clarificación, procesar normalmente
                    return self.chat(message, history, enable_evaluation=False)
        
        except Exception as e:
            logger.error(f"Error en chat con clarificación: {e}")
            error_response = f"❌ Error procesando con clarificación: {str(e)}"
            history.append([message, error_response])
            return "", history, error_response

    def _call_direct(self, message: str, enable_evaluation: bool) -> Dict[str, Any]:
        """Llamar componentes directamente"""
        try:
            # Procesar con orquestador
            result = self.orchestrator.process_query(
                query=message,
                session_id=self.session_id,
                notify_important=True
            )
            
            # Evaluación opcional
            evaluation_result = None
            if enable_evaluation and result["success"]:
                try:
                    evaluation = self.evaluator.evaluate_response(
                        original_query=message,
                        response=result["response"],
                        context_used="",  # Simplificado para UI
                        metadata=result["metadata"]
                    )
                    evaluation_result = evaluation.to_dict()
                except Exception as e:
                    logger.warning(f"Error en evaluación: {e}")
            
            return {
                **result,
                "evaluation": evaluation_result,
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error en llamada directa: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def _format_metadata(
        self,
        metadata: Dict[str, Any],
        evaluation: Optional[Dict[str, Any]] = None
    ) -> str:
        """Formatear metadata para mostrar en UI"""
        formatted_parts = []
        
        # Información básica
        if "processing_time" in metadata:
            formatted_parts.append(f"⏱️ Tiempo: {metadata['processing_time']:.2f}s")
        
        if "classification" in metadata:
            classification = metadata["classification"]
            formatted_parts.append(f"🏷️ Categoría: {classification.get('category', 'N/A')}")
            formatted_parts.append(f"🎯 Confianza: {classification.get('confidence', 0)}%")
        
        if "tools_used" in metadata:
            tools = ", ".join(metadata["tools_used"])
            formatted_parts.append(f"🔧 Herramientas: {tools}")
        
        # Evaluación
        if evaluation:
            formatted_parts.append(f"\n📊 **Evaluación:**")
            formatted_parts.append(f"• Score: {evaluation.get('overall_score', 0)}/100")
            formatted_parts.append(f"• Calidad: {'✅ Buena' if evaluation.get('overall_score', 0) >= 70 else '⚠️ Mejorable'}")
            
            if evaluation.get("strengths"):
                strengths = evaluation["strengths"][:2]  # Primeras 2
                formatted_parts.append(f"• Fortalezas: {', '.join(strengths)}")
            
            if evaluation.get("should_improve"):
                formatted_parts.append("• Recomendación: Mejorar respuesta")
        
        return "\n".join(formatted_parts) if formatted_parts else "ℹ️ Sin metadata disponible"
    
    def get_stats(self) -> str:
        """Obtener estadísticas del sistema"""
        try:
            if self.use_api:
                response = requests.get(f"{API_BASE_URL}/stats", timeout=10)
                response.raise_for_status()
                stats_data = response.json()
            else:
                session_stats = self.orchestrator.get_session_stats()
                evaluation_stats = self.evaluator.get_evaluation_stats()
                stats_data = {
                    "session_stats": session_stats,
                    "evaluation_stats": evaluation_stats
                }
            
            return self._format_stats(stats_data)
            
        except Exception as e:
            logger.error(f"Error obteniendo estadísticas: {e}")
            return f"❌ Error obteniendo estadísticas: {str(e)}"
    
    def _format_stats(self, stats_data: Dict[str, Any]) -> str:
        """Formatear estadísticas para mostrar"""
        formatted_parts = ["📊 **Estadísticas del Sistema**\n"]
        
        # Estadísticas de sesión
        if "session_stats" in stats_data:
            session = stats_data["session_stats"]
            formatted_parts.extend([
                "**Sesión Actual:**",
                f"• Total consultas: {session.get('total_queries', 0)}",
                f"• Búsquedas RAG: {session.get('rag_searches', 0)}",
                f"• Consultas FAQ: {session.get('faq_queries', 0)}",
                f"• Errores: {session.get('errors', 0)}",
                f"• Tasa de éxito: {session.get('success_rate', 0):.1f}%",
                f"• Tiempo promedio: {session.get('avg_processing_time', 0):.2f}s",
                ""
            ])
        
        # Estadísticas de evaluación
        if "evaluation_stats" in stats_data and stats_data["evaluation_stats"]:
            evaluation = stats_data["evaluation_stats"]
            formatted_parts.extend([
                "**Evaluaciones:**",
                f"• Total evaluaciones: {evaluation.get('total_evaluations', 0)}",
                f"• Score promedio: {evaluation.get('average_score', 0):.1f}/100",
                f"• Tasa de calidad: {evaluation.get('quality_rate', 0):.1f}%",
                f"• Mejoras sugeridas: {evaluation.get('improvement_rate', 0):.1f}%",
                ""
            ])
        
        # Estadísticas de notificaciones
        if "notification_stats" in stats_data:
            notifications = stats_data["notification_stats"]
            formatted_parts.extend([
                "**Notificaciones:**",
                f"• Total enviadas: {notifications.get('total_notifications', 0)}",
                f"• Tasa de éxito: {notifications.get('success_rate', 0):.1f}%",
            ])
        
        return "\n".join(formatted_parts)
    
    def clear_chat(self) -> Tuple[List, str]:
        """Limpiar historial de chat"""
        self.chat_history = []
        return [], "💬 Chat limpiado"
    
    def get_health_status(self) -> str:
        """Obtener estado de salud del sistema"""
        try:
            if self.use_api:
                response = requests.get(f"{API_BASE_URL}/health", timeout=5)
                response.raise_for_status()
                health_data = response.json()
                
                status = health_data.get("status", "unknown")
                components = health_data.get("components", {})
                
                status_icon = "✅" if status == "healthy" else "⚠️" if status == "degraded" else "❌"
                formatted_status = f"{status_icon} **Estado: {status.upper()}**\n\n"
                
                formatted_status += "**Componentes:**\n"
                for component, comp_status in components.items():
                    comp_icon = "✅" if comp_status == "healthy" else "❌"
                    formatted_status += f"• {component}: {comp_icon} {comp_status}\n"
                
                return formatted_status
            else:
                # En modo standalone, verificar componentes directamente
                return "✅ **Estado: HEALTHY** (Modo Standalone)\n\n**Componentes:**\n• Orquestador: ✅ healthy\n• Evaluador: ✅ healthy"
        
        except Exception as e:
            return f"❌ **Estado: ERROR**\n\nError verificando estado: {str(e)}"

# ==================== Gradio Interface ====================

def create_gradio_interface() -> gr.Blocks:
    """Crear interfaz Gradio"""
    
    # Inicializar UI en modo API
    ui = CVAgentUI(use_api=True)
    
    # Definir interfaz
    with gr.Blocks(
        title="CV Agent - Asistente Inteligente",
        theme=gr.themes.Soft(),
        css="""
        .container { max-width: 1200px; margin: auto; }
        .chat-container { height: 500px; }
        .metadata-box { background-color: #f5f5f5; padding: 10px; border-radius: 5px; }
        """
    ) as interface:
        
        gr.Markdown("""
        # 🤖 CV Agent - Asistente Inteligente
        
        Asistente de IA especializado en responder preguntas sobre experiencia profesional, 
        proyectos y competencias técnicas usando RAG y bases de conocimiento.
        """)
        
        with gr.Row():
            with gr.Column(scale=2):
                # Chat principal
                with gr.Group():
                    gr.Markdown("### 💬 Chat con el Agente")
                    
                    chatbot = gr.Chatbot(
                        label="Conversación",
                        height=400,
                        show_label=False,
                        container=True
                    )
                    
                    with gr.Row():
                        msg_input = gr.Textbox(
                            placeholder="Escribe tu pregunta aquí... (ej: '¿Cuáles son mis principales proyectos?')",
                            label="Tu pregunta",
                            lines=2,
                            scale=4
                        )
                        
                        with gr.Column(scale=1):
                            send_btn = gr.Button("Enviar", variant="primary")
                            clarify_btn = gr.Button("🤔 Con Clarificación", variant="secondary")
                            clear_btn = gr.Button("Limpiar", variant="secondary")
                    
                    enable_eval = gr.Checkbox(
                        label="Evaluar respuesta automáticamente",
                        value=False,
                        info="Incluir evaluación de calidad de la respuesta"
                    )
            
            with gr.Column(scale=1):
                # Panel de información
                with gr.Group():
                    gr.Markdown("### 📊 Información del Sistema")
                    
                    metadata_display = gr.Textbox(
                        label="Metadata de la última respuesta",
                        lines=8,
                        interactive=False,
                        placeholder="Aquí aparecerá información sobre la última consulta..."
                    )
                    
                    with gr.Row():
                        stats_btn = gr.Button("Ver Estadísticas", size="sm")
                        health_btn = gr.Button("Estado Sistema", size="sm")
                    
                    info_display = gr.Textbox(
                        label="Información del sistema",
                        lines=10,
                        interactive=False,
                        placeholder="Haz clic en los botones para ver información..."
                    )
        
        # Ejemplos de consultas
        with gr.Row():
            gr.Markdown("### 💡 Ejemplos de Consultas")
            
            examples = gr.Examples(
                examples=[
                    ["¿Cuáles son mis principales tecnologías?"],
                    ["Cuéntame sobre el proyecto de banca digital"],
                    ["¿Qué certificaciones tengo?"],
                    ["¿Cuál es mi experiencia en microservicios?"],
                    ["¿En qué sectores he trabajado?"],
                    ["¿Qué metodologías de trabajo domino?"]
                ],
                inputs=msg_input,
                label="Haz clic en cualquier ejemplo:"
            )
        
        # Footer con información
        gr.Markdown("""
        ---
        **Instrucciones:**
        - Escribe preguntas naturales sobre experiencia profesional, proyectos o tecnologías
        - El agente buscará en documentos y FAQs para dar respuestas precisas
        - Usa la evaluación automática para obtener feedback sobre la calidad de las respuestas
        - Revisa las estadísticas y estado del sistema en el panel lateral
        
        **Ejemplos de preguntas efectivas:**
        - "¿Qué experiencia tienes con AWS?"
        - "Describe el proyecto más complejo que has liderado"
        - "¿Cuáles son tus fortalezas como arquitecto?"
        """)
        
        # Event handlers
        def submit_message(message, history, evaluation):
            return ui.chat_with_agent(message, history, evaluation)
        
        def submit_with_clarification(message, history):
            return ui.chat_with_clarification(message, history)
        
        def clear_conversation():
            return ui.clear_chat()
        
        def get_system_stats():
            return ui.get_stats()
        
        def get_system_health():
            return ui.get_health_status()
        
        # Conectar eventos
        send_btn.click(
            fn=submit_message,
            inputs=[msg_input, chatbot, enable_eval],
            outputs=[msg_input, chatbot, metadata_display]
        )
        
        msg_input.submit(
            fn=submit_message,
            inputs=[msg_input, chatbot, enable_eval],
            outputs=[msg_input, chatbot, metadata_display]
        )
        
        clarify_btn.click(
            fn=submit_with_clarification,
            inputs=[msg_input, chatbot],
            outputs=[msg_input, chatbot, metadata_display]
        )
        
        clear_btn.click(
            fn=clear_conversation,
            outputs=[chatbot, metadata_display]
        )
        
        stats_btn.click(
            fn=get_system_stats,
            outputs=info_display
        )
        
        health_btn.click(
            fn=get_system_health,
            outputs=info_display
        )
    
    return interface

# ==================== Main Functions ====================

def launch_gradio_ui():
    """Lanzar interfaz Gradio"""
    try:
        logger.info("Iniciando interfaz Gradio...")
        
        interface = create_gradio_interface()
        
        interface.launch(
            server_name="127.0.0.1",
            server_port=GRADIO_PORT,
            share=GRADIO_SHARE,
            show_error=True,
            quiet=False,
            prevent_thread_lock=False
        )
        
    except Exception as e:
        logger.error(f"Error lanzando interfaz Gradio: {e}")
        raise

def main():
    """Función principal"""
    print("=" * 60)
    print("🚀 CV Agent - Interfaz Web Gradio")
    print("=" * 60)
    print(f"Puerto: {GRADIO_PORT}")
    print(f"Modo API: {not STANDALONE_MODE}")
    print(f"Compartir públicamente: {GRADIO_SHARE}")
    
    if not STANDALONE_MODE:
        print(f"URL de API: {API_BASE_URL}")
        print("\n⚠️  Asegúrate de que la API esté ejecutándose antes de usar la interfaz")
    
    print("\n🌐 La interfaz estará disponible en:")
    print(f"   Local: http://localhost:{GRADIO_PORT}")
    
    if GRADIO_SHARE:
        print("   Público: Se generará URL pública automáticamente")
    
    print("\nPresiona Ctrl+C para detener\n")
    
    launch_gradio_ui()

if __name__ == "__main__":
    main()