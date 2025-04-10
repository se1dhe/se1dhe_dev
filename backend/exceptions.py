from fastapi import HTTPException, status
from typing import Any, Dict, Optional

class BaseAPIException(HTTPException):
    def __init__(
        self,
        status_code: int,
        detail: Any = None,
        headers: Optional[Dict[str, str]] = None,
    ) -> None:
        super().__init__(status_code=status_code, detail=detail, headers=headers)

class UserNotFound(BaseAPIException):
    def __init__(self, user_id: int):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {user_id} not found"
        )

class UserAlreadyExists(BaseAPIException):
    def __init__(self, telegram_id: int):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"User with telegram_id {telegram_id} already exists"
        )

class InsufficientBalance(BaseAPIException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Insufficient balance"
        )

class BotNotFound(BaseAPIException):
    def __init__(self, bot_id: int):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Bot with id {bot_id} not found"
        )

class CategoryNotFound(BaseAPIException):
    def __init__(self, category_id: int):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Category with id {category_id} not found"
        )

class PurchaseNotFound(BaseAPIException):
    def __init__(self, purchase_id: int):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Purchase with id {purchase_id} not found"
        )

class BugReportNotFound(BaseAPIException):
    def __init__(self, bug_report_id: int):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Bug report with id {bug_report_id} not found"
        )

class ChangelogNotFound(BaseAPIException):
    def __init__(self, changelog_id: int):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Changelog with id {changelog_id} not found"
        )

class InvalidToken(BaseAPIException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication token"
        )

class TokenExpired(BaseAPIException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired"
        )

class PermissionDenied(BaseAPIException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Permission denied"
        ) 