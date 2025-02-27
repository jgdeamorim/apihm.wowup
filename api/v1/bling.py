from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database.connection import get_db
from services.bling_service import buscar_produtos_bling, atualizar_produto_no_bling
from database.models import Produto

router = APIRouter(prefix="/bling", tags=["Bling"])

@router.get("/produtos")
def listar_produtos_bling():
    """Busca todos os produtos cadastrados no Bling"""
    produtos = buscar_produtos_bling()
    if not produtos:
        raise HTTPException(status_code=404, detail="Nenhum produto encontrado no Bling")
    return produtos

@router.post("/atualizar/{produto_id}")
def atualizar_produto_bling(produto_id: int, db: Session = Depends(get_db)):
    """Atualiza um produto específico no Bling"""
    produto = db.query(Produto).filter(Produto.id == produto_id).first()
    if not produto:
        raise HTTPException(status_code=404, detail="Produto não encontrado")

    atualizar_produto_no_bling(produto)
    produto.status = "atualizado"
    db.commit()
    return {"message": f"Produto {produto_id} atualizado no Bling com sucesso!"}
