import requests
from sqlalchemy.orm import Session
from database.models import NCM
from services.mercadolivre_service import buscar_produto_por_gtin
from services.openai_service import gerar_sugestao_ncm

SISCOMEX_NCM_URL = "https://api.portalunico.siscomex.gov.br/classif/ncm/"

def obter_ncm(db: Session, gtin: str, descricao: str) -> str:
    """
    Busca o código NCM de um produto, priorizando as seguintes fontes:
    1️⃣ Banco de Dados local (economia de requisições)
    2️⃣ Mercado Livre (via GTIN)
    3️⃣ API do Portal Único Siscomex (via Descrição)
    4️⃣ OpenAI para refinamento se ainda não encontrado
    5️⃣ Salva no banco se um novo NCM for encontrado
    """

    # 🔎 1️⃣ Buscar primeiro no banco de dados
    ncm_existente = db.query(NCM).filter(NCM.descricao == descricao).first()
    if ncm_existente:
        return ncm_existente.ncm  # Retorna diretamente do banco se já existir

    # 🔎 2️⃣ Buscar no Mercado Livre via GTIN
    produto = buscar_produto_por_gtin(gtin)
    if produto and produto.get("ncm"):
        salvar_ncm(db, descricao, produto["ncm"])
        return produto["ncm"]

    # 🔎 3️⃣ Buscar na API do Siscomex pela descrição do produto
    resposta = requests.get(f"{SISCOMEX_NCM_URL}?descricao={descricao}")
    if resposta.status_code == 200:
        dados = resposta.json()
        if dados and "codigo" in dados[0]:  # Verifica se a resposta contém um NCM válido
            ncm = dados[0]["codigo"]
            salvar_ncm(db, descricao, ncm)
            return ncm

    # 🔎 4️⃣ Refinamento com OpenAI caso não tenha encontrado um NCM válido
    ncm_gerado = gerar_sugestao_ncm(descricao)
    salvar_ncm(db, descricao, ncm_gerado)
    return ncm_gerado

def salvar_ncm(db: Session, descricao: str, ncm: str):
    """Salva o código NCM no banco de dados"""
    novo_ncm = NCM(descricao=descricao, ncm=ncm)
    db.add(novo_ncm)
    db.commit()
