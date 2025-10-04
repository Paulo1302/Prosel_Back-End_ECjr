# Prosel_Back-End_ECjr
API de Gerenciamento de Empresas Clientes - Ecomp Jr.
 Sobre o Projeto

Esta API foi desenvolvida como parte de um processo seletivo para a Ecomp Jr., com o objetivo de criar um sistema centralizado para o gerenciamento de empresas clientes. A aplicação resolve o desafio de manter informações consistentes e acessíveis, substituindo o uso de planilhas descentralizadas por uma solução robusta, escalável e segura.

O projeto foi construído em FastAPI, seguindo as melhores práticas de desenvolvimento de software, incluindo uma arquitetura em camadas (Repositories, Services, Routers) para garantir um código limpo, de fácil manutenção e testável.
 Funcionalidades

    CRUD Completo para Empresas: Funcionalidades para Criar, Ler, Atualizar e Deletar empresas.

    Consultas Avançadas:

        Filtragem de empresas por cidade e ramo_atuacao.

        Busca textual (parcial e insensível a maiúsculas/minúsculas) pelo nome da empresa.

    Tratamento de Erros: Respostas claras e códigos de status HTTP apropriados para validações de dados (CNPJ/email duplicado) e recursos não encontrados.

    Arquitetura Profissional: Código organizado no padrão Repository, Service e Router para separação de responsabilidades.

    Gestão de Configurações: Uso de variáveis de ambiente (.env) para proteger dados sensíveis, como as credenciais do banco de dados.

 Tecnologias Utilizadas

    Backend:

        Python 3.10+

        FastAPI - Framework web de alta performance.

        Uvicorn - Servidor ASGI.

    Banco de Dados:

        PostgreSQL - Banco de dados relacional.

        SQLAlchemy - ORM para manipulação de dados em Python.

        Psycopg2 - Driver de conexão com o PostgreSQL.

    Validação e Configuração:

        Pydantic - Para validação de dados e configurações.

        Python-Dotenv - Para gerenciamento de variáveis de ambiente.

 Como Executar o Projeto

Siga os passos abaixo para configurar e executar a aplicação em seu ambiente local.
Pré-requisitos

    Python 3.10 ou superior.

    PostgreSQL instalado e em execução.

    Git para clonar o repositório.

1. Clone o Repositório

git clone [https://github.com/Paulo1302/Prosel_Back-End_ECjr.git](https://github.com/Paulo1302/Prosel_Back-End_ECjr.git)
cd Prosel_Back-End_ECjr

2. Crie e Ative um Ambiente Virtual

É uma boa prática isolar as dependências do projeto.

# Criar o ambiente virtual
python -m venv venv

# Ativar no Windows
venv\Scripts\activate

# Ativar no macOS/Linux
source venv/bin/activate

3. Instale as Dependências

O arquivo requirements.txt contém todas as bibliotecas necessárias.

pip install -r requirements.txt

4. Configure o Banco de Dados

    Crie um banco de dados no seu PostgreSQL (ex: clientdb).

    Renomeie o arquivo .env.example (se houver) para .env ou crie um novo.

    Edite o arquivo .env com suas credenciais do PostgreSQL:

# Exemplo de arquivo .env
DATABASE_URL="postgresql://SEU_USUARIO:SUA_SENHA@localhost:5432/NOME_DO_SEU_BANCO"

5. Execute a Aplicação

Com o ambiente virtual ativado, inicie o servidor Uvicorn:

uvicorn app.main:app --reload

O servidor estará rodando em http://127.0.0.1:8000.
6. Acesse a Documentação Interativa

O FastAPI gera automaticamente uma documentação interativa (Swagger UI). Acesse-a para testar todos os endpoints:
http://127.0.0.1:8000/docs
📖 API - Documentação dos Endpoints

Todos os endpoints estão sob o prefixo /empresas.
POST /empresas/ - Cadastrar Nova Empresa

Cria uma nova empresa no banco de dados. O CNPJ e o E-mail de Contato devem ser únicos.

Exemplo de Requisição (Body):

{
  "nome": "InovaTech Soluções",
  "cnpj": "11222333000144",
  "cidade": "Feira de Santana",
  "ramo_atuacao": "Tecnologia",
  "telefone": "75999998888",
  "email_contato": "contato@inovatech.com"
}

Exemplo de Resposta (Status 201 - Created):

{
  "nome": "InovaTech Soluções",
  "cnpj": "11222333000144",
  "cidade": "Feira de Santana",
  "ramo_atuacao": "Tecnologia",
  "telefone": "75999998888",
  "email_contato": "contato@inovatech.com",
  "id": 1,
  "data_cadastro": "2025-10-03T18:30:00.123456Z"
}

GET /empresas/ - Listar Empresas

Retorna uma lista de todas as empresas cadastradas. Suporta filtros via query parameters.

Parâmetros de Consulta (Opcionais):

    nome (str): Busca empresas por nome (busca parcial).

    cidade (str): Filtra empresas por cidade (busca parcial).

    ramo_atuacao (str): Filtra empresas por ramo de atuação (busca parcial).

    skip (int): Número de registros a pular (para paginação). Padrão: 0.

    limit (int): Número máximo de registros a retornar. Padrão: 100.

Exemplo de Requisição:
GET /empresas/?cidade=Feira&ramo_atuacao=Tecnologia

Exemplo de Resposta (Status 200 - OK):

[
  {
    "nome": "InovaTech Soluções",
    "cnpj": "11222333000144",
    "cidade": "Feira de Santana",
    "ramo_atuacao": "Tecnologia",
    "telefone": "75999998888",
    "email_contato": "contato@inovatech.com",
    "id": 1,
    "data_cadastro": "2025-10-03T18:30:00.123456Z"
  }
]

GET /empresas/{empresa_id} - Obter Detalhes de uma Empresa

Busca e retorna os dados de uma única empresa pelo seu id.

Exemplo de Requisição:
GET /empresas/1

Exemplo de Resposta (Status 200 - OK):

{
  "nome": "InovaTech Soluções",
  "cnpj": "11222333000144",
  "cidade": "Feira de Santana",
  "ramo_atuacao": "Tecnologia",
  "telefone": "75999998888",
  "email_contato": "contato@inovatech.com",
  "id": 1,
  "data_cadastro": "2025-10-03T18:30:00.123456Z"
}

Se a empresa não for encontrada, retornará um erro 404 Not Found.
PUT /empresas/{empresa_id} - Atualizar uma Empresa

Atualiza os dados de uma empresa existente. Os campos id, cnpj e data_cadastro não podem ser alterados.

Exemplo de Requisição (Body):
Você pode enviar apenas os campos que deseja alterar.

{
  "cidade": "Salvador",
  "telefone": "71988887777"
}

Exemplo de Resposta (Status 200 - OK):

{
  "nome": "InovaTech Soluções",
  "cnpj": "11222333000144",
  "cidade": "Salvador",
  "ramo_atuacao": "Tecnologia",
  "telefone": "71988887777",
  "email_contato": "contato@inovatech.com",
  "id": 1,
  "data_cadastro": "2025-10-03T18:30:00.123456Z"
}

Se a empresa não for encontrada, retornará um erro 404 Not Found.
DELETE /empresas/{empresa_id} - Excluir uma Empresa

Remove uma empresa do banco de dados pelo seu id.

Exemplo de Requisição:
DELETE /empresas/1

Resposta:

    Status 204 No Content: Em caso de sucesso, o servidor retorna uma resposta vazia.

    Status 404 Not Found: Se a empresa não for encontrada.

📝 Convenção de Commits

Este projeto utiliza a especificação Conventional Commits para padronizar as mensagens de commit.

Tipos mais comuns:

    feat: Adição de uma nova funcionalidade.

    fix: Correção de um bug.

    docs: Alterações na documentação.

    style: Alterações de formatação que não afetam o código.

    refactor: Refatoração de código que não altera a funcionalidade externa.

    chore: Tarefas de manutenção (atualização de dependências, etc.).

Exemplo:

git commit -m "feat: Adiciona endpoint para cadastro de empresas"

