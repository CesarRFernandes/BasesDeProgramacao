from dao.base_dao import BaseDAO
from models import FilaEspera
from typing import Optional, List
from datetime import date

class FilaEsperaDAO(BaseDAO):
    def __init__(self):
        super().__init__('fila_espera')
    
    def adicionar_fila(self, fila: FilaEspera) -> Optional[int]:
        """Adiciona cliente à fila de espera"""
        data = {
            'cliente_id': fila.cliente_id,
            'servico_id': fila.servico_id,
            'data_preferencia': fila.data_preferencia,
            'prioridade': fila.prioridade,
            'status': fila.status,
            'observacoes': fila.observacoes
        }
        return self.create(data)
    
    def buscar_aguardando(self) -> List[dict]:
        """Busca clientes aguardando na fila"""
        query = """
            SELECT fe.*, 
                   c.nome as cliente_nome, 
                   c.telefone as cliente_telefone,
                   s.nome as servico_nome
            FROM fila_espera fe
            JOIN clientes c ON fe.cliente_id = c.id
            JOIN servicos s ON fe.servico_id = s.id
            WHERE fe.status = 'aguardando'
            ORDER BY fe.prioridade DESC, fe.data_solicitacao ASC
        """
        return self.execute_query(query)
    
    def buscar_por_servico(self, servico_id: int) -> List[dict]:
        """Busca fila de espera por serviço"""
        query = """
            SELECT fe.*, 
                   c.nome as cliente_nome, 
                   c.telefone as cliente_telefone
            FROM fila_espera fe
            JOIN clientes c ON fe.cliente_id = c.id
            WHERE fe.servico_id = %s
            AND fe.status = 'aguardando'
            ORDER BY fe.prioridade DESC, fe.data_solicitacao ASC
        """
        return self.execute_query(query, (servico_id,))
    
    def buscar_por_cliente(self, cliente_id: int) -> List[dict]:
        """Busca solicitações de fila de um cliente"""
        query = """
            SELECT fe.*, s.nome as servico_nome
            FROM fila_espera fe
            JOIN servicos s ON fe.servico_id = s.id
            WHERE fe.cliente_id = %s
            ORDER BY fe.data_solicitacao DESC
        """
        return self.execute_query(query, (cliente_id,))
    
    def atualizar_status(self, id: int, status: str) -> bool:
        """Atualiza o status de uma solicitação na fila"""
        return self.update(id, {'status': status})
    
    def buscar_por_data_preferencia(self, data_preferencia: date) -> List[dict]:
        """Busca solicitações para uma data específica"""
        query = """
            SELECT fe.*, 
                   c.nome as cliente_nome, 
                   c.telefone as cliente_telefone,
                   s.nome as servico_nome
            FROM fila_espera fe
            JOIN clientes c ON fe.cliente_id = c.id
            JOIN servicos s ON fe.servico_id = s.id
            WHERE fe.data_preferencia = %s
            AND fe.status = 'aguardando'
            ORDER BY fe.prioridade DESC
        """
        return self.execute_query(query, (data_preferencia,))
    
    def aumentar_prioridade(self, id: int) -> bool:
        """Aumenta a prioridade de uma solicitação"""
        query = "UPDATE fila_espera SET prioridade = prioridade + 1 WHERE id = %s"
        return self.execute_update(query, (id,)) > 0