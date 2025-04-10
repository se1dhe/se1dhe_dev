from sqlalchemy.orm import Session
from . import models, schemas
from typing import List, Optional
from datetime import datetime

# User CRUD
def get_user(db: Session, user_id: int) -> Optional[models.User]:
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_telegram_id(db: Session, telegram_id: int) -> Optional[models.User]:
    return db.query(models.User).filter(models.User.telegram_id == telegram_id).first()

def get_users(db: Session, skip: int = 0, limit: int = 100) -> List[models.User]:
    return db.query(models.User).offset(skip).limit(limit).all()

def create_user(db: Session, user: schemas.UserCreate) -> models.User:
    db_user = models.User(**user.model_dump())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def update_user(db: Session, user_id: int, user: schemas.UserUpdate) -> Optional[models.User]:
    db_user = get_user(db, user_id)
    if db_user:
        for key, value in user.model_dump().items():
            setattr(db_user, key, value)
        db.commit()
        db.refresh(db_user)
    return db_user

def delete_user(db: Session, user_id: int) -> bool:
    db_user = get_user(db, user_id)
    if db_user:
        db.delete(db_user)
        db.commit()
        return True
    return False

# Category CRUD
def get_category(db: Session, category_id: int) -> Optional[models.Category]:
    return db.query(models.Category).filter(models.Category.id == category_id).first()

def get_categories(db: Session, skip: int = 0, limit: int = 100) -> List[models.Category]:
    return db.query(models.Category).offset(skip).limit(limit).all()

def create_category(db: Session, category: schemas.CategoryCreate) -> models.Category:
    db_category = models.Category(**category.model_dump())
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category

def update_category(db: Session, category_id: int, category: schemas.CategoryUpdate) -> Optional[models.Category]:
    db_category = get_category(db, category_id)
    if db_category:
        for key, value in category.model_dump().items():
            setattr(db_category, key, value)
        db.commit()
        db.refresh(db_category)
    return db_category

def delete_category(db: Session, category_id: int) -> bool:
    db_category = get_category(db, category_id)
    if db_category:
        db.delete(db_category)
        db.commit()
        return True
    return False

# Bot CRUD
def get_bot(db: Session, bot_id: int) -> Optional[models.Bot]:
    return db.query(models.Bot).filter(models.Bot.id == bot_id).first()

def get_bots(db: Session, skip: int = 0, limit: int = 100) -> List[models.Bot]:
    return db.query(models.Bot).offset(skip).limit(limit).all()

def create_bot(db: Session, bot: schemas.BotCreate) -> models.Bot:
    db_bot = models.Bot(**bot.model_dump())
    db.add(db_bot)
    db.commit()
    db.refresh(db_bot)
    return db_bot

def update_bot(db: Session, bot_id: int, bot: schemas.BotUpdate) -> Optional[models.Bot]:
    db_bot = get_bot(db, bot_id)
    if db_bot:
        for key, value in bot.model_dump().items():
            setattr(db_bot, key, value)
        db.commit()
        db.refresh(db_bot)
    return db_bot

def delete_bot(db: Session, bot_id: int) -> bool:
    db_bot = get_bot(db, bot_id)
    if db_bot:
        db.delete(db_bot)
        db.commit()
        return True
    return False

# Purchase CRUD
def get_purchase(db: Session, purchase_id: int) -> Optional[models.Purchase]:
    return db.query(models.Purchase).filter(models.Purchase.id == purchase_id).first()

def get_purchases(db: Session, skip: int = 0, limit: int = 100) -> List[models.Purchase]:
    return db.query(models.Purchase).offset(skip).limit(limit).all()

def create_purchase(db: Session, purchase: schemas.PurchaseCreate) -> models.Purchase:
    db_purchase = models.Purchase(**purchase.model_dump())
    db.add(db_purchase)
    db.commit()
    db.refresh(db_purchase)
    return db_purchase

# BugReport CRUD
def get_bug_report(db: Session, bug_report_id: int) -> Optional[models.BugReport]:
    return db.query(models.BugReport).filter(models.BugReport.id == bug_report_id).first()

def get_bug_reports(db: Session, skip: int = 0, limit: int = 100) -> List[models.BugReport]:
    return db.query(models.BugReport).offset(skip).limit(limit).all()

def create_bug_report(db: Session, bug_report: schemas.BugReportCreate) -> models.BugReport:
    db_bug_report = models.BugReport(**bug_report.model_dump())
    db.add(db_bug_report)
    db.commit()
    db.refresh(db_bug_report)
    return db_bug_report

def update_bug_report(db: Session, bug_report_id: int, bug_report: schemas.BugReportUpdate) -> Optional[models.BugReport]:
    db_bug_report = get_bug_report(db, bug_report_id)
    if db_bug_report:
        for key, value in bug_report.model_dump().items():
            setattr(db_bug_report, key, value)
        db.commit()
        db.refresh(db_bug_report)
    return db_bug_report

# Changelog CRUD
def get_changelog(db: Session, changelog_id: int) -> Optional[models.Changelog]:
    return db.query(models.Changelog).filter(models.Changelog.id == changelog_id).first()

def get_changelogs(db: Session, skip: int = 0, limit: int = 100) -> List[models.Changelog]:
    return db.query(models.Changelog).offset(skip).limit(limit).all()

def create_changelog(db: Session, changelog: schemas.ChangelogCreate) -> models.Changelog:
    db_changelog = models.Changelog(**changelog.model_dump())
    db.add(db_changelog)
    db.commit()
    db.refresh(db_changelog)
    return db_changelog 