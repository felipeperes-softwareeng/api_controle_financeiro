from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from models import TransacaoModel
from schemas import Transacao

# Cria um router responsável pelas rotas de transações
router = APIRouter(
    prefix="/transacoes", # Todas as rotas deste arquivo começam com /transacoes
    tags=["Transações"] # Nome exibido no Swagger /docs
)


# Lista todas as transações cadastradas
@router.get("/")
def listar_transacoes(db: Session = Depends(get_db)):

    transacoes_banco = db.query(TransacaoModel).all() # Busca todas as transações no banco

    return [
        {
            "id": transacao.id,
            "descricao": transacao.descricao,
            "valor": transacao.valor,
            "tipo": transacao.tipo
        }
        for transacao in transacoes_banco
    ]


# Busca uma transação específica pelo ID
@router.get("/{id}")
def buscar_transacao(id: int, db: Session = Depends(get_db)):

    transacao = db.query(TransacaoModel).filter(
        TransacaoModel.id == id
    ).first()

    # Retorna erro 404 caso a transação não exista
    if transacao is None:
        raise HTTPException(
            status_code=404,
            detail="Transação não encontrada"
        )

    return {
        "id": transacao.id,
        "descricao": transacao.descricao,
        "valor": transacao.valor,
        "tipo": transacao.tipo
    }


# Cria uma nova transação
@router.post("/")
def criar_transacao(transacao: Transacao, db: Session = Depends(get_db)):

    # Cria um objeto que representa a nova linha da tabela
    nova_transacao = TransacaoModel(
        descricao=transacao.descricao,
        valor=transacao.valor,
        tipo=transacao.tipo
    )

    db.add(nova_transacao) # Adiciona à sessão
    db.commit() # Salva no banco
    db.refresh(nova_transacao) # Atualiza o objeto com dados gerados pelo banco, como o ID

    return {
        "id": nova_transacao.id,
        "descricao": nova_transacao.descricao,
        "valor": nova_transacao.valor,
        "tipo": nova_transacao.tipo
    }


# Atualiza uma transação existente pelo ID
@router.put("/{id}")
def atualizar_transacao(id: int, transacao: Transacao, db: Session = Depends(get_db)):

    transacao_banco = db.query(TransacaoModel).filter(
        TransacaoModel.id == id
    ).first()

    if transacao_banco is None:
        raise HTTPException(
            status_code=404,
            detail="Transação não encontrada"
        )

    # Substitui os dados antigos pelos novos
    transacao_banco.descricao = transacao.descricao
    transacao_banco.valor = transacao.valor
    transacao_banco.tipo = transacao.tipo

    db.commit() # Salva as alterações
    db.refresh(transacao_banco)

    return {
        "id": transacao_banco.id,
        "descricao": transacao_banco.descricao,
        "valor": transacao_banco.valor,
        "tipo": transacao_banco.tipo
    }


# Exclui uma transação pelo ID
@router.delete("/{id}")
def deletar_transacao(id: int, db: Session = Depends(get_db)):

    transacao = db.query(TransacaoModel).filter(
        TransacaoModel.id == id
    ).first()

    if transacao is None:
        raise HTTPException(
            status_code=404,
            detail="Transação não encontrada"
        )

    db.delete(transacao) # Marca a transação para exclusão
    db.commit() # Confirma a exclusão no banco

    return {"mensagem": "Transação excluída com sucesso"}