from sqlalchemy import Column, Integer, ForeignKey, Float, DateTime, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from .base import Base

class UserPreference(Base):
    __tablename__ = "user_preferences"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False)
    preference_score = Column(Float, default=0.0)  # Оценка предпочтения (0-1)
    interaction_count = Column(Integer, default=0)  # Количество взаимодействий
    last_interaction = Column(DateTime, default=datetime.utcnow)
    metadata = Column(JSON, default={})  # Дополнительные метаданные

    # Связи
    user = relationship("User", back_populates="preferences")
    category = relationship("Category", back_populates="preferences")

    def __repr__(self):
        return f"<UserPreference(user_id={self.user_id}, category_id={self.category_id}, score={self.preference_score})>" 