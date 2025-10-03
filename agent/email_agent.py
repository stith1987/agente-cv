"""
Email Agent Module

Agente especializado en el envío de correos electrónicos con
resúmenes de consultas y respuestas del agente de CV.
"""

import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Dict, Any, Optional
import logging
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()
logger = logging.getLogger(__name__)

class EmailAgent:
    """Agente especializado en envío de correos electrónicos"""
    
    def __init__(self):
        """Inicializar el agente de email"""
        # Configuración SMTP
        self.smtp_server = os.getenv("SMTP_SERVER", "smtp.gmail.com")
        self.smtp_port = int(os.getenv("SMTP_PORT", "587"))
        self.smtp_username = os.getenv("SMTP_USERNAME", "")
        self.smtp_password = os.getenv("SMTP_PASSWORD", "")
        self.from_email = os.getenv("FROM_EMAIL", self.smtp_username)
        
        # Configuración por defecto
        self.default_recipient = os.getenv("DEFAULT_EMAIL_RECIPIENT", "")
        
        # Estadísticas
        self.stats = {
            "emails_sent": 0,
            "emails_failed": 0,
            "last_email_sent": None
        }
        
        # Verificar configuración
        self._verify_config()
    
    def _verify_config(self) -> bool:
        """Verificar que la configuración de email esté completa"""
        required_configs = [
            ("SMTP_USERNAME", self.smtp_username),
            ("SMTP_PASSWORD", self.smtp_password),
            ("FROM_EMAIL", self.from_email)
        ]
        
        missing_configs = [name for name, value in required_configs if not value]
        
        if missing_configs:
            logger.warning(f"Configuración de email incompleta. Faltan: {missing_configs}")
            logger.info("Para activar el email, configura las variables de entorno:")
            logger.info("SMTP_USERNAME, SMTP_PASSWORD, FROM_EMAIL")
            return False
        
        return True
    
    def send(
        self, 
        to: str, 
        subject: str, 
        html: str, 
        text: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Enviar email con resumen de consulta
        
        Args:
            to: Dirección de correo destinatario
            subject: Asunto del correo
            html: Contenido HTML del correo
            text: Contenido texto plano (opcional)
            metadata: Metadata adicional (opcional)
            
        Returns:
            Dict con resultado del envío
        """
        try:
            # Verificar configuración
            if not self._verify_config():
                return {
                    "success": False,
                    "error": "Configuración de email incompleta",
                    "sent_at": datetime.now().isoformat()
                }
            
            # Crear mensaje
            message = MIMEMultipart("alternative")
            message["Subject"] = subject
            message["From"] = self.from_email
            message["To"] = to
            
            # Agregar contenido texto plano si no se proporciona
            if text is None:
                text = self._html_to_text(html)
            
            # Crear partes del mensaje
            text_part = MIMEText(text, "plain", "utf-8")
            html_part = MIMEText(html, "html", "utf-8")
            
            message.attach(text_part)
            message.attach(html_part)
            
            # Enviar email
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.smtp_username, self.smtp_password)
                server.send_message(message)
            
            # Actualizar estadísticas
            self.stats["emails_sent"] += 1
            self.stats["last_email_sent"] = datetime.now().isoformat()
            
            logger.info(f"Email enviado exitosamente a {to}")
            
            return {
                "success": True,
                "recipient": to,
                "subject": subject,
                "sent_at": self.stats["last_email_sent"],
                "message_id": f"cv-agent-{datetime.now().timestamp()}",
                "metadata": metadata or {}
            }
            
        except Exception as e:
            self.stats["emails_failed"] += 1
            logger.error(f"Error enviando email: {e}")
            
            return {
                "success": False,
                "error": str(e),
                "recipient": to,
                "subject": subject,
                "sent_at": datetime.now().isoformat(),
                "metadata": metadata or {}
            }
    
    def send_query_summary(
        self, 
        query: str, 
        response: str, 
        recipient_email: Optional[str] = None,
        classification: Optional[Dict[str, Any]] = None,
        session_id: str = "anonymous"
    ) -> Dict[str, Any]:
        """
        Enviar resumen de consulta y respuesta por email
        
        Args:
            query: Consulta original del usuario
            response: Respuesta generada por el agente
            recipient: Destinatario (opcional, usa default si no se especifica)
            classification: Clasificación de la consulta (opcional)
            session_id: ID de sesión
            
        Returns:
            Dict con resultado del envío
        """
        if not recipient_email:
            recipient_email = self.default_recipient
        
        if not recipient_email:
            return {
                "success": False,
                "error": "No se especificó destinatario y no hay destinatario por defecto configurado"
            }
        
        # Generar subject
        subject = f"CV Agent - Consulta: {query[:50]}{'...' if len(query) > 50 else ''}"
        
        # Generar contenido HTML
        html_content = self._generate_html_summary(
            query, response, classification, session_id
        )
        
        # Metadata del email
        metadata = {
            "type": "query_summary",
            "session_id": session_id,
            "query_length": len(query),
            "response_length": len(response),
            "classification": classification
        }
        
        return self.send(
            to=recipient_email,
            subject=subject,
            html=html_content,
            metadata=metadata
        )
    
    def _generate_html_summary(
        self, 
        query: str, 
        response: str, 
        classification: Optional[Dict[str, Any]] = None,
        session_id: str = "anonymous"
    ) -> str:
        """
        Generar contenido HTML para el resumen de consulta
        
        Args:
            query: Consulta original
            response: Respuesta generada
            classification: Clasificación de la consulta
            session_id: ID de sesión
            
        Returns:
            Contenido HTML formateado
        """
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        classification_info = ""
        if classification:
            classification_info = f"""
            <div style="background-color: #f8f9fa; padding: 15px; border-radius: 5px; margin: 15px 0;">
                <h3 style="color: #495057; margin-top: 0;">📊 Clasificación de Consulta</h3>
                <p><strong>Categoría:</strong> {classification.get('category', 'N/A')}</p>
                <p><strong>Confianza:</strong> {classification.get('confidence', 0)}%</p>
                <p><strong>Herramienta recomendada:</strong> {classification.get('recommended_tool', 'N/A')}</p>
            </div>
            """
        
        html_template = f"""
        <!DOCTYPE html>
        <html lang="es">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>CV Agent - Resumen de Consulta</title>
        </head>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333; max-width: 800px; margin: 0 auto; padding: 20px;">
            <div style="background-color: #007bff; color: white; padding: 20px; border-radius: 10px; text-align: center;">
                <h1 style="margin: 0;">🤖 CV Agent - Resumen de Consulta</h1>
                <p style="margin: 5px 0 0 0;">Resumen generado automáticamente</p>
            </div>
            
            <div style="background-color: #e3f2fd; padding: 15px; border-radius: 5px; margin: 20px 0;">
                <h2 style="color: #1976d2; margin-top: 0;">❓ Consulta Original</h2>
                <p style="font-style: italic; background-color: white; padding: 10px; border-radius: 3px;">{query}</p>
            </div>
            
            {classification_info}
            
            <div style="background-color: #e8f5e8; padding: 15px; border-radius: 5px; margin: 20px 0;">
                <h2 style="color: #2e7d32; margin-top: 0;">💬 Respuesta Generada</h2>
                <div style="background-color: white; padding: 15px; border-radius: 3px; white-space: pre-wrap;">{response}</div>
            </div>
            
            <div style="background-color: #fff3e0; padding: 15px; border-radius: 5px; margin: 20px 0;">
                <h3 style="color: #f57c00; margin-top: 0;">📋 Información de Sesión</h3>
                <p><strong>Session ID:</strong> {session_id}</p>
                <p><strong>Timestamp:</strong> {timestamp}</p>
                <p><strong>Longitud de consulta:</strong> {len(query)} caracteres</p>
                <p><strong>Longitud de respuesta:</strong> {len(response)} caracteres</p>
            </div>
            
            <div style="text-align: center; margin-top: 40px; padding-top: 20px; border-top: 1px solid #ddd;">
                <p style="color: #666; font-size: 14px;">
                    Este email fue generado automáticamente por el CV Agent<br>
                    <strong>Agente de CV Inteligente</strong> - Sistema de IA Conversacional
                </p>
            </div>
        </body>
        </html>
        """
        
        return html_template
    
    def _html_to_text(self, html: str) -> str:
        """
        Convertir HTML básico a texto plano
        
        Args:
            html: Contenido HTML
            
        Returns:
            Contenido en texto plano
        """
        import re
        
        # Remover tags HTML
        text = re.sub(r'<[^>]+>', '', html)
        
        # Decodificar entidades HTML comunes
        text = text.replace('&nbsp;', ' ')
        text = text.replace('&amp;', '&')
        text = text.replace('&lt;', '<')
        text = text.replace('&gt;', '>')
        text = text.replace('&quot;', '"')
        
        # Limpiar espacios extra
        text = re.sub(r'\s+', ' ', text).strip()
        
        return text
    
    def get_stats(self) -> Dict[str, Any]:
        """Obtener estadísticas del agente de email"""
        total_attempts = self.stats["emails_sent"] + self.stats["emails_failed"]
        success_rate = (self.stats["emails_sent"] / max(total_attempts, 1)) * 100
        
        return {
            **self.stats,
            "total_attempts": total_attempts,
            "success_rate": round(success_rate, 2),
            "config_valid": self._verify_config()
        }

# Instancia global
_email_agent_instance = None

def get_email_agent() -> EmailAgent:
    """Obtener instancia singleton del agente de email"""
    global _email_agent_instance
    if _email_agent_instance is None:
        _email_agent_instance = EmailAgent()
    return _email_agent_instance