from typing import Optional

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base


class Projetos(Base):
    __tablename__ = "projetos"

    id: Mapped[int] = mapped_column(primary_key=True)
    nome: Mapped[str]
    contexto: Mapped[str]
    tecnologias: Mapped[str]
    descricao: Mapped[str]
    link: Mapped[Optional[str]]

    curriculo_id: Mapped[int] = mapped_column(ForeignKey("curriculos.id"))

    curriculo: Mapped["Curriculo"] = relationship(back_populates="projetos")
