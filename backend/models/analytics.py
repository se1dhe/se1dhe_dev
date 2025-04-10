from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Float, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from ..database import Base
import enum
from datetime import datetime

class AnalyticsEventType(enum.Enum):
    PAGE_VIEW = "page_view"
    BOT_VIEW = "bot_view"
    BOT_PURCHASE = "bot_purchase"
    CATEGORY_VIEW = "category_view"
    SEARCH = "search"
    USER_REGISTRATION = "user_registration"
    PAYMENT = "payment"
    REVIEW = "review"

class Analytics(Base):
    __tablename__ = "analytics"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    event_type = Column(String(50), nullable=False)
    event_data = Column(JSON, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    metadata = Column(JSON, nullable=True)

    # Связи
    user = relationship("User", back_populates="analytics_events")

    def __repr__(self):
        return f"<Analytics {self.id} - {self.event_type}>"

class BotAnalytics(Base):
    __tablename__ = "bot_analytics"

    id = Column(Integer, primary_key=True, index=True)
    bot_id = Column(Integer, ForeignKey("bots.id"), nullable=False)
    date = Column(DateTime, nullable=False)
    views = Column(Integer, default=0)
    purchases = Column(Integer, default=0)
    revenue = Column(Float, default=0.0)
    avg_rating = Column(Float, nullable=True)
    reviews_count = Column(Integer, default=0)
    metadata = Column(JSON, nullable=True)

    # Связи
    bot = relationship("Bot", back_populates="analytics")

    def __repr__(self):
        return f"<BotAnalytics {self.id} - Bot {self.bot_id}>" 