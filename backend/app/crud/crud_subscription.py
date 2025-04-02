from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import desc, and_

from app.models.subscription import Subscription, SubscriptionStatus, SubscriptionPlan
from app.schemas.subscription import SubscriptionCreate, SubscriptionUpdate
from app.services.telegram import telegram_service
from .base import CRUDBase


class CRUDSubscription(CRUDBase[Subscription, SubscriptionCreate, SubscriptionUpdate]):
    """CRUD операции для подписок на ботов"""
    
    async def create_with_payment(
        self, db: Session, *, obj_in: SubscriptionCreate, payment_data: Dict[str, Any]
    ) -> Subscription:
        """
        Создать новую подписку с информацией об оплате
        
        Args:
            db: Сессия БД
            obj_in: Данные для создания подписки
            payment_data: Данные об оплате
            
        Returns:
            Созданный объект подписки
        """
        data = obj_in.dict()
        db_obj = Subscription(
            **data,
            payment_method=payment_data.get("method"),
            payment_id=payment_data.get("id"),
            status=SubscriptionStatus.ACTIVE
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        
        # Отправляем уведомление пользователю
        await telegram_service.send_notification(
            user=db_obj.user,
            notification=await crud.notification.create_notification(
                db=db,
                user_id=db_obj.user_id,
                title="Подписка активирована",
                message=f"Ваша подписка на бота {db_obj.bot.name} успешно активирована!\n\n"
                       f"План: {db_obj.plan.value}\n"
                       f"Дата окончания: {db_obj.end_date.strftime('%d.%m.%Y')}",
                notification_type="SUBSCRIPTION",
                related_id=db_obj.id,
                link=f"/bots/{db_obj.bot_id}"
            )
        )
        
        return db_obj
    
    def get_active_subscription(
        self, db: Session, *, user_id: int, bot_id: int
    ) -> Optional[Subscription]:
        """
        Получить активную подписку пользователя на бота
        
        Args:
            db: Сессия БД
            user_id: ID пользователя
            bot_id: ID бота
            
        Returns:
            Объект подписки или None
        """
        return (
            db.query(Subscription)
            .filter(
                and_(
                    Subscription.user_id == user_id,
                    Subscription.bot_id == bot_id,
                    Subscription.status == SubscriptionStatus.ACTIVE,
                    Subscription.end_date > datetime.utcnow()
                )
            )
            .first()
        )
    
    def get_user_subscriptions(
        self, db: Session, *, user_id: int, skip: int = 0, limit: int = 100
    ) -> List[Subscription]:
        """
        Получить все подписки пользователя
        
        Args:
            db: Сессия БД
            user_id: ID пользователя
            skip: Сколько записей пропустить
            limit: Максимальное количество записей
            
        Returns:
            Список подписок пользователя
        """
        return (
            db.query(Subscription)
            .filter(Subscription.user_id == user_id)
            .order_by(desc(Subscription.created_at))
            .offset(skip)
            .limit(limit)
            .all()
        )
    
    def get_bot_subscriptions(
        self, db: Session, *, bot_id: int, skip: int = 0, limit: int = 100
    ) -> List[Subscription]:
        """
        Получить все активные подписки на бота
        
        Args:
            db: Сессия БД
            bot_id: ID бота
            skip: Сколько записей пропустить
            limit: Максимальное количество записей
            
        Returns:
            Список подписок на бота
        """
        return (
            db.query(Subscription)
            .filter(
                and_(
                    Subscription.bot_id == bot_id,
                    Subscription.status == SubscriptionStatus.ACTIVE,
                    Subscription.end_date > datetime.utcnow()
                )
            )
            .order_by(desc(Subscription.created_at))
            .offset(skip)
            .limit(limit)
            .all()
        )
    
    async def cancel_subscription(
        self, db: Session, *, subscription_id: int, user_id: int
    ) -> Optional[Subscription]:
        """
        Отменить подписку
        
        Args:
            db: Сессия БД
            subscription_id: ID подписки
            user_id: ID пользователя
            
        Returns:
            Обновленный объект подписки или None
        """
        subscription = self.get(db, id=subscription_id)
        if not subscription or subscription.user_id != user_id:
            return None
            
        subscription.status = SubscriptionStatus.CANCELLED
        subscription.auto_renew = False
        db.add(subscription)
        db.commit()
        db.refresh(subscription)
        
        # Отправляем уведомление пользователю
        await telegram_service.send_notification(
            user=subscription.user,
            notification=await crud.notification.create_notification(
                db=db,
                user_id=subscription.user_id,
                title="Подписка отменена",
                message=f"Ваша подписка на бота {subscription.bot.name} отменена.\n"
                       f"Доступ будет сохранен до {subscription.end_date.strftime('%d.%m.%Y')}",
                notification_type="SUBSCRIPTION",
                related_id=subscription.id,
                link=f"/bots/{subscription.bot_id}"
            )
        )
        
        return subscription
    
    async def renew_subscription(
        self, db: Session, *, subscription_id: int, payment_data: Dict[str, Any]
    ) -> Optional[Subscription]:
        """
        Продлить подписку
        
        Args:
            db: Сессия БД
            subscription_id: ID подписки
            payment_data: Данные об оплате
            
        Returns:
            Обновленный объект подписки или None
        """
        subscription = self.get(db, id=subscription_id)
        if not subscription:
            return None
            
        # Продлеваем подписку на месяц
        subscription.end_date = subscription.end_date + timedelta(days=30)
        subscription.status = SubscriptionStatus.ACTIVE
        subscription.payment_method = payment_data.get("method")
        subscription.payment_id = payment_data.get("id")
        
        db.add(subscription)
        db.commit()
        db.refresh(subscription)
        
        # Отправляем уведомление пользователю
        await telegram_service.send_notification(
            user=subscription.user,
            notification=await crud.notification.create_notification(
                db=db,
                user_id=subscription.user_id,
                title="Подписка продлена",
                message=f"Ваша подписка на бота {subscription.bot.name} успешно продлена!\n"
                       f"Новая дата окончания: {subscription.end_date.strftime('%d.%m.%Y')}",
                notification_type="SUBSCRIPTION",
                related_id=subscription.id,
                link=f"/bots/{subscription.bot_id}"
            )
        )
        
        return subscription


# Создание экземпляра CRUD для использования в API
subscription = CRUDSubscription(Subscription) 