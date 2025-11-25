from dao.pagamento_dao import PagamentoDAO, CreditoDAO
from dao.agendamento_dao import AgendamentoDAO
from dao.pacote_dao import ClientePacoteDAO
from dao.transacao_dao import TransacaoDAO
from models import Pagamento
from typing import Optional, List
from datetime import datetime

class PagamentoController:
    def __init__(self):
        self.pagamento_dao = PagamentoDAO()
        self.credito_dao = CreditoDAO()
        self.agendamento_dao = AgendamentoDAO()
        self.cliente_pacote_dao = ClientePacoteDAO()
        self.transacao_dao = TransacaoDAO()
    
    def criar_pagamento_agendamento(self, agendamento_id: int, tipo_pagamento: str,
                                   usar_credito: bool = False) -> tuple[bool, str]:
        """Cria pagamento para um agendamento"""
        try:
            agendamento = self.agendamento_dao.buscar_detalhado(agendamento_id)
            
            if not agendamento:
                return False, "Agendamento não encontrado"
            
            valor_total = float(agendamento['servico_preco'])
            valor_a_pagar = valor_total
            creditos_utilizados = []
            
            if usar_credito:
                creditos = self.credito_dao.buscar_creditos_disponiveis(agendamento['cliente_id'])
                
                for credito in creditos:
                    if valor_a_pagar <= 0:
                        break
                    
                    saldo_credito = float(credito['saldo'])
                    valor_usar = min(saldo_credito, valor_a_pagar)
                    
                    if self.credito_dao.utilizar_credito(credito['id'], valor_usar):
                        creditos_utilizados.append({
                            'id': credito['id'],
                            'valor': valor_usar
                        })
                        valor_a_pagar -= valor_usar
            
            if valor_a_pagar > 0:
                pagamento = Pagamento(
                    agendamento_id=agendamento_id,
                    cliente_id=agendamento['cliente_id'],
                    valor=valor_a_pagar,
                    tipo_pagamento=tipo_pagamento,
                    status='pendente',
                    descricao=f"Pagamento do serviço: {agendamento['servico_nome']}"
                )
                
                pagamento_id = self.pagamento_dao.criar_pagamento(pagamento)
                
                if not pagamento_id:
                    return False, "Erro ao criar pagamento"
            
            mensagem = f"Pagamento processado! Valor total: R$ {valor_total:.2f}"
            if creditos_utilizados:
                total_creditos = sum(c['valor'] for c in creditos_utilizados)
                mensagem += f" | Créditos utilizados: R$ {total_creditos:.2f}"
                
                # Registrar uso de crédito nas transações
                for credito in creditos_utilizados:
                    self.transacao_dao.registrar_transacao(
                        cliente_id=agendamento['cliente_id'],
                        tipo='credito_utilizado',
                        valor=credito['valor'],
                        agendamento_id=agendamento_id,
                        status='confirmado',
                        descricao=f"Crédito utilizado no pagamento do agendamento {agendamento_id}"
                    )
            
            if valor_a_pagar > 0:
                mensagem += f" | Valor a pagar: R$ {valor_a_pagar:.2f}"
            
            return True, mensagem
            
        except Exception as e:
            return False, f"Erro ao processar pagamento: {str(e)}"
    
    def confirmar_pagamento(self, pagamento_id: int) -> tuple[bool, str]:
        """Confirma um pagamento"""
        try:
            if self.pagamento_dao.confirmar_pagamento(pagamento_id):
                return True, "Pagamento confirmado com sucesso"
            return False, "Erro ao confirmar pagamento"
        except Exception as e:
            return False, f"Erro: {str(e)}"
    
    def criar_pagamento_pacote(self, cliente_id: int, pacote_id: int,
                              tipo_pagamento: str, usar_credito: bool = False) -> tuple[bool, str]:
        """Cria pagamento para contratação de pacote"""
        try:
            from dao.pacote_dao import PacoteDAO
            pacote_dao = PacoteDAO()
            
            pacote = pacote_dao.find_by_id(pacote_id)
            if not pacote:
                return False, "Pacote não encontrado"
            
            valor_total = float(pacote['preco_total'])
            valor_a_pagar = valor_total
            
            if usar_credito:
                creditos = self.credito_dao.buscar_creditos_disponiveis(cliente_id)
                
                for credito in creditos:
                    if valor_a_pagar <= 0:
                        break
                    
                    saldo_credito = float(credito['saldo'])
                    valor_usar = min(saldo_credito, valor_a_pagar)
                    
                    if self.credito_dao.utilizar_credito(credito['id'], valor_usar):
                        valor_a_pagar -= valor_usar
                        
                        # Registrar uso de crédito
                        self.transacao_dao.registrar_transacao(
                            cliente_id=cliente_id,
                            tipo='credito_utilizado',
                            valor=valor_usar,
                            pacote_id=pacote_id,
                            status='confirmado',
                            descricao=f"Crédito utilizado na contratação do pacote"
                        )
            
            cliente_pacote_id = self.cliente_pacote_dao.contratar_pacote(cliente_id, pacote_id)
            
            if not cliente_pacote_id:
                return False, "Erro ao contratar pacote"
            
            if valor_a_pagar > 0:
                pagamento = Pagamento(
                    cliente_pacote_id=cliente_pacote_id,
                    cliente_id=cliente_id,
                    valor=valor_a_pagar,
                    tipo_pagamento=tipo_pagamento,
                    status='pendente',
                    descricao=f"Contratação do pacote: {pacote['nome']}"
                )
                
                pagamento_id = self.pagamento_dao.criar_pagamento(pagamento)
                
                if pagamento_id:
                    self.pagamento_dao.confirmar_pagamento(pagamento_id)
            
            return True, f"Pacote contratado com sucesso! ID: {cliente_pacote_id}"
            
        except Exception as e:
            return False, f"Erro ao processar pagamento do pacote: {str(e)}"
    
    def buscar_saldo_creditos(self, cliente_id: int) -> float:
        """Busca saldo total de créditos disponíveis"""
        return self.credito_dao.calcular_saldo_total(cliente_id)
    
    def buscar_creditos_cliente(self, cliente_id: int) -> List[dict]:
        """Busca créditos disponíveis de um cliente"""
        return self.credito_dao.buscar_creditos_disponiveis(cliente_id)
    
    def buscar_pagamentos_pendentes(self) -> List[dict]:
        """Busca todos os pagamentos pendentes"""
        return self.pagamento_dao.buscar_pendentes()
    
    def buscar_historico_cliente(self, cliente_id: int) -> List[dict]:
        """Busca histórico de pagamentos de um cliente"""
        return self.pagamento_dao.buscar_por_cliente(cliente_id)