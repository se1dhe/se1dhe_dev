from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import select, func

from app.crud.base import CRUDBase
from app.models.category import Category
from app.schemas.category import CategoryCreate, CategoryUpdate


class CRUDCategory(CRUDBase[Category, CategoryCreate, CategoryUpdate]):
    """CRUD operations for categories."""
    
    async def get_active_categories(self, db: Session) -> List[Category]:
        """Get all active categories."""
        query = select(self.model).where(self.model.is_active == True)
        result = await db.execute(query)
        return result.scalars().all()
    
    async def get_category_with_bots(self, db: Session, category_id: int) -> Optional[Category]:
        """Get a category with its bots."""
        query = select(self.model).where(
            self.model.id == category_id,
            self.model.is_active == True
        )
        result = await db.execute(query)
        return result.scalar_one_or_none()
    
    async def get_categories_with_bot_count(self, db: Session) -> List[dict]:
        """Get all categories with their bot counts."""
        from app.models.bot import Bot
        
        query = select(
            self.model,
            func.count(Bot.id).label('bot_count')
        ).outerjoin(
            Bot,
            (Bot.category_id == self.model.id) & (Bot.is_active == True)
        ).where(
            self.model.is_active == True
        ).group_by(
            self.model.id
        )
        
        result = await db.execute(query)
        categories = []
        for category, bot_count in result:
            category_dict = {
                'id': category.id,
                'name': category.name,
                'description': category.description,
                'is_active': category.is_active,
                'created_at': category.created_at,
                'updated_at': category.updated_at,
                'bot_count': bot_count
            }
            categories.append(category_dict)
        return categories


category = CRUDCategory(Category) 