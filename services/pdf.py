from io import BytesIO
from pathlib import Path

from jinja2 import Environment, FileSystemLoader, select_autoescape
from xhtml2pdf import pisa

from models.curriculos import Curriculo

TEMPLATES_DIR = Path(__file__).resolve().parent.parent / "templates"

ambiente = Environment(
    loader=FileSystemLoader(TEMPLATES_DIR),
    autoescape=select_autoescape(["html"]),
)


def _dividir_em_linhas(texto: str) -> list[str]:
    linhas = [linha.strip() for linha in texto.splitlines() if linha.strip()]
    return linhas if linhas else [texto]


def _agrupar_habilidades(habilidades) -> dict[str, list[str]]:
    grupos: dict[str, list[str]] = {}
    for habilidade in habilidades:
        chave = habilidade.categoria.value if habilidade.categoria else "Outras"
        grupos.setdefault(chave, []).append(habilidade.nome)
    return grupos


def gerar_pdf(curriculo: Curriculo) -> bytes:
    contexto = {
        "curriculo": curriculo,
        "email": curriculo.usuario.email,
        "experiencias": [
            {
                "cargo": e.cargo,
                "empresa": e.empresa,
                "data_inicio": e.data_inicio,
                "data_fim": e.data_fim,
                "linhas": _dividir_em_linhas(e.descricao),
            }
            for e in curriculo.experiencias
        ],
        "formacoes": curriculo.formacoes,
        "projetos": [
            {
                "nome": p.nome,
                "contexto": p.contexto,
                "tecnologias": p.tecnologias,
                "link": p.link,
                "linhas": _dividir_em_linhas(p.descricao),
            }
            for p in curriculo.projetos
        ],
        "habilidades_agrupadas": _agrupar_habilidades(curriculo.habilidades),
        "certificados": curriculo.certificados,
        "idiomas": curriculo.idiomas,
    }

    template = ambiente.get_template("curriculo.html")
    html_renderizado = template.render(**contexto)

    pdf_buffer = BytesIO()
    resultado = pisa.CreatePDF(html_renderizado, dest=pdf_buffer)
    if resultado.err:
        raise ValueError("Erro ao gerar o PDF do curriculo")

    return pdf_buffer.getvalue()
