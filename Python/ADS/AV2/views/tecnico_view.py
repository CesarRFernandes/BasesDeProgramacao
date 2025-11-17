from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
                             QTableWidget, QTableWidgetItem, QLineEdit, QLabel,
                             QDialog, QFormLayout, QMessageBox, QCheckBox, QComboBox,
                             QDateEdit)
from PyQt5.QtCore import Qt, QDate
from dao.tecnico_dao import TecnicoDAO
from dao.servico_dao import EspecialidadeDAO
from models import Tecnico

class TecnicoView(QWidget):
    def __init__(self):
        super().__init__()
        self.tecnico_dao = TecnicoDAO()
        self.init_ui()
        self.carregar_tecnicos()
    
    def init_ui(self):
        layout = QVBoxLayout()
        self.setLayout(layout)
        
        btn_layout = QHBoxLayout()
        btn_novo = QPushButton("➕ Novo Técnico")
        btn_novo.clicked.connect(self.novo_tecnico)
        btn_editar = QPushButton("✏️ Editar")
        btn_editar.clicked.connect(self.editar_tecnico)
        btn_atualizar = QPushButton("🔄 Atualizar")
        btn_atualizar.clicked.connect(self.carregar_tecnicos)
        
        btn_layout.addWidget(btn_novo)
        btn_layout.addWidget(btn_editar)
        btn_layout.addWidget(btn_atualizar)
        btn_layout.addStretch()
        layout.addLayout(btn_layout)
        
        self.table = QTableWidget()
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels([
            "ID", "Nome", "CPF", "Telefone", "Email", "Especialidade", "Ativo"
        ])
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        layout.addWidget(self.table)
    
    def carregar_tecnicos(self):
        """Carrega todos os técnicos"""
        tecnicos = self.tecnico_dao.buscar_com_especialidade()
        self.preencher_tabela(tecnicos)
    
    def preencher_tabela(self, tecnicos):
        """Preenche tabela com técnicos"""
        self.table.setRowCount(len(tecnicos))
        for row, tecnico in enumerate(tecnicos):
            self.table.setItem(row, 0, QTableWidgetItem(str(tecnico['id'])))
            self.table.setItem(row, 1, QTableWidgetItem(tecnico['nome']))
            self.table.setItem(row, 2, QTableWidgetItem(tecnico['cpf']))
            self.table.setItem(row, 3, QTableWidgetItem(tecnico['telefone']))
            self.table.setItem(row, 4, QTableWidgetItem(tecnico.get('email', '')))
            self.table.setItem(row, 5, QTableWidgetItem(tecnico['especialidade_nome']))
            self.table.setItem(row, 6, QTableWidgetItem("Sim" if tecnico['ativo'] else "Não"))
    
    def novo_tecnico(self):
        """Abre diálogo para novo técnico"""
        dialog = TecnicoDialog(self)
        if dialog.exec_():
            tecnico = dialog.get_tecnico()
            tecnico_id = self.tecnico_dao.criar_tecnico(tecnico)
            if tecnico_id:
                QMessageBox.information(self, "Sucesso", "Técnico cadastrado com sucesso!")
                self.carregar_tecnicos()
            else:
                QMessageBox.warning(self, "Erro", "Erro ao cadastrar técnico")
    
    def editar_tecnico(self):
        """Edita técnico selecionado"""
        row = self.table.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Aviso", "Selecione um técnico")
            return
        
        tecnico_id = int(self.table.item(row, 0).text())
        tecnico_data = self.tecnico_dao.find_by_id(tecnico_id)
        
        if tecnico_data:
            dialog = TecnicoDialog(self, tecnico_data)
            if dialog.exec_():
                tecnico = dialog.get_tecnico()
                tecnico.id = tecnico_id
                if self.tecnico_dao.atualizar_tecnico(tecnico):
                    QMessageBox.information(self, "Sucesso", "Técnico atualizado!")
                    self.carregar_tecnicos()

class TecnicoDialog(QDialog):
    def __init__(self, parent=None, tecnico_data=None):
        super().__init__(parent)
        self.tecnico_data = tecnico_data
        self.especialidade_dao = EspecialidadeDAO()
        self.setWindowTitle("Técnico")
        self.setModal(True)
        self.init_ui()
    
    def init_ui(self):
        layout = QFormLayout()
        
        self.nome_input = QLineEdit()
        self.cpf_input = QLineEdit()
        self.telefone_input = QLineEdit()
        self.email_input = QLineEdit()
        
        self.especialidade_combo = QComboBox()
        especialidades = self.especialidade_dao.buscar_ativas()
        for esp in especialidades:
            self.especialidade_combo.addItem(esp['nome'], esp['id'])
        
        self.data_contratacao_input = QDateEdit()
        self.data_contratacao_input.setDate(QDate.currentDate())
        self.data_contratacao_input.setCalendarPopup(True)
        
        self.ativo_check = QCheckBox()
        self.ativo_check.setChecked(True)
        
        if self.tecnico_data:
            self.nome_input.setText(self.tecnico_data['nome'])
            self.cpf_input.setText(self.tecnico_data['cpf'])
            self.telefone_input.setText(self.tecnico_data['telefone'])
            self.email_input.setText(self.tecnico_data.get('email', ''))
            
            index = self.especialidade_combo.findData(self.tecnico_data['especialidade_id'])
            if index >= 0:
                self.especialidade_combo.setCurrentIndex(index)
            
            self.data_contratacao_input.setDate(QDate(self.tecnico_data['data_contratacao']))
            self.ativo_check.setChecked(self.tecnico_data['ativo'])
        
        layout.addRow("Nome*:", self.nome_input)
        layout.addRow("CPF*:", self.cpf_input)
        layout.addRow("Telefone*:", self.telefone_input)
        layout.addRow("Email:", self.email_input)
        layout.addRow("Especialidade*:", self.especialidade_combo)
        layout.addRow("Data Contratação:", self.data_contratacao_input)
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
    
    def get_tecnico(self):
        """Retorna objeto Tecnico"""
        return Tecnico(
            nome=self.nome_input.text(),
            cpf=self.cpf_input.text(),
            telefone=self.telefone_input.text(),
            email=self.email_input.text(),
            especialidade_id=self.especialidade_combo.currentData(),
            data_contratacao=self.data_contratacao_input.date().toPyDate(),
            ativo=self.ativo_check.isChecked()
        )