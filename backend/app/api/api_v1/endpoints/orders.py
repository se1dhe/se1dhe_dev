from typing import Any, List, Optional

from fastapi import APIRouter, Body, Depends, HTTPException, Path, Query, status
from sqlalchemy.orm import Session

from app import crud, schemas
from app.api import deps

router = APIRouter()


@router.get("/", response_model=List[schemas.Order])
def read_orders(
    db: Session = Depends(deps.get_db),
    skip: int = Query(0, description="Сколько записей пропустить"),
    limit: int = Query(100, description="Максимальное количество записей"),
    order_status: Optional[schemas.OrderStatus] = Query(None, description="Статус заказа для фильтрации"),
    current_user: schemas.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Получить список всех заказов.
    Только для администраторов.
    """
    if order_status:
        return crud.order.get_by_status(db, status=order_status, skip=skip, limit=limit)
    else:
        return crud.order.get_multi(db, skip=skip, limit=limit)


@router.get("/my", response_model=List[schemas.Order])
def read_my_orders(
    db: Session = Depends(deps.get_db),
    skip: int = Query(0, description="Сколько записей пропустить"),
    limit: int = Query(100, description="Максимальное количество записей"),
    current_user: schemas.User = Depends(deps.get_current_user),
) -> Any:
    """
    Получить список своих заказов.
    """
    return crud.order.get_by_user(db, user_id=current_user.id, skip=skip, limit=limit)


@router.post("/", response_model=schemas.Order)
def create_order(
    *,
    db: Session = Depends(deps.get_db),
    order_in: schemas.OrderCreate,
    current_user: schemas.User = Depends(deps.get_current_user),
) -> Any:
    """
    Создать новый заказ.
    """
    # Проверяем, что бот существует
    bot = crud.bot.get(db, id=order_in.bot_id)
    if not bot:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Указанный бот не найден"
        )
    
    # Принудительно устанавливаем user_id текущего пользователя
    order_data = order_in.dict()
    order_data["user_id"] = current_user.id
    
    return crud.order.create(db, obj_in=schemas.OrderCreate(**order_data))


@router.get("/details", response_model=List[schemas.OrderWithDetails])
def read_orders_with_details(
    db: Session = Depends(deps.get_db),
    skip: int = Query(0, description="Сколько записей пропустить"),
    limit: int = Query(100, description="Максимальное количество записей"),
    current_user: schemas.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Получить список заказов с детальной информацией о пользователях и ботах.
    Только для администраторов.
    """
    return crud.order.get_multi_with_details(db, skip=skip, limit=limit)


@router.get("/{order_id}", response_model=schemas.OrderWithDetails)
def read_order(
    *,
    db: Session = Depends(deps.get_db),
    order_id: int = Path(..., description="ID заказа"),
    current_user: schemas.User = Depends(deps.get_current_user),
) -> Any:
    """
    Получить информацию о заказе по ID.
    """
    order = crud.order.get_with_details(db, id=order_id)
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Заказ не найден"
        )
    
    # Обычные пользователи могут просматривать только свои заказы
    if not current_user.is_superuser and order.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Недостаточно прав доступа"
        )
    
    return order


@router.put("/{order_id}/status", response_model=schemas.Order)
def update_order_status(
    *,
    db: Session = Depends(deps.get_db),
    order_id: int = Path(..., description="ID заказа"),
    status: schemas.OrderStatus = Body(..., description="Новый статус заказа"),
    current_user: schemas.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Обновить статус заказа.
    Только для администраторов.
    """
    order = crud.order.get(db, id=order_id)
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Заказ не найден"
        )
    
    return crud.order.update_status(db, db_obj=order, status=status)


@router.put("/{order_id}/payment", response_model=schemas.Order)
def update_payment_info(
    *,
    db: Session = Depends(deps.get_db),
    order_id: int = Path(..., description="ID заказа"),
    payment_id: str = Body(..., description="ID платежа"),
    current_user: schemas.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Обновить информацию о платеже.
    Только для администраторов.
    """
    order = crud.order.get(db, id=order_id)
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Заказ не найден"
        )
    
    return crud.order.update_payment_info(db, db_obj=order, payment_id=payment_id) 