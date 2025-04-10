from fastapi import APIRouter
from . import users, categories, bots, purchases, bug_reports, changelog

router = APIRouter()

router.include_router(users.router)
router.include_router(categories.router)
router.include_router(bots.router)
router.include_router(purchases.router)
router.include_router(bug_reports.router)
router.include_router(changelog.router) 