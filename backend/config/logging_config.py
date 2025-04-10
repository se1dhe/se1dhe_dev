import os
from pathlib import Path

# Базовый путь для логов
BASE_DIR = Path(__file__).resolve().parent.parent
LOG_DIR = os.path.join(BASE_DIR, 'logs')

# Настройки логирования
LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        },
        'detailed': {
            'format': '%(asctime)s - %(name)s - %(levelname)s - %(module)s - %(funcName)s - %(lineno)d - %(message)s'
        }
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'level': 'INFO',
            'formatter': 'standard',
            'stream': 'ext://sys.stdout'
        },
        'file': {
            'class': 'logging.handlers.RotatingFileHandler',
            'level': 'DEBUG',
            'formatter': 'detailed',
            'filename': os.path.join(LOG_DIR, 'app.log'),
            'maxBytes': 10 * 1024 * 1024,  # 10MB
            'backupCount': 5,
            'encoding': 'utf-8'
        },
        'error_file': {
            'class': 'logging.handlers.RotatingFileHandler',
            'level': 'ERROR',
            'formatter': 'detailed',
            'filename': os.path.join(LOG_DIR, 'error.log'),
            'maxBytes': 10 * 1024 * 1024,  # 10MB
            'backupCount': 5,
            'encoding': 'utf-8'
        }
    },
    'loggers': {
        '': {  # Корневой логгер
            'handlers': ['console', 'file', 'error_file'],
            'level': 'DEBUG',
            'propagate': True
        },
        'app': {
            'handlers': ['console', 'file', 'error_file'],
            'level': 'DEBUG',
            'propagate': False
        },
        'sqlalchemy.engine': {
            'handlers': ['file'],
            'level': 'INFO',
            'propagate': False
        }
    }
} 