# Bar João & Maria

Aplicação estática de caixa desenvolvida conforme o enunciado **Bar Joao&Maria.pdf**, usando somente **HTML, CSS e JavaScript puro**. Sem frameworks, dependências externas, backend ou etapa de compilação. As ilustrações SVG também são locais.

## Como abrir

Abra `index.html` no navegador. Para usar um endereço local estável, caso tenha Node.js instalado, execute `npm start` e acesse `http://127.0.0.1:4173`. Não é necessário executar `npm install`.

## Como usar

1. Escolha a mesa (ou o balcão) na comanda.
2. Busque produtos ou filtre por categoria e clique em **Adicionar**. Ajuste as quantidades com **+** e **−**; a lixeira remove o item inteiro.
3. Clique em **Fechar conta** e escolha **Pagamento imediato** ou **Deixar fiado**. No fiado, informe o nome do cliente. Novas compras com o mesmo nome somam à dívida existente; espaços extras, maiúsculas e acentos são normalizados na identificação.
4. Na **Caderneta**, confira os saldos e use **Quitar dívida** para registrar o recebimento integral e zerar a conta. Uma confirmação precede a quitação.
5. Em **Vendas**, consulte pedidos e quitações, incluindo os totais do dia. A quitação aumenta os recebimentos, sem contabilizar a mesma venda novamente.
6. Use o botão de ajustes ao lado do título do cardápio para cadastrar produtos, alterar preços ou marcar um item como indisponível. Comandas que já contêm o produto conservam o nome e o preço registrados ao adicioná-lo.

Cada mesa mantém sua própria comanda. Produtos, comandas, mesa selecionada, fiados, vendas e quitações persistem após atualizar ou fechar a página. As vendas são apenas **registros locais** de pagamentos realizados no balcão; a aplicação não processa pagamentos reais.

## Persistência

Os dados são arrays de objetos armazenados em uma única chave de `localStorage`: `joao-maria:caixa:v1`. Cada operação grava um estado completo; em caso de falha de armazenamento, a operação não é concluída e os dados em memória permanecem intactos. Valores são calculados em centavos inteiros para evitar erros de arredondamento.

Os dados pertencem ao navegador e à origem utilizados. Abrir via `file://` e via `http://127.0.0.1:4173` usa armazenamentos diferentes. O comportamento de `localStorage` em arquivos locais varia entre navegadores; se houver bloqueio, use o servidor opcional. Limpar dados do navegador remove os registros; o modo privado não oferece persistência duradoura. O aplicativo não sincroniza dispositivos. Utilize uma aba de caixa por vez: alterações em outra aba são detectadas e exigem atualização antes de novas gravações.

**Exportar dados**, disponível na Caderneta e em Vendas, baixa uma cópia JSON de todos os registros para consulta ou backup manual. Não há importação automática pela interface. O cadastro inicial contém 12 produtos de exemplo e nenhuma dívida ou venda fictícia.

## Organização

- `index.html`: estrutura semântica, navegação e janelas de diálogo.
- `styles.css`: identidade visual, estados de interação e responsividade.
- `js/core.js`: dados iniciais, validações, regras de negócio e persistência.
- `js/app.js`: renderização dinâmica do DOM e eventos.
- `js/illustrations.js` e `assets/favicon.svg`: ilustrações vetoriais locais.
- `scripts/serve.cjs`: servidor HTTP local opcional, sem bibliotecas.
- `tests/core.test.cjs`: testes automatizados das regras de negócio.

## Verificação

Com Node.js instalado, execute `npm test`. Os testes cobrem valores, quantidades, comandas por mesa, pagamentos, acúmulo e quitação de fiado, persistência, falhas de armazenamento e edição de produtos.

Para conferir a interface, adicione dois produtos, finalize um pedido à vista, faça dois pedidos fiados para o mesmo nome, atualize a página e quite a dívida. Verifique também uma largura de celular e a navegação pelo teclado.

## Correspondência com o enunciado

| Requisito | Implementação |
| --- | --- |
| Cardápio dinâmico com nome, preço e botão | Cards gerados a partir do array de produtos |
| Comanda com quantidades, remoção e total | Comandas independentes por mesa e cálculo imediato |
| Pagamento imediato | Registro da venda, limpeza da comanda e aviso de sucesso |
| Deixar fiado | Nome obrigatório, registro da venda e acúmulo do saldo |
| Caderneta e quitação | Clientes com saldo positivo e quitação integral confirmada |
| Persistência em localStorage | Produtos e fiados, além de comandas e histórico |
| Manipulação de DOM com arrays de objetos | Renderização via JavaScript; produtos e clientes não são fixos no HTML |
| Responsividade | Layouts para computador, tablet e celular |
