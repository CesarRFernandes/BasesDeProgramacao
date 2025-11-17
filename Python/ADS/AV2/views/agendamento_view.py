from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
                             QTableWidget, QTableWidgetItem, QLabel, QDialog,
                             QFormLayout, QMessageBox, QComboBox, QDateTimeEdit,
                             QTextEdit, QGroupBox)
from PyQt5.QtCore import Qt, QDateTime
from dao.agendamento_dao import AgendamentoDAO
from dao.cliente_dao import ClienteDAO
from dao.servico_dao import ServicoDAO
from dao.pacote_dao import ClientePacoteDAO
from controllers.agendamento_controller import AgendamentoController
from models import Agendamento
from datetime import datetime, date

class AgendamentoView(QWidget):
    def __init__(self):
        super().__init__()
        self.agendamento_dao = AgendamentoDAO()
        self.agendamento_controller = AgendamentoController()
        self.init_ui()
        self.carregar_proximos()
    
    def init_ui(self):
        layout = QVBoxLayout()
        self.setLayout(layout)
        
        btn_layout = QHBoxLayout()
        btn_novo = QPushButton("➕ Novo Agendamento")
        btn_novo.clicked.connect(self.novo_agendamento)
        btn_cancelar = QPushButton("❌ Cancelar")
        btn_cancelar.clicked.connect(self.cancelar_agendamento)
        btn_iniciar = QPushButton("▶️ Iniciar Atendimento")
        btn_iniciar.clicked.connect(self.iniciar_atendimento)
        btn_concluir = QPushButton("✅ Concluir")
        btn_concluir.clicked.connect(self.concluir_atendimento)
        btn_nao_compareceu = QPushButton("⚠️ Não Compareceu")
        btn_nao_compareceu.clicked.connect(self.registrar_nao_comparecimento)
        btn_atualizar = QPushButton("🔄 Atualizar")
        btn_atualizar.clicked.connect(self.carregar_proximos)
        
        btn_layout.addWidget(btn_novo)
        btn_layout.addWidget(btn_cancelar)
        btn_layout.addWidget(btn_iniciar)
        btn_layout.addWidget(btn_concluir)
        btn_layout.addWidget(btn_nao_compareceu)
        btn_layout.addWidget(btn_atualizar)
        btn_layout.addStretch()
        layout.addLayout(btn_layout)
        
        self.table = QTableWidget()
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels([
            "ID", "Data/Hora", "Cliente", "Técnico", "Serviço", "Tipo", "Status"
        ])
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        layout.addWidget(self.table)
    
    def carregar_proximos(self):
        """Carrega próximos agendamentos"""
        agendamentos = self.agendamento_controller.buscar_proximos_agendamentos(20)
        self.preencher_tabela(agendamentos)
    
    def preencher_tabela(self, agendamentos):
        """Preenche tabela com agendamentos"""
        self.table.setRowCount(len(agendamentos))
        for row, agendamento in enumerate(agendamentos):
            data_hora = agendamento['data_agendamento'].strftime('%d/%m/%Y %H:%M')
            self.table.setItem(row, 0, QTableWidgetItem(str(agendamento['id'])))
            self.table.setItem(row, 1, QTableWidgetItem(data_hora))
            self.table.setItem(row, 2, QTableWidgetItem(agendamento['cliente_nome']))
            self.table.setItem(row, 3, QTableWidgetItem(agendamento['tecnico_nome']))
            self.table.setItem(row, 4, QTableWidgetItem(agendamento['servico_nome']))
            self.table.setItem(row, 5, QTableWidgetItem(agendamento['tipo_atendimento']))
            self.table.setItem(row, 6, QTableWidgetItem(agendamento['status']))
    
    def novo_agendamento(self):
        """Abre diálogo para novo agendamento"""
        dialog = AgendamentoDialog(self)
        if dialog.exec_():
            agendamento = dialog.get_agendamento()
            sucesso, mensagem = self.agendamento_controller.criar_agendamento(agendamento)
            
            if sucesso:
                QMessageBox.information(self, "Sucesso", mensagem)
                self.carregar_proximos()
            else:
                QMessageBox.warning(self, "Erro", mensagem)
    
    def cancelar_agendamento(self):
        """Cancela agendamento selecionado"""
        row = self.table.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Aviso", "Selecione um agendamento")
            return
        
        agendamento_id = int(self.table.item(row, 0).text())
        reply = QMessageBox.question(self, "Confirmar", "Cancelar este agendamento?",
                                    QMessageBox.Yes | QMessageBox.No)
        
        if reply == QMessageBox.Yes:
            sucesso, mensagem = self.agendamento_controller.cancelar_agendamento(agendamento_id)
            if sucesso:
                QMessageBox.information(self, "Sucesso", mensagem)
                self.carregar_proximos()
            else:
                QMessageBox.warning(self, "Erro", mensagem)
    
    def iniciar_atendimento(self):
        """Inicia atendimento"""
        row = self.table.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Aviso", "Selecione um agendamento")
            return
        
        agendamento_id = int(self.table.item(row, 0).text())
        sucesso, mensagem = self.agendamento_controller.iniciar_atendimento(agendamento_id)
        
        if sucesso:
            QMessageBox.information(self, "Sucesso", mensagem)
            self.carregar_proximos()
        else:
            QMessageBox.warning(self, "Erro", mensagem)
    
    def concluir_atendimento(self):
        """Conclui atendimento"""
        row = self.table.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Aviso", "Selecione um agendamento")
            return
        
        agendamento_id = int(self.table.item(row, 0).text())
        sucesso, mensagem = self.agendamento_controller.concluir_atendimento(agendamento_id)
        
        if sucesso:
            QMessageBox.information(self, "Sucesso", mensagem)
            self.carregar_proximos()
        else:
            QMessageBox.warning(self, "Erro", mensagem)
    
    def registrar_nao_comparecimento(self):
        """Registra não comparecimento e aplica penalidade"""
        row = self.table.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Aviso", "Selecione um agendamento")
            return
        
        agendamento_id = int(self.table.item(row, 0).text())
        reply = QMessageBox.question(
            self, "Confirmar",
            "Registrar não comparecimento?\n\nSerá aplicada penalidade de 50% (taxa) + 50% (crédito)",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            sucesso, mensagem = self.agendamento_controller.registrar_nao_comparecimento(agendamento_id)
            if sucesso:
                QMessageBox.information(self, "Sucesso", mensagem)
                self.carregar_proximos()
            else:
                QMessageBox.warning(self, "Erro", mensagem)

class AgendamentoDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.cliente_dao = ClienteDAO()
        self.servico_dao = ServicoDAO()
        self.cliente_pacote_dao = ClientePacoteDAO()
        self.agendamento_controller = AgendamentoController()
        self.setWindowTitle("Novo Agendamento")
        self.setModal(True)
        self.resize(500, 400)
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
            self.servico_combo.addItem(
                f"{servico['nome']} - R$ {servico['preco']:.2f} ({servico['duracao_minutos']}min)",
                servico['id']
            )
        self.servico_combo.currentIndexChanged.connect(self.atualizar_tecnicos)
        
        self.data_hora_input = QDateTimeEdit()
        self.data_hora_input.setDateTime(QDateTime.currentDateTime())
        self.data_hora_input.setCalendarPopup(True)
        self.data_hora_input.setDisplayFormat("dd/MM/yyyy HH:mm")
        self.data_hora_input.dateTimeChanged.connect(self.atualizar_tecnicos)
        
        self.tecnico_combo = QComboBox()
        
        self.tipo_combo = QComboBox()
        self.tipo_combo.addItem("Com Reserva", "com_reserva")
        self.tipo_combo.addItem("Sem Reserva", "sem_reserva")
        
        self.pacote_combo = QComboBox()
        self.pacote_combo.addItem("Sem Pacote", None)
        self.cliente_combo.currentIndexChanged.connect(self.atualizar_pacotes)
        
        self.observacoes_input = QTextEdit()
        self.observacoes_input.setMaximumHeight(80)
        
        layout.addRow("Cliente*:", self.cliente_combo)
        layout.addRow("Serviço*:", self.servico_combo)
        layout.addRow("Data/Hora*:", self.data_hora_input)
        layout.addRow("Técnico*:", self.tecnico_combo)
        layout.addRow("Tipo Atendimento:", self.tipo_combo)
        layout.addRow("Usar Pacote:", self.pacote_combo)
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
        
        self.atualizar_tecnicos()
        self.atualizar_pacotes()
    
    def atualizar_tecnicos(self):
        """Atualiza lista de técnicos disponíveis"""
        self.tecnico_combo.clear()
        
        if self.servico_combo.count() == 0:
            return
        
        servico_id = self.servico_combo.currentData()
        data_hora = self.data_hora_input.dateTime().toPyDateTime()
        
        tecnicos = self.agendamento_controller.buscar_tecnicos_disponiveis(data_hora, servico_id)
        
        for tecnico in tecnicos:
            self.tecnico_combo.addItem(
                f"{tecnico['nome']} - {tecnico['especialidade_nome']}",
                tecnico['id']
            )
    
    def atualizar_pacotes(self):
        """Atualiza lista de pacotes do cliente"""
        self.pacote_combo.clear()
        self.pacote_combo.addItem("Sem Pacote", None)
        
        if self.cliente_combo.count() == 0:
            return
        
        cliente_id = self.cliente_combo.currentData()
        pacotes = self.cliente_pacote_dao.buscar_pacotes_ativos(cliente_id)
        
        for pacote in pacotes:
            self.pacote_combo.addItem(pacote['pacote_nome'], pacote['id'])
    
    def get_agendamento(self):
        """Retorna objeto Agendamento"""
        return Agendamento(
            cliente_id=self.cliente_combo.currentData(),
            tecnico_id=self.tecnico_combo.currentData(),
            servico_id=self.servico_combo.currentData(),
            data_agendamento=self.data_hora_input.dateTime().toPyDateTime(),
            tipo_atendimento=self.tipo_combo.currentData(),
            observacoes=self.observacoes_input.toPlainText(),
            cliente_pacote_id=self.pacote_combo.currentData()
        )