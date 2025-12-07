from fastapi import APIRouter, status, Depends

from src.main import session_manager

from src.api.services.users import UsersService
from src.db.schemas.user import CreateUserRequest, UserResponse

from sqlalchemy.ext.asyncio import AsyncSession


router: APIRouter = APIRouter(
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
    return await UsersService(session).create_user(new_user)