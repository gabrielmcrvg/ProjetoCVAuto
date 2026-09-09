from typing import Optional

from pydantic import BaseModel, ConfigDict


class ProjetoEntrada(BaseModel):
    nome: str
    contexto: str
    tecnologias: str
    descricao: str
    link: Optional[str] = None


class ProjetoResposta(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    nome: str
    contexto: str
    tecnologias: str
    descricao: str
    link: Optional[str] = None
