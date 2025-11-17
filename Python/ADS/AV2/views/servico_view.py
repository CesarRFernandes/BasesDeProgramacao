from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
                             QTableWidget, QTableWidgetItem, QLineEdit, QLabel,
                             QDialog, QFormLayout, QMessageBox, QCheckBox,
                             QComboBox, QSpinBox, QDoubleSpinBox, QTextEdit)
from PyQt5.QtCore import Qt
from dao.servico_dao import ServicoDAO, EspecialidadeDAO
from models import Servico

class ServicoView(QWidget):
    def __init__(self):
        super().__init__()
        self.servico_dao = ServicoDAO()
        self.init_ui()
        self.carregar_servicos()
    
    def init_ui(self):
        layout = QVBoxLayout()
        self.setLayout(layout)
        
        btn_layout = QHBoxLayout()
        btn_novo = QPushButton("➕ Novo Serviço")
        btn_novo.clicked.connect(self.novo_servico)
        btn_editar = QPushButton("✏️ Editar")
        btn_editar.clicked.connect(self.editar_servico)
        btn_atualizar = QPushButton("🔄 Atualizar")
        btn_atualizar.clicked.connect(self.carregar_servicos)
        
        btn_layout.addWidget(btn_novo)
        btn_layout.addWidget(btn_editar)
        btn_layout.addWidget(btn_atualizar)
        btn_layout.addStretch()
        layout.addLayout(btn_layout)
        
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels([
            "ID", "Nome", "Duração (min)", "Preço (R$)", "Especialidade", "Ativo"
        ])
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        layout.addWidget(self.table)
    
    def carregar_servicos(self):
        """Carrega todos os serviços"""
        servicos = self.servico_dao.buscar_ativos()
        self.preencher_tabela(servicos)
    
    def preencher_tabela(self, servicos):
        """Preenche tabela com serviços"""
        self.table.setRowCount(len(servicos))
        for row, servico in enumerate(servicos):
            self.table.setItem(row, 0, QTableWidgetItem(str(servico['id'])))
            self.table.setItem(row, 1, QTableWidgetItem(servico['nome']))
            self.table.setItem(row, 2, QTableWidgetItem(str(servico['duracao_minutos'])))
            self.table.setItem(row, 3, QTableWidgetItem(f"{servico['preco']:.2f}"))
            self.table.setItem(row, 4, QTableWidgetItem(servico['especialidade_nome']))
            self.table.setItem(row, 5, QTableWidgetItem("Sim" if servico['ativo'] else "Não"))
    
    def novo_servico(self):
        """Abre diálogo para novo serviço"""
        dialog = ServicoDialog(self)
        if dialog.exec_():
            servico = dialog.get_servico()
            servico_id = self.servico_dao.criar_servico(servico)
            if servico_id:
                QMessageBox.information(self, "Sucesso", "Serviço cadastrado com sucesso!")
                self.carregar_servicos()
            else:
                QMessageBox.warning(self, "Erro", "Erro ao cadastrar serviço")
    
    def editar_servico(self):
        """Edita serviço selecionado"""
        row = self.table.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Aviso", "Selecione um serviço")
            return
        
        servico_id = int(self.table.item(row, 0).text())
        servico_data = self.servico_dao.find_by_id(servico_id)
        
        if servico_data:
            dialog = ServicoDialog(self, servico_data)
            if dialog.exec_():
                servico = dialog.get_servico()
                servico.id = servico_id
                if self.servico_dao.atualizar_servico(servico):
                    QMessageBox.information(self, "Sucesso", "Serviço atualizado!")
                    self.carregar_servicos()

class ServicoDialog(QDialog):
    def __init__(self, parent=None, servico_data=None):
        super().__init__(parent)
        self.servico_data = servico_data
        self.especialidade_dao = EspecialidadeDAO()
        self.setWindowTitle("Serviço")
        self.setModal(True)
        self.init_ui()
    
    def init_ui(self):
        layout = QFormLayout()
        
        self.nome_input = QLineEdit()
        self.descricao_input = QTextEdit()
        self.descricao_input.setMaximumHeight(80)
        
        self.duracao_input = QSpinBox()
        self.duracao_input.setRange(15, 480)
        self.duracao_input.setSuffix(" min")
        self.duracao_input.setValue(60)
        
        self.preco_input = QDoubleSpinBox()
        self.preco_input.setRange(0, 10000)
        self.preco_input.setPrefix("R$ ")
        self.preco_input.setDecimals(2)
        self.preco_input.setValue(100.00)
        
        self.especialidade_combo = QComboBox()
        especialidades = self.especialidade_dao.buscar_ativas()
        for esp in especialidades:
            self.especialidade_combo.addItem(esp['nome'], esp['id'])
        
        self.ativo_check = QCheckBox()
        self.ativo_check.setChecked(True)
        
        if self.servico_data:
            self.nome_input.setText(self.servico_data['nome'])
            self.descricao_input.setPlainText(self.servico_data.get('descricao', ''))
            self.duracao_input.setValue(self.servico_data['duracao_minutos'])
            self.preco_input.setValue(float(self.servico_data['preco']))
            
            index = self.especialidade_combo.findData(self.servico_data['especialidade_id'])
            if index >= 0:
                self.especialidade_combo.setCurrentIndex(index)
            
            self.ativo_check.setChecked(self.servico_data['ativo'])
        
        layout.addRow("Nome*:", self.nome_input)
        layout.addRow("Descrição:", self.descricao_input)
        layout.addRow("Duração*:", self.duracao_input)
        layout.addRow("Preço*:", self.preco_input)
        layout.addRow("Especialidade*:", self.especialidade_combo)
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
    
    def get_servico(self):
        """Retorna objeto Servico"""
        return Servico(
            nome=self.nome_input.text(),
            descricao=self.descricao_input.toPlainText(),
            duracao_minutos=self.duracao_input.value(),
            preco=self.preco_input.value(),
            especialidade_id=self.especialidade_combo.currentData(),
            ativo=self.ativo_check.isChecked()
        )