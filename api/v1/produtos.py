from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database.connection import get_db
from database.models import Produto
from database.schemas import ProdutoSchema, ProdutoCreate

router = APIRouter(prefix="/produtos", tags=["Produtos"])

@router.get("/", response_model=list[ProdutoSchema])
def listar_produtos(db: Session = Depends(get_db)):
    """Lista todos os produtos armazenados no banco"""
    return db.query(Produto).all()

@router.get("/{produto_id}", response_model=ProdutoSchema)
def obter_produto(produto_id: int, db: Session = Depends(get_db)):
    """Obtém um produto específico pelo ID"""
    produto = db.query(Produto).filter(Produto.id == produto_id).first()
    if not produto:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    return produto

@router.post("/", response_model=ProdutoSchema)
def cadastrar_produto(produto: ProdutoCreate, db: Session = Depends(get_db)):
    """Cadastra um novo produto no banco"""
    novo_produto = Produto(
        nome=produto.nome,
        categoria=produto.categoria,
        tags=produto.tags,
        ncm=produto.ncm,
        descricao=produto.descricao,
        status="pendente"
    )
    db.add(novo_produto)
    db.commit()
    db.refresh(novo_produto)
    return novo_produto

@router.put("/{produto_id}", response_model=ProdutoSchema)
def atualizar_produto(produto_id: int, produto: ProdutoCreate, db: Session = Depends(get_db)):
    """Atualiza os dados de um produto"""
    produto_db = db.query(Produto).filter(Produto.id == produto_id).first()
    if not produto_db:
        raise HTTPException(status_code=404, detail="Produto não encontrado")

    produto_db.nome = produto.nome
    produto_db.categoria = produto.categoria
    produto_db.tags = produto.tags
    produto_db.ncm = produto.ncm
    produto_db.descricao = produto.descricao
    db.commit()
    
    return produto_db

@router.delete("/{produto_id}")
def deletar_produto(produto_id: int, db: Session = Depends(get_db)):
    """Remove um produto do banco"""
    produto = db.query(Produto).filter(Produto.id == produto_id).first()
    if not produto:
        raise HTTPException(status_code=404, detail="Produto não encontrado")

    db.delete(produto)
    db.commit()
    return {"message": "Produto removido com sucesso!"}
