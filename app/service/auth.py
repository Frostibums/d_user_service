from datetime import datetime, timezone
from uuid import uuid4

from app.domain.dto.user import User
from app.domain.enums.role import Role
from app.infrastructure.security import create_jwt_token
from app.service.interfaces import IUserRepository
from app.utils.password import hash_password, verify_password


class AuthService:
    def __init__(self, user_repo: IUserRepository):
        self.user_repo = user_repo

    async def register_user(
            self,
            email: str,
            password: str,
            role: Role,
    ) -> User:
        existing = await self.user_repo.get_by_email(email)
        if existing:
            raise ValueError("User already exists")

        user = User(
            id=uuid4(),
            email=email,
            hashed_password=hash_password(password),
            role=role,
            is_active=True,
            created_at=datetime.now(timezone.utc),
        )
        await self.user_repo.save(user)
        return user

    async def login_user(self, email: str, password: str) -> str:
        user = await self.user_repo.get_by_email(email)
        if not user or not verify_password(password, user.hashed_password):
            raise ValueError("Invalid credentials")
        return create_jwt_token(user.id, user.role)
