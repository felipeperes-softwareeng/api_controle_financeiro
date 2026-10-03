from pydantic import BaseModel, Field
from typing import Literal
from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session

from database import engine, SessionLocal
from models import Base, TransacaoModel

Base.metadata.create_all(bind = engine) # Verifica os modelos que herdam na "Base" e cria a tabela no database caso nao existam 

app = FastAPI() #Cria a aplicação

def get_db(): #Cria e controla uma sessao com o banco de dados
    db = SessionLocal() #Abre uma nova sessao

    try:
        yield db
    finally:
        db.close()

class Transacao(BaseModel): #Cria o modelo de dados de uma transacao
    descricao: str
    valor: float = Field(gt=0) #o Field(gt=0) significa que o valor obrigatoriamente deve ser maior que 0
    tipo: Literal["receita", "despesa"] #Significa que o campo "tipo" aceita apenas: despesa e receita

transacoes = [
    {
        "id": 1,
        "descricao": "Salário",
        "valor": 3000,
        "tipo": "receita"
    },
    {
        "id": 2,
        "descricao": "Mercado",
        "valor": 250,
        "tipo": "despesa"
    }
]

@app.get("/") #Cria uma rota GET no endereço principal "/"
def inicio():
    return {"mensagem": "API de Controle Financeiro"} #Retorna msg em JSON

@app.get("/transacoes") 
def listar_transacoes(db: Session = Depends(get_db)): #lista todas as transacoes

    transacoes_banco = db.query(TransacaoModel).all()

    return[
        {
            "id": transacao.id,
            "descricao": transacao.descricao,
            "valor": transacao.valor,
            "tipo": transacao.tipo
        }
        for transacao in transacoes_banco
    ]

@app.get("/transacoes/{id}") 
def buscar_transacao(id: int, db: Session = Depends(get_db)):  #Busca uma transacao pelo id e caso nao ache retorna transacao nao encointrada

    transacao = db.query(TransacaoModel).filter(TransacaoModel.id == id).first()
    
    if transacao is None:
        raise HTTPException(status_code=404, detail="Transação não encontrada")

    return {
        "id": transacao.id,
        "descricao": transacao.descricao,
        "valor": transacao.valor,
        "tipo": transacao.tipo
    }

@app.delete("/transacoes/{id}")
def deletar_transacao(id: int): #Deleta transacao pelo id e se nao encontrada retorna transacoa nao encontrada

    for transacao in transacoes:
        if transacao["id"] == id:
            transacoes.remove(transacao)
            return {"mensagem": "Transação excluída com sucesso"}

    raise HTTPException(status_code=404, detail = "Transação não encontrada")

@app.post("/transacoes") #Cria rota post para receber uma nova transacao
def criar_transacao(transacao: Transacao, db: Session = Depends(get_db)):

    nova_transacao = TransacaoModel(
        descricao = transacao.descricao,
        valor = transacao.valor,
        tipo = transacao.tipo
    )

    db.add(nova_transacao)
    db.commit()
    db.refresh(nova_transacao)

    return {
        "id": nova_transacao.id,
        "descricao": nova_transacao.descricao,
        "valor": nova_transacao.valor,
        "tipo": nova_transacao.tipo
    }

@app.put("/transacoes/{id}")
def atualizar_transacao(id: int, transacao: Transacao):

    for item in transacoes:
        if item["id"] == id:
            item["descricao"] = transacao.descricao
            item["valor"] = transacao.valor
            item["tipo"] = transacao.tipo

            return item

    raise HTTPException(status_code=404, detail="Transação não encontrada")     