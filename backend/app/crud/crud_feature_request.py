from typing import List, Optional, Dict, Any, Union
from datetime import datetime

from sqlalchemy.orm import Session, joinedload
from sqlalchemy import desc, func, and_

from app.models.feature_request import (
    FeatureRequest, FeatureRequestStatus as DBFeatureRequestStatus,
    FeaturePriority as DBFeaturePriority
)
from app.schemas.feature_request import (
    FeatureRequestCreate, FeatureRequestUpdate, 
    FeatureRequestStatus, FeaturePriority
)
from .base import CRUDBase


class CRUDFeatureRequest(CRUDBase[FeatureRequest, FeatureRequestCreate, FeatureRequestUpdate]):
    """CRUD операции для запросов на новые функции"""
    
    def create(self, db: Session, *, obj_in: FeatureRequestCreate) -> FeatureRequest:
        """
        Создать новый запрос на функцию
        
        Args:
            db: Сессия БД
            obj_in: Данные для создания запроса
            
        Returns:
            Созданный объект запроса
        """
        db_obj = FeatureRequest(
            user_id=obj_in.user_id,
            bot_id=obj_in.bot_id,
            title=obj_in.title,
            description=obj_in.description,
            technical_details=obj_in.technical_details,
            status=DBFeatureRequestStatus.PROPOSED,
            priority=DBFeaturePriority[obj_in.priority.upper()],
            is_public=obj_in.is_public,
            votes_count=0,
            created_at=datetime.utcnow()
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj
    
    def get_by_user(
        self, db: Session, *, user_id: int, skip: int = 0, limit: int = 100
    ) -> List[FeatureRequest]:
        """
        Получить запросы, созданные конкретным пользователем
        
        Args:
            db: Сессия БД
            user_id: ID пользователя
            skip: Сколько записей пропустить
            limit: Максимальное количество записей
            
        Returns:
            Список запросов пользователя
        """
        return (
            db.query(FeatureRequest)
            .filter(FeatureRequest.user_id == user_id)
            .order_by(desc(FeatureRequest.created_at))
            .offset(skip)
            .limit(limit)
            .all()
        )
    
    def get_by_bot(
        self, db: Session, *, bot_id: int, skip: int = 0, limit: int = 100, 
        is_public_only: bool = False
    ) -> List[FeatureRequest]:
        """
        Получить запросы для конкретного бота
        
        Args:
            db: Сессия БД
            bot_id: ID бота
            skip: Сколько записей пропустить
            limit: Максимальное количество записей
            is_public_only: Только публичные запросы
            
        Returns:
            Список запросов для бота
        """
        query = db.query(FeatureRequest).filter(FeatureRequest.bot_id == bot_id)
        
        if is_public_only:
            query = query.filter(FeatureRequest.is_public == True)
            
        return (
            query
            .order_by(desc(FeatureRequest.votes_count), desc(FeatureRequest.created_at))
            .offset(skip)
            .limit(limit)
            .all()
        )
    
    def get_by_status(
        self, db: Session, *, status: FeatureRequestStatus, skip: int = 0, limit: int = 100
    ) -> List[FeatureRequest]:
        """
        Получить запросы с определенным статусом
        
        Args:
            db: Сессия БД
            status: Статус запроса
            skip: Сколько записей пропустить
            limit: Максимальное количество записей
            
        Returns:
            Список запросов с указанным статусом
        """
        db_status = DBFeatureRequestStatus[status.upper()]
        return (
            db.query(FeatureRequest)
            .filter(FeatureRequest.status == db_status)
            .order_by(desc(FeatureRequest.votes_count), desc(FeatureRequest.created_at))
            .offset(skip)
            .limit(limit)
            .all()
        )
    
    def get_by_priority(
        self, db: Session, *, priority: FeaturePriority, skip: int = 0, limit: int = 100
    ) -> List[FeatureRequest]:
        """
        Получить запросы с определенным приоритетом
        
        Args:
            db: Сессия БД
            priority: Приоритет запроса
            skip: Сколько записей пропустить
            limit: Максимальное количество записей
            
        Returns:
            Список запросов с указанным приоритетом
        """
        db_priority = DBFeaturePriority[priority.upper()]
        return (
            db.query(FeatureRequest)
            .filter(FeatureRequest.priority == db_priority)
            .order_by(desc(FeatureRequest.votes_count), desc(FeatureRequest.created_at))
            .offset(skip)
            .limit(limit)
            .all()
        )
    
    def get_top_voted(
        self, db: Session, *, bot_id: Optional[int] = None, limit: int = 10
    ) -> List[FeatureRequest]:
        """
        Получить самые популярные запросы (с наибольшим количеством голосов)
        
        Args:
            db: Сессия БД
            bot_id: ID бота (если нужны запросы только для конкретного бота)
            limit: Максимальное количество записей
            
        Returns:
            Список самых популярных запросов
        """
        query = db.query(FeatureRequest).filter(FeatureRequest.is_public == True)
        
        if bot_id:
            query = query.filter(FeatureRequest.bot_id == bot_id)
            
        return (
            query
            .order_by(desc(FeatureRequest.votes_count), desc(FeatureRequest.created_at))
            .limit(limit)
            .all()
        )
    
    def get_with_details(self, db: Session, id: int) -> Optional[FeatureRequest]:
        """
        Получить запрос с детальной информацией о пользователе и боте
        
        Args:
            db: Сессия БД
            id: ID запроса
            
        Returns:
            FeatureRequest с загруженными связанными объектами или None
        """
        return (
            db.query(FeatureRequest)
            .filter(FeatureRequest.id == id)
            .options(
                joinedload(FeatureRequest.user),
                joinedload(FeatureRequest.bot)
            )
            .first()
        )
    
    def get_multi_with_details(
        self, db: Session, *, skip: int = 0, limit: int = 100
    ) -> List[FeatureRequest]:
        """
        Получить список запросов с детальной информацией
        
        Args:
            db: Сессия БД
            skip: Сколько записей пропустить
            limit: Максимальное количество записей
            
        Returns:
            Список запросов с загруженными связанными объектами
        """
        return (
            db.query(FeatureRequest)
            .options(
                joinedload(FeatureRequest.user),
                joinedload(FeatureRequest.bot)
            )
            .order_by(desc(FeatureRequest.votes_count), desc(FeatureRequest.created_at))
            .offset(skip)
            .limit(limit)
            .all()
        )
    
    def update_status(
        self, db: Session, *, db_obj: FeatureRequest, status: FeatureRequestStatus
    ) -> FeatureRequest:
        """
        Обновить статус запроса на функцию
        
        Args:
            db: Сессия БД
            db_obj: Существующий объект запроса
            status: Новый статус запроса
            
        Returns:
            Обновленный объект запроса
        """
        db_status = DBFeatureRequestStatus[status.upper()]
        db_obj.status = db_status
        db_obj.updated_at = datetime.utcnow()
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj
    
    def update_priority(
        self, db: Session, *, db_obj: FeatureRequest, priority: FeaturePriority
    ) -> FeatureRequest:
        """
        Обновить приоритет запроса на функцию
        
        Args:
            db: Сессия БД
            db_obj: Существующий объект запроса
            priority: Новый приоритет запроса
            
        Returns:
            Обновленный объект запроса
        """
        db_priority = DBFeaturePriority[priority.upper()]
        db_obj.priority = db_priority
        db_obj.updated_at = datetime.utcnow()
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj
    
    def increment_votes(
        self, db: Session, *, db_obj: FeatureRequest
    ) -> FeatureRequest:
        """
        Увеличить счетчик голосов запроса
        
        Args:
            db: Сессия БД
            db_obj: Существующий объект запроса
            
        Returns:
            Обновленный объект запроса
        """
        db_obj.votes_count += 1
        db_obj.updated_at = datetime.utcnow()
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj
    
    def decrement_votes(
        self, db: Session, *, db_obj: FeatureRequest
    ) -> FeatureRequest:
        """
        Уменьшить счетчик голосов запроса
        
        Args:
            db: Сессия БД
            db_obj: Существующий объект запроса
            
        Returns:
            Обновленный объект запроса
        """
        if db_obj.votes_count > 0:
            db_obj.votes_count -= 1
            db_obj.updated_at = datetime.utcnow()
            db.add(db_obj)
            db.commit()
            db.refresh(db_obj)
        return db_obj


# Создание экземпляра CRUD для использования в API
feature_request = CRUDFeatureRequest(FeatureRequest) 