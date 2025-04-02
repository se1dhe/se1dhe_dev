from typing import List, Optional, Dict, Any, Union
from datetime import datetime, date, timedelta

from sqlalchemy.orm import Session
from sqlalchemy import func, and_, extract, desc
from sqlalchemy.sql.expression import cast
from sqlalchemy.types import Date

from app.models.metric import BotAnalytics, UserActivity
from app.schemas.metric import BotAnalyticsCreate, BotAnalyticsUpdate, UserActivityCreate
from .base import CRUDBase


class CRUDBotAnalytics(CRUDBase[BotAnalytics, BotAnalyticsCreate, BotAnalyticsUpdate]):
    """CRUD операции для аналитики ботов"""
    
    def create_analytics(
        self, db: Session, *, obj_in: BotAnalyticsCreate
    ) -> BotAnalytics:
        """
        Создать новую запись аналитики бота
        
        Args:
            db: Сессия БД
            obj_in: Данные для создания аналитики
            
        Returns:
            Созданная запись аналитики
        """
        db_obj = BotAnalytics(
            bot_id=obj_in.bot_id,
            views=obj_in.views,
            detail_views=obj_in.detail_views,
            orders=obj_in.orders,
            revenue=obj_in.revenue,
            date=obj_in.date or date.today()
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj
    
    def get_by_bot_id(
        self, db: Session, *, bot_id: int, skip: int = 0, limit: int = 100
    ) -> List[BotAnalytics]:
        """
        Получить аналитику по ID бота
        
        Args:
            db: Сессия БД
            bot_id: ID бота
            skip: Сколько записей пропустить
            limit: Максимальное количество записей
            
        Returns:
            Список записей аналитики для бота
        """
        return (
            db.query(BotAnalytics)
            .filter(BotAnalytics.bot_id == bot_id)
            .order_by(desc(BotAnalytics.date))
            .offset(skip)
            .limit(limit)
            .all()
        )
    
    def get_by_date_range(
        self, db: Session, *, bot_id: Optional[int] = None, 
        start_date: date = None, end_date: date = None,
        skip: int = 0, limit: int = 100
    ) -> List[BotAnalytics]:
        """
        Получить аналитику за определенный период времени
        
        Args:
            db: Сессия БД
            bot_id: ID бота (опционально)
            start_date: Начальная дата
            end_date: Конечная дата
            skip: Сколько записей пропустить
            limit: Максимальное количество записей
            
        Returns:
            Список записей аналитики за период
        """
        query = db.query(BotAnalytics)
        
        if bot_id is not None:
            query = query.filter(BotAnalytics.bot_id == bot_id)
            
        if start_date:
            query = query.filter(BotAnalytics.date >= start_date)
            
        if end_date:
            query = query.filter(BotAnalytics.date <= end_date)
            
        return (
            query
            .order_by(desc(BotAnalytics.date))
            .offset(skip)
            .limit(limit)
            .all()
        )
    
    def update_or_create_daily(
        self, db: Session, *, 
        bot_id: int, 
        views: int = 0, 
        detail_views: int = 0, 
        orders: int = 0, 
        revenue: float = 0.0,
        target_date: date = None
    ) -> BotAnalytics:
        """
        Обновить или создать запись аналитики за указанный день
        
        Args:
            db: Сессия БД
            bot_id: ID бота
            views: Количество просмотров для добавления
            detail_views: Количество просмотров деталей для добавления
            orders: Количество заказов для добавления
            revenue: Доход для добавления
            target_date: Целевая дата (по умолчанию - текущий день)
            
        Returns:
            Обновленная или созданная запись аналитики
        """
        if target_date is None:
            target_date = date.today()
            
        # Ищем запись за указанную дату
        db_obj = (
            db.query(BotAnalytics)
            .filter(
                BotAnalytics.bot_id == bot_id,
                BotAnalytics.date == target_date
            )
            .first()
        )
        
        if db_obj:
            # Обновляем существующую запись
            db_obj.views += views
            db_obj.detail_views += detail_views
            db_obj.orders += orders
            db_obj.revenue += revenue
        else:
            # Создаем новую запись
            db_obj = BotAnalytics(
                bot_id=bot_id,
                views=views,
                detail_views=detail_views,
                orders=orders,
                revenue=revenue,
                date=target_date
            )
            db.add(db_obj)
            
        db.commit()
        db.refresh(db_obj)
        return db_obj
    
    def get_summary_by_bot(
        self, db: Session, *, 
        start_date: date = None, 
        end_date: date = None
    ) -> List[Dict[str, Any]]:
        """
        Получить агрегированную аналитику по ботам за период
        
        Args:
            db: Сессия БД
            start_date: Начальная дата
            end_date: Конечная дата
            
        Returns:
            Список с агрегированными данными по ботам
        """
        query = db.query(
            BotAnalytics.bot_id,
            func.sum(BotAnalytics.views).label('total_views'),
            func.sum(BotAnalytics.detail_views).label('total_detail_views'),
            func.sum(BotAnalytics.orders).label('total_orders'),
            func.sum(BotAnalytics.revenue).label('total_revenue')
        )
        
        if start_date:
            query = query.filter(BotAnalytics.date >= start_date)
            
        if end_date:
            query = query.filter(BotAnalytics.date <= end_date)
            
        result = query.group_by(BotAnalytics.bot_id).all()
        
        return [dict(zip(r.keys(), r)) for r in result]


class CRUDUserActivity(CRUDBase[UserActivity, UserActivityCreate, None]):
    """CRUD операции для активности пользователей"""
    
    def create_activity(
        self, db: Session, *, obj_in: UserActivityCreate
    ) -> UserActivity:
        """
        Создать новую запись активности пользователя
        
        Args:
            db: Сессия БД
            obj_in: Данные для создания активности
            
        Returns:
            Созданная запись активности
        """
        db_obj = UserActivity(
            user_id=obj_in.user_id,
            action=obj_in.action,
            bot_id=obj_in.bot_id,
            details=obj_in.details,
            ip_address=obj_in.ip_address,
            user_agent=obj_in.user_agent,
            timestamp=datetime.utcnow()
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj
    
    def get_by_user_id(
        self, db: Session, *, user_id: int, skip: int = 0, limit: int = 100
    ) -> List[UserActivity]:
        """
        Получить активности пользователя по ID
        
        Args:
            db: Сессия БД
            user_id: ID пользователя
            skip: Сколько записей пропустить
            limit: Максимальное количество записей
            
        Returns:
            Список активностей пользователя
        """
        return (
            db.query(UserActivity)
            .filter(UserActivity.user_id == user_id)
            .order_by(desc(UserActivity.timestamp))
            .offset(skip)
            .limit(limit)
            .all()
        )
    
    def get_by_bot_id(
        self, db: Session, *, bot_id: int, skip: int = 0, limit: int = 100
    ) -> List[UserActivity]:
        """
        Получить активности пользователей для бота по ID
        
        Args:
            db: Сессия БД
            bot_id: ID бота
            skip: Сколько записей пропустить
            limit: Максимальное количество записей
            
        Returns:
            Список активностей для бота
        """
        return (
            db.query(UserActivity)
            .filter(UserActivity.bot_id == bot_id)
            .order_by(desc(UserActivity.timestamp))
            .offset(skip)
            .limit(limit)
            .all()
        )
    
    def get_by_action(
        self, db: Session, *, action: str, skip: int = 0, limit: int = 100
    ) -> List[UserActivity]:
        """
        Получить активности по типу действия
        
        Args:
            db: Сессия БД
            action: Тип действия
            skip: Сколько записей пропустить
            limit: Максимальное количество записей
            
        Returns:
            Список активностей определенного типа
        """
        return (
            db.query(UserActivity)
            .filter(UserActivity.action == action)
            .order_by(desc(UserActivity.timestamp))
            .offset(skip)
            .limit(limit)
            .all()
        )
    
    def get_by_time_range(
        self, db: Session, *, 
        start_date: datetime = None, 
        end_date: datetime = None,
        user_id: Optional[int] = None,
        bot_id: Optional[int] = None,
        action: Optional[str] = None,
        skip: int = 0, 
        limit: int = 100
    ) -> List[UserActivity]:
        """
        Получить активности за определенный период времени с фильтрами
        
        Args:
            db: Сессия БД
            start_date: Начальная дата
            end_date: Конечная дата
            user_id: ID пользователя (опционально)
            bot_id: ID бота (опционально)
            action: Тип действия (опционально)
            skip: Сколько записей пропустить
            limit: Максимальное количество записей
            
        Returns:
            Список активностей за период, отфильтрованный по параметрам
        """
        query = db.query(UserActivity)
        
        if start_date:
            query = query.filter(UserActivity.timestamp >= start_date)
            
        if end_date:
            query = query.filter(UserActivity.timestamp <= end_date)
            
        if user_id is not None:
            query = query.filter(UserActivity.user_id == user_id)
            
        if bot_id is not None:
            query = query.filter(UserActivity.bot_id == bot_id)
            
        if action:
            query = query.filter(UserActivity.action == action)
            
        return (
            query
            .order_by(desc(UserActivity.timestamp))
            .offset(skip)
            .limit(limit)
            .all()
        )
    
    def get_most_active_users(
        self, db: Session, *, 
        days: int = 30, 
        limit: int = 10
    ) -> List[Dict[str, Any]]:
        """
        Получить самых активных пользователей за указанный период
        
        Args:
            db: Сессия БД
            days: Количество дней для анализа
            limit: Количество пользователей в выборке
            
        Returns:
            Список с данными о самых активных пользователях
        """
        start_date = datetime.utcnow() - timedelta(days=days)
        
        result = (
            db.query(
                UserActivity.user_id,
                func.count(UserActivity.id).label('activity_count')
            )
            .filter(UserActivity.timestamp >= start_date)
            .group_by(UserActivity.user_id)
            .order_by(desc('activity_count'))
            .limit(limit)
            .all()
        )
        
        return [dict(zip(r.keys(), r)) for r in result]


# Создание экземпляров CRUD для использования в API
bot_analytics = CRUDBotAnalytics(BotAnalytics)
user_activity = CRUDUserActivity(UserActivity) 