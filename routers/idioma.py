from fastapi import APIRouter

from database import SessionDep
from models.idiomas import Idiomas
from schemas.idioma import IdiomaAtualizar, IdiomaEntrada, IdiomaResposta
from seguranca import CurriculoDoUsuario
from utils.dependencias import IdiomaDoUsuario

router = APIRouter(prefix="/curriculos/{curriculo_id}/idiomas", tags=["Idiomas"])


@router.get("/", response_model=list[IdiomaResposta])
def listar_idiomas(curriculo: CurriculoDoUsuario):
    return curriculo.idiomas


@router.get("/{idioma_id}", response_model=IdiomaResposta)
def buscar_idioma(idioma: IdiomaDoUsuario):
    return idioma


@router.post("/", response_model=IdiomaResposta, status_code=201)
def criar_idioma(dados: IdiomaEntrada, curriculo: CurriculoDoUsuario, session: SessionDep):
    idioma = Idiomas(**dados.model_dump(), curriculo_id=curriculo.id)
    session.add(idioma)
    session.commit()
    return idioma


@router.patch("/{idioma_id}", response_model=IdiomaResposta)
def atualizar_idioma(dados: IdiomaAtualizar, idioma: IdiomaDoUsuario, session: SessionDep):
    for campo, valor in dados.model_dump(exclude_unset=True).items():
        setattr(idioma, campo, valor)
    session.commit()
    return idioma


@router.delete("/{idioma_id}", status_code=204)
def deletar_idioma(idioma: IdiomaDoUsuario, session: SessionDep):
    session.delete(idioma)
    session.commit()
