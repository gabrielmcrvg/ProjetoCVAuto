import os

from dotenv import load_dotenv
from google import genai
from google.genai import types

from schemas.ia import SugestaoCategoria

load_dotenv()

MODELO = "gemini-3.6-flash"

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY"),
    http_options=types.HttpOptions(
        retry_options=types.HttpRetryOptions(
            attempts=8,
            initial_delay=2.0,
            max_delay=30.0,
        )
    ),
)

INSTRUCAO_REESCREVER = (
    "Voce e um assistente que melhora textos de curriculos profissionais, escritos em portugues. "
    "Corrija erros de gramatica e ortografia, e deixe o texto com um tom mais profissional e claro. "
    "Nao invente informacoes, numeros ou fatos que nao estejam no texto original. "
    "Mantenha a resposta em portugues. "
    "Responda apenas com o texto reescrito, sem nenhum comentario ou explicacao adicional."
)

INSTRUCAO_CATEGORIZAR = (
    "Voce recebe uma lista de habilidades de um curriculo, cada uma identificada por um id numerico e um nome. "
    "Para cada habilidade, escolha a categoria mais adequada dentre as opcoes disponiveis no schema de resposta. "
    "Nao invente categorias alem das fornecidas no schema. "
    "Responda com uma lista cobrindo todas as habilidades recebidas, contendo o id de cada uma e a categoria escolhida."
)


def reescrever_texto(texto: str) -> str:
    resposta = client.models.generate_content(
        model=MODELO,
        contents=texto,
        config=types.GenerateContentConfig(
            system_instruction=INSTRUCAO_REESCREVER,
        ),
    )
    return resposta.text


def categorizar_habilidades(habilidades: dict[int, str]) -> list[SugestaoCategoria]:
    texto_entrada = "\n".join(f"id={hid}: {nome}" for hid, nome in habilidades.items())
    resposta = client.models.generate_content(
        model=MODELO,
        contents=texto_entrada,
        config=types.GenerateContentConfig(
            system_instruction=INSTRUCAO_CATEGORIZAR,
            response_mime_type="application/json",
            response_schema=list[SugestaoCategoria],
        ),
    )
    if resposta.parsed is None:
        raise ValueError("A IA nao retornou um resultado no formato esperado")
    return resposta.parsed
