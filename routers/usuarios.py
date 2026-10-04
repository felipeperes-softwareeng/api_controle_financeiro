from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from models import UsuarioModel
from schemas import Usuario
from security import gerar_hash_senha


router = APIRouter(
    prefix="/usuarios",
    tags=["Usuários"]
)


@router.post("/")
def criar_usuario(usuario: Usuario, db: Session = Depends(get_db)):

    usuario_existente = db.query(UsuarioModel).filter(
        UsuarioModel.email == usuario.email
    ).first()

    if usuario_existente:
        raise HTTPException(
            status_code=400,
            detail="E-mail já cadastrado"
        )

    novo_usuario = UsuarioModel(
        nome=usuario.nome,
        email=usuario.email,
        senha_hash=gerar_hash_senha(usuario.senha)
    )

    db.add(novo_usuario)
    db.commit()
    db.refresh(novo_usuario)

    return {
        "id": novo_usuario.id,
        "nome": novo_usuario.nome,
        "email": novo_usuario.email
    }