from abc import ABC, abstractmethod
from config.database import DatabaseConfig
from typing import List, Optional, Any

class BaseDAO(ABC):
    """Classe base para todos os DAOs"""
    
    def __init__(self, table_name: str):
        self.table_name = table_name
    
    def create(self, data: dict) -> Optional[int]:
        """Insere um novo registro"""
        columns = ', '.join(data.keys())
        placeholders = ', '.join(['%s'] * len(data))
        query = f"INSERT INTO {self.table_name} ({columns}) VALUES ({placeholders})"
        
        with DatabaseConfig.get_cursor() as cursor:
            cursor.execute(query, list(data.values()))
            return cursor.lastrowid
    
    def find_by_id(self, id: int) -> Optional[dict]:
        """Busca um registro por ID"""
        query = f"SELECT * FROM {self.table_name} WHERE id = %s"
        
        with DatabaseConfig.get_cursor() as cursor:
            cursor.execute(query, (id,))
            return cursor.fetchone()
    
    def find_all(self) -> List[dict]:
        """Retorna todos os registros"""
        query = f"SELECT * FROM {self.table_name}"
        
        with DatabaseConfig.get_cursor() as cursor:
            cursor.execute(query)
            return cursor.fetchall()
    
    def update(self, id: int, data: dict) -> bool:
        """Atualiza um registro"""
        set_clause = ', '.join([f"{key} = %s" for key in data.keys()])
        query = f"UPDATE {self.table_name} SET {set_clause} WHERE id = %s"
        
        with DatabaseConfig.get_cursor() as cursor:
            values = list(data.values()) + [id]
            cursor.execute(query, values)
            return cursor.rowcount > 0
    
    def delete(self, id: int) -> bool:
        """Deleta um registro"""
        query = f"DELETE FROM {self.table_name} WHERE id = %s"
        
        with DatabaseConfig.get_cursor() as cursor:
            cursor.execute(query, (id,))
            return cursor.rowcount > 0
    
    def find_by_field(self, field: str, value: Any) -> List[dict]:
        """Busca registros por um campo específico"""
        query = f"SELECT * FROM {self.table_name} WHERE {field} = %s"
        
        with DatabaseConfig.get_cursor() as cursor:
            cursor.execute(query, (value,))
            return cursor.fetchall()
    
    def execute_query(self, query: str, params: tuple = ()) -> List[dict]:
        """Executa uma query personalizada"""
        with DatabaseConfig.get_cursor() as cursor:
            cursor.execute(query, params)
            return cursor.fetchall()
    
    def execute_update(self, query: str, params: tuple = ()) -> int:
        """Executa uma query de atualização/inserção"""
        with DatabaseConfig.get_cursor() as cursor:
            cursor.execute(query, params)
            return cursor.rowcount