from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.enums import ParseMode
from loguru import logger
import os
from dotenv import load_dotenv

# Загрузка переменных окружения
load_dotenv()

# Настройка логгера
logger.add(
    os.path.join(os.getenv("LOG_DIR", "logs"), "bot.log"),
    rotation="500 MB",
    retention="10 days",
    level=os.getenv("LOG_LEVEL", "INFO"),
    format=os.getenv("LOG_FORMAT", "%(asctime)s - %(name)s - %(levelname)s - %(message)s"),
    encoding="utf-8"
)

# Инициализация бота и диспетчера
bot = Bot(token=os.getenv("TELEGRAM_BOT_TOKEN"), parse_mode=ParseMode.HTML)
dp = Dispatcher()

@dp.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer(
        "👋 Привет! Я бот для покупки Telegram ботов.\n\n"
        "Используйте команды:\n"
        "/catalog - Просмотр каталога ботов\n"
        "/balance - Проверка баланса\n"
        "/help - Помощь"
    )

@dp.message(Command("help"))
async def cmd_help(message: Message):
    await message.answer(
        "📚 Список доступных команд:\n\n"
        "/start - Начать работу с ботом\n"
        "/catalog - Просмотр каталога ботов\n"
        "/balance - Проверка баланса\n"
        "/help - Показать это сообщение"
    )

@dp.message(Command("catalog"))
async def cmd_catalog(message: Message):
    await message.answer("📋 Каталог ботов будет доступен в ближайшее время!")

@dp.message(Command("balance"))
async def cmd_balance(message: Message):
    await message.answer("💰 Проверка баланса будет доступна в ближайшее время!")

async def main():
    logger.info("Starting bot...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main()) 