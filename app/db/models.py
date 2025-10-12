# Importa os componentes necessários do SQLAlchemy para definir os tipos de colunas e funções da BD.
from sqlalchemy import Column, Integer, String, DateTime, func

# Importa a classe 'Base' declarativa do nosso módulo de base de dados.
# Todas as classes de modelo ORM devem herdar desta Base para serem mapeadas pelo SQLAlchemy.
from .database import Base

class Empresa(Base):
    """
    Modelo ORM que mapeia para a tabela 'empresas' na base de dados.
    Cada atributo da classe representa uma coluna na tabela correspondente.
    """
    # __tablename__ define o nome exato da tabela na base de dados PostgreSQL.
    __tablename__ = "empresas"

    # Define a coluna 'id' como a chave primária da tabela.
    # - Integer: Tipo de dados da coluna (inteiro).
    # - primary_key=True: Designa esta coluna como a chave primária, que deve ser única e não nula.
    # - index=True: Cria um índice na base de dados para esta coluna, otimizando a performance de consultas (buscas) pelo ID.
    id = Column(Integer, primary_key=True, index=True)
    
    # Define a coluna 'nome'.
    # - String: Tipo de dados (VARCHAR). O SQLAlchemy não exige um tamanho, mas pode ser especificado (ex: String(100)).
    # - index=True: Otimiza buscas por nome.
    # - nullable=False: Impõe uma restrição NOT NULL a nível da base de dados, garantindo que cada registo tenha um nome.
    nome = Column(String, index=True, nullable=False)
    
    # Define a coluna 'cnpj'.
    # - unique=True: Impõe uma restrição UNIQUE a nível da base de dados, garantindo que não haja dois registos com o mesmo CNPJ.
    cnpj = Column(String, unique=True, index=True, nullable=False)
    
    cidade = Column(String, index=True)
    ramo_atuacao = Column(String, index=True)
    telefone = Column(String, nullable=False)
    
    # Define a coluna 'email_contato' com uma restrição UNIQUE.
    email_contato = Column(String, unique=True, index=True, nullable=False)
    
    # Define a coluna 'data_cadastro'.
    # - DateTime(timezone=True): Armazena a data e a hora com informação de fuso horário.
    # - server_default=func.now(): Define um valor padrão a nível da base de dados.
    #   'func.now()' é traduzido pelo SQLAlchemy para a função SQL 'NOW()' ou similar,
    #   que insere o timestamp atual do servidor da base de dados no momento da criação do registo.
    data_cadastro = Column(DateTime(timezone=True), server_default=func.now())

class Usuario(Base):
    """
    Modelo ORM que mapeia para a tabela 'usuarios' (administradores).
    """
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    
    # Define a coluna 'username' com uma restrição UNIQUE para garantir nomes de utilizador únicos.
    username = Column(String, unique=True, index=True, nullable=False)
    
    # Define a coluna 'hashed_password'.
    # Esta coluna irá armazenar a representação da senha após passar pelo algoritmo de hashing (bcrypt).
    # Nunca se deve armazenar senhas em texto plano.
    hashed_password = Column(String, nullable=False)

