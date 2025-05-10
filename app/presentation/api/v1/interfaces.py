from typing import Protocol

from app.domain.dto.user import User


class IAuthService(Protocol):
    async def register_user(self, email: str, password: str) -> User:
        ...

    async def login_user(self, email: str, password: str) -> str:
        ...
