from dao.agendamento_dao import AgendamentoDAO
from dao.tecnico_dao import TecnicoDAO
from dao.servico_dao import ServicoDAO
from dao.pagamento_dao import PagamentoDAO, PenalidadeDAO, CreditoDAO
from dao.pacote_dao import ClientePacoteDAO
from dao.transacao_dao import TransacaoDAO
from models import Agendamento, Pagamento
from typing import Optional, List
from datetime import datetime

class AgendamentoController:
    def __init__(self):
        self.agendamento_dao = AgendamentoDAO()
        self.tecnico_dao = TecnicoDAO()
        self.servico_dao = ServicoDAO()
        self.pagamento_dao = PagamentoDAO()
        self.penalidade_dao = PenalidadeDAO()
        self.credito_dao = CreditoDAO()
        self.cliente_pacote_dao = ClientePacoteDAO()
        self.transacao_dao = TransacaoDAO()
    
    def criar_agendamento(self, agendamento: Agendamento) -> tuple[bool, str]:
        """Cria um novo agendamento com validações"""
        try:
            if agendamento.data_agendamento < datetime.now():
                return False, "Data do agendamento não pode ser no passado"
            
            if self.agendamento_dao.verificar_conflito_tecnico(
                agendamento.tecnico_id,
                agendamento.data_agendamento,
                agendamento.duracao_minutos
            ):
                return False, "Técnico já possui agendamento neste horário"
            
            servico = self.servico_dao.find_by_id(agendamento.servico_id)
            if not servico:
                return False, "Serviço não encontrado"
            
            tecnico = self.tecnico_dao.find_by_id(agendamento.tecnico_id)
            if not tecnico:
                return False, "Técnico não encontrado"
            
            if tecnico['especialidade_id'] != servico['especialidade_id']:
                return False, "Técnico não possui especialidade necessária para este serviço"
            
            agendamento.duracao_minutos = servico['duracao_minutos']
            
            agendamento_id = self.agendamento_dao.criar_agendamento(agendamento)
            
            if agendamento_id:
                if agendamento.cliente_pacote_id:
                    self.cliente_pacote_dao.incrementar_uso(agendamento.cliente_pacote_id)
                
                return True, f"Agendamento criado com sucesso! ID: {agendamento_id}"
            
            return False, "Erro ao criar agendamento"
            
        except Exception as e:
            return False, f"Erro ao criar agendamento: {str(e)}"
    
    def buscar_tecnicos_disponiveis(self, data_hora: datetime, servico_id: int) -> List[dict]:
        """Busca técnicos disponíveis para um serviço em determinado horário"""
        try:
            servico = self.servico_dao.find_by_id(servico_id)
            if not servico:
                return []
            
            duracao = servico['duracao_minutos']
            tecnicos = self.tecnico_dao.buscar_disponiveis(data_hora, duracao)
            
            tecnicos_qualificados = [
                t for t in tecnicos 
                if t['especialidade_id'] == servico['especialidade_id']
            ]
            
            return tecnicos_qualificados
            
        except Exception as e:
            print(f"Erro ao buscar técnicos disponíveis: {e}")
            return []
    
    def cancelar_agendamento(self, agendamento_id: int) -> tuple[bool, str]:
        """Cancela um agendamento"""
        try:
            agendamento = self.agendamento_dao.find_by_id(agendamento_id)
            
            if not agendamento:
                return False, "Agendamento não encontrado"
            
            if agendamento['status'] == 'cancelado':
                return False, "Agendamento já está cancelado"
            
            if self.agendamento_dao.atualizar_status(agendamento_id, 'cancelado'):
                return True, "Agendamento cancelado com sucesso"
            
            return False, "Erro ao cancelar agendamento"
            
        except Exception as e:
            return False, f"Erro ao cancelar: {str(e)}"
    
    def registrar_nao_comparecimento(self, agendamento_id: int) -> tuple[bool, str]:
        """Registra não comparecimento e aplica penalidade"""
        try:
            agendamento = self.agendamento_dao.buscar_detalhado(agendamento_id)
            
            if not agendamento:
                return False, "Agendamento não encontrado"
            
            self.agendamento_dao.atualizar_status(agendamento_id, 'nao_compareceu')
            
            valor_servico = float(agendamento['servico_preco'])
            penalidade_id = self.penalidade_dao.aplicar_penalidade(
                agendamento['cliente_id'],
                agendamento_id,
                valor_servico
            )
            
            if penalidade_id:
                valor_credito = valor_servico * 0.5
                self.credito_dao.criar_credito(
                    agendamento['cliente_id'],
                    penalidade_id,
                    valor_credito
                )
                
                valor_taxa = valor_servico * 0.5
                pagamento = Pagamento(
                    agendamento_id=agendamento_id,
                    cliente_id=agendamento['cliente_id'],
                    valor=valor_taxa,
                    tipo_pagamento='dinheiro',
                    status='pendente',
                    descricao='Taxa de não comparecimento (50%)'
                )
                self.pagamento_dao.criar_pagamento(pagamento)
                
                return True, f"Penalidade aplicada: R$ {valor_taxa:.2f} taxa + R$ {valor_credito:.2f} crédito"
            
            return False, "Erro ao aplicar penalidade"
            
        except Exception as e:
            return False, f"Erro ao registrar não comparecimento: {str(e)}"
    
    def iniciar_atendimento(self, agendamento_id: int) -> tuple[bool, str]:
        """Marca agendamento como em atendimento"""
        try:
            if self.agendamento_dao.atualizar_status(agendamento_id, 'em_atendimento'):
                return True, "Atendimento iniciado"
            return False, "Erro ao iniciar atendimento"
        except Exception as e:
            return False, f"Erro: {str(e)}"
    
    def concluir_atendimento(self, agendamento_id: int) -> tuple[bool, str]:
        """Marca agendamento como concluído"""
        try:
            if self.agendamento_dao.atualizar_status(agendamento_id, 'concluido'):
                return True, "Atendimento concluído"
            return False, "Erro ao concluir atendimento"
        except Exception as e:
            return False, f"Erro: {str(e)}"
    
    def buscar_agendamentos_data(self, data) -> List[dict]:
        """Busca agendamentos de uma data"""
        return self.agendamento_dao.buscar_por_data(data)
    
    def buscar_proximos_agendamentos(self, limite: int = 10) -> List[dict]:
        """Busca próximos agendamentos"""
        return self.agendamento_dao.buscar_proximos(limite)