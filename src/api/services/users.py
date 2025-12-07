from sqlalchemy.ext.asyncio import AsyncSession

from src.api.repositories.users import UsersRepository

from src.db.models.users import Users
from src.db.schemas.user import CreateUserRequest


class UsersService:

    def __init__(self, session: AsyncSession):
        self.repository = UsersRepository(session)

    def create_user(self, user: CreateUserRequest) -> Users:
        
        # TODO: Hash password before creating user.
        hashed_password = user.password

        new_user = Users(
            email=user.email,
            username=user.username,
            password_hash=hashed_password
        )
        
        return self.repository.create(new_user)
