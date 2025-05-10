from datetime import datetime, timedelta
from uuid import UUID

import jwt

from app.config.jwt import jwt_settings


def create_jwt_token(user_id: UUID, role: str) -> str:
    payload = {
        "sub": str(user_id),
        "role": role,
        "exp": datetime.utcnow() + timedelta(minutes=jwt_settings.exp_minutes),
        "iat": datetime.utcnow(),
    }
    return jwt.encode(
        payload,
        jwt_settings.secret,
        algorithm=jwt_settings.algorithm,
    )


def decode_jwt_token(token: str) -> dict:
    return jwt.decode(
        token,
        jwt_settings.secret,
        algorithms=[jwt_settings.algorithm],
    )
