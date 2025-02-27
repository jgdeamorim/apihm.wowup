from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database.connection import get_db
from database.models import Cliente
from database.schemas import ClienteSchema, ClienteCreate

router = APIRouter(prefix="/clientes", tags=["Clientes"])

@router.get("/", response_model=list[ClienteSchema])
def listar_clientes(db: Session = Depends(get_db)):
    """Lista todos os clientes cadastrados"""
    return db.query(Cliente).all()

@router.post("/", response_model=ClienteSchema)
def cadastrar_cliente(cliente: ClienteCreate, db: Session = Depends(get_db)):
    """Cadastra um novo cliente com suas chaves de API"""
    novo_cliente = Cliente(
        nome=cliente.nome,
        api_bling_key=cliente.api_bling_key,
        api_mercadolivre_key=cliente.api_mercadolivre_key
    )
    db.add(novo_cliente)
    db.commit()
    db.refresh(novo_cliente)
    return novo_cliente

@router.get("/{cliente_id}", response_model=ClienteSchema)
def obter_cliente(cliente_id: int, db: Session = Depends(get_db)):
    """Obtém detalhes de um cliente específico"""
    cliente = db.query(Cliente).filter(Cliente.id == cliente_id).first()
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    return cliente

@router.put("/{cliente_id}")
def atualizar_cliente(cliente_id: int, cliente: ClienteCreate, db: Session = Depends(get_db)):
    """Atualiza as chaves de API de um cliente"""
    cliente_db = db.query(Cliente).filter(Cliente.id == cliente_id).first()
    if not cliente_db:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")

    cliente_db.api_bling_key = cliente.api_bling_key
    cliente_db.api_mercadolivre_key = cliente.api_mercadolivre_key
    db.commit()
    return {"message": "Cliente atualizado com sucesso!"}

@router.delete("/{cliente_id}")
def deletar_cliente(cliente_id: int, db: Session = Depends(get_db)):
    """Remove um cliente do sistema"""
    cliente = db.query(Cliente).filter(Cliente.id == cliente_id).first()
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")

    db.delete(cliente)
    db.commit()
    return {"message": "Cliente removido com sucesso!"}
