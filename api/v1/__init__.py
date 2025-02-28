from fastapi import APIRouter

# Criação do roteador principal
router = APIRouter(prefix="/api/v1")

# Importação dos módulos da API
from .admin import router as admin_router
from .bling import router as bling_router
from .clientes import router as clientes_router
from .mercadolivre import router as mercadolivre_router
from .openai import router as openai_router
from .produtos import router as produtos_router
from .status import router as status_router

# Inclusão dos sub-roteadores na API principal
router.include_router(admin_router, prefix="/admin", tags=["Admin"])
router.include_router(bling_router, prefix="/bling", tags=["Bling"])
router.include_router(clientes_router, prefix="/clientes", tags=["Clientes"])
router.include_router(mercadolivre_router, prefix="/mercadolivre", tags=["Mercado Livre"])
router.include_router(openai_router, prefix="/openai", tags=["OpenAI"])
router.include_router(produtos_router, prefix="/produtos", tags=["Produtos"])
router.include_router(status_router, prefix="/status", tags=["Status"])
