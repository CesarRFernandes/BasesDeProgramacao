<?php
header('Content-Type: application/json');

function obterValor($chave, $padrao) {
    if (isset($_GET[$chave]) && is_numeric($_GET[$chave]) && $_GET[$chave] > 0) {
        return (int) $_GET[$chave];
    }
    return $padrao;
}

$limite = obterValor('limite', 60);
$quantidade = obterValor('quantidade', 6);

$quantidade = min($quantidade, $limite);

$numerosSorteados = [];

while (count($numerosSorteados) < $quantidade) {
    $numero = random_int(1, $limite);
    $numerosSorteados[$numero] = true;
}

$resultado = array_keys($numerosSorteados);
sort($resultado);

echo json_encode(['numeros' => $resultado]);
?>