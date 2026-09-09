from pydantic import BaseModel, ConfigDict


class IdiomaEntrada(BaseModel):
    nome: str
    nivel: str


class IdiomaResposta(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    nome: str
    nivel: str
