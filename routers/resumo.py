from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func

from database import get_db
from models import TransacaoModel
from security import verificar_token


router = APIRouter(
    prefix="/resumo",
    tags=["Resumo Financeiro"]
)


@router.get("/")
def obter_resumo(
    db: Session = Depends(get_db),
    usuario_id: int = Depends(verificar_token)
):

    total_receitas = db.query(
        func.sum(TransacaoModel.valor)
    ).filter(
        TransacaoModel.usuario_id == usuario_id,
        TransacaoModel.tipo == "receita"
    ).scalar() or 0

    total_despesas = db.query(
        func.sum(TransacaoModel.valor)
    ).filter(
        TransacaoModel.usuario_id == usuario_id,
        TransacaoModel.tipo == "despesa"
    ).scalar() or 0

    saldo = total_receitas - total_despesas

    return {
        "total_receitas": total_receitas,
        "total_despesas": total_despesas,
        "saldo": saldo
    }