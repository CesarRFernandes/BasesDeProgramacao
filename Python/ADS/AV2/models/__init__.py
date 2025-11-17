from datetime import datetime, date
from typing import Optional

class Cliente:
    def __init__(self, id=None, nome='', cpf='', telefone='', email='', 
                 endereco='', data_cadastro=None, ativo=True):
        self.id = id
        self.nome = nome
        self.cpf = cpf
        self.telefone = telefone
        self.email = email
        self.endereco = endereco
        self.data_cadastro = data_cadastro or datetime.now()
        self.ativo = ativo

class Especialidade:
    def __init__(self, id=None, nome='', descricao='', ativo=True):
        self.id = id
        self.nome = nome
        self.descricao = descricao
        self.ativo = ativo

class Tecnico:
    def __init__(self, id=None, nome='', cpf='', telefone='', email='',
                 especialidade_id=None, data_contratacao=None, ativo=True):
        self.id = id
        self.nome = nome
        self.cpf = cpf
        self.telefone = telefone
        self.email = email
        self.especialidade_id = especialidade_id
        self.data_contratacao = data_contratacao or date.today()
        self.ativo = ativo

class Servico:
    def __init__(self, id=None, nome='', descricao='', duracao_minutos=0,
                 preco=0.0, especialidade_id=None, ativo=True):
        self.id = id
        self.nome = nome
        self.descricao = descricao
        self.duracao_minutos = duracao_minutos
        self.preco = preco
        self.especialidade_id = especialidade_id
        self.ativo = ativo

class Pacote:
    def __init__(self, id=None, nome='', descricao='', preco_total=0.0,
                 desconto_percentual=0.0, validade_dias=180, ativo=True,
                 data_criacao=None):
        self.id = id
        self.nome = nome
        self.descricao = descricao
        self.preco_total = preco_total
        self.desconto_percentual = desconto_percentual
        self.validade_dias = validade_dias
        self.ativo = ativo
        self.data_criacao = data_criacao or datetime.now()

class ClientePacote:
    def __init__(self, id=None, cliente_id=None, pacote_id=None,
                 data_contratacao=None, data_validade=None,
                 servicos_utilizados=0, ativo=True):
        self.id = id
        self.cliente_id = cliente_id
        self.pacote_id = pacote_id
        self.data_contratacao = data_contratacao or datetime.now()
        self.data_validade = data_validade
        self.servicos_utilizados = servicos_utilizados
        self.ativo = ativo

class Agendamento:
    def __init__(self, id=None, cliente_id=None, tecnico_id=None,
                 servico_id=None, data_agendamento=None, duracao_minutos=0,
                 tipo_atendimento='com_reserva', status='agendado',
                 observacoes='', data_criacao=None, cliente_pacote_id=None):
        self.id = id
        self.cliente_id = cliente_id
        self.tecnico_id = tecnico_id
        self.servico_id = servico_id
        self.data_agendamento = data_agendamento
        self.duracao_minutos = duracao_minutos
        self.tipo_atendimento = tipo_atendimento
        self.status = status
        self.observacoes = observacoes
        self.data_criacao = data_criacao or datetime.now()
        self.cliente_pacote_id = cliente_pacote_id

class FilaEspera:
    def __init__(self, id=None, cliente_id=None, servico_id=None,
                 data_solicitacao=None, data_preferencia=None, prioridade=0,
                 status='aguardando', observacoes=''):
        self.id = id
        self.cliente_id = cliente_id
        self.servico_id = servico_id
        self.data_solicitacao = data_solicitacao or datetime.now()
        self.data_preferencia = data_preferencia
        self.prioridade = prioridade
        self.status = status
        self.observacoes = observacoes

class Pagamento:
    def __init__(self, id=None, agendamento_id=None, cliente_pacote_id=None,
                 cliente_id=None, valor=0.0, tipo_pagamento='dinheiro',
                 status='pendente', data_pagamento=None, data_criacao=None,
                 descricao=''):
        self.id = id
        self.agendamento_id = agendamento_id
        self.cliente_pacote_id = cliente_pacote_id
        self.cliente_id = cliente_id
        self.valor = valor
        self.tipo_pagamento = tipo_pagamento
        self.status = status
        self.data_pagamento = data_pagamento
        self.data_criacao = data_criacao or datetime.now()
        self.descricao = descricao

class Penalidade:
    def __init__(self, id=None, cliente_id=None, agendamento_id=None,
                 valor_total=0.0, valor_taxa=0.0, valor_credito=0.0,
                 data_aplicacao=None, utilizado=False):
        self.id = id
        self.cliente_id = cliente_id
        self.agendamento_id = agendamento_id
        self.valor_total = valor_total
        self.valor_taxa = valor_taxa
        self.valor_credito = valor_credito
        self.data_aplicacao = data_aplicacao or datetime.now()
        self.utilizado = utilizado

class Credito:
    def __init__(self, id=None, cliente_id=None, penalidade_id=None,
                 valor=0.0, saldo=0.0, data_criacao=None, data_validade=None,
                 ativo=True):
        self.id = id
        self.cliente_id = cliente_id
        self.penalidade_id = penalidade_id
        self.valor = valor
        self.saldo = saldo
        self.data_criacao = data_criacao or datetime.now()
        self.data_validade = data_validade
        self.ativo = ativo