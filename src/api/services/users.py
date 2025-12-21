from sqlalchemy.ext.asyncio import AsyncSession

from src.api.repositories.users import UsersRepository
from src.auth.helpers.security import get_password_hash, verify_password
from src.core.errors import InvalidCredentialsError
from src.db.models.sqlalchemy import Users, UserLogins
from src.db.schemas.user import CreateUserRequest, LoginUserRequest


class UsersService:
    def __init__(self, session: AsyncSession):
        self.repository = UsersRepository(session)

    async def create_user(self, user: CreateUserRequest) -> Users:
        hashed_password = get_password_hash(user.password)

        new_user = Users(
            email=user.email, username=user.username, password_hash=hashed_password
        )

        return await self.repository.create(new_user)

    async def login_user(self, user: LoginUserRequest) -> Users:
        existing_user = await self.repository.retrieve_by(Users, username=user.username)

        if not existing_user or not verify_password(
            user.password, existing_user.password_hash
        ):
            raise InvalidCredentialsError()

        new_login = UserLogins(user_id=existing_user.id)
        await self.repository.create(new_login)

        return existing_user
