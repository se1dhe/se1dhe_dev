from typing import Optional
from pydantic import BaseModel
from datetime import datetime

class SubscriptionBase(BaseModel):
    """Base Subscription schema with common attributes."""
    user_id: int
    bot_id: int
    is_active: bool = True
    auto_renew: bool = False
    expires_at: datetime

class SubscriptionCreate(SubscriptionBase):
    """Schema for subscription creation."""
    pass

class SubscriptionUpdate(BaseModel):
    """Schema for updating subscription data."""
    is_active: Optional[bool] = None
    auto_renew: Optional[bool] = None
    expires_at: Optional[datetime] = None

class SubscriptionInDBBase(SubscriptionBase):
    """Schema for subscription data retrieved from DB with read-only fields."""
    id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class Subscription(SubscriptionInDBBase):
    """API schema for subscription output."""
    pass 