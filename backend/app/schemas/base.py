from typing import Optional
from pydantic import BaseModel
from datetime import datetime

class UserBase(BaseModel):
    email: str
    username: str
    telegram_id: Optional[int] = None
    telegram_username: Optional[str] = None
    is_active: bool = True
    is_superuser: bool = False
    is_verified: bool = False

class BotBase(BaseModel):
    name: str
    description: str
    price: float
    category_id: int
    owner_id: int
    telegram_token: str
    telegram_username: str
    is_active: bool = True
    is_verified: bool = False
    rating: float = 0.0
    total_sales: int = 0
    total_revenue: float = 0.0

class CategoryBase(BaseModel):
    name: str
    description: str
    is_active: bool = True 