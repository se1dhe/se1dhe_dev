from fastapi import APIRouter

from app.api.api_v1.endpoints import (
    auth,
    users,
    bots,
    categories,
    orders,
    reviews,
    subscriptions,
    notifications,
    metrics,
    bug_reports,
    feature_requests,
    changelogs,
)

api_router = APIRouter()

# Auth routes
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])

# User routes
api_router.include_router(users.router, prefix="/users", tags=["users"])

# Bot routes
api_router.include_router(bots.router, prefix="/bots", tags=["bots"])

# Category routes
api_router.include_router(categories.router, prefix="/categories", tags=["categories"])

# Order routes
api_router.include_router(orders.router, prefix="/orders", tags=["orders"])

# Review routes
api_router.include_router(reviews.router, prefix="/reviews", tags=["reviews"])

# Subscription routes
api_router.include_router(subscriptions.router, prefix="/subscriptions", tags=["subscriptions"])

# Notification routes
api_router.include_router(notifications.router, prefix="/notifications", tags=["notifications"])

# Metric routes
api_router.include_router(metrics.router, prefix="/metrics", tags=["metrics"])

# Bug report routes
api_router.include_router(bug_reports.router, prefix="/bug-reports", tags=["bug-reports"])

# Feature request routes
api_router.include_router(feature_requests.router, prefix="/feature-requests", tags=["feature-requests"])

# Changelog routes
api_router.include_router(changelogs.router, prefix="/changelogs", tags=["changelogs"]) 