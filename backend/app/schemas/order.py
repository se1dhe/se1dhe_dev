from typing import Optional, List, ClassVar
from pydantic import BaseModel
from datetime import datetime
from enum import Enum
from decimal import Decimal

from app.schemas.user import User
from app.schemas.bot import BotWithCategory


class OrderStatus(str, Enum):
    """Enum for order status values."""
    PENDING = "pending"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    FAILED = "failed"


class PaymentMethod(str, Enum):
    """Enum for payment methods."""
    CARD = "card"
    PAYPAL = "paypal"
    CRYPTO = "crypto"
    BANK_TRANSFER = "bank_transfer"


class OrderBase(BaseModel):
    """Base Order schema with common attributes."""
    user_id: int
    bot_id: int
    amount: Decimal
    status: str
    payment_method: str
    payment_id: Optional[str] = None


class OrderCreate(OrderBase):
    """Schema for order creation."""
    pass


class OrderUpdate(OrderBase):
    """Schema for updating order data."""
    bot_id: Optional[int] = None
    user_id: Optional[int] = None
    amount: Optional[Decimal] = None
    status: Optional[str] = None
    payment_method: Optional[str] = None


class OrderInDBBase(OrderBase):
    """Schema for order data retrieved from DB with read-only fields."""
    id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class Order(OrderInDBBase):
    """API schema for order output."""
    pass


class OrderWithDetails(Order):
    """Order schema with detailed user and bot information."""
    User: ClassVar[type] = User
    BotWithCategory: ClassVar[type] = BotWithCategory
    user: User
    bot: BotWithCategory 