"""
Endpoints de notificaciones
"""

import logging
from datetime import datetime
from typing import Optional

from fastapi import APIRouter, HTTPException
from tools.notify import notification_manager

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/notifications", tags=["Notifications"])


@router.post("")
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


@router.get("/stats")
async def get_notification_stats():
    """Obtener estadísticas de notificaciones"""
    try:
        stats = notification_manager.get_notification_stats()
        return {
            "success": True,
            "stats": stats,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Error obteniendo estadísticas de notificaciones: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Error obteniendo estadísticas: {str(e)}"
        )