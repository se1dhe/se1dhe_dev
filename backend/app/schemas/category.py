from typing import Optional, List
from pydantic import BaseModel, validator
from datetime import datetime


# Общие свойства
class CategoryBase(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    slug: Optional[str] = None
    image_url: Optional[str] = None
    is_active: Optional[bool] = True
    discount_percent: Optional[float] = 0


# Свойства для создания через API
class CategoryCreate(CategoryBase):
    name: str
    slug: str

    @validator('slug')
    def slug_alphanumeric_dash(cls, v):
        import re
        assert re.match(r'^[a-z0-9]+(-[a-z0-9]+)*$', v), 'Slug должен содержать только строчные буквы, цифры и дефисы'
        return v


# Свойства для обновления через API
class CategoryUpdate(CategoryBase):
    pass


# Свойства для чтения из БД
class CategoryInDBBase(CategoryBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True


# Дополнительные свойства для возврата через API
class Category(CategoryInDBBase):
    pass


# Расширенная схема с количеством ботов
class CategoryWithBotsCount(Category):
    bots_count: int = 0