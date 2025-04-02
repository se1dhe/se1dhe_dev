from typing import List, Optional
from datetime import datetime

from sqlalchemy.orm import Session, joinedload
from sqlalchemy import desc

from app.models.changelog import Changelog
from app.schemas.changelog import ChangelogCreate, ChangelogUpdate
from .base import CRUDBase


class CRUDChangelog(CRUDBase[Changelog, ChangelogCreate, ChangelogUpdate]):
    """CRUD операции для версий обновлений (changelogs)"""
    
    def get_by_bot(
        self, db: Session, *, bot_id: int, skip: int = 0, limit: int = 100
    ) -> List[Changelog]:
        """
        Получить версии обновлений для конкретного бота
        
        Args:
            db: Сессия БД
            bot_id: ID бота
            skip: Сколько записей пропустить
            limit: Максимальное количество записей
            
        Returns:
            Список версий обновлений для бота
        """
        return (
            db.query(Changelog)
            .filter(Changelog.bot_id == bot_id)
            .order_by(desc(Changelog.release_date))
            .offset(skip)
            .limit(limit)
            .all()
        )
    
    def get_latest(self, db: Session, *, limit: int = 10) -> List[Changelog]:
        """
        Получить последние версии обновлений
        
        Args:
            db: Сессия БД
            limit: Максимальное количество записей
            
        Returns:
            Список последних версий обновлений
        """
        return (
            db.query(Changelog)
            .order_by(desc(Changelog.release_date))
            .limit(limit)
            .all()
        )
    
    def get_with_bot(self, db: Session, id: int) -> Optional[Changelog]:
        """
        Получить версию обновления с информацией о боте
        
        Args:
            db: Сессия БД
            id: ID версии обновления
            
        Returns:
            Changelog с загруженным связанным ботом или None
        """
        return (
            db.query(Changelog)
            .filter(Changelog.id == id)
            .options(joinedload(Changelog.bot))
            .first()
        )


# Создание экземпляра CRUD для использования в API
changelog = CRUDChangelog(Changelog) 