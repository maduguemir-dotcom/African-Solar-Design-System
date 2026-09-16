from pydantic_settings import BaseSettings
from functools import lru_cache
from typing import Optional
import os

class Settings(BaseSettings):
    APP_NAME: str = "Solar PV Designer Pro Africa"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True
    DATABASE_URL: str = "sqlite:///./solar_pv.db"
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    ADMIN_EMAIL: str = "admin@solarpvdesigner.africa"
    ADMIN_PASSWORD: str = "admin123"
    SOLAR_RESOURCE_API_URL: Optional[str] = None
    STRIPE_SECRET_KEY: Optional[str] = None
    PAYSTACK_SECRET_KEY: Optional[str] = None
    
    class Config:
        env_file = ".env"
        case_sensitive = True

@lru_cache()
def get_settings() -> Settings:
    return Settings()

settings = get_settings()
