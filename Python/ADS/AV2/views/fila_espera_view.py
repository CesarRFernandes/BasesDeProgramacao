from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
                             QTableWidget, QTableWidgetItem, QLabel,
                             QMessageBox, QDialog, QFormLayout, QComboBox,
                             QDateEdit, QTextEdit, QSpinBox)
from PyQt5.QtCore import Qt, QDate
from dao.fila_espera_dao import FilaEsperaDAO
from dao.cliente_dao import ClienteDAO
from dao.servico_dao import ServicoDAO
from models import FilaEspera

class FilaEsperaView(QWidget):
    def __init__(self):
        super().__init__()
        self.fila_dao = FilaEsperaDAO()
        self.init_ui()
        self.carregar_fila()
    
    def init_ui(self):
        layout = QVBoxLayout()
        self.setLayout(layout)
        
        btn_layout = QHBoxLayout()
        btn_adicionar = QPushButton("➕ Adicionar à Fila")
        btn_adicionar.clicked.connect(self.adicionar_fila)
        btn_notificar = QPushButton("📧 Marcar como Notificado")
        btn_notificar.clicked.connect(self.marcar_notificado)
        btn_cancelar = QPushButton("❌ Cancelar")
        btn_cancelar.clicked.connect(self.cancelar_solicitacao)
        btn_aumentar_prioridade = QPushButton("⬆️ Aumentar Prioridade")
        btn_aumentar_prioridade.clicked.connect(self.aumentar_prioridade)
        btn_atualizar = QPushButton("🔄 Atualizar")
        btn_atualizar.clicked.connect(self.carregar_fila)
        
        btn_layout.addWidget(btn_adicionar)
        btn_layout.addWidget(btn_notificar)
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
    
    def marcar_notificado(self):
        """Marca solicitação como notificada"""
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