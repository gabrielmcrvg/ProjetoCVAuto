from typing import Optional

from pydantic import BaseModel, ConfigDict

from models.enums import Situacao


class FormacaoEntrada(BaseModel):
    curso: str
    instituicao: str
    ano_inicio: int
    ano_conclusao: Optional[int] = None
    situacao: Situacao


class FormacaoAtualizar(BaseModel):
    curso: Optional[str] = None
    instituicao: Optional[str] = None
    ano_inicio: Optional[int] = None
    ano_conclusao: Optional[int] = None
    situacao: Optional[Situacao] = None


class FormacaoResposta(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    curso: str
    instituicao: str
    ano_inicio: int
    ano_conclusao: Optional[int] = None
    situacao: Situacao
