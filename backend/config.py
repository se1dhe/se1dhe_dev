from pydantic_settings import BaseSettings
from typing import List, Optional
import os
from dotenv import load_dotenv

# Загрузка переменных окружения
load_dotenv()

class Settings(BaseSettings):
    # Основные настройки
    PROJECT_NAME: str = os.getenv("PROJECT_NAME", "se1dhe_dev")
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    
    # Настройки базы данных
    MYSQL_DATABASE: str = os.getenv("MYSQL_DATABASE", "se1dhe_dev")
    MYSQL_USER: str = os.getenv("MYSQL_USER", "root")
    MYSQL_PASSWORD: str = os.getenv("MYSQL_PASSWORD", "1234")
    MYSQL_HOST: str = os.getenv("MYSQL_HOST", "mysql")
    MYSQL_PORT: int = int(os.getenv("MYSQL_PORT", "3306"))
    
    # Настройки Redis
    REDIS_HOST: str = os.getenv("REDIS_HOST", "redis")
    REDIS_PORT: int = int(os.getenv("REDIS_PORT", "6379"))
    REDIS_PASSWORD: str = os.getenv("REDIS_PASSWORD", "")
    
    # Настройки Telegram бота
    TELEGRAM_BOT_TOKEN: str = os.getenv("TELEGRAM_BOT_TOKEN", "")
    TELEGRAM_BOT_USERNAME: str = os.getenv("TELEGRAM_BOT_USERNAME", "")
    
    # Настройки NGROK
    NGROK_AUTH_TOKEN: str = os.getenv("NGROK_AUTH_TOKEN", "")
    NGROK_REGION: str = os.getenv("NGROK_REGION", "eu")
    
    # Настройки платежных систем
    PAYKASSA_API_ID: str = os.getenv("PAYKASSA_API_ID", "")
    PAYKASSA_API_PASSWORD: str = os.getenv("PAYKASSA_API_PASSWORD", "")
    PAYKASSA_SHOP_ID: str = os.getenv("PAYKASSA_SHOP_ID", "")
    PAYKASSA_SECRET_KEY: str = os.getenv("PAYKASSA_SECRET_KEY", "")
    FREEKASSA_SHOP_ID: str = os.getenv("FREEKASSA_SHOP_ID", "")
    FREEKASSA_SECRET_KEY: str = os.getenv("FREEKASSA_SECRET_KEY", "")
    
    # Настройки логирования
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    LOG_DIR: str = "logs/backend"
    LOG_FILE: str = "app.log"
    
    # Настройки безопасности
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key")
    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
    
    # Настройки CORS
    CORS_ORIGINS: List[str] = eval(os.getenv("CORS_ORIGINS", "[]"))
    
    # Email
    SMTP_HOST: str = os.getenv("SMTP_HOST", "smtp.gmail.com")
    SMTP_PORT: int = int(os.getenv("SMTP_PORT", "587"))
    SMTP_USERNAME: str = os.getenv("SMTP_USERNAME", "your-email@gmail.com")
    SMTP_PASSWORD: str = os.getenv("SMTP_PASSWORD", "your-app-password")
    SMTP_FROM_EMAIL: str = os.getenv("SMTP_FROM_EMAIL", "your-email@gmail.com")
    
    # Redis
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    REDIS_CACHE_TTL: int = int(os.getenv("REDIS_CACHE_TTL", "3600"))  # Время жизни кэша в секундах
    
    class Config:
        case_sensitive = True
        env_file = ".env"

settings = Settings() 