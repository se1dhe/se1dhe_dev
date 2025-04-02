from typing import Optional, List, Dict, Any
from pydantic import BaseModel, validator
from datetime import datetime


class ChangelogBase(BaseModel):
    """Base Changelog schema with common attributes."""
    bot_id: int
    version: str
    title: str
    description: str
    release_date: datetime


class ChangelogCreate(ChangelogBase):
    """Schema for changelog creation."""
    pass


class ChangelogUpdate(BaseModel):
    """Schema for updating changelog data."""
    bot_id: Optional[int] = None
    version: Optional[str] = None
    title: Optional[str] = None
    description: Optional[str] = None
    release_date: Optional[datetime] = None


class ChangelogInDBBase(ChangelogBase):
    """Schema for changelog data retrieved from DB with read-only fields."""
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class Changelog(ChangelogInDBBase):
    """API schema for changelog output."""
    pass 