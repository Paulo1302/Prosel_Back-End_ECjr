# Importa a classe FastAPI, que é o núcleo do framework.
from fastapi import FastAPI

# Importa os módulos internos necessários para a aplicação.
# - 'models': Contém as classes que definem as tabelas da base de dados (ORM).
# - 'database': Contém a configuração da engine e da sessão da base de dados.
# - 'empresa' e 'auth': São os módulos de routers que contêm os endpoints da API.
from app.db import models, database
from app.routers import empresa, auth

# Inicialização da base de dados.
# Ele instrui o SQLAlchemy a criar todas as tabelas definidas em 'app/db/models.py'
# (que herdam de 'database.Base') na base de dados conectada, caso elas ainda não existam.
models.Base.metadata.create_all(bind=database.engine)

# Cria a instância principal da aplicação FastAPI.
# Todos os endpoints, configurações e middlewares serão associados a esta variável 'app'.
app = FastAPI(
    # Metadados para a documentação automática (Swagger UI / ReDoc).
    title="API de Gestão de Empresas Clentes",
    description="Uma API profissional para gerir empresas clientes, com autenticação e segurança.",
    version="3.0.0"
)

# Inclui os routers na aplicação principal.
# Esta é a forma organizada de adicionar todos os endpoints definidos em outros ficheiros.
# O router de 'auth' contém os endpoints públicos /register e /login.
app.include_router(auth.router)
# O router de 'empresa' contém todos os endpoints de CRUD para /empresas.
app.include_router(empresa.router)

# Define um endpoint para a raiz da API ("/")
# É útil para verificar rapidamente se a API está a funcionar.
@app.get("/", tags=["Root"])
def read_root():
    """
    Endpoint raiz para verificar o estado da API.
    Retorna uma mensagem de boas-vindas.
    """
    return {"message": "Bem-vindo à API de Gestão de Empresas!"}
