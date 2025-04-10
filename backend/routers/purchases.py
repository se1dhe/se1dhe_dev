from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from .. import crud, schemas
from ..database import get_db

router = APIRouter(
    prefix="/purchases",
    tags=["purchases"],
    responses={404: {"description": "Not found"}},
)

@router.post("/", response_model=schemas.Purchase)
def create_purchase(purchase: schemas.PurchaseCreate, db: Session = Depends(get_db)):
    # Проверяем существование пользователя
    db_user = crud.get_user(db, user_id=purchase.user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Проверяем существование бота
    db_bot = crud.get_bot(db, bot_id=purchase.bot_id)
    if db_bot is None:
        raise HTTPException(status_code=404, detail="Bot not found")
    
    # Проверяем баланс пользователя
    if db_user.balance < purchase.price:
        raise HTTPException(status_code=400, detail="Insufficient balance")
    
    # Создаем покупку
    db_purchase = crud.create_purchase(db=db, purchase=purchase)
    
    # Обновляем баланс пользователя
    db_user.balance -= purchase.price
    db.commit()
    db.refresh(db_user)
    
    return db_purchase

@router.get("/", response_model=List[schemas.Purchase])
def read_purchases(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    purchases = crud.get_purchases(db, skip=skip, limit=limit)
    return purchases

@router.get("/{purchase_id}", response_model=schemas.Purchase)
def read_purchase(purchase_id: int, db: Session = Depends(get_db)):
    db_purchase = crud.get_purchase(db, purchase_id=purchase_id)
    if db_purchase is None:
        raise HTTPException(status_code=404, detail="Purchase not found")
    return db_purchase 