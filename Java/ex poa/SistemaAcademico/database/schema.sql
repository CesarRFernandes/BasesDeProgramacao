-- Criar banco de dados
CREATE DATABASE IF NOT EXISTS sistema_academico CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE sistema_academico;

-- Tabela de Alunos
CREATE TABLE alunos (
    id INT PRIMARY KEY AUTO_INCREMENT,
    nome VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    senha VARCHAR(255) NOT NULL,
    ra VARCHAR(20) UNIQUE NOT NULL,
    curso VARCHAR(100) DEFAULT 'Análise e Desenvolvimento de Sistemas',
    periodo_atual INT DEFAULT 1,
    cep VARCHAR(9),
    endereco VARCHAR(255),
    cidade VARCHAR(100),
    estado VARCHAR(2),
    data_cadastro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabela de Disciplinas (Pré-cadastradas com cargas horárias)
CREATE TABLE disciplinas (
    id INT PRIMARY KEY AUTO_INCREMENT,
    codigo VARCHAR(10) UNIQUE NOT NULL,
    nome VARCHAR(100) NOT NULL,
    carga_horaria INT NOT NULL,
    periodo INT NOT NULL
);

-- Tabela de Notas
CREATE TABLE notas (
    id INT PRIMARY KEY AUTO_INCREMENT,
    aluno_id INT NOT NULL,
    disciplina_id INT NOT NULL,
    nota DECIMAL(4,2) NOT NULL CHECK (nota >= 0 AND nota <= 10),
    semestre VARCHAR(10) NOT NULL,
    ano INT NOT NULL,
    data_lancamento TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (aluno_id) REFERENCES alunos(id) ON DELETE CASCADE,
    FOREIGN KEY (disciplina_id) REFERENCES disciplinas(id) ON DELETE CASCADE,
    UNIQUE KEY unique_nota (aluno_id, disciplina_id, semestre, ano)
);

-- Tabela de Atividades Complementares
CREATE TABLE atividades_complementares (
    id INT PRIMARY KEY AUTO_INCREMENT,
    aluno_id INT NOT NULL,
    tipo VARCHAR(50) NOT NULL,
    descricao VARCHAR(255) NOT NULL,
    horas INT NOT NULL CHECK (horas > 0),
    data_realizacao DATE NOT NULL,
    certificado VARCHAR(255),
    data_cadastro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (aluno_id) REFERENCES alunos(id) ON DELETE CASCADE
);

-- Inserir disciplinas pré-cadastradas
INSERT INTO disciplinas (codigo, nome, carga_horaria, periodo) VALUES
-- 1º Período
('1ORG', 'Organização de Computadores', 80, 1),
('1MAC', 'Matemática para Computação', 80, 1),
('1FAC', 'Fundamentos de Algoritmos de Computação', 80, 1),
('1MAB', 'Matemática Básica', 80, 1),
('1IAS', 'Introdução à Análise de Sistemas', 80, 1),
('1LPO', 'Língua Portuguesa', 80, 1),
('1IHM', 'Interface Homem-Máquina', 40, 1),

-- 2º Período
('2TPH', 'Técnicas e Paradigmas Humanos', 80, 2),
('2REQ', 'Engenharia de Requisitos', 80, 2),
('2CAW', 'Construção de Aplicações Web', 80, 2),
('2FPR', 'Fundamentos de Programação', 80, 2),
('2LES', 'Língua Estrangeira', 40, 2),
('2MPA', 'Métodos e Processos Administrativos', 40, 2),
('2SOP', 'Fundamentos de Sistemas Operacionais', 80, 2),
('2CAL', 'Cálculo', 80, 2),

-- 3º Período
('3POB', 'Programação Orientada a Objetos Básica', 80, 3),
('3PBD', 'Projeto de Banco de Dados', 80, 3),
('3DAW', 'Desenvolvimento de Tecnologias Web', 80, 3),
('3ALG', 'Álgebra', 80, 3),
('3ESD', 'Estrutura de Dados', 80, 3),
('3RSD', 'Fundamentos de Redes e Sistemas Distribuídos', 80, 3),

-- 4º Período
('4POA', 'Programação Orientada a Objetos Avançada', 80, 4),
('4UBD', 'Utilização de Banco de Dados e SQL', 80, 4),
('4MOD', 'Modelagem de Sistemas', 80, 4),
('4SEG', 'Segurança da Informação', 80, 4),
('4EST', 'Estatística e Probabilidade', 80, 4),
('4ADS', 'Tópicos em Análise e Desenvolvimento de Sistemas', 80, 4),
('4MET', 'Metodologia da Pesquisa', 40, 4),
('4EMP', 'Empreendedorismo e Inovação', 40, 4),

-- 5º Período
('5SBD', 'Programação de Scripts de Banco de Dados e SQL', 80, 5),
('5PJS', 'Projeto de Sistemas', 80, 5),
('5PDM', 'Programação de Dispositivos Móveis', 80, 5),
('5GPS', 'Gerência e Projeto de Sistemas', 40, 5),
('5TAV', 'Tópicos Avançados', 80, 5);

-- Inserir aluno de exemplo (senha: 123456)
INSERT INTO alunos (nome, email, senha, ra, periodo_atual, cep, endereco, cidade, estado) 
VALUES ('João Silva', 'joao@email.com', '123456', '2024001', 3, '01310-100', 'Av. Paulista, 1578', 'São Paulo', 'SP');

-- Inserir notas de exemplo para o aluno
INSERT INTO notas (aluno_id, disciplina_id, nota, semestre, ano) VALUES
(1, 1, 8.5, '1', 2024),
(1, 2, 7.0, '1', 2024),
(1, 3, 9.0, '1', 2024),
(1, 4, 6.5, '1', 2024),
(1, 5, 8.0, '1', 2024),
(1, 6, 7.5, '1', 2024),
(1, 7, 9.5, '1', 2024),
(1, 8, 8.0, '2', 2024),
(1, 9, 7.5, '2', 2024),
(1, 10, 8.5, '2', 2024);

-- Inserir atividades complementares de exemplo
INSERT INTO atividades_complementares (aluno_id, tipo, descricao, horas, data_realizacao) VALUES
(1, 'Curso', 'Curso de Java Avançado', 40, '2024-03-15'),
(1, 'Palestra', 'Palestra sobre DevOps', 4, '2024-04-20'),
(1, 'Workshop', 'Workshop de Cloud Computing', 8, '2024-05-10');

-- Criar views úteis
CREATE VIEW view_cr_alunos AS
SELECT 
    a.id,
    a.nome,
    a.ra,
    ROUND(SUM(n.nota * d.carga_horaria) / SUM(d.carga_horaria), 2) AS cr,
    COUNT(DISTINCT n.disciplina_id) AS disciplinas_cursadas,
    SUM(d.carga_horaria) AS total_horas_cursadas
FROM alunos a
LEFT JOIN notas n ON a.id = n.aluno_id
LEFT JOIN disciplinas d ON n.disciplina_id = d.id
GROUP BY a.id, a.nome, a.ra;

CREATE VIEW view_horas_complementares AS
SELECT 
    a.id,
    a.nome,
    a.ra,
    COALESCE(SUM(ac.horas), 0) AS horas_cumpridas,
    200 AS horas_obrigatorias,
    200 - COALESCE(SUM(ac.horas), 0) AS horas_faltantes
FROM alunos a
LEFT JOIN atividades_complementares ac ON a.id = ac.aluno_id
GROUP BY a.id, a.nome, a.ra;