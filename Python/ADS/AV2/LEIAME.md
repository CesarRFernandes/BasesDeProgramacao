Sistema de Agendamento de Reparos Eletrônicos Automotivos
---------------------------------------------------------

Sistema desktop desenvolvido por Caio Fusco e César Rosa, utilizando Python (PyQt5) e MySQL, para gerenciamento de agendamentos de reparos eletrônicos automotivos.

---------------------------------------------------------
PRÉ-REQUISITOS — SOFTWARES NECESSÁRIOS
---------------------------------------------------------

1. Python 3.8+
Download: https://www.python.org/downloads/

2. XAMPP (Apache + MySQL)
Download: https://www.apachefriends.org/
Versão recomendada: 8.0+

---------------------------------------------------------
VERIFICAR INSTALAÇÕES
---------------------------------------------------------

No CMD ou Terminal:

python --version
pip --version


---------------------------------------------------------
PASSO 1 – CONFIGURAR O BANCO DE DADOS
---------------------------------------------------------

1.1 Acessar o phpMyAdmin:
- Abra o navegador
- Acesse: http://localhost/phpmyadmin
- Usuário: root
- Senha: (em branco)

1.2 Criar o Banco:
- Clique na aba SQL
- Execute o arquivo database_schema.sql


---------------------------------------------------------
PASSO 2 – CRIAR AMBIENTE VIRTUAL (RECOMENDADO)
---------------------------------------------------------

Windows:
cd C:\caminho\para\o\projeto
python -m venv venv
venv\Scripts\activate

Linux/Mac:
cd /caminho/para/o/projeto
python3 -m venv venv
source venv/bin/activate


---------------------------------------------------------
PASSO 3 – INSTALAR DEPENDÊNCIAS
---------------------------------------------------------

pip install -r requirements.txt

Ou manualmente:
pip install PyQt5==5.15.9
pip install mysql-connector-python==8.2.0


---------------------------------------------------------
PASSO 4 – CONFIGURAR CONEXÃO COM O BANCO
---------------------------------------------------------

Arquivo: config/database.py

class DatabaseConfig:
    HOST = 'localhost'
    PORT = 3306
    DATABASE = 'automotive_repair_system'
    USER = 'root'
    PASSWORD = ''


---------------------------------------------------------
PASSO 5 – VERIFICAR INSTALAÇÃO
---------------------------------------------------------

python install.py


---------------------------------------------------------
COMO EXECUTAR
---------------------------------------------------------

Windows:
cd C:\caminho\para\o\projeto
venv\Scripts\activate   (se estiver usando venv)
python main.py

Linux/Mac:
cd /caminho/para/o/projeto
source venv/bin/activate   (se estiver usando venv)
python3 main.py