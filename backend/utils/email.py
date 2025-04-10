import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from ..config import settings

async def send_email(to_email: str, subject: str, message: str) -> None:
    """Отправка email уведомления"""
    msg = MIMEMultipart()
    msg['From'] = settings.SMTP_FROM_EMAIL
    msg['To'] = to_email
    msg['Subject'] = subject

    msg.attach(MIMEText(message, 'plain'))

    try:
        with smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT) as server:
            server.starttls()
            server.login(settings.SMTP_USERNAME, settings.SMTP_PASSWORD)
            server.send_message(msg)
    except Exception as e:
        # TODO: Добавить логирование ошибок
        print(f"Ошибка отправки email: {e}") 