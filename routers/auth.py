from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from database import SessionDep
from models.usuarios import Usuario
from schemas.usuario import SenhaAtualizar, Token, UsuarioEntrada, UsuarioResposta
from seguranca import UsuarioAtual, criar_token, gerar_hash, verificar_senha

router = APIRouter(prefix="/usuarios", tags=["Autenticacao"])


@router.get("/me", response_model=UsuarioResposta)
def meus_dados(usuario: UsuarioAtual):
    return usuario


@router.post("/registrar", response_model=UsuarioResposta, status_code=201)
def registrar(dados: UsuarioEntrada, session: SessionDep):
    email_em_uso = session.query(Usuario).filter(Usuario.email == dados.email).first()
    if email_em_uso is not None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email ja cadastrado")

    usuario = Usuario(email=dados.email, hashed_password=gerar_hash(dados.senha))
    session.add(usuario)
    session.commit()
    return usuario


@router.post("/token", response_model=Token)
def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], session: SessionDep):
    usuario = session.query(Usuario).filter(Usuario.email == form_data.username).first()
    if usuario is None or not verificar_senha(form_data.password, usuario.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email ou senha invalidos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    token = criar_token({"sub": usuario.email})
    return Token(access_token=token, token_type="bearer")


@router.put("/senha", status_code=204)
def trocar_senha(dados: SenhaAtualizar, usuario: UsuarioAtual, session: SessionDep):
    if not verificar_senha(dados.senha_atual, usuario.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Senha atual incorreta")

    usuario.hashed_password = gerar_hash(dados.senha_nova)
    session.commit()


@router.delete("/me", status_code=204)
def deletar_minha_conta(session: SessionDep, usuario: UsuarioAtual):
    session.delete(usuario)
    session.commit()
