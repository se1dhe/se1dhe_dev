import asyncio
import uvicorn
import logging
from app.services.telegram_bot import telegram_bot_service

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

async def run_bot():
    """Запуск Telegram бота"""
    try:
        logger.info("Starting Telegram bot...")
        await telegram_bot_service.start()
    except Exception as e:
        logger.error(f"Error starting bot: {e}")
        raise

def run_api():
    """Запуск FastAPI приложения"""
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )

async def main():
    """Запуск всех компонентов приложения"""
    # Запускаем бота в отдельной задаче
    bot_task = asyncio.create_task(run_bot())
    
    # Запускаем API в основном потоке
    run_api()
    
    # Ждем завершения задачи бота
    await bot_task

if __name__ == "__main__":
    asyncio.run(main()) 