from datetime import datetime

from pydantic import BaseModel, EmailStr, ConfigDict


class CreateUserRequest(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    email: EmailStr
    username: str | None = None
    password: str


class LoginUserRequest(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    username: str
    password: str


class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    email: EmailStr
    username: str | None
    is_active: bool
    is_verified: bool
    role: str
    created_at: datetime
    updated_at: datetime
    last_login_at: datetime | None
    failed_login_attempts: int
    locked_until: datetime | None
