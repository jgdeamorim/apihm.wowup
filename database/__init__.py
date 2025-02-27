from .connection import SessionLocal, engine
from .models import Base

# Criar tabelas no banco de dados
def init_db():
    Base.metadata.create_all(bind=engine)