from pydantic import BaseSettings

class Settings(BaseSettings):
    env: str = "dev"
    database_url: str = "postgresql+psycopg://user:pass@localhost:5432/mlv1sion"
    s3_endpoint_url: str | None = None

    class Config:
        env_file = ".env"

settings = Settings()
