"""
FastAPI Application - Configuración Principal

API REST principal para el agente de CV. Configuración limpia y modular.
"""

import os
import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

# Imports locales
from agent.orchestrator import CVOrchestrator
from agent.evaluator import ResponseEvaluator
from tools.notify import notification_manager

# Imports de módulos refactorizados
from api.dependencies import set_orchestrator, set_evaluator
from api.exceptions import http_exception_handler, general_exception_handler
from api.routes import chat_router, health_router, stats_router, notifications_router

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Gestión del ciclo de vida de la aplicación"""
    # Startup
    logger.info("Inicializando CV Agent API...")
    try:
        orchestrator = CVOrchestrator()
        evaluator = ResponseEvaluator()
        
        # Configurar dependencias globales
        set_orchestrator(orchestrator)
        set_evaluator(evaluator)
        
        logger.info("✅ Orquestador y evaluador inicializados correctamente")
        
        notification_manager.send_custom_notification(
            message="CV Agent API iniciada correctamente",
            title="🚀 API Status",
            priority=0
        )
        
    except Exception as e:
        logger.error(f"❌ Error inicializando componentes: {e}")
        raise
    
    yield
    
    # Shutdown
    logger.info("Cerrando CV Agent API...")
    try:
        if orchestrator:
            stats = orchestrator.get_session_stats()
            notification_manager.send_custom_notification(
                message=f"API cerrada. Total consultas: {stats['total_queries']}, Éxito: {stats['success_rate']:.1f}%",
                title="📊 API Shutdown Stats"
            )
    except Exception as e:
        logger.warning(f"Error en shutdown: {e}")

app = FastAPI(
    title="CV Agent API",
    description="API REST para el agente inteligente de CV",
    version="1.0.0",
    lifespan=lifespan
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Registrar rutas
app.include_router(health_router)
app.include_router(chat_router)
app.include_router(stats_router)
app.include_router(notifications_router)

# Registrar handlers de excepciones
app.add_exception_handler(HTTPException, http_exception_handler)
app.add_exception_handler(Exception, general_exception_handler)

def main():
    """Función principal para ejecutar la API"""
    import uvicorn
    
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", "8000"))
    debug = os.getenv("DEBUG", "false").lower() == "true"
    
    logger.info(f"Iniciando CV Agent API en {host}:{port}")
    
    uvicorn.run(
        "api.app:app",
        host=host,
        port=port,
        reload=debug,
        log_level="info"
    )

if __name__ == "__main__":
    main()