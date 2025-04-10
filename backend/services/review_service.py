from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import func
from ..models.review import Review
from ..models.user import User
from ..models.bot import Bot
from ..schemas.review import ReviewCreate, ReviewUpdate
from ..services.notification_service import NotificationService

class ReviewService:
    def __init__(self, db: Session):
        self.db = db
        self.notification_service = NotificationService(db)

    async def create_review(self, user_id: int, review: ReviewCreate) -> Review:
        """Создание нового отзыва"""
        # Проверяем, есть ли уже отзыв от этого пользователя
        existing_review = self.db.query(Review).filter(
            Review.user_id == user_id,
            Review.bot_id == review.bot_id
        ).first()
        
        if existing_review:
            raise ValueError("Вы уже оставили отзыв на этого бота")

        # Проверяем, купил ли пользователь бота
        bot = self.db.query(Bot).filter(Bot.id == review.bot_id).first()
        if not bot:
            raise ValueError("Бот не найден")

        is_verified = self._check_purchase(user_id, review.bot_id)

        db_review = Review(
            user_id=user_id,
            bot_id=review.bot_id,
            rating=review.rating,
            comment=review.comment,
            is_verified=is_verified
        )
        
        self.db.add(db_review)
        self.db.commit()
        self.db.refresh(db_review)

        # Обновляем рейтинг бота
        await self._update_bot_rating(review.bot_id)

        # Отправляем уведомление владельцу бота
        await self.notification_service.notify_new_review(
            bot_owner_id=bot.owner_id,
            bot_id=bot.id,
            rating=review.rating,
            comment=review.comment
        )

        return db_review

    async def update_review(self, user_id: int, review_id: int, review: ReviewUpdate) -> Review:
        """Обновление отзыва"""
        db_review = self.db.query(Review).filter(
            Review.id == review_id,
            Review.user_id == user_id
        ).first()
        
        if not db_review:
            raise ValueError("Отзыв не найден")

        for field, value in review.dict(exclude_unset=True).items():
            setattr(db_review, field, value)

        self.db.commit()
        self.db.refresh(db_review)

        # Обновляем рейтинг бота
        await self._update_bot_rating(db_review.bot_id)

        return db_review

    async def delete_review(self, user_id: int, review_id: int) -> None:
        """Удаление отзыва"""
        db_review = self.db.query(Review).filter(
            Review.id == review_id,
            Review.user_id == user_id
        ).first()
        
        if not db_review:
            raise ValueError("Отзыв не найден")

        bot_id = db_review.bot_id
        self.db.delete(db_review)
        self.db.commit()

        # Обновляем рейтинг бота
        await self._update_bot_rating(bot_id)

    def get_reviews(
        self,
        bot_id: Optional[int] = None,
        user_id: Optional[int] = None,
        only_verified: bool = False,
        only_approved: bool = True,
        skip: int = 0,
        limit: int = 100
    ) -> List[Review]:
        """Получение списка отзывов с фильтрацией"""
        query = self.db.query(Review)

        if bot_id:
            query = query.filter(Review.bot_id == bot_id)
        if user_id:
            query = query.filter(Review.user_id == user_id)
        if only_verified:
            query = query.filter(Review.is_verified == True)
        if only_approved:
            query = query.filter(Review.is_approved == True)

        return query.offset(skip).limit(limit).all()

    def _check_purchase(self, user_id: int, bot_id: int) -> bool:
        """Проверка покупки бота пользователем"""
        # TODO: Реализовать проверку покупки через сервис покупок
        return False

    async def _update_bot_rating(self, bot_id: int) -> None:
        """Обновление рейтинга бота"""
        avg_rating = self.db.query(func.avg(Review.rating)).filter(
            Review.bot_id == bot_id,
            Review.is_verified == True,
            Review.is_approved == True
        ).scalar()

        if avg_rating is not None:
            bot = self.db.query(Bot).filter(Bot.id == bot_id).first()
            if bot:
                bot.rating = round(avg_rating, 2)
                self.db.commit() 