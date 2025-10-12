# Importa as funções e classes necessárias do SQLAlchemy.
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# Importa a instância de configurações para aceder à URL da base de dados.
from app.core.config import settings

# Cria a "engine" do SQLAlchemy, que é o ponto central de comunicação com a base de dados.
# A engine gere um pool de conexões com a base de dados para otimizar a performance.
# Ela é configurada uma única vez quando a aplicação inicia, usando a URL de conexão
# fornecida no ficheiro .env.
engine = create_engine(settings.DATABASE_URL)

# Cria uma "fábrica" de sessões chamada SessionLocal.
# Cada instância de SessionLocal será uma sessão transacional com a base de dados.
# - autocommit=False: Garante que as transações não são automaticamente commitadas.
#   Isto permite um controlo explícito sobre quando as alterações são gravadas.
# - autoflush=False: Impede que o estado da sessão seja enviado para a base de dados
#   automaticamente antes de um commit.
# - bind=engine: Associa esta fábrica de sessões à engine que acabámos de criar.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Cria uma classe base para todos os modelos ORM (Object-Relational Mapper) da aplicação.
# Todos os seus modelos (como Empresa e Usuario) devem herdar desta classe Base
# para que o SQLAlchemy possa mapeá-los para tabelas na base de dados.
Base = declarative_base()

def get_db():
    """
    Função de dependência do FastAPI para gerir o ciclo de vida da sessão da base de dados.
    
    Esta função:
    1. Cria uma nova instância de SessionLocal para um pedido específico.
    2. Usa 'yield' para injetar a sessão ('db') no endpoint da rota.
    3. Garante que a sessão é sempre fechada ('db.close()') após o pedido ser concluído,
       mesmo que ocorram erros, libertando assim a conexão de volta para o pool da engine.
    Isto previne o esgotamento de conexões com a base de dados.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
