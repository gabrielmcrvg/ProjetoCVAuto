from typing import Annotated

from fastapi import Depends, HTTPException, status

from database import SessionDep
from models.certificados import Certificados
from models.experiencias import Experiencias
from models.formacoes import Formacoes
from models.habilidades import Habilidades
from models.idiomas import Idiomas
from models.projetos import Projetos
from seguranca import CurriculoDoUsuario


def dono_da_experiencia(experiencia_id: int, curriculo: CurriculoDoUsuario, session: SessionDep) -> Experiencias:
    experiencia = session.query(Experiencias).filter(Experiencias.id == experiencia_id).first()
    if experiencia is None or experiencia.curriculo_id != curriculo.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Experiencia nao encontrada")
    return experiencia


ExperienciaDoUsuario = Annotated[Experiencias, Depends(dono_da_experiencia)]


def dono_da_formacao(formacao_id: int, curriculo: CurriculoDoUsuario, session: SessionDep) -> Formacoes:
    formacao = session.query(Formacoes).filter(Formacoes.id == formacao_id).first()
    if formacao is None or formacao.curriculo_id != curriculo.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Formacao nao encontrada")
    return formacao


FormacaoDoUsuario = Annotated[Formacoes, Depends(dono_da_formacao)]


def dono_da_habilidade(habilidade_id: int, curriculo: CurriculoDoUsuario, session: SessionDep) -> Habilidades:
    habilidade = session.query(Habilidades).filter(Habilidades.id == habilidade_id).first()
    if habilidade is None or habilidade.curriculo_id != curriculo.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Habilidade nao encontrada")
    return habilidade


HabilidadeDoUsuario = Annotated[Habilidades, Depends(dono_da_habilidade)]


def dono_do_idioma(idioma_id: int, curriculo: CurriculoDoUsuario, session: SessionDep) -> Idiomas:
    idioma = session.query(Idiomas).filter(Idiomas.id == idioma_id).first()
    if idioma is None or idioma.curriculo_id != curriculo.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Idioma nao encontrado")
    return idioma


IdiomaDoUsuario = Annotated[Idiomas, Depends(dono_do_idioma)]


def dono_do_projeto(projeto_id: int, curriculo: CurriculoDoUsuario, session: SessionDep) -> Projetos:
    projeto = session.query(Projetos).filter(Projetos.id == projeto_id).first()
    if projeto is None or projeto.curriculo_id != curriculo.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Projeto nao encontrado")
    return projeto


ProjetoDoUsuario = Annotated[Projetos, Depends(dono_do_projeto)]


def dono_do_certificado(certificado_id: int, curriculo: CurriculoDoUsuario, session: SessionDep) -> Certificados:
    certificado = session.query(Certificados).filter(Certificados.id == certificado_id).first()
    if certificado is None or certificado.curriculo_id != curriculo.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Certificado nao encontrado")
    return certificado


CertificadoDoUsuario = Annotated[Certificados, Depends(dono_do_certificado)]
