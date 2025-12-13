from sqlalchemy.ext.asyncio import AsyncSession

from src.api.repositories.users import UsersRepository
from src.auth.helpers.hasher import Hasher
from src.db.models.users import Users
from src.db.schemas.user import CreateUserRequest, LoginUserRequest


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

    async def login_user(self, user: LoginUserRequest):
        existing_user = await self.repository.retrieve_by(Users, username=user.username)
        if not existing_user:
            return
        if not Hasher.verify_password(user.password, existing_user.password_hash):
            return
        return existing_user