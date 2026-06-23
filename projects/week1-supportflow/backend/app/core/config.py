from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql+asyncpg://user:password@localhost:5432/supportflow"
    PROJECT_NAME: str = "SupportFlow"
    VERSION: str = "0.1.0"

    class Config:
        env_file = ".env"
        extra = "ignore"


settings = Settings()
