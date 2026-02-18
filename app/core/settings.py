from pydantic_settings import BaseSettings
from app.core.environment import Environment

class Settings(BaseSettings):
    app_env: Environment = Environment.DEV
    debug: bool = True

    class Config:
        env_file = ".env"

settings = Settings()
