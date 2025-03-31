from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Boolean, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from backend.app.db.session import Base


class NotificationType(str, enum.Enum):
    SYSTEM = "system"
    NEW_BOT = "new_bot"
    BOT_UPDATE = "bot_update"
    ORDER_STATUS = "order_status"
    SUBSCRIPTION = "subscription"
    BUG_REPORT = "bug_report"
    CUSTOM = "custom"


class Notification(Base):
    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    title = Column(String(255), nullable=False)
    content = Column(Text, nullable=False)
    notification_type = Column(Enum(NotificationType), default=NotificationType.SYSTEM)
    is_read = Column(Boolean, default=False)
    related_bot_id = Column(Integer, ForeignKey("bots.id"), nullable=True)
    related_order_id = Column(Integer, ForeignKey("orders.id"), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Связи
    user = relationship("User")
    related_bot = relationship("Bot")
    related_order = relationship("Order")