from sqlalchemy import Boolean, Column, Integer, String, DateTime, ForeignKey, Text, Float, JSON, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.session import Base
import enum

class BotStatus(str, enum.Enum):
    """Статусы бота"""
    DRAFT = "draft"           # Черновик
    PENDING = "pending"       # На проверке
    ACTIVE = "active"         # Активный
    SUSPENDED = "suspended"   # Приостановлен
    DELETED = "deleted"       # Удален

class Bot(Base):
    __tablename__ = "bots"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    description = Column(Text, nullable=False)
    price = Column(Float, nullable=False, default=0.0)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    status = Column(Enum(BotStatus), nullable=False, default=BotStatus.DRAFT)
    telegram_token = Column(String(255), nullable=False)
    telegram_username = Column(String(255), nullable=False)
    features = Column(JSON, nullable=False)  # List of bot features
    images = Column(JSON, nullable=True)  # List of image URLs
    videos = Column(JSON, nullable=True)  # List of video URLs
    readme = Column(Text, nullable=True)  # README.md content
    is_active = Column(Boolean, default=True)
    is_featured = Column(Boolean, default=False)
    discount_percentage = Column(Integer, default=0)
    is_verified = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    category = relationship("Category", back_populates="bots")
    owner = relationship("User", back_populates="bots")
    reviews = relationship("Review", back_populates="bot")
    orders = relationship("Order", back_populates="bot")
    subscriptions = relationship("Subscription", back_populates="bot")
    bug_reports = relationship("BugReport", back_populates="bot")
    changelogs = relationship("Changelog", back_populates="bot")
    feature_requests = relationship("FeatureRequest", back_populates="bot")
    analytics = relationship("BotAnalytics", back_populates="bot")
    user_activities = relationship("UserActivity", back_populates="bot")

    def __repr__(self):
        return f"<Bot {self.id}: {self.name}>" 