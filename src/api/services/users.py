from sqlalchemy.orm import Session
from src.api.repositories.users import UsersRepository

from src.db.models.users import Users
from src.db.schemas.user import CreateUserRequest


class UsersService:

    def __init__(
        self,
        repository: UsersRepository
    ):
        self.repository = repository

    def create_user(
        self,
        session: Session,
        user: CreateUserRequest
    ) -> Users:
        
        # TODO: Hash password before creating user.
        hashed_password = user.password

        new_user = Users(
            email=user.email,
            username=user.username,
            password_hash=hashed_password
        )
        
        return self.repository.create(
            session, new_user
        )
