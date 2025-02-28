from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from config.settings import settings

# Criar conexão com PostgreSQL com Pooling
engine = create_async_engine(settings.DATABASE_URL, echo=True, pool_size=5, max_overflow=10)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, class_=AsyncSession)
Base = declarative_base()

# Dependência do banco para FastAPI
async def get_db():
    async with SessionLocal() as db:
        yield db
