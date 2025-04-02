from typing import Any, List, Optional
from fastapi import APIRouter, Depends, HTTPException, Path, Query, status
from sqlalchemy.orm import Session

from app import crud, schemas
from app.api import deps
from app.core.cache import cached

router = APIRouter()


@router.get("/", response_model=List[schemas.Subscription])
@cached(namespace="subscriptions", expire=60 * 5)  # Кэшируем на 5 минут
async def read_subscriptions(
    db: Session = Depends(deps.get_db),
    skip: int = Query(0, description="Сколько записей пропустить"),
    limit: int = Query(100, description="Максимальное количество записей"),
    current_user: schemas.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Получить список всех подписок.
    Только для администраторов.
    """
    return crud.subscription.get_multi(db, skip=skip, limit=limit)


@router.get("/my", response_model=List[schemas.Subscription])
@cached(namespace="subscriptions", expire=60 * 5, user_specific=True)  # Кэшируем на 5 минут с учетом пользователя
async def read_my_subscriptions(
    db: Session = Depends(deps.get_db),
    skip: int = Query(0, description="Сколько записей пропустить"),
    limit: int = Query(100, description="Максимальное количество записей"),
    current_user: schemas.User = Depends(deps.get_current_user),
) -> Any:
    """
    Получить список своих подписок.
    """
    return crud.subscription.get_user_subscriptions(
        db, user_id=current_user.id, skip=skip, limit=limit
    )


@router.get("/bot/{bot_id}", response_model=List[schemas.Subscription])
@cached(namespace="subscriptions", expire=60 * 5)  # Кэшируем на 5 минут
async def read_bot_subscriptions(
    *,
    db: Session = Depends(deps.get_db),
    bot_id: int = Path(..., description="ID бота"),
    skip: int = Query(0, description="Сколько записей пропустить"),
    limit: int = Query(100, description="Максимальное количество записей"),
) -> Any:
    """
    Получить список активных подписок на бота.
    """
    # Проверяем, что бот существует
    bot = crud.bot.get(db, id=bot_id)
    if not bot:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Указанный бот не найден"
        )
    
    return crud.subscription.get_bot_subscriptions(
        db, bot_id=bot_id, skip=skip, limit=limit
    )


@router.get("/bot/{bot_id}/active", response_model=schemas.Subscription)
@cached(namespace="subscriptions", expire=60 * 5, user_specific=True)  # Кэшируем на 5 минут с учетом пользователя
async def read_active_subscription(
    *,
    db: Session = Depends(deps.get_db),
    bot_id: int = Path(..., description="ID бота"),
    current_user: schemas.User = Depends(deps.get_current_user),
) -> Any:
    """
    Получить активную подписку пользователя на бота.
    """
    # Проверяем, что бот существует
    bot = crud.bot.get(db, id=bot_id)
    if not bot:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Указанный бот не найден"
        )
    
    subscription = crud.subscription.get_active_subscription(
        db, user_id=current_user.id, bot_id=bot_id
    )
    if not subscription:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Активная подписка не найдена"
        )
    
    return subscription


@router.post("/bot/{bot_id}", response_model=schemas.Subscription)
async def create_subscription(
    *,
    db: Session = Depends(deps.get_db),
    bot_id: int = Path(..., description="ID бота"),
    subscription_in: schemas.SubscriptionCreate,
    current_user: schemas.User = Depends(deps.get_current_user),
) -> Any:
    """
    Создать новую подписку на бота.
    """
    # Проверяем, что бот существует
    bot = crud.bot.get(db, id=bot_id)
    if not bot:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Указанный бот не найден"
        )
    
    # Проверяем, нет ли уже активной подписки
    existing_subscription = crud.subscription.get_active_subscription(
        db, user_id=current_user.id, bot_id=bot_id
    )
    if existing_subscription:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="У вас уже есть активная подписка на этого бота"
        )
    
    # Здесь должна быть логика обработки платежа
    # В данном примере мы просто создаем подписку
    payment_data = {
        "method": "telegram",
        "id": "payment_id"  # В реальном приложении здесь будет ID платежа
    }
    
    return await crud.subscription.create_with_payment(
        db, obj_in=subscription_in, payment_data=payment_data
    )


@router.put("/{subscription_id}/cancel", response_model=schemas.Subscription)
async def cancel_subscription(
    *,
    db: Session = Depends(deps.get_db),
    subscription_id: int = Path(..., description="ID подписки"),
    current_user: schemas.User = Depends(deps.get_current_user),
) -> Any:
    """
    Отменить подписку.
    """
    subscription = crud.subscription.get(db, id=subscription_id)
    if not subscription:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Подписка не найдена"
        )
    
    # Проверяем права доступа
    if not current_user.is_superuser and subscription.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Недостаточно прав доступа"
        )
    
    return await crud.subscription.cancel_subscription(
        db, subscription_id=subscription_id, user_id=current_user.id
    )


@router.put("/{subscription_id}/renew", response_model=schemas.Subscription)
async def renew_subscription(
    *,
    db: Session = Depends(deps.get_db),
    subscription_id: int = Path(..., description="ID подписки"),
    current_user: schemas.User = Depends(deps.get_current_user),
) -> Any:
    """
    Продлить подписку.
    """
    subscription = crud.subscription.get(db, id=subscription_id)
    if not subscription:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Подписка не найдена"
        )
    
    # Проверяем права доступа
    if not current_user.is_superuser and subscription.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Недостаточно прав доступа"
        )
    
    # Здесь должна быть логика обработки платежа
    # В данном примере мы просто продлеваем подписку
    payment_data = {
        "method": "telegram",
        "id": "payment_id"  # В реальном приложении здесь будет ID платежа
    }
    
    return await crud.subscription.renew_subscription(
        db, subscription_id=subscription_id, payment_data=payment_data
    ) 