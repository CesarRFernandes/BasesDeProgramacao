document.addEventListener("DOMContentLoaded", function () {
  const temperaturaInput = document.getElementById("temperatura");
  const atualizarBtn = document.getElementById("atualizar");
  const retangulo = document.getElementById("retangulo");
  const mensagem = document.getElementById("mensagem");

  atualizarBtn.addEventListener("click", function () {
    const valor = parseInt(temperaturaInput.value);
    mensagem.textContent = "";

    if (isNaN(valor) || valor < 0 || valor > 70) {
      retangulo.style.backgroundColor = "white";
      mensagem.textContent = "Valor inválido";
    } else {
      if (valor >= 0 && valor <= 29) {
        retangulo.style.backgroundColor = "lightblue";
      } else if (valor >= 30 && valor <= 45) {
        retangulo.style.backgroundColor = "lightyellow";
      } else if (valor >= 46 && valor <= 60) {
        retangulo.style.backgroundColor = "lightcoral";
      } else {
        retangulo.style.backgroundColor = "darkred";
      }
    }
  });
});
