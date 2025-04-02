from typing import Any, List, Optional

from fastapi import APIRouter, Depends, HTTPException, Path, Query, status
from sqlalchemy.orm import Session

from app import crud, schemas
from app.api import deps

router = APIRouter()


@router.get("/", response_model=List[schemas.Notification])
async def read_notifications(
    db: Session = Depends(deps.get_db),
    skip: int = Query(0, description="Сколько записей пропустить"),
    limit: int = Query(100, description="Максимальное количество записей"),
    unread_only: bool = Query(False, description="Показать только непрочитанные"),
    current_user: schemas.User = Depends(deps.get_current_user),
) -> Any:
    """
    Получить список уведомлений текущего пользователя.
    """
    return crud.notification.get_user_notifications(
        db, user_id=current_user.id, skip=skip, limit=limit, unread_only=unread_only
    )


@router.get("/count", response_model=schemas.NotificationCount)
async def get_notification_count(
    db: Session = Depends(deps.get_db),
    current_user: schemas.User = Depends(deps.get_current_user),
) -> Any:
    """
    Получить количество уведомлений пользователя.
    """
    return crud.notification.get_notification_count(db, user_id=current_user.id)


@router.put("/{notification_id}/read", response_model=schemas.Notification)
async def mark_notification_as_read(
    *,
    db: Session = Depends(deps.get_db),
    notification_id: int = Path(..., description="ID уведомления"),
    current_user: schemas.User = Depends(deps.get_current_user),
) -> Any:
    """
    Отметить уведомление как прочитанное.
    """
    notification = crud.notification.mark_as_read(
        db, notification_id=notification_id, user_id=current_user.id
    )
    
    if not notification:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Уведомление не найдено или уже прочитано"
        )
    
    return notification


@router.put("/mark-all-read", response_model=dict)
async def mark_all_notifications_as_read(
    db: Session = Depends(deps.get_db),
    current_user: schemas.User = Depends(deps.get_current_user),
) -> Any:
    """
    Отметить все уведомления пользователя как прочитанные.
    """
    count = crud.notification.mark_all_as_read(db, user_id=current_user.id)
    
    return {"message": f"Отмечено {count} уведомлений как прочитанные"}


@router.delete("/{notification_id}", response_model=schemas.Notification)
async def delete_notification(
    *,
    db: Session = Depends(deps.get_db),
    notification_id: int = Path(..., description="ID уведомления"),
    current_user: schemas.User = Depends(deps.get_current_user),
) -> Any:
    """
    Удалить уведомление.
    """
    # Проверяем, существует ли уведомление и принадлежит ли оно пользователю
    notification = db.query(crud.notification.model).filter(
        crud.notification.model.id == notification_id,
        crud.notification.model.user_id == current_user.id
    ).first()
    
    if not notification:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Уведомление не найдено"
        )
    
    return crud.notification.remove(db, id=notification_id)


@router.post("/system", response_model=schemas.Notification)
async def create_system_notification(
    *,
    db: Session = Depends(deps.get_db),
    title: str,
    message: str,
    user_id: int,
    link: Optional[str] = None,
    send_telegram: bool = True,
    current_user: schemas.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Создать системное уведомление.
    Только для суперпользователей.
    """
    notification = await crud.notification.create_system_notification(
        db=db,
        user_id=user_id,
        title=title,
        message=message,
        link=link,
        send_telegram=send_telegram
    )
    return notification


@router.post("/order", response_model=schemas.Notification)
async def create_order_notification(
    *,
    db: Session = Depends(deps.get_db),
    title: str,
    message: str,
    user_id: int,
    order_id: int,
    link: Optional[str] = None,
    send_telegram: bool = True,
    current_user: schemas.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Создать уведомление о заказе.
    Только для суперпользователей.
    """
    notification = await crud.notification.create_order_notification(
        db=db,
        user_id=user_id,
        title=title,
        message=message,
        order_id=order_id,
        link=link,
        send_telegram=send_telegram
    )
    return notification


@router.post("/bot-update", response_model=schemas.Notification)
async def create_bot_update_notification(
    *,
    db: Session = Depends(deps.get_db),
    title: str,
    message: str,
    user_id: int,
    bot_id: int,
    link: Optional[str] = None,
    send_telegram: bool = True,
    current_user: schemas.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Создать уведомление об обновлении бота.
    Только для суперпользователей.
    """
    notification = await crud.notification.create_bot_update_notification(
        db=db,
        user_id=user_id,
        title=title,
        message=message,
        bot_id=bot_id,
        link=link,
        send_telegram=send_telegram
    )
    return notification


@router.post("/feature", response_model=schemas.Notification)
async def create_feature_notification(
    *,
    db: Session = Depends(deps.get_db),
    title: str,
    message: str,
    user_id: int,
    feature_id: int,
    link: Optional[str] = None,
    send_telegram: bool = True,
    current_user: schemas.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Создать уведомление о запросе функции.
    Только для суперпользователей.
    """
    notification = await crud.notification.create_feature_notification(
        db=db,
        user_id=user_id,
        title=title,
        message=message,
        feature_id=feature_id,
        link=link,
        send_telegram=send_telegram
    )
    return notification 