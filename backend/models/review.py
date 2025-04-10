from sqlalchemy import Column, Integer, ForeignKey, Text, Float, DateTime, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from .base import Base

class Review(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    bot_id = Column(Integer, ForeignKey("bots.id"), nullable=False)
    rating = Column(Float, nullable=False)
    comment = Column(Text)
    is_verified = Column(Boolean, default=False)  # Покупка подтверждена
    is_approved = Column(Boolean, default=True)   # Модерация пройдена
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Связи
    user = relationship("User", back_populates="reviews")
    bot = relationship("Bot", back_populates="reviews")

    def __repr__(self):
        return f"<Review(user_id={self.user_id}, bot_id={self.bot_id}, rating={self.rating})>" 