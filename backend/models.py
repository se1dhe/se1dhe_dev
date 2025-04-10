from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey, Text, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from .database import Base

class UserRole(str, enum.Enum):
    ADMIN = "admin"
    CLIENT = "client"
    USER = "user"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    telegram_id = Column(Integer, unique=True, index=True)
    username = Column(String(255), nullable=True)
    first_name = Column(String(255), nullable=True)
    last_name = Column(String(255), nullable=True)
    role = Column(Enum(UserRole), default=UserRole.USER)
    balance = Column(Float, default=0.0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Связи
    purchases = relationship("Purchase", back_populates="user")
    bug_reports = relationship("BugReport", back_populates="user")

class Bot(Base):
    __tablename__ = "bots"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), index=True)
    description = Column(Text)
    price = Column(Float)
    category_id = Column(Integer, ForeignKey("categories.id"))
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Связи
    category = relationship("Category", back_populates="bots")
    purchases = relationship("Purchase", back_populates="bot")
    changelog = relationship("Changelog", back_populates="bot")

class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), index=True)
    description = Column(Text)
    discount = Column(Float, default=0.0)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Связи
    bots = relationship("Bot", back_populates="category")

class Purchase(Base):
    __tablename__ = "purchases"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    bot_id = Column(Integer, ForeignKey("bots.id"))
    price = Column(Float)
    status = Column(String(50))
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Связи
    user = relationship("User", back_populates="purchases")
    bot = relationship("Bot", back_populates="purchases")

class BugReport(Base):
    __tablename__ = "bug_reports"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    bot_id = Column(Integer, ForeignKey("bots.id"))
    title = Column(String(255))
    description = Column(Text)
    status = Column(String(50), default="new")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Связи
    user = relationship("User", back_populates="bug_reports")
    bot = relationship("Bot")

class Changelog(Base):
    __tablename__ = "changelog"

    id = Column(Integer, primary_key=True, index=True)
    bot_id = Column(Integer, ForeignKey("bots.id"))
    version = Column(String(50))
    changes = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Связи
    bot = relationship("Bot", back_populates="changelog") 