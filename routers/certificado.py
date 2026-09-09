from fastapi import APIRouter

from database import SessionDep
from models.certificados import Certificados
from models.enums import Situacao
from schemas.certificado import CertificadoAtualizar, CertificadoEntrada, CertificadoResposta
from seguranca import CurriculoDoUsuario
from utils.dependencias import CertificadoDoUsuario

router = APIRouter(prefix="/curriculos/{curriculo_id}/certificados", tags=["Certificados"])


@router.get("/", response_model=list[CertificadoResposta])
def listar_certificados(curriculo: CurriculoDoUsuario):
    return curriculo.certificados


@router.get("/{certificado_id}", response_model=CertificadoResposta)
def buscar_certificado(certificado: CertificadoDoUsuario):
    return certificado


@router.post("/", response_model=CertificadoResposta, status_code=201)
def criar_certificado(dados: CertificadoEntrada, curriculo: CurriculoDoUsuario, session: SessionDep):
    certificado = Certificados(**dados.model_dump(), curriculo_id=curriculo.id, situacao=Situacao.CONCLUIDO)
    session.add(certificado)
    session.commit()
    return certificado


@router.patch("/{certificado_id}", response_model=CertificadoResposta)
def atualizar_certificado(dados: CertificadoAtualizar, certificado: CertificadoDoUsuario, session: SessionDep):
    for campo, valor in dados.model_dump(exclude_unset=True).items():
        setattr(certificado, campo, valor)
    session.commit()
    return certificado


@router.delete("/{certificado_id}", status_code=204)
def deletar_certificado(certificado: CertificadoDoUsuario, session: SessionDep):
    session.delete(certificado)
    session.commit()
