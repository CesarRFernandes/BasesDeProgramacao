from dao.base_dao import BaseDAO
from models import Pagamento, Penalidade, Credito
from typing import Optional, List
from datetime import datetime, timedelta

class PagamentoDAO(BaseDAO):
    def __init__(self):
        super().__init__('pagamentos')
    
    def criar_pagamento(self, pagamento: Pagamento) -> Optional[int]:
        """Cria um novo pagamento"""
        data = {
            'agendamento_id': pagamento.agendamento_id,
            'cliente_pacote_id': pagamento.cliente_pacote_id,
            'cliente_id': pagamento.cliente_id,
            'valor': pagamento.valor,
            'tipo_pagamento': pagamento.tipo_pagamento,
            'status': pagamento.status,
            'data_pagamento': pagamento.data_pagamento,
            'descricao': pagamento.descricao
        }
        return self.create(data)
    
    def confirmar_pagamento(self, id: int) -> bool:
        """Confirma um pagamento"""
        data = {
            'status': 'pago',
            'data_pagamento': datetime.now()
        }
        return self.update(id, data)
    
    def buscar_por_agendamento(self, agendamento_id: int) -> List[dict]:
        """Busca pagamentos de um agendamento"""
        return self.find_by_field('agendamento_id', agendamento_id)
    
    def buscar_por_cliente(self, cliente_id: int) -> List[dict]:
        """Busca histórico de pagamentos de um cliente"""
        query = """
            SELECT p.*, 
                   COALESCE(a.data_agendamento, cp.data_contratacao) as data_referencia
            FROM pagamentos p
            LEFT JOIN agendamentos a ON p.agendamento_id = a.id
            LEFT JOIN clientes_pacotes cp ON p.cliente_pacote_id = cp.id
            WHERE p.cliente_id = %s
            ORDER BY p.data_criacao DESC
        """
        return self.execute_query(query, (cliente_id,))
    
    def buscar_pendentes(self) -> List[dict]:
        """Busca pagamentos pendentes"""
        query = """
            SELECT p.*, c.nome as cliente_nome
            FROM pagamentos p
            JOIN clientes c ON p.cliente_id = c.id
            WHERE p.status = 'pendente'
            ORDER BY p.data_criacao
        """
        return self.execute_query(query)

class PenalidadeDAO(BaseDAO):
    def __init__(self):
        super().__init__('penalidades')
    
    def aplicar_penalidade(self, cliente_id: int, agendamento_id: int, valor_servico: float) -> Optional[int]:
        """Aplica penalidade de não comparecimento (50% taxa, 50% crédito)"""
        valor_taxa = valor_servico * 0.5
        valor_credito = valor_servico * 0.5
        
        data = {
            'cliente_id': cliente_id,
            'agendamento_id': agendamento_id,
            'valor_total': valor_servico,
            'valor_taxa': valor_taxa,
            'valor_credito': valor_credito,
            'utilizado': False
        }
        return self.create(data)
    
    def buscar_por_cliente(self, cliente_id: int) -> List[dict]:
        """Busca penalidades de um cliente"""
        query = """
            SELECT p.*, a.data_agendamento, s.nome as servico_nome
            FROM penalidades p
            JOIN agendamentos a ON p.agendamento_id = a.id
            JOIN servicos s ON a.servico_id = s.id
            WHERE p.cliente_id = %s
            ORDER BY p.data_aplicacao DESC
        """
        return self.execute_query(query, (cliente_id,))
    
    def marcar_utilizada(self, id: int) -> bool:
        """Marca penalidade como utilizada"""
        return self.update(id, {'utilizado': True})

class CreditoDAO(BaseDAO):
    def __init__(self):
        super().__init__('creditos')
    
    def criar_credito(self, cliente_id: int, penalidade_id: int, valor: float) -> Optional[int]:
        """Cria um crédito a partir de uma penalidade"""
        data_validade = datetime.now() + timedelta(days=365)
        
        data = {
            'cliente_id': cliente_id,
            'penalidade_id': penalidade_id,
            'valor': valor,
            'saldo': valor,
            'data_validade': data_validade.date(),
            'ativo': True
        }
        return self.create(data)
    
    def buscar_creditos_disponiveis(self, cliente_id: int) -> List[dict]:
        """Busca créditos disponíveis de um cliente"""
        query = """
            SELECT *
            FROM creditos
            WHERE cliente_id = %s
            AND ativo = TRUE
            AND saldo > 0
            AND data_validade >= CURDATE()
            ORDER BY data_validade ASC
        """
        return self.execute_query(query, (cliente_id,))
    
    def calcular_saldo_total(self, cliente_id: int) -> float:
        """Calcula saldo total de créditos disponíveis"""
        query = """
            SELECT COALESCE(SUM(saldo), 0) as total
            FROM creditos
            WHERE cliente_id = %s
            AND ativo = TRUE
            AND saldo > 0
            AND data_validade >= CURDATE()
        """
        result = self.execute_query(query, (cliente_id,))
        return float(result[0]['total']) if result else 0.0
    
    def utilizar_credito(self, credito_id: int, valor: float) -> bool:
        """Deduz valor do saldo de um crédito"""
        query = "UPDATE creditos SET saldo = saldo - %s WHERE id = %s AND saldo >= %s"
        return self.execute_update(query, (valor, credito_id, valor)) > 0
    
    def desativar_credito(self, credito_id: int) -> bool:
        """Desativa um crédito"""
        return self.update(credito_id, {'ativo': False})