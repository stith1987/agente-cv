"""
Inyección de dependencias para la API
"""

from typing import Optional
from fastapi import HTTPException
from agent.orchestrator import CVOrchestrator
from agent.evaluator import ResponseEvaluator

# Variables globales para mantener estado
orchestrator: Optional[CVOrchestrator] = None
evaluator: Optional[ResponseEvaluator] = None


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


def set_orchestrator(orch: CVOrchestrator) -> None:
    """Establecer instancia del orquestador"""
    global orchestrator
    orchestrator = orch


def set_evaluator(eval: ResponseEvaluator) -> None:
    """Establecer instancia del evaluador"""
    global evaluator
    evaluator = eval