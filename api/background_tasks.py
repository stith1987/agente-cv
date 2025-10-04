"""
Tareas en background para la API
"""

import logging
from typing import List
from api.dependencies import get_evaluator
from tools.notify import notification_manager

logger = logging.getLogger(__name__)


async def perform_self_critique(query: str, response: str, tools_used: List[str]):
    """Tarea en background para auto-crítica"""
    try:
        evaluator = get_evaluator()
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