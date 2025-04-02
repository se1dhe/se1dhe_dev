from typing import Any, Optional
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi_cache.decorator import cache
from redis import asyncio as aioredis

from app.core.config import settings

async def init_cache():
    """Инициализация кэша Redis"""
    redis = aioredis.from_url(settings.REDIS_URL)
    FastAPICache.init(
        backend=RedisBackend(redis),
        prefix="fastapi-cache",
        expire=60 * 5  # 5 минут по умолчанию
    )

def cache_key_builder(
    func,
    namespace: Optional[str] = "",
    *,
    user_id: Optional[int] = None,
    **kwargs: Any
) -> str:
    """
    Построитель ключей кэша с учетом пользователя
    
    Args:
        func: Кэшируемая функция
        namespace: Пространство имен
        user_id: ID пользователя
        **kwargs: Дополнительные параметры
        
    Returns:
        Ключ кэша
    """
    prefix = f"{namespace}:" if namespace else ""
    cache_key = f"{prefix}{func.__module__}:{func.__name__}"
    
    if user_id is not None:
        cache_key = f"{cache_key}:user:{user_id}"
    
    if kwargs:
        kwargs_str = ":".join(f"{k}={v}" for k, v in sorted(kwargs.items()))
        cache_key = f"{cache_key}:{kwargs_str}"
    
    return cache_key

def cached(
    *,
    expire: int = 60 * 5,  # 5 минут по умолчанию
    namespace: Optional[str] = None,
    user_specific: bool = False
):
    """
    Декоратор для кэширования с учетом пользователя
    
    Args:
        expire: Время жизни кэша в секундах
        namespace: Пространство имен
        user_specific: Учитывать ли ID пользователя в ключе кэша
        
    Returns:
        Декоратор кэширования
    """
    def decorator(func):
        async def wrapper(*args, **kwargs):
            # Если кэширование с учетом пользователя, ищем user_id в аргументах
            user_id = None
            if user_specific:
                for arg in args:
                    if hasattr(arg, "id"):
                        user_id = arg.id
                        break
            
            # Создаем ключ кэша
            key = cache_key_builder(
                func,
                namespace=namespace,
                user_id=user_id,
                **kwargs
            )
            
            # Применяем декоратор кэширования
            cached_func = cache(
                expire=expire,
                namespace=namespace,
                key_builder=lambda *a, **kw: key
            )(func)
            
            return await cached_func(*args, **kwargs)
        return wrapper
    return decorator 