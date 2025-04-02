from sqlalchemy import Boolean, Column, Integer, String, DateTime, ForeignKey, Table, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.session import Base
import enum

# Association table for user-bot subscriptions
user_bot_subscriptions = Table(
    'user_bot_subscriptions',
    Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id'), primary_key=True),
    Column('bot_id', Integer, ForeignKey('bots.id'), primary_key=True),
    Column('created_at', DateTime(timezone=True), server_default=func.now()),
    Column('expires_at', DateTime(timezone=True), nullable=True)
)

class UserRole(str, enum.Enum):
    """Роли пользователей"""
    USER = "user"           # Обычный пользователь
    DEVELOPER = "developer" # Разработчик ботов
    ADMIN = "admin"         # Администратор
    SUPERUSER = "superuser" # Суперпользователь

class User(Base):
    """Модель пользователя"""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(100))
    role = Column(Enum(UserRole), nullable=False, default=UserRole.USER)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
    telegram_id = Column(String(255), unique=True, index=True)
    telegram_username = Column(String(255))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    bots = relationship("Bot", back_populates="owner")
    orders = relationship("Order", back_populates="user")
    reviews = relationship("Review", back_populates="user")
    subscriptions = relationship("Subscription", back_populates="user")
    notifications = relationship("Notification", back_populates="user")
    bug_reports = relationship("BugReport", back_populates="user")
    feature_requests = relationship("FeatureRequest", back_populates="user")
    feature_votes = relationship("FeatureVote", back_populates="user")
    feature_comments = relationship("FeatureComment", back_populates="user")
    user_activities = relationship("UserActivity", back_populates="user")
    
    def __repr__(self):
        return f"<User {self.id}: {self.username}>" 