from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from backend import crud, schemas
from backend.database import get_db

router = APIRouter(
    prefix="/bots",
    tags=["bots"],
    responses={404: {"description": "Not found"}},
)

@router.post("/", response_model=schemas.Bot)
def create_bot(bot: schemas.BotCreate, db: Session = Depends(get_db)):
    # Проверяем существование категории
    db_category = crud.get_category(db, category_id=bot.category_id)
    if db_category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    return crud.create_bot(db=db, bot=bot)

@router.get("/", response_model=List[schemas.Bot])
def read_bots(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    bots = crud.get_bots(db, skip=skip, limit=limit)
    return bots

@router.get("/{bot_id}", response_model=schemas.Bot)
def read_bot(bot_id: int, db: Session = Depends(get_db)):
    db_bot = crud.get_bot(db, bot_id=bot_id)
    if db_bot is None:
        raise HTTPException(status_code=404, detail="Bot not found")
    return db_bot

@router.put("/{bot_id}", response_model=schemas.Bot)
def update_bot(bot_id: int, bot: schemas.BotUpdate, db: Session = Depends(get_db)):
    # Проверяем существование категории, если она указана
    if bot.category_id:
        db_category = crud.get_category(db, category_id=bot.category_id)
        if db_category is None:
            raise HTTPException(status_code=404, detail="Category not found")
    
    db_bot = crud.update_bot(db, bot_id=bot_id, bot=bot)
    if db_bot is None:
        raise HTTPException(status_code=404, detail="Bot not found")
    return db_bot

@router.delete("/{bot_id}")
def delete_bot(bot_id: int, db: Session = Depends(get_db)):
    success = crud.delete_bot(db, bot_id=bot_id)
    if not success:
        raise HTTPException(status_code=404, detail="Bot not found")
    return {"message": "Bot deleted successfully"} 