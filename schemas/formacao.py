from typing import Optional

from pydantic import BaseModel, ConfigDict

from models.enums import Situacao


class FormacaoEntrada(BaseModel):
    curso: str
    instituicao: str
    ano_inicio: int
    ano_conclusao: Optional[int] = None
    situacao: Situacao


class FormacaoResposta(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    curso: str
    instituicao: str
    ano_inicio: int
    ano_conclusao: Optional[int] = None
    situacao: Situacao
