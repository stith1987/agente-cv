"""
Endpoints relacionados con chat
"""

import logging
from datetime import datetime
from typing import Dict, Any, List

from fastapi import APIRouter, HTTPException, BackgroundTasks, Depends
from api.models import ChatRequest, ChatResponse, ClarificationRequest, ClarificationResponse, MultiQueryRequest
from api.dependencies import get_orchestrator, get_evaluator
from api.background_tasks import perform_self_critique
from agent.orchestrator import CVOrchestrator
from agent.evaluator import ResponseEvaluator
from tools.notify import notification_manager

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/chat", tags=["Chat"])


@router.post("", response_model=ChatResponse)
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


@router.post("/clarify", response_model=ClarificationResponse)
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


@router.post("/search/multi-query")
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