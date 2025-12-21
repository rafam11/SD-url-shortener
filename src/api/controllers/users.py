import src.core.constants as cons

from fastapi import APIRouter, Depends, HTTPException, status

from src.api.services.users import UsersService
from src.auth.helpers.security import create_access_token
from src.core.errors import InvalidCredentialsError
from src.db.schemas.token import TokenResponse
from src.db.schemas.user import CreateUserRequest, LoginUserRequest, UserResponse
from src.db.session import session_manager

from sqlalchemy.ext.asyncio import AsyncSession

router: APIRouter = APIRouter(prefix="/users", tags=["users"])


@router.post(
    path="/",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new user",
    description="Create a new user into the database with all the information",
)
async def create_user(
    new_user: CreateUserRequest,
    session: AsyncSession = Depends(session_manager.get_session),
):
    return await UsersService(session).create_user(new_user)


@router.post(
    path="/token/",
    response_model=TokenResponse,
    status_code=status.HTTP_200_OK,
    summary="Authenticate a user and return an access token",
    description="Authenticate a user using their credentials. If valid, the server issues an access token that can be"
    " used to authorize subsequent API requests.",
)
async def login_user(
    user: LoginUserRequest, session: AsyncSession = Depends(session_manager.get_session)
):
    try:
        logged_user = await UsersService(session).login_user(user)
    except InvalidCredentialsError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
            headers={cons.WWW_AUTH_HEADER: cons.BEARER_AUTH},
        )
    access_token = create_access_token(logged_user.id)

    return TokenResponse(
        access_token=access_token,
        token_type=cons.BEARER_AUTH.lower(),
        expires_in=3600 * cons.DEFAULT_EXPIRE_JWT_TOKEN,
    )
