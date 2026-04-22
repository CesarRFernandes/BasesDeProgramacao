/* 1. LIMPAR E CRIAR TABELAS */

IF OBJECT_ID('movimentacao') IS NOT NULL DROP TABLE movimentacao;
IF OBJECT_ID('compra') IS NOT NULL DROP TABLE compra;
IF OBJECT_ID('itensPedido') IS NOT NULL DROP TABLE itensPedido;
IF OBJECT_ID('pedidos') IS NOT NULL DROP TABLE pedidos;
IF OBJECT_ID('produtos') IS NOT NULL DROP TABLE produtos;
IF OBJECT_ID('clientes') IS NOT NULL DROP TABLE clientes;

CREATE TABLE clientes (
    codigoCliente VARCHAR(50) PRIMARY KEY,
    nome VARCHAR(100),
    email VARCHAR(100),
    cpf VARCHAR(20),
    telefone VARCHAR(20)
);

CREATE TABLE produtos (
    SKU VARCHAR(50) PRIMARY KEY,
    nomeProduto VARCHAR(100),
    estoque INT DEFAULT 0
);

CREATE TABLE pedidos (
    codigoPedido VARCHAR(20) PRIMARY KEY,
    codigoCliente VARCHAR(50),
    valorTotal DECIMAL(10,2),
    status VARCHAR(30)
);

CREATE TABLE itensPedido (
    id INT IDENTITY(1,1) PRIMARY KEY,
    codigoPedido VARCHAR(20),
    SKU VARCHAR(50),
    quantidade INT,
    valorUnitario DECIMAL(10,2)
);

CREATE TABLE compra (
    id INT IDENTITY(1,1) PRIMARY KEY,
    SKU VARCHAR(50),
    nomeProduto VARCHAR(100),
    quantidade INT
);

CREATE TABLE movimentacao (
    id INT IDENTITY(1,1) PRIMARY KEY,
    codigoPedido VARCHAR(20),
    SKU VARCHAR(50),
    quantidade INT,
    dataMov DATETIME DEFAULT GETDATE()
);

/* 2. CHAVES ESTRANGEIRAS */

ALTER TABLE pedidos
ADD CONSTRAINT FK_pedido_cliente
FOREIGN KEY (codigoCliente) REFERENCES clientes(codigoCliente);

ALTER TABLE itensPedido
ADD CONSTRAINT FK_item_pedido
FOREIGN KEY (codigoPedido) REFERENCES pedidos(codigoPedido);

ALTER TABLE itensPedido
ADD CONSTRAINT FK_item_produto
FOREIGN KEY (SKU) REFERENCES produtos(SKU);

/* 3. TABELA TEMPORÁRIA */

IF OBJECT_ID('tempdb..#tmp_pedidos') IS NOT NULL DROP TABLE #tmp_pedidos;

CREATE TABLE #tmp_pedidos (
    codigoPedido VARCHAR(20),
    codigoItem VARCHAR(20),
    dataPedido DATE,
    dataPagamento DATE,
    email VARCHAR(100),
    nomeComprador VARCHAR(100),
    cpf VARCHAR(20),
    telefone VARCHAR(20),
    SKU VARCHAR(50),
    nomeProduto VARCHAR(100),
    qtd INT,
    valor DECIMAL(10,2)
);

/* IMPORTAR CSV */
BULK INSERT #tmp_pedidos
FROM 'C:\temp\pedidos.txt'
WITH (
    FIRSTROW = 2,
    FIELDTERMINATOR = ';',
    ROWTERMINATOR = '0x0a',
    CODEPAGE = '65001'
);

/* 4. CLIENTES (SEM DUPLICAR) */

INSERT INTO clientes (codigoCliente, nome, email, cpf, telefone)
SELECT DISTINCT
    t.cpf,
    t.nomeComprador,
    t.email,
    t.cpf,
    t.telefone
FROM #tmp_pedidos t
WHERE NOT EXISTS (
    SELECT 1 FROM clientes c WHERE c.codigoCliente = t.cpf
);

/* 5. PRODUTOS (SEM DUPLICAR) */

INSERT INTO produtos (SKU, nomeProduto, estoque)
SELECT DISTINCT
    t.SKU,
    t.nomeProduto,
    0
FROM #tmp_pedidos t
WHERE NOT EXISTS (
    SELECT 1 FROM produtos p WHERE p.SKU = t.SKU
);

/* 6. PEDIDOS (VALOR TOTAL) */

IF OBJECT_ID('tempdb..#Totais') IS NOT NULL DROP TABLE #Totais;

SELECT
    codigoPedido,
    SUM(valor * qtd) AS total
INTO #Totais
FROM #tmp_pedidos
GROUP BY codigoPedido;

INSERT INTO pedidos
SELECT
    t.codigoPedido,
    MAX(p.cpf),
    t.total,
    'PENDENTE'
FROM #tmp_pedidos p
JOIN #Totais t ON t.codigoPedido = p.codigoPedido
GROUP BY t.codigoPedido, t.total;

/* 7. ITENS DO PEDIDO */

INSERT INTO itensPedido (codigoPedido, SKU, quantidade, valorUnitario)
SELECT
    codigoPedido,
    SKU,
    qtd,
    valor
FROM #tmp_pedidos;

/* 8. PROCESSAMENTO (MAIOR VALOR)*/

DECLARE @pedido VARCHAR(20);

DECLARE cursorPedidos CURSOR FOR
SELECT codigoPedido FROM pedidos ORDER BY valorTotal DESC;

OPEN cursorPedidos;
FETCH NEXT FROM cursorPedidos INTO @pedido;

WHILE @@FETCH_STATUS = 0
BEGIN
    DECLARE @podeAtender BIT = 1;

    -- verificar estoque
    IF EXISTS (
        SELECT 1
        FROM itensPedido i
        JOIN produtos p ON p.SKU = i.SKU
        WHERE i.codigoPedido = @pedido
        AND p.estoque < i.quantidade
    )
        SET @podeAtender = 0;

    IF @podeAtender = 1
    BEGIN
        INSERT INTO movimentacao (codigoPedido, SKU, quantidade)
        SELECT codigoPedido, SKU, quantidade
        FROM itensPedido
        WHERE codigoPedido = @pedido;

        UPDATE p
        SET p.estoque = p.estoque - i.quantidade
        FROM produtos p
        JOIN itensPedido i ON i.SKU = p.SKU
        WHERE i.codigoPedido = @pedido;

        UPDATE pedidos
        SET status = 'ATENDIDO'
        WHERE codigoPedido = @pedido;
    END
    ELSE
    BEGIN
        INSERT INTO compra (SKU, nomeProduto, quantidade)
        SELECT 
            i.SKU,
            p.nomeProduto,
            (i.quantidade - p.estoque)
        FROM itensPedido i
        JOIN produtos p ON p.SKU = i.SKU
        WHERE i.codigoPedido = @pedido
        AND p.estoque < i.quantidade;

        UPDATE pedidos
        SET status = 'PENDENTE'
        WHERE codigoPedido = @pedido;
    END

    FETCH NEXT FROM cursorPedidos INTO @pedido;
END

CLOSE cursorPedidos;
DEALLOCATE cursorPedidos;

/*  9. REPOSIÇÃO (CSV 2) */

IF OBJECT_ID('tempdb..#tmp_entrada') IS NOT NULL DROP TABLE #tmp_entrada;

CREATE TABLE #tmp_entrada (
    SKU VARCHAR(50),
    quantidade INT
);

BULK INSERT #tmp_entrada
FROM 'C:\temp\entrada.txt'
WITH (
    FIRSTROW = 2,
    FIELDTERMINATOR = ';',
    ROWTERMINATOR = '0x0a'
);

UPDATE p
SET p.estoque = p.estoque + e.quantidade
FROM produtos p
JOIN #tmp_entrada e ON e.SKU = p.SKU;

/* 10. REPROCESSAR PENDENTES */

DECLARE cursorPendentes CURSOR FOR
SELECT codigoPedido FROM pedidos WHERE status = 'PENDENTE';

OPEN cursorPendentes;
FETCH NEXT FROM cursorPendentes INTO @pedido;

WHILE @@FETCH_STATUS = 0
BEGIN
    IF NOT EXISTS (
        SELECT 1
        FROM itensPedido i
        JOIN produtos p ON p.SKU = i.SKU
        WHERE i.codigoPedido = @pedido
        AND p.estoque < i.quantidade
    )
    BEGIN
        INSERT INTO movimentacao (codigoPedido, SKU, quantidade)
        SELECT codigoPedido, SKU, quantidade
        FROM itensPedido
        WHERE codigoPedido = @pedido;

        UPDATE p
        SET p.estoque = p.estoque - i.quantidade
        FROM produtos p
        JOIN itensPedido i ON i.SKU = p.SKU
        WHERE i.codigoPedido = @pedido;

        UPDATE pedidos
        SET status = 'ATENDIDO'
        WHERE codigoPedido = @pedido;
    END

    FETCH NEXT FROM cursorPendentes INTO @pedido;
END

CLOSE cursorPendentes;
DEALLOCATE cursorPendentes;

/* 11. RESULTADO FINAL */

SELECT * FROM pedidos;
SELECT * FROM itensPedido;
SELECT * FROM produtos;
SELECT * FROM compra;
SELECT * FROM movimentacao;
