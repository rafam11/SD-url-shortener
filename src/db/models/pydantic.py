from datetime import datetime
from pydantic import BaseModel, Field


class URLModel(BaseModel):
    short_url: str = Field(...)
    long_url: str = Field(...)
    created_at: datetime = Field(default_factory=datetime.now)
    expires_at: datetime = Field(...)
    user_id: int = Field(...)
    is_active: bool = Field(default=True)
    last_accessed_at: datetime | None = Field(None)
    click_count: int = Field(default=0)
