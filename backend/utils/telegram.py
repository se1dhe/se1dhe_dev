import aiohttp
from ..config import settings

async def send_telegram_message(chat_id: int, text: str) -> None:
    """Отправка сообщения в Telegram"""
    url = f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/sendMessage"
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json={
                "chat_id": chat_id,
                "text": text,
                "parse_mode": "HTML"
            }) as response:
                if response.status != 200:
                    # TODO: Добавить логирование ошибок
                    print(f"Ошибка отправки Telegram сообщения: {await response.text()}")
    except Exception as e:
        # TODO: Добавить логирование ошибок
        print(f"Ошибка отправки Telegram сообщения: {e}") 