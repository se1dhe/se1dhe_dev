from typing import List, ClassVar, Optional
from app.schemas.user import User
from app.schemas.bot import Bot, BotWithCategory
from app.schemas.category import Category
from app.schemas.review import Review
from app.schemas.subscription import Subscription
from app.schemas.notification import Notification
from app.schemas.metric import BotAnalytics, UserActivity
from app.schemas.feature_request import FeatureRequest, FeatureComment
from app.schemas.changelog import Changelog

class UserWithBots(User):
    Bot: ClassVar[type] = BotWithCategory
    bots: List[BotWithCategory] = []

class BotWithCategory(Bot):
    Category: ClassVar[type] = Category
    category: Category

class BotWithDetails(Bot):
    User: ClassVar[type] = User
    Category: ClassVar[type] = Category
    owner: User
    category: Category

class CategoryWithBots(Category):
    Bot: ClassVar[type] = Bot
    bots: List[Bot] = []

class ReviewWithDetails(Review):
    User: ClassVar[type] = User
    Bot: ClassVar[type] = Bot
    user: User
    bot: Bot

class SubscriptionWithDetails(Subscription):
    User: ClassVar[type] = User
    Bot: ClassVar[type] = Bot
    user: User
    bot: Bot

class NotificationWithDetails(Notification):
    User: ClassVar[type] = User
    user: User

class BotAnalyticsWithBot(BotAnalytics):
    Bot: ClassVar[type] = Bot
    bot: Bot

class UserActivityWithDetails(UserActivity):
    User: ClassVar[type] = User
    Bot: ClassVar[type] = Bot
    user: User
    bot: Optional[Bot] = None

class FeatureRequestWithDetails(FeatureRequest):
    User: ClassVar[type] = User
    Bot: ClassVar[type] = Bot
    user: User
    bot: Bot

class FeatureCommentWithUser(FeatureComment):
    User: ClassVar[type] = User
    user: User

class ChangelogWithBot(Changelog):
    Bot: ClassVar[type] = Bot
    bot: Bot 