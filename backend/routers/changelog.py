from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from .. import crud, schemas
from ..database import get_db

router = APIRouter(
    prefix="/changelog",
    tags=["changelog"],
    responses={404: {"description": "Not found"}},
)

@router.post("/", response_model=schemas.Changelog)
def create_changelog(changelog: schemas.ChangelogCreate, db: Session = Depends(get_db)):
    # Проверяем существование бота
    db_bot = crud.get_bot(db, bot_id=changelog.bot_id)
    if db_bot is None:
        raise HTTPException(status_code=404, detail="Bot not found")
    
    return crud.create_changelog(db=db, changelog=changelog)

@router.get("/", response_model=List[schemas.Changelog])
def read_changelogs(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    changelogs = crud.get_changelogs(db, skip=skip, limit=limit)
    return changelogs

@router.get("/{changelog_id}", response_model=schemas.Changelog)
def read_changelog(changelog_id: int, db: Session = Depends(get_db)):
    db_changelog = crud.get_changelog(db, changelog_id=changelog_id)
    if db_changelog is None:
        raise HTTPException(status_code=404, detail="Changelog not found")
    return db_changelog 