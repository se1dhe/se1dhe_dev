import logging
import os
from pathlib import Path
import pytest

from backend.utils.logger import setup_logger
from backend.config.logging_config import LOG_DIR

@pytest.fixture
def test_log_file(tmp_path):
    """Создает временный файл для тестовых логов"""
    log_file = tmp_path / "test.log"
    return str(log_file)

def test_setup_logger_with_file(test_log_file):
    """Тестирует создание логгера с файлом"""
    logger = setup_logger("test_logger", test_log_file)
    
    # Проверяем, что логгер создан
    assert logger.name == "test_logger"
    assert logger.level == logging.DEBUG
    
    # Проверяем наличие обработчиков
    assert len(logger.handlers) == 2  # FileHandler и StreamHandler
    
    # Проверяем, что файл создан
    assert os.path.exists(test_log_file)

def test_setup_logger_without_file():
    """Тестирует создание логгера без файла"""
    logger = setup_logger("test_logger")
    
    # Проверяем, что логгер создан
    assert logger.name == "test_logger"
    assert logger.level == logging.DEBUG

def test_logger_output(test_log_file):
    """Тестирует запись логов"""
    logger = setup_logger("test_logger", test_log_file)
    test_message = "Test log message"
    
    logger.info(test_message)
    
    # Проверяем, что сообщение записано в файл
    with open(test_log_file, 'r') as f:
        log_content = f.read()
        assert test_message in log_content

def test_log_rotation(test_log_file):
    """Тестирует ротацию логов"""
    logger = setup_logger("test_logger", test_log_file, max_bytes=100)
    
    # Записываем достаточно данных для ротации
    for i in range(100):
        logger.info(f"Test message {i}")
    
    # Проверяем наличие файлов ротации
    log_files = list(Path(test_log_file).parent.glob("test.log*"))
    assert len(log_files) > 1

def test_custom_format(test_log_file):
    """Тестирует пользовательский формат логов"""
    custom_format = "%(levelname)s - %(message)s"
    logger = setup_logger("test_logger", test_log_file, format=custom_format)
    
    logger.info("Test message")
    
    with open(test_log_file, 'r') as f:
        log_content = f.read()
        assert "INFO - Test message" in log_content

def test_log_level(test_log_file):
    """Тестирует уровни логирования"""
    logger = setup_logger("test_logger", test_log_file, level=logging.WARNING)
    
    logger.debug("Debug message")
    logger.info("Info message")
    logger.warning("Warning message")
    
    with open(test_log_file, 'r') as f:
        log_content = f.read()
        assert "Debug message" not in log_content
        assert "Info message" not in log_content
        assert "Warning message" in log_content 