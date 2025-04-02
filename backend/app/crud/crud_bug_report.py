from typing import List, Optional, Dict, Any, Union
from datetime import datetime

from sqlalchemy.orm import Session, joinedload
from sqlalchemy import desc

from app.models.bug_report import BugReport, BugStatus as DBBugStatus, BugPriority as DBBugPriority
from app.schemas.bug_report import BugReportCreate, BugReportUpdate, BugReportStatus as BugStatus, BugReportPriority as BugPriority
from .base import CRUDBase


class CRUDBugReport(CRUDBase[BugReport, BugReportCreate, BugReportUpdate]):
    """CRUD операции для отчетов об ошибках"""
    
    def create(self, db: Session, *, obj_in: BugReportCreate) -> BugReport:
        """
        Создать новый отчет об ошибке
        
        Args:
            db: Сессия БД
            obj_in: Данные для создания отчета
            
        Returns:
            Созданный объект отчета
        """
        db_obj = BugReport(
            user_id=obj_in.user_id,
            bot_id=obj_in.bot_id,
            title=obj_in.title,
            description=obj_in.description,
            steps_to_reproduce=obj_in.steps_to_reproduce,
            status=DBBugStatus.OPEN,
            priority=DBBugPriority[obj_in.priority.upper()],
            created_at=datetime.utcnow()
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj
    
    def get_by_user(
        self, db: Session, *, user_id: int, skip: int = 0, limit: int = 100
    ) -> List[BugReport]:
        """
        Получить отчеты об ошибках от определенного пользователя
        
        Args:
            db: Сессия БД
            user_id: ID пользователя
            skip: Сколько записей пропустить
            limit: Максимальное количество записей
            
        Returns:
            Список отчетов об ошибках от пользователя
        """
        return (
            db.query(BugReport)
            .filter(BugReport.user_id == user_id)
            .order_by(desc(BugReport.created_at))
            .offset(skip)
            .limit(limit)
            .all()
        )
    
    def get_by_bot(
        self, db: Session, *, bot_id: int, skip: int = 0, limit: int = 100
    ) -> List[BugReport]:
        """
        Получить отчеты об ошибках для конкретного бота
        
        Args:
            db: Сессия БД
            bot_id: ID бота
            skip: Сколько записей пропустить
            limit: Максимальное количество записей
            
        Returns:
            Список отчетов об ошибках для бота
        """
        return (
            db.query(BugReport)
            .filter(BugReport.bot_id == bot_id)
            .order_by(desc(BugReport.created_at))
            .offset(skip)
            .limit(limit)
            .all()
        )
    
    def get_by_status(
        self, db: Session, *, status: BugStatus, skip: int = 0, limit: int = 100
    ) -> List[BugReport]:
        """
        Получить отчеты об ошибках с определенным статусом
        
        Args:
            db: Сессия БД
            status: Статус отчета
            skip: Сколько записей пропустить
            limit: Максимальное количество записей
            
        Returns:
            Список отчетов об ошибках с указанным статусом
        """
        db_status = DBBugStatus[status.upper()]
        return (
            db.query(BugReport)
            .filter(BugReport.status == db_status)
            .order_by(desc(BugReport.created_at))
            .offset(skip)
            .limit(limit)
            .all()
        )
    
    def get_by_priority(
        self, db: Session, *, priority: BugPriority, skip: int = 0, limit: int = 100
    ) -> List[BugReport]:
        """
        Получить отчеты об ошибках с определенным приоритетом
        
        Args:
            db: Сессия БД
            priority: Приоритет отчета
            skip: Сколько записей пропустить
            limit: Максимальное количество записей
            
        Returns:
            Список отчетов об ошибках с указанным приоритетом
        """
        db_priority = DBBugPriority[priority.upper()]
        return (
            db.query(BugReport)
            .filter(BugReport.priority == db_priority)
            .order_by(desc(BugReport.created_at))
            .offset(skip)
            .limit(limit)
            .all()
        )
    
    def get_with_details(self, db: Session, id: int) -> Optional[BugReport]:
        """
        Получить отчет об ошибке с детальной информацией о пользователе и боте
        
        Args:
            db: Сессия БД
            id: ID отчета
            
        Returns:
            BugReport с загруженными связанными объектами или None
        """
        return (
            db.query(BugReport)
            .filter(BugReport.id == id)
            .options(
                joinedload(BugReport.user),
                joinedload(BugReport.bot).joinedload(BugReport.bot.category)
            )
            .first()
        )
    
    def get_multi_with_details(
        self, db: Session, *, skip: int = 0, limit: int = 100
    ) -> List[BugReport]:
        """
        Получить список отчетов об ошибках с детальной информацией
        
        Args:
            db: Сессия БД
            skip: Сколько записей пропустить
            limit: Максимальное количество записей
            
        Returns:
            Список отчетов с загруженными связанными объектами
        """
        return (
            db.query(BugReport)
            .options(
                joinedload(BugReport.user),
                joinedload(BugReport.bot).joinedload(BugReport.bot.category)
            )
            .order_by(desc(BugReport.created_at))
            .offset(skip)
            .limit(limit)
            .all()
        )
    
    def update_status(
        self, db: Session, *, db_obj: BugReport, status: BugStatus
    ) -> BugReport:
        """
        Обновить статус отчета об ошибке
        
        Args:
            db: Сессия БД
            db_obj: Существующий объект отчета
            status: Новый статус отчета
            
        Returns:
            Обновленный объект отчета
        """
        db_status = DBBugStatus[status.upper()]
        db_obj.status = db_status
        db_obj.updated_at = datetime.utcnow()
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj
    
    def update_priority(
        self, db: Session, *, db_obj: BugReport, priority: BugPriority
    ) -> BugReport:
        """
        Обновить приоритет отчета об ошибке
        
        Args:
            db: Сессия БД
            db_obj: Существующий объект отчета
            priority: Новый приоритет отчета
            
        Returns:
            Обновленный объект отчета
        """
        db_priority = DBBugPriority[priority.upper()]
        db_obj.priority = db_priority
        db_obj.updated_at = datetime.utcnow()
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj


# Создание экземпляра CRUD для использования в API
bug_report = CRUDBugReport(BugReport) 