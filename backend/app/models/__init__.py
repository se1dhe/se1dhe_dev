from app.db.session import Base

# Импорты моделей для Alembic
from app.models.user import User  # noqa
from app.models.bot import Bot  # noqa
from app.models.category import Category  # noqa
from app.models.order import Order  # noqa
from app.models.bug_report import BugReport  # noqa
from app.models.changelog import Changelog  # noqa
from app.models.feature_request import FeatureRequest, FeatureVote  # noqa
from app.models.review import Review  # noqa
from app.models.notification import Notification  # noqa
from app.models.metric import Metric, BotAnalytics, UserActivity  # noqa
from app.models.subscription import Subscription  # noqa

__all__ = [
    "Base",
    "User",
    "Bot",
    "Category",
    "Order",
    "BugReport",
    "Changelog",
    "FeatureRequest",
    "FeatureVote",
    "Review",
    "Notification",
    "Metric",
    "BotAnalytics",
    "UserActivity",
    "Subscription"
] 