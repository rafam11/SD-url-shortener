from pymongo import AsyncMongoClient
from pymongo.errors import ConnectionFailure
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    AsyncEngine,
    create_async_engine,
    async_sessionmaker,
)
from src.db.utils.settings import settings
from typing import AsyncGenerator, ClassVar


class SessionManager:
    """Manages asynchronous database sessions."""

    def __init__(self) -> None:
        self.engine: AsyncEngine | None = None
        self.session_factory: async_sessionmaker[AsyncSession] | None = None

    def run_engine(self):
        """Initialize the database engine and session factory."""
        self.engine = create_async_engine(url=str(settings.postgres_uri), echo=True)
        self.session_factory = async_sessionmaker(
            self.engine, expire_on_commit=False, autoflush=False, class_=AsyncSession
        )

    async def get_session(self) -> AsyncGenerator[AsyncSession, None]:
        """Yield a database session."""
        if not self.session_factory:
            raise InvalidRequestError("Session has not been initialized")

        async with self.session_factory() as session:
            try:
                yield session
            except Exception:
                await session.rollback()
                raise

    async def close(self) -> None:
        """Dispose of the database engine."""
        if self.engine:
            await self.engine.dispose()


class MongoClient:
    """Manages asynchronous MongoDB client session."""

    _client: ClassVar[AsyncMongoClient | None] = None

    @classmethod
    async def start_client(cls):
        """Initialize the database client and verify connection."""
        if cls._client is not None:
            return
        try:
            client = AsyncMongoClient(host=settings.mongo_uri)
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


session_manager: SessionManager = SessionManager()
