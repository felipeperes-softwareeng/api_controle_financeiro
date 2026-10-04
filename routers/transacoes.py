from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from models import TransacaoModel, CategoriaModel
from schemas import Transacao
from security import verificar_token

# Cria um router responsável pelas rotas de transações
router = APIRouter(
    prefix="/transacoes", # Todas as rotas deste arquivo começam com /transacoes
    tags=["Transações"] # Nome exibido no Swagger /docs
)


# Lista todas as transações cadastradas
@router.get("/")
def listar_transacoes(
    db: Session = Depends(get_db),
    usuario_id: int = Depends(verificar_token)
):

    transacoes_banco = db.query(TransacaoModel).filter(
        TransacaoModel.usuario_id == usuario_id
    ).all()

    return [
        {
            "id": transacao.id,
            "descricao": transacao.descricao,
            "valor": transacao.valor,
            "tipo": transacao.tipo,
            "categoria_id": transacao.categoria_id,
            "categoria": transacao.categoria.nome
        }
        for transacao in transacoes_banco
    ]


# Busca uma transação específica pelo ID
@router.get("/{id}")
def buscar_transacao(
    id: int,
    db: Session = Depends(get_db),
    usuario_id: int = Depends(verificar_token)
):

    transacao = db.query(TransacaoModel).filter(
        TransacaoModel.id == id,
        TransacaoModel.usuario_id == usuario_id
    ).first()

    if transacao is None:
        raise HTTPException(
            status_code=404,
            detail="Transação não encontrada"
        )

    return {
        "id": transacao.id,
        "descricao": transacao.descricao,
        "valor": transacao.valor,
        "tipo": transacao.tipo,
        "categoria_id": transacao.categoria_id,
        "categoria": transacao.categoria.nome
    }


# Cria uma nova transação
@router.post("/")
def criar_transacao(
    transacao: Transacao,
    db: Session = Depends(get_db),
    usuario_id: int = Depends(verificar_token)
):

    categoria = db.query(CategoriaModel).filter(
        CategoriaModel.id == transacao.categoria_id
    ).first()

    if categoria is None:
        raise HTTPException(
            status_code=404,
            detail="Categoria não encontrada"
        )

    nova_transacao = TransacaoModel(
        descricao=transacao.descricao,
        valor=transacao.valor,
        tipo=transacao.tipo,
        categoria_id=transacao.categoria_id,
        usuario_id=usuario_id
    )

    db.add(nova_transacao)
    db.commit()
    db.refresh(nova_transacao)

    return {
        "id": nova_transacao.id,
        "descricao": nova_transacao.descricao,
        "valor": nova_transacao.valor,
        "tipo": nova_transacao.tipo,
        "categoria_id": nova_transacao.categoria_id,
        "categoria": categoria.nome,
        "usuario_id": nova_transacao.usuario_id
    }


# Atualiza uma transação existente pelo ID
@router.put("/{id}")
def atualizar_transacao(
    id: int,
    transacao: Transacao,
    db: Session = Depends(get_db),
    usuario_id: int = Depends(verificar_token)
):

    transacao_banco = db.query(TransacaoModel).filter(
        TransacaoModel.id == id,
        TransacaoModel.usuario_id == usuario_id
    ).first()

    if transacao_banco is None:
        raise HTTPException(
            status_code=404,
            detail="Transação não encontrada"
        )

    categoria = db.query(CategoriaModel).filter(
        CategoriaModel.id == transacao.categoria_id
    ).first()

    if categoria is None:
        raise HTTPException(
            status_code=404,
            detail="Categoria não encontrada"
        )

    transacao_banco.descricao = transacao.descricao
    transacao_banco.valor = transacao.valor
    transacao_banco.tipo = transacao.tipo
    transacao_banco.categoria_id = transacao.categoria_id

    db.commit()
    db.refresh(transacao_banco)

    return {
        "id": transacao_banco.id,
        "descricao": transacao_banco.descricao,
        "valor": transacao_banco.valor,
        "tipo": transacao_banco.tipo,
        "categoria_id": transacao_banco.categoria_id,
        "categoria": transacao_banco.categoria.nome
    }


# Exclui uma transação pelo ID
@router.delete("/{id}")
def deletar_transacao(
    id: int,
    db: Session = Depends(get_db),
    usuario_id: int = Depends(verificar_token)
):

    transacao = db.query(TransacaoModel).filter(
        TransacaoModel.id == id,
        TransacaoModel.usuario_id == usuario_id
    ).first()

    if transacao is None:
        raise HTTPException(
            status_code=404,
            detail="Transação não encontrada"
        )

    db.delete(transacao)
    db.commit()

    return {"mensagem": "Transação excluída com sucesso"}