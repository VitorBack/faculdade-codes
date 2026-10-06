"use strict";

// O array é a fonte de dados. Toda alteração passa por ele antes de atualizar o DOM.
const STORAGE_KEY = "em-dia.tasks.v1";
const PRIORITIES = { Alta: "high", Média: "medium", Baixa: "low" };
const form = document.querySelector("#task-form");
const textInput = document.querySelector("#task-text");
const dateInput = document.querySelector("#task-date");
const searchInput = document.querySelector("#task-search");
const taskList = document.querySelector("#task-list");
const filters = [...document.querySelectorAll("[data-filter]")];
const emptyState = document.querySelector("#empty-state");
const emptyAction = document.querySelector("#empty-action");
const toast = document.querySelector("#toast");
let activeFilter = "all";
let toastTimer;
let tasks = loadTasks();

// Datas do formulário são tratadas como datas locais, sem conversão para UTC.
function localDateKey(date = new Date()) {
  const year = String(date.getFullYear()).padStart(4, "0");
  const month = String(date.getMonth() + 1).padStart(2, "0");
  const day = String(date.getDate()).padStart(2, "0");
  return `${year}-${month}-${day}`;
}

function isValidDate(value) {
  if (typeof value !== "string" || !/^\d{4}-\d{2}-\d{2}$/.test(value)) return false;
  const [year, month, day] = value.split("-").map(Number);
  if (year < 1 || month < 1 || month > 12 || day < 1 || day > 31) return false;
  const date = new Date(0);
  date.setFullYear(year, month - 1, day);
  return localDateKey(date) === value;
}

function formatDate(value) {
  return value.split("-").reverse().join("/");
}

function storageWarning(message) {
  document.querySelector("#storage-note").classList.add("warning");
  document.querySelector("#storage-text").textContent = message;
}

function loadTasks() {
  try {
    const raw = localStorage.getItem(STORAGE_KEY);
    if (raw === null) return [];
    const saved = JSON.parse(raw);
    if (!Array.isArray(saved)) throw new Error("Lista inválida");
    const ids = new Set();
    const valid = saved.filter((task) => {
      if (!task || typeof task.id !== "string" || !task.id || ids.has(task.id)
        || typeof task.text !== "string" || !task.text.trim() || task.text.length > 180
        || !Object.hasOwn(PRIORITIES, task.priority) || !isValidDate(task.date)
        || typeof task.done !== "boolean") return false;
      ids.add(task.id);
      return true;
    });
    if (valid.length !== saved.length) storageWarning("Algumas tarefas salvas não puderam ser carregadas.");
    return valid;
  } catch {
    storageWarning("Não foi possível carregar as tarefas salvas neste navegador.");
    return [];
  }
}

function saveTasks() {
  try {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(tasks));
    document.querySelector("#storage-note").classList.remove("warning");
    document.querySelector("#storage-text").textContent = "Suas tarefas ficam salvas neste navegador.";
  } catch {
    storageWarning("Salvamento indisponível. Mantenha esta página aberta para preservar suas tarefas.");
  }
}

function notify(message) {
  clearTimeout(toastTimer);
  toast.textContent = message;
  toast.classList.add("visible");
  toastTimer = setTimeout(() => toast.classList.remove("visible"), 3200);
}

function createIcon(name) {
  const svg = document.createElementNS("http://www.w3.org/2000/svg", "svg");
  svg.classList.add("icon");
  svg.setAttribute("aria-hidden", "true");
  const use = document.createElementNS("http://www.w3.org/2000/svg", "use");
  use.setAttribute("href", `#icon-${name}`);
  svg.append(use);
  return svg;
}

function makeElement(tag, className, text) {
  const element = document.createElement(tag);
  element.className = className;
  // textContent mantém o texto digitado como texto, nunca como HTML executável.
  if (text !== undefined) element.textContent = text;
  return element;
}

function createTaskCard(task, today) {
  const card = makeElement("li", `task-card ${PRIORITIES[task.priority]}${task.done ? " is-done" : ""}`);
  card.dataset.id = task.id;

  const checkbox = makeElement("input", "task-checkbox");
  checkbox.type = "checkbox";
  checkbox.id = `task-${task.id}`;
  checkbox.checked = task.done;
  checkbox.setAttribute("aria-label", `${task.done ? "Marcar como pendente" : "Concluir"}: ${task.text}`);

  const body = makeElement("div", "task-body");
  const title = makeElement("label", "task-title", task.text);
  title.htmlFor = checkbox.id;
  const meta = makeElement("div", "task-meta");
  const priority = makeElement("span", "priority-tag", task.priority);
  priority.setAttribute("aria-label", `Prioridade ${task.priority.toLowerCase()}`);
  const deadline = makeElement("span", "task-deadline");
  const date = makeElement("time", "", formatDate(task.date));
  date.dateTime = task.date;
  deadline.append(createIcon("calendar"), date);
  meta.append(priority, deadline);

  if (!task.done && task.date <= today) {
    const overdue = task.date < today;
    meta.append(makeElement("span", `deadline-status${overdue ? " overdue" : ""}`, overdue ? "Atrasada" : "Hoje"));
  }

  const removeButton = makeElement("button", "delete-task");
  removeButton.type = "button";
  removeButton.title = "Excluir tarefa";
  removeButton.setAttribute("aria-label", `Excluir: ${task.text}`);
  removeButton.append(createIcon("trash"));
  body.append(title, meta);
  card.append(checkbox, body, removeButton);
  return card;
}

function normalizeText(text) {
  return text.normalize("NFD").replace(/[\u0300-\u036f]/g, "").toLocaleLowerCase("pt-BR");
}

function render() {
  const completed = tasks.filter((task) => task.done).length;
  const today = localDateKey();
  document.querySelector("#total-count").textContent = tasks.length;
  document.querySelector("#pending-count").textContent = tasks.length - completed;
  document.querySelector("#done-count").textContent = completed;
  document.querySelector("#progress-text").textContent = `${completed} de ${tasks.length} concluídas`;
  const percentage = tasks.length ? Math.round(completed / tasks.length * 100) : 0;
  const progress = document.querySelector("#task-progress");
  progress.value = percentage;
  progress.textContent = `${percentage}%`;

  const query = normalizeText(searchInput.value.trim());
  const visibleTasks = tasks.filter((task) => {
    const matchesFilter = activeFilter === "all" || (activeFilter === "done" ? task.done : !task.done);
    return matchesFilter && normalizeText(task.text).includes(query);
  });

  const fragment = document.createDocumentFragment();
  visibleTasks.forEach((task) => fragment.append(createTaskCard(task, today)));
  taskList.replaceChildren(fragment);
  document.querySelector("#list-count").textContent = visibleTasks.length;
  emptyState.hidden = visibleTasks.length > 0;
  emptyAction.hidden = false;

  let title = "Seu dia começa com uma tarefa";
  let description = "O que você quer tirar do papel hoje? Adicione sua primeira tarefa e vamos começar.";
  let action = "Criar minha primeira tarefa";
  if (query) {
    title = "Nenhuma tarefa encontrada";
    description = "Tente buscar por outra palavra ou veja todas as suas tarefas.";
    action = "Limpar busca e filtros";
  } else if (activeFilter === "done") {
    title = "Suas conquistas vão aparecer aqui";
    description = "Marque uma tarefa como concluída para acompanhar seu progresso.";
    action = "Ver todas as tarefas";
  } else if (activeFilter === "pending" && tasks.length > 0) {
    title = "Tudo em dia. Pode respirar!";
    description = "Você concluiu todas as suas tarefas. Aproveite essa pequena conquista.";
    action = "Adicionar outra tarefa";
  }
  document.querySelector("#empty-title").textContent = title;
  document.querySelector("#empty-description").textContent = description;
  emptyAction.replaceChildren(document.createTextNode(`${action} `), createIcon("arrow"));
  filters.forEach((button) => {
    const selected = button.dataset.filter === activeFilter;
    button.classList.toggle("active", selected);
    button.setAttribute("aria-pressed", String(selected));
  });
}

form.addEventListener("submit", (event) => {
  event.preventDefault();
  const text = textInput.value.trim();
  if (!text) {
    textInput.setCustomValidity("Digite uma tarefa, além de espaços em branco.");
    textInput.reportValidity();
    return;
  }
  if (!isValidDate(dateInput.value)) {
    dateInput.setCustomValidity("Escolha uma data válida para o prazo.");
    dateInput.reportValidity();
    return;
  }
  tasks.unshift({
    id: globalThis.crypto?.randomUUID?.() ?? `${Date.now()}-${Math.random().toString(36).slice(2)}`,
    text,
    priority: new FormData(form).get("priority"),
    date: dateInput.value,
    done: false,
  });
  saveTasks();
  form.reset();
  activeFilter = "all";
  searchInput.value = "";
  render();
  textInput.focus();
  notify("Tarefa adicionada. Um passo mais perto!");
});

textInput.addEventListener("input", () => textInput.setCustomValidity(""));
dateInput.addEventListener("input", () => dateInput.setCustomValidity(""));

// Delegação de eventos: a lista atende também aos cartões criados depois.
taskList.addEventListener("change", (event) => {
  if (!event.target.matches(".task-checkbox")) return;
  const id = event.target.closest(".task-card").dataset.id;
  const task = tasks.find((item) => item.id === id);
  if (!task) return;
  task.done = event.target.checked;
  saveTasks();
  render();
  const checkbox = document.getElementById(`task-${id}`);
  (checkbox ?? filters.find((button) => button.dataset.filter === activeFilter)).focus({ preventScroll: true });
  notify(task.done ? "Tarefa concluída. Boa!" : "Tarefa marcada como pendente.");
});

taskList.addEventListener("click", (event) => {
  const button = event.target.closest(".delete-task");
  if (!button) return;
  const card = button.closest(".task-card");
  const cards = [...taskList.children];
  const position = cards.indexOf(card);
  tasks = tasks.filter((task) => task.id !== card.dataset.id);
  saveTasks();
  render();
  const nextCard = taskList.children[Math.min(position, taskList.children.length - 1)];
  (nextCard?.querySelector(".delete-task") ?? emptyAction).focus({ preventScroll: true });
  notify("Tarefa excluída.");
});

filters.forEach((button) => button.addEventListener("click", () => {
  activeFilter = button.dataset.filter;
  render();
}));
searchInput.addEventListener("input", render);

emptyAction.addEventListener("click", () => {
  if (searchInput.value.trim() || activeFilter === "done") {
    searchInput.value = "";
    activeFilter = "all";
    render();
    filters[0].focus();
  } else {
    textInput.focus();
    textInput.scrollIntoView({ block: "center", behavior: "auto" });
  }
});

function updateToday() {
  const now = new Date();
  const element = document.querySelector("#today");
  element.dateTime = localDateKey(now);
  element.textContent = new Intl.DateTimeFormat("pt-BR", { day: "numeric", month: "long", year: "numeric" }).format(now);
}

// Atualiza a situação dos prazos quando o dia muda, sem recarregar a página.
let lastDay = localDateKey();
setInterval(() => {
  if (lastDay !== localDateKey()) {
    lastDay = localDateKey();
    updateToday();
    render();
  }
}, 60_000);

updateToday();
render();
