from typing import Optional

from pydantic import BaseModel, ConfigDict

from models.enums import CategoriaHabilidade


class HabilidadeEntrada(BaseModel):
    nome: str


class HabilidadeAtualizar(BaseModel):
    nome: Optional[str] = None


class HabilidadeResposta(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    nome: str
    categoria: Optional[CategoriaHabilidade] = None
