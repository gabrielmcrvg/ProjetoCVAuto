from fastapi import APIRouter, HTTPException, status

from database import SessionDep
from models.experiencias import Experiencias
from schemas.experiencia import ExperienciaAtualizar, ExperienciaEntrada, ExperienciaResposta
from schemas.ia import TextoSugerido
from seguranca import CurriculoDoUsuario
from services.gemini import reescrever_texto
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


@router.post("/{experiencia_id}/reescrever", response_model=TextoSugerido)
def reescrever_experiencia(experiencia: ExperienciaDoUsuario):
    try:
        texto_sugerido = reescrever_texto(experiencia.descricao)
    except Exception as erro:
        print(f"[IA] Erro ao chamar o Gemini: {erro}")
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="Erro ao se comunicar com o servico de IA",
        )
    return TextoSugerido(texto_sugerido=texto_sugerido)


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
