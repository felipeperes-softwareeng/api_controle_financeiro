from pydantic import BaseModel, Field
from typing import Literal


class Transacao(BaseModel):
    descricao: str
    valor: float = Field(gt=0)
    tipo: Literal["receita", "despesa"]

class Categoria(BaseModel):
    nome: str = Field(min_length=1)