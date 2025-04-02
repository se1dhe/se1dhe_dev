from typing import Any, List, Optional
from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, HTTPException, Path, Query, status
from sqlalchemy.orm import Session

from app import crud, schemas
from app.api import deps
from app.core.cache import cached

router = APIRouter()


@router.get("/", response_model=List[schemas.Bot])
@cached(namespace="bots", expire=60 * 5)  # Кэшируем на 5 минут
async def read_bots(
    db: Session = Depends(deps.get_db),
    skip: int = Query(0, description="Сколько записей пропустить"),
    limit: int = Query(100, description="Максимальное количество записей"),
    category_id: Optional[int] = Query(None, description="ID категории для фильтрации"),
    search: Optional[str] = Query(None, description="Поисковый запрос"),
    sort_by: Optional[str] = Query(None, description="Поле для сортировки"),
    sort_order: Optional[str] = Query("asc", description="Порядок сортировки (asc/desc)"),
) -> Any:
    """
    Получить список ботов с фильтрацией и сортировкой.
    """
    return crud.bot.get_multi(
        db,
        skip=skip,
        limit=limit,
        category_id=category_id,
        search=search,
        sort_by=sort_by,
        sort_order=sort_order
    )


@router.get("/featured", response_model=List[schemas.Bot])
@cached(namespace="bots", expire=60 * 15)  # Кэшируем на 15 минут
async def read_featured_bots(
    db: Session = Depends(deps.get_db),
    limit: int = Query(10, description="Максимальное количество записей"),
) -> Any:
    """
    Получить список рекомендуемых ботов.
    """
    return crud.bot.get_featured(db, limit=limit)


@router.get("/popular", response_model=List[schemas.Bot])
@cached(namespace="bots", expire=60 * 15)  # Кэшируем на 15 минут
async def read_popular_bots(
    db: Session = Depends(deps.get_db),
    limit: int = Query(10, description="Максимальное количество записей"),
) -> Any:
    """
    Получить список популярных ботов.
    """
    return crud.bot.get_popular(db, limit=limit)


@router.get("/my", response_model=List[schemas.Bot])
@cached(namespace="bots", expire=60 * 5, user_specific=True)  # Кэшируем на 5 минут с учетом пользователя
async def read_my_bots(
    db: Session = Depends(deps.get_db),
    current_user: schemas.User = Depends(deps.get_current_user),
    skip: int = Query(0, description="Сколько записей пропустить"),
    limit: int = Query(100, description="Максимальное количество записей"),
) -> Any:
    """
    Получить список своих ботов.
    """
    return crud.bot.get_by_owner(
        db, owner_id=current_user.id, skip=skip, limit=limit
    )


@router.get("/{bot_id}", response_model=schemas.BotWithDetails)
@cached(namespace="bots", expire=60 * 5)  # Кэшируем на 5 минут
async def read_bot(
    *,
    db: Session = Depends(deps.get_db),
    bot_id: int = Path(..., description="ID бота"),
) -> Any:
    """
    Получить информацию о боте по ID.
    """
    bot = crud.bot.get_with_details(db, id=bot_id)
    if not bot:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Бот не найден"
        )
    return bot


@router.post("/", response_model=schemas.Bot)
async def create_bot(
    *,
    db: Session = Depends(deps.get_db),
    bot_in: schemas.BotCreate,
    current_user: schemas.User = Depends(deps.get_current_user),
) -> Any:
    """
    Создать нового бота.
    """
    # Проверяем, что пользователь является разработчиком
    if not current_user.role == "developer":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Только разработчики могут создавать ботов"
        )
    
    # Проверяем, что категория существует
    category = crud.category.get(db, id=bot_in.category_id)
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Указанная категория не найдена"
        )
    
    # Создаем бота
    bot = crud.bot.create_with_owner(
        db=db,
        obj_in=bot_in,
        owner_id=current_user.id
    )
    
    return bot


@router.put("/{bot_id}", response_model=schemas.Bot)
async def update_bot(
    *,
    db: Session = Depends(deps.get_db),
    bot_id: int = Path(..., description="ID бота"),
    bot_in: schemas.BotUpdate,
    current_user: schemas.User = Depends(deps.get_current_user),
) -> Any:
    """
    Обновить бота.
    """
    bot = crud.bot.get(db, id=bot_id)
    if not bot:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Бот не найден"
        )
    
    # Проверяем права доступа
    if not current_user.is_superuser and bot.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Недостаточно прав доступа"
        )
    
    # Если меняется категория, проверяем, что она существует
    if bot_in.category_id is not None:
        category = crud.category.get(db, id=bot_in.category_id)
        if not category:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Указанная категория не найдена"
            )
    
    bot = crud.bot.update(db, db_obj=bot, obj_in=bot_in)
    return bot


@router.delete("/{bot_id}", response_model=schemas.Bot)
async def delete_bot(
    *,
    db: Session = Depends(deps.get_db),
    bot_id: int = Path(..., description="ID бота"),
    current_user: schemas.User = Depends(deps.get_current_user),
) -> Any:
    """
    Удалить бота.
    """
    bot = crud.bot.get(db, id=bot_id)
    if not bot:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Бот не найден"
        )
    
    # Проверяем права доступа
    if not current_user.is_superuser and bot.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Недостаточно прав доступа"
        )
    
    bot = crud.bot.remove(db, id=bot_id)
    return bot


@router.post("/{bot_id}/subscribe", response_model=schemas.Subscription)
def subscribe_to_bot(
    *,
    db: Session = Depends(deps.get_db),
    bot_id: int = Path(..., description="ID бота"),
    subscription_duration: int = Query(30, description="Продолжительность подписки в днях"),
    current_user: schemas.User = Depends(deps.get_current_user),
) -> Any:
    """
    Подписаться на бота.
    """
    bot = crud.bot.get(db, id=bot_id)
    if not bot:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Бот не найден"
        )
    
    expires_at = datetime.utcnow() + timedelta(days=subscription_duration)
    subscription_data = schemas.SubscriptionCreate(
        user_id=current_user.id,
        bot_id=bot_id,
        expires_at=expires_at
    )
    
    return crud.bot.create_subscription(db, obj_in=subscription_data)


@router.put("/{bot_id}/subscription", response_model=schemas.Subscription)
def update_subscription(
    *,
    db: Session = Depends(deps.get_db),
    bot_id: int = Path(..., description="ID бота"),
    subscription_duration: int = Query(30, description="Продолжительность подписки в днях"),
    current_user: schemas.User = Depends(deps.get_current_user),
) -> Any:
    """
    Обновить подписку на бота.
    """
    bot = crud.bot.get(db, id=bot_id)
    if not bot:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Бот не найден"
        )
    
    expires_at = datetime.utcnow() + timedelta(days=subscription_duration)
    subscription_update = schemas.SubscriptionUpdate(expires_at=expires_at)
    
    result = crud.bot.update_subscription(
        db, user_id=current_user.id, bot_id=bot_id, obj_in=subscription_update
    )
    
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Подписка не найдена"
        )
    
    # Преобразуем словарь в схему Subscription
    return schemas.Subscription(
        user_id=result["user_id"],
        bot_id=result["bot_id"],
        created_at=result["created_at"],
        expires_at=result["expires_at"]
    )


@router.delete("/{bot_id}/subscription", status_code=status.HTTP_204_NO_CONTENT)
def cancel_subscription(
    *,
    db: Session = Depends(deps.get_db),
    bot_id: int = Path(..., description="ID бота"),
    current_user: schemas.User = Depends(deps.get_current_user),
) -> None:
    """
    Отменить подписку на бота.
    """
    bot = crud.bot.get(db, id=bot_id)
    if not bot:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Бот не найден"
        )
    
    result = crud.bot.remove_subscription(db, user_id=current_user.id, bot_id=bot_id)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Подписка не найдена"
        ) 