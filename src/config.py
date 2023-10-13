from pydantic_settings import BaseSettings


class Config(BaseSettings):
    POSTGRES_USERNAME: str = 'postgres'
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str = 'postgres'
    POSTGRES_HOST: str = 'localhost'
    POSTGRES_PORT: int = 5432

    class Config:
        env_prefix = 'APP_'


config = Config()
