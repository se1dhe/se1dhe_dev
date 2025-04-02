from sqlalchemy import Column, Integer, DateTime, ForeignKey, String, Enum, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.session import Base
import enum

class SubscriptionStatus(str, enum.Enum):
    """Статусы подписки"""
    ACTIVE = "active"           # Активная подписка
    EXPIRED = "expired"         # Подписка истекла
    CANCELLED = "cancelled"     # Подписка отменена
    PENDING = "pending"         # Ожидает оплаты
    FAILED = "failed"          # Ошибка оплаты

class SubscriptionPlan(str, enum.Enum):
    """Планы подписки"""
    FREE = "free"              # Бесплатный план
    BASIC = "basic"            # Базовый план
    PRO = "pro"                # Профессиональный план
    ENTERPRISE = "enterprise"  # Корпоративный план

class Subscription(Base):
    """Модель подписки на бота"""
    __tablename__ = "subscriptions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    bot_id = Column(Integer, ForeignKey("bots.id"), nullable=False)
    plan = Column(Enum(SubscriptionPlan), nullable=False, default=SubscriptionPlan.FREE)
    status = Column(Enum(SubscriptionStatus), nullable=False, default=SubscriptionStatus.PENDING)
    start_date = Column(DateTime(timezone=True), nullable=False)
    end_date = Column(DateTime(timezone=True), nullable=True)
    auto_renew = Column(Boolean, default=False)
    payment_method = Column(String(50), nullable=True)
    payment_id = Column(String(255), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    user = relationship("User", back_populates="subscriptions")
    bot = relationship("Bot", back_populates="subscriptions")
    
    def __repr__(self):
        return f"<Subscription {self.id}: {self.user.username} -> {self.bot.name} ({self.plan})>" 