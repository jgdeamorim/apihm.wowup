import requests
from config.settings import settings

BLING_URL = "https://bling.com.br/Api/v3"

def atualizar_produto_no_bling(produto_id: int, dados: dict):
    """Atualiza um produto na API do Bling"""
    url = f"{BLING_URL}/produtos/{produto_id}"
    headers = {
        "Authorization": f"Bearer {settings.BLING_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "tipo": "variado",
        "categoria": dados['categoria'],
        "marca": dados['marca'],
        "peso_bruto": dados['peso_bruto'],
        "peso_liquido": dados['peso_liquido'],
        "dimensoes": {
            "altura": dados['altura'],
            "largura": dados['largura'],
            "profundidade": dados['profundidade']
        },
        "gtin": dados['gtin'],
        "tags": dados['tags'],
        "variacoes": dados['variacoes']
    }

    response = requests.put(url, json=payload, headers=headers)

    if response.status_code == 200:
        return {"status": "sucesso", "mensagem": f"Produto {produto_id} atualizado no Bling"}
    else:
        return {"status": "erro", "mensagem": response.text}
