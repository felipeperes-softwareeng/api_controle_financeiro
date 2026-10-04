from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from models import UsuarioModel
from schemas import Login
from security import verificar_senha, criar_token, verificar_token


router = APIRouter(
    prefix="/auth",
    tags=["Autenticação"]
)


@router.post("/login")
def login(dados: Login, db: Session = Depends(get_db)):

    usuario = db.query(UsuarioModel).filter(
        UsuarioModel.email == dados.email
    ).first()

    if usuario is None:
        raise HTTPException(
            status_code=401,
            detail="E-mail ou senha inválidos"
        )

    if not verificar_senha(dados.senha, usuario.senha_hash):
        raise HTTPException(
            status_code=401,
            detail="E-mail ou senha inválidos"
        )

    token = criar_token(usuario.id)

    return {
        "access_token": token,
        "token_type": "bearer"
    }

@router.get("/me")
def usuario_logado(usuario_id: int = Depends(verificar_token)):

    return {
        "usuario_id": usuario_id
    }