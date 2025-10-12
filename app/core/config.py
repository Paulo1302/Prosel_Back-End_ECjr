# Importa o módulo 'os' para interagir com o sistema operativo,
# especificamente para aceder a variáveis de ambiente.
import os

# Importa a função 'load_dotenv' da biblioteca python-dotenv.
# Esta função é responsável por procurar um ficheiro .env no diretório do projeto
# e carregar as variáveis definidas nele para o ambiente do sistema operativo.
from dotenv import load_dotenv

# Executa a função para carregar as variáveis de ambiente do ficheiro .env.
# A partir deste ponto, os.getenv() conseguirá ler os valores definidos no .env.
load_dotenv()

class Settings:
    """
    Classe de configurações que centraliza o acesso às variáveis de ambiente da aplicação.
    Utiliza type hints (ex: str, int) para documentar o tipo esperado de cada variável,
    melhorando a clareza e auxiliando ferramentas de análise estática de código.
    """
    
    # URL de conexão com a base de dados PostgreSQL, lida da variável de ambiente.
    # Esta string contém todas as informações necessárias para o SQLAlchemy se conectar à BD.
    DATABASE_URL: str = os.getenv("DATABASE_URL")
    
    # Chave secreta usada para assinar e verificar os tokens JWT (JSON Web Tokens).
    # É fundamental para a segurança da autenticação da API.
    SECRET_KEY: str = os.getenv("SECRET_KEY")
    
    # Algoritmo de hashing criptográfico usado na assinatura dos tokens JWT.
    # HS256 (HMAC using SHA-256) é um algoritmo simétrico comum para este fim.
    ALGORITHM: str = os.getenv("ALGORITHM")
    
    # Tempo de vida do token de acesso, em minutos.
    # A variável é lida como string e convertida explicitamente para um inteiro.
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))

# Cria uma instância única e global da classe Settings.
# Este padrão (singleton) garante que as configurações sejam carregadas apenas uma vez
# e possam ser importadas e utilizadas de forma consistente em toda a aplicação.
settings = Settings()
