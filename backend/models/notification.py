from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from ..database import Base
import enum

class NotificationType(enum.Enum):
    NEW_BOT = "new_bot"
    DISCOUNT = "discount"
    PAYMENT = "payment"
    REVIEW = "review"
    SYSTEM = "system"

class NotificationChannel(enum.Enum):
    EMAIL = "email"
    TELEGRAM = "telegram"
    BOTH = "both"

class Notification(Base):
    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    type = Column(Enum(NotificationType), nullable=False)
    channel = Column(Enum(NotificationChannel), nullable=False)
    title = Column(String(255), nullable=False)
    message = Column(Text, nullable=False)
    is_read = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    read_at = Column(DateTime(timezone=True), nullable=True)
    metadata = Column(Text, nullable=True)  # JSON строка с дополнительными данными

    # Связи
    user = relationship("User", back_populates="notifications")

    def __repr__(self):
        return f"<Notification {self.id} - {self.type.value}>" 