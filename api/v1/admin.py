from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database.connection import get_db
from database.models import Produto, LogProcesso
from database.schemas import ProdutoSchema
from services.bling_service import atualizar_produto_no_bling
import logging

router = APIRouter(prefix="/admin", tags=["Admin"])

# Configuração de logs
logger = logging.getLogger(__name__)

@router.get("/produtos_pendentes", response_model=list[ProdutoSchema])
def listar_produtos_pendentes(db: Session = Depends(get_db)):
    """Lista produtos pendentes de aprovação pelo admin"""
    produtos = db.query(Produto).filter(Produto.status == "pendente").all()
    if not produtos:
        raise HTTPException(status_code=404, detail="Nenhum produto pendente encontrado")
    
    return produtos

@router.put("/aprovar/{produto_id}")
def aprovar_produto(produto_id: int, db: Session = Depends(get_db)):
    """Admin aprova um produto para ser atualizado no Bling"""
    produto = db.query(Produto).filter(Produto.id == produto_id, Produto.status == "pendente").first()
    if not produto:
        raise HTTPException(status_code=404, detail="Produto não encontrado ou já aprovado")

    produto.status = "pronto"
    db.commit()

    # Registro no log de processos
    log = LogProcesso(produto_id=produto.id, acao="aprovar", status="sucesso", detalhes={"mensagem": "Produto aprovado"})
    db.add(log)
    db.commit()

    logger.info(f"Produto {produto.id} aprovado com sucesso!")
    return {"message": f"Produto {produto.id} aprovado com sucesso!"}

@router.post("/atualizar_bling")
def atualizar_bling(db: Session = Depends(get_db)):
    """Envia produtos aprovados para o Bling"""
    produtos = db.query(Produto).filter(Produto.status == "pronto").all()
    if not produtos:
        raise HTTPException(status_code=400, detail="Nenhum produto pronto para atualização")

    erros = []
    
    for produto in produtos:
        try:
            sucesso = atualizar_produto_no_bling(produto)
            if sucesso:
                produto.status = "atualizado"
                log_status = "sucesso"
            else:
                log_status = "erro"
                erros.append(produto.id)

            # Registro no log de processos
            log = LogProcesso(produto_id=produto.id, acao="atualizacao_bling", status=log_status)
            db.add(log)

        except Exception as e:
            logger.error(f"Erro ao atualizar produto {produto.id} no Bling: {str(e)}")
            erros.append(produto.id)

    db.commit()

    if erros:
        raise HTTPException(status_code=500, detail={"message": "Erro ao atualizar alguns produtos no Bling", "ids": erros})

    logger.info("Todos os produtos foram atualizados no Bling com sucesso!")
    return {"message": "Todos os produtos foram atualizados no Bling com sucesso!"}
