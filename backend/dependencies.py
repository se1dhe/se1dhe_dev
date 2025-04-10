from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from typing import Generator
from . import crud, utils, exceptions
from .database import get_db
from .config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/auth/token")

def get_current_user(
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme)
) -> crud.User:
    """Получение текущего пользователя"""
    payload = utils.verify_token(token)
    if payload is None:
        raise exceptions.InvalidToken()
    
    user_id = payload.get("sub")
    if user_id is None:
        raise exceptions.InvalidToken()
    
    user = crud.get_user(db, user_id=user_id)
    if user is None:
        raise exceptions.UserNotFound(user_id)
    
    return user

def get_current_active_user(
    current_user: crud.User = Depends(get_current_user)
) -> crud.User:
    """Получение текущего активного пользователя"""
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

def get_current_admin_user(
    current_user: crud.User = Depends(get_current_user)
) -> crud.User:
    """Получение текущего администратора"""
    if current_user.role != "admin":
        raise exceptions.PermissionDenied()
    return current_user

def get_db_session() -> Generator[Session, None, None]:
    """Получение сессии базы данных"""
    db = get_db()
    try:
        yield db
    finally:
        db.close()

def get_redis_client():
    """Получение клиента Redis"""
    import redis
    return redis.Redis(
        host=settings.REDIS_HOST,
        port=settings.REDIS_PORT,
        password=settings.REDIS_PASSWORD,
        decode_responses=True
    )

def get_telegram_bot():
    """Получение экземпляра Telegram бота"""
    from aiogram import Bot
    return Bot(token=settings.TELEGRAM_BOT_TOKEN)

def get_payment_service():
    """Получение сервиса оплаты"""
    from .services.payment import PaymentService
    return PaymentService() 