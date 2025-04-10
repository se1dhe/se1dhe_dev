from sqlalchemy.orm import Session
from ..services.user_service import UserService
from ..services.bot_service import BotService
from ..services.review_service import ReviewService
from ..services.notification_service import NotificationService
from ..services.analytics_service import AnalyticsService
from ..services.ab_test_service import ABTestService
from ..schemas.user import UserCreate
from ..schemas.bot import BotCreate
from ..schemas.review import ReviewCreate
from ..schemas.notification import NotificationCreate
from ..schemas.analytics import AnalyticsEventCreate
from ..schemas.ab_test import ABTestCreate, ABTestResultCreate
import pytest
from datetime import datetime

@pytest.fixture
def user_service(db: Session):
    return UserService(db)

@pytest.fixture
def bot_service(db: Session):
    return BotService(db)

@pytest.fixture
def review_service(db: Session):
    return ReviewService(db)

@pytest.fixture
def notification_service(db: Session):
    return NotificationService(db)

@pytest.fixture
def analytics_service(db: Session):
    return AnalyticsService(db)

@pytest.fixture
def ab_test_service(db: Session):
    return ABTestService(db)

async def test_user_service(user_service: UserService):
    user_data = UserCreate(
        email="test@example.com",
        username="testuser",
        password="testpass"
    )
    user = await user_service.create_user(user_data)
    assert user.id is not None
    assert user.email == user_data.email

async def test_bot_service(bot_service: BotService):
    bot_data = BotCreate(
        name="Test Bot",
        description="Test Description",
        price=10.0,
        category_id=1
    )
    bot = await bot_service.create_bot(bot_data)
    assert bot.id is not None
    assert bot.name == bot_data.name

async def test_review_service(review_service: ReviewService):
    review_data = ReviewCreate(
        user_id=1,
        bot_id=1,
        rating=5,
        comment="Great bot!"
    )
    review = await review_service.create_review(review_data)
    assert review.id is not None
    assert review.rating == review_data.rating

async def test_notification_service(notification_service: NotificationService):
    notification_data = NotificationCreate(
        user_id=1,
        type="system",
        channel="email",
        title="Test Notification",
        message="Test Message"
    )
    notification = await notification_service.create_notification(notification_data)
    assert notification.id is not None
    assert notification.title == notification_data.title

async def test_analytics_service(analytics_service: AnalyticsService):
    event_data = AnalyticsEventCreate(
        user_id=1,
        event_type="page_view",
        event_data={"page": "home"}
    )
    event = await analytics_service.track_event(event_data)
    assert event.id is not None
    assert event.event_type == event_data.event_type

async def test_ab_test_service(ab_test_service: ABTestService):
    # Создание теста
    test_data = ABTestCreate(
        name="Test AB Test",
        type="ui_changes",
        variants={"A": {"color": "red"}, "B": {"color": "blue"}},
        metrics=["conversion_rate"]
    )
    test = await ab_test_service.create_test(test_data)
    assert test.id is not None
    assert test.status == "draft"

    # Запуск теста
    started_test = await ab_test_service.start_test(test.id)
    assert started_test.status == "active"

    # Назначение варианта
    variant = await ab_test_service.assign_variant(test.id)
    assert variant in ["A", "B"]

    # Запись результата
    result_data = ABTestResultCreate(
        test_id=test.id,
        variant=variant,
        metrics_data={"conversion_rate": 0.5}
    )
    result = await ab_test_service.record_result(result_data)
    assert result.id is not None
    assert result.variant == variant

    # Получение статистики
    statistics = await ab_test_service.get_test_statistics(test.id)
    assert variant in statistics
    assert statistics[variant].total_participants == 1 