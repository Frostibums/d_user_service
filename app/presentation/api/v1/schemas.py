import datetime
from uuid import UUID

from pydantic import BaseModel, EmailStr

from app.domain.enums.role import Role


class BaseInput(BaseModel):
    email: EmailStr
    password: str


class RegisterInput(BaseInput):
    ...


class LoginInput(BaseInput):
    ...


class UserOutput(BaseModel):
    id: UUID
    email: EmailStr
    role: Role
    is_active: bool
    created_at: datetime.datetime


class TokenOutput(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user_id: UUID
    role: Role | None = None

