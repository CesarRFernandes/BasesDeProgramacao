from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
                             QTableWidget, QTableWidgetItem, QLabel,
                             QDialog, QFormLayout, QMessageBox, QComboBox,
                             QDoubleSpinBox, QSpinBox, QTextEdit, QListWidget)
from PyQt5.QtCore import Qt
from dao.pacote_dao import PacoteDAO, ClientePacoteDAO
from dao.servico_dao import ServicoDAO
from dao.cliente_dao import ClienteDAO
from controllers.pagamento_controller import PagamentoController

class PacoteView(QWidget):
    def __init__(self):
        super().__init__()
        self.pacote_dao = PacoteDAO()
        self.init_ui()
        self.carregar_pacotes()
    
    def init_ui(self):
        layout = QVBoxLayout()
        self.setLayout(layout)
        
        btn_layout = QHBoxLayout()
        btn_contratar = QPushButton("🛒 Contratar Pacote")
        btn_contratar.clicked.connect(self.contratar_pacote)
        btn_atualizar = QPushButton("🔄 Atualizar")
        btn_atualizar.clicked.connect(self.carregar_pacotes)
        
        btn_layout.addWidget(btn_contratar)
        btn_layout.addWidget(btn_atualizar)
        btn_layout.addStretch()
        layout.addLayout(btn_layout)
        
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels([
            "ID", "Nome", "Preço (R$)", "Desconto (%)", "Validade (dias)"
        ])
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        layout.addWidget(self.table)
    
    def carregar_pacotes(self):
        """Carrega todos os pacotes"""
        pacotes = self.pacote_dao.buscar_ativos()
        self.preencher_tabela(pacotes)
    
    def preencher_tabela(self, pacotes):
        """Preenche tabela com pacotes"""
        self.table.setRowCount(len(pacotes))
        for row, pacote in enumerate(pacotes):
            self.table.setItem(row, 0, QTableWidgetItem(str(pacote['id'])))
            self.table.setItem(row, 1, QTableWidgetItem(pacote['nome']))
            self.table.setItem(row, 2, QTableWidgetItem(f"{pacote['preco_total']:.2f}"))
            self.table.setItem(row, 3, QTableWidgetItem(f"{pacote['desconto_percentual']:.1f}"))
            self.table.setItem(row, 4, QTableWidgetItem(str(pacote['validade_dias'])))
    
    def contratar_pacote(self):
        """Abre diálogo para contratar pacote"""
        dialog = ContratarPacoteDialog(self)
        if dialog.exec_():
            cliente_id, pacote_id, tipo_pagamento = dialog.get_dados()
            
            controller = PagamentoController()
            sucesso, mensagem = controller.criar_pagamento_pacote(
                cliente_id, pacote_id, tipo_pagamento, usar_credito=True
            )
            
            if sucesso:
                QMessageBox.information(self, "Sucesso", mensagem)
            else:
                QMessageBox.warning(self, "Erro", mensagem)

class ContratarPacoteDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.cliente_dao = ClienteDAO()
        self.pacote_dao = PacoteDAO()
        self.setWindowTitle("Contratar Pacote")
        self.setModal(True)
        self.resize(500, 300)
        self.init_ui()
    
    def init_ui(self):
        layout = QFormLayout()
        
        self.cliente_combo = QComboBox()
        clientes = self.cliente_dao.buscar_ativos()
        for cliente in clientes:
            self.cliente_combo.addItem(cliente['nome'], cliente['id'])
        
        self.pacote_combo = QComboBox()
        pacotes = self.pacote_dao.buscar_ativos()
        for pacote in pacotes:
            self.pacote_combo.addItem(
                f"{pacote['nome']} - R$ {pacote['preco_total']:.2f}",
                pacote['id']
            )
        
        self.tipo_pagamento_combo = QComboBox()
        self.tipo_pagamento_combo.addItem("💳 Visa", "visa")
        self.tipo_pagamento_combo.addItem("💳 Mastercard", "mastercard")
        self.tipo_pagamento_combo.addItem("📱 Pix", "pix")
        self.tipo_pagamento_combo.addItem("💵 Dinheiro", "dinheiro")
        
        layout.addRow("Cliente*:", self.cliente_combo)
        layout.addRow("Pacote*:", self.pacote_combo)
        layout.addRow("Forma de Pagamento*:", self.tipo_pagamento_combo)
        
        btn_layout = QHBoxLayout()
        btn_confirmar = QPushButton("Confirmar")
        btn_confirmar.clicked.connect(self.accept)
        btn_cancelar = QPushButton("Cancelar")
        btn_cancelar.clicked.connect(self.reject)
        btn_layout.addWidget(btn_confirmar)
        btn_layout.addWidget(btn_cancelar)
        
        layout.addRow(btn_layout)
        self.setLayout(layout)
    
    def get_dados(self):
        """Retorna dados da contratação"""
        return (
            self.cliente_combo.currentData(),
            self.pacote_combo.currentData(),
            self.tipo_pagamento_combo.currentData()
        )