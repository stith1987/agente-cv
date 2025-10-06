"""
Enhanced Gradio UI Module with Multi-LLM Provider Selection

Interfaz web mejorada que permite seleccionar el proveedor LLM
en tiempo real (OpenAI, DeepSeek, Groq, Ollama, etc.)
"""

import os
import json
from typing import Dict, Any, List, Tuple, Optional
import logging
from datetime import datetime
from dotenv import load_dotenv

import gradio as gr
import requests

# Imports locales
try:
    from agent.core.orchestrator import CVOrchestrator
    from agent.utils.config import AgentConfig, OpenAIConfig
    from agent.utils.multi_llm_client import LLMProvider, PROVIDER_ENDPOINTS
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

# Configuraciones de proveedores
PROVIDER_CONFIGS = {
    "OpenAI": {
        "provider": "openai",
        "models": ["gpt-4", "gpt-3.5-turbo", "gpt-4-turbo", "gpt-4o"],
        "env_key": "OPENAI_API_KEY",
        "base_url": None,
        "icon": "🤖"
    },
    "DeepSeek": {
        "provider": "deepseek",
        "models": ["deepseek-chat", "deepseek-coder"],
        "env_key": "DEEPSEEK_API_KEY",
        "base_url": "https://api.deepseek.com/v1",
        "icon": "🧠"
    },
    "Groq": {
        "provider": "groq",
        "models": ["mixtral-8x7b-32768", "llama-3.1-70b-versatile", "llama-3.1-8b-instant", "gemma-7b-it"],
        "env_key": "GROQ_API_KEY",
        "base_url": "https://api.groq.com/openai/v1",
        "icon": "⚡"
    },
    "Ollama": {
        "provider": "ollama",
        "models": ["llama3.1", "mistral", "codellama", "llama2"],
        "env_key": None,  # No requiere API key
        "base_url": "http://localhost:11434/v1",
        "icon": "🦙"
    }
}


class MultiLLMCVAgentUI:
    """Interfaz Gradio mejorada con selector de proveedor LLM"""
    
    def __init__(self, use_api: bool = False):
        """
        Inicializar interfaz
        
        Args:
            use_api: Si usar API REST o componentes directos
        """
        self.use_api = use_api
        self.chat_history = []
        self.session_id = f"gradio_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        self.current_orchestrator = None
        
        # Detectar proveedores disponibles
        self.available_providers = self._detect_available_providers()
        
        if not use_api and STANDALONE_MODE:
            # Modo standalone - crear orquestador con provider por defecto
            self._create_orchestrator("OpenAI", "gpt-3.5-turbo")
        
        logger.info(f"UI inicializada - Proveedores disponibles: {self.available_providers}")
    
    def _detect_available_providers(self) -> Dict[str, bool]:
        """Detectar qué proveedores están configurados"""
        available = {}
        for name, config in PROVIDER_CONFIGS.items():
            if config["env_key"]:
                api_key = os.getenv(config["env_key"]) or os.getenv("OPENAI_API_KEY")
                available[name] = bool(api_key)
            else:
                # Ollama no requiere API key
                available[name] = True
        return available
    
    def _create_orchestrator(self, provider_name: str, model: str) -> bool:
        """
        Crear nuevo orquestador con el proveedor seleccionado
        
        Args:
            provider_name: Nombre del proveedor
            model: Modelo a usar
            
        Returns:
            True si se creó exitosamente
        """
        try:
            provider_config = PROVIDER_CONFIGS[provider_name]
            
            # Obtener API key
            if provider_config["env_key"]:
                api_key = os.getenv(provider_config["env_key"]) or os.getenv("OPENAI_API_KEY")
            else:
                api_key = "ollama"  # Placeholder para Ollama
            
            if not api_key and provider_config["env_key"]:
                logger.error(f"API key no encontrada para {provider_name}")
                return False
            
            # Crear configuración
            openai_config = OpenAIConfig(
                api_key=api_key,
                model=model,
                provider=provider_config["provider"],
                base_url=provider_config["base_url"],
                temperature=0.7,
                max_tokens=2000
            )
            
            agent_config = AgentConfig(
                openai=openai_config,
                email=AgentConfig.from_env().email
            )
            
            # Crear orquestador
            self.current_orchestrator = CVOrchestrator(agent_config)
            
            logger.info(f"Orquestador creado con {provider_name}/{model}")
            return True
            
        except Exception as e:
            logger.error(f"Error creando orquestador: {e}")
            return False
    
    def change_provider(
        self, 
        provider_name: str, 
        model: str
    ) -> Tuple[str, str]:
        """
        Cambiar el proveedor LLM
        
        Args:
            provider_name: Nombre del proveedor
            model: Modelo a usar
            
        Returns:
            Tupla de (mensaje_estado, info_proveedor)
        """
        if not self.available_providers.get(provider_name, False):
            return (
                f"❌ {provider_name} no está configurado. Añade la API key en .env",
                f"Proveedor actual: No cambiado"
            )
        
        success = self._create_orchestrator(provider_name, model)
        
        if success:
            icon = PROVIDER_CONFIGS[provider_name]["icon"]
            base_url = PROVIDER_CONFIGS[provider_name]["base_url"] or "Default"
            
            status_msg = f"✅ Proveedor cambiado a {icon} {provider_name}"
            info_msg = f"""**Configuración Actual:**
- **Proveedor**: {icon} {provider_name}
- **Modelo**: {model}
- **Endpoint**: {base_url}
- **Estado**: Activo ✅
"""
            return status_msg, info_msg
        else:
            return (
                f"❌ Error cambiando a {provider_name}",
                "Verifica la configuración y logs"
            )
    
    def chat_with_agent(
        self,
        message: str,
        history: List[List[str]],
        enable_evaluation: bool = False
    ) -> Tuple[str, List[List[str]], str]:
        """Chat con el agente usando el proveedor seleccionado"""
        if not message.strip():
            return "", history, "❌ Mensaje vacío"
        
        if not self.current_orchestrator:
            return "", history, "❌ No hay orquestador configurado. Selecciona un proveedor primero."
        
        try:
            # Procesar consulta
            result = self.current_orchestrator.process_query(
                query=message,
                context={"session_id": self.session_id}
            )
            
            if result.get("success", False):
                agent_response = result["response"]
                metadata = result.get("metadata", {})
                
                # Actualizar historial
                history.append([message, agent_response])
                
                # Formatear metadata
                provider_info = f"""
**Proveedor**: {metadata.get('provider', 'N/A')}
**Modelo**: {metadata.get('model', 'N/A')}
**Fuentes**: {', '.join(metadata.get('tools_used', []))}
**Tiempo**: {metadata.get('processing_time', 0):.2f}s
**Contexto**: {metadata.get('context_length', 0)} chars
"""
                
                if enable_evaluation and result.get("evaluation"):
                    eval_data = result["evaluation"]
                    provider_info += f"\n**Evaluación**: {eval_data.get('overall_score', 0):.1f}/10"
                
                return "", history, provider_info
            else:
                error_msg = result.get("error", "Error desconocido")
                history.append([message, f"❌ Error: {error_msg}"])
                return "", history, f"❌ Error: {error_msg}"
                
        except Exception as e:
            logger.error(f"Error en chat: {e}")
            error_response = f"❌ Error: {str(e)}"
            history.append([message, error_response])
            return "", history, error_response
    
    def clear_chat(self) -> Tuple[List, str]:
        """Limpiar historial de chat"""
        self.chat_history = []
        return [], "Chat limpiado"
    
    def get_provider_status(self) -> str:
        """Obtener estado de todos los proveedores"""
        status = "### 📊 Estado de Proveedores\n\n"
        
        for name, config in PROVIDER_CONFIGS.items():
            icon = config["icon"]
            is_available = self.available_providers.get(name, False)
            status_icon = "✅" if is_available else "❌"
            
            status += f"{status_icon} {icon} **{name}**"
            
            if is_available:
                status += f" - {len(config['models'])} modelos disponibles\n"
            else:
                if config["env_key"]:
                    status += f" - Requiere `{config['env_key']}` en .env\n"
                else:
                    status += " - No configurado\n"
        
        return status


def create_multi_llm_gradio_interface() -> gr.Blocks:
    """Crear interfaz Gradio con selector de proveedor"""
    
    ui = MultiLLMCVAgentUI(use_api=False)
    
    with gr.Blocks(
        title="CV Agent - Multi-LLM",
        theme=gr.themes.Soft()
    ) as interface:
        
        gr.Markdown("""
        # 🤖 CV Agent - Multi-LLM Edition
        
        Asistente de IA con soporte para **múltiples proveedores LLM**
        
        Cambia entre OpenAI, DeepSeek, Groq, Ollama y más en tiempo real.
        """)
        
        # Selector de proveedor (arriba)
        with gr.Group():
            gr.Markdown("### ⚙️ Configuración de Proveedor LLM")
            
            with gr.Row():
                provider_dropdown = gr.Dropdown(
                    choices=list(PROVIDER_CONFIGS.keys()),
                    value="OpenAI",
                    label="Proveedor",
                    scale=2
                )
                
                model_dropdown = gr.Dropdown(
                    choices=PROVIDER_CONFIGS["OpenAI"]["models"],
                    value="gpt-3.5-turbo",
                    label="Modelo",
                    scale=2
                )
                
                change_btn = gr.Button("🔄 Aplicar", variant="primary", scale=1)
            
            with gr.Row():
                status_msg = gr.Textbox(
                    label="Estado",
                    value="👋 Selecciona un proveedor y modelo",
                    interactive=False,
                    scale=2
                )
                
                provider_info = gr.Markdown(
                    value="Selecciona un proveedor para comenzar",
                    scale=2
                )
        
        # Chat principal
        with gr.Row():
            with gr.Column(scale=2):
                with gr.Group():
                    gr.Markdown("### 💬 Chat")
                    
                    chatbot = gr.Chatbot(
                        label="Conversación",
                        height=400
                    )
                    
                    with gr.Row():
                        msg_input = gr.Textbox(
                            placeholder="Escribe tu pregunta aquí...",
                            label="Tu pregunta",
                            lines=2,
                            scale=4
                        )
                        
                        with gr.Column(scale=1):
                            send_btn = gr.Button("📤 Enviar", variant="primary")
                            clear_btn = gr.Button("🗑️ Limpiar")
                    
                    enable_eval = gr.Checkbox(
                        label="📊 Evaluar respuesta",
                        value=False
                    )
            
            with gr.Column(scale=1):
                with gr.Group():
                    gr.Markdown("### 📊 Información")
                    
                    metadata_display = gr.Textbox(
                        label="Metadata de respuesta",
                        lines=10,
                        interactive=False
                    )
                    
                    status_btn = gr.Button("Ver Estado de Proveedores")
                    
                    system_info = gr.Markdown(
                        value="Haz clic en el botón para ver el estado"
                    )
        
        # Ejemplos
        with gr.Row():
            gr.Examples(
                examples=[
                    ["¿Cuáles son mis principales tecnologías?"],
                    ["Describe el proyecto de banca digital"],
                    ["¿Qué experiencia tengo con microservicios?"],
                ],
                inputs=msg_input,
                label="💡 Ejemplos"
            )
        
        # Footer
        gr.Markdown("""
        ---
        ### 🎯 Proveedores Soportados
        
        - 🤖 **OpenAI**: GPT-4, GPT-3.5 (Máxima calidad)
        - 🧠 **DeepSeek**: deepseek-chat (99% más barato)
        - ⚡ **Groq**: Mixtral, Llama (Ultra rápido)
        - 🦙 **Ollama**: Modelos locales (Privado y gratis)
        
        **Tip**: Cambia de proveedor en tiempo real para comparar resultados
        """)
        
        # Event handlers
        def update_models(provider_name):
            """Actualizar lista de modelos según proveedor"""
            models = PROVIDER_CONFIGS[provider_name]["models"]
            return gr.Dropdown(choices=models, value=models[0])
        
        # Cambiar modelos cuando cambia el proveedor
        provider_dropdown.change(
            fn=update_models,
            inputs=provider_dropdown,
            outputs=model_dropdown
        )
        
        # Aplicar cambio de proveedor
        change_btn.click(
            fn=ui.change_provider,
            inputs=[provider_dropdown, model_dropdown],
            outputs=[status_msg, provider_info]
        )
        
        # Chat
        send_btn.click(
            fn=ui.chat_with_agent,
            inputs=[msg_input, chatbot, enable_eval],
            outputs=[msg_input, chatbot, metadata_display]
        )
        
        msg_input.submit(
            fn=ui.chat_with_agent,
            inputs=[msg_input, chatbot, enable_eval],
            outputs=[msg_input, chatbot, metadata_display]
        )
        
        clear_btn.click(
            fn=ui.clear_chat,
            outputs=[chatbot, metadata_display]
        )
        
        status_btn.click(
            fn=ui.get_provider_status,
            outputs=system_info
        )
    
    return interface


def main():
    """Función principal"""
    print("=" * 60)
    print("🚀 CV Agent - Multi-LLM Edition")
    print("=" * 60)
    print(f"Puerto: {GRADIO_PORT}")
    print(f"Modo: Standalone con Multi-LLM")
    print("\n🌐 La interfaz estará disponible en:")
    print(f"   http://localhost:{GRADIO_PORT}")
    print("\nPresiona Ctrl+C para detener\n")
    
    interface = create_multi_llm_gradio_interface()
    
    interface.launch(
        server_name="0.0.0.0",
        server_port=GRADIO_PORT,
        share=GRADIO_SHARE,
        show_error=True
    )


if __name__ == "__main__":
    main()
