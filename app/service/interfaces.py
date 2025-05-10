from typing import Protocol
from uuid import UUID

from app.domain.dto.user import User


class IUserRepository(Protocol):
    async def get_by_email(self, email: str) -> User | None:
        ...

    async def get_by_id(self, user_id: UUID) -> User | None:
        ...

    async def save(self, date: User) -> None:
        ...
