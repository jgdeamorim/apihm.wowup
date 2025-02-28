# Inicialização do pacote API v1
from fastapi import APIRouter

router = APIRouter()

from .admin import router as admin_router
from .clientes import router as clientes_router
from .mercadolivre import router as mercadolivre_router
from .bling import router as bling_router
from .produtos import router as produtos_router
from .openai import router as openai_router
from .status import router as status_router
from .ncm import router as ncm_router

router.include_router(admin_router)
router.include_router(clientes_router)
router.include_router(mercadolivre_router)
router.include_router(bling_router)
router.include_router(produtos_router)
router.include_router(openai_router)
router.include_router(status_router)
router.include_router(ncm_router)
