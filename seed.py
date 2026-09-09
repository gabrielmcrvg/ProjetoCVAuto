from datetime import date

from database import Base, SessionLocal, engine
from models.certificados import Certificados
from models.curriculos import Curriculo
from models.enums import CategoriaHabilidade, Situacao
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
        "Estudante de backend, cursando SENAI, com foco em FastAPI e APIs REST. "
        "Experiencia com modelagem de banco de dados, autenticacao e integracao com IA."
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

# ----- Experiencias -----
session.add(Experiencias(
    cargo="Estagiario Backend",
    empresa="Empresa Teste",
    data_inicio=date(2025, 1, 1),
    data_fim=None,
    descricao=(
        "Desenvolvimento de APIs com FastAPI e SQLAlchemy.\n"
        "Implementacao de autenticacao via JWT.\n"
        "Participacao em revisao de codigo e testes das rotas."
    ),
    curriculo_id=curriculo.id,
))

session.add(Experiencias(
    cargo="Desenvolvedor Junior (Freelance)",
    empresa="Autonomo",
    data_inicio=date(2024, 6, 1),
    data_fim=date(2024, 12, 31),
    descricao=(
        "Criacao de pequenos sistemas web sob demanda para clientes locais.\n"
        "Modelagem de banco de dados relacional e integracao com APIs externas."
    ),
    curriculo_id=curriculo.id,
))

session.add(Experiencias(
    cargo="Suporte Tecnico",
    empresa="Loja de Informatica Central",
    data_inicio=date(2023, 3, 1),
    data_fim=date(2024, 5, 31),
    descricao=(
        "Atendimento e diagnostico de problemas em computadores e redes.\n"
        "Manutencao preventiva e corretiva de hardware e software."
    ),
    curriculo_id=curriculo.id,
))

# ----- Formacoes -----
session.add(Formacoes(
    curso="Tecnico em Desenvolvimento de Sistemas",
    instituicao="SENAI",
    ano_inicio=2024,
    ano_conclusao=None,
    situacao=Situacao.EM_ANDAMENTO,
    curriculo_id=curriculo.id,
))

session.add(Formacoes(
    curso="Ensino Medio",
    instituicao="Escola Estadual Exemplo",
    ano_inicio=2021,
    ano_conclusao=2023,
    situacao=Situacao.CONCLUIDO,
    curriculo_id=curriculo.id,
))

# ----- Habilidades -----
session.add(Habilidades(nome="Python", categoria=CategoriaHabilidade.LINGUAGENS_PROGRAMACAO, curriculo_id=curriculo.id))
session.add(Habilidades(nome="SQL", categoria=CategoriaHabilidade.LINGUAGENS_PROGRAMACAO, curriculo_id=curriculo.id))
session.add(Habilidades(nome="FastAPI", categoria=CategoriaHabilidade.FRAMEWORKS_BIBLIOTECAS, curriculo_id=curriculo.id))
session.add(Habilidades(nome="SQLAlchemy", categoria=CategoriaHabilidade.FRAMEWORKS_BIBLIOTECAS, curriculo_id=curriculo.id))
session.add(Habilidades(nome="PostgreSQL", categoria=CategoriaHabilidade.BANCO_DE_DADOS, curriculo_id=curriculo.id))
session.add(Habilidades(nome="SQLite", categoria=CategoriaHabilidade.BANCO_DE_DADOS, curriculo_id=curriculo.id))
session.add(Habilidades(nome="Git", categoria=CategoriaHabilidade.METODOLOGIAS_PROCESSOS, curriculo_id=curriculo.id))
session.add(Habilidades(nome="Scrum", categoria=CategoriaHabilidade.METODOLOGIAS_PROCESSOS, curriculo_id=curriculo.id))
session.add(Habilidades(nome="Docker", categoria=None, curriculo_id=curriculo.id))
session.add(Habilidades(nome="Linux", categoria=None, curriculo_id=curriculo.id))

# ----- Idiomas -----
session.add(Idiomas(nome="Ingles", nivel="Intermediario", curriculo_id=curriculo.id))
session.add(Idiomas(nome="Espanhol", nivel="Basico", curriculo_id=curriculo.id))

# ----- Projetos -----
session.add(Projetos(
    nome="Criador de Curriculo com IA",
    contexto="Projeto pessoal de portfolio",
    tecnologias="FastAPI, SQLAlchemy, SQLite, Gemini API",
    descricao=(
        "API que gera curriculos em PDF, com IA para reescrever textos e categorizar habilidades.\n"
        "Autenticacao via JWT e controle de propriedade dos recursos por usuario."
    ),
    link="https://github.com/gabmercon/curriculo-ia",
    curriculo_id=curriculo.id,
))

session.add(Projetos(
    nome="E-Commerce API",
    contexto="Projeto de portfolio",
    tecnologias="FastAPI, SQLAlchemy, JWT",
    descricao=(
        "API de loja virtual com cadastro de produtos, clientes e pedidos.\n"
        "Autenticacao de administradores e clientes com niveis de permissao distintos."
    ),
    link="https://github.com/gabmercon/ecommerce-api",
    curriculo_id=curriculo.id,
))

session.add(Projetos(
    nome="Automacao de Tarefas com Python",
    contexto="Projeto pessoal de estudo",
    tecnologias="Python, Selenium, Pandas",
    descricao="Script para automatizar coleta e organizacao de dados em planilhas.",
    link=None,
    curriculo_id=curriculo.id,
))

# ----- Certificados -----
session.add(Certificados(
    nome="Introducao a APIs REST",
    instituicao="Alura",
    carga_horaria=20,
    situacao=Situacao.CONCLUIDO,
    periodo="2025",
    curriculo_id=curriculo.id,
))

session.add(Certificados(
    nome="Python para Backend",
    instituicao="Alura",
    carga_horaria=40,
    situacao=Situacao.CONCLUIDO,
    periodo="2024",
    curriculo_id=curriculo.id,
))

session.add(Certificados(
    nome="Fundamentos de Banco de Dados",
    instituicao="SENAI",
    carga_horaria=30,
    situacao=Situacao.CONCLUIDO,
    periodo="2024",
    curriculo_id=curriculo.id,
))

session.commit()
session.close()

print("Seed concluido!")
print(f"Login -> email: {EMAIL} | senha: {SENHA}")
print(f"Curriculo criado com id: {curriculo.id}")
print("Obs: as habilidades 'Docker' e 'Linux' foram criadas sem categoria, de proposito, pra testar o /categorizar.")
