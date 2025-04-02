from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Float, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.session import Base

class Metric(Base):
    """Модель для хранения метрик и статистики"""
    __tablename__ = "metrics"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, index=True)
    value = Column(Float, nullable=False)
    dimensions = Column(JSON, nullable=True)  # Дополнительные измерения для группировки
    timestamp = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    
    def __repr__(self):
        return f"<Metric {self.name}={self.value} at {self.timestamp}>"


class BotAnalytics(Base):
    """Модель для хранения аналитики ботов"""
    __tablename__ = "bot_analytics"

    id = Column(Integer, primary_key=True, index=True)
    bot_id = Column(Integer, ForeignKey("bots.id"), nullable=False, index=True)
    views = Column(Integer, default=0)  # Количество просмотров
    detail_views = Column(Integer, default=0)  # Количество просмотров деталей
    orders = Column(Integer, default=0)  # Количество заказов
    revenue = Column(Float, default=0.0)  # Доход
    date = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    
    # Relationships
    bot = relationship("Bot", back_populates="analytics")
    
    def __repr__(self):
        return f"<BotAnalytics bot_id={self.bot_id} views={self.views} orders={self.orders} at {self.date}>"


class UserActivity(Base):
    """Модель для хранения активности пользователей"""
    __tablename__ = "user_activities"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    action = Column(String(255), nullable=False, index=True)
    bot_id = Column(Integer, ForeignKey("bots.id"), nullable=True)
    details = Column(JSON, nullable=True)  # Дополнительные детали активности
    ip_address = Column(String(50), nullable=True)
    user_agent = Column(String(255), nullable=True)
    timestamp = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    
    # Relationships
    user = relationship("User", back_populates="user_activities")
    bot = relationship("Bot", back_populates="user_activities")
    
    def __repr__(self):
        return f"<UserActivity user_id={self.user_id} action={self.action} at {self.timestamp}>" 