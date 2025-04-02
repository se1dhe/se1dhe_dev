from typing import Optional, List, Dict, Any, Union, ClassVar
from pydantic import BaseModel, validator, HttpUrl, Field
from datetime import datetime
from decimal import Decimal

from app.schemas.user import User
from app.schemas.category import Category
from app.schemas.base import BotBase


class CategoryBase(BaseModel):
    """Base Category schema with common attributes."""
    name: str
    description: Optional[str] = None
    slug: str
    is_active: bool = True
    discount_percentage: Optional[float] = 0


class CategoryCreate(CategoryBase):
    """Schema for category creation."""
    pass


class CategoryUpdate(CategoryBase):
    """Schema for updating category data."""
    name: Optional[str] = None
    description: Optional[str] = None
    slug: Optional[str] = None
    is_active: Optional[bool] = None
    discount_percentage: Optional[float] = None


class CategoryInDBBase(CategoryBase):
    """Schema for category data retrieved from DB with read-only fields."""
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class Category(CategoryInDBBase):
    """API schema for category output."""
    pass


# Bot Schemas
class BotCreate(BotBase):
    pass


class BotUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    category_id: Optional[int] = None
    telegram_token: Optional[str] = None
    telegram_username: Optional[str] = None
    is_active: Optional[bool] = None
    is_verified: Optional[bool] = None


class BotInDBBase(BotBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class Bot(BotInDBBase):
    pass


class BotWithCategory(Bot):
    Category: ClassVar[type] = Category
    category: Category


class BotWithDetails(Bot):
    User: ClassVar[type] = User
    Category: ClassVar[type] = Category
    owner: User
    category: Category


class SubscriptionBase(BaseModel):
    """Base schema for user-bot subscription."""
    user_id: int
    bot_id: int
    expires_at: datetime


class SubscriptionCreate(SubscriptionBase):
    """Schema for creating a subscription."""
    pass


class SubscriptionUpdate(BaseModel):
    """Schema for updating a subscription."""
    expires_at: Optional[datetime] = None


class Subscription(SubscriptionBase):
    """API schema for subscription output."""
    created_at: datetime
    
    class Config:
        from_attributes = True 