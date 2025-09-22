from pydantic import BaseModel, field_validator
from typing import List
import os
class Settings(BaseModel):
    DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql+psycopg://postgres:postgres@db:5432/app")
    API_LOG_LEVEL: str = os.getenv("API_LOG_LEVEL", "INFO")
    CORS_ORIGINS: List[str] = []
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "local")
    SENTRY_DSN: str | None = os.getenv("SENTRY_DSN")
    OTEL_EXPORTER_OTLP_ENDPOINT: str | None = os.getenv("OTEL_EXPORTER_OTLP_ENDPOINT")
    OTEL_SERVICE_NAME: str = os.getenv("OTEL_SERVICE_NAME", "users-api")
    @field_validator("CORS_ORIGINS", mode="before")
    @classmethod
    def split_origins(cls, v):
        if isinstance(v, list): return v
        if v: return [s.strip() for s in str(v).split(",")]
        return ["http://localhost:5173", "http://localhost:8080"]
settings = Settings()
