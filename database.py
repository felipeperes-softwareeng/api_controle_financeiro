from sqlalchemy import create_engine #Cria a conexão com o banco de dados
from sqlalchemy.orm import sessionmaker, declarative_base #Cria sessoes e a base dos modelos

DATABASE_URL = "sqlite:///./financeiro.db" #Define o caminho do SQLite

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} #Permite o uso do SQLite com o FastAPI
)

SessionLocal = sessionmaker(
    autocommit=False, #Não salva alterações altomaticamente
    autoflush=False, # Não envia alterações automaticamente antes das consultas
    bind=engine # Liga a sessão ao banco
)

Base = declarative_base() # Cria a classe usada pelos modelos/tabelas