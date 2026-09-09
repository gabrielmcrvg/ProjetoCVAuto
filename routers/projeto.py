from fastapi import APIRouter

from database import SessionDep
from models.projetos import Projetos
from schemas.projeto import ProjetoAtualizar, ProjetoEntrada, ProjetoResposta
from seguranca import CurriculoDoUsuario
from utils.dependencias import ProjetoDoUsuario

router = APIRouter(prefix="/curriculos/{curriculo_id}/projetos", tags=["Projetos"])


@router.get("/", response_model=list[ProjetoResposta])
def listar_projetos(curriculo: CurriculoDoUsuario):
    return curriculo.projetos


@router.get("/{projeto_id}", response_model=ProjetoResposta)
def buscar_projeto(projeto: ProjetoDoUsuario):
    return projeto


@router.post("/", response_model=ProjetoResposta, status_code=201)
def criar_projeto(dados: ProjetoEntrada, curriculo: CurriculoDoUsuario, session: SessionDep):
    projeto = Projetos(**dados.model_dump(), curriculo_id=curriculo.id)
    session.add(projeto)
    session.commit()
    return projeto


@router.patch("/{projeto_id}", response_model=ProjetoResposta)
def atualizar_projeto(dados: ProjetoAtualizar, projeto: ProjetoDoUsuario, session: SessionDep):
    for campo, valor in dados.model_dump(exclude_unset=True).items():
        setattr(projeto, campo, valor)
    session.commit()
    return projeto


@router.delete("/{projeto_id}", status_code=204)
def deletar_projeto(projeto: ProjetoDoUsuario, session: SessionDep):
    session.delete(projeto)
    session.commit()
