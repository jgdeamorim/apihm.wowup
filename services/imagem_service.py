import os
import requests

STORAGE_DIR = "storage/"
if not os.path.exists(STORAGE_DIR):
    os.makedirs(STORAGE_DIR)

def baixar_imagem(produto_id: str, url_imagem: str) -> str:
    """Baixa e armazena uma imagem localmente."""
    caminho_imagem = os.path.join(STORAGE_DIR, f"{produto_id}.jpg")

    if os.path.exists(caminho_imagem):
        return caminho_imagem  # Retorna a imagem se já existir

    resposta = requests.get(url_imagem, stream=True)
    if resposta.status_code == 200:
        with open(caminho_imagem, "wb") as file:
            for chunk in resposta.iter_content(1024):
                file.write(chunk)
        return caminho_imagem
    return None

def remover_imagem(produto_id: str):
    """Remove uma imagem armazenada localmente."""
    caminho_imagem = os.path.join(STORAGE_DIR, f"{produto_id}.jpg")
    if os.path.exists(caminho_imagem):
        os.remove(caminho_imagem)
