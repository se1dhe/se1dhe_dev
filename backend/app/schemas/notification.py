from typing import Optional
from pydantic import BaseModel
from datetime import datetime
from enum import Enum


class NotificationType(str, Enum):
    """Enum для типов уведомлений."""
    SYSTEM = "system"
    ORDER = "order"
    BOT_UPDATE = "bot_update"
    FEATURE = "feature"
    PAYMENT = "payment"
    SUPPORT = "support"
    REVIEW = "review"


class NotificationBase(BaseModel):
    """Base Notification schema with common attributes."""
    user_id: int
    title: str
    message: str
    notification_type: NotificationType
    link: Optional[str] = None
    related_id: Optional[int] = None


class NotificationCreate(NotificationBase):
    """Schema for notification creation."""
    pass


class NotificationUpdate(BaseModel):
    """Schema for updating notification data."""
    read: Optional[bool] = None


class NotificationInDBBase(NotificationBase):
    """Schema for notification data retrieved from DB with read-only fields."""
    id: int
    read: bool
    created_at: datetime
    
    class Config:
        from_attributes = True


class Notification(NotificationInDBBase):
    """API schema for notification output."""
    pass


class NotificationCount(BaseModel):
    """Schema for counting unread notifications."""
    total: int
    unread: int 