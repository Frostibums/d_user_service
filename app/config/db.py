from pydantic_settings import BaseSettings


class DatabaseConfig(BaseSettings):
    db_url: str = "postgresql+asyncpg://postgres:postgres@auth-db:5432/auth_db"


db_settings = DatabaseConfig()
