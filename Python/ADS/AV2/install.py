#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script de instalação e verificação do sistema
Executa verificações básicas antes de rodar o sistema
"""

import sys
import os

def verificar_python():
    """Verifica versão do Python"""
    print("Verificando versão do Python...")
    version = sys.version_info
    if version.major >= 3 and version.minor >= 8:
        print(f"✓ Python {version.major}.{version.minor}.{version.micro} - OK")
        return True
    else:
        print(f"✗ Python {version.major}.{version.minor}.{version.micro} - Requer Python 3.8+")
        return False

def verificar_dependencias():
    """Verifica se as dependências estão instaladas"""
    print("\nVerificando dependências...")
    
    dependencias = {
        'PyQt5': 'PyQt5',
        'mysql.connector': 'mysql-connector-python'
    }
    
    faltando = []
    
    for modulo, pacote in dependencias.items():
        try:
            __import__(modulo)
            print(f"✓ {pacote} - Instalado")
        except ImportError:
            print(f"✗ {pacote} - Não instalado")
            faltando.append(pacote)
    
    if faltando:
        print("\n⚠️  Dependências faltando. Execute:")
        print(f"pip install {' '.join(faltando)}")
        return False
    
    return True

def verificar_estrutura():
    """Verifica se a estrutura de pastas existe"""
    print("\nVerificando estrutura do projeto...")
    
    pastas = [
        'config',
        'models',
        'dao',
        'controllers',
        'views'
    ]
    
    todas_ok = True
    for pasta in pastas:
        if os.path.isdir(pasta):
            print(f"✓ Pasta '{pasta}' - OK")
        else:
            print(f"✗ Pasta '{pasta}' - Não encontrada")
            todas_ok = False
    
    return todas_ok

def verificar_banco():
    """Tenta conectar ao banco de dados"""
    print("\nVerificando conexão com banco de dados...")
    
    try:
        from config.database import DatabaseConfig
        
        if DatabaseConfig.test_connection():
            print("✓ Conexão com MySQL - OK")
            return True
        else:
            print("✗ Não foi possível conectar ao MySQL")
            print("\n⚠️  Verifique:")
            print("1. XAMPP está rodando (Apache e MySQL)")
            print("2. Banco 'automotive_repair_system' foi criado")
            print("3. Configurações em config/database.py estão corretas")
            return False
    except Exception as e:
        print(f"✗ Erro ao verificar banco: {e}")
        return False

def main():
    """Função principal"""
    print("=" * 60)
    print("Sistema de Agendamento de Reparos Eletrônicos Automotivos")
    print("Script de Verificação de Instalação")
    print("=" * 60)
    
    tudo_ok = True
    
    if not verificar_python():
        tudo_ok = False
    
    if not verificar_dependencias():
        tudo_ok = False
    
    if not verificar_estrutura():
        tudo_ok = False
    
    if not verificar_banco():
        tudo_ok = False
    
    print("\n" + "=" * 60)
    
    if tudo_ok:
        print("✓ Todas as verificações passaram!")
        print("\nPara executar o sistema, rode:")
        print("python main.py")
    else:
        print("✗ Algumas verificações falharam.")
        print("\nResolva os problemas acima antes de executar o sistema.")
    
    print("=" * 60)

if __name__ == "__main__":
    main()