let pagina = 1;
const armariosPorPagina = 18;
const totalpaginas = 6;
function gerarArmarios() {
  const container = document.getElementById("armarios");
  container.innerHTML = "";
  for (let i = 1; i <= armariosPorPagina; i++) {
    const armario = document.createElement("div");
    armario.className = "armario";
    armario.innerText = `Armário ${i + (pagina - 1) * armariosPorPagina}`;

    armario.onclick = () => {
    const id = i + (pagina -1) * armariosPorPagina;
    window.location.href = `armario.html?id=${id}`;
  }

    container.appendChild(armario);
  }
  
  
}

function trocarBloco() {
  pagina = 1;
  document.getElementById("pagina-atual").innerText = pagina;
  gerarArmarios();
}

function paginaAnterior() {
  if (pagina > 1) {
    pagina--;
    document.getElementById("pagina-atual").innerText = pagina;
    gerarArmarios();
  }
}

function proximaPagina() {
  if (pagina < totalpaginas) {
    pagina++;
    document.getElementById("pagina-atual").innerText = pagina;
    gerarArmarios();
  }
  
}




window.onload = gerarArmarios;
