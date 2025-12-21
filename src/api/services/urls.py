from pymongo import AsyncMongoClient

from src.api.repositories.urls import URLsRepository
from src.db.models.pydantic import URLModel
from src.db.schemas.url import LongUrlRequest


class URLsService:
    def __init__(self, client: AsyncMongoClient):
        self.repository = URLsRepository(client)

    async def shorten_url(self, user_id: str, request_url: LongUrlRequest) -> URLModel:
        url = URLModel(
            short_url="abcd123",
            long_url=str(request_url.long_url),
            expires_at=request_url.expires,
            user_id=int(user_id),
        )
        return await self.repository.insert(url)
