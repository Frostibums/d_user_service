import logging
from datetime import datetime, timedelta, timezone
from uuid import UUID

import jwt

from app.config.jwt import jwt_settings


def create_jwt_token(user_id: UUID, role: str) -> str:
    payload = {
        "sub": str(user_id),
        "role": role,
        "exp": datetime.now(
            tz=timezone.utc
        ) + timedelta(
            minutes=jwt_settings.exp_minutes
        ),
        "iat": datetime.now(tz=timezone.utc),
    }
    return jwt.encode(
        payload,
        jwt_settings.private_key,
        algorithm=jwt_settings.algorithm,
    )


def decode_jwt_token(token: str) -> dict:
    return jwt.decode(
        token,
        jwt_settings.public_key,
        algorithms=[jwt_settings.algorithm],
    )
