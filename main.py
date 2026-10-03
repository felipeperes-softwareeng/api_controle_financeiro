from pydantic import BaseModel
from fastapi import FastAPI, HTTPException

app = FastAPI() #Cria a aplicação

class Transacao(BaseModel): #Cria o modelo de dados de uma transacao
    descricao: str
    valor: float
    tipo: str

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
def listar_transacoes(): #lista todas as transacoes
    return transacoes

@app.get("/transacoes/{id}") 
def buscar_transacao(id: int): #Busca uma transacao pelo id e caso nao ache retorna transacao nao encointrada

    for transacao in transacoes:
        if transacao["id"] == id:
            return transacao

    raise HTTPException(status_code=404, detail = "Transação não encontrada")

@app.delete("/transacoes/{id}")
def deletar_transacao(id: int): #Deleta transacao pelo id e se nao encontrada retorna transacoa nao encontrada

    for transacao in transacoes:
        if transacao["id"] == id:
            transacoes.remove(transacao)
            return {"mensagem": "Transação excluída com sucesso"}

    raise HTTPException(status_code=404, detail = "Transação não encontrada")

@app.post("/transacoes") #Cria rota post para receber uma nova transacao
def criar_transacao(transacao: Transacao):

    if transacoes:
        novo_id = max(transacao["id"] for transacao in transacoes) + 1
    else:
        novo_id = 1

    nova_transacao = {
        "id": novo_id,
        "descricao": transacao.descricao,
        "valor": transacao.valor,
        "tipo": transacao.tipo
    }

    transacoes.append(nova_transacao)
    return nova_transacao

@app.put("/transacoes/{id}")
def atualizar_transacao(id: int, transacao: Transacao):

    for item in transacoes:
        if item["id"] == id:
            item["descricao"] = transacao.descricao
            item["valor"] = transacao.valor
            item["tipo"] = transacao.tipo

            return item

    raise HTTPException(status_code=404, detail="Transação não encontrada")     