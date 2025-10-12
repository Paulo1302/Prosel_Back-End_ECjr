# API de Gestão de Empresas Clientes - Ecomp Jr.

## Sobre o Projeto

Esta API foi desenvolvida como parte de um processo seletivo para a Ecomp Jr., com o objetivo de criar um sistema centralizado para a gestão de empresas clientes. A aplicação resolve o desafio de manter informações consistentes e acessíveis, substituindo o uso de folhas de cálculo descentralizadas por uma solução robusta, escalável e segura.

O projeto foi construído em FastAPI, seguindo as melhores práticas de desenvolvimento de software, incluindo uma arquitetura em camadas (Repositories, Services, Routers) e segurança com **autenticação baseada em tokens JWT**.

---

## Funcionalidades

- **Autenticação de Administradores**: Sistema de registo (`/register`) e login (`/login`) para administradores.
- **Proteção de Rotas com JWT**: Todas as rotas de gestão de empresas (`/empresas`) são protegidas e exigem um token de autenticação válido.
- **CRUD Completo para Empresas**: Funcionalidades para Criar, Ler, Atualizar e Apagar empresas.
- **Consultas Avançadas**:
  - Filtragem de empresas por `cidade` e `ramo_atuacao`.
  - Pesquisa textual (parcial e insensível a maiúsculas/minúsculas) pelo `nome` da empresa.
- **Tratamento de Erros**: Respostas claras e códigos de status HTTP apropriados para validações de dados (CNPJ/email duplicado) e recursos não encontrados.
- **Arquitetura Profissional**: Código organizado no padrão Repository, Service e Router para separação de responsabilidades.
- **Gestão de Configurações**: Uso de variáveis de ambiente (`.env`) para proteger dados sensíveis.

---

## Tecnologias Utilizadas

- **Backend:**
  - [Python 3.10+](https://www.python.org/)
  - [FastAPI](https://fastapi.tiangolo.com/) - Framework web de alta performance.
  - [Uvicorn](https://www.uvicorn.org/) - Servidor ASGI.
- **Base de Dados:**
  - [PostgreSQL](https://www.postgresql.org/) - Base de dados relacional.
  - [SQLAlchemy](https://www.sqlalchemy.org/) - ORM para manipulação de dados em Python.
  - [Psycopg2](https://www.psycopg.org/docs/) - Driver de conexão com o PostgreSQL.
- **Segurança e Autenticação:**
  - [JWT (JSON Web Tokens)](https://jwt.io/)
  - [Passlib](https://passlib.readthedocs.io/en/stable/) com `bcrypt` para hashing de senhas.
  - [OAuth2](https://oauth.net/2/) Password Bearer Flow.
- **Validação e Configuração:**
  - [Pantic](https://pydantic-docs.helpmanual.io/)
  - [Python-Dotenv](https://pypi.org/project/python-dotenv/) - Para gestão de variáveis de ambiente.

---

## Como Executar o Projeto

Siga os passos abaixo para configurar e executar a aplicação no seu ambiente local.

### Pré-requisitos

- **Python 3.10** ou superior.
- **PostgreSQL** instalado e em execução.
- **Git** para clonar o repositório.

### 1. Clone o Repositório
```bash
git clone [https://github.com/Paulo1302/Prosel_Back-End_ECjr.git](https://github.com/Paulo1302/Prosel_Back-End_ECjr.git)
cd Prosel_Back-End_ECjr

2. Crie e Ative um Ambiente Virtual

É uma boa prática isolar as dependências do projeto.
Bash

# Criar o ambiente virtual
python -m venv venv

# Ativar no Windows
venv\Scripts\activate

# Ativar no macOS/Linux
source venv/bin/activate

3. Instale as Dependências

O ficheiro requirements.txt contém todas as bibliotecas necessárias.
Bash

pip install -r requirements.txt

4. Configure a Base de Dados e as Chaves de Segurança

    Crie uma base de dados no seu PostgreSQL (ex: clientdb).

    Crie um ficheiro .env na raiz do projeto e adicione as seguintes variáveis, substituindo pelos seus dados:

Snippet de código

DATABASE_URL="postgresql://SEU_UTILIZADOR:SUA_SENHA@localhost:5432/NOME_DA_SUA_BD"
SECRET_KEY="sua-chave-secreta-super-segura-e-dificil-de-adivinhar"
ALGORITHM="HS256"
ACCESS_TOKEN_EXPIRE_MINUTES=30

5. Execute a Aplicação

Com o ambiente virtual ativado, inicie o servidor Uvicorn:
Bash

uvicorn app.main:app --reload

O servidor estará a correr em http://127.0.0.1:8000.

6. Aceda à Documentação Interativa

O FastAPI gera automaticamente uma documentação interativa (Swagger UI). Aceda a ela para testar todos os endpoints:
http://127.0.0.1:8000/docs

API - Guia de Utilização e Endpoints

Autenticação

POST /register - Registar Administrador

Cria um novo utilizador administrador.

Exemplo de Pedido (Body):
JSON

{
  "username": "admin",
  "password": "senhaForte123"
}

POST /login - Obter Token de Acesso

Faz o login e retorna um token JWT para ser usado nas rotas protegidas.

Exemplo de Pedido (form-data):

    username: admin

    password: senhaForte123

Exemplo de Resposta:
JSON

{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}

Rotas Protegidas de Empresas

Para usar os endpoints abaixo, precisa primeiro de obter um access_token na rota /login e enviá-lo no cabeçalho Authorization de cada pedido.

Como autorizar no Swagger UI:

    Execute a rota /login e copie o access_token retornado.

    Clique no botão "Authorize" no topo da página.

    Na janela que abrir, cole o token no formato Bearer SEU_TOKEN_AQUI.

    Agora pode testar todas as rotas de /empresas.

POST /empresas/ - Registar Nova Empresa

Cria uma nova empresa. (Requer autenticação)

GET /empresas/ - Listar Empresas

Retorna uma lista de empresas, com suporte a filtros. (Requer autenticação)

GET /empresas/{empresa_id} - Obter Detalhes de uma Empresa

Procura uma empresa pelo id. (Requer autenticação)

PUT /empresas/{empresa_id} - Atualizar uma Empresa

Atualiza os dados de uma empresa. (Requer autenticação)

DELETE /empresas/{empresa_id} - Apagar uma Empresa

Remove uma empresa da base de dados. (Requer autenticação)
