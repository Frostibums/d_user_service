from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from app.domain.enums.role import Role


@dataclass
class User:
    id: UUID
    email: str
    hashed_password: str
    is_active: bool
    created_at: datetime
    role: Role | None = None
