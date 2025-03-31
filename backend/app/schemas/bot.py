from typing import Optional, List, Any
from pydantic import BaseModel, validator
from datetime import datetime


# Общие свойства
class BotBase(BaseModel):
    name: Optional[str] = None
    slug: Optional[str] = None
    short_description: Optional[str] = None
    full_description: Optional[str] = None
    readme_md: Optional[str] = None
    price: Optional[float] = None
    discount_percent: Optional[float] = 0
    category_id: Optional[int] = None
    preview_image_url: Optional[str] = None
    images: Optional[List[str]] = None
    videos: Optional[List[str]] = None
    demo_url: Optional[str] = None
    features: Optional[List[str]] = None
    is_active: Optional[bool] = True
    is_featured: Optional[bool] = False


# Свойства для создания через API
class BotCreate(BotBase):
    name: str
    slug: str
    short_description: str
    price: float
    category_id: int

    @validator('slug')
    def slug_alphanumeric_dash(cls, v):
        import re
        assert re.match(r'^[a-z0-9]+(-[a-z0-9]+)*$', v), 'Slug должен содержать только строчные буквы, цифры и дефисы'
        return v


# Свойства для обновления через API
class BotUpdate(BotBase):
    pass


# Свойства для чтения из БД
class BotInDBBase(BotBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True


# Дополнительные свойства для возврата через API
class Bot(BotInDBBase):
    pass


# Расширенная схема со всеми деталями
class BotWithDetails(Bot):
    category_name: Optional[str] = None
    final_price: Optional[float] = None
    subscriptions_count: Optional[int] = 0

    @validator('final_price', always=True)
    def calculate_final_price(cls, v, values):
        price = values.get('price', 0)
        discount = values.get('discount_percent', 0)
        if price is not None and discount is not None:
            return price * (1 - discount / 100)
        return price