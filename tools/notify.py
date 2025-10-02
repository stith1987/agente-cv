"""
Notification Tool

Herramienta para enviar notificaciones push usando Pushover u otros servicios.
"""

import os
import requests
from typing import Dict, Any, Optional
import logging
from dotenv import load_dotenv
from dataclasses import dataclass
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

@dataclass
class NotificationResult:
    """Resultado de envío de notificación"""
    success: bool
    message: str
    request_id: Optional[str] = None
    timestamp: Optional[datetime] = None

class PushoverNotifier:
    """Cliente para notificaciones Pushover"""
    
    def __init__(self):
        """Inicializar cliente Pushover"""
        self.api_token = os.getenv("PUSHOVER_TOKEN")
        self.user_key = os.getenv("PUSHOVER_USER")
        self.api_url = "https://api.pushover.net/1/messages.json"
        
        if not self.api_token or not self.user_key:
            logger.warning("Pushover credentials no configuradas")
    
    def send_notification(
        self,
        message: str,
        title: str = "CV Agent",
        priority: int = 0,
        sound: str = "default",
        url: Optional[str] = None,
        url_title: Optional[str] = None
    ) -> NotificationResult:
        """
        Enviar notificación via Pushover
        
        Args:
            message: Mensaje a enviar
            title: Título de la notificación
            priority: Prioridad (-2 a 2)
            sound: Sonido de notificación
            url: URL opcional
            url_title: Título del URL
        """
        if not self.api_token or not self.user_key:
            return NotificationResult(
                success=False,
                message="Pushover credentials no configuradas",
                timestamp=datetime.now()
            )
        
        try:
            payload = {
                "token": self.api_token,
                "user": self.user_key,
                "message": message,
                "title": title,
                "priority": priority,
                "sound": sound
            }
            
            if url:
                payload["url"] = url
                payload["url_title"] = url_title or url
            
            response = requests.post(self.api_url, data=payload, timeout=10)
            response.raise_for_status()
            
            result_data = response.json()
            
            if result_data.get("status") == 1:
                logger.info(f"Notificación enviada exitosamente: {title}")
                return NotificationResult(
                    success=True,
                    message="Notificación enviada exitosamente",
                    request_id=result_data.get("request"),
                    timestamp=datetime.now()
                )
            else:
                errors = result_data.get("errors", ["Error desconocido"])
                error_msg = "; ".join(errors)
                logger.error(f"Error en Pushover: {error_msg}")
                return NotificationResult(
                    success=False,
                    message=f"Error de Pushover: {error_msg}",
                    timestamp=datetime.now()
                )
                
        except requests.exceptions.RequestException as e:
            logger.error(f"Error de red en Pushover: {e}")
            return NotificationResult(
                success=False,
                message=f"Error de red: {str(e)}",
                timestamp=datetime.now()
            )
        except Exception as e:
            logger.error(f"Error inesperado en notificación: {e}")
            return NotificationResult(
                success=False,
                message=f"Error inesperado: {str(e)}",
                timestamp=datetime.now()
            )

class NotificationManager:
    """Manager para múltiples canales de notificación"""
    
    def __init__(self):
        """Inicializar manager de notificaciones"""
        self.pushover = PushoverNotifier()
        self.notification_log = []
    
    def send_query_notification(
        self,
        user_query: str,
        response_summary: str,
        session_id: str = "anonymous"
    ) -> NotificationResult:
        """
        Notificar sobre una nueva consulta al CV
        
        Args:
            user_query: Consulta del usuario
            response_summary: Resumen de la respuesta
            session_id: ID de sesión del usuario
        """
        title = "Nueva Consulta CV"
        message = f"""
🔍 Consulta: {user_query[:100]}...

📝 Respuesta: {response_summary[:150]}...

👤 Sesión: {session_id}
⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
        """.strip()
        
        result = self.pushover.send_notification(
            message=message,
            title=title,
            priority=0,
            sound="default"
        )
        
        # Log interno
        self.notification_log.append({
            "type": "query",
            "query": user_query,
            "session_id": session_id,
            "timestamp": datetime.now(),
            "success": result.success
        })
        
        return result
    
    def send_error_notification(
        self,
        error_message: str,
        context: Dict[str, Any] = None
    ) -> NotificationResult:
        """
        Notificar sobre errores críticos
        
        Args:
            error_message: Mensaje de error
            context: Contexto adicional del error
        """
        title = "⚠️ Error CV Agent"
        message = f"""
Error: {error_message}

Contexto: {context or 'N/A'}

Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
        """.strip()
        
        result = self.pushover.send_notification(
            message=message,
            title=title,
            priority=1,  # Prioridad alta para errores
            sound="siren"
        )
        
        # Log interno
        self.notification_log.append({
            "type": "error",
            "error": error_message,
            "context": context,
            "timestamp": datetime.now(),
            "success": result.success
        })
        
        return result
    
    def send_daily_summary(self, stats: Dict[str, Any]) -> NotificationResult:
        """
        Enviar resumen diario de actividad
        
        Args:
            stats: Estadísticas del día
        """
        title = "📊 Resumen Diario CV Agent"
        message = f"""
Consultas: {stats.get('total_queries', 0)}
RAG Searches: {stats.get('rag_searches', 0)}
FAQ Queries: {stats.get('faq_queries', 0)}
Errores: {stats.get('errors', 0)}

Top Query: {stats.get('top_query', 'N/A')}

Fecha: {datetime.now().strftime('%Y-%m-%d')}
        """.strip()
        
        result = self.pushover.send_notification(
            message=message,
            title=title,
            priority=0,
            sound="echo"
        )
        
        return result
    
    def send_custom_notification(
        self,
        message: str,
        title: str = "CV Agent",
        priority: int = 0,
        **kwargs
    ) -> NotificationResult:
        """Enviar notificación personalizada"""
        result = self.pushover.send_notification(
            message=message,
            title=title,
            priority=priority,
            **kwargs
        )
        
        # Log interno
        self.notification_log.append({
            "type": "custom",
            "title": title,
            "message": message,
            "timestamp": datetime.now(),
            "success": result.success
        })
        
        return result
    
    def get_notification_stats(self) -> Dict[str, Any]:
        """Obtener estadísticas de notificaciones"""
        if not self.notification_log:
            return {
                "total_notifications": 0,
                "successful_notifications": 0,
                "failed_notifications": 0,
                "success_rate": 0.0,
                "notification_types": {}
            }
        
        total = len(self.notification_log)
        successful = sum(1 for log in self.notification_log if log["success"])
        failed = total - successful
        
        # Contar por tipo
        types_count = {}
        for log in self.notification_log:
            notification_type = log.get("type", "unknown")
            types_count[notification_type] = types_count.get(notification_type, 0) + 1
        
        return {
            "total_notifications": total,
            "successful_notifications": successful,
            "failed_notifications": failed,
            "success_rate": (successful / total) * 100 if total > 0 else 0.0,
            "notification_types": types_count,
            "last_notification": self.notification_log[-1]["timestamp"] if self.notification_log else None
        }
    
    def clear_log(self):
        """Limpiar log de notificaciones"""
        self.notification_log.clear()
        logger.info("Log de notificaciones limpiado")

# Instancia global del manager
notification_manager = NotificationManager()

def notify_query(user_query: str, response_summary: str, session_id: str = "anonymous") -> NotificationResult:
    """Helper function para notificar consultas"""
    return notification_manager.send_query_notification(user_query, response_summary, session_id)

def notify_error(error_message: str, context: Dict[str, Any] = None) -> NotificationResult:
    """Helper function para notificar errores"""
    return notification_manager.send_error_notification(error_message, context)

def notify_custom(message: str, title: str = "CV Agent", **kwargs) -> NotificationResult:
    """Helper function para notificaciones personalizadas"""
    return notification_manager.send_custom_notification(message, title, **kwargs)

def main():
    """Función de test para notificaciones"""
    try:
        manager = NotificationManager()
        
        # Test notificación de consulta
        print("Enviando notificación de consulta...")
        result1 = manager.send_query_notification(
            user_query="¿Cuáles son tus principales proyectos?",
            response_summary="Mencioné los proyectos de banca digital y arquitectura empresarial",
            session_id="test_user_123"
        )
        print(f"Resultado: {result1.success} - {result1.message}")
        
        # Test notificación de error
        print("\nEnviando notificación de error...")
        result2 = manager.send_error_notification(
            error_message="Error conectando a vector database",
            context={"component": "retriever", "attempt": 3}
        )
        print(f"Resultado: {result2.success} - {result2.message}")
        
        # Test notificación personalizada
        print("\nEnviando notificación personalizada...")
        result3 = manager.send_custom_notification(
            message="Sistema inicializado correctamente",
            title="🚀 CV Agent Status",
            priority=0,
            sound="intermission"
        )
        print(f"Resultado: {result3.success} - {result3.message}")
        
        # Mostrar estadísticas
        stats = manager.get_notification_stats()
        print(f"\nEstadísticas de notificaciones:")
        print(f"- Total: {stats['total_notifications']}")
        print(f"- Exitosas: {stats['successful_notifications']}")
        print(f"- Fallidas: {stats['failed_notifications']}")
        print(f"- Tasa de éxito: {stats['success_rate']:.1f}%")
        print(f"- Tipos: {stats['notification_types']}")
        
    except Exception as e:
        logger.error(f"Error en test de notificaciones: {e}")
        raise

if __name__ == "__main__":
    main()