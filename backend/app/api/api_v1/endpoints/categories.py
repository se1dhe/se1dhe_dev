from typing import Any, Dict, List, Optional

from fastapi import APIRouter, Depends, HTTPException, Path, Query, status
from sqlalchemy.orm import Session

from app import crud, schemas
from app.api import deps

router = APIRouter()


@router.get("/", response_model=List[schemas.Category])
def read_categories(
    db: Session = Depends(deps.get_db),
    skip: int = Query(0, description="Сколько записей пропустить"),
    limit: int = Query(100, description="Максимальное количество записей"),
) -> Any:
    """
    Получить список всех категорий ботов.
    """
    return crud.category.get_multi(db, skip=skip, limit=limit)


@router.get("/with-bots-count", response_model=List[Dict[str, Any]])
def read_categories_with_bots_count(
    db: Session = Depends(deps.get_db),
    skip: int = Query(0, description="Сколько записей пропустить"),
    limit: int = Query(100, description="Максимальное количество записей"),
) -> Any:
    """
    Получить список категорий с количеством ботов в каждой.
    """
    return crud.category.get_with_bots_count(db, skip=skip, limit=limit)


@router.get("/{category_id}", response_model=schemas.Category)
def read_category(
    *,
    db: Session = Depends(deps.get_db),
    category_id: int = Path(..., description="ID категории"),
) -> Any:
    """
    Получить категорию по ID.
    """
    category = crud.category.get(db, id=category_id)
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Категория не найдена"
        )
    return category


@router.get("/slug/{slug}", response_model=schemas.Category)
def read_category_by_slug(
    *,
    db: Session = Depends(deps.get_db),
    slug: str = Path(..., description="Slug категории"),
) -> Any:
    """
    Получить категорию по slug.
    """
    category = crud.category.get_by_slug(db, slug=slug)
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Категория не найдена"
        )
    return category


@router.post("/", response_model=schemas.Category)
def create_category(
    *,
    db: Session = Depends(deps.get_db),
    category_in: schemas.CategoryCreate,
    current_user: schemas.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Создать новую категорию.
    Только для администраторов.
    """
    existing = crud.category.get_by_slug(db, slug=category_in.slug)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Категория с таким slug уже существует"
        )
    return crud.category.create(db, obj_in=category_in)


@router.put("/{category_id}", response_model=schemas.Category)
def update_category(
    *,
    db: Session = Depends(deps.get_db),
    category_id: int = Path(..., description="ID категории"),
    category_in: schemas.CategoryUpdate,
    current_user: schemas.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Обновить категорию.
    Только для администраторов.
    """
    category = crud.category.get(db, id=category_id)
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Категория не найдена"
        )
        
    if category_in.slug:
        existing = crud.category.get_by_slug(db, slug=category_in.slug)
        if existing and existing.id != category_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Категория с таким slug уже существует"
            )
    
    return crud.category.update(db, db_obj=category, obj_in=category_in)


@router.delete("/{category_id}", response_model=schemas.Category)
def delete_category(
    *,
    db: Session = Depends(deps.get_db),
    category_id: int = Path(..., description="ID категории"),
    current_user: schemas.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Удалить категорию.
    Только для администраторов.
    """
    category = crud.category.get(db, id=category_id)
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Категория не найдена"
        )
    return crud.category.remove(db, id=category_id) 