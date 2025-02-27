from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database.connection import get_db
from services.openai_service import refinar_dados_com_ia
from database.models import Produto
from database.schemas import ProdutoSchema

router = APIRouter(prefix="/openai", tags=["OpenAI"])

@router.post("/refinar/{produto_id}")
def refinar_produto(produto_id: int, db: Session = Depends(get_db)):
    """Refina os dados do produto usando IA antes de enviá-lo ao Bling"""
    produto = db.query(Produto).filter(Produto.id == produto_id).first()
    if not produto:
        raise HTTPException(status_code=404, detail="Produto não encontrado")

    produto_refinado = refinar_dados_com_ia(produto)
    produto.categoria = produto_refinado["categoria"]
    produto.tags = produto_refinado["tags"]
    produto.ncm = produto_refinado["ncm"]
    produto.descricao = produto_refinado["descricao"]
    db.commit()
    
    return {"message": "Produto refinado com sucesso!", "produto": produto_refinado}
