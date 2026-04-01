<?php
header("Content-Type: application/json");

$params = filter_input_array(INPUT_POST, [
    "nome" => FILTER_SANITIZE_STRING,
    "faixa" => FILTER_SANITIZE_NUMBER_INT,
    "doenca" => FILTER_VALIDATE_BOOLEAN
]);

$nome = $params["nome"] ?? "Usuário";
$faixa = (int)($params["faixa"] ?? 1);
$doenca = $params["doenca"] ?? false;

$valorBase = 200;
$valorFaixa = $valorBase * pow(1.5, $faixa - 1);

if ($doenca) {
    $valorFaixa *= 1.3;
}

$valorFinal = number_format($valorFaixa, 2, ',', '');

echo json_encode([
    "nome" => $nome,
    "valor" => $valorFinal
]);
?>