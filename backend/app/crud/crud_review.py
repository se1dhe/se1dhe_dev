from typing import List, Optional, Dict, Any, Union, Tuple
from datetime import datetime

from sqlalchemy.orm import Session, joinedload
from sqlalchemy import desc, func, and_

from app.models.review import Review
from app.schemas.review import ReviewCreate, ReviewUpdate, ReviewStats
from app.services.telegram import telegram_service
from .base import CRUDBase


class CRUDReview(CRUDBase[Review, ReviewCreate, ReviewUpdate]):
    """CRUD операции для отзывов о ботах"""
    
    async def create_with_verification(
        self, db: Session, *, obj_in: ReviewCreate, user_id: int, bot_id: int
    ) -> Review:
        """
        Создать новый отзыв с проверкой покупки
        
        Args:
            db: Сессия БД
            obj_in: Данные для создания отзыва
            user_id: ID пользователя
            bot_id: ID бота
            
        Returns:
            Созданный объект отзыва
        """
        from .crud_order import order as order_crud
        
        # Проверяем, есть ли у пользователя завершенные заказы на этого бота
        verified_purchase = order_crud.has_completed_orders(
            db, user_id=user_id, bot_id=bot_id
        )
        
        data = obj_in.dict()
        db_obj = Review(
            user_id=user_id,
            bot_id=bot_id,
            rating=data["rating"],
            title=data["title"],
            content=data["content"],
            verified_purchase=verified_purchase,
            created_at=datetime.utcnow()
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        
        # Отправляем уведомление владельцу бота
        bot = db_obj.bot
        if bot and bot.owner:
            await telegram_service.send_notification(
                user=bot.owner,
                notification=await crud.notification.create_notification(
                    db=db,
                    user_id=bot.owner.id,
                    title="Новый отзыв о вашем боте",
                    message=f"Пользователь {db_obj.user.username} оставил отзыв о вашем боте {bot.name}:\n\n"
                           f"Оценка: {db_obj.rating}/5\n"
                           f"Заголовок: {db_obj.title}\n"
                           f"Отзыв: {db_obj.content}",
                    notification_type="REVIEW",
                    related_id=db_obj.id,
                    link=f"/bots/{bot_id}/reviews/{db_obj.id}"
                )
            )
        
        return db_obj
    
    def get_user_review_for_bot(
        self, db: Session, *, user_id: int, bot_id: int
    ) -> Optional[Review]:
        """
        Получить отзыв пользователя о конкретном боте
        
        Args:
            db: Сессия БД
            user_id: ID пользователя
            bot_id: ID бота
            
        Returns:
            Объект отзыва или None
        """
        return (
            db.query(Review)
            .filter(
                and_(
                    Review.user_id == user_id,
                    Review.bot_id == bot_id
                )
            )
            .first()
        )
    
    def get_by_user(
        self, db: Session, *, user_id: int, skip: int = 0, limit: int = 100
    ) -> List[Review]:
        """
        Получить отзывы, созданные конкретным пользователем
        
        Args:
            db: Сессия БД
            user_id: ID пользователя
            skip: Сколько записей пропустить
            limit: Максимальное количество записей
            
        Returns:
            Список отзывов пользователя
        """
        return (
            db.query(Review)
            .filter(Review.user_id == user_id)
            .order_by(desc(Review.created_at))
            .offset(skip)
            .limit(limit)
            .all()
        )
    
    def get_by_bot(
        self, db: Session, *, bot_id: int, verified_only: bool = False, 
        skip: int = 0, limit: int = 100
    ) -> List[Review]:
        """
        Получить отзывы для конкретного бота
        
        Args:
            db: Сессия БД
            bot_id: ID бота
            verified_only: Только подтвержденные покупки
            skip: Сколько записей пропустить
            limit: Максимальное количество записей
            
        Returns:
            Список отзывов для бота
        """
        query = db.query(Review).filter(Review.bot_id == bot_id)
        
        if verified_only:
            query = query.filter(Review.verified_purchase == True)
            
        return (
            query
            .order_by(desc(Review.created_at))
            .offset(skip)
            .limit(limit)
            .all()
        )
    
    def get_with_details(self, db: Session, id: int) -> Optional[Review]:
        """
        Получить отзыв с детальной информацией о пользователе и боте
        
        Args:
            db: Сессия БД
            id: ID отзыва
            
        Returns:
            Review с загруженными связанными объектами или None
        """
        return (
            db.query(Review)
            .filter(Review.id == id)
            .options(
                joinedload(Review.user),
                joinedload(Review.bot)
            )
            .first()
        )
    
    def get_multi_with_details(
        self, db: Session, *, skip: int = 0, limit: int = 100
    ) -> List[Review]:
        """
        Получить список отзывов с детальной информацией
        
        Args:
            db: Сессия БД
            skip: Сколько записей пропустить
            limit: Максимальное количество записей
            
        Returns:
            Список отзывов с загруженными связанными объектами
        """
        return (
            db.query(Review)
            .options(
                joinedload(Review.user),
                joinedload(Review.bot)
            )
            .order_by(desc(Review.created_at))
            .offset(skip)
            .limit(limit)
            .all()
        )
    
    async def update_user_review(
        self, db: Session, *, user_id: int, bot_id: int, obj_in: ReviewUpdate
    ) -> Optional[Review]:
        """
        Обновить отзыв пользователя о боте
        
        Args:
            db: Сессия БД
            user_id: ID пользователя
            bot_id: ID бота
            obj_in: Данные для обновления
            
        Returns:
            Обновленный отзыв или None, если отзыв не найден
        """
        db_obj = self.get_user_review_for_bot(db, user_id=user_id, bot_id=bot_id)
        if not db_obj:
            return None
            
        update_data = obj_in.dict(exclude_unset=True)
        
        # Обновляем поля
        for field in update_data:
            setattr(db_obj, field, update_data[field])
            
        db_obj.updated_at = datetime.utcnow()
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        
        # Отправляем уведомление владельцу бота об обновлении отзыва
        bot = db_obj.bot
        if bot and bot.owner:
            await telegram_service.send_notification(
                user=bot.owner,
                notification=await crud.notification.create_notification(
                    db=db,
                    user_id=bot.owner.id,
                    title="Отзыв о вашем боте обновлен",
                    message=f"Пользователь {db_obj.user.username} обновил свой отзыв о вашем боте {bot.name}:\n\n"
                           f"Оценка: {db_obj.rating}/5\n"
                           f"Заголовок: {db_obj.title}\n"
                           f"Отзыв: {db_obj.content}",
                    notification_type="REVIEW",
                    related_id=db_obj.id,
                    link=f"/bots/{bot_id}/reviews/{db_obj.id}"
                )
            )
        
        return db_obj
    
    def get_bot_stats(self, db: Session, *, bot_id: int) -> ReviewStats:
        """
        Получить статистику отзывов для бота
        
        Args:
            db: Сессия БД
            bot_id: ID бота
            
        Returns:
            Объект со статистикой отзывов
        """
        # Получаем общее количество отзывов
        total_reviews = db.query(Review).filter(Review.bot_id == bot_id).count()
        
        # Если отзывов нет, возвращаем пустую статистику
        if total_reviews == 0:
            return ReviewStats(
                bot_id=bot_id,
                average_rating=0.0,
                total_reviews=0,
                rating_distribution={1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
            )
        
        # Получаем средний рейтинг
        average_rating = db.query(func.avg(Review.rating)).filter(Review.bot_id == bot_id).scalar() or 0.0
        
        # Округляем средний рейтинг до 1 десятичного знака
        average_rating = round(float(average_rating), 1)
        
        # Получаем распределение оценок
        rating_distribution = {}
        for i in range(1, 6):
            count = db.query(Review).filter(
                Review.bot_id == bot_id, 
                func.floor(Review.rating) == i
            ).count()
            rating_distribution[i] = count
        
        return ReviewStats(
            bot_id=bot_id,
            average_rating=average_rating,
            total_reviews=total_reviews,
            rating_distribution=rating_distribution
        )


# Создание экземпляра CRUD для использования в API
review = CRUDReview(Review) 