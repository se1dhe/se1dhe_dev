from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import desc
from backend.app.db.repositories.base import BaseRepository
from backend.app.models.bot import Bot
from backend.app.schemas.bot import BotCreate, BotUpdate


class BotRepository(BaseRepository[Bot, BotCreate, BotUpdate]):
    def get_by_slug(self, db: Session, *, slug: str) -> Optional[Bot]:
        """Получить бот по slug"""
        return db.query(Bot).filter(Bot.slug == slug).first()

    def get_by_category(
            self, db: Session, *, category_id: int, skip: int = 0, limit: int = 100
    ) -> List[Bot]:
        """Получить боты по категории"""
        return db.query(Bot).filter(
            Bot.category_id == category_id,
            Bot.is_active == True
        ).offset(skip).limit(limit).all()

    def get_featured(
            self, db: Session, *, skip: int = 0, limit: int = 100
    ) -> List[Bot]:
        """Получить избранные боты"""
        return db.query(Bot).filter(
            Bot.is_active == True,
            Bot.is_featured == True
        ).offset(skip).limit(limit).all()

    def get_latest(
            self, db: Session, *, skip: int = 0, limit: int = 100
    ) -> List[Bot]:
        """Получить последние добавленные боты"""
        return db.query(Bot).filter(
            Bot.is_active == True
        ).order_by(desc(Bot.created_at)).offset(skip).limit(limit).all()

    def search(
            self, db: Session, *, query: str, skip: int = 0, limit: int = 100
    ) -> List[Bot]:
        """Поиск ботов по названию или описанию"""
        search_query = f"%{query}%"
        return db.query(Bot).filter(
            (Bot.name.ilike(search_query) |
             Bot.short_description.ilike(search_query) |
             Bot.full_description.ilike(search_query)),
            Bot.is_active == True
        ).offset(skip).limit(limit).all()

    def get_active_count(self, db: Session) -> int:
        """Получить количество активных ботов"""
        return db.query(Bot).filter(Bot.is_active == True).count()

    def update_readme(self, db: Session, *, bot_id: int, readme_content: str) -> Bot:
        """Обновить README.md для бота"""
        bot = self.get(db, id=bot_id)
        if not bot:
            return None
        bot.readme_md = readme_content
        db.add(bot)
        db.commit()
        db.refresh(bot)
        return bot


bot_repository = BotRepository(Bot)