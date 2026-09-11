from typing import Optional

from pydantic import BaseModel, ConfigDict

from models.enums import SituacaoCertificado


class CertificadoEntrada(BaseModel):
    nome: str
    instituicao: str
    carga_horaria: Optional[int] = None
    periodo: str
    situacao: SituacaoCertificado = SituacaoCertificado.CONCLUIDO


class CertificadoAtualizar(BaseModel):
    nome: Optional[str] = None
    instituicao: Optional[str] = None
    carga_horaria: Optional[int] = None
    periodo: Optional[str] = None
    situacao: Optional[SituacaoCertificado] = None


class CertificadoResposta(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    nome: str
    instituicao: str
    carga_horaria: Optional[int] = None
    situacao: SituacaoCertificado
    periodo: str
