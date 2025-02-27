from sqlalchemy import Column, Integer, String, Float, JSON, ForeignKey, TIMESTAMP, text
from sqlalchemy.orm import relationship
from database.connection import Base

class NCM(Base):
    """Tabela de armazenamento de códigos NCM já pesquisados"""
    __tablename__ = "ncm"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    descricao = Column(String, unique=True, index=True, nullable=False)
    ncm = Column(String, nullable=False, unique=True)  # Código NCM de 8 dígitos


class Cliente(Base):
    """Tabela de clientes (cada cliente possui suas credenciais de API)"""
    __tablename__ = "clientes"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nome = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    bling_api_key = Column(String, nullable=False)
    mercadolivre_client_id = Column(String, nullable=False)
    mercadolivre_client_secret = Column(String, nullable=False)

    produtos = relationship("Produto", back_populates="cliente")
    configuracoes = relationship("ConfiguracaoAPI", back_populates="cliente")


class Produto(Base):
    """Tabela de produtos"""
    __tablename__ = "produtos"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    cliente_id = Column(Integer, ForeignKey("clientes.id"), nullable=False)
    nome = Column(String, nullable=False)
    categoria = Column(String, nullable=True)
    tags = Column(JSON, nullable=True)  # Exemplo: ["eletrônicos", "promoção"]
    ncm = Column(String, ForeignKey("ncm.ncm"), nullable=True)
    peso_bruto = Column(Float, nullable=True)
    peso_liquido = Column(Float, nullable=True)
    dimensoes = Column(JSON, nullable=True)  # { "altura": 0.0, "largura": 0.0, "profundidade": 0.0 }
    gtin = Column(String, unique=True, nullable=True)
    descricao = Column(String, nullable=True)
    status = Column(String, default="pendente")  # ["pendente", "pronto", "enviado"]
    atualizado_em = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"), onupdate=text("CURRENT_TIMESTAMP"))

    cliente = relationship("Cliente", back_populates="produtos")
    logs = relationship("LogProcesso", back_populates="produto")


class LogProcesso(Base):
    """Tabela para rastreamento de atualizações e erros"""
    __tablename__ = "logs_processo"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    produto_id = Column(Integer, ForeignKey("produtos.id"), nullable=False)
    acao = Column(String, nullable=False)  # Exemplo: "refinamento", "atualizacao_bling"
    status = Column(String, nullable=False)  # Exemplo: "sucesso", "erro"
    detalhes = Column(JSON, nullable=True)
    criado_em = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))

    produto = relationship("Produto", back_populates="logs")


class ConfiguracaoAPI(Base):
    """Armazena configurações personalizadas de cada cliente"""
    __tablename__ = "configuracoes"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    cliente_id = Column(Integer, ForeignKey("clientes.id"), nullable=False)
    chave = Column(String, nullable=False)  # Exemplo: "categoria_default"
    valor = Column(String, nullable=False)

    cliente = relationship("Cliente", back_populates="configuracoes")
