from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from .. import crud, schemas
from ..database import get_db

router = APIRouter(
    prefix="/bug-reports",
    tags=["bug_reports"],
    responses={404: {"description": "Not found"}},
)

@router.post("/", response_model=schemas.BugReport)
def create_bug_report(bug_report: schemas.BugReportCreate, db: Session = Depends(get_db)):
    # Проверяем существование пользователя
    db_user = crud.get_user(db, user_id=bug_report.user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Проверяем существование бота
    db_bot = crud.get_bot(db, bot_id=bug_report.bot_id)
    if db_bot is None:
        raise HTTPException(status_code=404, detail="Bot not found")
    
    return crud.create_bug_report(db=db, bug_report=bug_report)

@router.get("/", response_model=List[schemas.BugReport])
def read_bug_reports(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    bug_reports = crud.get_bug_reports(db, skip=skip, limit=limit)
    return bug_reports

@router.get("/{bug_report_id}", response_model=schemas.BugReport)
def read_bug_report(bug_report_id: int, db: Session = Depends(get_db)):
    db_bug_report = crud.get_bug_report(db, bug_report_id=bug_report_id)
    if db_bug_report is None:
        raise HTTPException(status_code=404, detail="Bug report not found")
    return db_bug_report

@router.put("/{bug_report_id}", response_model=schemas.BugReport)
def update_bug_report(bug_report_id: int, bug_report: schemas.BugReportUpdate, db: Session = Depends(get_db)):
    db_bug_report = crud.update_bug_report(db, bug_report_id=bug_report_id, bug_report=bug_report)
    if db_bug_report is None:
        raise HTTPException(status_code=404, detail="Bug report not found")
    return db_bug_report 