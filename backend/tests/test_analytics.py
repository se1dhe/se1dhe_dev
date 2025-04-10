import pytest
from datetime import datetime, timedelta
from ..services.analytics_service import AnalyticsService
from ..models.analytics import Analytics, BotAnalytics
from ..models.user import User
from ..models.bot import Bot
from ..models.category import Category
from ..schemas.analytics import AnalyticsCreate, BotAnalyticsCreate

@pytest.fixture
def db_session(test_db):
    return test_db

@pytest.fixture
def analytics_service(db_session):
    return AnalyticsService(db_session)

@pytest.fixture
def test_user(db_session):
    user = User(
        email="test@example.com",
        username="testuser",
        hashed_password="hashedpass"
    )
    db_session.add(user)
    db_session.commit()
    return user

@pytest.fixture
def test_category(db_session):
    category = Category(name="Test Category")
    db_session.add(category)
    db_session.commit()
    return category

@pytest.fixture
def test_bot(db_session, test_category):
    bot = Bot(
        name="Test Bot",
        description="Test Description",
        price=10.0,
        category_id=test_category.id
    )
    db_session.add(bot)
    db_session.commit()
    return bot

async def test_track_event(analytics_service, test_user):
    event = AnalyticsCreate(
        user_id=test_user.id,
        event_type="page_view",
        event_data={"page": "home"},
        metadata={"ip": "127.0.0.1"}
    )
    
    tracked_event = await analytics_service.track_event(event)
    
    assert tracked_event.id is not None
    assert tracked_event.user_id == test_user.id
    assert tracked_event.event_type == "page_view"

async def test_update_bot_analytics(analytics_service, test_bot):
    # Тестируем просмотры
    analytics = await analytics_service.update_bot_analytics(test_bot.id, "view")
    assert analytics.views == 1
    assert analytics.purchases == 0
    
    # Тестируем покупки
    analytics = await analytics_service.update_bot_analytics(test_bot.id, "purchase", 10.0)
    assert analytics.views == 1
    assert analytics.purchases == 1
    assert analytics.revenue == 10.0

async def test_get_bot_analytics(analytics_service, test_bot):
    # Создаем несколько записей аналитики
    await analytics_service.update_bot_analytics(test_bot.id, "view")
    await analytics_service.update_bot_analytics(test_bot.id, "purchase", 10.0)
    
    start_date = datetime.utcnow() - timedelta(days=1)
    end_date = datetime.utcnow() + timedelta(days=1)
    
    analytics = await analytics_service.get_bot_analytics(test_bot.id, start_date, end_date)
    
    assert len(analytics) > 0
    assert analytics[0].views == 1
    assert analytics[0].purchases == 1

async def test_get_analytics_summary(analytics_service, test_bot, test_category):
    # Создаем несколько записей аналитики
    await analytics_service.update_bot_analytics(test_bot.id, "view")
    await analytics_service.update_bot_analytics(test_bot.id, "purchase", 10.0)
    
    summary = await analytics_service.get_analytics_summary(days=30)
    
    assert summary.total_views > 0
    assert summary.total_purchases > 0
    assert summary.total_revenue > 0
    assert test_category.name in summary.top_categories
    assert test_bot.name in summary.top_bots 