-- Tabela temporária
CREATE TABLE #tmp_pedidos (
    codigoPedido VARCHAR(20),
    dataPedido DATE,
    SKU VARCHAR(50),
    nomeProduto VARCHAR(100),
    qtd INT,
    valor DECIMAL(10,2),
    frete DECIMAL(10,2),
    codigoComprador INT
);


-- Inserindo dados
INSERT INTO #tmp_pedidos VALUES
('abc123','2024-03-19','brinq456rio','quebra-cabeca',1,43.22,5.32,123),
('abc123','2024-03-19','brinq789rio','jogo',1,43.22,5.32,123),
('abc789','2024-03-20','roupa123rio','camisa',2,47.25,6.21,789),
('abc741','2024-03-21','brinq789rio','jogo',1,43.22,5.32,123);


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
FROM #tmp_pedidos p
JOIN #Totais t ON t.codigoPedido = p.codigoPedido
GROUP BY p.codigoPedido, t.valor_total;

-- Atualizando tabela de compra com os pedidos
INSERT INTO compra (codigoPedido, SKU, quantidade, valorUnitario)
SELECT
    codigoPedido,
    SKU,
    qtd,
    valor
FROM #tmp_pedidos;

-- Pedidos semdp inseridos na ordem da fila
INSERT INTO expedicao (codigoPedido)
SELECT codigoPedido
FROM #Fila;
