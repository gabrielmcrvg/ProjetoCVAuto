from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base


class Idiomas(Base):
    __tablename__ = "idiomas"

    id: Mapped[int] = mapped_column(primary_key=True)
    nome: Mapped[str]
    nivel: Mapped[str]

    curriculo_id: Mapped[int] = mapped_column(ForeignKey("curriculos.id"))

    curriculo: Mapped["Curriculo"] = relationship(back_populates="idiomas")
