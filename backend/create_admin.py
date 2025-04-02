import os
import sys
from passlib.context import CryptContext
from dotenv import load_dotenv

# Добавляем путь к корневой директории проекта
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.app.core.config import settings

# Загружаем переменные окружения
load_dotenv()

def create_admin():
    # Создаем контекст для хеширования паролей
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    
    # Хешируем пароль администратора
    hashed_password = pwd_context.hash(settings.ADMIN_PASSWORD)
    
    # Создаем SQL-запрос для создания/обновления администратора
    sql_query = f"""
    INSERT INTO users (email, username, hashed_password, is_active, is_superuser, role)
    VALUES (
        '{settings.ADMIN_EMAIL}',
        '{settings.ADMIN_USERNAME}',
        '{hashed_password}',
        1,
        1,
        'ADMIN'
    )
    ON DUPLICATE KEY UPDATE
        hashed_password = '{hashed_password}',
        is_active = 1,
        is_superuser = 1,
        role = 'ADMIN';
    """
    
    print("SQL Query:")
    print(sql_query)

if __name__ == "__main__":
    create_admin() 