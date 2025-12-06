from sqlalchemy.orm import Session
from src.api.repositories.users import UsersRepository

from src.db.models.users import Users
from src.db.schemas.users import CreateUserRequest, UserResponse


class UsersService:

    @staticmethod
    def create_user(db: Session, data: CreateUserRequest) -> Users:
        user = Users(
            email=data.email,
            username=data.username,
            password_hash=data.password_hash
        )
        db_user = UsersRepository.create(db, user)
        return UserResponse.model_validate(db_user)