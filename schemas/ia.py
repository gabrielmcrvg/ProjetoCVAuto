from pydantic import BaseModel

from models.enums import CategoriaHabilidade


class TextoEntrada(BaseModel):
    texto: str


class TextoSugerido(BaseModel):
    texto_sugerido: str


class SugestaoCategoria(BaseModel):
    id: int
    categoria: CategoriaHabilidade
