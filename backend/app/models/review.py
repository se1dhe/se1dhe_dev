from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, Float, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.session import Base

class Review(Base):
    """Модель отзыва о боте"""
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    bot_id = Column(Integer, ForeignKey("bots.id"), nullable=False)
    rating = Column(Float, nullable=False)  # Оценка от 1 до 5
    title = Column(String(255), nullable=False)
    content = Column(Text, nullable=False)
    verified_purchase = Column(Boolean, default=False)  # Подтвержденная покупка
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    user = relationship("User", back_populates="reviews")
    bot = relationship("Bot", back_populates="reviews") 