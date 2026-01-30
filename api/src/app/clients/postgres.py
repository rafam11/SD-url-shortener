from typing import AsyncGenerator, ClassVar

from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from app.core.config import Settings


class SessionManager:
    """Manages asynchronous database sessions."""

    _engine: ClassVar[AsyncEngine | None] = None
    _session_factory: ClassVar[async_sessionmaker[AsyncSession] | None] = None

    @classmethod
    def run_engine(cls, settings: Settings) -> None:
        """Initialize the database engine and session factory."""
        if cls._engine is not None:
            return

        cls._engine = create_async_engine(url=str(settings.postgres_uri), echo=True)
        cls._session_factory = async_sessionmaker(
            cls._engine, expire_on_commit=False, autoflush=False, class_=AsyncSession
        )

    @classmethod
    async def get_session(cls) -> AsyncGenerator[AsyncSession, None]:
        """Yield a database session."""
        if cls._session_factory is None:
            raise InvalidRequestError("Session has not been initialized")

        async with cls._session_factory() as session:
            try:
                yield session
            except Exception:
                await session.rollback()
                raise

    @classmethod
    async def close(cls) -> None:
        """Dispose of the database engine."""
        if cls._engine is not None:
            await cls._engine.dispose()
            cls._engine = None
            cls._session_factory = None
