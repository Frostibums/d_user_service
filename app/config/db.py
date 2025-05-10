from pydantic_settings import BaseSettings


class DatabaseConfig(BaseSettings):
    db_url: str = "postgresql+asyncpg://user:password@localhost:5432/auth_db"


db_settings = DatabaseConfig()
