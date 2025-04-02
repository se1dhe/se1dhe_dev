from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from app.core.config import settings
from app.services.telegram_auth import telegram_auth_service

class TelegramBotService:
    def __init__(self):
        if settings.TELEGRAM_BOT_ENABLED:
            self.bot = Bot(token=settings.TELEGRAM_BOT_TOKEN)
            self.dp = Dispatcher()
            self._setup_handlers()
        else:
            self.bot = None
            self.dp = None
    
    def _setup_handlers(self):
        """Настройка обработчиков команд и сообщений"""
        if not self.dp:
            return

        # Команда /start
        @self.dp.message(Command("start"))
        async def cmd_start(message: Message):
            await message.answer(
                "Привет! Я бот для авторизации на сайте Telegram Bots Marketplace.\n"
                "Используйте меня для входа на сайт через Telegram."
            )
        
        # Команда /login
        @self.dp.message(Command("login"))
        async def cmd_login(message: Message):
            login_url = await telegram_auth_service.get_login_url(message.from_user.id)
            await message.answer(
                "Для входа на сайт через Telegram, перейдите по ссылке:",
                reply_markup=types.InlineKeyboardMarkup(
                    inline_keyboard=[
                        [
                            types.InlineKeyboardButton(
                                text="Войти через Telegram",
                                url=login_url.url
                            )
                        ]
                    ]
                )
            )
    
    async def start(self):
        """Запуск бота в режиме longpolling"""
        if not settings.TELEGRAM_BOT_ENABLED:
            print("Telegram bot is disabled")
            return

        try:
            await self.dp.start_polling(
                self.bot,
                polling_interval=settings.TELEGRAM_POLLING_INTERVAL,
                polling_timeout=settings.TELEGRAM_POLLING_TIMEOUT
            )
        finally:
            if self.bot:
                await self.bot.session.close()

# Создаем экземпляр сервиса
telegram_bot_service = TelegramBotService() 