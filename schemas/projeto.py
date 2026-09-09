from typing import Optional

from pydantic import BaseModel, ConfigDict


class ProjetoEntrada(BaseModel):
    nome: str
    contexto: str
    tecnologias: str
    descricao: str
    link: Optional[str] = None


class ProjetoAtualizar(BaseModel):
    nome: Optional[str] = None
    contexto: Optional[str] = None
    tecnologias: Optional[str] = None
    descricao: Optional[str] = None
    link: Optional[str] = None


class ProjetoResposta(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    nome: str
    contexto: str
    tecnologias: str
    descricao: str
    link: Optional[str] = None
