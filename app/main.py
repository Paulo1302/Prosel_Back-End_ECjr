from fastapi import FastAPI
from app.db import models, database
from app.routers import empresa, auth

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(
    title="API de Gerenciamento de Empresas Clientes",
    description="Uma API profissional para gerenciar empresas clientes, com autenticação e segurança.",
    version="3.0.0"
)

app.include_router(auth.router)
app.include_router(empresa.router)

@app.get("/", tags=["Root"])
def read_root():
    return {"message": "Bem-vindo à API de Gerenciamento de Empresas!"}