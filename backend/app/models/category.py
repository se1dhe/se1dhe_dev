from sqlalchemy import Column, Integer, String, DateTime, Boolean, Float
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from backend.app.db.session import Base


class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    description = Column(String(1000))
    slug = Column(String(255), unique=True, index=True)
    image_url = Column(String(255))
    is_active = Column(Boolean, default=True)
    discount_percent = Column(Float, default=0)  # Скидка на категорию
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Связи
    bots = relationship("Bot", back_populates="category")