"""
Manejo de excepciones para la API
"""

import logging
from datetime import datetime
from fastapi import HTTPException
from fastapi.responses import JSONResponse
from starlette.requests import Request

logger = logging.getLogger(__name__)


async def http_exception_handler(request: Request, exc: HTTPException):
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


async def general_exception_handler(request: Request, exc: Exception):
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