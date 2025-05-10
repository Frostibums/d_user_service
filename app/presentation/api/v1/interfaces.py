from typing import Protocol

from app.domain.dto.user import User
from app.domain.enums.role import Role


class IAuthService(Protocol):
    async def register_user(
            self,
            email: str,
            password: str,
            role: Role,
    ) -> User:
        ...

    async def login_user(self, email: str, password: str) -> str:
        ...
