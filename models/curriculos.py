from typing import Optional

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base


class Curriculo(Base):
    __tablename__ = "curriculos"

    id: Mapped[int] = mapped_column(primary_key=True)
    titulo: Mapped[str]
    resumo_profissional: Mapped[str]

    nome_completo: Mapped[str]
    localizacao: Mapped[str]
    telefone: Mapped[str]
    url_1: Mapped[Optional[str]]
    url_2: Mapped[Optional[str]]

    usuario_id: Mapped[int] = mapped_column(ForeignKey("usuarios.id"))

    usuario: Mapped["Usuario"] = relationship(back_populates="curriculos")
    experiencias: Mapped[list["Experiencias"]] = relationship(back_populates="curriculo", cascade="all, delete-orphan")
    formacoes: Mapped[list["Formacoes"]] = relationship(back_populates="curriculo", cascade="all, delete-orphan")
    habilidades: Mapped[list["Habilidades"]] = relationship(back_populates="curriculo", cascade="all, delete-orphan")
    idiomas: Mapped[list["Idiomas"]] = relationship(back_populates="curriculo", cascade="all, delete-orphan")
    projetos: Mapped[list["Projetos"]] = relationship(back_populates="curriculo", cascade="all, delete-orphan")
    certificados: Mapped[list["Certificados"]] = relationship(back_populates="curriculo", cascade="all, delete-orphan")
