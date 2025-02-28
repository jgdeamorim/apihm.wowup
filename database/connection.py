from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from config.settings import settings

# Ajustando a URL do Banco de Dados para o formato assíncrono correto
DATABASE_URL = settings.DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://")

# Criar conexão assíncrona com PostgreSQL
engine = create_async_engine(DATABASE_URL, echo=True)

# Criar sessão assíncrona
SessionLocal = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

Base = declarative_base()

# Dependência do banco para FastAPI
async def get_db():
    async with SessionLocal() as session:
        yield session
