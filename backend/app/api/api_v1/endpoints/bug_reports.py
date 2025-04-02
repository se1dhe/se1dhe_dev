from typing import Any, List, Optional

from fastapi import APIRouter, Body, Depends, HTTPException, Path, Query, status
from sqlalchemy.orm import Session

from app import crud, schemas
from app.api import deps

router = APIRouter()


@router.get("/", response_model=List[schemas.BugReport])
def read_bug_reports(
    db: Session = Depends(deps.get_db),
    skip: int = Query(0, description="Сколько записей пропустить"),
    limit: int = Query(100, description="Максимальное количество записей"),
    bug_status: Optional[schemas.BugReportStatus] = Query(None, description="Статус отчета для фильтрации"),
    priority: Optional[schemas.BugReportPriority] = Query(None, description="Приоритет для фильтрации"),
    current_user: schemas.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Получить список всех отчетов об ошибках.
    Только для администраторов.
    """
    if bug_status:
        return crud.bug_report.get_by_status(db, status=bug_status, skip=skip, limit=limit)
    elif priority:
        return crud.bug_report.get_by_priority(db, priority=priority, skip=skip, limit=limit)
    else:
        return crud.bug_report.get_multi(db, skip=skip, limit=limit)


@router.get("/my", response_model=List[schemas.BugReport])
def read_my_bug_reports(
    db: Session = Depends(deps.get_db),
    skip: int = Query(0, description="Сколько записей пропустить"),
    limit: int = Query(100, description="Максимальное количество записей"),
    current_user: schemas.User = Depends(deps.get_current_user),
) -> Any:
    """
    Получить список своих отчетов об ошибках.
    """
    return crud.bug_report.get_by_user(db, user_id=current_user.id, skip=skip, limit=limit)


@router.get("/bot/{bot_id}", response_model=List[schemas.BugReport])
def read_bot_bug_reports(
    *,
    db: Session = Depends(deps.get_db),
    bot_id: int = Path(..., description="ID бота"),
    skip: int = Query(0, description="Сколько записей пропустить"),
    limit: int = Query(100, description="Максимальное количество записей"),
    current_user: schemas.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Получить список отчетов об ошибках для конкретного бота.
    Только для администраторов.
    """
    # Проверяем, что бот существует
    bot = crud.bot.get(db, id=bot_id)
    if not bot:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Указанный бот не найден"
        )
    
    return crud.bug_report.get_by_bot(db, bot_id=bot_id, skip=skip, limit=limit)


@router.post("/", response_model=schemas.BugReport)
def create_bug_report(
    *,
    db: Session = Depends(deps.get_db),
    bug_report_in: schemas.BugReportCreate,
    current_user: schemas.User = Depends(deps.get_current_user),
) -> Any:
    """
    Создать новый отчет об ошибке.
    """
    # Проверяем, что бот существует
    bot = crud.bot.get(db, id=bug_report_in.bot_id)
    if not bot:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Указанный бот не найден"
        )
    
    # Принудительно устанавливаем user_id текущего пользователя
    bug_report_data = bug_report_in.dict()
    bug_report_data["user_id"] = current_user.id
    
    return crud.bug_report.create(db, obj_in=schemas.BugReportCreate(**bug_report_data))


@router.get("/details", response_model=List[schemas.BugReportWithDetails])
def read_bug_reports_with_details(
    db: Session = Depends(deps.get_db),
    skip: int = Query(0, description="Сколько записей пропустить"),
    limit: int = Query(100, description="Максимальное количество записей"),
    current_user: schemas.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Получить список отчетов об ошибках с детальной информацией.
    Только для администраторов.
    """
    return crud.bug_report.get_multi_with_details(db, skip=skip, limit=limit)


@router.get("/{bug_report_id}", response_model=schemas.BugReportWithDetails)
def read_bug_report(
    *,
    db: Session = Depends(deps.get_db),
    bug_report_id: int = Path(..., description="ID отчета об ошибке"),
    current_user: schemas.User = Depends(deps.get_current_user),
) -> Any:
    """
    Получить информацию об отчете об ошибке по ID.
    """
    bug_report = crud.bug_report.get_with_details(db, id=bug_report_id)
    if not bug_report:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Отчет об ошибке не найден"
        )
    
    # Обычные пользователи могут просматривать только свои отчеты
    if not current_user.is_superuser and bug_report.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Недостаточно прав доступа"
        )
    
    return bug_report


@router.put("/{bug_report_id}", response_model=schemas.BugReport)
def update_bug_report(
    *,
    db: Session = Depends(deps.get_db),
    bug_report_id: int = Path(..., description="ID отчета об ошибке"),
    bug_report_in: schemas.BugReportUpdate,
    current_user: schemas.User = Depends(deps.get_current_user),
) -> Any:
    """
    Обновить отчет об ошибке.
    Админы могут менять все поля, обычные пользователи - только свои отчеты и ограниченный набор полей.
    """
    bug_report = crud.bug_report.get(db, id=bug_report_id)
    if not bug_report:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Отчет об ошибке не найден"
        )
    
    # Обычные пользователи могут обновлять только свои отчеты
    if not current_user.is_superuser and bug_report.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Недостаточно прав доступа"
        )
    
    # Обычные пользователи не могут менять статус и приоритет
    if not current_user.is_superuser and (bug_report_in.status or bug_report_in.priority):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Недостаточно прав для изменения статуса или приоритета"
        )
    
    return crud.bug_report.update(db, db_obj=bug_report, obj_in=bug_report_in)


@router.put("/{bug_report_id}/status", response_model=schemas.BugReport)
def update_bug_status(
    *,
    db: Session = Depends(deps.get_db),
    bug_report_id: int = Path(..., description="ID отчета об ошибке"),
    status: schemas.BugReportStatus = Body(..., description="Новый статус отчета"),
    current_user: schemas.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Обновить статус отчета об ошибке.
    Только для администраторов.
    """
    bug_report = crud.bug_report.get(db, id=bug_report_id)
    if not bug_report:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Отчет об ошибке не найден"
        )
    
    return crud.bug_report.update_status(db, db_obj=bug_report, status=status)


@router.put("/{bug_report_id}/priority", response_model=schemas.BugReport)
def update_bug_priority(
    *,
    db: Session = Depends(deps.get_db),
    bug_report_id: int = Path(..., description="ID отчета об ошибке"),
    priority: schemas.BugReportPriority = Body(..., description="Новый приоритет отчета"),
    current_user: schemas.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Обновить приоритет отчета об ошибке.
    Только для администраторов.
    """
    bug_report = crud.bug_report.get(db, id=bug_report_id)
    if not bug_report:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Отчет об ошибке не найден"
        )
    
    return crud.bug_report.update_priority(db, db_obj=bug_report, priority=priority) 