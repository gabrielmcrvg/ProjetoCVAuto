from pydantic import BaseModel, ConfigDict, EmailStr, Field


class UsuarioEntrada(BaseModel):
    email: EmailStr
    senha: str = Field(min_length=6)

class UsuarioResposta(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    email: EmailStr

class SenhaAtualizar(BaseModel):
    senha_atual: str
    senha_nova: str = Field(min_length=6)

class Token(BaseModel):
    access_token: str
    token_type: str
