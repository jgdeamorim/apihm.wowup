import requests
import os

def validar_credenciais_mercadolivre(client_id: str, client_secret: str) -> bool:
    """Valida as credenciais do Mercado Livre."""
    url = "https://api.mercadolibre.com/oauth/token"
    payload = {
        "grant_type": "client_credentials",
        "client_id": client_id,
        "client_secret": client_secret,
    }
    resposta = requests.post(url, data=payload)
    return resposta.status_code == 200

def validar_credenciais_bling(api_key: str) -> bool:
    """Valida a API Key do Bling."""
    url = f"https://bling.com.br/Api/v3/produtos?apikey={api_key}"
    resposta = requests.get(url)
    return resposta.status_code == 200
