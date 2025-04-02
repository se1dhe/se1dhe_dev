from typing import Any, Dict, Optional, Union, List

from sqlalchemy.orm import Session

from app.core.security import get_password_hash, verify_password
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate
from .base import CRUDBase


class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):
    """
    CRUD операции для пользователей с дополнительной логикой безопасности
    """
    
    def get_by_email(self, db: Session, *, email: str) -> Optional[User]:
        """
        Получить пользователя по email
        
        Args:
            db: Сессия БД
            email: Email пользователя
            
        Returns:
            User или None, если пользователь не найден
        """
        return db.query(User).filter(User.email == email).first()
    
    def get_by_username(self, db: Session, *, username: str) -> Optional[User]:
        """
        Получить пользователя по имени пользователя
        
        Args:
            db: Сессия БД
            username: Имя пользователя
            
        Returns:
            User или None, если пользователь не найден
        """
        return db.query(User).filter(User.username == username).first()
        
    def get_by_telegram_id(self, db: Session, *, telegram_id: str) -> Optional[User]:
        """
        Получить пользователя по ID в Telegram
        
        Args:
            db: Сессия БД
            telegram_id: ID пользователя в Telegram
            
        Returns:
            User или None, если пользователь не найден
        """
        return db.query(User).filter(User.telegram_id == telegram_id).first()

    def create(self, db: Session, *, obj_in: UserCreate) -> User:
        """
        Создать нового пользователя с хешированием пароля
        
        Args:
            db: Сессия БД
            obj_in: Данные для создания пользователя
            
        Returns:
            Созданный объект пользователя
        """
        db_obj = User(
            email=obj_in.email,
            username=obj_in.username,
            hashed_password=get_password_hash(obj_in.password),
            telegram_id=obj_in.telegram_id,
            is_active=obj_in.is_active,
            is_superuser=obj_in.is_superuser,
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
        self, db: Session, *, db_obj: User, obj_in: Union[UserUpdate, Dict[str, Any]]
    ) -> User:
        """
        Обновить пользователя, с особой обработкой пароля
        
        Args:
            db: Сессия БД
            db_obj: Существующий объект пользователя
            obj_in: Данные для обновления
            
        Returns:
            Обновленный объект пользователя
        """
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
            
        if update_data.get("password"):
            hashed_password = get_password_hash(update_data["password"])
            del update_data["password"]
            update_data["hashed_password"] = hashed_password
            
        return super().update(db, db_obj=db_obj, obj_in=update_data)

    def authenticate(
        self, db: Session, *, email: str, password: str
    ) -> Optional[User]:
        """
        Аутентифицировать пользователя по email и паролю
        
        Args:
            db: Сессия БД
            email: Email пользователя
            password: Пароль в открытом виде
            
        Returns:
            User если аутентификация успешна, иначе None
        """
        user = self.get_by_email(db, email=email)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user

    def is_active(self, user: User) -> bool:
        """
        Проверить, активен ли пользователь
        
        Args:
            user: Объект пользователя
            
        Returns:
            bool: True если пользователь активен
        """
        return user.is_active

    def is_superuser(self, user: User) -> bool:
        """
        Проверить, является ли пользователь суперпользователем
        
        Args:
            user: Объект пользователя
            
        Returns:
            bool: True если пользователь является суперпользователем
        """
        return user.is_superuser
        
    def get_users_with_subscriptions(
        self, db: Session, *, skip: int = 0, limit: int = 100
    ) -> List[User]:
        """
        Получить пользователей с их подписками
        
        Args:
            db: Сессия БД
            skip: Сколько записей пропустить
            limit: Максимальное количество записей
            
        Returns:
            Список пользователей с загруженными подписками
        """
        return (
            db.query(User)
            .offset(skip)
            .limit(limit)
            .all()
        )


# Создание экземпляра CRUD для использования в API
user = CRUDUser(User) 