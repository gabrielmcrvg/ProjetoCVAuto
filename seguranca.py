from typing import Annotated

from pwdlib import PasswordHash
from datetime import datetime, timedelta, timezone
import jwt

import os
from dotenv import load_dotenv
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from database import SessionDep
from models.usuarios import Usuario
from models.curriculos import Curriculo

load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"

pwd_hash = PasswordHash.recommended()
OAuth2_scheme = OAuth2PasswordBearer(tokenUrl="usuarios/token")

def gerar_hash(senha: str) -> str:
    return pwd_hash.hash(senha)

def verificar_senha(senha, hash_senha) -> bool:
    return pwd_hash.verify(senha, hash_senha)

def criar_token(dados: dict) -> str:
    payload = dados.copy()
    exp = datetime.now(timezone.utc) + timedelta(minutes=30)
    payload.update({"exp": exp})
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def usuario_atual(session: SessionDep, token: str = Depends(OAuth2_scheme)) -> Usuario:
    erro = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Nao foi possivel validar as credenciais",
        headers={"WWW-Authenticate": "Bearer"})
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")
        if email is None:
            raise erro
    except jwt.PyJWTError:
        raise erro
    usuario = session.query(Usuario).filter(Usuario.email == email).first()
    if usuario is None:
        raise erro
    return usuario

UsuarioAtual = Annotated[Usuario, Depends(usuario_atual)]

def dono_do_curriculo(curriculo_id: int, usuario: UsuarioAtual, session: SessionDep) -> Curriculo:
    curriculo = session.query(Curriculo).filter(Curriculo.id == curriculo_id).first()
    erro = HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Curriculo nao encontrado")
    if curriculo is None or curriculo.usuario_id != usuario.id:
        raise erro
    return curriculo

CurriculoDoUsuario = Annotated[Curriculo, Depends(dono_do_curriculo)]
