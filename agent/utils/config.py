"""
Configuration Module

Configuración centralizada para el sistema de agentes.
"""

import os
from typing import Dict, Any, Optional
from dataclasses import dataclass

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    # dotenv es opcional
    pass

@dataclass
class OpenAIConfig:
    """Configuración para OpenAI y proveedores compatibles"""
    api_key: str
    model: str = "gpt-4"
    temperature: float = 0.7
    max_tokens: int = 2000
    base_url: Optional[str] = None  # Para proveedores alternativos
    provider: str = "openai"  # openai, deepseek, groq, gemini, ollama, etc.
    
    def __post_init__(self):
        if not self.api_key:
            raise ValueError("API key is required")
    
    def get_provider_name(self) -> str:
        """Obtener nombre del proveedor configurado"""
        return self.provider
    
    def is_openai_compatible(self) -> bool:
        """Verificar si el proveedor es compatible con OpenAI API"""
        return True  # Todos los proveedores soportados usan API compatible

@dataclass 
class EmailConfig:
    """Configuración para email"""
    smtp_server: str = "smtp.gmail.com"
    smtp_port: int = 587
    username: str = ""
    password: str = ""
    from_email: str = ""
    default_recipient: str = ""
    
    def is_configured(self) -> bool:
        """Verificar si email está configurado"""
        return bool(self.username and self.password and self.from_email)

@dataclass
class AgentConfig:
    """Configuración principal del sistema de agentes"""
    
    # OpenAI
    openai: OpenAIConfig
    
    # Email
    email: EmailConfig
    
    # Configuraciones de búsqueda
    rag_similarity_threshold: float = 0.7
    rag_top_k: int = 5
    faq_limit: int = 10
    
    # Configuraciones de clasificación
    classification_confidence_threshold: float = 0.8
    
    # Configuraciones de evaluación
    evaluation_min_score: float = 7.0
    
    # Configuraciones de logging
    log_level: str = "INFO"
    log_to_file: bool = True
    log_file_path: str = "logs/agent.log"
    
    @classmethod
    def from_env(cls) -> 'AgentConfig':
        """Crear configuración desde variables de entorno"""
        
        # OpenAI / Multi-LLM
        openai_config = OpenAIConfig(
            api_key=os.getenv("OPENAI_API_KEY", ""),
            model=os.getenv("OPENAI_MODEL", "gpt-4"),
            temperature=float(os.getenv("OPENAI_TEMPERATURE", "0.7")),
            max_tokens=int(os.getenv("OPENAI_MAX_TOKENS", "2000")),
            base_url=os.getenv("OPENAI_BASE_URL"),  # None si no está configurado
            provider=os.getenv("LLM_PROVIDER", "openai")
        )
        
        # Email
        email_config = EmailConfig(
            smtp_server=os.getenv("SMTP_SERVER", "smtp.gmail.com"),
            smtp_port=int(os.getenv("SMTP_PORT", "587")),
            username=os.getenv("SMTP_USERNAME", ""),
            password=os.getenv("SMTP_PASSWORD", ""),
            from_email=os.getenv("FROM_EMAIL", ""),
            default_recipient=os.getenv("DEFAULT_EMAIL_RECIPIENT", "")
        )
        
        return cls(
            openai=openai_config,
            email=email_config,
            rag_similarity_threshold=float(os.getenv("RAG_SIMILARITY_THRESHOLD", "0.7")),
            rag_top_k=int(os.getenv("RAG_TOP_K", "5")),
            faq_limit=int(os.getenv("FAQ_LIMIT", "10")),
            classification_confidence_threshold=float(os.getenv("CLASSIFICATION_CONFIDENCE_THRESHOLD", "0.8")),
            evaluation_min_score=float(os.getenv("EVALUATION_MIN_SCORE", "7.0")),
            log_level=os.getenv("LOG_LEVEL", "INFO"),
            log_to_file=os.getenv("LOG_TO_FILE", "true").lower() == "true",
            log_file_path=os.getenv("LOG_FILE_PATH", "logs/agent.log")
        )
    
    def to_dict(self) -> Dict[str, Any]:
        """Convertir a diccionario"""
        return {
            "openai": {
                "model": self.openai.model,
                "temperature": self.openai.temperature,
                "max_tokens": self.openai.max_tokens
            },
            "email": {
                "smtp_server": self.email.smtp_server,
                "smtp_port": self.email.smtp_port,
                "is_configured": self.email.is_configured()
            },
            "rag_similarity_threshold": self.rag_similarity_threshold,
            "rag_top_k": self.rag_top_k,
            "faq_limit": self.faq_limit,
            "classification_confidence_threshold": self.classification_confidence_threshold,
            "evaluation_min_score": self.evaluation_min_score,
            "log_level": self.log_level,
            "log_to_file": self.log_to_file,
            "log_file_path": self.log_file_path
        }