from fastapi import APIRouter, Depends, HTTPException, status

from src.api.services.users import UsersService
from src.db.schemas.user import CreateUserRequest, LoginUserRequest, UserResponse
from src.db.schemas.token import AccessToken
from src.db.session import session_manager

from src.auth.helpers.jwt_token import JwtToken

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
    path="/token"
)
async def login_user(
    user: LoginUserRequest,
    session: AsyncSession = Depends(session_manager.get_session)
):
    logged_user = await UsersService(session).login_user(user)
    if not logged_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password"
        )
    access_token = JwtToken.create_access_token(logged_user.username)
    return AccessToken(
        token=access_token,
        type="bearer"
    )