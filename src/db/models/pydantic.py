from bson import Int64
from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field, field_validator


class URLModel(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    short_url: str
    long_url: str
    created_at: datetime = Field(default_factory=datetime.now)
    expires_at: datetime
    user_id: Int64
    is_active: bool = Field(default=True)
    last_accessed_at: datetime | None = Field(None)
    click_count: int = Field(default=0)

    @field_validator("user_id", mode="before")
    def cast_user_id(cls, v):
        """Convert user_id from string or int to Int64"""

        if isinstance(v, Int64):
            return v
        try:
            return Int64(int(v))
        except (ValueError, TypeError):
            raise ValueError("user_id must be convertible to 64-bit integer")
