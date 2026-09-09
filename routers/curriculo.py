from fastapi import APIRouter, HTTPException, Response, status

from database import SessionDep
from models.curriculos import Curriculo
from schemas.curriculo import CurriculoAtualizar, CurriculoCompleto, CurriculoEntrada, CurriculoResposta
from schemas.ia import TextoSugerido
from seguranca import CurriculoDoUsuario, UsuarioAtual
from services.gemini import reescrever_texto
from services.pdf import gerar_pdf

router = APIRouter(prefix="/curriculos", tags=["Curriculos"])


@router.get("/", response_model=list[CurriculoResposta])
def listar_meus_curriculos(usuario: UsuarioAtual, session: SessionDep):
    return session.query(Curriculo).filter(Curriculo.usuario_id == usuario.id).all()


@router.get("/{curriculo_id}", response_model=CurriculoCompleto)
def buscar_curriculo(curriculo: CurriculoDoUsuario):
    return curriculo


@router.get("/{curriculo_id}/pdf")
def baixar_pdf(curriculo: CurriculoDoUsuario):
    pdf_bytes = gerar_pdf(curriculo)
    nome_arquivo = f"curriculo_{curriculo.id}.pdf"
    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={"Content-Disposition": f'attachment; filename="{nome_arquivo}"'},
    )


@router.post("/", response_model=CurriculoResposta, status_code=201)
def criar_curriculo(dados: CurriculoEntrada, usuario: UsuarioAtual, session: SessionDep):
    curriculo = Curriculo(**dados.model_dump(), usuario_id=usuario.id)
    session.add(curriculo)
    session.commit()
    return curriculo


@router.post("/{curriculo_id}/reescrever-resumo", response_model=TextoSugerido)
def reescrever_resumo(curriculo: CurriculoDoUsuario):
    try:
        texto_sugerido = reescrever_texto(curriculo.resumo_profissional)
    except Exception as erro:
        print(f"[IA] Erro ao chamar o Gemini: {erro}")
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="Erro ao se comunicar com o servico de IA",
        )
    return TextoSugerido(texto_sugerido=texto_sugerido)


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
