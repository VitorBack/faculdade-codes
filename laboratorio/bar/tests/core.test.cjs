const { test } = require('node:test');
const assert = require('node:assert/strict');
const Core = require('../js/core.js');

function memoryStorage() {
  const entries = new Map();
  return { getItem: key => entries.has(key) ? entries.get(key) : null, setItem: (key, value) => entries.set(key, String(value)), entries };
}
function order(state, id = 'produto-1', count = 1) { for (let i = 0; i < count; i++) Core.addItem(state, id); }

test('inicializa e persiste produtos sem inventar vendas ou dívidas', () => {
  const storage = memoryStorage();
  const store = Core.createStore(storage);
  assert.equal(store.state.products.length, 12);
  assert.deepEqual(store.state.debts, []);
  assert.deepEqual(store.state.sales, []);
  assert.ok(Core.validState(JSON.parse(storage.getItem(Core.STORAGE_KEY))));
});

test('adiciona, agrupa, reduz e remove itens da comanda', () => {
  const state = Core.initialState();
  order(state, 'produto-1', 2); order(state, 'produto-4');
  assert.equal(Core.cart(state).length, 2);
  assert.equal(Core.quantity(Core.cart(state)), 3);
  assert.equal(Core.total(Core.cart(state)), 4900);
  Core.changeQuantity(state, 'produto-1', -1);
  assert.equal(Core.total(Core.cart(state)), 3700);
  Core.removeItem(state, 'produto-4');
  Core.changeQuantity(state, 'produto-1', -1);
  assert.equal(Core.cart(state).length, 0);
});

test('mantém comandas independentes entre as mesas', () => {
  const state = Core.initialState(); order(state);
  state.activeTable = 'Mesa 02'; order(state, 'produto-4');
  Core.checkout(state, 'imediato');
  assert.equal(Core.cart(state).length, 0);
  state.activeTable = 'Mesa 01';
  assert.equal(Core.total(Core.cart(state)), 1200);
});

test('pagamento imediato registra os itens, limpa a comanda e não gera fiado', () => {
  const state = Core.initialState(); order(state);
  const sale = Core.checkout(state, 'imediato');
  assert.equal(sale.total, 1200);
  assert.equal(sale.method, 'imediato');
  assert.equal(sale.items[0].quantity, 1);
  assert.equal(Core.cart(state).length, 0);
  assert.equal(state.debts.length, 0);
  assert.equal(state.sales.length, 1);
  order(state);
  assert.equal(sale.items[0].quantity, 1, 'histórico não compartilha referência com a comanda');
});

test('fiados do mesmo nome somam, ignorando espaços, caixa e acentos', () => {
  const state = Core.initialState(); order(state);
  Core.checkout(state, 'fiado', '  João   Silva ');
  order(state, 'produto-4');
  Core.checkout(state, 'fiado', 'JOAO SILVA');
  assert.equal(state.debts.length, 1);
  assert.equal(state.debts[0].name, 'João Silva');
  assert.equal(state.debts[0].balance, 3700);
  assert.equal(state.sales.length, 2);
});

test('quitação zera saldo e registra recebimento sem duplicar vendas', () => {
  const state = Core.initialState(); order(state); Core.checkout(state, 'fiado', 'Ana');
  const payment = Core.settleDebt(state, state.debts[0].id);
  assert.equal(payment.amount, 1200);
  assert.equal(state.debts[0].balance, 0);
  assert.equal(state.payments.length, 1);
  assert.equal(state.sales.length, 1);
  assert.throws(() => Core.settleDebt(state, state.debts[0].id), /já está quitada/);
  order(state); Core.checkout(state, 'fiado', 'Ana');
  assert.equal(state.debts.length, 1);
  assert.equal(state.debts[0].balance, 1200);
});

test('impede conta vazia, pagamento desconhecido e fiado sem nome', () => {
  const storage = memoryStorage(); const store = Core.createStore(storage);
  assert.throws(() => store.transact(s => Core.checkout(s, 'imediato')), /Adicione/);
  store.transact(s => Core.addItem(s, 'produto-1'));
  const before = JSON.stringify(store.state);
  assert.throws(() => store.transact(s => Core.checkout(s, 'fiado', '   ')), /nome/);
  assert.throws(() => store.transact(s => Core.checkout(s, 'desconhecido')), /pagamento/);
  assert.equal(JSON.stringify(store.state), before);
});

test('calcula preços em centavos sem erros de ponto flutuante', () => {
  assert.equal(Core.parsePrice('0,10'), 10);
  assert.equal(Core.parsePrice('0.20'), 20);
  assert.equal(Core.parsePrice('12,5'), 1250);
  assert.equal(Core.parsePrice('25'), 2500);
  assert.equal(Core.total([{ price: 10, quantity: 1 }, { price: 20, quantity: 1 }]), 30);
  for (const price of ['', '-1', '0', '1,999', '1.234,50', 'abc', 'Infinity', '1e3']) assert.throws(() => Core.parsePrice(price));
});

test('recupera produtos, comanda e fiados depois de recarregar', () => {
  const storage = memoryStorage(); const first = Core.createStore(storage);
  first.transact(s => { Core.addItem(s, 'produto-1'); Core.checkout(s, 'fiado', 'Carlos'); Core.addItem(s, 'produto-4'); Core.saveProduct(s, { name: 'Café', description: 'Coado', category: 'Sem álcool', price: 350, available: true }); });
  const next = Core.createStore(storage);
  assert.deepEqual(next.state, first.state);
  assert.equal(next.state.debts[0].balance, 1200);
  assert.equal(Core.total(Core.cart(next.state)), 2500);
  assert.equal(next.state.products.at(-1).name, 'Café');
});

test('falha de armazenamento não perde a comanda nem confirma a venda', () => {
  const storage = memoryStorage(); const store = Core.createStore(storage);
  store.transact(s => Core.addItem(s, 'produto-1'));
  const before = storage.getItem(Core.STORAGE_KEY);
  storage.setItem = () => { throw new Error('QuotaExceededError'); };
  assert.throws(() => store.transact(s => Core.checkout(s, 'fiado', 'Ana')), /não foi concluída/);
  assert.equal(store.state.sales.length, 0);
  assert.equal(store.state.debts.length, 0);
  assert.equal(Core.cart(store.state).length, 1);
  assert.equal(storage.getItem(Core.STORAGE_KEY), before);
});

test('dados corrompidos são preservados e novas gravações são bloqueadas', () => {
  const storage = memoryStorage(); storage.setItem(Core.STORAGE_KEY, '{inválido');
  const store = Core.createStore(storage);
  assert.match(store.error, /Não foi possível acessar/);
  assert.throws(() => store.transact(s => Core.addItem(s, 'produto-1')), /sobrescrito/);
  assert.equal(storage.getItem(Core.STORAGE_KEY), '{inválido');
});

test('não sobrescreve mudanças de outra aba', () => {
  const storage = memoryStorage(); const first = Core.createStore(storage); const second = Core.createStore(storage);
  first.transact(s => Core.addItem(s, 'produto-4'));
  assert.throws(() => second.transact(s => Core.addItem(s, 'produto-1')), /outra aba/);
  assert.equal(Core.total(Core.cart(Core.createStore(storage).state)), 2500);
});

test('editar preço preserva o preço anterior nos itens de uma comanda aberta', () => {
  const state = Core.initialState(); order(state);
  Core.saveProduct(state, { ...state.products[0], price: 1500 });
  order(state);
  assert.equal(Core.total(Core.cart(state)), 2400);
  Core.checkout(state, 'imediato'); order(state);
  assert.equal(Core.total(Core.cart(state)), 1500);
});

test('produto indisponível sai de novos pedidos e continua em comandas abertas', () => {
  const state = Core.initialState(); order(state);
  Core.saveProduct(state, { ...state.products[0], available: false });
  assert.throws(() => Core.addItem(state, 'produto-1'), /não está disponível/);
  assert.equal(Core.checkout(state, 'imediato').total, 1200);
});

test('validação rejeita produtos, linhas e totais inconsistentes', () => {
  const state = Core.initialState();
  state.products[0].price = -1; assert.equal(Core.validState(state), false);
  state.products[0].price = 1200; order(state);
  Core.cart(state)[0].quantity = -3; assert.equal(Core.validState(state), false);
  Core.cart(state)[0].quantity = 1;
  const sale = Core.checkout(state, 'imediato'); sale.total = 1;
  assert.equal(Core.validState(state), false);
  const invalidDate = Core.initialState();
  invalidDate.debts.push({ id: 'teste', name: 'Carlos', balance: 100, updatedAt: 'data inválida' });
  assert.equal(Core.validState(invalidDate), false);
});

test('quantidade não ultrapassa 999 e não pode receber deltas arbitrários', () => {
  const state = Core.initialState(); order(state); Core.cart(state)[0].quantity = 999;
  assert.throws(() => Core.addItem(state, 'produto-1'), /999/);
  assert.throws(() => Core.changeQuantity(state, 'produto-1', 1), /999/);
  assert.throws(() => Core.changeQuantity(state, 'produto-1', -999), /inválida/);
});
