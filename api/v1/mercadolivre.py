from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from services.mercadolivre_service import buscar_produto_mercadolivre, buscar_produto_por_gtin
from database.connection import get_db
from database.models import Produto
from database.schemas import ProdutoSchema

router = APIRouter(prefix="/mercadolivre", tags=["Mercado Livre"])

@router.get("/produto/{produto_nome}")
def obter_produto_mercadolivre(produto_nome: str):
    """Obtém dados do produto pelo nome na API do Mercado Livre"""
    produto = buscar_produto_mercadolivre(produto_nome)
    if not produto:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    return produto

@router.get("/gtin/{gtin}")
def obter_produto_por_gtin(gtin: str):
    """Obtém dados do produto pelo código GTIN"""
    produto = buscar_produto_por_gtin(gtin)
    if not produto:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    return produto

@router.post("/importar/{produto_nome}", response_model=ProdutoSchema)
def importar_produto_mercadolivre(produto_nome: str, db: Session = Depends(get_db)):
    """Importa um produto do Mercado Livre para o banco de dados"""
    produto_ml = buscar_produto_mercadolivre(produto_nome)
    if not produto_ml:
        raise HTTPException(status_code=404, detail="Produto não encontrado")

    novo_produto = Produto(
        nome=produto_ml["nome"],
        gtin=produto_ml.get("gtin"),
        categoria=produto_ml.get("categoria"),
        preco=produto_ml.get("preco"),
        imagem=produto_ml.get("imagem"),
        status="pendente"
    )
    db.add(novo_produto)
    db.commit()
    db.refresh(novo_produto)
    return novo_produto
