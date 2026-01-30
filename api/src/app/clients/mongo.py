from typing import ClassVar

from pymongo import AsyncMongoClient
from pymongo.errors import ConnectionFailure

from app.core.config import Settings


class MongoClient:
    """Manages asynchronous MongoDB client session."""

    _client: ClassVar[AsyncMongoClient | None] = None

    @classmethod
    async def start_client(cls, settings: Settings):
        """Initialize the database client and verify connection."""
        if cls._client is not None:
            return
        try:
            client: AsyncMongoClient = AsyncMongoClient(host=str(settings.mongo_uri))
            await client.admin.command("ping")
            cls._client = client
        except ConnectionFailure as exc:
            await client.close()
            raise RuntimeError("MongoDB connection failed during startup") from exc

    @classmethod
    def get_client(cls) -> AsyncMongoClient:
        if cls._client is None:
            raise RuntimeError("MongoDB client has not been initialized")
        return cls._client

    @classmethod
    async def close_client(cls):
        if cls._client is not None:
            await cls._client.close()
            cls._client = None
