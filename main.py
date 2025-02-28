from fastapi import FastAPI
from api.v1 import admin, bling, clientes, mercadolivre, openai, produtos, status
from database import init_db
from database.connection import get_engine

app = FastAPI()

# Criar tabelas no banco de dados
init_db(get_engine())

# Incluir routers
app.include_router(admin.router)
app.include_router(bling.router)
app.include_router(clientes.router)
app.include_router(mercadolivre.router)
app.include_router(openai.router)
app.include_router(produtos.router)
app.include_router(status.router)
