from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List
from datetime import datetime
from ..models.ab_test import ABTestType, ABTestStatus

class ABTestBase(BaseModel):
    name: str = Field(..., max_length=255)
    description: Optional[str] = None
    type: ABTestType
    target_audience: Optional[Dict[str, Any]] = None
    variants: Dict[str, Any]
    metrics: List[str]

class ABTestCreate(ABTestBase):
    pass

class ABTestUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=255)
    description: Optional[str] = None
    status: Optional[ABTestStatus] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    target_audience: Optional[Dict[str, Any]] = None
    variants: Optional[Dict[str, Any]] = None
    metrics: Optional[List[str]] = None

class ABTestInDB(ABTestBase):
    id: int
    status: ABTestStatus
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class ABTestResponse(ABTestInDB):
    pass

class ABTestResultBase(BaseModel):
    test_id: int
    variant: str
    user_id: Optional[int] = None
    metrics_data: Dict[str, Any]

class ABTestResultCreate(ABTestResultBase):
    pass

class ABTestResultInDB(ABTestResultBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

class ABTestResultResponse(ABTestResultInDB):
    pass

class ABTestStatistics(BaseModel):
    test_id: int
    variant: str
    total_participants: int
    metrics_summary: Dict[str, Dict[str, float]]
    confidence_level: Optional[float] = None
    is_significant: Optional[bool] = None 