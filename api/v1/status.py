from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database.connection import get_db
from database.models import Produto
from database.schemas import ProdutoSchema

router = APIRouter(prefix="/status", tags=["Status"])

@router.get("/produtos", response_model=list[ProdutoSchema])
def status_produtos(db: Session = Depends(get_db)):
    """Lista todos os produtos e seus status"""
    return db.query(Produto).all()

@router.get("/produtos/pendentes", response_model=list[ProdutoSchema])
def produtos_pendentes(db: Session = Depends(get_db)):
    """Lista produtos pendentes de refinamento ou atualização"""
    return db.query(Produto).filter(Produto.status == "pendente").all()

@router.get("/produtos/prontos", response_model=list[ProdutoSchema])
def produtos_prontos(db: Session = Depends(get_db)):
    """Lista produtos que estão prontos para atualização no Bling"""
    return db.query(Produto).filter(Produto.status == "pronto").all()

@router.get("/produtos/atualizados", response_model=list[ProdutoSchema])
def produtos_atualizados(db: Session = Depends(get_db)):
    """Lista produtos que já foram atualizados no Bling"""
    return db.query(Produto).filter(Produto.status == "atualizado").all()
