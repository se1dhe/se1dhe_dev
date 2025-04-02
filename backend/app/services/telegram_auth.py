from typing import Optional, Dict, Any
from datetime import datetime, timedelta
from aiogram import Bot, Dispatcher
from aiogram.types import LoginUrl, WebAppInfo
from app.core.config import settings
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate
from app.crud.crud_user import user as crud_user
from app.core.security import create_access_token

class TelegramAuthService:
    def __init__(self):
        self.bot = Bot(token=settings.TELEGRAM_BOT_TOKEN)
        self.dp = Dispatcher()
        
    async def get_login_url(self, user_id: int) -> LoginUrl:
        """
        Создает URL для авторизации через Telegram
        
        Args:
            user_id: ID пользователя в Telegram
            
        Returns:
            LoginUrl объект для авторизации
        """
        return LoginUrl(
            url=f"{settings.FRONTEND_URL}/auth/telegram",
            forward_text="Войти через Telegram",
            bot_username=settings.TELEGRAM_BOT_USERNAME,
            request_write_access=True
        )
    
    async def get_webapp_url(self) -> str:
        """
        Создает URL для Telegram Web App
        
        Returns:
            URL для Web App
        """
        return f"https://t.me/{settings.TELEGRAM_BOT_USERNAME}/webapp"
    
    async def verify_telegram_data(self, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Проверяет данные, полученные от Telegram
        
        Args:
            data: Данные от Telegram
            
        Returns:
            Проверенные данные или None
        """
        # Здесь должна быть проверка подписи данных
        # В реальном приложении нужно использовать crypto
        return data
    
    async def get_or_create_user(self, telegram_data: Dict[str, Any]) -> User:
        """
        Получает или создает пользователя на основе данных Telegram
        
        Args:
            telegram_data: Данные пользователя из Telegram
            
        Returns:
            Объект пользователя
        """
        telegram_id = str(telegram_data.get("id"))
        username = telegram_data.get("username")
        first_name = telegram_data.get("first_name")
        last_name = telegram_data.get("last_name")
        
        # Проверяем, существует ли пользователь
        user = await crud_user.get_by_telegram_id(telegram_id)
        if user:
            return user
        
        # Создаем нового пользователя
        user_in = UserCreate(
            username=username or f"tg_{telegram_id}",
            email=f"tg_{telegram_id}@telegram.com",  # Временный email
            telegram_id=telegram_id,
            telegram_username=username,
            full_name=f"{first_name} {last_name}".strip() if last_name else first_name,
            is_active=True,
            is_superuser=telegram_id in settings.TELEGRAM_ADMIN_IDS
        )
        
        return await crud_user.create(user_in)
    
    async def create_access_token(self, user: User) -> str:
        """
        Создает JWT токен для пользователя
        
        Args:
            user: Объект пользователя
            
        Returns:
            JWT токен
        """
        return create_access_token(
            subject=user.id,
            expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        )

# Создаем экземпляр сервиса
telegram_auth_service = TelegramAuthService() 