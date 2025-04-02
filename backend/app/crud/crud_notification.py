from typing import List, Optional, Dict, Any, Union, Tuple
from datetime import datetime

from sqlalchemy.orm import Session
from sqlalchemy import desc, func

from app.models.notification import Notification, NotificationType as DBNotificationType
from app.models.user import User
from app.schemas.notification import NotificationCreate, NotificationUpdate, NotificationCount, NotificationType
from app.services.telegram import telegram_service
from .base import CRUDBase


class CRUDNotification(CRUDBase[Notification, NotificationCreate, NotificationUpdate]):
    """CRUD операции для уведомлений"""
    
    async def create_notification(
        self, db: Session, *, user_id: int, title: str, message: str, 
        notification_type: NotificationType, link: Optional[str] = None, 
        related_id: Optional[int] = None, send_telegram: bool = True
    ) -> Notification:
        """
        Создать новое уведомление
        
        Args:
            db: Сессия БД
            user_id: ID пользователя
            title: Заголовок уведомления
            message: Текст уведомления
            notification_type: Тип уведомления
            link: Ссылка (опционально)
            related_id: ID связанного объекта (опционально)
            send_telegram: Отправлять ли уведомление в Telegram
            
        Returns:
            Созданное уведомление
        """
        db_type = DBNotificationType[notification_type.upper()]
        
        db_obj = Notification(
            user_id=user_id,
            title=title,
            message=message,
            notification_type=db_type,
            link=link,
            related_id=related_id,
            read=False,
            created_at=datetime.utcnow()
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        
        # Отправляем уведомление в Telegram, если нужно
        if send_telegram:
            user = db.query(User).filter(User.id == user_id).first()
            if user:
                await telegram_service.send_notification(user, db_obj)
        
        return db_obj
    
    def get_user_notifications(
        self, db: Session, *, user_id: int, skip: int = 0, 
        limit: int = 100, unread_only: bool = False
    ) -> List[Notification]:
        """
        Получить уведомления пользователя
        
        Args:
            db: Сессия БД
            user_id: ID пользователя
            skip: Сколько записей пропустить
            limit: Максимальное количество записей
            unread_only: Только непрочитанные
            
        Returns:
            Список уведомлений
        """
        query = db.query(Notification).filter(Notification.user_id == user_id)
        
        if unread_only:
            query = query.filter(Notification.read == False)
            
        return (
            query
            .order_by(desc(Notification.created_at))
            .offset(skip)
            .limit(limit)
            .all()
        )
    
    def mark_as_read(
        self, db: Session, *, notification_id: int, user_id: int
    ) -> Optional[Notification]:
        """
        Отметить уведомление как прочитанное
        
        Args:
            db: Сессия БД
            notification_id: ID уведомления
            user_id: ID пользователя (для проверки)
            
        Returns:
            Обновленное уведомление или None
        """
        notification = (
            db.query(Notification)
            .filter(
                Notification.id == notification_id,
                Notification.user_id == user_id
            )
            .first()
        )
        
        if notification and not notification.read:
            notification.read = True
            db.add(notification)
            db.commit()
            db.refresh(notification)
            
        return notification
    
    def mark_all_as_read(
        self, db: Session, *, user_id: int
    ) -> int:
        """
        Отметить все уведомления пользователя как прочитанные
        
        Args:
            db: Сессия БД
            user_id: ID пользователя
            
        Returns:
            Количество обновленных записей
        """
        result = (
            db.query(Notification)
            .filter(
                Notification.user_id == user_id,
                Notification.read == False
            )
            .update({"read": True})
        )
        
        db.commit()
        return result
    
    def get_notification_count(
        self, db: Session, *, user_id: int
    ) -> NotificationCount:
        """
        Получить количество уведомлений пользователя
        
        Args:
            db: Сессия БД
            user_id: ID пользователя
            
        Returns:
            Объект с общим количеством и количеством непрочитанных
        """
        total = db.query(Notification).filter(Notification.user_id == user_id).count()
        unread = db.query(Notification).filter(
            Notification.user_id == user_id,
            Notification.read == False
        ).count()
        
        return NotificationCount(total=total, unread=unread)
    
    async def create_system_notification(
        self, db: Session, *, user_id: int, title: str, message: str, 
        link: Optional[str] = None, send_telegram: bool = True
    ) -> Notification:
        """
        Создать системное уведомление
        
        Args:
            db: Сессия БД
            user_id: ID пользователя
            title: Заголовок
            message: Сообщение
            link: Ссылка (опционально)
            send_telegram: Отправлять ли уведомление в Telegram
            
        Returns:
            Созданное уведомление
        """
        return await self.create_notification(
            db=db,
            user_id=user_id,
            title=title,
            message=message,
            notification_type=NotificationType.SYSTEM,
            link=link,
            send_telegram=send_telegram
        )
    
    async def create_order_notification(
        self, db: Session, *, user_id: int, title: str, message: str, 
        order_id: int, link: Optional[str] = None, send_telegram: bool = True
    ) -> Notification:
        """
        Создать уведомление о заказе
        
        Args:
            db: Сессия БД
            user_id: ID пользователя
            title: Заголовок
            message: Сообщение
            order_id: ID заказа
            link: Ссылка (опционально)
            send_telegram: Отправлять ли уведомление в Telegram
            
        Returns:
            Созданное уведомление
        """
        return await self.create_notification(
            db=db,
            user_id=user_id,
            title=title,
            message=message,
            notification_type=NotificationType.ORDER,
            related_id=order_id,
            link=link,
            send_telegram=send_telegram
        )
    
    async def create_bot_update_notification(
        self, db: Session, *, user_id: int, title: str, message: str, 
        bot_id: int, link: Optional[str] = None, send_telegram: bool = True
    ) -> Notification:
        """
        Создать уведомление об обновлении бота
        
        Args:
            db: Сессия БД
            user_id: ID пользователя
            title: Заголовок
            message: Сообщение
            bot_id: ID бота
            link: Ссылка (опционально)
            send_telegram: Отправлять ли уведомление в Telegram
            
        Returns:
            Созданное уведомление
        """
        return await self.create_notification(
            db=db,
            user_id=user_id,
            title=title,
            message=message,
            notification_type=NotificationType.BOT_UPDATE,
            related_id=bot_id,
            link=link,
            send_telegram=send_telegram
        )
    
    async def create_feature_notification(
        self, db: Session, *, user_id: int, title: str, message: str, 
        feature_id: int, link: Optional[str] = None, send_telegram: bool = True
    ) -> Notification:
        """
        Создать уведомление о запросе функции
        
        Args:
            db: Сессия БД
            user_id: ID пользователя
            title: Заголовок
            message: Сообщение
            feature_id: ID запроса функции
            link: Ссылка (опционально)
            send_telegram: Отправлять ли уведомление в Telegram
            
        Returns:
            Созданное уведомление
        """
        return await self.create_notification(
            db=db,
            user_id=user_id,
            title=title,
            message=message,
            notification_type=NotificationType.FEATURE,
            related_id=feature_id,
            link=link,
            send_telegram=send_telegram
        )


# Создание экземпляра CRUD для использования в API
notification = CRUDNotification(Notification) 