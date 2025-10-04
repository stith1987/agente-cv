"""
Email Handler Agent Module

Agente especializado refactorizado para manejo inteligente de correos electrónicos
con resúmenes de consultas y notificaciones del sistema.
"""

import smtplib
import time
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Dict, Any, Optional
from datetime import datetime

from ..utils.config import AgentConfig, EmailConfig
from ..utils.logger import AgentLogger
from ..utils.prompts import PromptManager, PromptType


class EmailAgent:
    """Agente especializado en envío de correos electrónicos"""
    
    def __init__(self, config: AgentConfig, logger: AgentLogger = None):
        """
        Inicializar agente de email
        
        Args:
            config: Configuración del agente
            logger: Logger para registrar actividad
        """
        self.config = config
        self.email_config = config.email
        self.logger = logger or AgentLogger("email_agent")
        self.prompt_manager = PromptManager()
        
        # Estadísticas
        self.stats = {
            "emails_sent": 0,
            "emails_failed": 0,
            "last_email_sent": None,
            "total_recipients": set(),
            "email_types": {
                "summary": 0,
                "notification": 0,
                "error": 0
            }
        }
        
        # Verificar configuración
        self.is_configured = self._verify_configuration()
        
        if self.is_configured:
            self.logger.info("EmailAgent initialized successfully")
        else:
            self.logger.warning("EmailAgent initialized but email is not properly configured")
    
    def _verify_configuration(self) -> bool:
        """Verificar que la configuración de email esté completa"""
        required_configs = [
            ("SMTP_USERNAME", self.email_config.username),
            ("SMTP_PASSWORD", self.email_config.password),
            ("FROM_EMAIL", self.email_config.from_email)
        ]
        
        missing_configs = []
        for config_name, config_value in required_configs:
            if not config_value:
                missing_configs.append(config_name)
        
        if missing_configs:
            self.logger.warning(f"Missing email configurations: {', '.join(missing_configs)}")
            return False
        
        return True
    
    def send_summary_email(self, 
                          recipient: str,
                          query: str,
                          response: str,
                          metadata: Optional[Dict[str, Any]] = None) -> bool:
        """
        Enviar email con resumen de consulta y respuesta
        
        Args:
            recipient: Destinatario del email
            query: Consulta original
            response: Respuesta proporcionada
            metadata: Metadatos adicionales
            
        Returns:
            True si el email se envió exitosamente
        """
        if not self.is_configured:
            self.logger.warning("Cannot send email - not properly configured")
            return False
        
        start_time = time.time()
        metadata = metadata or {}
        
        try:
            self.logger.debug(f"Sending summary email to {recipient}")
            
            # Generar contenido del email usando prompts
            email_content = self._generate_email_content(query, response, metadata)
            
            # Crear mensaje
            msg = self._create_email_message(
                recipient=recipient,
                subject=f"Resumen CV - {query[:50]}...",
                content=email_content,
                email_type="summary"
            )
            
            # Enviar email
            success = self._send_email(msg, recipient)
            
            if success:
                self.stats["emails_sent"] += 1
                self.stats["email_types"]["summary"] += 1
                self.stats["total_recipients"].add(recipient)
                self.stats["last_email_sent"] = datetime.now().isoformat()
            else:
                self.stats["emails_failed"] += 1
            
            execution_time = time.time() - start_time
            self.logger.log_tool_usage(
                "send_summary_email",
                {"recipient": recipient, "query_length": len(query)},
                success,
                execution_time
            )
            
            return success
            
        except Exception as e:
            self.logger.error("Error sending summary email", exception=e)
            self.stats["emails_failed"] += 1
            return False
    
    def send_notification_email(self,
                               recipient: str, 
                               title: str,
                               message: str,
                               priority: str = "normal") -> bool:
        """
        Enviar email de notificación
        
        Args:
            recipient: Destinatario del email
            title: Título de la notificación
            message: Mensaje de la notificación
            priority: Prioridad (low, normal, high)
            
        Returns:
            True si el email se envió exitosamente
        """
        if not self.is_configured:
            self.logger.warning("Cannot send notification email - not properly configured")
            return False
        
        try:
            self.logger.debug(f"Sending notification email to {recipient}")
            
            # Crear mensaje de notificación
            subject = f"[{priority.upper()}] {title}"
            
            content = f"""
            <html>
            <body>
                <h2>Notificación del Agente CV</h2>
                <p><strong>Título:</strong> {title}</p>
                <p><strong>Prioridad:</strong> {priority.upper()}</p>
                <p><strong>Mensaje:</strong></p>
                <div style="padding: 10px; background-color: #f5f5f5; border-left: 4px solid #007bff;">
                    {message}
                </div>
                <p><strong>Timestamp:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
            </body>
            </html>
            """
            
            # Crear mensaje
            msg = self._create_email_message(
                recipient=recipient,
                subject=subject,
                content=content,
                email_type="notification"
            )
            
            # Enviar email
            success = self._send_email(msg, recipient)
            
            if success:
                self.stats["emails_sent"] += 1
                self.stats["email_types"]["notification"] += 1
                self.stats["total_recipients"].add(recipient)
                self.stats["last_email_sent"] = datetime.now().isoformat()
            else:
                self.stats["emails_failed"] += 1
            
            return success
            
        except Exception as e:
            self.logger.error("Error sending notification email", exception=e)
            self.stats["emails_failed"] += 1
            return False
    
    def send_error_email(self,
                        recipient: str,
                        error_title: str,
                        error_details: str,
                        context: Optional[Dict[str, Any]] = None) -> bool:
        """
        Enviar email de error
        
        Args:
            recipient: Destinatario del email
            error_title: Título del error
            error_details: Detalles del error
            context: Contexto adicional
            
        Returns:
            True si el email se envió exitosamente
        """
        if not self.is_configured:
            self.logger.warning("Cannot send error email - not properly configured")
            return False
        
        try:
            context = context or {}
            
            subject = f"[ERROR] Agente CV - {error_title}"
            
            content = f"""
            <html>
            <body>
                <h2 style="color: #dc3545;">Error en Agente CV</h2>
                <p><strong>Título:</strong> {error_title}</p>
                <p><strong>Detalles:</strong></p>
                <div style="padding: 10px; background-color: #f8d7da; border-left: 4px solid #dc3545; color: #721c24;">
                    <pre>{error_details}</pre>
                </div>
                
                <h3>Contexto:</h3>
                <ul>
            """
            
            for key, value in context.items():
                content += f"<li><strong>{key}:</strong> {value}</li>"
            
            content += f"""
                </ul>
                <p><strong>Timestamp:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
            </body>
            </html>
            """
            
            # Crear mensaje
            msg = self._create_email_message(
                recipient=recipient,
                subject=subject,
                content=content,
                email_type="error"
            )
            
            # Enviar email
            success = self._send_email(msg, recipient)
            
            if success:
                self.stats["emails_sent"] += 1
                self.stats["email_types"]["error"] += 1
                self.stats["total_recipients"].add(recipient)
                self.stats["last_email_sent"] = datetime.now().isoformat()
            else:
                self.stats["emails_failed"] += 1
            
            return success
            
        except Exception as e:
            self.logger.error("Error sending error email", exception=e)
            self.stats["emails_failed"] += 1
            return False
    
    def _generate_email_content(self, query: str, response: str, metadata: Dict[str, Any]) -> str:
        """Generar contenido del email usando prompts"""
        try:
            # Usar prompt manager para generar contenido
            email_prompt = self.prompt_manager.format_email_prompt(
                query=query,
                response=response,
                recipient=metadata.get("recipient", "Usuario"),
                timestamp=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            )
            
            # Para esta implementación, generar contenido básico
            # En el futuro se podría usar OpenAI para generar contenido más sofisticado
            
            content = f"""
            <html>
            <body>
                <h2>Resumen de Consulta - Agente CV</h2>
                
                <h3>Consulta Realizada:</h3>
                <div style="padding: 10px; background-color: #e9ecef; border-left: 4px solid #6c757d;">
                    {query}
                </div>
                
                <h3>Respuesta Proporcionada:</h3>
                <div style="padding: 15px; background-color: #f8f9fa; border: 1px solid #dee2e6; border-radius: 5px;">
                    {self._format_response_for_email(response)}
                </div>
                
                <h3>Información Adicional:</h3>
                <ul>
                    <li><strong>Timestamp:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</li>
                    <li><strong>Fuente:</strong> {metadata.get('source', 'No especificada')}</li>
                    <li><strong>Herramientas usadas:</strong> {', '.join(metadata.get('tools_used', []))}</li>
            """
            
            if metadata.get("evaluation"):
                eval_data = metadata["evaluation"]
                content += f"<li><strong>Puntuación de calidad:</strong> {eval_data.get('overall_score', 'N/A'):.1f}/10</li>"
            
            content += """
                </ul>
                
                <hr>
                <p style="font-size: 12px; color: #6c757d;">
                    Este email fue generado automáticamente por el Agente CV.
                </p>
            </body>
            </html>
            """
            
            return content
            
        except Exception as e:
            self.logger.error("Error generating email content", exception=e)
            # Contenido básico de fallback
            return f"""
            <html>
            <body>
                <h2>Resumen de Consulta - Agente CV</h2>
                <p><strong>Consulta:</strong> {query}</p>
                <p><strong>Respuesta:</strong> {response[:500]}...</p>
                <p><strong>Timestamp:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
            </body>
            </html>
            """
    
    def _format_response_for_email(self, response: str) -> str:
        """Formatear respuesta para email HTML"""
        # Convertir saltos de línea a <br>
        formatted = response.replace('\n', '<br>')
        
        # Escapar caracteres HTML básicos si es necesario
        formatted = formatted.replace('<', '&lt;').replace('>', '&gt;')
        formatted = formatted.replace('<br>', '<br>')  # Restaurar <br>
        
        return formatted
    
    def _create_email_message(self, 
                             recipient: str,
                             subject: str,
                             content: str,
                             email_type: str = "general") -> MIMEMultipart:
        """Crear mensaje de email"""
        msg = MIMEMultipart("alternative")
        msg["Subject"] = subject
        msg["From"] = self.email_config.from_email
        msg["To"] = recipient
        msg["X-Email-Type"] = email_type
        
        # Crear versión HTML
        html_part = MIMEText(content, "html", "utf-8")
        msg.attach(html_part)
        
        # Crear versión texto plano básica
        text_content = self._html_to_text(content)
        text_part = MIMEText(text_content, "plain", "utf-8")
        msg.attach(text_part)
        
        return msg
    
    def _html_to_text(self, html_content: str) -> str:
        """Convertir HTML básico a texto plano"""
        import re
        
        # Remover tags HTML básicos
        text = re.sub(r'<[^>]+>', '', html_content)
        
        # Limpiar espacios múltiples
        text = re.sub(r'\s+', ' ', text)
        
        return text.strip()
    
    def _send_email(self, msg: MIMEMultipart, recipient: str) -> bool:
        """Enviar email usando SMTP"""
        try:
            with smtplib.SMTP(self.email_config.smtp_server, self.email_config.smtp_port) as server:
                server.starttls()
                server.login(self.email_config.username, self.email_config.password)
                
                text = msg.as_string()
                server.sendmail(self.email_config.from_email, recipient, text)
                
                self.logger.info(f"Email sent successfully to {recipient}")
                return True
                
        except smtplib.SMTPAuthenticationError as e:
            self.logger.error(f"SMTP authentication failed: {e}")
            return False
        except smtplib.SMTPRecipientsRefused as e:
            self.logger.error(f"Recipients refused: {e}")
            return False
        except smtplib.SMTPException as e:
            self.logger.error(f"SMTP error occurred: {e}")
            return False
        except Exception as e:
            self.logger.error(f"Unexpected error sending email: {e}")
            return False
    
    def test_email_configuration(self, test_recipient: Optional[str] = None) -> Dict[str, Any]:
        """
        Probar configuración de email
        
        Args:
            test_recipient: Destinatario para prueba (opcional)
            
        Returns:
            Resultado de la prueba
        """
        test_result = {
            "configuration_valid": False,
            "connection_successful": False,
            "test_email_sent": False,
            "details": []
        }
        
        # Verificar configuración
        if not self.is_configured:
            test_result["details"].append("Email configuration is incomplete")
            return test_result
        
        test_result["configuration_valid"] = True
        test_result["details"].append("Email configuration is valid")
        
        # Probar conexión SMTP
        try:
            with smtplib.SMTP(self.email_config.smtp_server, self.email_config.smtp_port) as server:
                server.starttls()
                server.login(self.email_config.username, self.email_config.password)
                
                test_result["connection_successful"] = True
                test_result["details"].append("SMTP connection successful")
                
                # Enviar email de prueba si se especifica destinatario
                if test_recipient:
                    test_msg = self._create_email_message(
                        recipient=test_recipient,
                        subject="Test Email - Agente CV",
                        content="<html><body><h2>Test Email</h2><p>Esta es una prueba de configuración del sistema de email.</p></body></html>",
                        email_type="test"
                    )
                    
                    success = self._send_email(test_msg, test_recipient)
                    test_result["test_email_sent"] = success
                    
                    if success:
                        test_result["details"].append(f"Test email sent successfully to {test_recipient}")
                    else:
                        test_result["details"].append(f"Failed to send test email to {test_recipient}")
                
        except Exception as e:
            test_result["details"].append(f"SMTP connection failed: {str(e)}")
        
        return test_result
    
    def get_stats(self) -> Dict[str, Any]:
        """Obtener estadísticas del agente"""
        success_rate = 0
        total_emails = self.stats["emails_sent"] + self.stats["emails_failed"]
        
        if total_emails > 0:
            success_rate = (self.stats["emails_sent"] / total_emails) * 100
        
        return {
            **{k: v for k, v in self.stats.items() if k != "total_recipients"},
            "total_unique_recipients": len(self.stats["total_recipients"]),
            "success_rate": round(success_rate, 2),
            "is_configured": self.is_configured
        }
    
    def reset_stats(self):
        """Reiniciar estadísticas"""
        self.stats = {
            "emails_sent": 0,
            "emails_failed": 0,
            "last_email_sent": None,
            "total_recipients": set(),
            "email_types": {
                "summary": 0,
                "notification": 0,
                "error": 0
            }
        }
        self.logger.info("Email stats reset")