from typing import List, Optional
from datetime import datetime

from sqlalchemy.orm import Session, joinedload
from sqlalchemy import desc

from app.models.feature_request import FeatureComment
from app.schemas.feature_request import FeatureCommentCreate, FeatureCommentUpdate
from .base import CRUDBase


class CRUDFeatureComment(CRUDBase[FeatureComment, FeatureCommentCreate, FeatureCommentUpdate]):
    """CRUD операции для комментариев к запросам функций"""
    
    def get_by_feature(
        self, db: Session, *, feature_id: int, skip: int = 0, limit: int = 100
    ) -> List[FeatureComment]:
        """
        Получить комментарии для конкретного запроса функции
        
        Args:
            db: Сессия БД
            feature_id: ID запроса функции
            skip: Сколько записей пропустить
            limit: Максимальное количество записей
            
        Returns:
            Список комментариев для запроса
        """
        return (
            db.query(FeatureComment)
            .filter(FeatureComment.feature_id == feature_id)
            .order_by(desc(FeatureComment.created_at))
            .offset(skip)
            .limit(limit)
            .all()
        )
    
    def get_with_user(self, db: Session, id: int) -> Optional[FeatureComment]:
        """
        Получить комментарий с информацией о пользователе
        
        Args:
            db: Сессия БД
            id: ID комментария
            
        Returns:
            FeatureComment с загруженным пользователем или None
        """
        return (
            db.query(FeatureComment)
            .filter(FeatureComment.id == id)
            .options(joinedload(FeatureComment.user))
            .first()
        )
    
    def get_by_feature_with_users(
        self, db: Session, *, feature_id: int, skip: int = 0, limit: int = 100
    ) -> List[FeatureComment]:
        """
        Получить комментарии для запроса с информацией о пользователях
        
        Args:
            db: Сессия БД
            feature_id: ID запроса функции
            skip: Сколько записей пропустить
            limit: Максимальное количество записей
            
        Returns:
            Список комментариев с загруженными пользователями
        """
        return (
            db.query(FeatureComment)
            .filter(FeatureComment.feature_id == feature_id)
            .options(joinedload(FeatureComment.user))
            .order_by(desc(FeatureComment.created_at))
            .offset(skip)
            .limit(limit)
            .all()
        )
    
    def count_by_feature(self, db: Session, *, feature_id: int) -> int:
        """
        Подсчитать количество комментариев для запроса
        
        Args:
            db: Сессия БД
            feature_id: ID запроса функции
            
        Returns:
            Количество комментариев
        """
        return db.query(FeatureComment).filter(FeatureComment.feature_id == feature_id).count()


# Создание экземпляра CRUD для использования в API
feature_comment = CRUDFeatureComment(FeatureComment) 