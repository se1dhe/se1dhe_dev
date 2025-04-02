from typing import Optional, List, ClassVar
from pydantic import BaseModel
from datetime import datetime
from enum import Enum

from app.schemas.user import User
from app.schemas.bot import BotWithCategory


class BugReportStatus(str, Enum):
    NEW = "new"
    IN_PROGRESS = "in_progress"
    RESOLVED = "resolved"
    CLOSED = "closed"


class BugReportPriority(int, Enum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    CRITICAL = 4


class BugReportBase(BaseModel):
    title: str
    description: str
    user_id: int
    bot_id: int
    status: BugReportStatus = BugReportStatus.NEW
    priority: BugReportPriority = BugReportPriority.MEDIUM


class BugReportCreate(BugReportBase):
    pass


class BugReportUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[BugReportStatus] = None
    priority: Optional[BugReportPriority] = None


class BugReportInDBBase(BugReportBase):
    id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class BugReport(BugReportInDBBase):
    pass


class BugReportWithDetails(BugReport):
    User: ClassVar[type] = User
    BotWithCategory: ClassVar[type] = BotWithCategory
    user: User
    bot: BotWithCategory 