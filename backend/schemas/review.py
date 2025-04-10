from pydantic import BaseModel, Field, validator
from typing import Optional
from datetime import datetime

class ReviewBase(BaseModel):
    rating: float = Field(..., ge=1, le=5)
    comment: Optional[str] = None

    @validator('rating')
    def round_rating(cls, v):
        return round(v * 2) / 2  # Округляем до 0.5

class ReviewCreate(ReviewBase):
    bot_id: int

class ReviewUpdate(ReviewBase):
    pass

class ReviewInDB(ReviewBase):
    id: int
    user_id: int
    bot_id: int
    is_verified: bool
    is_approved: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class ReviewResponse(ReviewInDB):
    user_name: str
    bot_name: str

    class Config:
        from_attributes = True 