from typing import Optional

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base
from models.enums import Situacao


class Formacoes(Base):
    __tablename__ = "formacoes"

    id: Mapped[int] = mapped_column(primary_key=True)
    curso: Mapped[str]
    instituicao: Mapped[str]
    ano_inicio: Mapped[int]
    ano_conclusao: Mapped[Optional[int]]
    situacao: Mapped[Situacao]

    curriculo_id: Mapped[int] = mapped_column(ForeignKey("curriculos.id"))

    curriculo: Mapped["Curriculo"] = relationship(back_populates="formacoes")
