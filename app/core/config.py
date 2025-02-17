from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Основные настройки приложения
    PROJECT_NAME: str = "Referral System API"
    VERSION: str = "1.0.0"
    DESCRIPTION: str = "RESTful API для реферальной системы."

    # Настройки безопасности
    SECRET_KEY: str
    ALGORITHM: str = "HS256"  # Значение по умолчанию
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30  # Значение по умолчанию

    # Настройки базы данных
    DATABASE_URL: str

    # Настройки Redis (для кеширования)
    REDIS_URL: str = "redis://localhost:6379"  # Значение по умолчанию

    # Настройки внешних сервисов
    CLEARBIT_API_KEY: str
    EMAILHUNTER_API_KEY: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()