from fastapi import APIRouter, Depends, HTTPException
from starlette import status

from app.infrastructure.security import decode_jwt_token
from app.presentation.api.v1.dependencies import get_auth_service
from app.presentation.api.v1.interfaces import IAuthService
from app.presentation.api.v1.schemas import (
    LoginInput,
    RegisterInput,
    TokenOutput,
    UserOutput,
)

router = APIRouter()


@router.post(
    "/register",
    status_code=status.HTTP_201_CREATED,
    response_model=UserOutput,
)
async def register(
        data: RegisterInput,
        service: IAuthService = Depends(get_auth_service),
):
    try:
        user = await service.register_user(
            email=data.email,
            password=data.password,
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
        data: LoginInput,
        service: IAuthService = Depends(get_auth_service),
):
    try:
        token = await service.login_user(
            email=data.email,
            password=data.password,
        )
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))
    payload = decode_jwt_token(token)
    return TokenOutput(
        access_token=token,
        token_type="bearer",
        user_id=payload["sub"],
        role=payload["role"],
    )
