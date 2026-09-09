from fastapi import APIRouter, HTTPException, status

from database import SessionDep
from models.projetos import Projetos
from schemas.ia import TextoSugerido
from schemas.projeto import ProjetoAtualizar, ProjetoEntrada, ProjetoResposta
from seguranca import CurriculoDoUsuario
from services.gemini import reescrever_texto
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


@router.post("/{projeto_id}/reescrever", response_model=TextoSugerido)
def reescrever_projeto(projeto: ProjetoDoUsuario):
    try:
        texto_sugerido = reescrever_texto(projeto.descricao)
    except Exception as erro:
        print(f"[IA] Erro ao chamar o Gemini: {erro}")
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="Erro ao se comunicar com o servico de IA",
        )
    return TextoSugerido(texto_sugerido=texto_sugerido)


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
