from typing import List, Optional
from datetime import datetime

from sqlalchemy.orm import Session
from sqlalchemy import and_

from app.models.feature_request import FeatureVote
from app.schemas.feature_request import FeatureVoteCreate
from .base import CRUDBase


class CRUDFeatureVote(CRUDBase[FeatureVote, FeatureVoteCreate, None]):
    """CRUD операции для голосов за запросы функций"""
    
    def get_by_user_and_feature(
        self, db: Session, *, user_id: int, feature_id: int
    ) -> Optional[FeatureVote]:
        """
        Получить голос пользователя за конкретный запрос
        
        Args:
            db: Сессия БД
            user_id: ID пользователя
            feature_id: ID запроса функции
            
        Returns:
            Объект голоса или None
        """
        return (
            db.query(FeatureVote)
            .filter(
                and_(
                    FeatureVote.user_id == user_id,
                    FeatureVote.feature_id == feature_id
                )
            )
            .first()
        )
    
    def get_by_feature(
        self, db: Session, *, feature_id: int, skip: int = 0, limit: int = 100
    ) -> List[FeatureVote]:
        """
        Получить все голоса за конкретный запрос
        
        Args:
            db: Сессия БД
            feature_id: ID запроса функции
            skip: Сколько записей пропустить
            limit: Максимальное количество записей
            
        Returns:
            Список голосов для запроса
        """
        return (
            db.query(FeatureVote)
            .filter(FeatureVote.feature_id == feature_id)
            .offset(skip)
            .limit(limit)
            .all()
        )
    
    def create_if_not_exists(
        self, db: Session, *, user_id: int, feature_id: int
    ) -> Optional[FeatureVote]:
        """
        Создать голос, если он еще не существует
        
        Args:
            db: Сессия БД
            user_id: ID пользователя
            feature_id: ID запроса функции
            
        Returns:
            Созданный голос или None, если голос уже существует
        """
        existing_vote = self.get_by_user_and_feature(
            db=db, user_id=user_id, feature_id=feature_id
        )
        
        if existing_vote:
            return None
            
        db_obj = FeatureVote(
            user_id=user_id,
            feature_id=feature_id,
            created_at=datetime.utcnow()
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj
    
    def count_by_feature(self, db: Session, *, feature_id: int) -> int:
        """
        Подсчитать количество голосов для запроса
        
        Args:
            db: Сессия БД
            feature_id: ID запроса функции
            
        Returns:
            Количество голосов
        """
        return db.query(FeatureVote).filter(FeatureVote.feature_id == feature_id).count()


# Создание экземпляра CRUD для использования в API
feature_vote = CRUDFeatureVote(FeatureVote) 