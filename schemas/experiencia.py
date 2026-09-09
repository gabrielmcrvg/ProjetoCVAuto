from datetime import date
from typing import Optional

from pydantic import BaseModel, ConfigDict


class ExperienciaEntrada(BaseModel):
    cargo: str
    empresa: str
    data_inicio: date
    data_fim: Optional[date] = None
    descricao: str


class ExperienciaResposta(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    cargo: str
    empresa: str
    data_inicio: date
    data_fim: Optional[date] = None
    descricao: str
