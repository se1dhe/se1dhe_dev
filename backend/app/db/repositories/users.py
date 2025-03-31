from typing import Any, Dict, Optional, Union, List
from sqlalchemy.orm import Session
from backend.app.db.repositories.base import BaseRepository
from backend.app.models.user import User
from backend.app.schemas.user import UserCreate, UserUpdate
from backend.app.core.security import get_password_hash, verify_password


class UserRepository(BaseRepository[User, UserCreate, UserUpdate]):
    def get_by_email(self, db: Session, *, email: str) -> Optional[User]:
        """Получить пользователя по email"""
        return db.query(User).filter(User.email == email).first()

    def get_by_username(self, db: Session, *, username: str) -> Optional[User]:
        """Получить пользователя по имени пользователя"""
        return db.query(User).filter(User.username == username).first()

    def get_by_telegram_id(self, db: Session, *, telegram_id: str) -> Optional[User]:
        """Получить пользователя по ID Telegram"""
        return db.query(User).filter(User.telegram_id == telegram_id).first()

    def create(self, db: Session, *, obj_in: UserCreate) -> User:
        """Создать нового пользователя с хешированным паролем"""
        db_obj = User(
            email=obj_in.email,
            username=obj_in.username,
            hashed_password=get_password_hash(obj_in.password),
            full_name=obj_in.full_name,
            is_superuser=obj_in.is_superuser,
            telegram_id=obj_in.telegram_id,
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
            self, db: Session, *, db_obj: User, obj_in: Union[UserUpdate, Dict[str, Any]]
    ) -> User:
        """Обновить данные пользователя"""
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)

        # Если в обновлении есть пароль, хешируем его
        if "password" in update_data:
            hashed_password = get_password_hash(update_data["password"])
            del update_data["password"]
            update_data["hashed_password"] = hashed_password

        return super().update(db, db_obj=db_obj, obj_in=update_data)

    def authenticate(self, db: Session, *, email: str, password: str) -> Optional[User]:
        """Аутентифицировать пользователя по email и паролю"""
        user = self.get_by_email(db, email=email)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user

    def is_active(self, user: User) -> bool:
        """Проверить, активен ли пользователь"""
        return user.is_active

    def is_superuser(self, user: User) -> bool:
        """Проверить, является ли пользователь суперпользователем"""
        return user.is_superuser

    def get_subscribed_bots(self, db: Session, *, user_id: int) -> List[Any]:
        """Получить список ботов, на которые подписан пользователь"""
        user = self.get(db, id=user_id)
        if not user:
            return []
        return [subscription.bot for subscription in user.subscriptions if subscription.is_active]


user_repository = UserRepository(User)