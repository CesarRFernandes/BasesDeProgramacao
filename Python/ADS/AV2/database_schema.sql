-- Sistema de Agendamento de Reparos Eletrônicos Automotivos
-- Executar este script no MySQL via phpMyAdmin (XAMPP)

CREATE DATABASE IF NOT EXISTS reparos_automotivos_bd 
CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

USE reparos_automotivos_bd;

-- Tabela de Clientes
CREATE TABLE clientes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    cpf VARCHAR(14) UNIQUE NOT NULL,
    telefone VARCHAR(20) NOT NULL,
    email VARCHAR(100),
    endereco TEXT,
    data_cadastro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    ativo BOOLEAN DEFAULT TRUE,
    INDEX idx_cpf (cpf),
    INDEX idx_nome (nome)
) ENGINE=InnoDB;

-- Tabela de Especialidades
CREATE TABLE especialidades (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(50) NOT NULL UNIQUE,
    descricao TEXT,
    ativo BOOLEAN DEFAULT TRUE
) ENGINE=InnoDB;

-- Tabela de Técnicos
CREATE TABLE tecnicos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    cpf VARCHAR(14) UNIQUE NOT NULL,
    telefone VARCHAR(20) NOT NULL,
    email VARCHAR(100),
    especialidade_id INT NOT NULL,
    data_contratacao DATE NOT NULL,
    ativo BOOLEAN DEFAULT TRUE,
    FOREIGN KEY (especialidade_id) REFERENCES especialidades(id),
    INDEX idx_especialidade (especialidade_id),
    INDEX idx_ativo (ativo)
) ENGINE=InnoDB;

-- Tabela de Serviços
CREATE TABLE servicos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    descricao TEXT,
    duracao_minutos INT NOT NULL,
    preco DECIMAL(10, 2) NOT NULL,
    especialidade_id INT NOT NULL,
    ativo BOOLEAN DEFAULT TRUE,
    FOREIGN KEY (especialidade_id) REFERENCES especialidades(id),
    INDEX idx_especialidade (especialidade_id),
    INDEX idx_ativo (ativo)
) ENGINE=InnoDB;

-- Tabela de Pacotes de Serviços
CREATE TABLE pacotes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    descricao TEXT,
    preco_total DECIMAL(10, 2) NOT NULL,
    desconto_percentual DECIMAL(5, 2) DEFAULT 0,
    validade_dias INT NOT NULL DEFAULT 180,
    ativo BOOLEAN DEFAULT TRUE,
    data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB;

-- Tabela de Serviços incluídos em Pacotes
CREATE TABLE pacotes_servicos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    pacote_id INT NOT NULL,
    servico_id INT NOT NULL,
    quantidade INT DEFAULT 1,
    FOREIGN KEY (pacote_id) REFERENCES pacotes(id) ON DELETE CASCADE,
    FOREIGN KEY (servico_id) REFERENCES servicos(id),
    UNIQUE KEY unique_pacote_servico (pacote_id, servico_id)
) ENGINE=InnoDB;

-- Tabela de Contratação de Pacotes por Clientes
CREATE TABLE clientes_pacotes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    cliente_id INT NOT NULL,
    pacote_id INT NOT NULL,
    data_contratacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    data_validade DATE NOT NULL,
    servicos_utilizados INT DEFAULT 0,
    ativo BOOLEAN DEFAULT TRUE,
    FOREIGN KEY (cliente_id) REFERENCES clientes(id),
    FOREIGN KEY (pacote_id) REFERENCES pacotes(id),
    INDEX idx_cliente (cliente_id),
    INDEX idx_ativo (ativo)
) ENGINE=InnoDB;

-- Tabela de Agendamentos
CREATE TABLE agendamentos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    cliente_id INT NOT NULL,
    tecnico_id INT NOT NULL,
    servico_id INT NOT NULL,
    data_agendamento DATETIME NOT NULL,
    duracao_minutos INT NOT NULL,
    tipo_atendimento ENUM('com_reserva', 'sem_reserva') NOT NULL,
    status ENUM('agendado', 'em_atendimento', 'concluido', 'cancelado', 'nao_compareceu') DEFAULT 'agendado',
    observacoes TEXT,
    data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    cliente_pacote_id INT NULL,
    FOREIGN KEY (cliente_id) REFERENCES clientes(id),
    FOREIGN KEY (tecnico_id) REFERENCES tecnicos(id),
    FOREIGN KEY (servico_id) REFERENCES servicos(id),
    FOREIGN KEY (cliente_pacote_id) REFERENCES clientes_pacotes(id),
    INDEX idx_data_agendamento (data_agendamento),
    INDEX idx_tecnico (tecnico_id),
    INDEX idx_status (status),
    INDEX idx_cliente (cliente_id)
) ENGINE=InnoDB;

-- Tabela de Fila de Espera
CREATE TABLE fila_espera (
    id INT AUTO_INCREMENT PRIMARY KEY,
    cliente_id INT NOT NULL,
    servico_id INT NOT NULL,
    data_solicitacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    data_preferencia DATE NULL,
    prioridade INT DEFAULT 0,
    status ENUM('aguardando', 'notificado', 'agendado', 'cancelado') DEFAULT 'aguardando',
    observacoes TEXT,
    FOREIGN KEY (cliente_id) REFERENCES clientes(id),
    FOREIGN KEY (servico_id) REFERENCES servicos(id),
    INDEX idx_status (status),
    INDEX idx_data_preferencia (data_preferencia)
) ENGINE=InnoDB;

-- Tabela de Pagamentos
CREATE TABLE pagamentos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    agendamento_id INT NULL,
    cliente_pacote_id INT NULL,
    cliente_id INT NOT NULL,
    valor DECIMAL(10, 2) NOT NULL,
    tipo_pagamento ENUM('visa', 'mastercard', 'pix', 'dinheiro') NOT NULL,
    status ENUM('pendente', 'pago', 'cancelado', 'estornado') DEFAULT 'pendente',
    data_pagamento TIMESTAMP NULL,
    data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    descricao TEXT,
    FOREIGN KEY (agendamento_id) REFERENCES agendamentos(id),
    FOREIGN KEY (cliente_pacote_id) REFERENCES clientes_pacotes(id),
    FOREIGN KEY (cliente_id) REFERENCES clientes(id),
    INDEX idx_agendamento (agendamento_id),
    INDEX idx_cliente (cliente_id),
    INDEX idx_status (status)
) ENGINE=InnoDB;

-- Tabela de Penalidades
CREATE TABLE penalidades (
    id INT AUTO_INCREMENT PRIMARY KEY,
    cliente_id INT NOT NULL,
    agendamento_id INT NOT NULL,
    valor_total DECIMAL(10, 2) NOT NULL,
    valor_taxa DECIMAL(10, 2) NOT NULL,
    valor_credito DECIMAL(10, 2) NOT NULL,
    data_aplicacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    utilizado BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (cliente_id) REFERENCES clientes(id),
    FOREIGN KEY (agendamento_id) REFERENCES agendamentos(id),
    INDEX idx_cliente (cliente_id),
    INDEX idx_utilizado (utilizado)
) ENGINE=InnoDB;

-- Tabela de Créditos
CREATE TABLE creditos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    cliente_id INT NOT NULL,
    penalidade_id INT NOT NULL,
    valor DECIMAL(10, 2) NOT NULL,
    saldo DECIMAL(10, 2) NOT NULL,
    data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    data_validade DATE NOT NULL,
    ativo BOOLEAN DEFAULT TRUE,
    FOREIGN KEY (cliente_id) REFERENCES clientes(id),
    FOREIGN KEY (penalidade_id) REFERENCES penalidades(id),
    INDEX idx_cliente (cliente_id),
    INDEX idx_ativo (ativo)
) ENGINE=InnoDB;

-- Inserção de dados iniciais
INSERT INTO especialidades (nome, descricao) VALUES
('Eletrônica Geral', 'Reparos gerais em sistemas eletrônicos automotivos'),
('Injeção Eletrônica', 'Especialista em sistemas de injeção eletrônica'),
('Ar Condicionado', 'Manutenção e reparo de sistemas de climatização'),
('Som e Multimídia', 'Instalação e reparo de sistemas de áudio e multimídia'),
('Alarmes e Travas', 'Instalação e manutenção de sistemas de segurança');

INSERT INTO servicos (nome, descricao, duracao_minutos, preco, especialidade_id) VALUES
('Diagnóstico Eletrônico Completo', 'Análise completa dos sistemas eletrônicos', 60, 150.00, 1),
('Limpeza de Bicos Injetores', 'Limpeza e teste de bicos injetores', 90, 200.00, 2),
('Recarga de Ar Condicionado', 'Recarga de gás e verificação do sistema', 45, 180.00, 3),
('Instalação de Som', 'Instalação de sistema de som automotivo', 120, 250.00, 4),
('Instalação de Alarme', 'Instalação de sistema de alarme completo', 150, 350.00, 5),
('Manutenção Preventiva Eletrônica', 'Revisão geral dos sistemas eletrônicos', 75, 120.00, 1),
('Reparo de Central de Injeção', 'Reparo ou substituição de central', 180, 450.00, 2),
('Higienização de Ar Condicionado', 'Limpeza e higienização completa', 60, 120.00, 3);

INSERT INTO pacotes (nome, descricao, preco_total, desconto_percentual, validade_dias) VALUES
('Pacote Manutenção Básica', 'Inclui diagnóstico e manutenção preventiva', 240.00, 10, 180),
('Pacote Conforto', 'Ar condicionado completo', 270.00, 15, 180),
('Pacote Premium', 'Serviços completos de eletrônica', 900.00, 20, 365);

INSERT INTO pacotes_servicos (pacote_id, servico_id, quantidade) VALUES
(1, 1, 1), (1, 6, 1),
(2, 3, 1), (2, 8, 1),
(3, 1, 1), (3, 2, 1), (3, 3, 1), (3, 6, 1);