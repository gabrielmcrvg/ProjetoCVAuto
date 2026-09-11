from datetime import date

from database import Base, SessionLocal, engine
from models.certificados import Certificados
from models.curriculos import Curriculo
from models.enums import CategoriaHabilidade, Situacao, SituacaoCertificado
from models.experiencias import Experiencias
from models.formacoes import Formacoes
from models.habilidades import Habilidades
from models.idiomas import Idiomas
from models.projetos import Projetos
from models.usuarios import Usuario
from seguranca import gerar_hash

Base.metadata.create_all(bind=engine)

session = SessionLocal()

EMAIL = "teste@teste.com"
SENHA = "senha123"

usuario_existente = session.query(Usuario).filter(Usuario.email == EMAIL).first()
if usuario_existente is not None:
    print(f"Usuario '{EMAIL}' ja existe (id={usuario_existente.id}). Nada foi criado, pra nao duplicar.")
    session.close()
    raise SystemExit

usuario = Usuario(email=EMAIL, hashed_password=gerar_hash(SENHA))
session.add(usuario)
session.commit()
session.refresh(usuario)

curriculo = Curriculo(
    titulo="Curriculo Backend Python",
    resumo_profissional=(
        "Estudante de backend, cursando o Tecnico em Desenvolvimento de Sistemas pelo SENAI, "
        "com foco em construcao de APIs REST usando FastAPI e SQLAlchemy. "
        "Experiencia pratica com modelagem de banco de dados relacional, autenticacao via JWT "
        "e organizacao de codigo em camadas. "
        "Venho me aprofundando tambem em integracao com IA, aplicando modelos de linguagem "
        "para automatizar tarefas como revisao de texto e categorizacao de dados."
    ),
    nome_completo="Gabriel Mercon de Oliveira",
    localizacao="Brasil",
    telefone="11999999999",
    url_1="https://github.com/gabmercon",
    url_2="https://linkedin.com/in/gabmercon",
    usuario_id=usuario.id,
)
session.add(curriculo)
session.commit()
session.refresh(curriculo)

session.add(Experiencias(
    cargo="Estagiario Backend",
    empresa="Empresa Teste",
    data_inicio=date(2025, 1, 1),
    data_fim=None,
    descricao="Desenvolvimento de APIs com FastAPI e SQLAlchemy.\nImplementacao de autenticacao via JWT.",
    curriculo_id=curriculo.id,
))

session.add(Formacoes(
    curso="Tecnico em Desenvolvimento de Sistemas",
    instituicao="SENAI",
    ano_inicio=2024,
    ano_conclusao=None,
    situacao=Situacao.EM_ANDAMENTO,
    curriculo_id=curriculo.id,
))

session.add(Habilidades(nome="Python", categoria=CategoriaHabilidade.LINGUAGENS_PROGRAMACAO, curriculo_id=curriculo.id))
session.add(Habilidades(nome="FastAPI", categoria=CategoriaHabilidade.FRAMEWORKS_BIBLIOTECAS, curriculo_id=curriculo.id))
session.add(Habilidades(nome="Docker", categoria=None, curriculo_id=curriculo.id))

session.add(Idiomas(nome="Ingles", nivel="Intermediario", curriculo_id=curriculo.id))

session.add(Projetos(
    nome="Criador de Curriculo com IA",
    contexto="Projeto pessoal de portfolio",
    tecnologias="FastAPI, SQLAlchemy, SQLite, Gemini API",
    descricao="API que gera curriculos em PDF, com IA para reescrever textos e categorizar habilidades.",
    link="https://github.com/gabmercon/curriculo-ia",
    curriculo_id=curriculo.id,
))

session.add(Certificados(
    nome="Introducao a APIs REST",
    instituicao="Alura",
    carga_horaria=20,
    situacao=SituacaoCertificado.CONCLUIDO,
    periodo="2025",
    curriculo_id=curriculo.id,
))

session.commit()
session.close()

print("Seed concluido!")
print(f"Login -> email: {EMAIL} | senha: {SENHA}")
print(f"Curriculo criado com id: {curriculo.id}")
