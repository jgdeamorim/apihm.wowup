from pydantic_settings import BaseSettings
from dotenv import load_dotenv
import os

# Carregar variáveis do .env
load_dotenv()

class Settings(BaseSettings):
    DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql://postgres:GLYMJODznGycGYYfCjHrSfQHOoxCBjDQ@mainline.proxy.rlwy.net:28010/railway")
    
    # APIs
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    BLING_API_KEY: str = os.getenv("BLING_API_KEY", "")
    ML_CLIENT_ID: str = os.getenv("ML_CLIENT_ID", "")
    ML_CLIENT_SECRET: str = os.getenv("ML_CLIENT_SECRET", "")
    ML_REDIRECT_URI: str = os.getenv("ML_REDIRECT_URI", "")

    # Redis e Celery
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    CELERY_BROKER_URL: str = os.getenv("CELERY_BROKER_URL", REDIS_URL)
    CELERY_RESULT_BACKEND: str = os.getenv("CELERY_RESULT_BACKEND", REDIS_URL)

    # Segurança
    SECRET_KEY: str = os.getenv("SECRET_KEY", "supersecret")
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRATION_MINUTES: int = int(os.getenv("JWT_EXPIRATION_MINUTES", 60))

    class Config:
        case_sensitive = True

settings = Settings()
