from sqlalchemy.orm import Session
from database.models import Produto
from services.mercadolivre_service import obter_produto_por_gtin
from services.openai_service import refinar_dados_com_ia

def validar_produto(produto: dict):
    """Valida se o produto tem todas as informações obrigatórias"""
    campos_obrigatorios = ["nome", "categoria", "marca", "peso_bruto", "peso_liquido", "dimensoes", "gtin"]
    
    for campo in campos_obrigatorios:
        if not produto.get(campo):
            return False
    return True

def processar_produto(produto_id: int, db: Session):
    """Processa e refina um produto antes da atualização no Bling"""
    produto = db.query(Produto).filter(Produto.id == produto_id).first()
    
    if not produto:
        return {"status": "erro", "mensagem": "Produto não encontrado"}
    
    if not produto.gtin:
        return {"status": "erro", "mensagem": "Produto sem GTIN"}

    # Buscar dados do Mercado Livre pelo GTIN
    dados_ml = obter_produto_por_gtin(produto.gtin)
    
    if dados_ml:
        produto.categoria = dados_ml.get("categoria", produto.categoria)
        produto.marca = dados_ml.get("marca", produto.marca)
        produto.dimensoes = dados_ml.get("dimensoes", produto.dimensoes)
        produto.peso_bruto = dados_ml.get("peso", produto.peso_bruto)
    
    # Refinar dados com OpenAI
    if not validar_produto(vars(produto)):
        descricao = refinar_dados_com_ia(vars(produto))
        produto.descricao = descricao
    
    db.commit()
    
    return {"status": "sucesso", "mensagem": "Produto processado e pronto para atualização"}
