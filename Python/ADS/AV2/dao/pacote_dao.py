from dao.base_dao import BaseDAO
from models import Pacote, ClientePacote
from typing import Optional, List
from datetime import datetime, timedelta

class PacoteDAO(BaseDAO):
    def __init__(self):
        super().__init__('pacotes')
    
    def criar_pacote(self, pacote: Pacote, servicos: List[dict]) -> Optional[int]:
        """Cria um novo pacote com seus serviços"""
        data = {
            'nome': pacote.nome,
            'descricao': pacote.descricao,
            'preco_total': pacote.preco_total,
            'desconto_percentual': pacote.desconto_percentual,
            'validade_dias': pacote.validade_dias,
            'ativo': pacote.ativo
        }
        pacote_id = self.create(data)
        
        if pacote_id and servicos:
            for servico in servicos:
                query = "INSERT INTO pacotes_servicos (pacote_id, servico_id, quantidade) VALUES (%s, %s, %s)"
                self.execute_update(query, (pacote_id, servico['servico_id'], servico['quantidade']))
        
        return pacote_id
    
    def buscar_ativos(self) -> List[dict]:
        """Retorna todos os pacotes ativos"""
        return self.find_by_field('ativo', True)
    
    def buscar_com_servicos(self, pacote_id: int) -> Optional[dict]:
        """Busca pacote com lista de serviços incluídos"""
        query_pacote = "SELECT * FROM pacotes WHERE id = %s"
        pacote = self.execute_query(query_pacote, (pacote_id,))
        
        if not pacote:
            return None
        
        query_servicos = """
            SELECT s.*, ps.quantidade
            FROM servicos s
            JOIN pacotes_servicos ps ON s.id = ps.servico_id
            WHERE ps.pacote_id = %s
        """
        servicos = self.execute_query(query_servicos, (pacote_id,))
        
        resultado = pacote[0]
        resultado['servicos'] = servicos
        return resultado
    
    def atualizar_pacote(self, pacote: Pacote) -> bool:
        """Atualiza dados do pacote"""
        data = {
            'nome': pacote.nome,
            'descricao': pacote.descricao,
            'preco_total': pacote.preco_total,
            'desconto_percentual': pacote.desconto_percentual,
            'validade_dias': pacote.validade_dias,
            'ativo': pacote.ativo
        }
        return self.update(pacote.id, data)

class ClientePacoteDAO(BaseDAO):
    def __init__(self):
        super().__init__('clientes_pacotes')
    
    def contratar_pacote(self, cliente_id: int, pacote_id: int) -> Optional[int]:
        """Registra a contratação de um pacote por um cliente"""
        query_pacote = "SELECT validade_dias FROM pacotes WHERE id = %s"
        resultado = self.execute_query(query_pacote, (pacote_id,))
        
        if not resultado:
            return None
        
        validade_dias = resultado[0]['validade_dias']
        data_validade = datetime.now() + timedelta(days=validade_dias)
        
        data = {
            'cliente_id': cliente_id,
            'pacote_id': pacote_id,
            'data_validade': data_validade.date(),
            'servicos_utilizados': 0,
            'ativo': True
        }
        return self.create(data)
    
    def buscar_pacotes_cliente(self, cliente_id: int) -> List[dict]:
        """Busca pacotes contratados por um cliente"""
        query = """
            SELECT cp.*, p.nome as pacote_nome, p.desconto_percentual
            FROM clientes_pacotes cp
            JOIN pacotes p ON cp.pacote_id = p.id
            WHERE cp.cliente_id = %s
            ORDER BY cp.data_contratacao DESC
        """
        return self.execute_query(query, (cliente_id,))
    
    def buscar_pacotes_ativos(self, cliente_id: int) -> List[dict]:
        """Busca pacotes ativos e válidos de um cliente"""
        query = """
            SELECT cp.*, p.nome as pacote_nome, p.desconto_percentual
            FROM clientes_pacotes cp
            JOIN pacotes p ON cp.pacote_id = p.id
            WHERE cp.cliente_id = %s
            AND cp.ativo = TRUE
            AND cp.data_validade >= CURDATE()
            ORDER BY cp.data_contratacao DESC
        """
        return self.execute_query(query, (cliente_id,))
    
    def incrementar_uso(self, cliente_pacote_id: int) -> bool:
        """Incrementa o contador de serviços utilizados"""
        query = "UPDATE clientes_pacotes SET servicos_utilizados = servicos_utilizados + 1 WHERE id = %s"
        return self.execute_update(query, (cliente_pacote_id,)) > 0
    
    def desativar_pacote(self, cliente_pacote_id: int) -> bool:
        """Desativa um pacote contratado"""
        return self.update(cliente_pacote_id, {'ativo': False})