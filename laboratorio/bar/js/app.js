(function () {
  'use strict';
  const Core = window.BarCore;
  let storage;
  try { storage = window.localStorage; } catch (_) { storage = { getItem() { throw new Error('Armazenamento indisponível'); } }; }
  const store = Core.createStore(storage);
  const $ = selector => document.querySelector(selector);
  const $$ = selector => [...document.querySelectorAll(selector)];
  const currency = new Intl.NumberFormat('pt-BR', { style: 'currency', currency: 'BRL' });
  const brl = cents => currency.format(cents / 100);
  const dateTime = value => new Intl.DateTimeFormat('pt-BR', { dateStyle: 'short', timeStyle: 'short' }).format(new Date(value));
  const paths = {
    menu: '<rect x="3" y="3" width="7" height="7" rx="1.5"/><rect x="14" y="3" width="7" height="7" rx="1.5"/><rect x="3" y="14" width="7" height="7" rx="1.5"/><rect x="14" y="14" width="7" height="7" rx="1.5"/>',
    book: '<path d="M5 3h14v18H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2Zm0 14h14M7 3v14m3-9h6m-6 4h4"/>',
    receipt: '<path d="m5 3 3 2 4-2 4 2 3-2v18l-3-2-4 2-4-2-3 2ZM9 9h6m-6 4h6"/>',
    search: '<circle cx="10.5" cy="10.5" r="6.5"/><path d="m16 16 4.5 4.5"/>',
    sliders: '<path d="M4 7h7m4 0h5M4 17h3m4 0h9"/><circle cx="13" cy="7" r="2"/><circle cx="9" cy="17" r="2"/>',
    plus: '<path d="M12 5v14M5 12h14"/>', close: '<path d="m6 6 12 12M6 18 18 6"/>',
    check: '<path d="m5 12 4 4L19 6"/>',
    table: '<rect x="3" y="5" width="18" height="9" rx="2"/><path d="M6 14v5m12-5v5M7 9h10"/>',
    lock: '<rect x="5" y="10" width="14" height="11" rx="2"/><path d="M8 10V7a4 4 0 0 1 8 0v3m-4 5v2"/>',
    trash: '<path d="M3 6h18M9 6V3h6v3M6 6l1 15h10l1-15M10 10v7m4-7v7"/>',
    beer: '<path d="M5 7h11v13H5ZM16 9h3a2 2 0 0 1 2 2v4a2 2 0 0 1-2 2h-3M5 7a3 3 0 0 1 2-5 3 3 0 0 1 5 0 3 3 0 0 1 4 5M9 10v6m3-6v6"/>',
    food: '<path d="M3 13a9 9 0 0 1 18 0ZM2 17h20m-10-13V2"/>',
    drink: '<path d="m4 3 8 10 8-10ZM12 13v8m-4 0h8M7 7h10"/>',
    water: '<path d="M9 3h6v4l3 4v9H6v-9l3-4ZM6 13h12m-9-6h6"/>',
    wallet: '<path d="M20 7H5a2 2 0 0 1 0-4h13v4M3 5v14a2 2 0 0 0 2 2h15V7m0 5h-6v5h6"/><path d="M16 14.5h1"/>',
    download: '<path d="M12 3v12m-5-5 5 5 5-5M4 16v5h16v-5"/>',
    edit: '<path d="m14 5 5 5M4 20l5-1L21 7l-5-5L4 14ZM13 20h8"/>'
  };
  function icon(name) { return `<svg class="icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">${paths[name] || paths.menu}</svg>`; }
  function node(tag, className, text) {
    const element = document.createElement(tag);
    if (className) element.className = className;
    if (text !== undefined) element.textContent = text;
    return element;
  }
  function iconNode(name, className = '') { const el = node('span', className); el.innerHTML = icon(name); return el; }
  function button(text, className, action, iconName) {
    const el = node('button', className);
    el.type = 'button';
    if (iconName) el.append(iconNode(iconName));
    el.append(document.createTextNode(text));
    el.addEventListener('click', action);
    return el;
  }
  let activeView = 'cardapio';
  let activeCategory = 'Todos';
  let toastTimer;
  let confirmAction = null;
  let editingId = null;
  let checkoutSnapshot = '';
  let checkoutTable = '';
  function toast(message, error = false) {
    clearTimeout(toastTimer);
    $('#toast').textContent = message;
    $('#toast').classList.toggle('error', error);
    $('#toast').hidden = false;
    toastTimer = setTimeout(() => { $('#toast').hidden = true; }, error ? 9000 : 4000);
  }
  function transact(operation, onSuccess) {
    try {
      const result = store.transact(operation);
      renderAll();
      onSuccess?.(result);
      return true;
    } catch (error) { toast(error.message, true); return false; }
  }
  function emptyState(title, description, iconName, action) {
    const empty = node('div', 'empty-state');
    empty.append(iconNode(iconName, 'empty-illustration'), node('h3', '', title), node('p', '', description));
    if (action) empty.append(button(action.label, 'button secondary', action.callback));
    return empty;
  }
  function setView(view) {
    if (!['cardapio', 'caderneta', 'vendas'].includes(view)) view = 'cardapio';
    activeView = view;
    $$('.view').forEach(el => { el.hidden = el.id !== `view-${view}`; });
    $$('.nav-item').forEach(el => {
      const selected = el.dataset.view === view;
      el.classList.toggle('active', selected);
      if (selected) el.setAttribute('aria-current', 'page'); else el.removeAttribute('aria-current');
    });
    $('#mobile-cart').hidden = view !== 'cardapio';
    window.scrollTo({ top: 0, behavior: 'instant' });
    renderAll();
  }
  function renderCategories() {
    const icons = ['menu', 'beer', 'food', 'drink', 'water'];
    $('#category-filters').replaceChildren(...['Todos', ...Core.CATEGORIES].map((category, i) => {
      const el = button(category, `filter-button${category === activeCategory ? ' active' : ''}`, () => {
        activeCategory = category;
        renderCategories(); renderProducts();
        [...$('#category-filters').children].find(child => child.textContent === category)?.focus();
      }, icons[i]);
      el.setAttribute('aria-pressed', String(category === activeCategory));
      return el;
    }));
  }
  function renderProducts() {
    const query = Core.nameKey($('#product-search').value);
    const products = store.state.products.filter(p => p.available && (activeCategory === 'Todos' || p.category === activeCategory) && Core.nameKey(`${p.name} ${p.description} ${p.category}`).includes(query));
    $('#products-heading').textContent = activeCategory === 'Todos' ? 'Nosso cardápio' : activeCategory;
    $('#product-count').textContent = `${products.length} ${products.length === 1 ? 'opção' : 'opções'} da casa`;
    const cards = products.map(product => {
      const card = node('article', 'product-card');
      const art = node('div', 'product-art');
      art.dataset.category = product.category;
      art.innerHTML = window.BarArt.product(product.art);
      if (product.id === 'produto-1') art.append(node('span', 'product-tag', 'A QUERIDINHA'));
      if (product.id === 'produto-4') art.append(node('span', 'product-tag', 'PRA COMPARTILHAR'));
      const item = Core.cart(store.state).find(line => line.productId === product.id);
      if (item) art.append(node('span', 'product-quantity', `${item.quantity} na comanda`));
      const body = node('div', 'product-body');
      body.append(node('h3', '', product.name), node('p', 'product-description', product.description));
      const actions = node('div', 'product-action');
      const add = button('Adicionar', 'add-button', () => {
        transact(s => Core.addItem(s, product.id), () => {
          toast(`${product.name} na comanda · ${store.state.activeTable}.`);
          const next = [...$('#product-grid').querySelectorAll('button')].find(el => el.dataset.productId === product.id);
          next?.focus({ preventScroll: true });
        });
      }, 'plus');
      add.setAttribute('aria-label', `Adicionar ${product.name}`);
      add.dataset.productId = product.id;
      actions.append(node('strong', 'product-price', brl(product.price)), add);
      body.append(actions); card.append(art, body);
      return card;
    });
    $('#product-grid').replaceChildren(...(cards.length ? cards : [emptyState('Nada por aqui ainda.', 'Tente outro nome ou escolha uma categoria diferente.', 'search', { label: 'Ver todo o cardápio', callback: () => { $('#product-search').value = ''; activeCategory = 'Todos'; renderCategories(); renderProducts(); } })]));
  }
  function cartControl(productId, label, className, action, iconName) {
    const el = button(iconName ? '' : label, className, () => {
      if (transact(action)) {
        const selector = `[data-line-id="${CSS.escape(productId)}"]`;
        const line = $('#cart-items').querySelector(selector);
        const replacement = line && [...line.querySelectorAll('button')].find(b => b.getAttribute('aria-label') === el.getAttribute('aria-label'));
        (replacement || $('#table-select')).focus({ preventScroll: true });
      }
    }, iconName);
    return el;
  }
  function renderCart() {
    const items = Core.cart(store.state);
    const count = Core.quantity(items);
    const total = brl(Core.total(items));
    $('#table-select').value = store.state.activeTable;
    $('#cart-count').textContent = count;
    $('#cart-total').textContent = total;
    $('#cart-subtotal').textContent = total;
    $('#mobile-cart-count').textContent = count;
    $('#mobile-cart-total').textContent = total;
    $('#checkout-button').disabled = !count || !!store.error;
    $('#clear-cart').disabled = !count;
    if (!items.length) {
      const empty = node('div', 'cart-empty');
      empty.append(iconNode('receipt', 'empty-illustration'), node('strong', '', 'A mesa está esperando.'), node('p', '', 'Adicione os favoritos do cardápio para começar a comanda.'));
      $('#cart-items').replaceChildren(empty); return;
    }
    $('#cart-items').replaceChildren(...items.map(item => {
      const row = node('article', 'cart-line'); row.dataset.lineId = item.productId;
      const info = node('div'); info.append(node('h3', '', item.name), node('p', 'line-price', `${brl(item.price)} / un.`));
      const remove = cartControl(item.productId, '', 'remove-button', s => Core.removeItem(s, item.productId), 'trash');
      remove.setAttribute('aria-label', `Remover ${item.name}`);
      const quantity = node('div', 'quantity-control');
      const minus = cartControl(item.productId, '−', '', s => Core.changeQuantity(s, item.productId, -1));
      minus.setAttribute('aria-label', `Diminuir quantidade de ${item.name}`);
      const plus = cartControl(item.productId, '+', '', s => Core.changeQuantity(s, item.productId, 1));
      plus.setAttribute('aria-label', `Aumentar quantidade de ${item.name}`);
      const countLabel = node('span', '', item.quantity); countLabel.setAttribute('aria-label', `${item.quantity} unidades`);
      quantity.append(minus, countLabel, plus);
      row.append(info, remove, quantity, node('strong', 'line-total', brl(item.price * item.quantity)));
      return row;
    }));
  }
  function renderLedger() {
    const debts = store.state.debts.filter(d => d.balance > 0);
    $('#debt-count').textContent = debts.length; $('#debt-count').hidden = !debts.length;
    $('#debt-total').textContent = brl(debts.reduce((sum, debt) => sum + debt.balance, 0));
    $('#debt-clients').textContent = debts.length;
    const query = Core.nameKey($('#customer-search').value);
    const filtered = debts.filter(d => Core.nameKey(d.name).includes(query)).sort((a, b) => a.name.localeCompare(b.name, 'pt-BR'));
    const rows = filtered.map(debt => {
      const row = node('article', 'debt-card');
      const initials = debt.name.split(' ').filter(Boolean).slice(0, 2).map(word => word[0]).join('').toLocaleUpperCase('pt-BR');
      const info = node('div', 'debt-info');
      info.append(node('h3', '', debt.name), node('p', '', `Último pedido: ${dateTime(debt.updatedAt)}`));
      const settle = button('Quitar dívida', 'button secondary', () => openConfirm('Acertar a caderneta?', `Confirmar o recebimento de ${brl(debt.balance)} de ${debt.name}?\nA dívida será zerada e a quitação ficará no histórico.`, 'Confirmar quitação', () => {
        const payment = store.transact(s => Core.settleDebt(s, debt.id));
        renderAll(); toast(`Conta de ${payment.customer} quitada. Tudo certo!`);
      }), 'check');
      settle.setAttribute('aria-label', `Quitar dívida de ${debt.name}`);
      row.append(node('div', 'customer-avatar', initials), info, node('strong', 'debt-amount', brl(debt.balance)), settle);
      return row;
    });
    $('#debt-list').replaceChildren(...(rows.length ? rows : [emptyState(query ? 'Cliente não encontrado.' : 'Tudo em dia por aqui.', query ? 'Tente buscar por outro nome.' : 'Quando alguém deixar a conta para depois, o nome e o valor aparecem aqui.', query ? 'search' : 'check')]));
  }
  function renderSales() {
    const today = new Date().toDateString();
    const todaySales = store.state.sales.filter(s => new Date(s.date).toDateString() === today);
    const todayPayments = store.state.payments.filter(p => new Date(p.date).toDateString() === today);
    $('#sales-today').textContent = brl(todaySales.reduce((sum, sale) => sum + sale.total, 0));
    $('#received-today').textContent = brl(todaySales.filter(s => s.method === 'imediato').reduce((sum, sale) => sum + sale.total, 0) + todayPayments.reduce((sum, p) => sum + p.amount, 0));
    $('#orders-today').textContent = todaySales.length;
    const sales = [...store.state.sales].reverse().map(sale => {
      const row = node('article', 'sale-row');
      const info = node('div', 'sale-info');
      info.append(node('h3', '', `${sale.table}${sale.customer ? ` · ${sale.customer}` : ''}`), node('p', '', sale.items.map(item => `${item.quantity}× ${item.name}`).join(' · ')), node('small', '', dateTime(sale.date)));
      row.append(iconNode('receipt', 'sale-icon'), info, node('span', `payment-badge${sale.method === 'fiado' ? ' credit' : ''}`, sale.method === 'fiado' ? 'Na caderneta' : 'Pagamento imediato'), node('strong', 'sale-total', brl(sale.total)));
      return row;
    });
    $('#sales-list').replaceChildren(...(sales.length ? sales : [emptyState('A primeira rodada vem aí.', 'As comandas finalizadas aparecem aqui, com data, mesa e forma de pagamento.', 'receipt', { label: 'Abrir o cardápio', callback: () => navigate('cardapio') })]));
    const payments = [...store.state.payments].reverse().map(payment => {
      const row = node('article', 'sale-row');
      const info = node('div', 'sale-info'); info.append(node('h3', '', payment.customer), node('p', '', dateTime(payment.date)));
      row.append(iconNode('check', 'sale-icon'), info, node('span', 'payment-badge', 'Dívida quitada'), node('strong', 'sale-total', brl(payment.amount)));
      return row;
    });
    $('#payments-list').replaceChildren(...(payments.length ? payments : [emptyState('Nenhuma quitação registrada.', 'Ao quitar uma dívida, o recebimento será anotado aqui.', 'book')]));
  }
  function renderManagedProducts() {
    $('#managed-products').replaceChildren(...store.state.products.map(product => {
      const row = node('div', 'managed-product'); const info = node('div');
      info.append(node('h3', '', product.name), node('p', '', `${product.category}${product.available ? '' : ' · Indisponível'}`));
      const edit = button('Editar', 'button secondary', () => openProductEditor(product.id), 'edit');
      edit.setAttribute('aria-label', `Editar ${product.name}`);
      row.append(info, node('strong', '', brl(product.price)), edit); return row;
    }));
  }
  function renderAll() {
    renderProducts(); renderCart(); renderLedger();
    if (activeView === 'vendas') renderSales();
    if ($('#products-dialog').open) renderManagedProducts();
  }
  function navigate(view) { if (location.hash === `#${view}`) setView(view); else location.hash = view; }
  function openConfirm(title, description, label, action) {
    $('#confirm-heading').textContent = title;
    $('#confirm-description').textContent = description;
    $('#confirm-action').textContent = label;
    $('#confirm-error').hidden = true;
    confirmAction = action;
    $('#confirm-dialog').showModal();
  }
  function showError(selector, error) { $(selector).textContent = error.message; $(selector).hidden = false; }
  function openCheckout() {
    if (!Core.cart(store.state).length) return;
    checkoutSnapshot = JSON.stringify(Core.cart(store.state)); checkoutTable = store.state.activeTable;
    $('#checkout-form').reset(); $('#checkout-error').hidden = true;
    $('#customer-field').hidden = true; $('#customer-name').required = false;
    $('#confirm-checkout').textContent = 'Confirmar pagamento →';
    $('#checkout-table').textContent = store.state.activeTable;
    const count = Core.quantity(Core.cart(store.state));
    $('#checkout-items').textContent = `${count} ${count === 1 ? 'item na comanda' : 'itens na comanda'}`;
    $('#checkout-total').textContent = brl(Core.total(Core.cart(store.state)));
    $('#customer-suggestions').replaceChildren(...store.state.debts.map(d => { const option = node('option'); option.value = d.name; return option; }));
    $('#checkout-dialog').showModal();
  }
  function openProductEditor(id = null) {
    editingId = id;
    const product = store.state.products.find(p => p.id === id);
    $('#products-dialog').close(); $('#product-form').reset(); $('#product-error').hidden = true;
    $('#product-heading').textContent = id ? 'Editar produto' : 'Novo produto';
    if (product) {
      $('#product-name').value = product.name; $('#product-description').value = product.description;
      $('#product-price').value = (product.price / 100).toFixed(2).replace('.', ',');
      $('#product-category').value = product.category; $('#product-available').checked = product.available;
    }
    $('#product-dialog').showModal();
  }
  function exportData() {
    const exported = { exportedAt: new Date().toISOString(), ...store.state };
    const url = URL.createObjectURL(new Blob([JSON.stringify(exported, null, 2)], { type: 'application/json;charset=utf-8' }));
    const link = node('a'); link.href = url;
    const date = new Date();
    link.download = `joao-maria-${date.getFullYear()}-${String(date.getMonth() + 1).padStart(2, '0')}-${String(date.getDate()).padStart(2, '0')}.json`;
    document.body.append(link); link.click(); link.remove();
    setTimeout(() => URL.revokeObjectURL(url), 10000);
    toast('Cópia dos dados exportada. Guarde o arquivo em um lugar seguro.');
  }
  // Estruturas fixas e eventos. Dados do usuário entram sempre por textContent.
  $$('[data-icon]').forEach(el => { el.innerHTML = icon(el.dataset.icon); });
  $('#banner-art').innerHTML = window.BarArt.banner();
  $('#today-label').textContent = new Intl.DateTimeFormat('pt-BR', { day: '2-digit', month: 'short', year: 'numeric' }).format(new Date()).replace(' de ', ' ');
  $('#table-select').replaceChildren(...Core.TABLES.map(table => { const option = node('option', '', table); option.value = table; return option; }));
  $('#product-category').replaceChildren(...Core.CATEGORIES.map(category => { const option = node('option', '', category); option.value = category; return option; }));
  $$('.nav-item').forEach(el => el.addEventListener('click', () => navigate(el.dataset.view)));
  window.addEventListener('hashchange', () => setView(location.hash.slice(1)));
  $('#product-search').addEventListener('input', renderProducts);
  $('#customer-search').addEventListener('input', renderLedger);
  $('#table-select').addEventListener('change', event => { transact(s => { s.activeTable = event.target.value; }); $('#table-select').value = store.state.activeTable; });
  $('#clear-cart').addEventListener('click', () => openConfirm('Limpar esta comanda?', `Os itens de ${store.state.activeTable} serão removidos. Nenhuma venda será registrada.`, 'Limpar comanda', () => { store.transact(s => { s.carts[s.activeTable] = []; }); renderAll(); toast('Comanda limpa. Pronta para um novo pedido.'); }));
  $('#checkout-button').addEventListener('click', openCheckout);
  $('#mobile-cart').addEventListener('click', () => { $('#cart-panel').scrollIntoView({ behavior: matchMedia('(prefers-reduced-motion: reduce)').matches ? 'instant' : 'smooth', block: 'start' }); $('#table-select').focus({ preventScroll: true }); });
  $$('[data-close]').forEach(el => el.addEventListener('click', () => document.getElementById(el.dataset.close).close()));
  $$('dialog').forEach(dialog => dialog.addEventListener('click', event => { if (event.target === dialog) { const rect = dialog.getBoundingClientRect(); if (event.clientX < rect.left || event.clientX > rect.right || event.clientY < rect.top || event.clientY > rect.bottom) dialog.close(); } }));
  $('#checkout-form').addEventListener('change', event => {
    if (event.target.name !== 'payment') return;
    const credit = event.target.value === 'fiado';
    $('#customer-field').hidden = !credit; $('#customer-name').required = credit;
    $('#confirm-checkout').textContent = credit ? 'Anotar na caderneta →' : 'Confirmar pagamento →';
    $('#checkout-error').hidden = true;
    if (credit) $('#customer-name').focus();
  });
  $('#checkout-form').addEventListener('submit', event => {
    event.preventDefault(); $('#checkout-error').hidden = true;
    const submit = $('#confirm-checkout'); submit.disabled = true;
    try {
      if (checkoutSnapshot !== JSON.stringify(Core.cart(store.state)) || checkoutTable !== store.state.activeTable) throw new Error('A comanda mudou. Feche esta janela e confira os itens.');
      const method = new FormData(event.currentTarget).get('payment');
      const sale = store.transact(s => Core.checkout(s, method, $('#customer-name').value));
      $('#checkout-dialog').close(); renderAll();
      toast(method === 'fiado' ? `${brl(sale.total)} anotados para ${sale.customer}. Até a próxima!` : `Pagamento de ${brl(sale.total)} registrado. Conta fechada!`);
    } catch (error) { showError('#checkout-error', error); }
    finally { submit.disabled = false; }
  });
  $('#confirm-form').addEventListener('submit', event => {
    event.preventDefault(); $('#confirm-action').disabled = true;
    try { confirmAction?.(); $('#confirm-dialog').close(); }
    catch (error) { showError('#confirm-error', error); }
    finally { $('#confirm-action').disabled = false; }
  });
  $('#confirm-dialog').addEventListener('close', () => { confirmAction = null; });
  $('#manage-products').addEventListener('click', () => { renderManagedProducts(); $('#products-dialog').showModal(); });
  $('#new-product').addEventListener('click', () => openProductEditor());
  $('#product-dialog').addEventListener('close', () => { renderManagedProducts(); $('#products-dialog').showModal(); });
  $('#product-form').addEventListener('submit', event => {
    event.preventDefault(); $('#product-error').hidden = true;
    try {
      const price = Core.parsePrice($('#product-price').value);
      store.transact(s => Core.saveProduct(s, { id: editingId, name: $('#product-name').value, description: $('#product-description').value, price, category: $('#product-category').value, available: $('#product-available').checked }));
      $('#product-dialog').close(); renderAll(); toast('Produto salvo. Cardápio atualizado!');
    } catch (error) { showError('#product-error', error); }
  });
  $$('.export-button').forEach(el => el.addEventListener('click', exportData));
  document.addEventListener('keydown', event => {
    if (event.key === '/' && !['INPUT', 'SELECT', 'TEXTAREA'].includes(document.activeElement.tagName) && !$$('dialog').some(d => d.open) && activeView === 'cardapio') { event.preventDefault(); $('#product-search').focus(); }
  });
  window.addEventListener('storage', event => {
    if (event.key === Core.STORAGE_KEY || event.key === null) {
      $('#storage-warning').textContent = 'Os dados foram alterados em outra aba. Atualize esta página antes de continuar para usar a versão mais recente.';
      $('#storage-warning').hidden = false;
      $('#storage-status').textContent = 'Atualização necessária';
    }
  });
  if (store.error) { $('#storage-warning').textContent = store.error; $('#storage-warning').hidden = false; $('#storage-status').textContent = 'Armazenamento indisponível'; }
  renderCategories(); setView(location.hash.slice(1));
})();
