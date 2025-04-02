from typing import List, Optional, Dict, Any, Union
from datetime import datetime

from sqlalchemy.orm import Session, joinedload
from sqlalchemy import func, desc

from app.models.bot import Bot
from app.models.category import Category
from app.models.user import user_bot_subscriptions
from app.schemas.bot import BotCreate, BotUpdate, SubscriptionCreate, SubscriptionUpdate
from .base import CRUDBase


class CRUDBot(CRUDBase[Bot, BotCreate, BotUpdate]):
    """CRUD операции для Telegram ботов"""
    
    def get_with_category(self, db: Session, id: int) -> Optional[Bot]:
        """
        Получить бота вместе с данными о его категории
        
        Args:
            db: Сессия БД
            id: ID бота
            
        Returns:
            Bot с загруженной категорией или None
        """
        return (
            db.query(Bot)
            .filter(Bot.id == id)
            .options(joinedload(Bot.category))
            .first()
        )
    
    def get_multi_with_categories(
        self, db: Session, *, skip: int = 0, limit: int = 100
    ) -> List[Bot]:
        """
        Получить список ботов с их категориями
        
        Args:
            db: Сессия БД
            skip: Сколько записей пропустить
            limit: Максимальное количество записей
            
        Returns:
            Список ботов с загруженными категориями
        """
        return (
            db.query(Bot)
            .options(joinedload(Bot.category))
            .offset(skip)
            .limit(limit)
            .all()
        )
    
    def get_by_category(
        self, db: Session, *, category_id: int, skip: int = 0, limit: int = 100
    ) -> List[Bot]:
        """
        Получить ботов определенной категории
        
        Args:
            db: Сессия БД
            category_id: ID категории
            skip: Сколько записей пропустить
            limit: Максимальное количество записей
            
        Returns:
            Список ботов данной категории
        """
        return (
            db.query(Bot)
            .filter(Bot.category_id == category_id)
            .offset(skip)
            .limit(limit)
            .all()
        )
    
    def get_featured(
        self, db: Session, *, skip: int = 0, limit: int = 100
    ) -> List[Bot]:
        """
        Получить выделенных (featured) ботов
        
        Args:
            db: Сессия БД
            skip: Сколько записей пропустить
            limit: Максимальное количество записей
            
        Returns:
            Список выделенных ботов
        """
        return (
            db.query(Bot)
            .filter(Bot.is_featured == True)
            .options(joinedload(Bot.category))
            .offset(skip)
            .limit(limit)
            .all()
        )
    
    def search_bots(
        self, db: Session, *, query: str, skip: int = 0, limit: int = 100
    ) -> List[Bot]:
        """
        Поиск ботов по имени или описанию
        
        Args:
            db: Сессия БД
            query: Поисковый запрос
            skip: Сколько записей пропустить
            limit: Максимальное количество записей
            
        Returns:
            Список ботов, соответствующих запросу
        """
        search_query = f"%{query}%"
        return (
            db.query(Bot)
            .filter(
                (Bot.name.ilike(search_query)) | 
                (Bot.description.ilike(search_query))
            )
            .options(joinedload(Bot.category))
            .offset(skip)
            .limit(limit)
            .all()
        )
    
    def create_subscription(
        self, db: Session, *, obj_in: SubscriptionCreate
    ) -> dict:
        """
        Создать подписку пользователя на бота
        
        Args:
            db: Сессия БД
            obj_in: Данные для создания подписки
            
        Returns:
            Словарь с информацией о подписке
        """
        subscription_data = {
            "user_id": obj_in.user_id,
            "bot_id": obj_in.bot_id,
            "created_at": datetime.utcnow(),
            "expires_at": obj_in.expires_at
        }
        
        stmt = user_bot_subscriptions.insert().values(**subscription_data)
        db.execute(stmt)
        db.commit()
        
        return subscription_data
    
    def update_subscription(
        self, db: Session, *, user_id: int, bot_id: int, obj_in: SubscriptionUpdate
    ) -> dict:
        """
        Обновить подписку пользователя на бота
        
        Args:
            db: Сессия БД
            user_id: ID пользователя
            bot_id: ID бота
            obj_in: Данные для обновления подписки
            
        Returns:
            Словарь с информацией о подписке
        """
        update_data = {}
        if obj_in.expires_at:
            update_data["expires_at"] = obj_in.expires_at
            
        stmt = (
            user_bot_subscriptions.update()
            .where(
                (user_bot_subscriptions.c.user_id == user_id) &
                (user_bot_subscriptions.c.bot_id == bot_id)
            )
            .values(**update_data)
        )
        db.execute(stmt)
        db.commit()
        
        # Получаем обновленные данные
        stmt = (
            user_bot_subscriptions.select()
            .where(
                (user_bot_subscriptions.c.user_id == user_id) &
                (user_bot_subscriptions.c.bot_id == bot_id)
            )
        )
        subscription = db.execute(stmt).first()
        
        if subscription:
            return {
                "user_id": subscription.user_id,
                "bot_id": subscription.bot_id,
                "created_at": subscription.created_at,
                "expires_at": subscription.expires_at
            }
        return {}
    
    def remove_subscription(
        self, db: Session, *, user_id: int, bot_id: int
    ) -> bool:
        """
        Удалить подписку пользователя на бота
        
        Args:
            db: Сессия БД
            user_id: ID пользователя
            bot_id: ID бота
            
        Returns:
            True если подписка была удалена, иначе False
        """
        stmt = (
            user_bot_subscriptions.delete()
            .where(
                (user_bot_subscriptions.c.user_id == user_id) &
                (user_bot_subscriptions.c.bot_id == bot_id)
            )
        )
        result = db.execute(stmt)
        db.commit()
        
        return result.rowcount > 0


class CRUDCategory(CRUDBase[Category, BotCreate, BotUpdate]):
    """CRUD операции для категорий ботов"""
    
    def get_by_slug(self, db: Session, *, slug: str) -> Optional[Category]:
        """
        Получить категорию по slug
        
        Args:
            db: Сессия БД
            slug: Slug категории
            
        Returns:
            Category или None
        """
        return db.query(Category).filter(Category.slug == slug).first()
    
    def get_with_bots_count(
        self, db: Session, *, skip: int = 0, limit: int = 100
    ) -> List[Dict[str, Any]]:
        """
        Получить категории с количеством ботов в каждой
        
        Args:
            db: Сессия БД
            skip: Сколько записей пропустить
            limit: Максимальное количество записей
            
        Returns:
            Список категорий с количеством ботов
        """
        categories = (
            db.query(Category, func.count(Bot.id).label("bots_count"))
            .outerjoin(Bot, Category.id == Bot.category_id)
            .group_by(Category.id)
            .offset(skip)
            .limit(limit)
            .all()
        )
        
        result = []
        for category, bots_count in categories:
            category_dict = {
                "id": category.id,
                "name": category.name,
                "description": category.description,
                "slug": category.slug,
                "is_active": category.is_active,
                "discount_percentage": category.discount_percentage,
                "created_at": category.created_at,
                "updated_at": category.updated_at,
                "bots_count": bots_count
            }
            result.append(category_dict)
            
        return result


# Создание экземпляров CRUD для использования в API
bot = CRUDBot(Bot)
category = CRUDCategory(Category) 