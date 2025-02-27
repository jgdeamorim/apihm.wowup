from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database.connection import get_db
from services.ncm_service import obter_ncm

router = APIRouter(prefix="/ncm", tags=["NCM"])

@router.get("/{gtin}")
def buscar_ncm(gtin: str, descricao: str, db: Session = Depends(get_db)):
    """Busca o código NCM de um produto e o salva no banco se ainda não existir"""
    return {"gtin": gtin, "descricao": descricao, "ncm": obter_ncm(db, gtin, descricao)}
