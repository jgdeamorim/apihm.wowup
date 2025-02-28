from fastapi import APIRouter
from api.v1 import admin, bling, clientes, mercadolivre, openai, produtos, status

router = APIRouter()

router.include_router(admin.router)
router.include_router(bling.router)
router.include_router(clientes.router)
router.include_router(mercadolivre.router)
router.include_router(openai.router)
router.include_router(produtos.router)
router.include_router(status.router)
