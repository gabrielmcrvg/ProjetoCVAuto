from fastapi import APIRouter

from database import SessionDep
from models.formacoes import Formacoes
from schemas.formacao import FormacaoAtualizar, FormacaoEntrada, FormacaoResposta
from seguranca import CurriculoDoUsuario
from utils.dependencias import FormacaoDoUsuario

router = APIRouter(prefix="/curriculos/{curriculo_id}/formacoes", tags=["Formacoes"])


@router.get("/", response_model=list[FormacaoResposta])
def listar_formacoes(curriculo: CurriculoDoUsuario):
    return curriculo.formacoes


@router.get("/{formacao_id}", response_model=FormacaoResposta)
def buscar_formacao(formacao: FormacaoDoUsuario):
    return formacao


@router.post("/", response_model=FormacaoResposta, status_code=201)
def criar_formacao(dados: FormacaoEntrada, curriculo: CurriculoDoUsuario, session: SessionDep):
    formacao = Formacoes(**dados.model_dump(), curriculo_id=curriculo.id)
    session.add(formacao)
    session.commit()
    return formacao


@router.patch("/{formacao_id}", response_model=FormacaoResposta)
def atualizar_formacao(dados: FormacaoAtualizar, formacao: FormacaoDoUsuario, session: SessionDep):
    for campo, valor in dados.model_dump(exclude_unset=True).items():
        setattr(formacao, campo, valor)
    session.commit()
    return formacao


@router.delete("/{formacao_id}", status_code=204)
def deletar_formacao(formacao: FormacaoDoUsuario, session: SessionDep):
    session.delete(formacao)
    session.commit()
