from fastapi import APIRouter, status, Depends

from src.api.services.users import UsersService
from src.api.repositories.users import UsersRepository

from src.db.schemas.user import CreateUserRequest, UserResponse
from src.db.utils.sql_alchemy import get_session


router = APIRouter(
    prefix="/users",
    tags=[
        "users"
    ],
    dependencies=[
        Depends(get_session)
    ]
)


@router.post(
    path="/",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    tags=[
        "users"
    ],
    dependencies=[

    ],
    summary="Create a new user",
    description="Create a new user into the database with all the information"
)
async def create_user(
    data: CreateUserRequest,
    session=Depends(get_session)
):
    user_service = UsersService(UsersRepository())
    return user_service.create_user(session, data)