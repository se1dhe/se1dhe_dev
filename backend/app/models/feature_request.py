from sqlalchemy import Boolean, Column, Integer, String, DateTime, ForeignKey, Text, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.session import Base
import enum

class FeatureRequestStatus(str, enum.Enum):
    """Статусы запросов на новые функции"""
    PROPOSED = "proposed"     # Предложено
    REVIEWING = "reviewing"   # На рассмотрении
    APPROVED = "approved"     # Одобрено
    IN_PROGRESS = "in_progress"  # В разработке
    COMPLETED = "completed"   # Реализовано
    REJECTED = "rejected"     # Отклонено

class FeaturePriority(str, enum.Enum):
    """Приоритеты запросов на функции"""
    LOW = "low"           # Низкий
    MEDIUM = "medium"     # Средний
    HIGH = "high"         # Высокий
    CRITICAL = "critical" # Критический

class FeatureRequest(Base):
    """Модель запроса на новую функцию (ТЗ)"""
    __tablename__ = "feature_requests"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    bot_id = Column(Integer, ForeignKey("bots.id"), nullable=False)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    technical_details = Column(Text, nullable=True)
    status = Column(Enum(FeatureRequestStatus), default=FeatureRequestStatus.PROPOSED)
    priority = Column(Enum(FeaturePriority), default=FeaturePriority.MEDIUM)
    votes_count = Column(Integer, default=0)
    is_public = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    user = relationship("User", back_populates="feature_requests")
    bot = relationship("Bot", back_populates="feature_requests")
    votes = relationship("FeatureVote", back_populates="feature_request", cascade="all, delete-orphan")
    comments = relationship("FeatureComment", back_populates="feature_request", cascade="all, delete-orphan")

class FeatureVote(Base):
    """Модель для голосов за запросы функций"""
    __tablename__ = "feature_votes"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    feature_id = Column(Integer, ForeignKey("feature_requests.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    user = relationship("User", back_populates="feature_votes")
    feature_request = relationship("FeatureRequest", back_populates="votes")
    
    # Уникальный индекс для предотвращения дублирования голосов
    __table_args__ = (
        {'sqlite_autoincrement': True},
    )

class FeatureComment(Base):
    """Модель для комментариев к запросам функций"""
    __tablename__ = "feature_comments"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    feature_id = Column(Integer, ForeignKey("feature_requests.id"), nullable=False)
    text = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    user = relationship("User", back_populates="feature_comments")
    feature_request = relationship("FeatureRequest", back_populates="comments") 