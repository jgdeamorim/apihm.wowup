from fastapi import FastAPI
from api.api_routes import router as api_router
from database import init_db
from database.connection import get_engine

app = FastAPI(title="HubMercado API", version="1.26")

# Criar tabelas no banco de dados
init_db(get_engine())

# Incluir as rotas da API
app.include_router(api_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True, workers=1)
