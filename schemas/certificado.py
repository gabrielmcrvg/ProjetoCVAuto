from typing import Optional

from pydantic import BaseModel, ConfigDict

from models.enums import Situacao


class CertificadoEntrada(BaseModel):
    nome: str
    instituicao: str
    carga_horaria: Optional[int] = None
    periodo: str


class CertificadoResposta(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    nome: str
    instituicao: str
    carga_horaria: Optional[int] = None
    situacao: Situacao
    periodo: str
