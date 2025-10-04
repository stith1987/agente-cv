"""
Agent Module

Sistema de agentes especializado para el manejo de consultas sobre CV profesional.
Incluye orquestación inteligente, clasificación de consultas y agentes especializados.
"""

from .core.orchestrator import CVOrchestrator
from .core.query_classifier import QueryClassifier, QueryClassification
from .core.response_evaluator import ResponseEvaluator, EvaluationResult
from .specialists.clarifier import ClarifierAgent
from .specialists.email_handler import EmailAgent
from .utils.prompts import PromptManager
from .utils.config import AgentConfig
from .utils.logger import AgentLogger

__version__ = "2.0.0"

__all__ = [
    "CVOrchestrator",
    "QueryClassifier", 
    "QueryClassification",
    "ResponseEvaluator",
    "EvaluationResult", 
    "ClarifierAgent",
    "EmailAgent",
    "PromptManager",
    "AgentConfig",
    "AgentLogger"
]