import logging
import logging.config
import os
from logging.handlers import RotatingFileHandler
from pathlib import Path
from typing import Optional

from backend.config.logging_config import LOGGING_CONFIG, LOG_DIR

def setup_logger(
    name: str,
    log_file: Optional[str] = None,
    level: int = logging.DEBUG,
    max_bytes: int = 10 * 1024 * 1024,  # 10MB
    backup_count: int = 5,
    format: Optional[str] = None
) -> logging.Logger:
    """
    Настраивает и возвращает логгер с указанными параметрами.
    
    Args:
        name: Имя логгера
        log_file: Путь к файлу логов (если None, используется конфигурация из LOGGING_CONFIG)
        level: Уровень логирования
        max_bytes: Максимальный размер файла логов
        backup_count: Количество файлов для ротации
        format: Формат сообщений логов
        
    Returns:
        logging.Logger: Настроенный логгер
    """
    # Создаем директорию для логов, если она не существует
    os.makedirs(LOG_DIR, exist_ok=True)
    
    # Если файл логов не указан, используем конфигурацию из LOGGING_CONFIG
    if log_file is None:
        logging.config.dictConfig(LOGGING_CONFIG)
        return logging.getLogger(name)
    
    # Создаем логгер
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    # Формат сообщений
    if format is None:
        format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    
    formatter = logging.Formatter(format)
    
    # Обработчик для файла
    file_handler = RotatingFileHandler(
        log_file,
        maxBytes=max_bytes,
        backupCount=backup_count,
        encoding='utf-8'
    )
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    
    # Обработчик для консоли
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    return logger 