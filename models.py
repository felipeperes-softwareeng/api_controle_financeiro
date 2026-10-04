from sqlalchemy import Column, Integer, String, Float #Importa os tipos de coluna
from database import Base #Importa a base criada em database.py

class TransacaoModel(Base): # Criação do modelo que representa a tabela de transacoes
    __tablename__ = "transacoes" #Define o nome da tabela no banco

    id = Column(Integer, primary_key=True, index=True) #CHAVE PRIMARIA
    descricao = Column(String, nullable=False)
    valor = Column(Float, nullable=False)
    tipo = Column(String, nullable=False)

class CategoriaModel(Base):
    __tablename__ = "categorias"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False, unique=True)