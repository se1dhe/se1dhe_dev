from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from datetime import datetime, timedelta
from ..models.analytics import Analytics, BotAnalytics, AnalyticsEventType
from ..schemas.analytics import AnalyticsEventCreate, BotAnalyticsCreate, BotAnalyticsUpdate, AnalyticsCreate, AnalyticsSummary
from ..models.bot import Bot
from ..models.category import Category

class AnalyticsService:
    def __init__(self, db: Session):
        self.db = db

    async def track_event(self, event: AnalyticsCreate) -> Analytics:
        db_event = Analytics(
            user_id=event.user_id,
            event_type=event.event_type,
            event_data=event.event_data,
            metadata=event.metadata
        )
        self.db.add(db_event)
        self.db.commit()
        self.db.refresh(db_event)
        return db_event

    async def update_bot_analytics(self, bot_id: int, event_type: str, amount: float = 0.0) -> BotAnalytics:
        today = datetime.utcnow().date()
        bot_analytics = self.db.query(BotAnalytics).filter(
            BotAnalytics.bot_id == bot_id,
            func.date(BotAnalytics.date) == today
        ).first()

        if not bot_analytics:
            bot_analytics = BotAnalytics(
                bot_id=bot_id,
                date=datetime.utcnow(),
                views=0,
                purchases=0,
                revenue=0.0
            )
            self.db.add(bot_analytics)

        if event_type == "view":
            bot_analytics.views += 1
        elif event_type == "purchase":
            bot_analytics.purchases += 1
            bot_analytics.revenue += amount

        self.db.commit()
        self.db.refresh(bot_analytics)
        return bot_analytics

    async def get_bot_analytics(self, bot_id: int, start_date: datetime, end_date: datetime) -> List[BotAnalytics]:
        return self.db.query(BotAnalytics).filter(
            BotAnalytics.bot_id == bot_id,
            BotAnalytics.date >= start_date,
            BotAnalytics.date <= end_date
        ).all()

    async def get_analytics_summary(self, days: int = 30) -> AnalyticsSummary:
        end_date = datetime.utcnow()
        start_date = end_date - timedelta(days=days)

        # Получаем общую статистику
        total_stats = self.db.query(
            func.sum(BotAnalytics.views).label('total_views'),
            func.sum(BotAnalytics.purchases).label('total_purchases'),
            func.sum(BotAnalytics.revenue).label('total_revenue'),
            func.avg(BotAnalytics.avg_rating).label('avg_rating'),
            func.sum(BotAnalytics.reviews_count).label('total_reviews')
        ).filter(
            BotAnalytics.date >= start_date,
            BotAnalytics.date <= end_date
        ).first()

        # Получаем топ категорий
        top_categories = self.db.query(
            Category.name,
            func.sum(BotAnalytics.views).label('views')
        ).join(
            Bot, Bot.category_id == Category.id
        ).join(
            BotAnalytics, BotAnalytics.bot_id == Bot.id
        ).filter(
            BotAnalytics.date >= start_date,
            BotAnalytics.date <= end_date
        ).group_by(
            Category.name
        ).order_by(
            func.sum(BotAnalytics.views).desc()
        ).limit(5).all()

        # Получаем топ ботов
        top_bots = self.db.query(
            Bot.name,
            func.sum(BotAnalytics.views).label('views')
        ).join(
            BotAnalytics, BotAnalytics.bot_id == Bot.id
        ).filter(
            BotAnalytics.date >= start_date,
            BotAnalytics.date <= end_date
        ).group_by(
            Bot.name
        ).order_by(
            func.sum(BotAnalytics.views).desc()
        ).limit(5).all()

        return AnalyticsSummary(
            total_views=total_stats.total_views or 0,
            total_purchases=total_stats.total_purchases or 0,
            total_revenue=total_stats.total_revenue or 0.0,
            avg_rating=float(total_stats.avg_rating) if total_stats.avg_rating else None,
            total_reviews=total_stats.total_reviews or 0,
            top_categories={cat.name: int(cat.views) for cat in top_categories},
            top_bots={bot.name: int(bot.views) for bot in top_bots}
        )

    async def get_popular_bots(
        self,
        limit: int = 10,
        days: int = 30
    ) -> List[Dict[str, Any]]:
        """Получение списка популярных ботов"""
        start_date = datetime.now() - timedelta(days=days)
        
        popular_bots = self.db.query(
            BotAnalytics.bot_id,
            func.sum(BotAnalytics.views).label("total_views"),
            func.sum(BotAnalytics.purchases).label("total_purchases"),
            func.sum(BotAnalytics.revenue).label("total_revenue")
        ).filter(
            BotAnalytics.date >= start_date
        ).group_by(
            BotAnalytics.bot_id
        ).order_by(
            desc("total_views")
        ).limit(limit).all()

        return [
            {
                "bot_id": bot_id,
                "total_views": total_views,
                "total_purchases": total_purchases,
                "total_revenue": total_revenue
            }
            for bot_id, total_views, total_purchases, total_revenue in popular_bots
        ]

    async def get_user_activity(
        self,
        user_id: int,
        days: int = 30
    ) -> Dict[str, Any]:
        """Получение активности пользователя"""
        start_date = datetime.now() - timedelta(days=days)
        
        activity = self.db.query(
            Analytics.event_type,
            func.count(Analytics.id).label("count")
        ).filter(
            Analytics.user_id == user_id,
            Analytics.created_at >= start_date
        ).group_by(
            Analytics.event_type
        ).all()

        return {
            event_type.value: count
            for event_type, count in activity
        } 