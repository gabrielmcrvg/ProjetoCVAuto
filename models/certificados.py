from typing import Optional

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base
from models.enums import SituacaoCertificado


class Certificados(Base):
    __tablename__ = "certificados"

    id: Mapped[int] = mapped_column(primary_key=True)
    nome: Mapped[str]
    instituicao: Mapped[str]
    carga_horaria: Mapped[Optional[int]]
    situacao: Mapped[SituacaoCertificado]
    periodo: Mapped[str]
    arquivo_path: Mapped[Optional[str]]

    curriculo_id: Mapped[int] = mapped_column(ForeignKey("curriculos.id"))

    curriculo: Mapped["Curriculo"] = relationship(back_populates="certificados")
