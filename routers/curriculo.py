from fastapi import APIRouter

from database import SessionDep
from models.curriculos import Curriculo
from schemas.curriculo import CurriculoAtualizar, CurriculoCompleto, CurriculoEntrada, CurriculoResposta
from seguranca import CurriculoDoUsuario, UsuarioAtual

router = APIRouter(prefix="/curriculos", tags=["Curriculos"])


@router.get("/", response_model=list[CurriculoResposta])
def listar_meus_curriculos(usuario: UsuarioAtual, session: SessionDep):
    return session.query(Curriculo).filter(Curriculo.usuario_id == usuario.id).all()


@router.get("/{curriculo_id}", response_model=CurriculoCompleto)
def buscar_curriculo(curriculo: CurriculoDoUsuario):
    return curriculo


@router.post("/", response_model=CurriculoResposta, status_code=201)
def criar_curriculo(dados: CurriculoEntrada, usuario: UsuarioAtual, session: SessionDep):
    curriculo = Curriculo(**dados.model_dump(), usuario_id=usuario.id)
    session.add(curriculo)
    session.commit()
    return curriculo


@router.patch("/{curriculo_id}", response_model=CurriculoResposta)
def atualizar_curriculo(dados: CurriculoAtualizar, curriculo: CurriculoDoUsuario, session: SessionDep):
    for campo, valor in dados.model_dump(exclude_unset=True).items():
        setattr(curriculo, campo, valor)
    session.commit()
    return curriculo


@router.delete("/{curriculo_id}", status_code=204)
def deletar_curriculo(curriculo: CurriculoDoUsuario, session: SessionDep):
    session.delete(curriculo)
    session.commit()
