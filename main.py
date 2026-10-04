from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session

from database import engine, get_db
from models import Base, TransacaoModel
from schemas import Transacao
from routers import transacoes, categorias, usuarios, auth

Base.metadata.create_all(bind = engine) # Verifica os modelos que herdam na "Base" e cria a tabela no database caso nao existam 

app = FastAPI() #Cria a aplicação

app.include_router(transacoes.router)
app.include_router(categorias.router)
app.include_router(usuarios.router)
app.include_router(auth.router)

@app.get("/") #Cria uma rota GET no endereço principal "/"
def inicio():
    return {"mensagem": "API de Controle Financeiro"} #Retorna msg em JSON