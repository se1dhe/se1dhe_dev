from typing import List, Union
from pydantic import AnyHttpUrl, validator
from pydantic_settings import BaseSettings
from pathlib import Path

# Get the backend directory path
BACKEND_DIR = Path(__file__).resolve().parent.parent.parent

class Settings(BaseSettings):
    # Project settings
    PROJECT_NAME: str
    VERSION: str
    API_V1_STR: str
    
    # Database Configuration
    MYSQL_USER: str
    MYSQL_PASSWORD: str
    MYSQL_HOST: str
    MYSQL_PORT: str
    MYSQL_DB: str
    
    @property
    def SQLALCHEMY_DATABASE_URI(self) -> str:
        return f"mysql+pymysql://{self.MYSQL_USER}:{self.MYSQL_PASSWORD}@{self.MYSQL_HOST}:{self.MYSQL_PORT}/{self.MYSQL_DB}"

    # Redis Configuration
    REDIS_HOST: str
    REDIS_PORT: int
    REDIS_DB: int
    REDIS_PASSWORD: str
    
    @property
    def REDIS_URL(self) -> str:
        if self.REDIS_PASSWORD:
            return f"redis://:{self.REDIS_PASSWORD}@{self.REDIS_HOST}:{self.REDIS_PORT}/{self.REDIS_DB}"
        return f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}/{self.REDIS_DB}"

    # JWT Configuration
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8  # 8 days

    # Frontend URL for CORS
    FRONTEND_URL: str
    
    # CORS Configuration
    BACKEND_CORS_ORIGINS: List[str]

    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> List[str]:
        if isinstance(v, str):
            return [i.strip() for i in v.split(",")]
        return v

    # Telegram Configuration
    TELEGRAM_BOT_ENABLED: bool
    TELEGRAM_BOT_TOKEN: str
    TELEGRAM_API_ID: str
    TELEGRAM_API_HASH: str
    TELEGRAM_BOT_USERNAME: str
    TELEGRAM_ADMIN_IDS: List[int]
    
    # Longpolling settings
    TELEGRAM_POLLING_INTERVAL: float = 1.0  # seconds
    TELEGRAM_POLLING_TIMEOUT: float = 30.0  # seconds

    # Admin credentials
    ADMIN_USERNAME: str
    ADMIN_PASSWORD: str

    @validator("TELEGRAM_ADMIN_IDS", pre=True)
    def assemble_admin_ids(cls, v: Union[str, List[int]]) -> List[int]:
        if isinstance(v, str):
            return [int(i.strip()) for i in v.split(",")]
        elif isinstance(v, list):
            return v
        raise ValueError(v)

    class Config:
        case_sensitive = True
        env_file = BACKEND_DIR / ".env"
        env_file_encoding = "utf-8"

settings = Settings() 