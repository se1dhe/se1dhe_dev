from enum import Enum
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from datetime import datetime
from ..models.notification import NotificationType, NotificationChannel

class NotificationType(str, Enum):
    NEW_BOT = "new_bot"
    DISCOUNT = "discount"
    PAYMENT = "payment"
    SUPPORT = "support"
    REVIEW = "review"

class NotificationBase(BaseModel):
    type: NotificationType
    channel: NotificationChannel
    title: str = Field(..., max_length=255)
    message: str
    metadata: Optional[str] = None

class NotificationCreate(NotificationBase):
    user_id: int

class NotificationUpdate(BaseModel):
    is_read: Optional[bool] = None
    read_at: Optional[datetime] = None

class NotificationInDB(NotificationBase):
    id: int
    user_id: int
    is_read: bool
    created_at: datetime
    read_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class NotificationResponse(NotificationInDB):
    pass 