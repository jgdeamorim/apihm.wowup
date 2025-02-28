from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from config.settings import settings

Base = declarative_base()

def get_engine():
    """Retorna uma instância do engine configurado"""
    return create_engine(settings.DATABASE_URL, echo=True)

engine = get_engine()

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dependência do banco para FastAPI
def get_db():
    """Cria uma sessão do banco de dados"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
