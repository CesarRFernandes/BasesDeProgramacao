-- 1: LIMPEZA
IF OBJECT_ID('movimentacao')  IS NOT NULL DROP TABLE movimentacao;
IF OBJECT_ID('compra')        IS NOT NULL DROP TABLE compra;
IF OBJECT_ID('itensPedido')   IS NOT NULL DROP TABLE itensPedido;
IF OBJECT_ID('pedidos')       IS NOT NULL DROP TABLE pedidos;
IF OBJECT_ID('produtos')      IS NOT NULL DROP TABLE produtos;
IF OBJECT_ID('clientes')      IS NOT NULL DROP TABLE clientes;
 

-- 2: CRIAÇÃO DAS TABELAS PRINCIPAIS 
CREATE TABLE clientes (
    codigoCliente VARCHAR(50)  PRIMARY KEY,
    nome          VARCHAR(100),
    email         VARCHAR(100),
    cpf           VARCHAR(20),
    telefone      VARCHAR(20)
);
 
CREATE TABLE produtos (
    SKU         VARCHAR(50)  PRIMARY KEY,
    nomeProduto VARCHAR(150),
    estoque     INT DEFAULT 0
);
 
CREATE TABLE pedidos (
    codigoPedido  VARCHAR(50)    PRIMARY KEY,
    codigoCliente VARCHAR(50),
    valorTotal    DECIMAL(10,2),
    status        VARCHAR(30)
);
 
CREATE TABLE itensPedido (
    id            INT IDENTITY PRIMARY KEY,
    codigoPedido  VARCHAR(50),
    SKU           VARCHAR(50),
    quantidade    INT,
    valorUnitario DECIMAL(10,2)
);
 
CREATE TABLE compra (
    id          INT IDENTITY PRIMARY KEY,
    SKU         VARCHAR(50),
    nomeProduto VARCHAR(150),
    quantidade  INT
);
 
CREATE TABLE movimentacao (
    id           INT IDENTITY PRIMARY KEY,
    codigoPedido VARCHAR(50),
    SKU          VARCHAR(50),
    quantidade   INT,
    dataMov      DATETIME DEFAULT GETDATE()
);
 
 
-- 3: RELACIONAMENTOS (FOREIGN KEYS)
ALTER TABLE pedidos
    ADD FOREIGN KEY (codigoCliente) REFERENCES clientes(codigoCliente);
 
ALTER TABLE itensPedido
    ADD FOREIGN KEY (codigoPedido)  REFERENCES pedidos(codigoPedido);
 
ALTER TABLE itensPedido
    ADD FOREIGN KEY (SKU)           REFERENCES produtos(SKU);
 
 
-- 4: TABELA TEMPORÁRIA PARA IMPORTAÇÃO DO CSV PRINCIPAL
IF OBJECT_ID('tempdb..#tmp_pedidos') IS NOT NULL DROP TABLE #tmp_pedidos;
 
CREATE TABLE #tmp_pedidos (
    order_id            VARCHAR(50),
    order_item_id       VARCHAR(50),
    purchase_date       VARCHAR(30),   
    payments_date       VARCHAR(30),
    buyer_email         VARCHAR(100),
    buyer_name          VARCHAR(100),
    cpf                 VARCHAR(14),
    buyer_phone_number  VARCHAR(30),
    sku                 VARCHAR(50),
    upc                 VARCHAR(50),
    product_name        VARCHAR(150),
    quantity_purchased  VARCHAR(10),   
    currency            VARCHAR(10),
    item_price          VARCHAR(20),   
    ship_service_level  VARCHAR(50),
    ship_address_1      VARCHAR(150),
    ship_address_2      VARCHAR(150),
    ship_address_3      VARCHAR(150),
    ship_city           VARCHAR(100),
    ship_state          VARCHAR(50),
    ship_postal_code    VARCHAR(20),
    ship_country        VARCHAR(50)
);
 
 

-- 5: IMPORTAÇÃO DO CSV PRINCIPAL (BULK INSERT) 
BULK INSERT #tmp_pedidos
FROM 'C:\temp\TESTE.csv'
WITH (
    FIRSTROW      = 2,        
    FIELDTERMINATOR = ',',
    ROWTERMINATOR   = '0x0a',
    CODEPAGE        = '65001' 
);
 

-- 6: TRATAMENTO E NORMALIZAÇÃO DOS DADOS 
IF OBJECT_ID('tempdb..#dados') IS NOT NULL DROP TABLE #dados;
 
SELECT
    order_id,
    buyer_name,
    buyer_email,
    cpf,
    buyer_phone_number,
    sku,
    product_name,
    TRY_CAST(quantity_purchased AS INT) AS quantity_purchased,
 
    TRY_CAST(
        CASE
            WHEN CHARINDEX(',', item_price) > CHARINDEX('.', item_price)
                 AND CHARINDEX('.', item_price) > 0
                THEN REPLACE(REPLACE(LTRIM(RTRIM(item_price)), '.', ''), ',', '.')
 
            WHEN CHARINDEX('.', item_price) > CHARINDEX(',', item_price)
                 AND CHARINDEX(',', item_price) > 0
                THEN REPLACE(LTRIM(RTRIM(item_price)), ',', '')
            WHEN CHARINDEX(',', item_price) > 0
                 AND CHARINDEX('.', item_price) = 0
                THEN REPLACE(LTRIM(RTRIM(item_price)), ',', '.')
            ELSE LTRIM(RTRIM(item_price))
        END
    AS DECIMAL(10,2)) AS item_price
 
INTO #dados
FROM #tmp_pedidos
WHERE LTRIM(RTRIM(ISNULL(order_id, ''))) <> ''; 
 
 
-- 7: CARGA DE CLIENTES
INSERT INTO clientes (codigoCliente, nome, email, cpf, telefone)
SELECT DISTINCT
    cpf,
    buyer_name,
    buyer_email,
    cpf,
    buyer_phone_number
FROM #dados d
WHERE NOT EXISTS (
    SELECT 1 FROM clientes c WHERE c.codigoCliente = d.cpf
);
 
 
-- 8: CARGA DE PRODUTOS
INSERT INTO produtos (SKU, nomeProduto, estoque)
SELECT DISTINCT
    sku,
    product_name,
    0
FROM #dados d
WHERE NOT EXISTS (
    SELECT 1 FROM produtos p WHERE p.SKU = d.sku
);
 
 
-- 9: CARGA DE PEDIDOS (CABEÇALHO) 
IF OBJECT_ID('tempdb..#Totais') IS NOT NULL DROP TABLE #Totais;
 
SELECT
    order_id,
    SUM(item_price * quantity_purchased) AS total
INTO #Totais
FROM #dados
GROUP BY order_id;
 
INSERT INTO pedidos (codigoPedido, codigoCliente, valorTotal, status)
SELECT
    t.order_id,
    MIN(d.cpf),  
    t.total,
    'PENDENTE'
FROM #dados d
JOIN #Totais t ON t.order_id = d.order_id
GROUP BY t.order_id, t.total;
 
 
-- 10: CARGA DOS ITENS DO PEDIDO
INSERT INTO itensPedido (codigoPedido, SKU, quantidade, valorUnitario)
SELECT
    order_id,
    sku,
    quantity_purchased,
    item_price
FROM #dados;
 
 
-- 11: PROCESSAMENTO DOS PEDIDOS (CURSOR) 
DECLARE @pedido VARCHAR(50);
 
DECLARE cursorPedidos CURSOR FOR
    SELECT codigoPedido FROM pedidos ORDER BY valorTotal DESC;
 
OPEN cursorPedidos;
FETCH NEXT FROM cursorPedidos INTO @pedido;
 
WHILE @@FETCH_STATUS = 0
BEGIN
    DECLARE @pode BIT = 1;
 
    IF EXISTS (
        SELECT 1
        FROM itensPedido i
        JOIN produtos p ON p.SKU = i.SKU
        WHERE i.codigoPedido = @pedido
          AND p.estoque < i.quantidade
    )
        SET @pode = 0;
 
    IF @pode = 1
    BEGIN
        INSERT INTO movimentacao (codigoPedido, SKU, quantidade, dataMov)
            SELECT codigoPedido, SKU, quantidade, GETDATE()
            FROM itensPedido
            WHERE codigoPedido = @pedido;
 
        UPDATE p
        SET p.estoque = p.estoque - i.quantidade
        FROM produtos p
        JOIN itensPedido i ON i.SKU = p.SKU
        WHERE i.codigoPedido = @pedido;
 
        UPDATE pedidos SET status = 'ATENDIDO' WHERE codigoPedido = @pedido;
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
    END
 
    FETCH NEXT FROM cursorPedidos INTO @pedido;
END
 
CLOSE    cursorPedidos;
DEALLOCATE cursorPedidos;
 
 
-- 12: REPOSIÇÃO DE ESTOQUE (CSV DO FORNECEDOR) 
IF OBJECT_ID('tempdb..#tmp_entrada') IS NOT NULL DROP TABLE #tmp_entrada;
 
CREATE TABLE #tmp_entrada (
    SKU          VARCHAR(50),
    QTD_ENTREGUE VARCHAR(20)   
);
 
BULK INSERT #tmp_entrada
FROM 'C:\temp\TESTE_FORNECEDOR.csv'
WITH (
    FIRSTROW        = 2,
    FIELDTERMINATOR = ',',
    ROWTERMINATOR   = '0x0a',
    CODEPAGE        = '65001'
);
 
UPDATE p
SET p.estoque = p.estoque + TRY_CAST(
    CASE
        WHEN CHARINDEX(',', e.QTD_ENTREGUE) > CHARINDEX('.', e.QTD_ENTREGUE)
             AND CHARINDEX('.', e.QTD_ENTREGUE) > 0
            THEN REPLACE(REPLACE(LTRIM(RTRIM(e.QTD_ENTREGUE)), '.', ''), ',', '.')
        WHEN CHARINDEX('.', e.QTD_ENTREGUE) > CHARINDEX(',', e.QTD_ENTREGUE)
             AND CHARINDEX(',', e.QTD_ENTREGUE) > 0
            THEN REPLACE(LTRIM(RTRIM(e.QTD_ENTREGUE)), ',', '')
        WHEN CHARINDEX(',', e.QTD_ENTREGUE) > 0
             AND CHARINDEX('.', e.QTD_ENTREGUE) = 0
            THEN REPLACE(LTRIM(RTRIM(e.QTD_ENTREGUE)), ',', '.')
        ELSE LTRIM(RTRIM(e.QTD_ENTREGUE))
    END
AS INT)
FROM produtos p
JOIN #tmp_entrada e ON e.SKU = p.SKU;
 

-- 13: REPROCESSAMENTO DOS PEDIDOS PENDENTES
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
        INSERT INTO movimentacao (codigoPedido, SKU, quantidade, dataMov)
            SELECT codigoPedido, SKU, quantidade, GETDATE()
            FROM itensPedido
            WHERE codigoPedido = @pedido;
 
        UPDATE p
        SET p.estoque = p.estoque - i.quantidade
        FROM produtos p
        JOIN itensPedido i ON i.SKU = p.SKU
        WHERE i.codigoPedido = @pedido;
 
        UPDATE pedidos SET status = 'ATENDIDO' WHERE codigoPedido = @pedido;
    END
 
    FETCH NEXT FROM cursorPendentes INTO @pedido;
END
 
CLOSE    cursorPendentes;
DEALLOCATE cursorPendentes;
 

-- 14: CONSULTAS DE RESULTADO 
SELECT * FROM pedidos;
SELECT * FROM itensPedido;
SELECT * FROM produtos;
SELECT * FROM compra;
SELECT * FROM movimentacao;
SELECT * FROM #tmp_pedidos;
