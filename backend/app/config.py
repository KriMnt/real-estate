# backend/app/config.py
from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    # Updated for MySQL
    DATABASE_URL: str = "mysql+mysqlconnector://root:your_password@localhost/real_estate_db"
    REDIS_URL: str = "redis://localhost"
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Real Estate Aggregator"
    
    # Image storage settings
    IMAGES_STORE_PATH: str = "images"
    MAX_IMAGE_SIZE: int = 10485760  # 10MB
    
    # External API settings
    API_TIMEOUT: int = 30
    API_RATE_LIMIT: int = 100

    class Config:
        env_file = ".env"

@lru_cache()
def get_settings():
    return Settings()
