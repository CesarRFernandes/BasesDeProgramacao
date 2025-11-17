from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QPushButton, QTabWidget, QLabel, QMessageBox)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from views.cliente_view import ClienteView
from views.tecnico_view import TecnicoView
from views.servico_view import ServicoView
from views.agendamento_view import AgendamentoView
from views.pacote_view import PacoteView
from views.pagamento_view import PagamentoView
from views.fila_espera_view import FilaEsperaView
from config.database import DatabaseConfig

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sistema de Agendamento - Reparos Automotivos")
        self.setGeometry(100, 100, 1200, 800)
        
        if not self.verificar_conexao():
            QMessageBox.critical(
                self,
                "Erro de Conexão",
                "Não foi possível conectar ao banco de dados.\n"
                "Verifique se o XAMPP está rodando e as configurações estão corretas."
            )
            return
        
        self.init_ui()
    
    def verificar_conexao(self):
        """Verifica conexão com banco de dados"""
        try:
            return DatabaseConfig.test_connection()
        except Exception as e:
            print(f"Erro ao verificar conexão: {e}")
            return False
    
    def init_ui(self):
        """Inicializa a interface"""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout()
        central_widget.setLayout(layout)
        
        header = QLabel("Sistema de Agendamento de Reparos Eletrônicos Automotivos")
        header.setFont(QFont("Arial", 16, QFont.Bold))
        header.setAlignment(Qt.AlignCenter)
        header.setStyleSheet("padding: 10px; background-color: #2c3e50; color: white;")
        layout.addWidget(header)
        
        self.tabs = QTabWidget()
        layout.addWidget(self.tabs)
        
        self.tabs.addTab(AgendamentoView(), "📅 Agendamentos")
        self.tabs.addTab(ClienteView(), "👤 Clientes")
        self.tabs.addTab(TecnicoView(), "🔧 Técnicos")
        self.tabs.addTab(ServicoView(), "⚙️ Serviços")
        self.tabs.addTab(PacoteView(), "📦 Pacotes")
        self.tabs.addTab(PagamentoView(), "💰 Pagamentos")
        self.tabs.addTab(FilaEsperaView(), "⏳ Fila de Espera")
        
        footer = QLabel("Sistema desenvolvido em Python + MySQL")
        footer.setAlignment(Qt.AlignCenter)
        footer.setStyleSheet("padding: 5px; background-color: #ecf0f1;")
        layout.addWidget(footer)