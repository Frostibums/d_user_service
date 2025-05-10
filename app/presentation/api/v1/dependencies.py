from uuid import UUID

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from app.infrastructure.db.repository import SQLAlchemyUserRepository
from app.infrastructure.db.session import get_session
from app.infrastructure.security import decode_jwt_token
from app.service.auth import AuthService
from app.service.interfaces import IUserRepository


def get_user_repo(session: AsyncSession = Depends(get_session)):
    return SQLAlchemyUserRepository(session=session)


def get_auth_service(user_repo: IUserRepository = Depends(get_user_repo)):
    return AuthService(user_repo=user_repo)


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")


def get_current_user_id(token: str = Depends(oauth2_scheme)) -> UUID:
    try:
        payload = decode_jwt_token(token)
        return UUID(payload["sub"])
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )
