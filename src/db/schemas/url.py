from datetime import datetime, timedelta

from pydantic import BaseModel, ConfigDict, Field, HttpUrl
from typing import List


class LongUrlRequest(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    long_url: HttpUrl
    tags: List[str] | None = None
    expires: datetime = Field(
        default_factory=lambda: datetime.now() + timedelta(days=5 * 365)
    )
    custom: str | None = None


class ShortUrlResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    long_url: HttpUrl | None
    short_url: str
    created_at: datetime = datetime.now()
    is_active: bool | None
