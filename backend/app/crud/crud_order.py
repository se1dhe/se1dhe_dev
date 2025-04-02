from typing import List, Optional, Dict, Any, Union
from datetime import datetime

from sqlalchemy.orm import Session, joinedload
from sqlalchemy import desc

from app.models.order import Order, OrderStatus as DBOrderStatus
from app.schemas.order import OrderCreate, OrderUpdate, OrderStatus
from .base import CRUDBase


class CRUDOrder(CRUDBase[Order, OrderCreate, OrderUpdate]):
    """CRUD операции для заказов"""
    
    def create(self, db: Session, *, obj_in: OrderCreate) -> Order:
        """
        Создать новый заказ
        
        Args:
            db: Сессия БД
            obj_in: Данные для создания заказа
            
        Returns:
            Созданный объект заказа
        """
        db_obj = Order(
            user_id=obj_in.user_id,
            bot_id=obj_in.bot_id,
            amount=obj_in.amount,
            status=DBOrderStatus.PENDING,
            payment_method=obj_in.payment_method,
            created_at=datetime.utcnow()
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj
    
    def get_by_user(
        self, db: Session, *, user_id: int, skip: int = 0, limit: int = 100
    ) -> List[Order]:
        """
        Получить заказы пользователя
        
        Args:
            db: Сессия БД
            user_id: ID пользователя
            skip: Сколько записей пропустить
            limit: Максимальное количество записей
            
        Returns:
            Список заказов пользователя
        """
        return (
            db.query(Order)
            .filter(Order.user_id == user_id)
            .order_by(desc(Order.created_at))
            .offset(skip)
            .limit(limit)
            .all()
        )
    
    def get_by_bot(
        self, db: Session, *, bot_id: int, skip: int = 0, limit: int = 100
    ) -> List[Order]:
        """
        Получить заказы для конкретного бота
        
        Args:
            db: Сессия БД
            bot_id: ID бота
            skip: Сколько записей пропустить
            limit: Максимальное количество записей
            
        Returns:
            Список заказов для бота
        """
        return (
            db.query(Order)
            .filter(Order.bot_id == bot_id)
            .order_by(desc(Order.created_at))
            .offset(skip)
            .limit(limit)
            .all()
        )
    
    def get_by_status(
        self, db: Session, *, status: OrderStatus, skip: int = 0, limit: int = 100
    ) -> List[Order]:
        """
        Получить заказы с определенным статусом
        
        Args:
            db: Сессия БД
            status: Статус заказа
            skip: Сколько записей пропустить
            limit: Максимальное количество записей
            
        Returns:
            Список заказов с указанным статусом
        """
        db_status = DBOrderStatus[status.upper()]
        return (
            db.query(Order)
            .filter(Order.status == db_status)
            .order_by(desc(Order.created_at))
            .offset(skip)
            .limit(limit)
            .all()
        )
    
    def get_with_details(self, db: Session, id: int) -> Optional[Order]:
        """
        Получить заказ с детальной информацией о пользователе и боте
        
        Args:
            db: Сессия БД
            id: ID заказа
            
        Returns:
            Order с загруженными связанными объектами или None
        """
        return (
            db.query(Order)
            .filter(Order.id == id)
            .options(
                joinedload(Order.user),
                joinedload(Order.bot).joinedload(Order.bot.category)
            )
            .first()
        )
    
    def get_multi_with_details(
        self, db: Session, *, skip: int = 0, limit: int = 100
    ) -> List[Order]:
        """
        Получить список заказов с детальной информацией
        
        Args:
            db: Сессия БД
            skip: Сколько записей пропустить
            limit: Максимальное количество записей
            
        Returns:
            Список заказов с загруженными связанными объектами
        """
        return (
            db.query(Order)
            .options(
                joinedload(Order.user),
                joinedload(Order.bot).joinedload(Order.bot.category)
            )
            .order_by(desc(Order.created_at))
            .offset(skip)
            .limit(limit)
            .all()
        )
    
    def update_status(
        self, db: Session, *, db_obj: Order, status: OrderStatus
    ) -> Order:
        """
        Обновить статус заказа
        
        Args:
            db: Сессия БД
            db_obj: Существующий объект заказа
            status: Новый статус заказа
            
        Returns:
            Обновленный объект заказа
        """
        db_status = DBOrderStatus[status.upper()]
        db_obj.status = db_status
        db_obj.updated_at = datetime.utcnow()
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj
    
    def update_payment_info(
        self, db: Session, *, db_obj: Order, payment_id: str
    ) -> Order:
        """
        Обновить информацию о платеже
        
        Args:
            db: Сессия БД
            db_obj: Существующий объект заказа
            payment_id: ID платежа
            
        Returns:
            Обновленный объект заказа
        """
        db_obj.payment_id = payment_id
        db_obj.updated_at = datetime.utcnow()
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def has_completed_orders(
        self, db: Session, *, user_id: int, bot_id: int
    ) -> bool:
        """
        Проверить, есть ли у пользователя завершенные заказы на конкретного бота
        
        Args:
            db: Сессия БД
            user_id: ID пользователя
            bot_id: ID бота
            
        Returns:
            True, если есть хотя бы один завершенный заказ
        """
        from app.schemas.order import OrderStatus
        
        # Статусы завершенных заказов
        completed_statuses = [OrderStatus.COMPLETED, OrderStatus.DELIVERED]
        
        # Проверяем наличие заказов
        orders = (
            db.query(self.model)
            .filter(
                self.model.user_id == user_id,
                self.model.bot_id == bot_id,
                self.model.status.in_([s.value for s in completed_statuses])
            )
            .first()
        )
        
        return orders is not None


# Создание экземпляра CRUD для использования в API
order = CRUDOrder(Order) 