from typing import Optional, List
from pydantic import BaseModel, EmailStr, validator
from datetime import datetime


# Общие свойства
class UserBase(BaseModel):
    email: Optional[EmailStr] = None
    username: Optional[str] = None
    is_active: Optional[bool] = True
    is_superuser: bool = False
    full_name: Optional[str] = None
    telegram_id: Optional[str] = None


# Свойства для создания через API
class UserCreate(UserBase):
    email: EmailStr
    username: str
    password: str

    @validator('username')
    def username_alphanumeric(cls, v):
        assert v.isalnum(), 'Username должен содержать только буквы и цифры'
        return v


# Свойства для обновления через API
class UserUpdate(UserBase):
    password: Optional[str] = None


# Свойства для чтения из БД
class UserInDBBase(UserBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True


# Дополнительные свойства для возврата через API
class User(UserInDBBase):
    pass


# Дополнительные свойства, хранящиеся в БД
class UserInDB(UserInDBBase):
    hashed_password: str


# Схема для расширенной информации о пользователе
class UserWithDetails(User):
    subscriptions_count: Optional[int] = 0
    orders_count: Optional[int] = 0