from dao.base_dao import BaseDAO
from models import Servico, Especialidade
from typing import Optional, List

class ServicoDAO(BaseDAO):
    def __init__(self):
        super().__init__('servicos')
    
    def criar_servico(self, servico: Servico) -> Optional[int]:
        """Cria um novo serviço"""
        data = {
            'nome': servico.nome,
            'descricao': servico.descricao,
            'duracao_minutos': servico.duracao_minutos,
            'preco': servico.preco,
            'especialidade_id': servico.especialidade_id,
            'ativo': servico.ativo
        }
        return self.create(data)
    
    def buscar_por_especialidade(self, especialidade_id: int) -> List[dict]:
        """Busca serviços por especialidade"""
        query = """
            SELECT s.*, e.nome as especialidade_nome
            FROM servicos s
            JOIN especialidades e ON s.especialidade_id = e.id
            WHERE s.especialidade_id = %s AND s.ativo = TRUE
        """
        return self.execute_query(query, (especialidade_id,))
    
    def buscar_ativos(self) -> List[dict]:
        """Retorna todos os serviços ativos"""
        query = """
            SELECT s.*, e.nome as especialidade_nome
            FROM servicos s
            JOIN especialidades e ON s.especialidade_id = e.id
            WHERE s.ativo = TRUE
            ORDER BY s.nome
        """
        return self.execute_query(query)
    
    def atualizar_servico(self, servico: Servico) -> bool:
        """Atualiza dados do serviço"""
        data = {
            'nome': servico.nome,
            'descricao': servico.descricao,
            'duracao_minutos': servico.duracao_minutos,
            'preco': servico.preco,
            'especialidade_id': servico.especialidade_id,
            'ativo': servico.ativo
        }
        return self.update(servico.id, data)

class EspecialidadeDAO(BaseDAO):
    def __init__(self):
        super().__init__('especialidades')
    
    def criar_especialidade(self, especialidade: Especialidade) -> Optional[int]:
        """Cria uma nova especialidade"""
        data = {
            'nome': especialidade.nome,
            'descricao': especialidade.descricao,
            'ativo': especialidade.ativo
        }
        return self.create(data)
    
    def buscar_ativas(self) -> List[dict]:
        """Retorna todas as especialidades ativas"""
        return self.find_by_field('ativo', True)
    
    def atualizar_especialidade(self, especialidade: Especialidade) -> bool:
        """Atualiza dados da especialidade"""
        data = {
            'nome': especialidade.nome,
            'descricao': especialidade.descricao,
            'ativo': especialidade.ativo
        }
        return self.update(especialidade.id, data)