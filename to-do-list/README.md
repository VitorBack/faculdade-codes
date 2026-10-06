# em dia — Lista de Tarefas Avançada

Aplicação responsiva desenvolvida com **HTML, CSS e JavaScript puro**, sem bibliotecas ou instalação de dependências.

## Como executar

Abra o arquivo `index.html` em um navegador moderno. Também é possível usar um servidor local, como a extensão Live Server do VS Code.

## Funcionalidades

- Adicionar tarefas com descrição, prioridade e prazo obrigatórios.
- Selecionar prioridade **Alta**, **Média** ou **Baixa**, identificadas por cores e rótulos.
- Exibir a data no formato brasileiro e sinalizar tarefas atrasadas ou com prazo para hoje.
- Concluir e reabrir tarefas com um checkbox; tarefas concluídas ficam tachadas e esmaecidas.
- Excluir tarefas pelo botão de lixeira de cada cartão.
- Filtrar por todas, pendentes ou concluídas e buscar pelo texto, com ou sem acentos.
- Acompanhar contadores e uma barra de progresso.
- Salvar as tarefas automaticamente no navegador com `localStorage`.
- Usar a interface em computadores e celulares, com navegação por teclado e rótulos acessíveis.

## Organização do projeto

| Arquivo | Responsabilidade |
| --- | --- |
| `index.html` | Estrutura semântica, formulário e regiões da interface. |
| `styles.css` | Cores, cartões, estados visuais e adaptação a telas menores. |
| `script.js` | Estado da aplicação, eventos, validação, filtros e persistência. |
| `favicon.svg` | Ícone exibido na aba do navegador. |

## Funcionamento do JavaScript

O array `tasks` guarda objetos com as propriedades `id`, `text`, `priority`, `date` e `done`. Os eventos alteram esse array, salvam os dados e chamam `render()` para atualizar a interface.

As datas usam `YYYY-MM-DD` internamente e são formatadas para `DD/MM/YYYY` na tela, sem conversão de fuso horário. O texto fornecido pelo usuário é inserido com `textContent`, sem ser interpretado como HTML.

Os dados ficam apenas no navegador e endereço usados. Abrir por outro endereço, trocar de navegador ou limpar seus dados não preserva a mesma lista. Caso o armazenamento esteja bloqueado ou cheio, a aplicação avisa e continua funcionando enquanto a página permanecer aberta.

## Verificação manual

1. Tente enviar o formulário vazio ou com uma descrição contendo apenas espaços.
2. Crie tarefas com cada prioridade e com datas passadas, atuais e futuras.
3. Conclua e reabra uma tarefa, observando os contadores, filtros e progresso.
4. Busque uma palavra com e sem acentos.
5. Recarregue a página para verificar a persistência.
6. Exclua as tarefas e recarregue para confirmar a remoção.
7. Reduza a largura da janela para conferir a interface em celular.
