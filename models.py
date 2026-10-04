from sqlalchemy import Column, Integer, String, Float, ForeignKey #Importa os tipos de coluna
from sqlalchemy.orm import relationship
from database import Base #Importa a base criada em database.py

class TransacaoModel(Base): # Criação do modelo que representa a tabela de transacoes
    __tablename__ = "transacoes" #Define o nome da tabela no banco

    id = Column(Integer, primary_key=True, index=True) #CHAVE PRIMARIA
    descricao = Column(String, nullable=False)
    valor = Column(Float, nullable=False)
    tipo = Column(String, nullable=False)

    categoria_id = Column(Integer, ForeignKey("categorias.id"), nullable=False)
    categoria = relationship("CategoriaModel", back_populates="transacoes")

    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    usuario = relationship("UsuarioModel", back_populates="transacoes")

class CategoriaModel(Base):
    __tablename__ = "categorias"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False, unique=True)

    transacoes = relationship("TransacaoModel", back_populates="categoria")

class UsuarioModel(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True, index=True)
    senha_hash = Column(String, nullable=False)
    transacoes = relationship("TransacaoModel", back_populates="usuario")