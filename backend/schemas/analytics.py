from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from datetime import datetime
from ..models.analytics import AnalyticsEventType

class AnalyticsEventBase(BaseModel):
    event_type: AnalyticsEventType
    event_data: Optional[Dict[str, Any]] = None
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None
    referrer: Optional[str] = None

class AnalyticsEventCreate(AnalyticsEventBase):
    user_id: Optional[int] = None

class AnalyticsEventInDB(AnalyticsEventBase):
    id: int
    user_id: Optional[int]
    created_at: datetime

    class Config:
        from_attributes = True

class AnalyticsEventResponse(AnalyticsEventInDB):
    pass

class BotAnalyticsBase(BaseModel):
    bot_id: int
    date: datetime
    views: int = 0
    purchases: int = 0
    revenue: float = 0.0
    avg_rating: Optional[float] = None
    review_count: int = 0

class BotAnalyticsCreate(BotAnalyticsBase):
    pass

class BotAnalyticsUpdate(BaseModel):
    views: Optional[int] = None
    purchases: Optional[int] = None
    revenue: Optional[float] = None
    avg_rating: Optional[float] = None
    review_count: Optional[int] = None

class BotAnalyticsInDB(BotAnalyticsBase):
    id: int

    class Config:
        from_attributes = True

class BotAnalyticsResponse(BotAnalyticsInDB):
    pass 