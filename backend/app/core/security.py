from datetime import datetime, timedelta
from typing import Any, Union, Optional

from jose import jwt
from passlib.context import CryptContext
from pydantic import ValidationError
import bcrypt

from app.core.config import settings
from app.schemas.token import TokenPayload


# Создаем контекст для хеширования паролей
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_access_token(
    subject: Union[str, Any], expires_delta: Optional[timedelta] = None
) -> str:
    """
    Создает JWT токен для аутентификации пользователя.
    
    Args:
        subject: Идентификатор пользователя или другие данные для включения в токен
        expires_delta: Срок действия токена (опционально)
        
    Returns:
        str: Закодированный JWT токен
    """
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
    
    to_encode = {"exp": expire, "sub": str(subject)}
    encoded_jwt = jwt.encode(
        to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM
    )
    return encoded_jwt


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Проверяет соответствие пароля в открытом виде его хешированной версии.
    
    Args:
        plain_password: Пароль в открытом виде
        hashed_password: Хешированный пароль
        
    Returns:
        bool: True если пароль верен, иначе False
    """
    # Если хеш начинается с b$, заменяем на $2b$
    if hashed_password.startswith('b$'):
        hashed_password = '$2b$' + hashed_password[2:]
    return bcrypt.checkpw(plain_password.encode(), hashed_password.encode())


def get_password_hash(password: str) -> str:
    """
    Хеширует пароль для безопасного хранения.
    
    Args:
        password: Пароль в открытом виде
        
    Returns:
        str: Хешированный пароль
    """
    # Генерируем хеш с правильным префиксом $2b$
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()


def decode_token(token: str) -> Optional[TokenPayload]:
    """
    Декодирует и проверяет JWT токен.
    
    Args:
        token: JWT токен для декодирования
        
    Returns:
        TokenPayload: Данные токена, если токен валиден
        None: Если токен невалиден
    """
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        token_data = TokenPayload(**payload)
        
        if datetime.fromtimestamp(token_data.exp) < datetime.utcnow():
            return None
        
        return token_data
    except (jwt.JWTError, ValidationError):
        return None 