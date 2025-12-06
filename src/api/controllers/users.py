from typing import Annotated
from fastapi import APIRouter, status, Depends
from sqlalchemy.orm import Session

from src.api.services.users import UsersService

from src.db.schemas.users import CreateUserRequest, UserResponse
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
)
def create_user(
    data: CreateUserRequest,
    session=Depends(get_session)
):
    return UsersService.create_user(session, data)