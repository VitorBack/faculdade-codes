/* Regras de negócio independentes do DOM. Valores monetários em centavos. */
(function (root, factory) {
  const api = factory();
  if (typeof module === 'object' && module.exports) module.exports = api;
  else root.BarCore = api;
})(typeof globalThis !== 'undefined' ? globalThis : this, function () {
  'use strict';
  const STORAGE_KEY = 'joao-maria:caixa:v1';
  const CATEGORIES = ['Cervejas', 'Petiscos', 'Drinks', 'Sem álcool'];
  const TABLES = ['Balcão', ...Array.from({ length: 10 }, (_, i) => `Mesa ${String(i + 1).padStart(2, '0')}`)];
  const seeds = [
    ['Cerveja Pilsen', '600 ml · Gelada no ponto', 1200, 'Cervejas', 'beer'],
    ['Cerveja Long Neck', '330 ml · Leve e refrescante', 900, 'Cervejas', 'bottle'],
    ['Chopp da casa', '300 ml · Colarinho caprichado', 800, 'Cervejas', 'chopp'],
    ['Porção de fritas', 'Crocantes, com um toque de sal', 2500, 'Petiscos', 'fries'],
    ['Calabresa acebolada', 'Na chapa, com pão fresquinho', 3200, 'Petiscos', 'sausage'],
    ['Pastelzinho da casa', '6 unidades · Queijo e carne', 2800, 'Petiscos', 'pastel'],
    ['Caipirinha', 'Limão, cachaça e aquele capricho', 1800, 'Drinks', 'caipirinha'],
    ['Gin tônica', 'Gin, tônica e um toque de limão', 2400, 'Drinks', 'gin'],
    ['Refrigerante', 'Lata 350 ml · Bem gelado', 600, 'Sem álcool', 'soda'],
    ['Suco de laranja', '300 ml · Feito na hora', 800, 'Sem álcool', 'juice'],
    ['Água mineral', '500 ml · Com ou sem gás', 400, 'Sem álcool', 'water'],
    ['Mandioca frita', 'Douradinha, macia por dentro', 2200, 'Petiscos', 'cassava']
  ];
  const copy = value => JSON.parse(JSON.stringify(value));
  const normalizeName = value => String(value).trim().replace(/\s+/g, ' ');
  const nameKey = value => normalizeName(value).normalize('NFD').replace(/[\u0300-\u036f]/g, '').toLocaleLowerCase('pt-BR');
  const uid = () => (globalThis.crypto?.randomUUID?.() || `${Date.now()}-${Math.random().toString(16).slice(2)}`);
  const money = value => Number.isSafeInteger(value) && value >= 0;
  function initialState() {
    return { version: 1, products: seeds.map((p, i) => ({ id: `produto-${i + 1}`, name: p[0], description: p[1], price: p[2], category: p[3], art: p[4], available: true })), carts: {}, activeTable: 'Mesa 01', debts: [], sales: [], payments: [] };
  }
  function validLine(line) { return line && typeof line.productId === 'string' && typeof line.name === 'string' && money(line.price) && Number.isInteger(line.quantity) && line.quantity > 0 && line.quantity <= 999; }
  function validState(s) {
    return !!(s && s.version === 1 && TABLES.includes(s.activeTable) && Array.isArray(s.products) &&
      s.products.every(p => p && typeof p.id === 'string' && typeof p.name === 'string' && p.name.trim() && typeof p.description === 'string' && money(p.price) && p.price > 0 && CATEGORIES.includes(p.category) && typeof p.available === 'boolean' && typeof p.art === 'string') &&
      new Set(s.products.map(p => p.id)).size === s.products.length &&
      s.carts && typeof s.carts === 'object' && !Array.isArray(s.carts) && Object.entries(s.carts).every(([table, lines]) => TABLES.includes(table) && Array.isArray(lines) && lines.every(validLine) && new Set(lines.map(l => l.productId)).size === lines.length) &&
      Array.isArray(s.debts) && s.debts.every(d => d && typeof d.id === 'string' && typeof d.name === 'string' && d.name.trim() && money(d.balance) && typeof d.updatedAt === 'string' && Number.isFinite(Date.parse(d.updatedAt))) &&
      new Set(s.debts.map(d => nameKey(d.name))).size === s.debts.length &&
      Array.isArray(s.sales) && s.sales.every(v => v && typeof v.id === 'string' && TABLES.includes(v.table) && ['imediato', 'fiado'].includes(v.method) && typeof v.customer === 'string' && typeof v.date === 'string' && Number.isFinite(Date.parse(v.date)) && money(v.total) && Array.isArray(v.items) && v.items.length > 0 && v.items.every(validLine) && total(v.items) === v.total) &&
      Array.isArray(s.payments) && s.payments.every(p => p && typeof p.id === 'string' && typeof p.customer === 'string' && money(p.amount) && typeof p.date === 'string' && Number.isFinite(Date.parse(p.date))));
  }
  function total(lines) { return lines.reduce((sum, line) => sum + line.price * line.quantity, 0); }
  function cart(s) { return s.carts[s.activeTable] || []; }
  function quantity(lines) { return lines.reduce((sum, line) => sum + line.quantity, 0); }
  function addItem(s, productId) {
    const product = s.products.find(p => p.id === productId && p.available);
    if (!product) throw new Error('Este produto não está disponível.');
    const lines = s.carts[s.activeTable] ||= [];
    const existing = lines.find(line => line.productId === productId);
    if (existing) {
      if (existing.quantity >= 999) throw new Error('O limite é de 999 unidades por produto.');
      existing.quantity++;
    } else lines.push({ productId, name: product.name, price: product.price, quantity: 1 });
  }
  function changeQuantity(s, productId, delta) {
    if (![1, -1].includes(delta)) throw new Error('Quantidade inválida.');
    const line = cart(s).find(item => item.productId === productId);
    if (!line) throw new Error('Item não encontrado na comanda.');
    if (line.quantity + delta > 999) throw new Error('O limite é de 999 unidades por produto.');
    line.quantity += delta;
    s.carts[s.activeTable] = cart(s).filter(item => item.quantity > 0);
  }
  function removeItem(s, productId) { s.carts[s.activeTable] = cart(s).filter(item => item.productId !== productId); }
  function checkout(s, method, customer = '', date = new Date().toISOString()) {
    const items = cart(s);
    if (!items.length) throw new Error('Adicione pelo menos um produto à comanda.');
    if (!['imediato', 'fiado'].includes(method)) throw new Error('Escolha uma forma de pagamento.');
    const name = normalizeName(customer);
    if (method === 'fiado' && (!name || name.length > 80)) throw new Error('Informe o nome do cliente (até 80 caracteres).');
    const amount = total(items);
    if (!money(amount)) throw new Error('O valor da comanda é inválido.');
    if (method === 'fiado') {
      let debt = s.debts.find(d => nameKey(d.name) === nameKey(name));
      if (debt) {
        if (!money(debt.balance + amount)) throw new Error('O saldo ultrapassa o limite permitido.');
        debt.balance += amount;
        debt.updatedAt = date;
      } else s.debts.push({ id: uid(), name, balance: amount, updatedAt: date });
    }
    const sale = { id: uid(), table: s.activeTable, items: copy(items), total: amount, method, customer: method === 'fiado' ? name : '', date };
    s.sales.push(sale);
    s.carts[s.activeTable] = [];
    return sale;
  }
  function settleDebt(s, debtId, date = new Date().toISOString()) {
    const debt = s.debts.find(d => d.id === debtId);
    if (!debt || debt.balance <= 0) throw new Error('Esta conta já está quitada.');
    const payment = { id: uid(), customer: debt.name, amount: debt.balance, date };
    s.payments.push(payment);
    debt.balance = 0;
    debt.updatedAt = date;
    return payment;
  }
  function parsePrice(value) {
    const normalized = String(value).trim();
    if (!/^\d{1,5}([,.]\d{1,2})?$/.test(normalized)) throw new Error('Informe um preço válido, como 12,50 (sem separador de milhar).');
    const [whole, fraction = ''] = normalized.replace(',', '.').split('.');
    const price = Number(whole) * 100 + Number(fraction.padEnd(2, '0'));
    if (price <= 0) throw new Error('O preço precisa ser maior que zero.');
    return price;
  }
  function saveProduct(s, input) {
    const name = normalizeName(input.name);
    if (!name || name.length > 60) throw new Error('Informe um nome com até 60 caracteres.');
    if (!CATEGORIES.includes(input.category)) throw new Error('Escolha uma categoria válida.');
    if (!money(input.price) || input.price <= 0 || input.price > 9999999) throw new Error('Informe um preço válido.');
    const existing = input.id ? s.products.find(p => p.id === input.id) : null;
    if (input.id && !existing) throw new Error('Produto não encontrado.');
    const arts = { Cervejas: 'beer', Petiscos: 'fries', Drinks: 'caipirinha', 'Sem álcool': 'juice' };
    const product = { id: existing?.id || uid(), name, description: String(input.description || '').trim().slice(0, 100), price: input.price, category: input.category, available: !!input.available, art: existing?.category === input.category ? existing.art : arts[input.category] };
    if (existing) Object.assign(existing, product); else s.products.push(product);
    return product;
  }
  /* Uma gravação única por operação evita vendas salvas sem a baixa da comanda. */
  function createStore(storage) {
    let state, lastRaw, blocked = false, initialError = '';
    try {
      lastRaw = storage.getItem(STORAGE_KEY);
      state = lastRaw === null ? initialState() : JSON.parse(lastRaw);
      if (!validState(state)) throw new Error('Dados inválidos');
      if (lastRaw === null) { lastRaw = JSON.stringify(state); storage.setItem(STORAGE_KEY, lastRaw); }
    } catch (_) {
      state = initialState(); blocked = true;
      initialError = 'Não foi possível acessar os dados salvos. Verifique o armazenamento do navegador. Nenhum dado existente será sobrescrito.';
    }
    return {
      get state() { return state; },
      get error() { return initialError; },
      transact(operation) {
        if (blocked) throw new Error(initialError);
        let raw;
        try { raw = storage.getItem(STORAGE_KEY); } catch (_) { throw new Error('O navegador bloqueou o armazenamento. A operação não foi concluída.'); }
        if (raw !== lastRaw) throw new Error('Os dados mudaram em outra aba. Atualize a página antes de continuar.');
        const next = copy(state);
        const result = operation(next);
        if (!validState(next)) throw new Error('Não foi possível validar os dados desta operação.');
        const serialized = JSON.stringify(next);
        try { storage.setItem(STORAGE_KEY, serialized); } catch (_) { throw new Error('Não foi possível salvar. O armazenamento pode estar cheio ou bloqueado. A operação não foi concluída.'); }
        state = next; lastRaw = serialized;
        return result;
      }
    };
  }
  return { STORAGE_KEY, CATEGORIES, TABLES, initialState, validState, cart, total, quantity, nameKey, normalizeName, addItem, changeQuantity, removeItem, checkout, settleDebt, parsePrice, saveProduct, createStore };
});
