from pymongo import AsyncMongoClient

from api.core.errors import URLNotFoundException
from api.models.pydantic import URLModel
from api.repositories.urls import URLRepository
from api.schemas.url import LongUrlRequest
from api.services.kgs import KGSService


class URLService:
    def __init__(
        self,
        client: AsyncMongoClient,
        kgs_service: KGSService,
    ):
        self.kgs_service = kgs_service
        self.repository = URLRepository(client)

    async def shorten_url(self, user_id: str, request_url: LongUrlRequest) -> URLModel:
        short_url = await self.kgs_service.get_short_url_key()
        url = URLModel(
            short_url=short_url,
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
