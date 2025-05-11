from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from starlette.requests import Request

from app.domain.dto.user import User
from app.domain.enums.role import Role
from app.infrastructure.bus.kafka.producer import KafkaEventProducer
from app.infrastructure.db.repository import SQLAlchemyUserRepository
from app.infrastructure.db.session import get_session
from app.infrastructure.security import decode_jwt_token
from app.service.auth import AuthService
from app.service.interfaces import IUserRepository
from app.service.user import UserService


def get_kafka_producer(request: Request) -> KafkaEventProducer:
    return request.app.state.kafka_producer


def get_user_repo(session: AsyncSession = Depends(get_session)):
    return SQLAlchemyUserRepository(session=session)


def get_user_service(user_repo: IUserRepository = Depends(get_user_repo)):
    return UserService(user_repo=user_repo)


def get_auth_service(
        user_repo: IUserRepository = Depends(get_user_repo),
        producer=Depends(get_kafka_producer),
):
    return AuthService(user_repo=user_repo, producer=producer)


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


async def get_current_user(
        token: str = Depends(oauth2_scheme),
        user_service=Depends(get_user_service),
) -> User:
    try:
        payload = decode_jwt_token(token)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    current_user = await user_service.get_by_id(payload.get("sub"))
    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User not found",
        )
    return current_user


async def get_current_admin_user(user: User = Depends(get_current_user)):
    if user.role == Role.admin.value:
        return user
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Insufficient privileges",
    )
