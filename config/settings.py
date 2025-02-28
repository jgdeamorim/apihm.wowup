from pydantic_settings import BaseSettings
from dotenv import load_dotenv
import os

# 🔄 Carregar variáveis do .env
load_dotenv()

class Settings(BaseSettings):
    """Configurações principais do sistema"""

    # 📦 Banco de Dados
    DATABASE_URL: str = os.getenv("DATABASE_URL")
    if not DATABASE_URL:
        raise ValueError("⚠️ DATABASE_URL não foi definida no ambiente!")

    # 🔗 APIs Externas
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY")
    BLING_API_KEY: str = os.getenv("BLING_API_KEY")
    ML_CLIENT_ID: str = os.getenv("ML_CLIENT_ID")
    ML_CLIENT_SECRET: str = os.getenv("ML_CLIENT_SECRET")
    ML_REDIRECT_URI: str = os.getenv("ML_REDIRECT_URI")

    # ⚡ Redis e Celery
    REDIS_URL: str = os.getenv("REDIS_URL")
    CELERY_BROKER_URL: str = os.getenv("CELERY_BROKER_URL", REDIS_URL)
    CELERY_RESULT_BACKEND: str = os.getenv("CELERY_RESULT_BACKEND", REDIS_URL)
    
    if not REDIS_URL:
        raise ValueError("⚠️ REDIS_URL não foi definida no ambiente!")

    # 🔐 Segurança
    SECRET_KEY: str = os.getenv("SECRET_KEY")
    if not SECRET_KEY:
        raise ValueError("⚠️ SECRET_KEY não foi definida no ambiente!")

    JWT_ALGORITHM: str = os.getenv("JWT_ALGORITHM", "HS256")
    JWT_EXPIRATION_MINUTES: int = int(os.getenv("JWT_EXPIRATION_MINUTES", 60))

    class Config:
        """Configurações adicionais do Pydantic"""
        case_sensitive = True

# 🔥 Inicializa as configurações carregadas do ambiente
settings = Settings()
