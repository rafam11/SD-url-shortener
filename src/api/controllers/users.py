from fastapi import APIRouter, status, Depends

from src.main import session_manager

from src.api.services.users import UsersService
from src.api.repositories.users import UsersRepository
from src.db.schemas.user import CreateUserRequest, UserResponse

from sqlalchemy.ext.asyncio import AsyncSession


router = APIRouter(
    prefix="/users",
    tags=["users"]
)


@router.post(
    path="/",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new user",
    description="Create a new user into the database with all the information"
)
async def create_user(
    new_user: CreateUserRequest,
    session: AsyncSession = Depends(session_manager.get_session)
):
    return UsersService(session).create_user(new_user)