from uuid import UUID

from app.domain.dto.user import User
from app.service.interfaces import IUserRepository


class UserService:
    def __init__(self, user_repo: IUserRepository):
        self.user_repo = user_repo

    async def get_by_id(self, user_id: UUID) -> User | None:
        return await self.user_repo.get_by_id(user_id)
