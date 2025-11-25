from dao.base_dao import BaseDAO
from typing import Optional, List
from datetime import datetime, date
import csv
import os

class TransacaoDAO(BaseDAO):
    def __init__(self):
        super().__init__('transacoes')
    
    def registrar_transacao(self, cliente_id: int, tipo: str, valor: float,
                           metodo_pagamento: str = None, agendamento_id: int = None,
                           pacote_id: int = None, status: str = 'confirmado',
                           descricao: str = '') -> Optional[int]:
        """Registra uma nova transação"""
        data = {
            'cliente_id': cliente_id,
            'agendamento_id': agendamento_id,
            'pacote_id': pacote_id,
            'tipo': tipo,
            'metodo_pagamento': metodo_pagamento,
            'valor': valor,
            'data_hora': datetime.now(),
            'status': status,
            'descricao': descricao
        }
        return self.create(data)
    
    def buscar_todas(self, limite: int = 1000) -> List[dict]:
        """Busca todas as transações com informações completas"""
        query = """
            SELECT 
                t.*,
                c.nome as cliente_nome,
                c.cpf as cliente_cpf,
                COALESCE(s.nome, 'N/A') as servico_nome,
                COALESCE(p.nome, 'N/A') as pacote_nome
            FROM transacoes t
            JOIN clientes c ON t.cliente_id = c.id
            LEFT JOIN agendamentos a ON t.agendamento_id = a.id
            LEFT JOIN servicos s ON a.servico_id = s.id
            LEFT JOIN pacotes p ON t.pacote_id = p.id
            ORDER BY t.data_hora DESC
            LIMIT %s
        """
        return self.execute_query(query, (limite,))
    
    def buscar_por_cliente(self, cliente_id: int) -> List[dict]:
        """Busca transações de um cliente específico"""
        query = """
            SELECT 
                t.*,
                c.nome as cliente_nome,
                COALESCE(s.nome, 'N/A') as servico_nome,
                COALESCE(p.nome, 'N/A') as pacote_nome
            FROM transacoes t
            JOIN clientes c ON t.cliente_id = c.id
            LEFT JOIN agendamentos a ON t.agendamento_id = a.id
            LEFT JOIN servicos s ON a.servico_id = s.id
            LEFT JOIN pacotes p ON t.pacote_id = p.id
            WHERE t.cliente_id = %s
            ORDER BY t.data_hora DESC
        """
        return self.execute_query(query, (cliente_id,))
    
    def buscar_por_tipo(self, tipo: str) -> List[dict]:
        """Busca transações por tipo"""
        query = """
            SELECT 
                t.*,
                c.nome as cliente_nome,
                COALESCE(s.nome, 'N/A') as servico_nome
            FROM transacoes t
            JOIN clientes c ON t.cliente_id = c.id
            LEFT JOIN agendamentos a ON t.agendamento_id = a.id
            LEFT JOIN servicos s ON a.servico_id = s.id
            WHERE t.tipo = %s
            ORDER BY t.data_hora DESC
        """
        return self.execute_query(query, (tipo,))
    
    def buscar_por_periodo(self, data_inicio: date, data_fim: date) -> List[dict]:
        """Busca transações em um período"""
        query = """
            SELECT 
                t.*,
                c.nome as cliente_nome,
                COALESCE(s.nome, 'N/A') as servico_nome,
                COALESCE(p.nome, 'N/A') as pacote_nome
            FROM transacoes t
            JOIN clientes c ON t.cliente_id = c.id
            LEFT JOIN agendamentos a ON t.agendamento_id = a.id
            LEFT JOIN servicos s ON a.servico_id = s.id
            LEFT JOIN pacotes p ON t.pacote_id = p.id
            WHERE DATE(t.data_hora) BETWEEN %s AND %s
            ORDER BY t.data_hora DESC
        """
        return self.execute_query(query, (data_inicio, data_fim))
    
    def buscar_com_filtros(self, cliente_id: int = None, tipo: str = None,
                          data_inicio: date = None, data_fim: date = None,
                          status: str = None) -> List[dict]:
        """Busca transações com múltiplos filtros"""
        query = """
            SELECT 
                t.*,
                c.nome as cliente_nome,
                c.cpf as cliente_cpf,
                COALESCE(s.nome, 'N/A') as servico_nome,
                COALESCE(p.nome, 'N/A') as pacote_nome
            FROM transacoes t
            JOIN clientes c ON t.cliente_id = c.id
            LEFT JOIN agendamentos a ON t.agendamento_id = a.id
            LEFT JOIN servicos s ON a.servico_id = s.id
            LEFT JOIN pacotes p ON t.pacote_id = p.id
            WHERE 1=1
        """
        params = []
        
        if cliente_id:
            query += " AND t.cliente_id = %s"
            params.append(cliente_id)
        
        if tipo and tipo != 'Todos':
            query += " AND t.tipo = %s"
            params.append(tipo)
        
        if status and status != 'Todos':
            query += " AND t.status = %s"
            params.append(status)
        
        if data_inicio:
            query += " AND DATE(t.data_hora) >= %s"
            params.append(data_inicio)
        
        if data_fim:
            query += " AND DATE(t.data_hora) <= %s"
            params.append(data_fim)
        
        query += " ORDER BY t.data_hora DESC LIMIT 1000"
        
        return self.execute_query(query, tuple(params))
    
    def buscar_tipos_unicos(self) -> List[str]:
        """Retorna lista de tipos de transações únicos"""
        query = "SELECT DISTINCT tipo FROM transacoes ORDER BY tipo"
        result = self.execute_query(query)
        return [r['tipo'] for r in result]
    
    def calcular_total_por_tipo(self, tipo: str = None) -> float:
        """Calcula total de transações por tipo"""
        if tipo:
            query = "SELECT COALESCE(SUM(valor), 0) as total FROM transacoes WHERE tipo = %s AND status = 'confirmado'"
            result = self.execute_query(query, (tipo,))
        else:
            query = "SELECT COALESCE(SUM(valor), 0) as total FROM transacoes WHERE status = 'confirmado'"
            result = self.execute_query(query)
        
        return float(result[0]['total']) if result else 0.0
    
    def calcular_totais_periodo(self, data_inicio: date, data_fim: date) -> dict:
        """Calcula totais de receitas e despesas em um período"""
        query = """
            SELECT 
                SUM(CASE WHEN tipo IN ('pagamento_servico', 'pagamento_pacote', 'taxa_nao_comparecimento') 
                    AND status = 'confirmado' THEN valor ELSE 0 END) as receitas,
                SUM(CASE WHEN tipo IN ('credito_utilizado', 'reembolso', 'estorno') 
                    AND status = 'confirmado' THEN valor ELSE 0 END) as despesas,
                COUNT(*) as total_transacoes
            FROM transacoes
            WHERE DATE(data_hora) BETWEEN %s AND %s
        """
        result = self.execute_query(query, (data_inicio, data_fim))
        
        if result:
            return {
                'receitas': float(result[0]['receitas'] or 0),
                'despesas': float(result[0]['despesas'] or 0),
                'total_transacoes': int(result[0]['total_transacoes'] or 0)
            }
        return {'receitas': 0.0, 'despesas': 0.0, 'total_transacoes': 0}
    
    def exportar_csv(self, transacoes: List[dict], caminho_arquivo: str) -> bool:
        """Exporta transações para arquivo CSV"""
        try:
            with open(caminho_arquivo, 'w', newline='', encoding='utf-8') as csvfile:
                if not transacoes:
                    return False
                
                fieldnames = [
                    'ID', 'Data/Hora', 'Cliente', 'CPF', 'Tipo', 
                    'Método Pagamento', 'Valor', 'Status', 'Serviço/Pacote', 'Descrição'
                ]
                
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                
                for t in transacoes:
                    writer.writerow({
                        'ID': t['id'],
                        'Data/Hora': t['data_hora'].strftime('%d/%m/%Y %H:%M:%S'),
                        'Cliente': t['cliente_nome'],
                        'CPF': t.get('cliente_cpf', 'N/A'),
                        'Tipo': t['tipo'],
                        'Método Pagamento': t.get('metodo_pagamento', 'N/A'),
                        'Valor': f"R$ {t['valor']:.2f}",
                        'Status': t['status'],
                        'Serviço/Pacote': t.get('servico_nome', t.get('pacote_nome', 'N/A')),
                        'Descrição': t.get('descricao', '')
                    })
                
                return True
        except Exception as e:
            print(f"Erro ao exportar CSV: {e}")
            return False
    
    def atualizar_status(self, id: int, status: str) -> bool:
        """Atualiza o status de uma transação"""
        return self.update(id, {'status': status})
    
    def buscar_estatisticas_cliente(self, cliente_id: int) -> dict:
        """Retorna estatísticas de transações de um cliente"""
        query = """
            SELECT 
                COUNT(*) as total_transacoes,
                SUM(CASE WHEN status = 'confirmado' THEN valor ELSE 0 END) as valor_total,
                SUM(CASE WHEN tipo IN ('pagamento_servico', 'pagamento_pacote') 
                    AND status = 'confirmado' THEN valor ELSE 0 END) as total_pago,
                SUM(CASE WHEN tipo = 'credito_recebido' THEN valor ELSE 0 END) as total_credito
            FROM transacoes
            WHERE cliente_id = %s
        """
        result = self.execute_query(query, (cliente_id,))
        
        if result:
            return {
                'total_transacoes': int(result[0]['total_transacoes'] or 0),
                'valor_total': float(result[0]['valor_total'] or 0),
                'total_pago': float(result[0]['total_pago'] or 0),
                'total_credito': float(result[0]['total_credito'] or 0)
            }
        return {
            'total_transacoes': 0,
            'valor_total': 0.0,
            'total_pago': 0.0,
            'total_credito': 0.0
        }