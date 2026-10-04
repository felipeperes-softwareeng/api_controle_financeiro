from pydantic import BaseModel, Field
from typing import Literal


class Transacao(BaseModel):
    descricao: str
    valor: float = Field(gt=0)
    tipo: Literal["receita", "despesa"]
    categoria_id: int

class Categoria(BaseModel):
    nome: str = Field(min_length=1)

class Usuario(BaseModel):
    nome: str = Field(min_length=2)
    email: str
    senha: str = Field(min_length=6)

class Login(BaseModel):
    email: str
    senha: str