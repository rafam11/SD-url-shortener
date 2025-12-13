from fastapi import APIRouter, Depends, HTTPException, status

from src.api.services.users import UsersService
from src.db.schemas.user import CreateUserRequest, LoginUserRequest, UserResponse
from src.db.session import session_manager

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

@router.post(
    path="/token",
    response_model=UserResponse,
)
async def login_user(
    user: LoginUserRequest,
    session: AsyncSession = Depends(session_manager.get_session)
):
    result = await UsersService(session).login_user(user)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password"
        )
    return result