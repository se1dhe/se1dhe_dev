from typing import Optional, List
from pydantic import BaseModel
from datetime import datetime

from app.schemas.base import UserBase
from app.schemas.subscription import Subscription


# Общие свойства
class UserBase(BaseModel):
    """Base User schema with common attributes."""
    email: Optional[str] = None
    username: Optional[str] = None
    telegram_id: Optional[int] = None
    telegram_username: Optional[str] = None
    full_name: Optional[str] = None
    is_active: Optional[bool] = True
    is_superuser: bool = False


class UserCreate(UserBase):
    """Schema for user creation with required fields."""
    password: str


class UserUpdate(BaseModel):
    """Schema for updating user data."""
    email: Optional[str] = None
    username: Optional[str] = None
    password: Optional[str] = None
    telegram_id: Optional[int] = None
    telegram_username: Optional[str] = None
    is_active: Optional[bool] = None
    is_superuser: Optional[bool] = None
    is_verified: Optional[bool] = None


class UserInDBBase(UserBase):
    """Schema for user data retrieved from DB with read-only fields."""
    id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class User(UserInDBBase):
    """API schema for regular user output (no sensitive data)."""
    pass


class UserInDB(UserInDBBase):
    """DB schema for user with hashed password (not exposed in API)."""
    hashed_password: str


class UserWithSubscriptions(User):
    """API schema for user with their subscriptions."""
    subscriptions: List[Subscription] = [] 