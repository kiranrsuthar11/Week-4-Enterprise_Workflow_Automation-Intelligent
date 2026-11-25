import logging
import smtplib
import ssl
from email.message import EmailMessage
from app.config import settings

logger = logging.getLogger(__name__)

def notify_pending(workflow_id: int, title: str) -> str:
    message = f"Workflow #{workflow_id} is pending approval: {title}"
    logger.info(message)
    # Email is optional. If SMTP is not configured, the notification remains in logs.
    if settings.smtp_host and settings.smtp_from and settings.notification_email:
        email = EmailMessage()
        email["Subject"] = f"Pending approval: {title}"
        email["From"] = settings.smtp_from
        email["To"] = settings.notification_email
        email.set_content(message)
        try:
            if settings.smtp_port == 465:
                with smtplib.SMTP_SSL(settings.smtp_host, settings.smtp_port, context=ssl.create_default_context(), timeout=10) as server:
                    if settings.smtp_username:
                        server.login(settings.smtp_username, settings.smtp_password)
                    server.send_message(email)
            else:
                with smtplib.SMTP(settings.smtp_host, settings.smtp_port, timeout=10) as server:
                    server.starttls(context=ssl.create_default_context())
                    if settings.smtp_username:
                        server.login(settings.smtp_username, settings.smtp_password)
                    server.send_message(email)
            logger.info("Pending notification email sent for workflow_id=%s", workflow_id)
        except Exception:
            logger.exception("Could not send pending notification email for workflow_id=%s", workflow_id)
    return message
