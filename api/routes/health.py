"""
Endpoints de salud y información básica
"""

import logging
from datetime import datetime
from typing import Dict

from fastapi import APIRouter
from api.models import HealthResponse
from api.dependencies import orchestrator, evaluator

logger = logging.getLogger(__name__)
router = APIRouter(tags=["Health"])


@router.get("/", response_model=Dict[str, str])
async def root():
    """Endpoint raíz con información básica"""
    return {
        "message": "CV Agent API",
        "version": "1.0.0",
        "documentation": "/docs",
        "health": "/health"
    }


@router.get("/health", response_model=HealthResponse)
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