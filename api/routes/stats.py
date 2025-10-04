"""
Endpoints de estadísticas
"""

import logging
from datetime import datetime
from typing import Optional

from fastapi import APIRouter, HTTPException, Depends
from api.models import StatsResponse
from api.dependencies import get_orchestrator, get_evaluator
from agent.orchestrator import CVOrchestrator
from agent.evaluator import ResponseEvaluator
from tools.notify import notification_manager

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/stats", tags=["Statistics"])


@router.get("", response_model=StatsResponse)
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


@router.post("/evaluate")
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