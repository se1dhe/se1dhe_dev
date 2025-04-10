from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from datetime import datetime

class UserPreferenceBase(BaseModel):
    category_id: int
    preference_score: float = Field(..., ge=0.0, le=1.0)
    metadata: Optional[Dict[str, Any]] = None

class UserPreferenceCreate(UserPreferenceBase):
    pass

class UserPreferenceUpdate(BaseModel):
    preference_score: Optional[float] = Field(None, ge=0.0, le=1.0)
    metadata: Optional[Dict[str, Any]] = None

class UserPreferenceInDB(UserPreferenceBase):
    id: int
    user_id: int
    interaction_count: int
    last_interaction: datetime

    class Config:
        from_attributes = True

class UserPreferenceResponse(UserPreferenceInDB):
    category_name: str

    class Config:
        from_attributes = True 