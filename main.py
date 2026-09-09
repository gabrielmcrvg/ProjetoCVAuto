from fastapi import FastAPI

from database import Base, engine
from routers import auth, certificado, curriculo, experiencia, formacao, habilidade, idioma, projeto

Base.metadata.create_all(bind=engine)

app = FastAPI(title="CVAuto")

app.include_router(auth.router)
app.include_router(certificado.router)
app.include_router(curriculo.router)
app.include_router(experiencia.router)
app.include_router(formacao.router)
app.include_router(habilidade.router)
app.include_router(idioma.router)
app.include_router(projeto.router)

