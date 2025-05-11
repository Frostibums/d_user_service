from pydantic_settings import BaseSettings, SettingsConfigDict


class JWTConfig(BaseSettings):
    private_key: str = "super-secret"
    public_key: str = "not-so-secret"
    algorithm: str = "RS256"
    exp_minutes: int = 60

    model_config = SettingsConfigDict(env_file=".env", env_prefix="jwt_")


jwt_settings = JWTConfig()
