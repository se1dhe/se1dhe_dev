from typing import Any, Optional, Union
import json
import pickle
from redis import Redis
from ..config import settings

class CacheService:
    def __init__(self):
        self.redis = Redis.from_url(settings.REDIS_URL)

    async def get(self, key: str) -> Optional[Any]:
        """Получение значения из кэша"""
        value = self.redis.get(key)
        if value is None:
            return None
        try:
            return pickle.loads(value)
        except pickle.UnpicklingError:
            try:
                return json.loads(value)
            except json.JSONDecodeError:
                return value.decode('utf-8')

    async def set(
        self,
        key: str,
        value: Any,
        expire: Optional[int] = None
    ) -> None:
        """Сохранение значения в кэш"""
        if isinstance(value, (str, int, float, bool)):
            value = str(value).encode('utf-8')
        elif isinstance(value, (dict, list)):
            value = json.dumps(value).encode('utf-8')
        else:
            value = pickle.dumps(value)

        self.redis.set(key, value, ex=expire)

    async def delete(self, key: str) -> None:
        """Удаление значения из кэша"""
        self.redis.delete(key)

    async def exists(self, key: str) -> bool:
        """Проверка существования ключа в кэше"""
        return bool(self.redis.exists(key))

    async def increment(self, key: str, amount: int = 1) -> int:
        """Увеличение числового значения в кэше"""
        return self.redis.incr(key, amount)

    async def decrement(self, key: str, amount: int = 1) -> int:
        """Уменьшение числового значения в кэше"""
        return self.redis.decr(key, amount)

    def get_key(self, prefix: str, *args) -> str:
        """Генерация ключа кэша"""
        return f"{prefix}:{':'.join(str(arg) for arg in args)}"

    # Специфичные методы для нашего приложения
    async def get_popular_bots(self, category_id: Optional[int] = None) -> Optional[list]:
        """Получение популярных ботов из кэша"""
        key = self.get_key("popular_bots", category_id or "all")
        return await self.get(key)

    async def set_popular_bots(
        self,
        bots: list,
        category_id: Optional[int] = None,
        expire: int = 3600
    ) -> None:
        """Сохранение популярных ботов в кэш"""
        key = self.get_key("popular_bots", category_id or "all")
        await self.set(key, bots, expire)

    async def get_user_preferences(self, user_id: int) -> Optional[dict]:
        """Получение предпочтений пользователя из кэша"""
        key = self.get_key("user_preferences", user_id)
        return await self.get(key)

    async def set_user_preferences(
        self,
        user_id: int,
        preferences: dict,
        expire: int = 3600
    ) -> None:
        """Сохранение предпочтений пользователя в кэш"""
        key = self.get_key("user_preferences", user_id)
        await self.set(key, preferences, expire)

    async def get_recommendations(
        self,
        user_id: int,
        category_id: Optional[int] = None
    ) -> Optional[list]:
        """Получение рекомендаций из кэша"""
        key = self.get_key("recommendations", user_id, category_id or "all")
        return await self.get(key)

    async def set_recommendations(
        self,
        user_id: int,
        recommendations: list,
        category_id: Optional[int] = None,
        expire: int = 1800
    ) -> None:
        """Сохранение рекомендаций в кэш"""
        key = self.get_key("recommendations", user_id, category_id or "all")
        await self.set(key, recommendations, expire) 