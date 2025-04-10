from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
from ..database import get_db
from ..services.monitoring_service import MonitoringService
from ..schemas.monitoring import (
    MetricCreate,
    MetricResponse,
    AlertCreate,
    AlertResponse,
    AlertUpdate,
    AlertHistoryResponse,
    MonitoringSummary
)

router = APIRouter(prefix="/monitoring", tags=["monitoring"])

@router.post("/metrics/", response_model=MetricResponse)
async def record_metric(
    metric: MetricCreate,
    db: Session = Depends(get_db)
):
    monitoring_service = MonitoringService(db)
    return await monitoring_service.record_metric(metric)

@router.get("/metrics/", response_model=List[MetricResponse])
async def get_metrics(
    name: Optional[str] = None,
    start_time: Optional[datetime] = None,
    end_time: Optional[datetime] = None,
    db: Session = Depends(get_db)
):
    monitoring_service = MonitoringService(db)
    return await monitoring_service.get_metrics(name, start_time, end_time)

@router.post("/alerts/", response_model=AlertResponse)
async def create_alert(
    alert: AlertCreate,
    db: Session = Depends(get_db)
):
    monitoring_service = MonitoringService(db)
    return await monitoring_service.create_alert(alert)

@router.patch("/alerts/{alert_id}/", response_model=AlertResponse)
async def update_alert(
    alert_id: int,
    alert_update: AlertUpdate,
    db: Session = Depends(get_db)
):
    monitoring_service = MonitoringService(db)
    try:
        return await monitoring_service.update_alert(alert_id, alert_update)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.get("/alerts/", response_model=List[AlertResponse])
async def get_alerts(
    status: Optional[str] = None,
    severity: Optional[str] = None,
    db: Session = Depends(get_db)
):
    monitoring_service = MonitoringService(db)
    return await monitoring_service.get_alerts(status, severity)

@router.get("/alerts/{alert_id}/history/", response_model=List[AlertHistoryResponse])
async def get_alert_history(
    alert_id: int,
    start_time: Optional[datetime] = None,
    end_time: Optional[datetime] = None,
    db: Session = Depends(get_db)
):
    monitoring_service = MonitoringService(db)
    return await monitoring_service.get_alert_history(alert_id, start_time, end_time)

@router.get("/summary/", response_model=MonitoringSummary)
async def get_monitoring_summary(db: Session = Depends(get_db)):
    monitoring_service = MonitoringService(db)
    return await monitoring_service.get_monitoring_summary() 