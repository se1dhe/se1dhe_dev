from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import func
import numpy as np
from ..models.user_preference import UserPreference
from ..models.bot import Bot
from ..models.category import Category
from ..schemas.user_preference import UserPreferenceCreate, UserPreferenceUpdate
from .cache_service import CacheService

class RecommendationService:
    def __init__(self, db: Session):
        self.db = db
        self.cache = CacheService()

    async def update_user_preference(
        self,
        user_id: int,
        category_id: int,
        interaction_type: str,
        interaction_weight: float = 0.1
    ) -> None:
        """Обновление предпочтений пользователя на основе взаимодействия"""
        preference = self.db.query(UserPreference).filter(
            UserPreference.user_id == user_id,
            UserPreference.category_id == category_id
        ).first()

        if not preference:
            preference = UserPreference(
                user_id=user_id,
                category_id=category_id,
                preference_score=0.0,
                interaction_count=0
            )
            self.db.add(preference)

        # Обновляем счетчик взаимодействий
        preference.interaction_count += 1
        preference.last_interaction = func.now()

        # Обновляем оценку предпочтения
        if interaction_type == "view":
            weight = interaction_weight
        elif interaction_type == "purchase":
            weight = interaction_weight * 2
        elif interaction_type == "review":
            weight = interaction_weight * 1.5
        else:
            weight = interaction_weight

        # Экспоненциальное затухание для старых взаимодействий
        time_factor = 1.0 / (1.0 + np.log(1 + preference.interaction_count))
        preference.preference_score = min(1.0, preference.preference_score + weight * time_factor)

        self.db.commit()

        # Инвалидируем кэш предпочтений и рекомендаций
        await self.cache.delete(f"user_preferences:{user_id}")
        await self.cache.delete(f"recommendations:{user_id}:all")
        await self.cache.delete(f"recommendations:{user_id}:{category_id}")

    async def get_recommendations(
        self,
        user_id: int,
        limit: int = 10,
        category_id: Optional[int] = None
    ) -> List[Bot]:
        """Получение рекомендаций для пользователя"""
        # Пробуем получить рекомендации из кэша
        cached_recommendations = await self.cache.get_recommendations(user_id, category_id)
        if cached_recommendations:
            return cached_recommendations

        # Получаем предпочтения пользователя
        preferences = self.db.query(UserPreference).filter(
            UserPreference.user_id == user_id
        ).all()

        if not preferences:
            # Если нет предпочтений, возвращаем популярные боты
            bots = await self._get_popular_bots(limit, category_id)
            # Сохраняем в кэш
            await self.cache.set_recommendations(user_id, bots, category_id)
            return bots

        # Создаем вектор предпочтений
        preference_vector = {
            pref.category_id: pref.preference_score
            for pref in preferences
        }

        # Получаем боты с учетом предпочтений
        query = self.db.query(Bot).join(Category)

        if category_id:
            query = query.filter(Bot.category_id == category_id)

        # Сортируем по рейтингу и предпочтениям
        bots = query.all()
        scored_bots = []

        for bot in bots:
            # Базовый вес - рейтинг бота
            score = bot.rating or 0.0

            # Учитываем предпочтения пользователя
            if bot.category_id in preference_vector:
                score *= (1.0 + preference_vector[bot.category_id])

            scored_bots.append((bot, score))

        # Сортируем по итоговому весу
        scored_bots.sort(key=lambda x: x[1], reverse=True)
        recommendations = [bot for bot, _ in scored_bots[:limit]]

        # Сохраняем в кэш
        await self.cache.set_recommendations(user_id, recommendations, category_id)
        return recommendations

    async def _get_popular_bots(
        self,
        limit: int = 10,
        category_id: Optional[int] = None
    ) -> List[Bot]:
        """Получение популярных ботов"""
        # Пробуем получить из кэша
        cached_bots = await self.cache.get_popular_bots(category_id)
        if cached_bots:
            return cached_bots

        query = self.db.query(Bot).filter(Bot.rating.isnot(None))

        if category_id:
            query = query.filter(Bot.category_id == category_id)

        bots = query.order_by(Bot.rating.desc()).limit(limit).all()

        # Сохраняем в кэш
        await self.cache.set_popular_bots(bots, category_id)
        return bots

    async def get_similar_users(
        self,
        user_id: int,
        limit: int = 5
    ) -> List[int]:
        """Получение списка похожих пользователей"""
        # TODO: Реализовать поиск похожих пользователей на основе предпочтений
        return []

    async def get_category_recommendations(
        self,
        user_id: int,
        limit: int = 5
    ) -> List[Category]:
        """Получение рекомендаций категорий для пользователя"""
        # Пробуем получить из кэша
        cached_preferences = await self.cache.get_user_preferences(user_id)
        if cached_preferences:
            return [self.db.query(Category).get(cat_id) for cat_id in cached_preferences.keys()][:limit]

        preferences = self.db.query(UserPreference).filter(
            UserPreference.user_id == user_id
        ).order_by(UserPreference.preference_score.desc()).limit(limit).all()

        # Сохраняем в кэш
        preferences_dict = {pref.category_id: pref.preference_score for pref in preferences}
        await self.cache.set_user_preferences(user_id, preferences_dict)

        return [pref.category for pref in preferences] 