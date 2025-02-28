import uvicorn
import os
from fastapi import FastAPI
from api.api_routes import router as api_router
from database import init_db
from database.connection import get_engine

app = FastAPI()

# Criar tabelas no banco de dados
init_db(get_engine())

# Incluir routers
app.include_router(api_router)

# Pegando a porta correta do Railway
PORT = int(os.getenv("PORT", 8000))

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=PORT, reload=True)
