"""
Pydantic schemas for API models.
These schemas handle request/response validation and serialization/deserialization.
"""

from .user import (
    User,
    UserCreate,
    UserUpdate,
    UserInDBBase,
    UserWithSubscriptions,
)

from .bot import (
    Bot,
    BotCreate,
    BotUpdate,
    BotInDBBase,
)

from .category import (
    Category,
    CategoryCreate,
    CategoryUpdate,
    CategoryInDBBase,
)

from .relationships import (
    UserWithBots,
    BotWithCategory,
    BotWithDetails,
    CategoryWithBots,
    ReviewWithDetails,
    SubscriptionWithDetails,
    NotificationWithDetails,
    BotAnalyticsWithBot,
    UserActivityWithDetails,
    FeatureRequestWithDetails,
    FeatureCommentWithUser,
    ChangelogWithBot,
)

from .order import (
    Order,
    OrderCreate,
    OrderUpdate,
    OrderInDBBase,
    OrderWithDetails,
    OrderStatus,
    PaymentMethod,
)

from .review import (
    Review,
    ReviewCreate,
    ReviewUpdate,
    ReviewInDBBase,
    ReviewStats,
)

from .subscription import (
    Subscription,
    SubscriptionCreate,
    SubscriptionUpdate,
    SubscriptionInDBBase,
)

from .notification import (
    Notification,
    NotificationCreate,
    NotificationUpdate,
    NotificationInDBBase,
    NotificationCount,
)

from .metric import (
    Metric,
    MetricCreate,
    MetricUpdate,
    MetricInDBBase,
    BotAnalytics,
    UserActivity,
    MetricQuery,
)

from .bug_report import (
    BugReport,
    BugReportCreate,
    BugReportUpdate,
    BugReportInDBBase,
    BugReportWithDetails,
    BugReportStatus,
    BugReportPriority,
)

from .feature_request import (
    FeatureRequest,
    FeatureRequestCreate,
    FeatureRequestUpdate,
    FeatureRequestInDBBase,
    FeatureRequestStatus,
    FeaturePriority,
    FeatureVote,
    FeatureVoteCreate,
    FeatureVoteInDBBase,
    FeatureComment,
    FeatureCommentCreate,
    FeatureCommentUpdate,
    FeatureCommentInDBBase,
)

from .changelog import (
    Changelog,
    ChangelogCreate,
    ChangelogUpdate,
    ChangelogInDBBase,
)

from .token import (
    Token,
    TokenPayload,
    TokenData,
) 