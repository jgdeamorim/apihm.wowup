import os
from pydantic import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "HubMercado"
    API_VERSION: str = "1.26"

    # Configuração do banco de dados
    DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql://postgres:GLYMJODznGycGYYfCjHrSfQHOoxCBjDQ@mainline.proxy.rlwy.net:28010/railway")

    # Configuração do Redis para filas assíncronas (Celery)
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379/0")

    # Configurações das APIs externas
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY")
    BLING_API_KEY: str = os.getenv("BLING_API_KEY")
    MERCADOLIVRE_CLIENT_ID: str = os.getenv("MERCADOLIVRE_CLIENT_ID")
    MERCADOLIVRE_CLIENT_SECRET: str = os.getenv("MERCADOLIVRE_CLIENT_SECRET")

    # Configuração do Token JWT
    JWT_SECRET_KEY: str = os.getenv("JWT_SECRET_KEY", "supersecret")
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRE_MINUTES: int = 60 * 24

    class Config:
        case_sensitive = True

settings = Settings()
