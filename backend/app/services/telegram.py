from typing import Optional
import aiohttp
from app.core.config import settings
from app.models.user import User
from app.models.notification import Notification
from app.schemas.notification import NotificationType


class TelegramService:
    """Сервис для отправки уведомлений через Telegram"""
    
    def __init__(self):
        self.bot_token = settings.TELEGRAM_BOT_TOKEN
        self.api_url = f"https://api.telegram.org/bot{self.bot_token}"
    
    async def send_message(
        self, 
        chat_id: str, 
        text: str, 
        parse_mode: str = "HTML",
        disable_web_page_preview: bool = True,
        reply_markup: Optional[dict] = None
    ) -> bool:
        """
        Отправить сообщение через Telegram
        
        Args:
            chat_id: ID чата
            text: Текст сообщения
            parse_mode: Режим форматирования (HTML/Markdown)
            disable_web_page_preview: Отключить предпросмотр ссылок
            reply_markup: Разметка клавиатуры
            
        Returns:
            True если сообщение отправлено успешно
        """
        if not self.bot_token:
            return False
            
        url = f"{self.api_url}/sendMessage"
        data = {
            "chat_id": chat_id,
            "text": text,
            "parse_mode": parse_mode,
            "disable_web_page_preview": disable_web_page_preview
        }
        
        if reply_markup:
            data["reply_markup"] = reply_markup
            
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(url, json=data) as response:
                    return response.status == 200
        except Exception as e:
            print(f"Error sending Telegram message: {e}")
            return False
    
    def format_notification_message(self, notification: Notification) -> str:
        """
        Форматировать уведомление для отправки в Telegram
        
        Args:
            notification: Объект уведомления
            
        Returns:
            Отформатированный текст сообщения
        """
        # Базовый текст с заголовком
        message = f"<b>{notification.title}</b>\n\n{notification.message}"
        
        # Добавляем ссылку, если есть
        if notification.link:
            message += f"\n\n<a href='{notification.link}'>Подробнее</a>"
            
        return message
    
    def get_inline_keyboard(self, notification: Notification) -> Optional[dict]:
        """
        Получить разметку inline-клавиатуры для уведомления
        
        Args:
            notification: Объект уведомления
            
        Returns:
            Разметка клавиатуры или None
        """
        if not notification.link:
            return None
            
        return {
            "inline_keyboard": [[
                {
                    "text": "Открыть",
                    "url": notification.link
                }
            ]]
        }
    
    async def send_notification(self, user: User, notification: Notification) -> bool:
        """
        Отправить уведомление пользователю через Telegram
        
        Args:
            user: Объект пользователя
            notification: Объект уведомления
            
        Returns:
            True если уведомление отправлено успешно
        """
        if not user.telegram_id:
            return False
            
        message = self.format_notification_message(notification)
        keyboard = self.get_inline_keyboard(notification)
        
        return await self.send_message(
            chat_id=user.telegram_id,
            text=message,
            reply_markup=keyboard
        )


# Создание экземпляра сервиса
telegram_service = TelegramService() 