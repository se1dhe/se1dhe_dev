from sqlalchemy.orm import Session
from ..models.user import User
from ..models.bot import Bot
from ..models.category import Category
from ..models.review import Review
from ..models.notification import Notification
from ..models.analytics import Analytics, BotAnalytics
from ..models.ab_test import ABTest, ABTestResult
import pytest
from datetime import datetime

def test_user_model(db: Session):
    user = User(
        email="test@example.com",
        username="testuser",
        hashed_password="hashedpassword"
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    
    assert user.id is not None
    assert user.email == "test@example.com"
    assert user.username == "testuser"
    assert not user.is_active

def test_bot_model(db: Session):
    category = Category(name="Test Category")
    db.add(category)
    db.commit()
    
    bot = Bot(
        name="Test Bot",
        description="Test Description",
        price=10.0,
        category_id=category.id
    )
    db.add(bot)
    db.commit()
    db.refresh(bot)
    
    assert bot.id is not None
    assert bot.name == "Test Bot"
    assert bot.category_id == category.id

def test_review_model(db: Session):
    user = User(email="reviewer@example.com", username="reviewer")
    bot = Bot(name="Test Bot", description="Test", price=10.0)
    db.add_all([user, bot])
    db.commit()
    
    review = Review(
        user_id=user.id,
        bot_id=bot.id,
        rating=5,
        comment="Great bot!"
    )
    db.add(review)
    db.commit()
    db.refresh(review)
    
    assert review.id is not None
    assert review.rating == 5
    assert review.is_verified is False

def test_notification_model(db: Session):
    user = User(email="notified@example.com", username="notified")
    db.add(user)
    db.commit()
    
    notification = Notification(
        user_id=user.id,
        type="system",
        channel="email",
        title="Test Notification",
        message="Test Message"
    )
    db.add(notification)
    db.commit()
    db.refresh(notification)
    
    assert notification.id is not None
    assert notification.is_read == 0

def test_analytics_model(db: Session):
    user = User(email="analytics@example.com", username="analytics")
    db.add(user)
    db.commit()
    
    analytics = Analytics(
        user_id=user.id,
        event_type="page_view",
        event_data={"page": "home"}
    )
    db.add(analytics)
    db.commit()
    db.refresh(analytics)
    
    assert analytics.id is not None
    assert analytics.event_type == "page_view"

def test_bot_analytics_model(db: Session):
    bot = Bot(name="Analytics Bot", description="Test", price=10.0)
    db.add(bot)
    db.commit()
    
    bot_analytics = BotAnalytics(
        bot_id=bot.id,
        date=datetime.now(),
        views=100,
        purchases=10,
        revenue=100.0
    )
    db.add(bot_analytics)
    db.commit()
    db.refresh(bot_analytics)
    
    assert bot_analytics.id is not None
    assert bot_analytics.views == 100

def test_ab_test_model(db: Session):
    ab_test = ABTest(
        name="Test AB Test",
        type="ui_changes",
        variants={"A": {"color": "red"}, "B": {"color": "blue"}},
        metrics=["conversion_rate"]
    )
    db.add(ab_test)
    db.commit()
    db.refresh(ab_test)
    
    assert ab_test.id is not None
    assert ab_test.status == "draft"

def test_ab_test_result_model(db: Session):
    ab_test = ABTest(
        name="Test AB Test",
        type="ui_changes",
        variants={"A": {}, "B": {}},
        metrics=["conversion_rate"]
    )
    db.add(ab_test)
    db.commit()
    
    result = ABTestResult(
        test_id=ab_test.id,
        variant="A",
        metrics_data={"conversion_rate": 0.5}
    )
    db.add(result)
    db.commit()
    db.refresh(result)
    
    assert result.id is not None
    assert result.variant == "A" 