from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.dto.user import User
from app.infrastructure.db.models.user import UserORM


class SQLAlchemyUserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_email(self, email: str) -> User | None:
        result = await self.session.execute(
            select(UserORM).where(UserORM.email == email)
        )
        row = result.scalar_one_or_none()
        return row.to_domain() if row else None

    async def get_by_id(self, user_id: UUID) -> User | None:
        result = await self.session.execute(
            select(UserORM).where(UserORM.id == user_id)
        )
        row = result.scalar_one_or_none()
        return row.to_domain() if row else None

    async def save(self, user: User) -> None:
        orm = UserORM.from_domain(user)
        self.session.add(orm)
        # await self.session.commit()
