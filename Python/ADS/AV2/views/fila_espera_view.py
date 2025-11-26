from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
                             QTableWidget, QTableWidgetItem, QLabel,
                             QMessageBox, QDialog, QFormLayout, QComboBox,
                             QDateEdit, QTextEdit, QSpinBox, QCheckBox, QGroupBox)
from PyQt5.QtCore import Qt, QDate, QDateTime
from dao.fila_espera_dao import FilaEsperaDAO
from dao.cliente_dao import ClienteDAO
from dao.servico_dao import ServicoDAO
from dao.tecnico_dao import TecnicoDAO
from dao.agendamento_dao import AgendamentoDAO
from controllers.agendamento_controller import AgendamentoController
from controllers.pagamento_controller import PagamentoController
from models import FilaEspera, Agendamento
from datetime import datetime

class FilaEsperaView(QWidget):
    def __init__(self):
        super().__init__()
        self.fila_dao = FilaEsperaDAO()
        self.agendamento_controller = AgendamentoController()
        self.pagamento_controller = PagamentoController()
        self.init_ui()
        self.carregar_fila()
    
    def init_ui(self):
        layout = QVBoxLayout()
        self.setLayout(layout)
        
        btn_layout = QHBoxLayout()
        btn_adicionar = QPushButton("➕ Adicionar à Fila")
        btn_adicionar.clicked.connect(self.adicionar_fila)
        btn_atender = QPushButton("▶️ Começar Atendimento")
        btn_atender.clicked.connect(self.comecar_atendimento)
        btn_atender.setStyleSheet("background-color: #27ae60; color: white; font-weight: bold;")
        btn_cancelar = QPushButton("❌ Cancelar")
        btn_cancelar.clicked.connect(self.cancelar_solicitacao)
        btn_aumentar_prioridade = QPushButton("⬆️ Aumentar Prioridade")
        btn_aumentar_prioridade.clicked.connect(self.aumentar_prioridade)
        btn_atualizar = QPushButton("🔄 Atualizar")
        btn_atualizar.clicked.connect(self.carregar_fila)
        
        btn_layout.addWidget(btn_adicionar)
        btn_layout.addWidget(btn_atender)
        btn_layout.addWidget(btn_cancelar)
        btn_layout.addWidget(btn_aumentar_prioridade)
        btn_layout.addWidget(btn_atualizar)
        btn_layout.addStretch()
        layout.addLayout(btn_layout)
        
        label = QLabel("Fila de Espera - Aguardando")
        label.setStyleSheet("font-weight: bold; font-size: 14px; padding: 5px;")
        layout.addWidget(label)
        
        self.table = QTableWidget()
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels([
            "ID", "Cliente", "Telefone", "Serviço", "Data Preferência", 
            "Prioridade", "Status"
        ])
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        layout.addWidget(self.table)
    
    def carregar_fila(self):
        """Carrega fila de espera"""
        fila = self.fila_dao.buscar_aguardando()
        self.preencher_tabela(fila)
    
    def preencher_tabela(self, fila):
        """Preenche tabela com a fila"""
        self.table.setRowCount(len(fila))
        for row, item in enumerate(fila):
            data_pref = item['data_preferencia'].strftime('%d/%m/%Y') if item['data_preferencia'] else 'N/A'
            self.table.setItem(row, 0, QTableWidgetItem(str(item['id'])))
            self.table.setItem(row, 1, QTableWidgetItem(item['cliente_nome']))
            self.table.setItem(row, 2, QTableWidgetItem(item['cliente_telefone']))
            self.table.setItem(row, 3, QTableWidgetItem(item['servico_nome']))
            self.table.setItem(row, 4, QTableWidgetItem(data_pref))
            self.table.setItem(row, 5, QTableWidgetItem(str(item['prioridade'])))
            self.table.setItem(row, 6, QTableWidgetItem(item['status']))
    
    def adicionar_fila(self):
        """Adiciona cliente à fila"""
        dialog = FilaEsperaDialog(self)
        if dialog.exec_():
            fila = dialog.get_fila()
            fila_id = self.fila_dao.adicionar_fila(fila)
            if fila_id:
                QMessageBox.information(self, "Sucesso", "Cliente adicionado à fila!")
                self.carregar_fila()
            else:
                QMessageBox.warning(self, "Erro", "Erro ao adicionar à fila")
    
    def comecar_atendimento(self):
        """Cria agendamento imediato e abre tela de pagamento"""
        row = self.table.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Aviso", "Selecione um cliente da fila")
            return
        
        fila_id = int(self.table.item(row, 0).text())
        
        # Buscar dados da fila
        fila_data = self.fila_dao.find_by_id(fila_id)
        
        if not fila_data:
            QMessageBox.warning(self, "Erro", "Registro não encontrado")
            return
        
        # Abrir diálogo para selecionar técnico e confirmar atendimento
        dialog = IniciarAtendimentoDialog(self, fila_data)
        if dialog.exec_():
            tecnico_id = dialog.get_tecnico_id()
            
            # Criar agendamento imediato
            agendamento = Agendamento(
                cliente_id=fila_data['cliente_id'],
                tecnico_id=tecnico_id,
                servico_id=fila_data['servico_id'],
                data_agendamento=datetime.now(),
                tipo_atendimento='sem_reserva',
                status='em_atendimento',
                observacoes=f"Atendimento iniciado da fila de espera (ID: {fila_id})"
            )
            
            # Criar agendamento
            sucesso, mensagem = self.agendamento_controller.criar_agendamento(agendamento)
            
            if sucesso:
                # Extrair ID do agendamento da mensagem
                import re
                match = re.search(r'ID: (\d+)', mensagem)
                if match:
                    agendamento_id = int(match.group(1))
                    
                    # Marcar na fila como agendado
                    self.fila_dao.atualizar_status(fila_id, 'agendado')
                    
                    # Buscar detalhes do agendamento
                    agendamento_detalhes = self.agendamento_controller.buscar_agendamento_detalhado(agendamento_id)
                    
                    if agendamento_detalhes:
                        # Abrir diálogo de pagamento
                        pagamento_dialog = PagamentoFilaDialog(self, agendamento_detalhes)
                        if pagamento_dialog.exec_():
                            QMessageBox.information(
                                self, 
                                "Sucesso", 
                                "Atendimento iniciado e pagamento processado!\nCliente removido da fila de espera."
                            )
                            self.carregar_fila()
                        else:
                            QMessageBox.information(
                                self, 
                                "Atenção", 
                                "Atendimento iniciado, mas pagamento não foi processado.\nCliente removido da fila de espera."
                            )
                            self.carregar_fila()
                else:
                    QMessageBox.information(self, "Sucesso", mensagem)
                    self.carregar_fila()
            else:
                QMessageBox.warning(self, "Erro", mensagem)
    
    def marcar_notificado(self):
        """Marca solicitação como notificada (mantido para compatibilidade)"""
        row = self.table.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Aviso", "Selecione uma solicitação")
            return
        
        fila_id = int(self.table.item(row, 0).text())
        if self.fila_dao.atualizar_status(fila_id, 'notificado'):
            QMessageBox.information(self, "Sucesso", "Cliente notificado!")
            self.carregar_fila()
    
    def cancelar_solicitacao(self):
        """Cancela solicitação da fila"""
        row = self.table.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Aviso", "Selecione uma solicitação")
            return
        
        fila_id = int(self.table.item(row, 0).text())
        reply = QMessageBox.question(
            self, "Confirmar",
            "Cancelar esta solicitação?",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            if self.fila_dao.atualizar_status(fila_id, 'cancelado'):
                QMessageBox.information(self, "Sucesso", "Solicitação cancelada!")
                self.carregar_fila()
    
    def aumentar_prioridade(self):
        """Aumenta prioridade de uma solicitação"""
        row = self.table.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Aviso", "Selecione uma solicitação")
            return
        
        fila_id = int(self.table.item(row, 0).text())
        if self.fila_dao.aumentar_prioridade(fila_id):
            QMessageBox.information(self, "Sucesso", "Prioridade aumentada!")
            self.carregar_fila()

class FilaEsperaDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.cliente_dao = ClienteDAO()
        self.servico_dao = ServicoDAO()
        self.setWindowTitle("Adicionar à Fila de Espera")
        self.setModal(True)
        self.resize(400, 300)
        self.init_ui()
    
    def init_ui(self):
        layout = QFormLayout()
        
        self.cliente_combo = QComboBox()
        clientes = self.cliente_dao.buscar_ativos()
        for cliente in clientes:
            self.cliente_combo.addItem(cliente['nome'], cliente['id'])
        
        self.servico_combo = QComboBox()
        servicos = self.servico_dao.buscar_ativos()
        for servico in servicos:
            self.servico_combo.addItem(servico['nome'], servico['id'])
        
        self.data_preferencia_input = QDateEdit()
        self.data_preferencia_input.setDate(QDate.currentDate())
        self.data_preferencia_input.setCalendarPopup(True)
        
        self.prioridade_input = QSpinBox()
        self.prioridade_input.setRange(0, 10)
        self.prioridade_input.setValue(0)
        
        self.observacoes_input = QTextEdit()
        self.observacoes_input.setMaximumHeight(80)
        
        layout.addRow("Cliente*:", self.cliente_combo)
        layout.addRow("Serviço*:", self.servico_combo)
        layout.addRow("Data Preferência:", self.data_preferencia_input)
        layout.addRow("Prioridade:", self.prioridade_input)
        layout.addRow("Observações:", self.observacoes_input)
        
        btn_layout = QHBoxLayout()
        btn_salvar = QPushButton("Salvar")
        btn_salvar.clicked.connect(self.accept)
        btn_cancelar = QPushButton("Cancelar")
        btn_cancelar.clicked.connect(self.reject)
        btn_layout.addWidget(btn_salvar)
        btn_layout.addWidget(btn_cancelar)
        
        layout.addRow(btn_layout)
        self.setLayout(layout)
    
    def get_fila(self):
        """Retorna objeto FilaEspera"""
        return FilaEspera(
            cliente_id=self.cliente_combo.currentData(),
            servico_id=self.servico_combo.currentData(),
            data_preferencia=self.data_preferencia_input.date().toPyDate(),
            prioridade=self.prioridade_input.value(),
            observacoes=self.observacoes_input.toPlainText()
        )

class IniciarAtendimentoDialog(QDialog):
    """Diálogo para selecionar técnico antes de iniciar atendimento"""
    def __init__(self, parent=None, fila_data=None):
        super().__init__(parent)
        self.fila_data = fila_data
        self.tecnico_dao = TecnicoDAO()
        self.servico_dao = ServicoDAO()
        self.setWindowTitle("Iniciar Atendimento - Selecionar Técnico")
        self.setModal(True)
        self.resize(450, 300)
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout()
        
        # Informações do cliente e serviço
        info_group = QGroupBox("Informações do Atendimento")
        info_layout = QFormLayout()
        
        # Buscar nome do serviço
        servico = self.servico_dao.find_by_id(self.fila_data['servico_id'])
        servico_nome = servico['nome'] if servico else 'N/A'
        
        info_layout.addRow("Cliente:", QLabel(f"ID: {self.fila_data['cliente_id']}"))
        info_layout.addRow("Serviço:", QLabel(servico_nome))
        
        if self.fila_data.get('data_preferencia'):
            info_layout.addRow("Data Preferência:", QLabel(str(self.fila_data['data_preferencia'])))
        
        if self.fila_data.get('observacoes'):
            info_layout.addRow("Observações:", QLabel(self.fila_data['observacoes']))
        
        info_group.setLayout(info_layout)
        layout.addWidget(info_group)
        
        # Seleção de técnico
        tecnico_group = QGroupBox("Selecionar Técnico")
        tecnico_layout = QFormLayout()
        
        self.tecnico_combo = QComboBox()
        
        # Buscar técnicos disponíveis com a especialidade correta
        if servico:
            tecnicos = self.tecnico_dao.buscar_por_especialidade(servico['especialidade_id'])
            
            if tecnicos:
                for tecnico in tecnicos:
                    self.tecnico_combo.addItem(
                        f"{tecnico['nome']} - {tecnico['especialidade_nome']}",
                        tecnico['id']
                    )
            else:
                QMessageBox.warning(
                    self, 
                    "Aviso", 
                    f"Nenhum técnico disponível com a especialidade necessária:\n{servico.get('especialidade_nome', 'N/A')}"
                )
        
        tecnico_layout.addRow("Técnico*:", self.tecnico_combo)
        
        info_label = QLabel("O atendimento será iniciado imediatamente (sem reserva)")
        info_label.setStyleSheet("color: #3498db; font-style: italic;")
        tecnico_layout.addRow("", info_label)
        
        tecnico_group.setLayout(tecnico_layout)
        layout.addWidget(tecnico_group)
        
        # Botões
        btn_layout = QHBoxLayout()
        btn_iniciar = QPushButton("▶️ Iniciar Atendimento")
        btn_iniciar.clicked.connect(self.accept)
        btn_iniciar.setStyleSheet("background-color: #27ae60; color: white; padding: 10px;")
        btn_cancelar = QPushButton("❌ Cancelar")
        btn_cancelar.clicked.connect(self.reject)
        
        btn_layout.addWidget(btn_iniciar)
        btn_layout.addWidget(btn_cancelar)
        
        layout.addLayout(btn_layout)
        self.setLayout(layout)
    
    def get_tecnico_id(self):
        """Retorna ID do técnico selecionado"""
        return self.tecnico_combo.currentData()

class PagamentoFilaDialog(QDialog):
    """Diálogo para processar pagamento de atendimento da fila"""
    def __init__(self, parent=None, agendamento=None):
        super().__init__(parent)
        self.agendamento = agendamento
        self.pagamento_controller = PagamentoController()
        self.setWindowTitle("Processar Pagamento")
        self.setModal(True)
        self.resize(500, 400)
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout()
        
        # Informações do agendamento
        info_group = QGroupBox("Informações do Atendimento")
        info_layout = QFormLayout()
        
        info_layout.addRow("Cliente:", QLabel(self.agendamento['cliente_nome']))
        info_layout.addRow("Serviço:", QLabel(self.agendamento['servico_nome']))
        
        valor_label = QLabel(f"R$ {self.agendamento['servico_preco']:.2f}")
        valor_label.setStyleSheet("font-size: 16px; font-weight: bold; color: green;")
        info_layout.addRow("Valor:", valor_label)
        
        info_group.setLayout(info_layout)
        layout.addWidget(info_group)
        
        # Opções de pagamento
        pagamento_group = QGroupBox("Forma de Pagamento")
        pagamento_layout = QFormLayout()
        
        self.tipo_pagamento_combo = QComboBox()
        self.tipo_pagamento_combo.addItem("💵 Dinheiro", "dinheiro")
        self.tipo_pagamento_combo.addItem("💳 Visa", "visa")
        self.tipo_pagamento_combo.addItem("💳 Mastercard", "mastercard")
        self.tipo_pagamento_combo.addItem("📱 Pix", "pix")
        pagamento_layout.addRow("Método:", self.tipo_pagamento_combo)
        
        self.usar_credito_check = QCheckBox("Usar créditos disponíveis")
        self.usar_credito_check.setChecked(True)
        self.usar_credito_check.stateChanged.connect(self.atualizar_valor)
        pagamento_layout.addRow("", self.usar_credito_check)
        
        # Verificar créditos disponíveis
        saldo_creditos = self.pagamento_controller.buscar_saldo_creditos(
            self.agendamento['cliente_id']
        )
        
        self.creditos_label = QLabel(f"Créditos disponíveis: R$ {saldo_creditos:.2f}")
        self.creditos_label.setStyleSheet("color: blue; font-weight: bold;")
        pagamento_layout.addRow("", self.creditos_label)
        
        self.valor_pagar_label = QLabel(f"Valor a pagar: R$ {self.agendamento['servico_preco']:.2f}")
        self.valor_pagar_label.setStyleSheet("font-size: 14px; font-weight: bold; color: red;")
        pagamento_layout.addRow("", self.valor_pagar_label)
        
        pagamento_group.setLayout(pagamento_layout)
        layout.addWidget(pagamento_group)
        
        # Botões
        btn_layout = QHBoxLayout()
        btn_processar = QPushButton("✅ Processar Pagamento")
        btn_processar.clicked.connect(self.processar_pagamento)
        btn_processar.setStyleSheet("background-color: #27ae60; color: white; padding: 10px;")
        btn_cancelar = QPushButton("❌ Cancelar")
        btn_cancelar.clicked.connect(self.reject)
        
        btn_layout.addWidget(btn_processar)
        btn_layout.addWidget(btn_cancelar)
        
        layout.addLayout(btn_layout)
        self.setLayout(layout)
        
        self.atualizar_valor()
    
    def atualizar_valor(self):
        """Atualiza o valor a pagar considerando créditos"""
        if self.usar_credito_check.isChecked():
            saldo_creditos = self.pagamento_controller.buscar_saldo_creditos(
                self.agendamento['cliente_id']
            )
            valor_servico = float(self.agendamento['servico_preco'])
            valor_a_pagar = max(0, valor_servico - saldo_creditos)
            
            self.valor_pagar_label.setText(f"Valor a pagar: R$ {valor_a_pagar:.2f}")
        else:
            self.valor_pagar_label.setText(
                f"Valor a pagar: R$ {self.agendamento['servico_preco']:.2f}"
            )
    
    def processar_pagamento(self):
        """Processa o pagamento do agendamento"""
        tipo_pagamento = self.tipo_pagamento_combo.currentData()
        usar_credito = self.usar_credito_check.isChecked()
        
        sucesso, mensagem = self.pagamento_controller.criar_pagamento_agendamento(
            self.agendamento['id'],
            tipo_pagamento,
            usar_credito
        )
        
        if sucesso:
            QMessageBox.information(self, "Sucesso", mensagem)
            self.accept()
        else:
            QMessageBox.warning(self, "Erro", mensagem)