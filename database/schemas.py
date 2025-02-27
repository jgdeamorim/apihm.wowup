from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class ClienteSchema(BaseModel):
    id: Optional[int]
    nome: str
    api_key_bling: str
    api_key_mercadolivre: str
    created_at: Optional[datetime]

    class Config:
        orm_mode = True

class ProdutoSchema(BaseModel):
    id: Optional[int]
    cliente_id: int
    nome: str
    gtin: Optional[str]
    categoria: Optional[str]
    marca: Optional[str]
    tags: Optional[List[str]]
    peso: Optional[float]
    dimensoes: Optional[str]
    ncm: Optional[str]
    descricao: Optional[str]
    status: Optional[str]
    imagem_url: Optional[str]
    atualizado_em: Optional[datetime]

    class Config:
        orm_mode = True

class LogOperacaoSchema(BaseModel):
    id: Optional[int]
    cliente_id: int
    operacao: str
    status: str
    detalhes: Optional[str]
    created_at: Optional[datetime]

    class Config:
        orm_mode = True

class ConfiguracaoAPISchema(BaseModel):
    id: Optional[int]
    cliente_id: int
    chave: str
    valor: str

    class Config:
        orm_mode = True
