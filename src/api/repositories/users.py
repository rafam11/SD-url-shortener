from sqlalchemy.ext.asyncio import AsyncSession
from src.api.repositories.base import BaseRepository


class UsersRepository(BaseRepository):

    def __init__(
        self,
        session: AsyncSession
    ):
        super().__init__(session)
