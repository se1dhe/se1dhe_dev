from sqlalchemy import Column, Integer, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from .base import Base

class CategorySubscription(Base):
    __tablename__ = "category_subscriptions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Связи
    user = relationship("User", back_populates="category_subscriptions")
    category = relationship("Category", back_populates="subscriptions")

    def __repr__(self):
        return f"<CategorySubscription(user_id={self.user_id}, category_id={self.category_id})>" 