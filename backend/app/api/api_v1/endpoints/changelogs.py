from typing import Any, List, Optional

from fastapi import APIRouter, Depends, HTTPException, Path, Query, status
from sqlalchemy.orm import Session

from app import crud, schemas
from app.api import deps

router = APIRouter()


@router.get("/", response_model=List[schemas.Changelog])
def read_changelogs(
    db: Session = Depends(deps.get_db),
    skip: int = Query(0, description="Сколько записей пропустить"),
    limit: int = Query(100, description="Максимальное количество записей"),
    bot_id: Optional[int] = Query(None, description="ID бота для фильтрации")
) -> Any:
    """
    Получить список версий обновлений.
    """
    if bot_id:
        return crud.changelog.get_by_bot(db, bot_id=bot_id, skip=skip, limit=limit)
    else:
        return crud.changelog.get_multi(db, skip=skip, limit=limit)


@router.get("/latest", response_model=List[schemas.Changelog])
def read_latest_changelogs(
    db: Session = Depends(deps.get_db),
    limit: int = Query(10, description="Максимальное количество записей")
) -> Any:
    """
    Получить список последних версий обновлений.
    """
    return crud.changelog.get_latest(db, limit=limit)


@router.get("/{changelog_id}", response_model=schemas.ChangelogWithBot)
def read_changelog(
    *,
    db: Session = Depends(deps.get_db),
    changelog_id: int = Path(..., description="ID версии обновления")
) -> Any:
    """
    Получить информацию о версии обновления по ID.
    """
    changelog = crud.changelog.get_with_bot(db, id=changelog_id)
    if not changelog:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Версия обновления не найдена"
        )
    return changelog


@router.post("/", response_model=schemas.Changelog)
def create_changelog(
    *,
    db: Session = Depends(deps.get_db),
    changelog_in: schemas.ChangelogCreate,
    current_user: schemas.User = Depends(deps.get_current_active_superuser)
) -> Any:
    """
    Создать новую версию обновления.
    Только для администраторов.
    """
    # Проверяем, что бот существует
    bot = crud.bot.get(db, id=changelog_in.bot_id)
    if not bot:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Указанный бот не найден"
        )
    
    return crud.changelog.create(db, obj_in=changelog_in)


@router.put("/{changelog_id}", response_model=schemas.Changelog)
def update_changelog(
    *,
    db: Session = Depends(deps.get_db),
    changelog_id: int = Path(..., description="ID версии обновления"),
    changelog_in: schemas.ChangelogUpdate,
    current_user: schemas.User = Depends(deps.get_current_active_superuser)
) -> Any:
    """
    Обновить информацию о версии обновления.
    Только для администраторов.
    """
    changelog = crud.changelog.get(db, id=changelog_id)
    if not changelog:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Версия обновления не найдена"
        )
    
    if changelog_in.bot_id:
        # Проверяем, что новый бот существует
        bot = crud.bot.get(db, id=changelog_in.bot_id)
        if not bot:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Указанный бот не найден"
            )
    
    return crud.changelog.update(db, db_obj=changelog, obj_in=changelog_in)


@router.delete("/{changelog_id}", response_model=schemas.Changelog)
def delete_changelog(
    *,
    db: Session = Depends(deps.get_db),
    changelog_id: int = Path(..., description="ID версии обновления"),
    current_user: schemas.User = Depends(deps.get_current_active_superuser)
) -> Any:
    """
    Удалить версию обновления.
    Только для администраторов.
    """
    changelog = crud.changelog.get(db, id=changelog_id)
    if not changelog:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Версия обновления не найдена"
        )
    
    return crud.changelog.remove(db, id=changelog_id) 