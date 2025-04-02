from typing import Any, List, Dict, Optional
from datetime import datetime, date, timedelta

from fastapi import APIRouter, Depends, HTTPException, Query, Body
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps
from app.core.config import settings

router = APIRouter()


# Роуты для аналитики ботов
@router.post("/bots", response_model=schemas.BotAnalytics)
def create_bot_analytics(
    *,
    db: Session = Depends(deps.get_db),
    analytics_in: schemas.BotAnalyticsCreate,
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Создание новой записи аналитики бота.
    Только для суперпользователей.
    """
    analytics = crud.bot_analytics.create_analytics(db=db, obj_in=analytics_in)
    return analytics


@router.post("/bots/{bot_id}/daily", response_model=schemas.BotAnalytics)
def update_daily_analytics(
    *,
    db: Session = Depends(deps.get_db),
    bot_id: int,
    views: int = Body(0),
    detail_views: int = Body(0),
    orders: int = Body(0),
    revenue: float = Body(0.0),
    target_date: Optional[date] = Body(None),
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Обновление или создание аналитики бота за день.
    Только для суперпользователей.
    """
    # Проверяем существование бота
    bot = crud.bot.get(db=db, id=bot_id)
    if not bot:
        raise HTTPException(
            status_code=404,
            detail="Bot not found",
        )
    
    # Обновляем или создаем аналитику
    analytics = crud.bot_analytics.update_or_create_daily(
        db=db,
        bot_id=bot_id,
        views=views,
        detail_views=detail_views,
        orders=orders,
        revenue=revenue,
        target_date=target_date
    )
    return analytics


@router.get("/bots/{bot_id}", response_model=List[schemas.BotAnalytics])
def read_bot_analytics(
    *,
    db: Session = Depends(deps.get_db),
    bot_id: int,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Получение аналитики для конкретного бота.
    Владелец бота может видеть аналитику своих ботов.
    Суперпользователи могут видеть аналитику любых ботов.
    """
    # Проверяем существование бота
    bot = crud.bot.get(db=db, id=bot_id)
    if not bot:
        raise HTTPException(
            status_code=404,
            detail="Bot not found",
        )
    
    # Проверяем права доступа
    if not crud.user.is_superuser(current_user) and bot.owner_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="Not enough permissions to access this bot's analytics",
        )
    
    # Получаем аналитику
    if start_date or end_date:
        analytics = crud.bot_analytics.get_by_date_range(
            db=db,
            bot_id=bot_id,
            start_date=start_date,
            end_date=end_date,
            skip=skip,
            limit=limit
        )
    else:
        analytics = crud.bot_analytics.get_by_bot_id(
            db=db, bot_id=bot_id, skip=skip, limit=limit
        )
    
    return analytics


@router.get("/bots", response_model=List[Dict[str, Any]])
def read_bots_summary(
    *,
    db: Session = Depends(deps.get_db),
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Получение агрегированной аналитики по всем ботам.
    Только для суперпользователей.
    """
    summary = crud.bot_analytics.get_summary_by_bot(
        db=db, start_date=start_date, end_date=end_date
    )
    return summary


# Роуты для активности пользователей
@router.post("/activity", response_model=schemas.UserActivity)
def create_user_activity(
    *,
    db: Session = Depends(deps.get_db),
    activity_in: schemas.UserActivityCreate,
    current_user: models.User = Depends(deps.get_current_user),
) -> Any:
    """
    Запись активности пользователя.
    Аутентифицированные пользователи могут создавать записи о своей активности.
    """
    # Проверяем, что пользователь создает запись для себя или является администратором
    if activity_in.user_id != current_user.id and not crud.user.is_superuser(current_user):
        raise HTTPException(
            status_code=403,
            detail="Not enough permissions to create activity for another user",
        )
    
    # Проверяем существование бота, если указан
    if activity_in.bot_id:
        bot = crud.bot.get(db=db, id=activity_in.bot_id)
        if not bot:
            raise HTTPException(
                status_code=404,
                detail="Bot not found",
            )
    
    # Создаем запись активности
    activity = crud.user_activity.create_activity(db=db, obj_in=activity_in)
    return activity


@router.get("/activity/users/{user_id}", response_model=List[schemas.UserActivity])
def read_user_activity(
    *,
    db: Session = Depends(deps.get_db),
    user_id: int,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    bot_id: Optional[int] = None,
    action: Optional[str] = None,
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Получение активности конкретного пользователя.
    Пользователи могут видеть только свою активность.
    Суперпользователи могут видеть активность любого пользователя.
    """
    # Проверяем права доступа
    if user_id != current_user.id and not crud.user.is_superuser(current_user):
        raise HTTPException(
            status_code=403,
            detail="Not enough permissions to access another user's activity",
        )
    
    # Проверяем существование пользователя
    user = crud.user.get(db=db, id=user_id)
    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found",
        )
    
    # Получаем активность пользователя с фильтрами
    activities = crud.user_activity.get_by_time_range(
        db=db,
        user_id=user_id,
        start_date=start_date,
        end_date=end_date,
        bot_id=bot_id,
        action=action,
        skip=skip,
        limit=limit
    )
    
    return activities


@router.get("/activity/bots/{bot_id}", response_model=List[schemas.UserActivity])
def read_bot_user_activity(
    *,
    db: Session = Depends(deps.get_db),
    bot_id: int,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    action: Optional[str] = None,
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Получение активностей пользователей для конкретного бота.
    Владелец бота может видеть активность пользователей своих ботов.
    Суперпользователи могут видеть активность пользователей любых ботов.
    """
    # Проверяем существование бота
    bot = crud.bot.get(db=db, id=bot_id)
    if not bot:
        raise HTTPException(
            status_code=404,
            detail="Bot not found",
        )
    
    # Проверяем права доступа
    if not crud.user.is_superuser(current_user) and bot.owner_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="Not enough permissions to access this bot's user activity",
        )
    
    # Получаем активности пользователей для бота с фильтрами
    activities = crud.user_activity.get_by_time_range(
        db=db,
        bot_id=bot_id,
        start_date=start_date,
        end_date=end_date,
        action=action,
        skip=skip,
        limit=limit
    )
    
    return activities


@router.get("/activity/most-active", response_model=List[Dict[str, Any]])
def read_most_active_users(
    *,
    db: Session = Depends(deps.get_db),
    days: int = 30,
    limit: int = 10,
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Получение списка самых активных пользователей за указанный период.
    Только для суперпользователей.
    """
    users = crud.user_activity.get_most_active_users(
        db=db, days=days, limit=limit
    )
    return users 