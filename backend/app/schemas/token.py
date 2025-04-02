from typing import Optional
from pydantic import BaseModel


class Token(BaseModel):
    """Schema for token response."""
    access_token: str
    token_type: str


class TokenPayload(BaseModel):
    """Schema for token payload data."""
    sub: Optional[int] = None
    exp: Optional[int] = None


class TokenData(BaseModel):
    """Schema for token data extracted from JWT."""
    user_id: Optional[int] = None 