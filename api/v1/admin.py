from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database.connection import get_db
from database.models import Produto
from database.schemas import ProdutoSchema
from services.bling_service import atualizar_produto_no_bling

router = APIRouter(prefix="/admin", tags=["Admin"])

@router.get("/produtos_pendentes", response_model=list[ProdutoSchema])
def listar_produtos_pendentes(db: Session = Depends(get_db)):
    """Lista produtos pendentes de aprovação pelo admin"""
    produtos = db.query(Produto).filter(Produto.status == "pendente").all()
    return produtos

@router.put("/aprovar/{produto_id}")
def aprovar_produto(produto_id: int, db: Session = Depends(get_db)):
    """Admin aprova um produto para ser atualizado no Bling"""
    produto = db.query(Produto).filter(Produto.id == produto_id, Produto.status == "pendente").first()
    if not produto:
        raise HTTPException(status_code=404, detail="Produto não encontrado ou já aprovado")

    produto.status = "pronto"
    db.commit()
    return {"message": "Produto aprovado com sucesso!"}

@router.post("/atualizar_bling")
def atualizar_bling(db: Session = Depends(get_db)):
    """Envia produtos aprovados para o Bling"""
    produtos = db.query(Produto).filter(Produto.status == "pronto").all()
    if not produtos:
        raise HTTPException(status_code=400, detail="Nenhum produto pronto para atualização")

    for produto in produtos:
        atualizar_produto_no_bling(produto)
        produto.status = "atualizado"
    
    db.commit()
    return {"message": "Produtos atualizados no Bling com sucesso!"}
