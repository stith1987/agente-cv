"""
Logger Module

Sistema de logging centralizado para el módulo de agentes.
"""

import os
import logging
import sys
from datetime import datetime
from typing import Optional
from pathlib import Path

class AgentLogger:
    """Logger especializado para el sistema de agentes"""
    
    def __init__(self, 
                 name: str = "agent",
                 level: str = "INFO",
                 log_to_file: bool = True,
                 log_file_path: str = "logs/agent.log"):
        """
        Inicializar logger
        
        Args:
            name: Nombre del logger
            level: Nivel de logging (DEBUG, INFO, WARNING, ERROR, CRITICAL)
            log_to_file: Si debe escribir logs a archivo
            log_file_path: Ruta del archivo de log
        """
        self.name = name
        self.level = getattr(logging, level.upper())
        self.log_to_file = log_to_file
        self.log_file_path = log_file_path
        
        # Crear logger
        self.logger = logging.getLogger(name)
        self.logger.setLevel(self.level)
        
        # Evitar duplicar handlers
        if not self.logger.handlers:
            self._setup_handlers()
    
    def _setup_handlers(self):
        """Configurar handlers de logging"""
        # Formatter
        formatter = logging.Formatter(
            fmt='%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        # Console handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(self.level)
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)
        
        # File handler
        if self.log_to_file:
            # Crear directorio de logs si no existe
            log_dir = Path(self.log_file_path).parent
            log_dir.mkdir(parents=True, exist_ok=True)
            
            file_handler = logging.FileHandler(self.log_file_path, encoding='utf-8')
            file_handler.setLevel(self.level)
            file_handler.setFormatter(formatter)
            self.logger.addHandler(file_handler)
    
    def debug(self, message: str, **kwargs):
        """Log debug message"""
        self.logger.debug(message, extra=kwargs)
    
    def info(self, message: str, **kwargs):
        """Log info message"""
        self.logger.info(message, extra=kwargs)
    
    def warning(self, message: str, **kwargs):
        """Log warning message"""
        self.logger.warning(message, extra=kwargs)
    
    def error(self, message: str, exception: Optional[Exception] = None, **kwargs):
        """Log error message"""
        if exception:
            self.logger.error(f"{message}: {str(exception)}", exc_info=exception, extra=kwargs)
        else:
            self.logger.error(message, extra=kwargs)
    
    def critical(self, message: str, exception: Optional[Exception] = None, **kwargs):
        """Log critical message"""
        if exception:
            self.logger.critical(f"{message}: {str(exception)}", exc_info=exception, extra=kwargs)
        else:
            self.logger.critical(message, extra=kwargs)
    
    def log_query(self, query: str, response_type: str, execution_time: float, success: bool = True):
        """Log específico para consultas"""
        self.info(
            f"Query processed - Type: {response_type}, Time: {execution_time:.2f}s, Success: {success}",
            query=query,
            response_type=response_type,
            execution_time=execution_time,
            success=success
        )
    
    def log_tool_usage(self, tool_name: str, parameters: dict, success: bool, execution_time: float):
        """Log específico para uso de herramientas"""
        self.info(
            f"Tool used - {tool_name}, Success: {success}, Time: {execution_time:.2f}s",
            tool_name=tool_name,
            parameters=parameters,
            success=success,
            execution_time=execution_time
        )
    
    def log_agent_action(self, agent_name: str, action: str, context: dict = None):
        """Log específico para acciones de agentes"""
        context = context or {}
        self.info(
            f"Agent action - {agent_name}: {action}",
            agent_name=agent_name,
            action=action,
            context=context
        )

# Logger global por defecto
default_logger = AgentLogger()

def get_logger(name: str = "agent", 
               level: str = "INFO",
               log_to_file: bool = True,
               log_file_path: str = "logs/agent.log") -> AgentLogger:
    """
    Obtener logger configurado
    
    Args:
        name: Nombre del logger
        level: Nivel de logging
        log_to_file: Si debe escribir a archivo
        log_file_path: Ruta del archivo de log
        
    Returns:
        Logger configurado
    """
    return AgentLogger(name, level, log_to_file, log_file_path)