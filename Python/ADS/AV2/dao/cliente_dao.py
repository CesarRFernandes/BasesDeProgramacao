from dao.base_dao import BaseDAO
from models import Cliente
from typing import Optional, List

class ClienteDAO(BaseDAO):
    def __init__(self):
        super().__init__('clientes')
    
    def criar_cliente(self, cliente: Cliente) -> Optional[int]:
        """Cria um novo cliente"""
        data = {
            'nome': cliente.nome,
            'cpf': cliente.cpf,
            'telefone': cliente.telefone,
            'email': cliente.email,
            'endereco': cliente.endereco,
            'ativo': cliente.ativo
        }
        return self.create(data)
    
    def buscar_por_cpf(self, cpf: str) -> Optional[dict]:
        """Busca cliente por CPF"""
        results = self.find_by_field('cpf', cpf)
        return results[0] if results else None
    
    def buscar_ativos(self) -> List[dict]:
        """Retorna todos os clientes ativos"""
        return self.find_by_field('ativo', True)
    
    def atualizar_cliente(self, cliente: Cliente) -> bool:
        """Atualiza dados do cliente"""
        data = {
            'nome': cliente.nome,
            'cpf': cliente.cpf,
            'telefone': cliente.telefone,
            'email': cliente.email,
            'endereco': cliente.endereco,
            'ativo': cliente.ativo
        }
        return self.update(cliente.id, data)
    
    def desativar_cliente(self, id: int) -> bool:
        """Desativa um cliente"""
        return self.update(id, {'ativo': False})
    
    def buscar_por_nome(self, nome: str) -> List[dict]:
        """Busca clientes por nome parcial"""
        query = f"SELECT * FROM {self.table_name} WHERE nome LIKE %s"
        return self.execute_query(query, (f"%{nome}%",))