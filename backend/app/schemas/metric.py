from typing import Optional, Dict, Any, List
from pydantic import BaseModel
from datetime import datetime, date


class MetricBase(BaseModel):
    """Base schema for metrics."""
    name: str
    value: float
    dimensions: Optional[Dict[str, Any]] = None


class MetricCreate(MetricBase):
    """Schema for metric creation."""
    pass


class MetricUpdate(BaseModel):
    """Schema for updating metric data."""
    name: Optional[str] = None
    value: Optional[float] = None
    dimensions: Optional[Dict[str, Any]] = None


class MetricInDBBase(MetricBase):
    """Schema for metric data retrieved from DB with read-only fields."""
    id: int
    timestamp: datetime
    
    class Config:
        from_attributes = True


class Metric(MetricInDBBase):
    """Schema for metric data with read-only fields."""
    pass


class MetricQuery(BaseModel):
    """Schema for querying metrics."""
    name: str
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    dimensions: Optional[Dict[str, Any]] = None
    group_by: Optional[List[str]] = None
    limit: Optional[int] = 100


class BotAnalyticsBase(BaseModel):
    """Base schema for bot analytics."""
    bot_id: int
    views: int = 0
    detail_views: int = 0
    orders: int = 0
    revenue: float = 0.0
    date: date


class BotAnalyticsCreate(BaseModel):
    """Schema for bot analytics creation."""
    bot_id: int
    views: Optional[int] = 0
    detail_views: Optional[int] = 0
    orders: Optional[int] = 0
    revenue: Optional[float] = 0.0


class BotAnalyticsUpdate(BaseModel):
    """Schema for bot analytics update."""
    views: Optional[int] = None
    detail_views: Optional[int] = None
    orders: Optional[int] = None
    revenue: Optional[float] = None


class BotAnalytics(BotAnalyticsBase):
    """Schema for bot analytics data with read-only fields."""
    id: int
    
    class Config:
        from_attributes = True


class UserActivityBase(BaseModel):
    """Base schema for user activity."""
    user_id: int
    action: str
    bot_id: Optional[int] = None
    details: Optional[Dict[str, Any]] = None
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None


class UserActivityCreate(UserActivityBase):
    """Schema for user activity creation."""
    pass


class UserActivity(UserActivityBase):
    """Schema for user activity data with read-only fields."""
    id: int
    timestamp: datetime
    
    class Config:
        from_attributes = True 