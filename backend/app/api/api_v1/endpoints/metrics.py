from typing import Any, List, Dict, Optional
from datetime import datetime, date, timedelta

from fastapi import APIRouter, Depends, HTTPException, Query, Body
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps
from app.core.config import settings

router = APIRouter()


@router.post("/", response_model=schemas.Metric)
def create_metric(
    *,
    db: Session = Depends(deps.get_db),
    metric_in: schemas.MetricCreate,
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Создание новой метрики.
    Только для суперпользователей.
    """
    metric = crud.metric.create_metric(
        db=db, 
        name=metric_in.name, 
        value=metric_in.value, 
        dimensions=metric_in.dimensions
    )
    return metric


@router.get("/", response_model=List[schemas.Metric])
def read_metrics(
    *,
    db: Session = Depends(deps.get_db),
    name: Optional[str] = None,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Получение списка метрик с возможностью фильтрации.
    Только для суперпользователей.
    """
    if name and (start_date or end_date):
        # Если указано имя и даты, фильтруем по времени
        metrics = crud.metric.get_by_time_range(
            db=db, 
            start_date=start_date or datetime.min, 
            end_date=end_date or datetime.utcnow(),
            name=name,
            skip=skip,
            limit=limit
        )
    elif name:
        # Если указано только имя, фильтруем по нему
        metrics = crud.metric.get_by_name(
            db=db, name=name, skip=skip, limit=limit
        )
    elif start_date or end_date:
        # Если указаны только даты, фильтруем по времени
        metrics = crud.metric.get_by_time_range(
            db=db, 
            start_date=start_date or datetime.min, 
            end_date=end_date or datetime.utcnow(),
            skip=skip,
            limit=limit
        )
    else:
        # Если ничего не указано, возвращаем все метрики
        metrics = crud.metric.get_multi(db, skip=skip, limit=limit)
    
    return metrics


@router.post("/query", response_model=List[Dict[str, Any]])
def query_metrics(
    *,
    db: Session = Depends(deps.get_db),
    query: schemas.MetricQuery,
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Сложный запрос метрик с агрегацией.
    Только для суперпользователей.
    """
    result = crud.metric.query_metrics(db=db, query=query)
    return result


@router.get("/last/{name}", response_model=Dict[str, Any])
def get_last_metric(
    *,
    db: Session = Depends(deps.get_db),
    name: str,
    dimensions: Optional[Dict[str, Any]] = Body(None),
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Получить последнее значение метрики по имени и опциональным измерениям.
    Только для суперпользователей.
    """
    value = crud.metric.get_last_value(db=db, name=name, dimensions=dimensions)
    if value is None:
        raise HTTPException(
            status_code=404,
            detail=f"Metric with name {name} not found",
        )
    return {"name": name, "value": value, "dimensions": dimensions} 