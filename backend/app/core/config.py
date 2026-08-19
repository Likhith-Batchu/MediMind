"""
Central application configuration.

All environment-dependent values (DB credentials, secrets, ports) come
from environment variables. NEVER hard-code secrets here.
Pydantic's BaseSettings automatically reads from the environment / .env file.
"""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # App
    APP_NAME: str = "MediMind AI"
    ENV: str = "development"
    DEBUG: bool = True

    # Database
    DATABASE_URL: str = "postgresql://medimind:medimind@localhost:5432/medimind_db"

    # Auth (placeholder for Phase 1 — not used yet in Phase 0)
    JWT_SECRET_KEY: str = "change-me-in-env-file"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # CORS
    FRONTEND_ORIGIN: str = "http://localhost:3000"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
