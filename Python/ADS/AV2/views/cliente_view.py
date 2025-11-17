from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
                             QTableWidget, QTableWidgetItem, QLineEdit, QLabel,
                             QDialog, QFormLayout, QMessageBox, QCheckBox, QGroupBox)
from PyQt5.QtCore import Qt
from dao.cliente_dao import ClienteDAO
from models import Cliente

class ClienteView(QWidget):
    def __init__(self):
        super().__init__()
        self.cliente_dao = ClienteDAO()
        self.init_ui()
        self.carregar_clientes()
    
    def init_ui(self):
        layout = QVBoxLayout()
        self.setLayout(layout)
        
        btn_layout = QHBoxLayout()
        btn_novo = QPushButton("➕ Novo Cliente")
        btn_novo.clicked.connect(self.novo_cliente)
        btn_editar = QPushButton("✏️ Editar")
        btn_editar.clicked.connect(self.editar_cliente)
        btn_desativar = QPushButton("🚫 Desativar")
        btn_desativar.clicked.connect(self.desativar_cliente)
        btn_atualizar = QPushButton("🔄 Atualizar")
        btn_atualizar.clicked.connect(self.carregar_clientes)
        
        btn_layout.addWidget(btn_novo)
        btn_layout.addWidget(btn_editar)
        btn_layout.addWidget(btn_desativar)
        btn_layout.addWidget(btn_atualizar)
        btn_layout.addStretch()
        layout.addLayout(btn_layout)
        
        search_layout = QHBoxLayout()
        search_layout.addWidget(QLabel("Buscar por nome:"))
        self.search_input = QLineEdit()
        self.search_input.textChanged.connect(self.buscar_clientes)
        search_layout.addWidget(self.search_input)
        layout.addLayout(search_layout)
        
        self.table = QTableWidget()
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels(["ID", "Nome", "CPF", "Telefone", "Email", "Endereço", "Ativo"])
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        layout.addWidget(self.table)
    
    def carregar_clientes(self):
        """Carrega todos os clientes na tabela"""
        clientes = self.cliente_dao.find_all()
        self.preencher_tabela(clientes)
    
    def buscar_clientes(self):
        """Busca clientes por nome"""
        nome = self.search_input.text()
        if nome:
            clientes = self.cliente_dao.buscar_por_nome(nome)
        else:
            clientes = self.cliente_dao.find_all()
        self.preencher_tabela(clientes)
    
    def preencher_tabela(self, clientes):
        """Preenche a tabela com os clientes"""
        self.table.setRowCount(len(clientes))
        for row, cliente in enumerate(clientes):
            self.table.setItem(row, 0, QTableWidgetItem(str(cliente['id'])))
            self.table.setItem(row, 1, QTableWidgetItem(cliente['nome']))
            self.table.setItem(row, 2, QTableWidgetItem(cliente['cpf']))
            self.table.setItem(row, 3, QTableWidgetItem(cliente['telefone']))
            self.table.setItem(row, 4, QTableWidgetItem(cliente.get('email', '')))
            self.table.setItem(row, 5, QTableWidgetItem(cliente.get('endereco', '')))
            self.table.setItem(row, 6, QTableWidgetItem("Sim" if cliente['ativo'] else "Não"))
    
    def novo_cliente(self):
        """Abre diálogo para novo cliente"""
        dialog = ClienteDialog(self)
        if dialog.exec_():
            cliente = dialog.get_cliente()
            cliente_id = self.cliente_dao.criar_cliente(cliente)
            if cliente_id:
                QMessageBox.information(self, "Sucesso", "Cliente cadastrado com sucesso!")
                self.carregar_clientes()
            else:
                QMessageBox.warning(self, "Erro", "Erro ao cadastrar cliente")
    
    def editar_cliente(self):
        """Edita cliente selecionado"""
        row = self.table.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Aviso", "Selecione um cliente")
            return
        
        cliente_id = int(self.table.item(row, 0).text())
        cliente_data = self.cliente_dao.find_by_id(cliente_id)
        
        if cliente_data:
            dialog = ClienteDialog(self, cliente_data)
            if dialog.exec_():
                cliente = dialog.get_cliente()
                cliente.id = cliente_id
                if self.cliente_dao.atualizar_cliente(cliente):
                    QMessageBox.information(self, "Sucesso", "Cliente atualizado!")
                    self.carregar_clientes()
    
    def desativar_cliente(self):
        """Desativa cliente selecionado"""
        row = self.table.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Aviso", "Selecione um cliente")
            return
        
        cliente_id = int(self.table.item(row, 0).text())
        reply = QMessageBox.question(self, "Confirmar", "Desativar este cliente?",
                                    QMessageBox.Yes | QMessageBox.No)
        
        if reply == QMessageBox.Yes:
            if self.cliente_dao.desativar_cliente(cliente_id):
                QMessageBox.information(self, "Sucesso", "Cliente desativado!")
                self.carregar_clientes()

class ClienteDialog(QDialog):
    def __init__(self, parent=None, cliente_data=None):
        super().__init__(parent)
        self.cliente_data = cliente_data
        self.setWindowTitle("Cliente")
        self.setModal(True)
        self.init_ui()
    
    def init_ui(self):
        layout = QFormLayout()
        
        self.nome_input = QLineEdit()
        self.cpf_input = QLineEdit()
        self.telefone_input = QLineEdit()
        self.email_input = QLineEdit()
        self.endereco_input = QLineEdit()
        self.ativo_check = QCheckBox()
        self.ativo_check.setChecked(True)
        
        if self.cliente_data:
            self.nome_input.setText(self.cliente_data['nome'])
            self.cpf_input.setText(self.cliente_data['cpf'])
            self.telefone_input.setText(self.cliente_data['telefone'])
            self.email_input.setText(self.cliente_data.get('email', ''))
            self.endereco_input.setText(self.cliente_data.get('endereco', ''))
            self.ativo_check.setChecked(self.cliente_data['ativo'])
        
        layout.addRow("Nome*:", self.nome_input)
        layout.addRow("CPF*:", self.cpf_input)
        layout.addRow("Telefone*:", self.telefone_input)
        layout.addRow("Email:", self.email_input)
        layout.addRow("Endereço:", self.endereco_input)
        layout.addRow("Ativo:", self.ativo_check)
        
        btn_layout = QHBoxLayout()
        btn_salvar = QPushButton("Salvar")
        btn_salvar.clicked.connect(self.accept)
        btn_cancelar = QPushButton("Cancelar")
        btn_cancelar.clicked.connect(self.reject)
        btn_layout.addWidget(btn_salvar)
        btn_layout.addWidget(btn_cancelar)
        
        layout.addRow(btn_layout)
        self.setLayout(layout)
    
    def get_cliente(self):
        """Retorna objeto Cliente com dados do formulário"""
        return Cliente(
            nome=self.nome_input.text(),
            cpf=self.cpf_input.text(),
            telefone=self.telefone_input.text(),
            email=self.email_input.text(),
            endereco=self.endereco_input.text(),
            ativo=self.ativo_check.isChecked()
        )