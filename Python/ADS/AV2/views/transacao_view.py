from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
                             QTableWidget, QTableWidgetItem, QLabel, QMessageBox,
                             QComboBox, QDateEdit, QGroupBox, QGridLayout,
                             QFileDialog, QHeaderView)
from PyQt5.QtCore import Qt, QDate
from PyQt5.QtGui import QColor
from dao.transacao_dao import TransacaoDAO
from dao.cliente_dao import ClienteDAO
from datetime import datetime, timedelta
import os

class TransacaoView(QWidget):
    def __init__(self):
        super().__init__()
        self.transacao_dao = TransacaoDAO()
        self.cliente_dao = ClienteDAO()
        self.init_ui()
        self.carregar_transacoes()
    
    def init_ui(self):
        layout = QVBoxLayout()
        self.setLayout(layout)
        
        # Grupo de Filtros
        filtros_group = QGroupBox("Filtros")
        filtros_layout = QGridLayout()
        
        filtros_layout.addWidget(QLabel("Cliente:"), 0, 0)
        self.cliente_combo = QComboBox()
        self.cliente_combo.addItem("Todos", None)
        clientes = self.cliente_dao.find_all()
        for cliente in clientes:
            self.cliente_combo.addItem(cliente['nome'], cliente['id'])
        filtros_layout.addWidget(self.cliente_combo, 0, 1)
        
        filtros_layout.addWidget(QLabel("Tipo:"), 0, 2)
        self.tipo_combo = QComboBox()
        self.tipo_combo.addItem("Todos")
        tipos = [
            'pagamento_servico',
            'pagamento_pacote',
            'credito_recebido',
            'credito_utilizado',
            'taxa_nao_comparecimento',
            'penalidade',
            'estorno',
            'reembolso'
        ]
        self.tipo_combo.addItems(tipos)
        filtros_layout.addWidget(self.tipo_combo, 0, 3)
        
        filtros_layout.addWidget(QLabel("Status:"), 1, 0)
        self.status_combo = QComboBox()
        self.status_combo.addItem("Todos")
        self.status_combo.addItems(['confirmado', 'pendente', 'cancelado'])
        filtros_layout.addWidget(self.status_combo, 1, 1)
        
        filtros_layout.addWidget(QLabel("Data Início:"), 1, 2)
        self.data_inicio = QDateEdit()
        self.data_inicio.setDate(QDate.currentDate().addDays(-30))
        self.data_inicio.setCalendarPopup(True)
        self.data_inicio.setDisplayFormat("dd/MM/yyyy")
        filtros_layout.addWidget(self.data_inicio, 1, 3)
        
        filtros_layout.addWidget(QLabel("Data Fim:"), 2, 0)
        self.data_fim = QDateEdit()
        self.data_fim.setDate(QDate.currentDate())
        self.data_fim.setCalendarPopup(True)
        self.data_fim.setDisplayFormat("dd/MM/yyyy")
        filtros_layout.addWidget(self.data_fim, 2, 1)
        
        btn_filtrar = QPushButton("🔍 Filtrar")
        btn_filtrar.clicked.connect(self.aplicar_filtros)
        filtros_layout.addWidget(btn_filtrar, 2, 2)
        
        btn_limpar = QPushButton("🗑️ Limpar Filtros")
        btn_limpar.clicked.connect(self.limpar_filtros)
        filtros_layout.addWidget(btn_limpar, 2, 3)
        
        filtros_group.setLayout(filtros_layout)
        layout.addWidget(filtros_group)
        
        # Estatísticas
        stats_group = QGroupBox("Resumo do Período")
        stats_layout = QHBoxLayout()
        
        self.receitas_label = QLabel("Receitas: R$ 0,00")
        self.receitas_label.setStyleSheet("font-size: 14px; font-weight: bold; color: green;")
        stats_layout.addWidget(self.receitas_label)
        
        self.despesas_label = QLabel("Despesas: R$ 0,00")
        self.despesas_label.setStyleSheet("font-size: 14px; font-weight: bold; color: red;")
        stats_layout.addWidget(self.despesas_label)
        
        self.saldo_label = QLabel("Saldo: R$ 0,00")
        self.saldo_label.setStyleSheet("font-size: 14px; font-weight: bold; color: blue;")
        stats_layout.addWidget(self.saldo_label)
        
        self.total_label = QLabel("Total de Transações: 0")
        self.total_label.setStyleSheet("font-size: 14px; font-weight: bold;")
        stats_layout.addWidget(self.total_label)
        
        stats_group.setLayout(stats_layout)
        layout.addWidget(stats_group)
        
        # Botões de ação
        btn_layout = QHBoxLayout()
        btn_exportar = QPushButton("📊 Exportar CSV")
        btn_exportar.clicked.connect(self.exportar_csv)
        btn_estatisticas = QPushButton("📈 Estatísticas Cliente")
        btn_estatisticas.clicked.connect(self.mostrar_estatisticas_cliente)
        btn_atualizar = QPushButton("🔄 Atualizar")
        btn_atualizar.clicked.connect(self.carregar_transacoes)
        
        btn_layout.addWidget(btn_exportar)
        btn_layout.addWidget(btn_estatisticas)
        btn_layout.addWidget(btn_atualizar)
        btn_layout.addStretch()
        layout.addLayout(btn_layout)
        
        # Tabela de transações
        self.table = QTableWidget()
        self.table.setColumnCount(10)
        self.table.setHorizontalHeaderLabels([
            "ID", "Data/Hora", "Cliente", "Tipo", "Método Pagamento", 
            "Valor (R$)", "Status", "Serviço/Pacote", "Agendamento ID", "Descrição"
        ])
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.setSortingEnabled(True)
        
        # Ajustar largura das colunas
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.Stretch)
        header.setSectionResizeMode(3, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(4, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(5, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(6, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(7, QHeaderView.Stretch)
        header.setSectionResizeMode(8, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(9, QHeaderView.Stretch)
        
        layout.addWidget(self.table)
        
        # Label de informações
        self.info_label = QLabel("Exibindo transações...")
        self.info_label.setStyleSheet("padding: 5px; background-color: #ecf0f1;")
        layout.addWidget(self.info_label)
    
    def carregar_transacoes(self):
        """Carrega todas as transações"""
        transacoes = self.transacao_dao.buscar_todas()
        self.preencher_tabela(transacoes)
        self.atualizar_estatisticas()
        self.info_label.setText(f"Total de transações: {len(transacoes)}")
    
    def aplicar_filtros(self):
        """Aplica filtros selecionados"""
        cliente_id = self.cliente_combo.currentData()
        tipo = self.tipo_combo.currentText()
        status = self.status_combo.currentText()
        data_inicio = self.data_inicio.date().toPyDate()
        data_fim = self.data_fim.date().toPyDate()
        
        transacoes = self.transacao_dao.buscar_com_filtros(
            cliente_id=cliente_id,
            tipo=tipo if tipo != 'Todos' else None,
            status=status if status != 'Todos' else None,
            data_inicio=data_inicio,
            data_fim=data_fim
        )
        
        self.preencher_tabela(transacoes)
        self.atualizar_estatisticas(data_inicio, data_fim)
        self.info_label.setText(f"Transações filtradas: {len(transacoes)}")
    
    def limpar_filtros(self):
        """Limpa todos os filtros"""
        self.cliente_combo.setCurrentIndex(0)
        self.tipo_combo.setCurrentIndex(0)
        self.status_combo.setCurrentIndex(0)
        self.data_inicio.setDate(QDate.currentDate().addDays(-30))
        self.data_fim.setDate(QDate.currentDate())
        self.carregar_transacoes()
    
    def preencher_tabela(self, transacoes):
        """Preenche tabela com transações"""
        self.table.setSortingEnabled(False)
        self.table.setRowCount(len(transacoes))
        
        for row, transacao in enumerate(transacoes):
            data_hora = transacao['data_hora'].strftime('%d/%m/%Y %H:%M')
            
            # Colorir linhas por status
            cor_fundo = None
            if transacao['status'] == 'pendente':
                cor_fundo = QColor(255, 255, 200)  # Amarelo claro
            elif transacao['status'] == 'cancelado':
                cor_fundo = QColor(255, 200, 200)  # Vermelho claro
            elif transacao['status'] == 'confirmado':
                cor_fundo = QColor(200, 255, 200)  # Verde claro
            
            items = [
                QTableWidgetItem(str(transacao['id'])),
                QTableWidgetItem(data_hora),
                QTableWidgetItem(transacao['cliente_nome']),
                QTableWidgetItem(self.formatar_tipo(transacao['tipo'])),
                QTableWidgetItem(transacao.get('metodo_pagamento', 'N/A')),
                QTableWidgetItem(f"{transacao['valor']:.2f}"),
                QTableWidgetItem(transacao['status'].upper()),
                QTableWidgetItem(transacao.get('servico_nome', transacao.get('pacote_nome', 'N/A'))),
                QTableWidgetItem(str(transacao.get('agendamento_id', 'N/A'))),
                QTableWidgetItem(transacao.get('descricao', ''))
            ]
            
            for col, item in enumerate(items):
                if cor_fundo:
                    item.setBackground(cor_fundo)
                self.table.setItem(row, col, item)
        
        self.table.setSortingEnabled(True)
    
    def formatar_tipo(self, tipo: str) -> str:
        """Formata o tipo de transação para exibição"""
        tipos_formatados = {
            'pagamento_servico': 'Pagamento Serviço',
            'pagamento_pacote': 'Pagamento Pacote',
            'credito_recebido': 'Crédito Recebido',
            'credito_utilizado': 'Crédito Utilizado',
            'taxa_nao_comparecimento': 'Taxa Não Comparecimento',
            'penalidade': 'Penalidade',
            'estorno': 'Estorno',
            'reembolso': 'Reembolso'
        }
        return tipos_formatados.get(tipo, tipo)
    
    def atualizar_estatisticas(self, data_inicio=None, data_fim=None):
        """Atualiza labels de estatísticas"""
        if not data_inicio:
            data_inicio = self.data_inicio.date().toPyDate()
        if not data_fim:
            data_fim = self.data_fim.date().toPyDate()
        
        totais = self.transacao_dao.calcular_totais_periodo(data_inicio, data_fim)
        
        receitas = totais['receitas']
        despesas = totais['despesas']
        saldo = receitas - despesas
        total = totais['total_transacoes']
        
        self.receitas_label.setText(f"Receitas: R$ {receitas:.2f}")
        self.despesas_label.setText(f"Despesas: R$ {despesas:.2f}")
        self.saldo_label.setText(f"Saldo: R$ {saldo:.2f}")
        self.total_label.setText(f"Total de Transações: {total}")
    
    def exportar_csv(self):
        """Exporta transações para CSV"""
        if self.table.rowCount() == 0:
            QMessageBox.warning(self, "Aviso", "Não há transações para exportar")
            return
        
        # Obter transações atuais (com filtros aplicados)
        cliente_id = self.cliente_combo.currentData()
        tipo = self.tipo_combo.currentText()
        status = self.status_combo.currentText()
        data_inicio = self.data_inicio.date().toPyDate()
        data_fim = self.data_fim.date().toPyDate()
        
        transacoes = self.transacao_dao.buscar_com_filtros(
            cliente_id=cliente_id,
            tipo=tipo if tipo != 'Todos' else None,
            status=status if status != 'Todos' else None,
            data_inicio=data_inicio,
            data_fim=data_fim
        )
        
        # Diálogo para salvar arquivo
        nome_arquivo, _ = QFileDialog.getSaveFileName(
            self,
            "Exportar Transações",
            f"transacoes_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            "CSV Files (*.csv)"
        )
        
        if nome_arquivo:
            if self.transacao_dao.exportar_csv(transacoes, nome_arquivo):
                QMessageBox.information(
                    self,
                    "Sucesso",
                    f"Transações exportadas com sucesso!\n\nArquivo: {nome_arquivo}"
                )
            else:
                QMessageBox.warning(self, "Erro", "Erro ao exportar transações")
    
    def mostrar_estatisticas_cliente(self):
        """Mostra estatísticas de um cliente específico"""
        from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton
        
        if self.cliente_combo.currentIndex() == 0:
            QMessageBox.warning(self, "Aviso", "Selecione um cliente nos filtros")
            return
        
        cliente_id = self.cliente_combo.currentData()
        cliente_nome = self.cliente_combo.currentText()
        
        stats = self.transacao_dao.buscar_estatisticas_cliente(cliente_id)
        
        dialog = QDialog(self)
        dialog.setWindowTitle(f"Estatísticas - {cliente_nome}")
        dialog.setModal(True)
        dialog.resize(400, 300)
        
        layout = QVBoxLayout()
        
        layout.addWidget(QLabel(f"<h2>Estatísticas de {cliente_nome}</h2>"))
        layout.addWidget(QLabel(f"<b>Total de Transações:</b> {stats['total_transacoes']}"))
        layout.addWidget(QLabel(f"<b>Valor Total:</b> R$ {stats['valor_total']:.2f}"))
        layout.addWidget(QLabel(f"<b>Total Pago:</b> R$ {stats['total_pago']:.2f}"))
        layout.addWidget(QLabel(f"<b>Total em Créditos:</b> R$ {stats['total_credito']:.2f}"))
        
        btn_fechar = QPushButton("Fechar")
        btn_fechar.clicked.connect(dialog.accept)
        layout.addWidget(btn_fechar)
        
        dialog.setLayout(layout)
        dialog.exec_()