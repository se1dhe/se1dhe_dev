import pytest
from datetime import datetime, timedelta
from ..services.recommendation_service import RecommendationService
from ..models.user import User
from ..models.bot import Bot
from ..models.category import Category
from ..models.user_preference import UserPreference

@pytest.fixture
def db_session(test_db):
    return test_db

@pytest.fixture
def recommendation_service(db_session):
    return RecommendationService(db_session)

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

def test_update_user_preference(recommendation_service, db_session, test_user, test_category):
    # Обновляем предпочтения пользователя
    recommendation_service.update_user_preference(
        user_id=test_user.id,
        category_id=test_category.id,
        interaction_type="view",
        interaction_weight=1.0
    )
    
    # Проверяем, что предпочтение создано
    preference = db_session.query(UserPreference).filter(
        UserPreference.user_id == test_user.id,
        UserPreference.category_id == test_category.id
    ).first()
    
    assert preference is not None
    assert preference.preference_score > 0
    assert preference.interaction_count == 1

def test_get_recommendations(recommendation_service, db_session, test_user, test_category, test_bot):
    # Создаем предпочтение пользователя
    recommendation_service.update_user_preference(
        user_id=test_user.id,
        category_id=test_category.id,
        interaction_type="view",
        interaction_weight=1.0
    )
    
    # Получаем рекомендации
    recommendations = recommendation_service.get_recommendations(test_user.id)
    
    assert len(recommendations) > 0
    assert any(bot.id == test_bot.id for bot in recommendations)

def test_get_popular_bots(recommendation_service, db_session, test_category, test_bot):
    # Получаем популярные боты
    popular_bots = recommendation_service._get_popular_bots()
    
    assert len(popular_bots) > 0
    assert any(bot.id == test_bot.id for bot in popular_bots)

def test_get_category_recommendations(recommendation_service, db_session, test_user, test_category):
    # Создаем предпочтение пользователя
    recommendation_service.update_user_preference(
        user_id=test_user.id,
        category_id=test_category.id,
        interaction_type="view",
        interaction_weight=1.0
    )
    
    # Получаем рекомендации по категориям
    category_recommendations = recommendation_service.get_category_recommendations(test_user.id)
    
    assert len(category_recommendations) > 0
    assert any(cat.id == test_category.id for cat in category_recommendations) 