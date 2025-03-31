from typing import List, Optional
from sqlalchemy.orm import Session
from backend.app.db.repositories.base import BaseRepository
from backend.app.models.category import Category
from backend.app.schemas.category import CategoryCreate, CategoryUpdate


class CategoryRepository(BaseRepository[Category, CategoryCreate, CategoryUpdate]):
    def get_by_slug(self, db: Session, *, slug: str) -> Optional[Category]:
        """Получить категорию по slug"""
        return db.query(Category).filter(Category.slug == slug).first()

    def get_active(
            self, db: Session, *, skip: int = 0, limit: int = 100
    ) -> List[Category]:
        """Получить активные категории"""
        return db.query(Category).filter(
            Category.is_active == True
        ).offset(skip).limit(limit).all()

    def get_with_bots_count(self, db: Session) -> List[dict]:
        """Получить категории с количеством ботов в каждой"""
        from sqlalchemy import func
        from backend.app.models.bot import Bot

        result = db.query(
            Category,
            func.count(Bot.id).label('bots_count')
        ).outerjoin(
            Bot, Category.id == Bot.category_id
        ).filter(
            Category.is_active == True
        ).group_by(
            Category.id
        ).all()

        return [
            {
                "id": category.id,
                "name": category.name,
                "description": category.description,
                "slug": category.slug,
                "image_url": category.image_url,
                "discount_percent": category.discount_percent,
                "bots_count": bots_count
            }
            for category, bots_count in result
        ]

    def apply_discount(self, db: Session, *, category_id: int, discount_percent: float) -> Category:
        """Применить скидку к категории"""
        category = self.get(db, id=category_id)
        if not category:
            return None
        category.discount_percent = discount_percent
        db.add(category)
        db.commit()
        db.refresh(category)
        return category


category_repository = CategoryRepository(Category)