from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime, timedelta
from ..database import get_db
from ..services.analytics_service import AnalyticsService
from ..schemas.analytics import (
    AnalyticsCreate,
    AnalyticsResponse,
    BotAnalyticsResponse,
    AnalyticsSummary
)

router = APIRouter(prefix="/analytics", tags=["analytics"])

@router.post("/events/", response_model=AnalyticsResponse)
async def track_event(
    event: AnalyticsCreate,
    db: Session = Depends(get_db)
):
    analytics_service = AnalyticsService(db)
    return await analytics_service.track_event(event)

@router.get("/bots/{bot_id}/", response_model=List[BotAnalyticsResponse])
async def get_bot_analytics(
    bot_id: int,
    start_date: datetime,
    end_date: datetime,
    db: Session = Depends(get_db)
):
    analytics_service = AnalyticsService(db)
    return await analytics_service.get_bot_analytics(bot_id, start_date, end_date)

@router.get("/summary/", response_model=AnalyticsSummary)
async def get_analytics_summary(
    days: int = 30,
    db: Session = Depends(get_db)
):
    analytics_service = AnalyticsService(db)
    return await analytics_service.get_analytics_summary(days) 