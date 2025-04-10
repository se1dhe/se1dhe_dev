from typing import Optional
from ..models.notification import Notification
from ..config import settings
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class EmailService:
    def __init__(self):
        self.smtp_server = settings.SMTP_HOST
        self.smtp_port = settings.SMTP_PORT
        self.smtp_username = settings.SMTP_USERNAME
        self.smtp_password = settings.SMTP_PASSWORD
        self.from_email = settings.SMTP_FROM_EMAIL

    async def send_notification(self, notification: Notification) -> bool:
        """Отправка уведомления по email"""
        try:
            # Получаем email пользователя из базы данных
            user_email = notification.user.email
            if not user_email:
                return False

            # Создаем сообщение
            msg = MIMEMultipart()
            msg['From'] = self.from_email
            msg['To'] = user_email
            msg['Subject'] = notification.title

            # Добавляем текст сообщения
            msg.attach(MIMEText(notification.message, 'plain'))

            # Отправляем сообщение
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.smtp_username, self.smtp_password)
                server.send_message(msg)

            return True
        except Exception as e:
            # TODO: Добавить логирование ошибок
            print(f"Error sending email notification: {str(e)}")
            return False 