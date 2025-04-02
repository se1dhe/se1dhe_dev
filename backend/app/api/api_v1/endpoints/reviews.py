from typing import Any, List, Optional

from fastapi import APIRouter, Depends, HTTPException, Path, Query, status
from sqlalchemy.orm import Session

from app import crud, schemas
from app.api import deps

router = APIRouter()


@router.get("/", response_model=List[schemas.Review])
async def read_reviews(
    db: Session = Depends(deps.get_db),
    skip: int = Query(0, description="Сколько записей пропустить"),
    limit: int = Query(100, description="Максимальное количество записей"),
    current_user: schemas.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Получить список всех отзывов.
    Только для администраторов.
    """
    return crud.review.get_multi(db, skip=skip, limit=limit)


@router.get("/my", response_model=List[schemas.Review])
async def read_my_reviews(
    db: Session = Depends(deps.get_db),
    skip: int = Query(0, description="Сколько записей пропустить"),
    limit: int = Query(100, description="Максимальное количество записей"),
    current_user: schemas.User = Depends(deps.get_current_user),
) -> Any:
    """
    Получить список своих отзывов.
    """
    return crud.review.get_by_user(db, user_id=current_user.id, skip=skip, limit=limit)


@router.get("/bot/{bot_id}", response_model=List[schemas.Review])
async def read_bot_reviews(
    *,
    db: Session = Depends(deps.get_db),
    bot_id: int = Path(..., description="ID бота"),
    verified_only: bool = Query(False, description="Только подтвержденные покупки"),
    skip: int = Query(0, description="Сколько записей пропустить"),
    limit: int = Query(100, description="Максимальное количество записей"),
) -> Any:
    """
    Получить список отзывов для конкретного бота.
    """
    # Проверяем, что бот существует
    bot = crud.bot.get(db, id=bot_id)
    if not bot:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Указанный бот не найден"
        )
    
    return crud.review.get_by_bot(
        db, bot_id=bot_id, verified_only=verified_only, skip=skip, limit=limit
    )


@router.get("/bot/{bot_id}/stats", response_model=schemas.ReviewStats)
async def read_bot_review_stats(
    *,
    db: Session = Depends(deps.get_db),
    bot_id: int = Path(..., description="ID бота"),
) -> Any:
    """
    Получить статистику отзывов для конкретного бота.
    """
    # Проверяем, что бот существует
    bot = crud.bot.get(db, id=bot_id)
    if not bot:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Указанный бот не найден"
        )
    
    return crud.review.get_bot_stats(db, bot_id=bot_id)


@router.get("/details", response_model=List[schemas.ReviewWithDetails])
async def read_reviews_with_details(
    db: Session = Depends(deps.get_db),
    skip: int = Query(0, description="Сколько записей пропустить"),
    limit: int = Query(100, description="Максимальное количество записей"),
    current_user: schemas.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Получить список отзывов с детальной информацией.
    Только для администраторов.
    """
    return crud.review.get_multi_with_details(db, skip=skip, limit=limit)


@router.get("/{review_id}", response_model=schemas.ReviewWithDetails)
async def read_review(
    *,
    db: Session = Depends(deps.get_db),
    review_id: int = Path(..., description="ID отзыва"),
) -> Any:
    """
    Получить информацию об отзыве по ID.
    """
    review = crud.review.get_with_details(db, id=review_id)
    if not review:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Отзыв не найден"
        )
    
    return review


@router.post("/bot/{bot_id}", response_model=schemas.Review)
async def create_or_update_review(
    *,
    db: Session = Depends(deps.get_db),
    bot_id: int = Path(..., description="ID бота"),
    review_in: schemas.ReviewCreate,
    current_user: schemas.User = Depends(deps.get_current_user),
) -> Any:
    """
    Создать новый отзыв о боте или обновить существующий.
    """
    # Проверяем, что бот существует
    bot = crud.bot.get(db, id=bot_id)
    if not bot:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Указанный бот не найден"
        )
    
    # Проверяем, есть ли у пользователя уже отзыв на этого бота
    existing_review = crud.review.get_user_review_for_bot(
        db, user_id=current_user.id, bot_id=bot_id
    )
    
    if existing_review:
        # Обновляем существующий отзыв
        update_data = {
            "rating": review_in.rating,
            "title": review_in.title,
            "content": review_in.content,
        }
        return await crud.review.update_user_review(
            db, user_id=current_user.id, bot_id=bot_id, obj_in=schemas.ReviewUpdate(**update_data)
        )
    else:
        # Создаем новый отзыв
        # Принудительно устанавливаем user_id и bot_id
        review_data = review_in.dict()
        review_data["user_id"] = current_user.id
        review_data["bot_id"] = bot_id
        
        return await crud.review.create_with_verification(
            db, 
            obj_in=schemas.ReviewCreate(**review_data),
            user_id=current_user.id,
            bot_id=bot_id
        )


@router.put("/{review_id}", response_model=schemas.Review)
async def update_review(
    *,
    db: Session = Depends(deps.get_db),
    review_id: int = Path(..., description="ID отзыва"),
    review_in: schemas.ReviewUpdate,
    current_user: schemas.User = Depends(deps.get_current_user),
) -> Any:
    """
    Обновить отзыв.
    Пользователи могут обновлять только свои отзывы.
    """
    review = crud.review.get(db, id=review_id)
    if not review:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Отзыв не найден"
        )
    
    # Проверяем права доступа
    if not current_user.is_superuser and review.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Недостаточно прав доступа"
        )
    
    return await crud.review.update_user_review(
        db, user_id=current_user.id, bot_id=review.bot_id, obj_in=review_in
    )


@router.delete("/{review_id}", response_model=schemas.Review)
async def delete_review(
    *,
    db: Session = Depends(deps.get_db),
    review_id: int = Path(..., description="ID отзыва"),
    current_user: schemas.User = Depends(deps.get_current_user),
) -> Any:
    """
    Удалить отзыв.
    Пользователи могут удалять только свои отзывы.
    """
    review = crud.review.get(db, id=review_id)
    if not review:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Отзыв не найден"
        )
    
    # Проверяем права доступа
    if not current_user.is_superuser and review.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Недостаточно прав доступа"
        )
    
    return crud.review.remove(db, id=review_id) 