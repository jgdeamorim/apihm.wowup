import requests
import os
from database.connection import SessionLocal
from database.models import Produto
from sqlalchemy.orm import Session

ML_ACCESS_TOKEN = os.getenv("ML_ACCESS_TOKEN")

def buscar_produto_mercadolivre(produto_nome: str):
    """Busca informações do produto no Mercado Livre pelo nome"""
    url = f"https://api.mercadolibre.com/sites/MLB/search?q={produto_nome}&limit=1"
    headers = {"Authorization": f"Bearer {ML_ACCESS_TOKEN}"}
    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200 and response.json().get("results"):
        produto = response.json()["results"][0]
        return {
            "id": produto["id"],
            "nome": produto["title"],
            "gtin": produto.get("catalog_product_id"),
            "preco": produto["price"],
            "imagem": produto["thumbnail"]
        }
    return None

def buscar_produto_por_gtin(gtin: str):
    """Busca informações detalhadas do produto pelo GTIN no Mercado Livre"""
    url = f"https://api.mercadolibre.com/catalog_items/{gtin}"
    headers = {"Authorization": f"Bearer {ML_ACCESS_TOKEN}"}

    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        produto = response.json()
        return {
            "nome": produto["title"],
            "marca": produto.get("brand"),
            "dimensoes": produto.get("dimensions"),
            "peso": produto.get("weight"),
            "categoria": produto["category_id"]
        }
    return None

def salvar_produto_no_banco(produto: dict, db: Session = SessionLocal()):
    """Salva ou atualiza um produto no banco de dados"""
    db_produto = db.query(Produto).filter(Produto.gtin == produto["gtin"]).first()
    
    if not db_produto:
        novo_produto = Produto(
            nome=produto["nome"],
            gtin=produto["gtin"],
            categoria=produto.get("categoria"),
            marca=produto.get("marca"),
            peso=produto.get("peso"),
            dimensoes=produto.get("dimensoes"),
            imagem_url=produto.get("imagem"),
            status="pendente"
        )
        db.add(novo_produto)
        db.commit()
        return novo_produto
    return db_produto
