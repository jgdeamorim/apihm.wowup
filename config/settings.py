import os
from pydantic import BaseSettings
from dotenv import load_dotenv

load_dotenv()  # Carrega variáveis de ambiente do .env

class Settings(BaseSettings):
    """Configurações Gerais do HubMercado"""

    PROJECT_NAME: str = "HubMercado"
    API_VERSION: str = "1.26"

    # ✅ Configuração do Banco de Dados PostgreSQL
    DB_USER: str = os.getenv("DB_USER", "user")
    DB_PASSWORD: str = os.getenv("DB_PASSWORD", "password")
    DB_HOST: str = os.getenv("DB_HOST", "localhost")
    DB_PORT: int = int(os.getenv("DB_PORT", 5432))
    DB_NAME: str = os.getenv("DB_NAME", "hubmercado")
    DATABASE_URL: str = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

    # ✅ Configuração do Redis (Cache e Celery)
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379/0")

    # ✅ OpenAI (Uso Global para IA)
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY")

    # ✅ Multi-clientes → Credenciais do Bling e Mercado Livre
    CLIENTES_ATIVOS: list = os.getenv("CLIENTES_ATIVOS", "").split(",")  # Lista separada por vírgula

    MERCADOLIVRE_CREDENTIALS = {
        cliente: {
            "CLIENT_ID": os.getenv(f"{cliente}_ML_CLIENT_ID"),
            "CLIENT_SECRET": os.getenv(f"{cliente}_ML_CLIENT_SECRET"),
            "ACCESS_TOKEN": os.getenv(f"{cliente}_ML_ACCESS_TOKEN"),
            "REFRESH_TOKEN": os.getenv(f"{cliente}_ML_REFRESH_TOKEN"),
        }
        for cliente in CLIENTES_ATIVOS
    }

    BLING_CREDENTIALS = {
        cliente: os.getenv(f"{cliente}_BLING_API_KEY")
        for cliente in CLIENTES_ATIVOS
    }

    # ✅ Segurança → Configuração do Token JWT
    JWT_SECRET_KEY: str = os.getenv("JWT_SECRET_KEY", "supersecret")
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRE_MINUTES: int = 60 * 24  # 24 horas

    class Config:
        case_sensitive = True  # Sensível a maiúsculas/minúsculas

settings = Settings()
