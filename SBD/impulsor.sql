--------------------------------------------------
-- CRIAÇÃO DAS TABELAS
--------------------------------------------------
IF OBJECT_ID('pedidos') IS NULL
CREATE TABLE pedidos (
    codigoPedido VARCHAR(20),
    codigoCliente VARCHAR(50),
    valorTotal DECIMAL(10,2),
    status VARCHAR(20)
);

IF OBJECT_ID('compra') IS NULL
CREATE TABLE compra (
    codigoPedido VARCHAR(20),
    SKU VARCHAR(50),
    nomeProduto VARCHAR(100),
    quantidade INT,
    valorUnitario DECIMAL(10,2)
);

IF OBJECT_ID('expedicao') IS NULL
CREATE TABLE expedicao (
    codigoPedido VARCHAR(20)
);

IF OBJECT_ID('estoque') IS NULL
CREATE TABLE estoque (
    SKU VARCHAR(50),
    quantidadeDisponivel INT
);

--------------------------------------------------
-- LIMPEZA
--------------------------------------------------
TRUNCATE TABLE expedicao;
TRUNCATE TABLE compra;
TRUNCATE TABLE pedidos;
TRUNCATE TABLE estoque;

IF OBJECT_ID('tempdb..#tmp_pedidos') IS NOT NULL DROP TABLE #tmp_pedidos;
IF OBJECT_ID('tempdb..#Totais') IS NOT NULL DROP TABLE #Totais;
IF OBJECT_ID('tempdb..#Fila') IS NOT NULL DROP TABLE #Fila;

--------------------------------------------------
-- TABELA TEMP
--------------------------------------------------
CREATE TABLE #tmp_pedidos (
    codigoPedido VARCHAR(20),
    dataPedido DATE,
    SKU VARCHAR(50),
    UPC VARCHAR(50),
    nomeProduto VARCHAR(100),
    qtd INT,
    valor VARCHAR(20),   
    frete VARCHAR(20),   
    email VARCHAR(100),
    codigoComprador VARCHAR(50),
    nomeComprador VARCHAR(100),
    endereco VARCHAR(100),
    CEP VARCHAR(20),
    UF VARCHAR(10),
    pais VARCHAR(50)
);

--------------------------------------------------
-- IMPORTAÇÃO
--------------------------------------------------
BULK INSERT #tmp_pedidos
FROM 'C:\temp\pedidos.txt'
WITH (
    FIRSTROW = 2,
    FIELDTERMINATOR = ';',
    ROWTERMINATOR = '0x0a',
    CODEPAGE = '65001'
);

--------------------------------------------------
-- TOTAL DOS PEDIDOS
--------------------------------------------------
SELECT
    codigoPedido,
    SUM(CAST(REPLACE(valor, ',', '.') AS DECIMAL(10,2)) * qtd)
    + MAX(CAST(REPLACE(frete, ',', '.') AS DECIMAL(10,2))) AS valor_total
INTO #Totais
FROM #tmp_pedidos
GROUP BY codigoPedido;

--------------------------------------------------
-- FILA (MAIOR VALOR PRIMEIRO)
--------------------------------------------------
SELECT
    codigoPedido,
    valor_total,
    ROW_NUMBER() OVER (ORDER BY valor_total DESC) AS ordem
INTO #Fila
FROM #Totais;

--------------------------------------------------
-- PEDIDOS
--------------------------------------------------
INSERT INTO pedidos (codigoPedido, codigoCliente, valorTotal, status)
SELECT
    p.codigoPedido,
    MAX(p.codigoComprador),
    t.valor_total,
    'Pendente'
FROM #tmp_pedidos p
JOIN #Totais t ON t.codigoPedido = p.codigoPedido
GROUP BY p.codigoPedido, t.valor_total;

--------------------------------------------------
-- ITENS
--------------------------------------------------
INSERT INTO compra (codigoPedido, SKU, nomeProduto, quantidade, valorUnitario)
SELECT
    codigoPedido,
    SKU,
    nomeProduto,
    qtd,
    CAST(REPLACE(valor, ',', '.') AS DECIMAL(10,2))
FROM #tmp_pedidos;

--------------------------------------------------
-- ESTOQUE (EXEMPLO)
--------------------------------------------------
INSERT INTO estoque (SKU, quantidadeDisponivel)
SELECT SKU, SUM(qtd) * 2
FROM #tmp_pedidos
GROUP BY SKU;

--------------------------------------------------
-- CURSOR (REGRA DE NEGÓCIO)
--------------------------------------------------
DECLARE @codigoPedido VARCHAR(20);

DECLARE cursor_pedidos CURSOR FOR
SELECT codigoPedido
FROM #Fila
ORDER BY ordem;

OPEN cursor_pedidos;
FETCH NEXT FROM cursor_pedidos INTO @codigoPedido;

WHILE @@FETCH_STATUS = 0
BEGIN
    -- Verifica se o pedido está completo
    IF NOT EXISTS (
        SELECT 1
        FROM compra c
        JOIN estoque e ON e.SKU = c.SKU
        WHERE c.codigoPedido = @codigoPedido
        AND c.quantidade > e.quantidadeDisponivel
    )
    BEGIN
        -- Atualiza status para ATENDIDO
        UPDATE pedidos
        SET status = 'Atendido'
        WHERE codigoPedido = @codigoPedido;

        -- Insere na expedição
        INSERT INTO expedicao (codigoPedido)
        VALUES (@codigoPedido);

        -- Debita estoque
        UPDATE e
        SET e.quantidadeDisponivel = e.quantidadeDisponivel - c.quantidade
        FROM estoque e
        JOIN compra c ON c.SKU = e.SKU
        WHERE c.codigoPedido = @codigoPedido;
    END

    FETCH NEXT FROM cursor_pedidos INTO @codigoPedido;
END

CLOSE cursor_pedidos;
DEALLOCATE cursor_pedidos;

--------------------------------------------------
-- RESULTADOS
--------------------------------------------------
SELECT * FROM pedidos;
SELECT * FROM expedicao;
SELECT * FROM estoque;
SELECT * FROM #Fila ORDER BY ordem;