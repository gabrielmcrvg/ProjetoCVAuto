from database import Base, engine
import models.certificados
import models.curriculos
import models.experiencias
import models.formacoes
import models.habilidades
import models.idiomas
import models.projetos
import models.usuarios

Base.metadata.create_all(bind=engine)