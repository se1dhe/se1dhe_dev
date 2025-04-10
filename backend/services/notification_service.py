from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import func
from ..models.notification import Notification, NotificationType, NotificationChannel
from ..schemas.notification import NotificationCreate, NotificationUpdate
from .email_service import EmailService
from .telegram_service import TelegramService

class NotificationService:
    def __init__(self, db: Session):
        self.db = db
        self.email_service = EmailService()
        self.telegram_service = TelegramService()

    async def create_notification(
        self,
        notification: NotificationCreate
    ) -> Notification:
        """Создание нового уведомления"""
        db_notification = Notification(
            user_id=notification.user_id,
            type=notification.type,
            channel=notification.channel,
            title=notification.title,
            message=notification.message,
            metadata=notification.metadata
        )
        self.db.add(db_notification)
        self.db.commit()
        self.db.refresh(db_notification)

        # Отправка уведомления через выбранные каналы
        await self._send_notification(db_notification)

        return db_notification

    async def _send_notification(self, notification: Notification) -> None:
        """Отправка уведомления через выбранные каналы"""
        if notification.channel in [NotificationChannel.EMAIL, NotificationChannel.BOTH]:
            await self.email_service.send_notification(notification)

        if notification.channel in [NotificationChannel.TELEGRAM, NotificationChannel.BOTH]:
            await self.telegram_service.send_notification(notification)

    async def get_user_notifications(
        self,
        user_id: int,
        skip: int = 0,
        limit: int = 100,
        unread_only: bool = False
    ) -> List[Notification]:
        """Получение уведомлений пользователя"""
        query = self.db.query(Notification).filter(Notification.user_id == user_id)
        
        if unread_only:
            query = query.filter(Notification.is_read == 0)
            
        return query.order_by(Notification.created_at.desc()).offset(skip).limit(limit).all()

    async def mark_as_read(
        self,
        notification_id: int,
        user_id: int
    ) -> Optional[Notification]:
        """Пометка уведомления как прочитанного"""
        notification = self.db.query(Notification).filter(
            Notification.id == notification_id,
            Notification.user_id == user_id
        ).first()

        if notification:
            notification.is_read = 1
            notification.read_at = func.now()
            self.db.commit()
            self.db.refresh(notification)

        return notification

    async def mark_all_as_read(self, user_id: int) -> None:
        """Пометка всех уведомлений пользователя как прочитанных"""
        self.db.query(Notification).filter(
            Notification.user_id == user_id,
            Notification.is_read == 0
        ).update({
            Notification.is_read: 1,
            Notification.read_at: func.now()
        })
        self.db.commit()

    async def get_unread_count(self, user_id: int) -> int:
        """Получение количества непрочитанных уведомлений"""
        return self.db.query(Notification).filter(
            Notification.user_id == user_id,
            Notification.is_read == 0
        ).count() 