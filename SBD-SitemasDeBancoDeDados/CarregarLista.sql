--criando tabela temporaria
CREATE TEMP TABLE tmp_pedidos (
    codigoPedido VARCHAR(20),
    dataPedido DATE,
    SKU VARCHAR(50),
    UPC VARCHAR(20),
    nomeProduto VARCHAR(100),
    qtd INT,
    valor DECIMAL(10,2),
    frete DECIMAL(10,2),
    email VARCHAR(100),
    codigoComprador INT,
    nomeComprador VARCHAR(100),
    endereco VARCHAR(200),
    CEP VARCHAR(20),
    UF VARCHAR(5),
    pais VARCHAR(50)
);


--inserindo dados
INSERT INTO tmp_pedidos VALUES
('abc123','2024-03-19','brinq456rio','456','quebra-cabeca',1,43.22,5.32,'samir@gmail.com',123,'Samir','Rua Exemplo 1','21212322','RJ','Brasil'),
('abc123','2024-03-19','brinq789rio','789','jogo',1,43.22,5.32,'samir@gmail.com',123,'Samir','Rua Exemplo 1','21212322','RJ','Brasil'),
('abc789','2024-03-20','roupa123rio','123','camisa',2,47.25,6.21,'teste@gmail.com',789,'Fulano','Rua Exemplo 2','14784520','RJ','Brasil'),
('abc741','2024-03-21','brinq789rio','789','jogo',1,43.22,5.32,'samir@gmail.com',123,'Samir','Rua Exemplo 1','21212322','RJ','Brasil');


--atualizando a tabela de clientes
INSERT INTO clientes (codigoComprador, nome, email, endereco, CEP, UF, pais)
SELECT DISTINCT
    codigoComprador,
    nomeComprador,
    email,
    endereco,
    CEP,
    UF,
    pais
FROM tmp_pedidos t
WHERE NOT EXISTS (
    SELECT 1 FROM clientes c WHERE c.codigoComprador = t.codigoComprador
);


--atualizando a tabela de produtos
INSERT INTO produtos (SKU, UPC, nomeProduto, valor)
SELECT DISTINCT
    SKU,
    UPC,
    nomeProduto,
    valor
FROM tmp_pedidos t
WHERE NOT EXISTS (
    SELECT 1 FROM produtos p WHERE p.SKU = t.SKU
);


--calcular o valor total do pedido
SELECT 
    codigoPedido,
    dataPedido,
    SUM(valor * qtd) + MAX(frete) AS valor_total
FROM tmp_pedidos
GROUP BY codigoPedido, dataPedido;


--inserindo pedidos na tabela
INSERT INTO pedidos (codigoPedido, dataPedido, codigoComprador, valor_total)
SELECT 
    t.codigoPedido,
    t.dataPedido,
    t.codigoComprador,
    SUM(t.valor * t.qtd) + MAX(t.frete) AS valor_total
FROM tmp_pedidos t
GROUP BY t.codigoPedido, t.dataPedido, t.codigoComprador;


--inserindo pedidos na tabela de compra
INSERT INTO compra (codigoPedido, SKU, qtd, valor_unitario)
SELECT 
    codigoPedido,
    SKU,
    qtd,
    valor
FROM tmp_pedidos;


--inserindo na tabela expedição
INSERT INTO expedicao (codigoPedido, endereco, CEP, UF, pais, status)
SELECT DISTINCT
    codigoPedido,
    endereco,
    CEP,
    UF,
    pais,
    'PENDENTE'
FROM tmp_pedidos;