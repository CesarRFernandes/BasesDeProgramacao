import sys
from PyQt5.QtWidgets import QApplication
from views.main_window import MainWindow

def main():
    """Função principal que inicia a aplicação"""
    app = QApplication(sys.argv)
    
    app.setStyle('Fusion')
    
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()