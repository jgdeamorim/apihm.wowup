from fastapi import APIRouter
from api.v1 import admin, clientes, mercadolivre, bling, produtos, openai, status, ncm

router = APIRouter()

# Incluindo os roteadores de cada módulo
router.include_router(admin.router, prefix="/admin", tags=["Admin"])
router.include_router(clientes.router, prefix="/clientes", tags=["Clientes"])
router.include_router(mercadolivre.router, prefix="/mercadolivre", tags=["Mercado Livre"])
router.include_router(bling.router, prefix="/bling", tags=["Bling"])
router.include_router(produtos.router, prefix="/produtos", tags=["Produtos"])
router.include_router(openai.router, prefix="/openai", tags=["OpenAI"])
router.include_router(status.router, prefix="/status", tags=["Status"])
router.include_router(ncm.router, prefix="/ncm", tags=["NCM"])
