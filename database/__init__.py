from .connection import SessionLocal, engine
from .models import Base

# Inicializa as tabelas no banco de dados
def init_db():
    Base.metadata.create_all(bind=engine)

init_db()
