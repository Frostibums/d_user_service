from uuid import UUID

from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from starlette.requests import Request

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


def get_jwt_payload(request: Request) -> dict:
    token = request.cookies.get("access_token")
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing access token",
        )

    if token.startswith("Bearer "):
        token = token[7:]
    try:
        return decode_jwt_token(token)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid or expired token{e}",
        )


def get_current_teacher_id(payload: dict = Depends(get_jwt_payload)) -> UUID:
    if payload.get("role") not in (Role.teacher.value, Role.admin.value):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only for stuff"
        )
    return UUID(payload["sub"])


def get_current_user_id(payload: dict = Depends(get_jwt_payload)) -> UUID:
    return UUID(payload["sub"])


def get_current_admin_id(payload: dict = Depends(get_jwt_payload)) -> UUID:
    if payload.get("role") != Role.admin.value:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only for stuff"
        )
    return UUID(payload["sub"])
