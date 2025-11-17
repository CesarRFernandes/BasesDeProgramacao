from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
                             QTableWidget, QTableWidgetItem, QLabel,
                             QMessageBox, QComboBox, QDialog, QFormLayout)
from PyQt5.QtCore import Qt
from controllers.pagamento_controller import PagamentoController
from dao.cliente_dao import ClienteDAO

class PagamentoView(QWidget):
    def __init__(self):
        super().__init__()
        self.pagamento_controller = PagamentoController()
        self.init_ui()
        self.carregar_pendentes()
    
    def init_ui(self):
        layout = QVBoxLayout()
        self.setLayout(layout)
        
        btn_layout = QHBoxLayout()
        btn_confirmar = QPushButton("✅ Confirmar Pagamento")
        btn_confirmar.clicked.connect(self.confirmar_pagamento)
        btn_creditos = QPushButton("💰 Consultar Créditos")
        btn_creditos.clicked.connect(self.consultar_creditos)
        btn_atualizar = QPushButton("🔄 Atualizar")
        btn_atualizar.clicked.connect(self.carregar_pendentes)
        
        btn_layout.addWidget(btn_confirmar)
        btn_layout.addWidget(btn_creditos)
        btn_layout.addWidget(btn_atualizar)
        btn_layout.addStretch()
        layout.addLayout(btn_layout)
        
        label = QLabel("Pagamentos Pendentes")
        label.setStyleSheet("font-weight: bold; font-size: 14px; padding: 5px;")
        layout.addWidget(label)
        
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels([
            "ID", "Cliente", "Valor (R$)", "Tipo", "Status", "Data"
        ])
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        layout.addWidget(self.table)
    
    def carregar_pendentes(self):
        """Carrega pagamentos pendentes"""
        pagamentos = self.pagamento_controller.buscar_pagamentos_pendentes()
        self.preencher_tabela(pagamentos)
    
    def preencher_tabela(self, pagamentos):
        """Preenche tabela com pagamentos"""
        self.table.setRowCount(len(pagamentos))
        for row, pagamento in enumerate(pagamentos):
            data = pagamento['data_criacao'].strftime('%d/%m/%Y')
            self.table.setItem(row, 0, QTableWidgetItem(str(pagamento['id'])))
            self.table.setItem(row, 1, QTableWidgetItem(pagamento['cliente_nome']))
            self.table.setItem(row, 2, QTableWidgetItem(f"{pagamento['valor']:.2f}"))
            self.table.setItem(row, 3, QTableWidgetItem(pagamento['tipo_pagamento']))
            self.table.setItem(row, 4, QTableWidgetItem(pagamento['status']))
            self.table.setItem(row, 5, QTableWidgetItem(data))
    
    def confirmar_pagamento(self):
        """Confirma pagamento selecionado"""
        row = self.table.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Aviso", "Selecione um pagamento")
            return
        
        pagamento_id = int(self.table.item(row, 0).text())
        reply = QMessageBox.question(
            self, "Confirmar",
            "Confirmar este pagamento?",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            sucesso, mensagem = self.pagamento_controller.confirmar_pagamento(pagamento_id)
            if sucesso:
                QMessageBox.information(self, "Sucesso", mensagem)
                self.carregar_pendentes()
            else:
                QMessageBox.warning(self, "Erro", mensagem)
    
    def consultar_creditos(self):
        """Abre diálogo para consultar créditos de cliente"""
        dialog = ConsultarCreditosDialog(self)
        dialog.exec_()

class ConsultarCreditosDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.cliente_dao = ClienteDAO()
        self.pagamento_controller = PagamentoController()
        self.setWindowTitle("Consultar Créditos")
        self.setModal(True)
        self.resize(500, 400)
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout()
        
        form_layout = QFormLayout()
        
        self.cliente_combo = QComboBox()
        clientes = self.cliente_dao.buscar_ativos()
        for cliente in clientes:
            self.cliente_combo.addItem(cliente['nome'], cliente['id'])
        
        self.cliente_combo.currentIndexChanged.connect(self.atualizar_creditos)
        form_layout.addRow("Cliente:", self.cliente_combo)
        
        layout.addLayout(form_layout)
        
        self.saldo_label = QLabel("Saldo total: R$ 0,00")
        self.saldo_label.setStyleSheet("font-size: 16px; font-weight: bold; padding: 10px;")
        layout.addWidget(self.saldo_label)
        
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels([
            "ID", "Valor (R$)", "Saldo (R$)", "Validade"
        ])
        layout.addWidget(self.table)
        
        btn_fechar = QPushButton("Fechar")
        btn_fechar.clicked.connect(self.accept)
        layout.addWidget(btn_fechar)
        
        self.setLayout(layout)
        self.atualizar_creditos()
    
    def atualizar_creditos(self):
        """Atualiza lista de créditos"""
        if self.cliente_combo.count() == 0:
            return
        
        cliente_id = self.cliente_combo.currentData()
        
        saldo = self.pagamento_controller.buscar_saldo_creditos(cliente_id)
        self.saldo_label.setText(f"Saldo total: R$ {saldo:.2f}")
        
        creditos = self.pagamento_controller.buscar_creditos_cliente(cliente_id)
        
        self.table.setRowCount(len(creditos))
        for row, credito in enumerate(creditos):
            validade = credito['data_validade'].strftime('%d/%m/%Y')
            self.table.setItem(row, 0, QTableWidgetItem(str(credito['id'])))
            self.table.setItem(row, 1, QTableWidgetItem(f"{credito['valor']:.2f}"))
            self.table.setItem(row, 2, QTableWidgetItem(f"{credito['saldo']:.2f}"))
            self.table.setItem(row, 3, QTableWidgetItem(validade))