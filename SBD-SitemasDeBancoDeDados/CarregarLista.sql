-- Tabela temporária
CREATE TABLE #tmp_pedidos (
    codigoPedido VARCHAR(20),
    dataPedido VARCHAR (100),
    SKU VARCHAR(50),
    UPC VARCHAR (100),
    nomeProduto VARCHAR(100),
    qtd VARCHAR (100),
    valor DECIMAL(10,2),
    frete DECIMAL(10,2),
    email VARCHAR (100),
    codigoComprador VARCHAR (50),
    nomeComprador VARCHAR (100),
    endereco VARCHAR (100),
    CEP VARCHAR (100),
    UF VARCHAR (100),
    pais VARCHAR (100)
);


--Inserindo do txt
BULK INSERT #tmp_pedidos
FROM 'C:\Users\Crf15\Downloads\pedidos.txt'
WITH (
    FIRSTROW = 2,
    FIELDTERMINATOR = ':',
    ROWTERMINATOR = '\n',
    CODEPAGE = '65001'
    );


-- Caluclar total pedido
SELECT
    codigoPedido,
    SUM(valor * qtd) + MAX(frete) AS valor_total
INTO #Totais
FROM #tmp_pedidos
GROUP BY codigoPedido;


-- Regra de negocio: maior valor primeiro, criando fila
SELECT
    codigoPedido,
    valor_total
INTO #Fila
FROM #Totais
ORDER BY valor_total DESC;


-- Atualizando tabela pedidos
INSERT INTO pedidos (codigoPedido, codigoCliente, valorTotal)
SELECT
    p.codigoPedido,
    MAX(p.codigoComprador),
    t.valor_total
FROM #tmp-pedidos p
JOIN #Totais t ON t.codigoPedido = p.codigoPedido
GROUP BY p.codigoPedido, t.valor_total;


-- Atualizando tabela de compra com os pedidos
INSERT INTO compra (codigoPedido, SKU, quantidade, valorUnitario)
SELECT
    codigoPedido,
    SKU,
    qtd,
    valor
FROM #tmp-pedidos;


-- Pedidos semdp inseridos na ordem da fila
INSERT INTO expedicao (codigoPedido)
SELECT codigoPedido
FROM #Fila;
