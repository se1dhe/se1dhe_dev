from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, Boolean, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.session import Base
import enum

class NotificationType(str, enum.Enum):
    """Типы уведомлений"""
    SYSTEM = "system"           # Системное уведомление
    ORDER = "order"             # Уведомление о заказе
    BOT_UPDATE = "bot_update"   # Обновление бота
    FEATURE = "feature"         # Уведомление о функции
    PAYMENT = "payment"         # Платежное уведомление
    SUPPORT = "support"         # Поддержка
    REVIEW = "review"           # Отзыв

class Notification(Base):
    """Модель уведомления"""
    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    title = Column(String(255), nullable=False)
    message = Column(Text, nullable=False)
    notification_type = Column(Enum(NotificationType), nullable=False)
    read = Column(Boolean, default=False)
    link = Column(String(255), nullable=True)  # Ссылка для перехода
    related_id = Column(Integer, nullable=True)  # ID связанного объекта
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    user = relationship("User", back_populates="notifications") 