from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field
from datetime import datetime
from enum import Enum


class FeatureRequestStatus(str, Enum):
    """Enum for feature request status values."""
    PROPOSED = "proposed"
    REVIEWING = "reviewing"
    APPROVED = "approved"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    REJECTED = "rejected"


class FeaturePriority(str, Enum):
    """Enum for feature priority levels."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class FeatureRequestBase(BaseModel):
    """Base FeatureRequest schema with common attributes."""
    user_id: int
    bot_id: int
    title: str
    description: str
    technical_details: Optional[str] = None
    priority: FeaturePriority = FeaturePriority.MEDIUM
    is_public: bool = True


class FeatureRequestCreate(FeatureRequestBase):
    """Schema for feature request creation."""
    pass


class FeatureRequestUpdate(BaseModel):
    """Schema for updating feature request data."""
    title: Optional[str] = None
    description: Optional[str] = None
    technical_details: Optional[str] = None
    status: Optional[FeatureRequestStatus] = None
    priority: Optional[FeaturePriority] = None
    is_public: Optional[bool] = None


class FeatureRequestInDBBase(FeatureRequestBase):
    """Schema for feature request data retrieved from DB with read-only fields."""
    id: int
    status: FeatureRequestStatus
    votes_count: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class FeatureRequest(FeatureRequestInDBBase):
    """API schema for feature request output."""
    pass


# Схемы для голосов
class FeatureVoteBase(BaseModel):
    """Base FeatureVote schema with common attributes."""
    user_id: int
    feature_id: int


class FeatureVoteCreate(FeatureVoteBase):
    """Schema for feature vote creation."""
    pass


class FeatureVoteInDBBase(FeatureVoteBase):
    """Schema for feature vote data retrieved from DB with read-only fields."""
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True


class FeatureVote(FeatureVoteInDBBase):
    """API schema for feature vote output."""
    pass


# Схемы для комментариев
class FeatureCommentBase(BaseModel):
    """Base FeatureComment schema with common attributes."""
    user_id: int
    feature_id: int
    text: str


class FeatureCommentCreate(FeatureCommentBase):
    """Schema for feature comment creation."""
    pass


class FeatureCommentUpdate(BaseModel):
    """Schema for updating feature comment data."""
    text: Optional[str] = None


class FeatureCommentInDBBase(FeatureCommentBase):
    """Schema for feature comment data retrieved from DB with read-only fields."""
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class FeatureComment(FeatureCommentInDBBase):
    """API schema for feature comment output."""
    pass 