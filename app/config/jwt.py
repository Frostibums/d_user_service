from pydantic_settings import BaseSettings


class JWTConfig(BaseSettings):
    secret: str = "super-secret"
    algorithm: str = "HS256"
    exp_minutes: int = 60


jwt_settings = JWTConfig()
