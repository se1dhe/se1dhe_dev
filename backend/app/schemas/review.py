from typing import Optional
from pydantic import BaseModel, Field, validator
from datetime import datetime


class ReviewBase(BaseModel):
    """Base Review schema with common attributes."""
    user_id: int
    bot_id: int
    rating: float = Field(..., ge=1.0, le=5.0, description="Оценка от 1 до 5")
    title: str
    content: str
    
    @validator('rating')
    def rating_must_be_valid(cls, v):
        """Проверяем, что рейтинг в диапазоне от 1 до 5"""
        if v < 1.0 or v > 5.0:
            raise ValueError('Рейтинг должен быть от 1 до 5')
        return round(v, 1)  # Округляем до 1 десятичного знака


class ReviewCreate(ReviewBase):
    """Schema for review creation."""
    pass


class ReviewUpdate(BaseModel):
    """Schema for updating review data."""
    rating: Optional[float] = Field(None, ge=1.0, le=5.0, description="Оценка от 1 до 5")
    title: Optional[str] = None
    content: Optional[str] = None
    
    @validator('rating')
    def rating_must_be_valid(cls, v):
        """Проверяем, что рейтинг в диапазоне от 1 до 5"""
        if v is not None:
            if v < 1.0 or v > 5.0:
                raise ValueError('Рейтинг должен быть от 1 до 5')
            return round(v, 1)  # Округляем до 1 десятичного знака
        return v


class ReviewInDBBase(ReviewBase):
    """Schema for review data retrieved from DB with read-only fields."""
    id: int
    verified_purchase: bool
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class Review(ReviewInDBBase):
    """API schema for review output."""
    pass


class ReviewStats(BaseModel):
    """Schema for bot review statistics."""
    bot_id: int
    average_rating: float
    total_reviews: int
    rating_distribution: dict[int, int]  # {5: 10, 4: 5, 3: 2, 2: 1, 1: 0} 