from fastapi import APIRouter, HTTPException, status

from database import SessionDep
from models.habilidades import Habilidades
from schemas.habilidade import HabilidadeAtualizar, HabilidadeEntrada, HabilidadeResposta
from schemas.ia import SugestaoCategoria
from seguranca import CurriculoDoUsuario
from services.gemini import categorizar_habilidades
from utils.dependencias import HabilidadeDoUsuario

router = APIRouter(prefix="/curriculos/{curriculo_id}/habilidades", tags=["Habilidades"])


@router.get("/", response_model=list[HabilidadeResposta])
def listar_habilidades(curriculo: CurriculoDoUsuario):
    return curriculo.habilidades


@router.get("/{habilidade_id}", response_model=HabilidadeResposta)
def buscar_habilidade(habilidade: HabilidadeDoUsuario):
    return habilidade


@router.post("/", response_model=HabilidadeResposta, status_code=201)
def criar_habilidade(dados: HabilidadeEntrada, curriculo: CurriculoDoUsuario, session: SessionDep):
    habilidade = Habilidades(**dados.model_dump(), curriculo_id=curriculo.id)
    session.add(habilidade)
    session.commit()
    return habilidade


@router.post("/categorizar", response_model=list[SugestaoCategoria])
def categorizar(curriculo: CurriculoDoUsuario):
    pendentes = [h for h in curriculo.habilidades if h.categoria is None]
    if not pendentes:
        return []

    try:
        sugestoes = categorizar_habilidades({h.id: h.nome for h in pendentes})
    except Exception as erro:
        print(f"[IA] Erro ao chamar o Gemini: {erro}")
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="Erro ao se comunicar com o servico de IA",
        )
    return sugestoes


@router.patch("/{habilidade_id}", response_model=HabilidadeResposta)
def atualizar_habilidade(dados: HabilidadeAtualizar, habilidade: HabilidadeDoUsuario, session: SessionDep):
    for campo, valor in dados.model_dump(exclude_unset=True).items():
        setattr(habilidade, campo, valor)
    session.commit()
    return habilidade


@router.delete("/{habilidade_id}", status_code=204)
def deletar_habilidade(habilidade: HabilidadeDoUsuario, session: SessionDep):
    session.delete(habilidade)
    session.commit()
