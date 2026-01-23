from api.core.config import settings

from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    AsyncEngine,
    create_async_engine,
    async_sessionmaker,
)
from typing import AsyncGenerator


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


session_manager: SessionManager = SessionManager()
