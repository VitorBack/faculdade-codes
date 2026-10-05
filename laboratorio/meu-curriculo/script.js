// 1. Mapear o botão do HTML para o JavaScript
const botaoTema = document.getElementById('btn-tema');
// 2. Adicionar um evento de clique no botão
botaoTema.addEventListener('click', function() {
// LACUNA 8: Adicione a lógica para alternar a classe 'dark-mode' no corpo (body) da página.
// DICA DE PESQUISA: Busque por "javascript classList toggle" para descobrir o comando exato.
document.body.classList.toggle('dark-mode');
console.log("Tema alterado!");
});