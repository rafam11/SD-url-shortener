from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.base import BaseRepository


class UserRepository(BaseRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(session)
