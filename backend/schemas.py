from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from enum import Enum

class UserRole(str, Enum):
    ADMIN = "admin"
    CLIENT = "client"
    USER = "user"

class UserBase(BaseModel):
    telegram_id: int
    username: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    role: UserRole = UserRole.USER
    balance: float = 0.0

class UserCreate(UserBase):
    pass

class UserUpdate(UserBase):
    pass

class User(UserBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class CategoryBase(BaseModel):
    name: str
    description: Optional[str] = None
    discount: float = 0.0
    is_active: bool = True

class CategoryCreate(CategoryBase):
    pass

class CategoryUpdate(CategoryBase):
    pass

class Category(CategoryBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class BotBase(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    category_id: int
    is_active: bool = True

class BotCreate(BotBase):
    pass

class BotUpdate(BotBase):
    pass

class Bot(BotBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class PurchaseBase(BaseModel):
    user_id: int
    bot_id: int
    price: float
    status: str

class PurchaseCreate(PurchaseBase):
    pass

class Purchase(PurchaseBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

class BugReportBase(BaseModel):
    user_id: int
    bot_id: int
    title: str
    description: str
    status: str = "new"

class BugReportCreate(BugReportBase):
    pass

class BugReportUpdate(BugReportBase):
    pass

class BugReport(BugReportBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class ChangelogBase(BaseModel):
    bot_id: int
    version: str
    changes: str

class ChangelogCreate(ChangelogBase):
    pass

class Changelog(ChangelogBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True 