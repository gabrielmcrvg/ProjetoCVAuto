from datetime import date
from typing import Optional

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base


class Experiencias(Base):
    __tablename__ = "experiencias"

    id: Mapped[int] = mapped_column(primary_key=True)
    cargo: Mapped[str]
    empresa: Mapped[str]
    data_inicio: Mapped[date]
    data_fim: Mapped[Optional[date]]
    descricao: Mapped[str]

    curriculo_id: Mapped[int] = mapped_column(ForeignKey("curriculos.id"))

    curriculo: Mapped["Curriculo"] = relationship(back_populates="experiencias")
