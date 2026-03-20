const params = new URLSearchParams(window.location.search);
const idArmario = params.get('id');

document.getElementById('titulo').innerText = `Armário ${id}`;

