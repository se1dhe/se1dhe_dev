from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from .config import settings
import uuid

# Настройка для хеширования паролей
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Проверка пароля"""
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """Хеширование пароля"""
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Создание JWT токена"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

def verify_token(token: str) -> Optional[dict]:
    """Проверка JWT токена"""
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return payload
    except JWTError:
        return None

def format_price(price: float) -> str:
    """Форматирование цены"""
    return f"{price:.2f}"

def calculate_discount_price(price: float, discount: float) -> float:
    """Расчет цены со скидкой"""
    return price * (1 - discount / 100)

def format_datetime(dt: datetime) -> str:
    """Форматирование даты и времени"""
    return dt.strftime("%Y-%m-%d %H:%M:%S")

def get_current_time() -> datetime:
    """Получение текущего времени"""
    return datetime.utcnow()

def generate_order_id() -> str:
    """Генерация уникального ID заказа"""
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    unique_id = str(uuid.uuid4())[:8]
    return f"ORDER-{timestamp}-{unique_id}"

def get_random_string(length: int) -> str:
    """Генерация случайной строки заданной длины"""
    import random
    import string
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length)) 