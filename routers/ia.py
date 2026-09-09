from fastapi import APIRouter, HTTPException, status

from schemas.ia import TextoEntrada, TextoSugerido
from seguranca import UsuarioAtual
from services.gemini import reescrever_texto

router = APIRouter(prefix="/ia", tags=["IA"])


@router.post("/reescrever", response_model=TextoSugerido)
def reescrever(dados: TextoEntrada, _usuario: UsuarioAtual):
    try:
        texto_sugerido = reescrever_texto(dados.texto)
    except Exception as erro:
        print(f"[IA] Erro ao chamar o Gemini: {erro}")
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="Erro ao se comunicar com o servico de IA",
        )
    return TextoSugerido(texto_sugerido=texto_sugerido)
