from typing import Optional

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base
from models.enums import CategoriaHabilidade


class Habilidades(Base):
    __tablename__ = "habilidades"

    id: Mapped[int] = mapped_column(primary_key=True)
    nome: Mapped[str]
    categoria: Mapped[Optional[CategoriaHabilidade]]

    curriculo_id: Mapped[int] = mapped_column(ForeignKey("curriculos.id"))

    curriculo: Mapped["Curriculo"] = relationship(back_populates="habilidades")
