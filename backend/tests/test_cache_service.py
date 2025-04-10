import pytest
from datetime import datetime
from ..services.cache_service import CacheService
from ..models.bot import Bot
from ..models.category import Category

@pytest.fixture
def cache_service():
    return CacheService()

@pytest.fixture
def test_bot():
    return Bot(
        id=1,
        name="Test Bot",
        description="Test Description",
        price=10.0,
        category_id=1
    )

@pytest.fixture
def test_category():
    return Category(
        id=1,
        name="Test Category"
    )

def test_set_get_string(cache_service):
    # Тестируем сохранение и получение строки
    key = "test_key"
    value = "test_value"
    
    cache_service.set(key, value)
    cached_value = cache_service.get(key)
    
    assert cached_value == value

def test_set_get_json(cache_service):
    # Тестируем сохранение и получение JSON
    key = "test_json_key"
    value = {"test": "value"}
    
    cache_service.set(key, value, data_type="json")
    cached_value = cache_service.get(key, data_type="json")
    
    assert cached_value == value

def test_set_get_pickle(cache_service, test_bot):
    # Тестируем сохранение и получение объекта через pickle
    key = "test_pickle_key"
    
    cache_service.set(key, test_bot, data_type="pickle")
    cached_value = cache_service.get(key, data_type="pickle")
    
    assert isinstance(cached_value, Bot)
    assert cached_value.name == test_bot.name

def test_delete(cache_service):
    # Тестируем удаление из кэша
    key = "test_delete_key"
    value = "test_value"
    
    cache_service.set(key, value)
    cache_service.delete(key)
    
    assert cache_service.get(key) is None

def test_exists(cache_service):
    # Тестируем проверку существования ключа
    key = "test_exists_key"
    value = "test_value"
    
    assert not cache_service.exists(key)
    
    cache_service.set(key, value)
    assert cache_service.exists(key)

def test_increment_decrement(cache_service):
    # Тестируем инкремент и декремент
    key = "test_counter_key"
    
    cache_service.set(key, 0)
    cache_service.increment(key)
    assert cache_service.get(key) == 1
    
    cache_service.decrement(key)
    assert cache_service.get(key) == 0

def test_get_set_popular_bots(cache_service, test_bot):
    # Тестируем кэширование популярных ботов
    bots = [test_bot]
    
    cache_service.set_popular_bots(bots)
    cached_bots = cache_service.get_popular_bots()
    
    assert len(cached_bots) == 1
    assert cached_bots[0].name == test_bot.name

def test_get_set_user_preferences(cache_service, test_category):
    # Тестируем кэширование предпочтений пользователя
    user_id = 1
    preferences = [test_category]
    
    cache_service.set_user_preferences(user_id, preferences)
    cached_preferences = cache_service.get_user_preferences(user_id)
    
    assert len(cached_preferences) == 1
    assert cached_preferences[0].name == test_category.name

def test_get_set_recommendations(cache_service, test_bot):
    # Тестируем кэширование рекомендаций
    user_id = 1
    recommendations = [test_bot]
    
    cache_service.set_recommendations(user_id, recommendations)
    cached_recommendations = cache_service.get_recommendations(user_id)
    
    assert len(cached_recommendations) == 1
    assert cached_recommendations[0].name == test_bot.name 