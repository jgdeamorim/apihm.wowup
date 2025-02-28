import uvicorn
from fastapi import FastAPI
from contextlib import asynccontextmanager

from api.api_routes import router
from database.connection import get_engine
from database import init_db
from config.settings import settings

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Executa ações no início e final do ciclo de vida da aplicação."""
    print("🔄 Criando tabelas no banco de dados...")
    init_db(get_engine())  # Inicializa as tabelas na inicialização da API
    yield  # Permite que a aplicação continue rodando
    print("🛑 Encerrando aplicação...")

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.API_VERSION,
    lifespan=lifespan,
)

# ✅ Incluindo todos os routers
app.include_router(router)

# ✅ Prevenindo problemas de multiprocessing no Docker
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True, workers=1)
