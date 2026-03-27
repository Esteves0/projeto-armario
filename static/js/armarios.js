console.log("JS carregou");

let pagina = 1;
let blocoAtual = "A";



const blocos = {
  A: 0,
  B:36,
  C: 72,
  D: 108,
}

const armariosPorPagina = 18;
const totalpaginas = 2;
const totalArmariosPorPagina = armariosPorPagina * totalpaginas ;

function gerarArmarios() {
  const container = document.getElementById("armarios");
  container.innerHTML = "";
  for (let i = 1; i <= armariosPorPagina; i++) {
    const numeroArmario = i + (pagina -1) * armariosPorPagina + blocos[blocoAtual];

    const armario = document.createElement("div");
    armario.className = "armario";
    armario.id = `armario-${numeroArmario}`;

    armario.innerText = `Armario ${numeroArmario}`;

    armario.onclick = () => {
    
    window.location.href = `armario.html?id=${numeroArmario}`;
  }

    container.appendChild(armario);
  }
  
  
}

window.onload = gerarArmarios;

function trocarBloco() {
  blocoAtual = document.getElementById("bloco").value;
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
