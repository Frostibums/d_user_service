from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from starlette import status
from starlette.responses import Response

from app.infrastructure.security import decode_jwt_token
from app.presentation.api.v1.dependencies import (
    get_auth_service,
    get_current_admin_id,
    get_current_user_id,
    get_user_service,
)
from app.presentation.api.v1.interfaces import IAuthService
from app.presentation.api.v1.schemas import (
    RegisterInput,
    TokenOutput,
    UserOutput,
)
from app.service.user import UserService

router = APIRouter()


@router.get("/me", response_model=UserOutput)
async def get_current_user(
        user_id: UUID = Depends(get_current_user_id),
        user_service: UserService = Depends(get_user_service),
):
    return await user_service.get_by_id(user_id)


@router.post(
    "/register",
    status_code=status.HTTP_201_CREATED,
    response_model=UserOutput,
    dependencies=[Depends(get_current_admin_id)],
)
async def register(
        data: RegisterInput,
        service: IAuthService = Depends(get_auth_service),
):
    try:
        user = await service.register_user(
            email=str(data.email),
            password=data.password,
            role=data.role,
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return user


@router.post(
    "/login",
    status_code=status.HTTP_200_OK,
    response_model=TokenOutput,
)
async def login(
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
        response: Response,
        service: IAuthService = Depends(get_auth_service),
):
    try:
        token = await service.login_user(
            email=str(form_data.username),
            password=form_data.password,
        )
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))
    payload = decode_jwt_token(token)
    token = TokenOutput(
        access_token=token,
        token_type="bearer",
        user_id=payload["sub"],
        role=payload["role"],
    )
    response.set_cookie(
        key="access_token",
        value=f"Bearer {token.access_token}",
        httponly=True,
    )
    return token
