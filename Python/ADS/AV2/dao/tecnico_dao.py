from dao.base_dao import BaseDAO
from models import Tecnico
from typing import Optional, List
from datetime import datetime

class TecnicoDAO(BaseDAO):
    def __init__(self):
        super().__init__('tecnicos')
    
    def criar_tecnico(self, tecnico: Tecnico) -> Optional[int]:
        """Cria um novo técnico"""
        data = {
            'nome': tecnico.nome,
            'cpf': tecnico.cpf,
            'telefone': tecnico.telefone,
            'email': tecnico.email,
            'especialidade_id': tecnico.especialidade_id,
            'data_contratacao': tecnico.data_contratacao,
            'ativo': tecnico.ativo
        }
        return self.create(data)
    
    def buscar_por_especialidade(self, especialidade_id: int) -> List[dict]:
        """Busca técnicos por especialidade"""
        query = """
            SELECT t.*, e.nome as especialidade_nome
            FROM tecnicos t
            JOIN especialidades e ON t.especialidade_id = e.id
            WHERE t.especialidade_id = %s AND t.ativo = TRUE
        """
        return self.execute_query(query, (especialidade_id,))
    
    def buscar_disponiveis(self, data_hora: datetime, duracao: int) -> List[dict]:
        """Busca técnicos disponíveis em um horário específico"""
        query = """
            SELECT DISTINCT t.*, e.nome as especialidade_nome
            FROM tecnicos t
            JOIN especialidades e ON t.especialidade_id = e.id
            WHERE t.ativo = TRUE
            AND t.id NOT IN (
                SELECT tecnico_id FROM agendamentos
                WHERE status IN ('agendado', 'em_atendimento')
                AND (
                    (data_agendamento <= %s AND DATE_ADD(data_agendamento, INTERVAL duracao_minutos MINUTE) > %s)
                    OR
                    (data_agendamento < DATE_ADD(%s, INTERVAL %s MINUTE) AND data_agendamento >= %s)
                )
            )
        """
        return self.execute_query(query, (data_hora, data_hora, data_hora, duracao, data_hora))
    
    def atualizar_tecnico(self, tecnico: Tecnico) -> bool:
        """Atualiza dados do técnico"""
        data = {
            'nome': tecnico.nome,
            'cpf': tecnico.cpf,
            'telefone': tecnico.telefone,
            'email': tecnico.email,
            'especialidade_id': tecnico.especialidade_id,
            'data_contratacao': tecnico.data_contratacao,
            'ativo': tecnico.ativo
        }
        return self.update(tecnico.id, data)
    
    def buscar_com_especialidade(self) -> List[dict]:
        """Busca todos os técnicos com nome da especialidade"""
        query = """
            SELECT t.*, e.nome as especialidade_nome
            FROM tecnicos t
            JOIN especialidades e ON t.especialidade_id = e.id
            ORDER BY t.nome
        """
        return self.execute_query(query)