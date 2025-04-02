from typing import Any, List, Optional

from fastapi import APIRouter, Body, Depends, HTTPException, Path, Query, status
from sqlalchemy.orm import Session

from app import crud, schemas
from app.api import deps
from app.models.feature_request import FeatureRequestStatus as DBFeatureRequestStatus

router = APIRouter()


@router.get("/", response_model=List[schemas.FeatureRequest])
def read_feature_requests(
    db: Session = Depends(deps.get_db),
    skip: int = Query(0, description="Сколько записей пропустить"),
    limit: int = Query(100, description="Максимальное количество записей"),
    status: Optional[schemas.FeatureRequestStatus] = Query(None, description="Статус запроса для фильтрации"),
    priority: Optional[schemas.FeaturePriority] = Query(None, description="Приоритет для фильтрации"),
    current_user: schemas.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Получить список всех запросов на новые функции.
    Только для администраторов.
    """
    if status:
        return crud.feature_request.get_by_status(db, status=status, skip=skip, limit=limit)
    elif priority:
        return crud.feature_request.get_by_priority(db, priority=priority, skip=skip, limit=limit)
    else:
        return crud.feature_request.get_multi(db, skip=skip, limit=limit)


@router.get("/my", response_model=List[schemas.FeatureRequest])
def read_my_feature_requests(
    db: Session = Depends(deps.get_db),
    skip: int = Query(0, description="Сколько записей пропустить"),
    limit: int = Query(100, description="Максимальное количество записей"),
    current_user: schemas.User = Depends(deps.get_current_user),
) -> Any:
    """
    Получить список своих запросов на новые функции.
    """
    return crud.feature_request.get_by_user(db, user_id=current_user.id, skip=skip, limit=limit)


@router.get("/bot/{bot_id}", response_model=List[schemas.FeatureRequest])
def read_bot_feature_requests(
    *,
    db: Session = Depends(deps.get_db),
    bot_id: int = Path(..., description="ID бота"),
    skip: int = Query(0, description="Сколько записей пропустить"),
    limit: int = Query(100, description="Максимальное количество записей"),
    public_only: bool = Query(False, description="Показывать только публичные запросы"),
    current_user: schemas.User = Depends(deps.get_current_user),
) -> Any:
    """
    Получить список запросов на новые функции для конкретного бота.
    """
    # Проверяем, что бот существует
    bot = crud.bot.get(db, id=bot_id)
    if not bot:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Указанный бот не найден"
        )
    
    # Проверяем, что пользователь имеет подписку на этот бот (клиент бота)
    if not current_user.is_superuser:
        subscription = crud.bot.get_user_subscription(db, user_id=current_user.id, bot_id=bot_id)
        if not subscription:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Доступ запрещен. Вы должны быть клиентом этого бота."
            )
    
    return crud.feature_request.get_by_bot(
        db, bot_id=bot_id, skip=skip, limit=limit, 
        is_public_only=(public_only and not current_user.is_superuser)
    )


@router.get("/top", response_model=List[schemas.FeatureRequest])
def read_top_feature_requests(
    db: Session = Depends(deps.get_db),
    bot_id: Optional[int] = Query(None, description="ID бота (опционально)"),
    limit: int = Query(10, description="Количество записей"),
    current_user: schemas.User = Depends(deps.get_current_user),
) -> Any:
    """
    Получить топ самых популярных запросов на новые функции по голосам.
    """
    # Если указан бот, проверяем, что пользователь подписан на него
    if bot_id and not current_user.is_superuser:
        subscription = crud.bot.get_user_subscription(db, user_id=current_user.id, bot_id=bot_id)
        if not subscription:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Доступ запрещен. Вы должны быть клиентом этого бота."
            )
    
    return crud.feature_request.get_top_voted(db, bot_id=bot_id, limit=limit)


@router.post("/", response_model=schemas.FeatureRequest)
def create_feature_request(
    *,
    db: Session = Depends(deps.get_db),
    feature_request_in: schemas.FeatureRequestCreate,
    current_user: schemas.User = Depends(deps.get_current_user),
) -> Any:
    """
    Создать новый запрос на функцию.
    """
    # Проверяем, что бот существует
    bot = crud.bot.get(db, id=feature_request_in.bot_id)
    if not bot:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Указанный бот не найден"
        )
    
    # Проверяем, что пользователь имеет подписку на этот бот (клиент бота)
    if not current_user.is_superuser:
        subscription = crud.bot.get_user_subscription(db, user_id=current_user.id, bot_id=feature_request_in.bot_id)
        if not subscription:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Доступ запрещен. Вы должны быть клиентом этого бота."
            )
    
    # Принудительно устанавливаем user_id текущего пользователя
    feature_request_data = feature_request_in.dict()
    feature_request_data["user_id"] = current_user.id
    
    return crud.feature_request.create(db, obj_in=schemas.FeatureRequestCreate(**feature_request_data))


@router.get("/details", response_model=List[schemas.FeatureRequestWithDetails])
def read_feature_requests_with_details(
    db: Session = Depends(deps.get_db),
    skip: int = Query(0, description="Сколько записей пропустить"),
    limit: int = Query(100, description="Максимальное количество записей"),
    current_user: schemas.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Получить список запросов на новые функции с детальной информацией.
    Только для администраторов.
    """
    return crud.feature_request.get_multi_with_details(db, skip=skip, limit=limit)


@router.get("/{feature_request_id}", response_model=schemas.FeatureRequestWithDetails)
def read_feature_request(
    *,
    db: Session = Depends(deps.get_db),
    feature_request_id: int = Path(..., description="ID запроса на функцию"),
    current_user: schemas.User = Depends(deps.get_current_user),
) -> Any:
    """
    Получить информацию о запросе на функцию по ID.
    """
    feature_request = crud.feature_request.get_with_details(db, id=feature_request_id)
    if not feature_request:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Запрос на функцию не найден"
        )
    
    # Проверяем права доступа
    if not current_user.is_superuser:
        # Если запрос не публичный и пользователь не автор
        if not feature_request.is_public and feature_request.user_id != current_user.id:
            # Проверяем, является ли пользователь клиентом бота
            subscription = crud.bot.get_user_subscription(
                db, user_id=current_user.id, bot_id=feature_request.bot_id
            )
            if not subscription:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Доступ запрещен"
                )
    
    return feature_request


@router.put("/{feature_request_id}", response_model=schemas.FeatureRequest)
def update_feature_request(
    *,
    db: Session = Depends(deps.get_db),
    feature_request_id: int = Path(..., description="ID запроса на функцию"),
    feature_request_in: schemas.FeatureRequestUpdate,
    current_user: schemas.User = Depends(deps.get_current_user),
) -> Any:
    """
    Обновить запрос на функцию.
    Админы могут менять все поля, обычные пользователи - только свои запросы и ограниченный набор полей.
    """
    feature_request = crud.feature_request.get(db, id=feature_request_id)
    if not feature_request:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Запрос на функцию не найден"
        )
    
    # Обычные пользователи могут обновлять только свои запросы
    if not current_user.is_superuser and feature_request.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Недостаточно прав доступа"
        )
    
    # Обычные пользователи не могут менять статус, приоритет и bot_id
    if not current_user.is_superuser and (
        feature_request_in.status or 
        feature_request_in.priority or 
        feature_request_in.bot_id
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Недостаточно прав для изменения статуса, приоритета или бота"
        )
    
    return crud.feature_request.update(db, db_obj=feature_request, obj_in=feature_request_in)


@router.put("/{feature_request_id}/status", response_model=schemas.FeatureRequest)
def update_feature_status(
    *,
    db: Session = Depends(deps.get_db),
    feature_request_id: int = Path(..., description="ID запроса на функцию"),
    status: schemas.FeatureRequestStatus = Body(..., description="Новый статус запроса"),
    current_user: schemas.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Обновить статус запроса на функцию.
    Только для администраторов.
    """
    feature_request = crud.feature_request.get(db, id=feature_request_id)
    if not feature_request:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Запрос на функцию не найден"
        )
    
    return crud.feature_request.update_status(db, db_obj=feature_request, status=status)


@router.put("/{feature_request_id}/priority", response_model=schemas.FeatureRequest)
def update_feature_priority(
    *,
    db: Session = Depends(deps.get_db),
    feature_request_id: int = Path(..., description="ID запроса на функцию"),
    priority: schemas.FeaturePriority = Body(..., description="Новый приоритет запроса"),
    current_user: schemas.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Обновить приоритет запроса на функцию.
    Только для администраторов.
    """
    feature_request = crud.feature_request.get(db, id=feature_request_id)
    if not feature_request:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Запрос на функцию не найден"
        )
    
    return crud.feature_request.update_priority(db, db_obj=feature_request, priority=priority)


# Эндпоинты для голосования
@router.post("/{feature_request_id}/vote", response_model=schemas.FeatureRequest)
def vote_for_feature(
    *,
    db: Session = Depends(deps.get_db),
    feature_request_id: int = Path(..., description="ID запроса на функцию"),
    current_user: schemas.User = Depends(deps.get_current_user),
) -> Any:
    """
    Проголосовать за запрос на функцию.
    """
    feature_request = crud.feature_request.get(db, id=feature_request_id)
    if not feature_request:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Запрос на функцию не найден"
        )
    
    # Проверяем, что пользователь имеет подписку на этот бот (клиент бота)
    if not current_user.is_superuser:
        subscription = crud.bot.get_user_subscription(db, user_id=current_user.id, bot_id=feature_request.bot_id)
        if not subscription:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Доступ запрещен. Вы должны быть клиентом этого бота."
            )
    
    # Проверяем, голосовал ли уже пользователь
    existing_vote = crud.feature_vote.get_by_user_and_feature(
        db, user_id=current_user.id, feature_id=feature_request_id
    )
    
    if existing_vote:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Вы уже проголосовали за этот запрос"
        )
    
    # Создаем голос
    vote = crud.feature_vote.create_if_not_exists(
        db, user_id=current_user.id, feature_id=feature_request_id
    )
    
    if vote:
        # Увеличиваем счетчик голосов у запроса
        feature_request = crud.feature_request.increment_votes(db, db_obj=feature_request)
    
    return feature_request


@router.delete("/{feature_request_id}/vote", response_model=schemas.FeatureRequest)
def remove_vote_from_feature(
    *,
    db: Session = Depends(deps.get_db),
    feature_request_id: int = Path(..., description="ID запроса на функцию"),
    current_user: schemas.User = Depends(deps.get_current_user),
) -> Any:
    """
    Удалить свой голос за запрос на функцию.
    """
    feature_request = crud.feature_request.get(db, id=feature_request_id)
    if not feature_request:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Запрос на функцию не найден"
        )
    
    # Проверяем, голосовал ли пользователь
    existing_vote = crud.feature_vote.get_by_user_and_feature(
        db, user_id=current_user.id, feature_id=feature_request_id
    )
    
    if not existing_vote:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Вы не голосовали за этот запрос"
        )
    
    # Удаляем голос
    crud.feature_vote.remove(db, id=existing_vote.id)
    
    # Уменьшаем счетчик голосов у запроса
    feature_request = crud.feature_request.decrement_votes(db, db_obj=feature_request)
    
    return feature_request


# Эндпоинты для комментариев
@router.get("/{feature_request_id}/comments", response_model=List[schemas.FeatureCommentWithUser])
def read_feature_comments(
    *,
    db: Session = Depends(deps.get_db),
    feature_request_id: int = Path(..., description="ID запроса на функцию"),
    skip: int = Query(0, description="Сколько записей пропустить"),
    limit: int = Query(100, description="Максимальное количество записей"),
    current_user: schemas.User = Depends(deps.get_current_user),
) -> Any:
    """
    Получить комментарии к запросу на функцию.
    """
    feature_request = crud.feature_request.get(db, id=feature_request_id)
    if not feature_request:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Запрос на функцию не найден"
        )
    
    # Проверяем права доступа
    if not current_user.is_superuser and feature_request.user_id != current_user.id:
        # Если запрос не публичный, проверяем подписку на бота
        if not feature_request.is_public:
            subscription = crud.bot.get_user_subscription(
                db, user_id=current_user.id, bot_id=feature_request.bot_id
            )
            if not subscription:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Доступ запрещен"
                )
    
    return crud.feature_comment.get_by_feature_with_users(
        db, feature_id=feature_request_id, skip=skip, limit=limit
    )


@router.post("/{feature_request_id}/comments", response_model=schemas.FeatureComment)
def create_feature_comment(
    *,
    db: Session = Depends(deps.get_db),
    feature_request_id: int = Path(..., description="ID запроса на функцию"),
    comment_in: schemas.FeatureCommentCreate,
    current_user: schemas.User = Depends(deps.get_current_user),
) -> Any:
    """
    Добавить комментарий к запросу на функцию.
    """
    feature_request = crud.feature_request.get(db, id=feature_request_id)
    if not feature_request:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Запрос на функцию не найден"
        )
    
    # Проверяем права доступа (аналогично как при просмотре комментариев)
    if not current_user.is_superuser and feature_request.user_id != current_user.id:
        if not feature_request.is_public:
            subscription = crud.bot.get_user_subscription(
                db, user_id=current_user.id, bot_id=feature_request.bot_id
            )
            if not subscription:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Доступ запрещен"
                )
    
    # Принудительно устанавливаем user_id и feature_id
    comment_data = {
        "user_id": current_user.id,
        "feature_id": feature_request_id,
        "text": comment_in.text
    }
    
    return crud.feature_comment.create(db, obj_in=schemas.FeatureCommentCreate(**comment_data))


@router.put("/{feature_request_id}/comments/{comment_id}", response_model=schemas.FeatureComment)
def update_feature_comment(
    *,
    db: Session = Depends(deps.get_db),
    feature_request_id: int = Path(..., description="ID запроса на функцию"),
    comment_id: int = Path(..., description="ID комментария"),
    comment_in: schemas.FeatureCommentUpdate,
    current_user: schemas.User = Depends(deps.get_current_user),
) -> Any:
    """
    Обновить комментарий к запросу на функцию.
    """
    comment = crud.feature_comment.get(db, id=comment_id)
    if not comment or comment.feature_id != feature_request_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Комментарий не найден"
        )
    
    # Только автор комментария или админ может его обновить
    if not current_user.is_superuser and comment.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Недостаточно прав для редактирования комментария"
        )
    
    return crud.feature_comment.update(db, db_obj=comment, obj_in=comment_in)


@router.delete("/{feature_request_id}/comments/{comment_id}", response_model=schemas.FeatureComment)
def delete_feature_comment(
    *,
    db: Session = Depends(deps.get_db),
    feature_request_id: int = Path(..., description="ID запроса на функцию"),
    comment_id: int = Path(..., description="ID комментария"),
    current_user: schemas.User = Depends(deps.get_current_user),
) -> Any:
    """
    Удалить комментарий к запросу на функцию.
    """
    comment = crud.feature_comment.get(db, id=comment_id)
    if not comment or comment.feature_id != feature_request_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Комментарий не найден"
        )
    
    # Только автор комментария или админ может его удалить
    if not current_user.is_superuser and comment.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Недостаточно прав для удаления комментария"
        )
    
    return crud.feature_comment.remove(db, id=comment_id) 