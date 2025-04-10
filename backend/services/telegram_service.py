from typing import Optional
from ..models.notification import Notification
from ..config import settings
import aiohttp

class TelegramService:
    def __init__(self):
        self.bot_token = settings.TELEGRAM_BOT_TOKEN
        self.api_url = f"https://api.telegram.org/bot{self.bot_token}"

    async def send_notification(self, notification: Notification) -> bool:
        """Отправка уведомления через Telegram"""
        try:
            # Получаем Telegram ID пользователя из базы данных
            telegram_id = notification.user.telegram_id
            if not telegram_id:
                return False

            # Формируем сообщение
            message = f"*{notification.title}*\n\n{notification.message}"

            # Отправляем сообщение через Telegram API
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.api_url}/sendMessage",
                    json={
                        "chat_id": telegram_id,
                        "text": message,
                        "parse_mode": "Markdown"
                    }
                ) as response:
                    if response.status == 200:
                        return True
                    else:
                        # TODO: Добавить логирование ошибок
                        print(f"Error sending Telegram notification: {await response.text()}")
                        return False

        except Exception as e:
            # TODO: Добавить логирование ошибок
            print(f"Error sending Telegram notification: {str(e)}")
            return False 