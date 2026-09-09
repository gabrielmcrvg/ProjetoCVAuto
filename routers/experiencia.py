from fastapi import APIRouter

from database import SessionDep
from models.experiencias import Experiencias
from schemas.experiencia import ExperienciaAtualizar, ExperienciaEntrada, ExperienciaResposta
from seguranca import CurriculoDoUsuario
from utils.dependencias import ExperienciaDoUsuario

router = APIRouter(prefix="/curriculos/{curriculo_id}/experiencias", tags=["Experiencias"])


@router.get("/", response_model=list[ExperienciaResposta])
def listar_experiencias(curriculo: CurriculoDoUsuario):
    return curriculo.experiencias


@router.get("/{experiencia_id}", response_model=ExperienciaResposta)
def buscar_experiencia(experiencia: ExperienciaDoUsuario):
    return experiencia


@router.post("/", response_model=ExperienciaResposta, status_code=201)
def criar_experiencia(dados: ExperienciaEntrada, curriculo: CurriculoDoUsuario, session: SessionDep):
    experiencia = Experiencias(**dados.model_dump(), curriculo_id=curriculo.id)
    session.add(experiencia)
    session.commit()
    return experiencia


@router.patch("/{experiencia_id}", response_model=ExperienciaResposta)
def atualizar_experiencia(dados: ExperienciaAtualizar, experiencia: ExperienciaDoUsuario, session: SessionDep):
    for campo, valor in dados.model_dump(exclude_unset=True).items():
        setattr(experiencia, campo, valor)
    session.commit()
    return experiencia


@router.delete("/{experiencia_id}", status_code=204)
def deletar_experiencia(experiencia: ExperienciaDoUsuario, session: SessionDep):
    session.delete(experiencia)
    session.commit()
