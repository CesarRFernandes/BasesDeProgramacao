import mysql.connector
from mysql.connector import Error
from contextlib import contextmanager

class DatabaseConfig:
    """Configuração do banco de dados MySQL"""
    
    HOST = 'localhost'
    PORT = 3306
    DATABASE = 'reparos_automotivos_bd'
    USER = 'root'
    PASSWORD = ''
    
    @staticmethod
    def get_connection():
        """Cria e retorna uma conexão com o banco de dados"""
        try:
            connection = mysql.connector.connect(
                host=DatabaseConfig.HOST,
                port=DatabaseConfig.PORT,
                database=DatabaseConfig.DATABASE,
                user=DatabaseConfig.USER,
                password=DatabaseConfig.PASSWORD,
                charset='utf8mb4',
                collation='utf8mb4_unicode_ci'
            )
            return connection
        except Error as e:
            print(f"Erro ao conectar ao banco de dados: {e}")
            raise
    
    @staticmethod
    @contextmanager
    def get_cursor(dictionary=True):
        """Context manager para gerenciar conexão e cursor"""
        connection = None
        cursor = None
        try:
            connection = DatabaseConfig.get_connection()
            cursor = connection.cursor(dictionary=dictionary)
            yield cursor
            connection.commit()
        except Error as e:
            if connection:
                connection.rollback()
            print(f"Erro na operação do banco de dados: {e}")
            raise
        finally:
            if cursor:
                cursor.close()
            if connection and connection.is_connected():
                connection.close()
    
    @staticmethod
    def test_connection():
        """Testa a conexão com o banco de dados"""
        try:
            connection = DatabaseConfig.get_connection()
            if connection.is_connected():
                print("✓ Conexão com banco de dados estabelecida com sucesso")
                connection.close()
                return True
        except Error as e:
            print(f"✗ Falha ao conectar ao banco de dados: {e}")
            return False