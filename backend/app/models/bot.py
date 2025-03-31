from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, Float, ForeignKey, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from backend.app.db.session import Base

class Bot(Base):
    __tablename__ = "bots"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    slug = Column(String(255), unique=True, index=True)
    short_description = Column(String(500))
    full_description = Column(Text)
    readme_md = Column(Text)
    price = Column(Float, nullable=False)
    discount_percent = Column(Float, default=0)
    category_id = Column(Integer, ForeignKey("categories.id"))
    preview_image_url = Column(String(255))
    images = Column(JSON)  # Массив URL изображений
    videos = Column(JSON)  # Массив URL видео
    demo_url = Column(String(255))
    features = Column(JSON)  # Массив функций
    is_active = Column(Boolean, default=True)
    is_featured = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Связи
    category = relationship("Category", back_populates="bots")
    subscriptions = relationship("Subscription", back_populates="bot")
    changelogs = relationship("Changelog", back_populates="bot")
    bug_reports = relationship("BugReport", back_populates="bot")