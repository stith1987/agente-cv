"""
FastAPI Application

API REST principal para el agente de CV. Proporciona endpoints para
interactuar con el agente de manera programática.
"""

import os
import json
from typing import Dict, Any, List, Optional
import logging
from datetime import datetime
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, BackgroundTasks, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
import uvicorn
from dotenv import load_dotenv

# Imports locales
from agent.orchestrator import CVOrchestrator
from agent.evaluator import ResponseEvaluator
from tools.notify import notification_manager

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

# ==================== Global State ====================

# Variables globales para mantener estado
orchestrator: Optional[CVOrchestrator] = None
evaluator: Optional[ResponseEvaluator] = None

# ==================== Lifespan Management ====================

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Gestión del ciclo de vida de la aplicación"""
    global orchestrator, evaluator
    
    # Startup
    logger.info("Inicializando CV Agent API...")
    try:
        orchestrator = CVOrchestrator()
        evaluator = ResponseEvaluator()
        logger.info("✅ Orquestador y evaluador inicializados correctamente")
        
        # Notificar inicio
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
        # Enviar estadísticas finales
        if orchestrator:
            stats = orchestrator.get_session_stats()
            notification_manager.send_custom_notification(
                message=f"API cerrada. Total consultas: {stats['total_queries']}, Éxito: {stats['success_rate']:.1f}%",
                title="📊 API Shutdown Stats"
            )
    except Exception as e:
        logger.warning(f"Error en shutdown: {e}")

# ==================== Models ====================

class ChatRequest(BaseModel):
    """Modelo para requests de chat"""
    message: str = Field(
        description="Mensaje/consulta del usuario",
        min_length=3,
        max_length=1000
    )
    session_id: Optional[str] = Field(
        default="anonymous",
        description="ID de sesión del usuario"
    )
    notify_important: Optional[bool] = Field(
        default=True,
        description="Si enviar notificaciones para consultas importantes"
    )
    evaluate_response: Optional[bool] = Field(
        default=False,
        description="Si evaluar la respuesta automáticamente"
    )

class ChatResponse(BaseModel):
    """Modelo para respuestas de chat"""
    success: bool = Field(description="Si la consulta fue procesada exitosamente")
    response: str = Field(description="Respuesta del agente")
    metadata: Dict[str, Any] = Field(description="Metadata de la respuesta")
    evaluation: Optional[Dict[str, Any]] = Field(
        default=None,
        description="Evaluación de la respuesta (si se solicitó)"
    )
    timestamp: str = Field(description="Timestamp de la respuesta")

class HealthResponse(BaseModel):
    """Modelo para respuesta de health check"""
    status: str = Field(description="Estado del servicio")
    timestamp: str = Field(description="Timestamp del check")
    version: str = Field(description="Versión de la API")
    components: Dict[str, str] = Field(description="Estado de componentes")

class StatsResponse(BaseModel):
    """Modelo para respuesta de estadísticas"""
    session_stats: Dict[str, Any] = Field(description="Estadísticas de sesión")
    evaluation_stats: Optional[Dict[str, Any]] = Field(description="Estadísticas de evaluación")
    notification_stats: Dict[str, Any] = Field(description="Estadísticas de notificaciones")

# ==================== Dependency Injection ====================

def get_orchestrator() -> CVOrchestrator:
    """Dependency para obtener el orquestador"""
    if orchestrator is None:
        raise HTTPException(
            status_code=503,
            detail="Orquestador no inicializado"
        )
    return orchestrator

def get_evaluator() -> ResponseEvaluator:
    """Dependency para obtener el evaluador"""
    if evaluator is None:
        raise HTTPException(
            status_code=503,
            detail="Evaluador no inicializado"
        )
    return evaluator

# ==================== FastAPI App ====================

app = FastAPI(
    title="CV Agent API",
    description="API REST para el agente inteligente de CV",
    version="1.0.0",
    lifespan=lifespan
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, especificar origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==================== Endpoints ====================

@app.get("/", response_model=Dict[str, str])
async def root():
    """Endpoint raíz con información básica"""
    return {
        "message": "CV Agent API",
        "version": "1.0.0",
        "documentation": "/docs",
        "health": "/health"
    }

@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    components_status = {}
    
    # Verificar componentes
    try:
        if orchestrator:
            # Test básico del orquestador
            stats = orchestrator.get_session_stats()
            components_status["orchestrator"] = "healthy"
        else:
            components_status["orchestrator"] = "not_initialized"
    except Exception as e:
        components_status["orchestrator"] = f"error: {str(e)}"
    
    try:
        if evaluator:
            eval_stats = evaluator.get_evaluation_stats()
            components_status["evaluator"] = "healthy"
        else:
            components_status["evaluator"] = "not_initialized"
    except Exception as e:
        components_status["evaluator"] = f"error: {str(e)}"
    
    # Estado general
    all_healthy = all(status == "healthy" for status in components_status.values())
    overall_status = "healthy" if all_healthy else "degraded"
    
    return HealthResponse(
        status=overall_status,
        timestamp=datetime.now().isoformat(),
        version="1.0.0",
        components=components_status
    )

@app.post("/chat", response_model=ChatResponse)
async def chat(
    request: ChatRequest,
    background_tasks: BackgroundTasks,
    orchestrator: CVOrchestrator = Depends(get_orchestrator),
    evaluator: ResponseEvaluator = Depends(get_evaluator)
):
    """
    Endpoint principal de chat con el agente
    
    Procesa consultas del usuario y retorna respuestas inteligentes
    usando RAG, FAQ y otras herramientas disponibles.
    """
    try:
        logger.info(f"Nueva consulta de {request.session_id}: {request.message[:50]}...")
        
        # Procesar consulta con el orquestador
        result = orchestrator.process_query(
            query=request.message,
            session_id=request.session_id,
            notify_important=request.notify_important
        )
        
        response_data = {
            "success": result["success"],
            "response": result["response"],
            "metadata": result["metadata"],
            "timestamp": datetime.now().isoformat()
        }
        
        # Evaluación opcional
        evaluation_result = None
        if request.evaluate_response and result["success"]:
            try:
                evaluation = evaluator.evaluate_response(
                    original_query=request.message,
                    response=result["response"],
                    context_used=result.get("tool_results", {}).get("combined", {}).get("combined_summary", ""),
                    metadata=result["metadata"]
                )
                evaluation_result = evaluation.to_dict()
                
                # Si la evaluación sugiere mejoras, programar auto-crítica en background
                if evaluation.should_improve:
                    background_tasks.add_task(
                        perform_self_critique,
                        request.message,
                        result["response"],
                        result["metadata"].get("tools_used", [])
                    )
                
            except Exception as e:
                logger.warning(f"Error en evaluación: {e}")
                evaluation_result = {"error": str(e)}
        
        response_data["evaluation"] = evaluation_result
        
        return ChatResponse(**response_data)
        
    except Exception as e:
        logger.error(f"Error en endpoint /chat: {e}")
        
        # Notificar error crítico
        try:
            notification_manager.send_error_notification(
                error_message=str(e),
                context={
                    "endpoint": "/chat",
                    "session_id": request.session_id,
                    "query": request.message
                }
            )
        except:
            pass  # No fallar si la notificación falla
        
        raise HTTPException(
            status_code=500,
            detail=f"Error procesando consulta: {str(e)}"
        )

# ==================== Nuevos Endpoints Agentic ====================

class ClarificationRequest(BaseModel):
    """Modelo para solicitud de clarificación"""
    message: str = Field(description="Consulta del usuario")
    session_id: str = Field(default="anonymous", description="ID de sesión")

class ClarificationResponse(BaseModel):
    """Modelo para respuesta de clarificación"""
    needs_clarification: bool = Field(description="Si necesita clarificación")
    clarifying_questions: List[str] = Field(description="Preguntas de aclaración")
    original_query: str = Field(description="Consulta original")
    timestamp: str = Field(description="Timestamp")

@app.post("/chat/clarify", response_model=ClarificationResponse)
async def chat_with_clarification(
    request: ClarificationRequest,
    orchestrator: CVOrchestrator = Depends(get_orchestrator)
):
    """
    Endpoint de chat con capacidad de clarificación automática
    
    Analiza la consulta y genera preguntas de aclaración si es necesario
    antes de procesar la respuesta completa.
    """
    try:
        logger.info(f"Consulta con clarificación de {request.session_id}: {request.message[:50]}...")
        
        # Procesar con clarificación
        result = orchestrator.process_query_with_clarification(
            query=request.message,
            session_id=request.session_id,
            enable_clarification=True
        )
        
        if result.get("needs_clarification", False):
            return ClarificationResponse(
                needs_clarification=True,
                clarifying_questions=result.get("clarifying_questions", []),
                original_query=request.message,
                timestamp=datetime.now().isoformat()
            )
        else:
            # Si no necesita clarificación, devolver respuesta directa
            return ClarificationResponse(
                needs_clarification=False,
                clarifying_questions=[],
                original_query=request.message,
                timestamp=datetime.now().isoformat()
            )
        
    except Exception as e:
        logger.error(f"Error en endpoint /chat/clarify: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Error procesando clarificación: {str(e)}"
        )

class MultiQueryRequest(BaseModel):
    """Modelo para búsqueda multi-query"""
    queries: List[str] = Field(description="Lista de consultas refinadas")
    document_types: Optional[List[str]] = Field(default=None, description="Tipos de documentos")
    session_id: str = Field(default="anonymous", description="ID de sesión")

@app.post("/search/multi-query")
async def multi_query_search(
    request: MultiQueryRequest,
    orchestrator: CVOrchestrator = Depends(get_orchestrator)
):
    """
    Endpoint para búsqueda con múltiples consultas refinadas
    
    Ejecuta varias consultas y fusiona los resultados para mayor recall.
    """
    try:
        logger.info(f"Búsqueda multi-query con {len(request.queries)} consultas")
        
        result = orchestrator.multi_query_search(
            queries=request.queries,
            document_types=request.document_types
        )
        
        return {
            "success": result["success"],
            "results": [
                {
                    "content": r.content,
                    "score": r.score,
                    "metadata": r.metadata
                } for r in result.get("results", [])
            ],
            "total_found": result.get("total_found", 0),
            "queries_used": result.get("queries_used", []),
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Error en endpoint /search/multi-query: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Error en búsqueda multi-query: {str(e)}"
        )

@app.get("/stats", response_model=StatsResponse)
async def get_stats(
    orchestrator: CVOrchestrator = Depends(get_orchestrator),
    evaluator: ResponseEvaluator = Depends(get_evaluator)
):
    """Obtener estadísticas del sistema"""
    try:
        session_stats = orchestrator.get_session_stats()
        evaluation_stats = evaluator.get_evaluation_stats()
        notification_stats = notification_manager.get_notification_stats()
        
        return StatsResponse(
            session_stats=session_stats,
            evaluation_stats=evaluation_stats,
            notification_stats=notification_stats
        )
        
    except Exception as e:
        logger.error(f"Error obteniendo estadísticas: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Error obteniendo estadísticas: {str(e)}"
        )

@app.post("/evaluate")
async def evaluate_response(
    query: str,
    response: str,
    context: Optional[str] = None,
    evaluator: ResponseEvaluator = Depends(get_evaluator)
):
    """Endpoint para evaluar una respuesta específica"""
    try:
        evaluation = evaluator.evaluate_response(
            original_query=query,
            response=response,
            context_used=context or ""
        )
        
        return {
            "success": True,
            "evaluation": evaluation.to_dict(),
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Error en evaluación: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Error en evaluación: {str(e)}"
        )

@app.post("/notify")
async def send_notification(
    message: str,
    title: Optional[str] = None,
    priority: Optional[str] = "normal"
):
    """Endpoint para enviar notificaciones personalizadas"""
    try:
        result = notification_manager.send_custom_notification(
            message=message,
            title=title or "CV Agent Custom",
            priority=0 if priority == "normal" else 1 if priority == "high" else -1
        )
        
        return {
            "success": result.success,
            "message": result.message,
            "timestamp": result.timestamp.isoformat() if result.timestamp else None
        }
        
    except Exception as e:
        logger.error(f"Error enviando notificación: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Error enviando notificación: {str(e)}"
        )

# ==================== Background Tasks ====================

async def perform_self_critique(query: str, response: str, tools_used: List[str]):
    """Tarea en background para auto-crítica"""
    try:
        if evaluator:
            critique = evaluator.self_critique(
                original_query=query,
                response=response,
                tools_used=tools_used
            )
            logger.info(f"Auto-crítica completada para query: {query[:30]}...")
            
            # Si la auto-crítica identifica problemas serios, notificar
            if "error" in critique["critique_text"].lower() or "problema" in critique["critique_text"].lower():
                notification_manager.send_custom_notification(
                    message=f"Auto-crítica identificó posibles problemas en respuesta: {critique['critique_text'][:100]}...",
                    title="🔍 Auto-Critique Alert",
                    priority=0
                )
                
    except Exception as e:
        logger.error(f"Error en auto-crítica: {e}")

# ==================== Exception Handlers ====================

@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """Handler para excepciones HTTP"""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": True,
            "message": exc.detail,
            "status_code": exc.status_code,
            "timestamp": datetime.now().isoformat()
        }
    )

@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    """Handler para excepciones generales"""
    logger.error(f"Error no manejado: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={
            "error": True,
            "message": "Error interno del servidor",
            "timestamp": datetime.now().isoformat()
        }
    )

# ==================== Main ====================

def main():
    """Función principal para ejecutar la API"""
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