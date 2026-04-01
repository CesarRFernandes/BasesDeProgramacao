-- CRIAR TABELAS 
IF OBJECT_ID('pedidos') IS NULL
CREATE TABLE pedidos (
    codigoPedido VARCHAR(20),
    codigoCliente VARCHAR(50),
    valorTotal DECIMAL(10,2)
);

IF OBJECT_ID('compra') IS NULL
CREATE TABLE compra (
    codigoPedido VARCHAR(20),
    SKU VARCHAR(50),
    quantidade INT,
    valorUnitario DECIMAL(10,2)
);

IF OBJECT_ID('expedicao') IS NULL
CREATE TABLE expedicao (
    codigoPedido VARCHAR(20)
);



-- LIMPEZA DAS TEMPORÁRIAS (CASO EXISTA)
IF OBJECT_ID('tempdb..#tmp_pedidos') IS NOT NULL DROP TABLE #tmp_pedidos;
IF OBJECT_ID('tempdb..#Totais') IS NOT NULL DROP TABLE #Totais;
IF OBJECT_ID('tempdb..#Fila') IS NOT NULL DROP TABLE #Fila;



-- Tabela temporária
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



--Inserindo do txt
BULK INSERT #tmp_pedidos
FROM 'C:\temp\pedidos.txt'
WITH (
    FIRSTROW = 2,
    FIELDTERMINATOR = ';',
    ROWTERMINATOR = '0x0a',
    CODEPAGE = '65001'
);



-- Verificacao
SELECT COUNT(*) AS total_importado FROM #tmp_pedidos;


-- Caluclar total pedido
SELECT
    codigoPedido,
    SUM(CAST(REPLACE(valor, ',', '.') AS DECIMAL(10,2)) * qtd)
    + MAX(CAST(REPLACE(frete, ',', '.') AS DECIMAL(10,2))) AS valor_total
INTO #Totais
FROM #tmp_pedidos
GROUP BY codigoPedido;


-- Regra de negocio: maior valor primeiro, criando fila
SELECT
    codigoPedido,
    valor_total,
    ROW_NUMBER() OVER (ORDER BY valor_total DESC) AS ordem
INTO #Fila
FROM #Totais;


-- Atualizando tabela pedidos
INSERT INTO pedidos (codigoPedido, codigoCliente, valorTotal)
SELECT
    p.codigoPedido,
    MAX(p.codigoComprador),
    t.valor_total
FROM #tmp_pedidos p
JOIN #Totais t ON t.codigoPedido = p.codigoPedido
GROUP BY p.codigoPedido, t.valor_total;


-- Atualizando tabela de compra com os pedidos
INSERT INTO compra (codigoPedido, SKU, quantidade, valorUnitario)
SELECT
    codigoPedido,
    SKU,
    qtd,
    CAST(REPLACE(valor, ',', '.') AS DECIMAL(10,2))
FROM #tmp_pedidos;


-- Pedidos semdp inseridos na ordem da fila
INSERT INTO expedicao (codigoPedido)
SELECT codigoPedido
FROM #Fila
ORDER BY ordem;


-- Resultado
SELECT * FROM #Fila ORDER BY ordem;
