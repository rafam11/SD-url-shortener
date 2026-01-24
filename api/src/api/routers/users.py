from fastapi import APIRouter, Depends, HTTPException, status

from api.auth.security import create_access_token
from api.core import constants as cons
from api.core.config import Settings, get_settings
from api.core.errors import InvalidCredentialsError
from api.dependencies import get_user_service
from api.schemas.token import TokenResponse
from api.schemas.user import CreateUserRequest, LoginUserRequest, UserResponse
from api.services.users import UserService

router: APIRouter = APIRouter(prefix="/users", tags=["users"])


@router.post(
    path="/",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new user",
    description="Create a new user into the database with all the information",
)
async def create_user(
    new_user: CreateUserRequest, service: UserService = Depends(get_user_service)
):
    return await service.create_user(new_user)


@router.post(
    path="/login/",
    response_model=TokenResponse,
    status_code=status.HTTP_200_OK,
    summary="Authenticate a user and return an access token",
    description="Authenticate a user using their credentials. If valid, the server issues an access token that can be"
    " used to authorize subsequent API requests.",
)
async def login_user(
    user: LoginUserRequest,
    service: UserService = Depends(get_user_service),
    settings: Settings = Depends(get_settings),
):
    try:
        logged_user = await service.login_user(user)
    except InvalidCredentialsError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
            headers={cons.WWW_AUTH_HEADER: cons.BEARER_AUTH},
        )
    access_token = create_access_token(logged_user.id, settings.secret_key)

    return TokenResponse(
        access_token=access_token,
        token_type=cons.BEARER_AUTH.lower(),
        expires_in=3600 * cons.DEFAULT_EXPIRE_JWT_TOKEN,
    )
