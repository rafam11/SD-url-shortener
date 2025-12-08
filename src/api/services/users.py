from sqlalchemy.ext.asyncio import AsyncSession

from src.api.repositories.users import UsersRepository
from src.auth.hasher import Hasher
from src.db.models.users import Users
from src.db.schemas.user import CreateUserRequest


class UsersService:

    def __init__(self, session: AsyncSession):
        self.repository = UsersRepository(session)

    async def create_user(self, user: CreateUserRequest) -> Users:
        
        hashed_password = Hasher.get_password_hash(user.password)

        new_user = Users(
            email=user.email,
            username=user.username,
            password_hash=hashed_password
        )
        
        return await self.repository.create(new_user)
