from dao.base_dao import BaseDAO
from models import Agendamento
from typing import Optional, List
from datetime import datetime, date

class AgendamentoDAO(BaseDAO):
    def __init__(self):
        super().__init__('agendamentos')
    
    def criar_agendamento(self, agendamento: Agendamento) -> Optional[int]:
        """Cria um novo agendamento"""
        data = {
            'cliente_id': agendamento.cliente_id,
            'tecnico_id': agendamento.tecnico_id,
            'servico_id': agendamento.servico_id,
            'data_agendamento': agendamento.data_agendamento,
            'duracao_minutos': agendamento.duracao_minutos,
            'tipo_atendimento': agendamento.tipo_atendimento,
            'status': agendamento.status,
            'observacoes': agendamento.observacoes,
            'cliente_pacote_id': agendamento.cliente_pacote_id
        }
        return self.create(data)
    
    def verificar_conflito_tecnico(self, tecnico_id: int, data_hora: datetime, duracao: int, agendamento_id: int = None) -> bool:
        """Verifica se há conflito de horário para o técnico"""
        query = """
            SELECT COUNT(*) as conflitos
            FROM agendamentos
            WHERE tecnico_id = %s
            AND status IN ('agendado', 'em_atendimento')
            AND (
                (data_agendamento <= %s AND DATE_ADD(data_agendamento, INTERVAL duracao_minutos MINUTE) > %s)
                OR
                (data_agendamento < DATE_ADD(%s, INTERVAL %s MINUTE) AND data_agendamento >= %s)
            )
        """
        params = [tecnico_id, data_hora, data_hora, data_hora, duracao, data_hora]
        
        if agendamento_id:
            query += " AND id != %s"
            params.append(agendamento_id)
        
        result = self.execute_query(query, tuple(params))
        return result[0]['conflitos'] > 0 if result else False
    
    def buscar_por_data(self, data: date) -> List[dict]:
        """Busca agendamentos por data"""
        query = """
            SELECT a.*, 
                   c.nome as cliente_nome, 
                   t.nome as tecnico_nome, 
                   s.nome as servico_nome
            FROM agendamentos a
            JOIN clientes c ON a.cliente_id = c.id
            JOIN tecnicos t ON a.tecnico_id = t.id
            JOIN servicos s ON a.servico_id = s.id
            WHERE DATE(a.data_agendamento) = %s
            ORDER BY a.data_agendamento
        """
        return self.execute_query(query, (data,))
    
    def buscar_por_cliente(self, cliente_id: int) -> List[dict]:
        """Busca agendamentos de um cliente"""
        query = """
            SELECT a.*, 
                   t.nome as tecnico_nome, 
                   s.nome as servico_nome,
                   s.preco as servico_preco
            FROM agendamentos a
            JOIN tecnicos t ON a.tecnico_id = t.id
            JOIN servicos s ON a.servico_id = s.id
            WHERE a.cliente_id = %s
            ORDER BY a.data_agendamento DESC
        """
        return self.execute_query(query, (cliente_id,))
    
    def buscar_por_tecnico(self, tecnico_id: int, data_inicio: date = None) -> List[dict]:
        """Busca agendamentos de um técnico"""
        query = """
            SELECT a.*, 
                   c.nome as cliente_nome, 
                   s.nome as servico_nome
            FROM agendamentos a
            JOIN clientes c ON a.cliente_id = c.id
            JOIN servicos s ON a.servico_id = s.id
            WHERE a.tecnico_id = %s
        """
        params = [tecnico_id]
        
        if data_inicio:
            query += " AND DATE(a.data_agendamento) >= %s"
            params.append(data_inicio)
        
        query += " ORDER BY a.data_agendamento"
        return self.execute_query(query, tuple(params))
    
    def atualizar_status(self, id: int, status: str) -> bool:
        """Atualiza o status de um agendamento"""
        return self.update(id, {'status': status})
    
    def buscar_proximos(self, limite: int = 10) -> List[dict]:
        """Busca os próximos agendamentos"""
        query = """
            SELECT a.*, 
                   c.nome as cliente_nome, 
                   t.nome as tecnico_nome, 
                   s.nome as servico_nome
            FROM agendamentos a
            JOIN clientes c ON a.cliente_id = c.id
            JOIN tecnicos t ON a.tecnico_id = t.id
            JOIN servicos s ON a.servico_id = s.id
            WHERE a.data_agendamento >= NOW()
            AND a.status = 'agendado'
            ORDER BY a.data_agendamento
            LIMIT %s
        """
        return self.execute_query(query, (limite,))
    
    def buscar_detalhado(self, id: int) -> Optional[dict]:
        """Busca agendamento com todos os detalhes"""
        query = """
            SELECT a.*, 
                   c.nome as cliente_nome, c.cpf as cliente_cpf, c.telefone as cliente_telefone,
                   t.nome as tecnico_nome, 
                   s.nome as servico_nome, s.preco as servico_preco
            FROM agendamentos a
            JOIN clientes c ON a.cliente_id = c.id
            JOIN tecnicos t ON a.tecnico_id = t.id
            JOIN servicos s ON a.servico_id = s.id
            WHERE a.id = %s
        """
        results = self.execute_query(query, (id,))
        return results[0] if results else None