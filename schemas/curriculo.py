from typing import Optional

from pydantic import BaseModel, ConfigDict

from schemas.experiencia import ExperienciaResposta
from schemas.formacao import FormacaoResposta
from schemas.habilidade import HabilidadeResposta
from schemas.idioma import IdiomaResposta
from schemas.projeto import ProjetoResposta
from schemas.certificado import CertificadoResposta


class CurriculoEntrada(BaseModel):
    titulo: str
    resumo_profissional: str
    nome_completo: str
    localizacao: str
    telefone: str
    url_1: Optional[str] = None
    url_2: Optional[str] = None


class CurriculoAtualizar(BaseModel):
    titulo: Optional[str] = None
    resumo_profissional: Optional[str] = None
    nome_completo: Optional[str] = None
    localizacao: Optional[str] = None
    telefone: Optional[str] = None
    url_1: Optional[str] = None
    url_2: Optional[str] = None


class CurriculoResposta(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    titulo: str
    resumo_profissional: str
    nome_completo: str
    localizacao: str
    telefone: str
    url_1: Optional[str] = None
    url_2: Optional[str] = None


class CurriculoCompleto(CurriculoResposta):
    experiencias: list[ExperienciaResposta] = []
    formacoes: list[FormacaoResposta] = []
    habilidades: list[HabilidadeResposta] = []
    idiomas: list[IdiomaResposta] = []
    projetos: list[ProjetoResposta] = []
    certificados: list[CertificadoResposta] = []
