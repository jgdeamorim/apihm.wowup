from fastapi import FastAPI
from api.v1 import admin, bling, clientes, mercadolivre, openai, produtos, status
from config.settings import settings
from config.logger import setup_logger
from config.celery_config import celery_app

app = FastAPI(title="HubMercado API", version="1.26")

# Configuração de Rotas
app.include_router(admin.router, prefix="/api/v1/admin")
app.include_router(bling.router, prefix="/api/v1/bling")
app.include_router(clientes.router, prefix="/api/v1/clientes")
app.include_router(mercadolivre.router, prefix="/api/v1/mercadolivre")
app.include_router(openai.router, prefix="/api/v1/openai")
app.include_router(produtos.router, prefix="/api/v1/produtos")
app.include_router(status.router, prefix="/api/v1/status")

# Configuração de Logs
setup_logger()

@app.get("/")
def root():
    return {"message": "HubMercado API - Versão 1.26"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=settings.HOST, port=settings.PORT)
