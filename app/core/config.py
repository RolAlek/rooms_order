from pydantic import BaseSettings


class Settings(BaseSettings):
    """Класс с настройками FastAPI проекта."""

    app_title: str = 'Бронирование переговорок'
    database_url: str
    secret: str = 'SECRET'

    class Config:

        env_file = '.env'


settings = Settings()
