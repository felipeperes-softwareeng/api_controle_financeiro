from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from models import CategoriaModel
from schemas import Categoria


router = APIRouter(
    prefix="/categorias",
    tags=["Categorias"]
)


# Lista todas as categorias
@router.get("/")
def listar_categorias(db: Session = Depends(get_db)):

    categorias_banco = db.query(CategoriaModel).all()

    return [
        {
            "id": categoria.id,
            "nome": categoria.nome
        }
        for categoria in categorias_banco
    ]


# Busca uma categoria pelo ID
@router.get("/{id}")
def buscar_categoria(id: int, db: Session = Depends(get_db)):

    categoria = db.query(CategoriaModel).filter(
        CategoriaModel.id == id
    ).first()

    if categoria is None:
        raise HTTPException(
            status_code=404,
            detail="Categoria não encontrada"
        )

    return {
        "id": categoria.id,
        "nome": categoria.nome
    }


# Cria uma nova categoria
@router.post("/")
def criar_categoria(categoria: Categoria, db: Session = Depends(get_db)):

    categoria_existente = db.query(CategoriaModel).filter(
        CategoriaModel.nome == categoria.nome
    ).first()

    if categoria_existente:
        raise HTTPException(
            status_code=400,
            detail="Categoria já cadastrada"
        )

    nova_categoria = CategoriaModel(
        nome=categoria.nome
    )

    db.add(nova_categoria)
    db.commit()
    db.refresh(nova_categoria)

    return {
        "id": nova_categoria.id,
        "nome": nova_categoria.nome
    }


# Atualiza uma categoria pelo ID
@router.put("/{id}")
def atualizar_categoria(id: int, categoria: Categoria, db: Session = Depends(get_db)):

    categoria_banco = db.query(CategoriaModel).filter(
        CategoriaModel.id == id
    ).first()

    if categoria_banco is None:
        raise HTTPException(
            status_code=404,
            detail="Categoria não encontrada"
        )

    categoria_existente = db.query(CategoriaModel).filter(
        CategoriaModel.nome == categoria.nome,
        CategoriaModel.id != id
    ).first()

    if categoria_existente:
        raise HTTPException(
            status_code=400,
            detail="Categoria já cadastrada"
        )

    categoria_banco.nome = categoria.nome

    db.commit()
    db.refresh(categoria_banco)

    return {
        "id": categoria_banco.id,
        "nome": categoria_banco.nome
    }


# Exclui uma categoria pelo ID
@router.delete("/{id}")
def deletar_categoria(id: int, db: Session = Depends(get_db)):

    categoria = db.query(CategoriaModel).filter(
        CategoriaModel.id == id
    ).first()

    if categoria is None:
        raise HTTPException(
            status_code=404,
            detail="Categoria não encontrada"
        )

    # Impede excluir uma categoria que possui transações
    if categoria.transacoes:
        raise HTTPException(
            status_code=400,
            detail="Categoria possui transações cadastradas"
        )

    db.delete(categoria)
    db.commit()

    return {"mensagem": "Categoria excluída com sucesso"}