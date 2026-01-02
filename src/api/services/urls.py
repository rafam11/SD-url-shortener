from pymongo import AsyncMongoClient

from src.api.repositories.urls import URLRepository
from src.core.errors import URLNotFoundException
from src.db.models.pydantic import URLModel
from src.db.schemas.url import LongUrlRequest


class URLService:
    def __init__(self, client: AsyncMongoClient):
        self.repository = URLRepository(client)

    async def shorten_url(self, user_id: str, request_url: LongUrlRequest) -> URLModel:
        url = URLModel(
            short_url="abcd123",
            long_url=str(request_url.long_url),
            expires_at=request_url.expires,
            user_id=user_id,
        )
        return await self.repository.insert(url)

    async def retrieve_long_url(self, short_url: str) -> str:
        document: URLModel | None = await self.repository.retrieve_by(
            {"short_url": short_url}
        )
        if not document:
            raise URLNotFoundException()
        return document.long_url
