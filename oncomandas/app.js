/**
 * Sistema de Comandas PWA
 * Desenvolvido com JavaScript puro, HTML5 e CSS3
 * Funciona offline com IndexedDB
 * Otimizado para dispositivos móveis
 */

"use strict";

// CONFIGURAÇÕES E CONSTANTES

const CONFIG = {
  dbName: "ComandaDB",
  dbVersion: 1,
  storeName: "comandas",
  maxCommands: 1000, // Limite máximo de comandas armazenadas
  toastDuration: 3000, // Duração do toast em ms
  debounceDelay: 300, // Delay para busca em ms
};

// CARDÁPIO - PRODUTOS E CATEGORIAS

// TODO: Adicionar produtos reais aqui
const CARDAPIO = {
  bebidas: {
    nome: "Bebidas",
    produtos: [
      // Exemplo de estrutura - substitua pelos produtos reais
      { id: "coca-lata", nome: "Coca-Cola lata", preco: 6.0 },
      { id: "guarana-lata", nome: "Guarana lata", preco: 6.0 },
      { id: "agua500", nome: "Água Mineral 500ml", preco: 4.0 },
      {
        id: "cerveja-heineken-long",
        nome: "Cerveja heineken Long Neck ",
        preco: 10.0,
      },
      { id: "cerveja-bud-long", nome: "Cerveja bud Long Neck", preco: 10.0 },
      {
        id: "cerveja-heineken-long-especial",
        nome: "Cerveja heineken Long Especial ",
        preco: 12.0,
      },
      {
        id: "cerveja-bud-long-especial",
        nome: "Cerveja bud Long Especial",
        preco: 12.0,
      },
      { id: "cerveja-bud-lata", nome: "Cerveja bud lata", preco: 8.0 },
      {
        id: "cerveja-heineken-lata",
        nome: "Cerveja heineken lata",
        preco: 8.0,
      },
      {
        id: "suco-abacaxi-com-laranja",
        nome: "Suco abacaxi com laranja",
        preco: 15.0,
      },
      {
        id: "suco-manga-com-laranja",
        nome: "Suco manga com laranja",
        preco: 15.0,
      },
      {
        id: "suco-abacaxi-com-manga",
        nome: "Suco abacaxi com manga",
        preco: 15.0,
      },
      { id: "vitaminas", nome: "vitaminas", preco: 18.0 },
      { id: "energetico", nome: "energetico", preco: 15.0 },
      // Adicione mais bebidas aqui...
    ],
  },
  caipira: {
    nome: "Caipira",
    produtos: [
      // Exemplo de estrutura - substitua pelos produtos reais
      { id: "limao-cachaca", nome: "Limão com Cachaça", preco: 26.0 },
      { id: "limao-vodka", nome: "Limão com Vodka", preco: 26.0 },
      { id: "limao-vinho", nome: "Limão com Vinho", preco: 26.0 },
      { id: "frutas-cachaca", nome: "Frutas com Cachaça", preco: 28.0 },
      { id: "frutas-vodka", nome: "Frutas com vodka", preco: 28.0 },
      // Adicione mais bebidas aqui...
    ],
  },
  drinks: {
    nome: "Drinks",
    produtos: [
      { id: "batidas", nome: "Batidas com Vodka", preco: 28.0 },
      { id: "mojito", nome: "Mojito", preco: 28.0 },
      { id: "pina", nome: "Pina Colada", preco: 28.0 },
      // Adicione mais bebidas aqui...
    ],
  },
  doses: {
    nome: "Doses",
    produtos: [
      { id: "bacardi", nome: "Bacardi", preco: 10.0 },
      { id: "campari", nome: "Campari", preco: 10.0 },
      { id: "gin", nome: "Gin", preco: 14.0 },
      { id: "vod-nac", nome: "Vodka Nacional", preco: 10.0 },
      { id: "vod-abs", nome: "vodka Absolut", preco: 15.0 },
      { id: "tequila", nome: "tequila", preco: 15.0 },
      { id: "wisky", nome: "wisky", preco: 15.0 },
      // Adicione mais bebidas aqui...
    ],
  },
  pratos: {
    nome: "Pratos",
    produtos: [
      // Exemplo de estrutura - substitua pelos produtos reais
      { id: "px-mila", nome: "Peixe à milanesa", preco: 28.0 },
      { id: "px-gre", nome: "Peixe Grelhado", preco: 35.0 },
      { id: "cam-mila", nome: "Camarão à milanesa", preco: 38.0 },
      { id: "carne", nome: "Carne", preco: 35.0 },
      { id: "veg", nome: "Vegano", preco: 29.0 },
      { id: "fran-mila", nome: "Frango à milanesa", preco: 28.0 },
      { id: "fran-gre", nome: "Frango grelhado", preco: 28.0 },
      { id: "str-carne", nome: "Strogonoff de carne", preco: 35.0 },
      { id: "str-frango", nome: "Strogonoff de frango", preco: 30.0 },
      { id: "str-camarao", nome: "Strogonoff de camarão", preco: 38.0 },
      { id: "str-funghi", nome: "Strogonoff de funghi", preco: 30.0 },
      { id: "add-cam", nome: "Adicional de molho de camarão", preco: 12.0 },
      // Adicione mais pratos aqui...
    ],
  },
  pratoskids: {
    nome: "Pratos Kids",
    produtos: [
      // Exemplo de estrutura - substitua pelos produtos reais
      { id: "px-kd", nome: "Peixe Kids", preco: 25.0 },
      { id: "carne-kd", nome: "Carne Kids", preco: 25.0 },
      { id: "frango-kd", nome: "Frango Kids", preco: 25.0 },
      { id: "cam-kids", nome: "Camarão à milanesa Kids", preco: 28.0 },
    ],
  },
  aperitivos: {
    nome: "aperitivos",
    produtos: [
      // Exemplo de estrutura - substitua pelos produtos reais
      { id: "cam-mila", nome: "Camarão à Milanesa", preco: 80.0 },
      { id: "cam-alho", nome: "Camarão alho e oleo", preco: 70.0 },
      { id: "isca-peixe", nome: "Isca de Peixe", preco: 48.0 },
      { id: "posta-peixe", nome: "Posta de Peixe Frito", preco: 38.0 },
      { id: "isca-frango", nome: "Isca de Frango", preco: 42.0 },
      { id: "batata-pole", nome: "Batata ou Polenta Frita", preco: 27.0 },
      { id: "mini-cox", nome: "Mini coxinha(6 und)", preco: 26.0 },
      { id: "mini-almo", nome: "Mini almondegas(6 und)", preco: 28.0 },
      { id: "bol-peixe", nome: "Bolinho Peixe(6 und)", preco: 28.0 },
      { id: "bol-siri", nome: "Bolinho Siri(6 und)", preco: 35.0 },
      {
        id: "btt-baconcheader",
        nome: "Batata Frita com bacon e cheddar",
        preco: 37.0,
      },
      {
        id: "frango-apassarinho",
        nome: "frango a passarinho c/fritas",
        preco: 42.0,
      },
      { id: "tabua-frios", nome: "Tabua de frios", preco: 53.0 },
      { id: "tabua-mista", nome: "Tabua Mista", preco: 82.0 },
      // Adicione mais petiscos aqui...
    ],
  },
  hamburguer: {
    nome: "hamburguer",
    produtos: [
      // Exemplo de estrutura - substitua pelos produtos reais
      { id: "ham-casa", nome: "Hamburguer da casa", preco: 28.0 },
      { id: "ham-veg", nome: "Hamburguer Vegetariano", preco: 28.0 },
      // Adicione mais petiscos aqui...
    ],
  },
  sobremesas: {
    nome: "sobremesas",
    produtos: [
      // Exemplo de estrutura - substitua pelos produtos reais
      { id: "acai", nome: "Tijela de Açaí", preco: 25.0 },
      { id: "acai-surf", nome: "Tijela de Açaí Surf", preco: 28.0 },
      { id: "brownie", nome: "Brownie", preco: 6.0 },
      { id: "bombom", nome: "bom bom", preco: 8.0 },
      // Adicione mais petiscos aqui...
    ],
  },
  // Adicione mais categorias conforme necessário
};

// ESTADO GLOBAL DA APLICAÇÃO

let appState = {
  db: null,
  currentScreen: "list",
  currentCommand: null,
  commands: [],
  filteredCommands: [],
  isEditing: false,
  searchDebounce: null,
  tempItems: [], // Lista temporária para novos itens
};

// ELEMENTOS DOM

const elements = {
  // Telas
  screens: {
    list: document.getElementById("screenList"),
    form: document.getElementById("screenForm"),
    view: document.getElementById("screenView"),
    settings: document.getElementById("screenSettings"),
  },

  // Navegação
  settingsBtn: document.getElementById("settingsBtn"),
  backFromFormBtn: document.getElementById("backFromFormBtn"),
  backFromViewBtn: document.getElementById("backFromViewBtn"),
  backFromSettingsBtn: document.getElementById("backFromSettingsBtn"),

  // Lista
  searchInput: document.getElementById("searchInput"),
  commandsList: document.getElementById("commandsList"),
  emptyState: document.getElementById("emptyState"),
  newCommandBtn: document.getElementById("newCommandBtn"),

  // Formulário
  formTitle: document.getElementById("formTitle"),
  commandForm: document.getElementById("commandForm"),
  clientName: document.getElementById("clientName"),
  tableNumber: document.getElementById("tableNumber"),

  // Seleção de produtos
  categorySelect: document.getElementById("categorySelect"),
  productSelect: document.getElementById("productSelect"),
  productQuantity: document.getElementById("productQuantity"),
  productObservation: document.getElementById("productObservation"),
  addProductBtn: document.getElementById("addProductBtn"),
  orderTotal: document.getElementById("orderTotal"),

  // Lista de itens (mantido para compatibilidade)
  newItem: document.getElementById("newItem"),
  addItemBtn: document.getElementById("addItemBtn"),
  itemsList: document.getElementById("itemsList"),

  // Visualização
  commandDetails: document.getElementById("commandDetails"),
  editCommandBtn: document.getElementById("editCommandBtn"),
  deleteCommandBtn: document.getElementById("deleteCommandBtn"),
  copyCommandBtn: document.getElementById("copyCommandBtn"),

  // Configurações
  totalCommands: document.getElementById("totalCommands"),
  todayCommands: document.getElementById("todayCommands"),
  deleteAllBtn: document.getElementById("deleteAllBtn"),

  // Modal
  overlay: document.getElementById("overlay"),
  modalTitle: document.getElementById("modalTitle"),
  modalText: document.getElementById("modalText"),
  modalCancel: document.getElementById("modalCancel"),
  modalConfirm: document.getElementById("modalConfirm"),

  // Toast
  toast: document.getElementById("toast"),
  toastText: document.getElementById("toastText"),
};

// GERENCIAMENTO DO INDEXEDDB

/**
 * Inicializa o banco de dados IndexedDB
 * @returns {Promise<IDBDatabase>}
 */
function initDB() {
  return new Promise((resolve, reject) => {
    const request = indexedDB.open(CONFIG.dbName, CONFIG.dbVersion);

    request.onerror = () => {
      console.error("Erro ao abrir banco de dados:", request.error);
      reject(request.error);
    };

    request.onsuccess = () => {
      appState.db = request.result;
      resolve(request.result);
    };

    request.onupgradeneeded = (event) => {
      const db = event.target.result;

      // Cria a store de comandas se não existir
      if (!db.objectStoreNames.contains(CONFIG.storeName)) {
        const store = db.createObjectStore(CONFIG.storeName, {
          keyPath: "id",
          autoIncrement: true,
        });

        // Cria índices para busca eficiente
        store.createIndex("clientName", "clientName", { unique: false });
        store.createIndex("createdAt", "createdAt", { unique: false });
        store.createIndex("tableNumber", "tableNumber", { unique: false });
      }
    };
  });
}

/**
 * Salva uma comanda no banco
 * @param {Object} command - Dados da comanda
 * @returns {Promise<number>} ID da comanda salva
 */
function saveCommand(command) {
  return new Promise((resolve, reject) => {
    const transaction = appState.db.transaction(
      [CONFIG.storeName],
      "readwrite"
    );
    const store = transaction.objectStore(CONFIG.storeName);

    const request = store.put(command);

    request.onsuccess = () => resolve(request.result);
    request.onerror = () => reject(request.error);
  });
}

/**
 * Busca todas as comandas
 * @returns {Promise<Array>}
 */
function getAllCommands() {
  return new Promise((resolve, reject) => {
    const transaction = appState.db.transaction([CONFIG.storeName], "readonly");
    const store = transaction.objectStore(CONFIG.storeName);

    const request = store.getAll();

    request.onsuccess = () => {
      const commands = request.result.sort(
        (a, b) => new Date(b.createdAt) - new Date(a.createdAt)
      );
      resolve(commands);
    };
    request.onerror = () => reject(request.error);
  });
}

/**
 * Busca uma comanda específica por ID
 * @param {number} id - ID da comanda
 * @returns {Promise<Object>}
 */
function getCommand(id) {
  return new Promise((resolve, reject) => {
    const transaction = appState.db.transaction([CONFIG.storeName], "readonly");
    const store = transaction.objectStore(CONFIG.storeName);

    const request = store.get(id);

    request.onsuccess = () => resolve(request.result);
    request.onerror = () => reject(request.error);
  });
}

/**
 * Remove uma comanda do banco
 * @param {number} id - ID da comanda
 * @returns {Promise<void>}
 */
function deleteCommand(id) {
  return new Promise((resolve, reject) => {
    const transaction = appState.db.transaction(
      [CONFIG.storeName],
      "readwrite"
    );
    const store = transaction.objectStore(CONFIG.storeName);

    const request = store.delete(id);

    request.onsuccess = () => resolve();
    request.onerror = () => reject(request.error);
  });
}

/**
 * Remove todas as comandas
 * @returns {Promise<void>}
 */
function deleteAllCommands() {
  return new Promise((resolve, reject) => {
    const transaction = appState.db.transaction(
      [CONFIG.storeName],
      "readwrite"
    );
    const store = transaction.objectStore(CONFIG.storeName);

    const request = store.clear();

    request.onsuccess = () => resolve();
    request.onerror = () => reject(request.error);
  });
}

// UTILITÁRIOS

/**
 * Formata data/hora para exibição
 * @param {Date|string} date - Data a ser formatada
 * @returns {string}
 */
function formatDateTime(date) {
  const d = new Date(date);
  const now = new Date();
  const today = new Date(now.getFullYear(), now.getMonth(), now.getDate());
  const dateOnly = new Date(d.getFullYear(), d.getMonth(), d.getDate());

  const timeString = d.toLocaleTimeString("pt-BR", {
    hour: "2-digit",
    minute: "2-digit",
  });

  if (dateOnly.getTime() === today.getTime()) {
    return `Hoje às ${timeString}`;
  } else {
    const dateString = d.toLocaleDateString("pt-BR", {
      day: "2-digit",
      month: "2-digit",
    });
    return `${dateString} às ${timeString}`;
  }
}

/**
 * Conta comandas criadas hoje
 * @param {Array} commands - Lista de comandas
 * @returns {number}
 */
function countTodayCommands(commands) {
  const today = new Date();
  const todayStart = new Date(
    today.getFullYear(),
    today.getMonth(),
    today.getDate()
  );

  return commands.filter((cmd) => new Date(cmd.createdAt) >= todayStart).length;
}

/**
 * Gera ID único para itens
 * @returns {string}
 */
function generateId() {
  return Date.now().toString() + Math.random().toString(36).substr(2, 5);
}

/**
 * Debounce function para busca
 * @param {Function} func - Função a ser chamada
 * @param {number} wait - Tempo de espera em ms
 * @returns {Function}
 */
function debounce(func, wait) {
  let timeout;
  return function executedFunction(...args) {
    const later = () => {
      clearTimeout(timeout);
      func.apply(this, args);
    };
    clearTimeout(timeout);
    timeout = setTimeout(later, wait);
  };
}

/**
 * Sanitiza texto para evitar XSS
 * @param {string} text - Texto a ser sanitizado
 * @returns {string}
 */
function sanitizeText(text) {
  const div = document.createElement("div");
  div.textContent = text;
  return div.innerHTML;
}

/**
 * Formata valor monetário para exibição
 * @param {number} value - Valor a ser formatado
 * @returns {string}
 */
function formatCurrency(value) {
  return new Intl.NumberFormat("pt-BR", {
    style: "currency",
    currency: "BRL",
  }).format(value);
}

/**
 * Calcula o total de uma lista de itens
 * @param {Array} items - Lista de itens com preço e quantidade
 * @returns {number}
 */
function calculateTotal(items) {
  return items.reduce((total, item) => {
    if (item.preco && item.quantidade) {
      return total + item.preco * item.quantidade;
    }
    return total;
  }, 0);
}

// INTERFACE DO USUÁRIO

/**
 * Exibe notificação toast
 * @param {string} message - Mensagem a ser exibida
 * @param {string} type - Tipo da notificação (success, error, info)
 */
function showToast(message, type = "info") {
  elements.toastText.textContent = message;
  elements.toast.className = `toast show ${type}`;

  setTimeout(() => {
    elements.toast.classList.remove("show");
  }, CONFIG.toastDuration);
}

/**
 * Exibe modal de confirmação
 * @param {string} title - Título do modal
 * @param {string} text - Texto do modal
 * @returns {Promise<boolean>}
 */
function showConfirmModal(title, text) {
  return new Promise((resolve) => {
    elements.modalTitle.textContent = title;
    elements.modalText.textContent = text;
    elements.overlay.classList.add("active");

    const handleConfirm = () => {
      elements.overlay.classList.remove("active");
      elements.modalConfirm.removeEventListener("click", handleConfirm);
      elements.modalCancel.removeEventListener("click", handleCancel);
      resolve(true);
    };

    const handleCancel = () => {
      elements.overlay.classList.remove("active");
      elements.modalConfirm.removeEventListener("click", handleConfirm);
      elements.modalCancel.removeEventListener("click", handleCancel);
      resolve(false);
    };

    elements.modalConfirm.addEventListener("click", handleConfirm);
    elements.modalCancel.addEventListener("click", handleCancel);
  });
}

/**
 * Navega entre telas
 * @param {string} screenName - Nome da tela de destino
 */
function navigateToScreen(screenName) {
  // Esconde todas as telas
  Object.values(elements.screens).forEach((screen) => {
    screen.classList.remove("active");
  });

  // Mostra a tela solicitada
  if (elements.screens[screenName]) {
    elements.screens[screenName].classList.add("active");
    appState.currentScreen = screenName;
  }

  // Foco específico por tela
  setTimeout(() => {
    switch (screenName) {
      case "list":
        if (elements.searchInput) elements.searchInput.focus();
        break;
      case "form":
        // Inicializa categorias quando navega para formulário (se ainda não foi feito)
        if (
          elements.categorySelect &&
          elements.categorySelect.options.length <= 1
        ) {
          initializeCategorySelect();
        }
        if (elements.clientName) elements.clientName.focus();
        break;
    }
  }, 100);
}

// GERENCIAMENTO DA LISTA DE COMANDAS

/**
 * Renderiza a lista de comandas
 * @param {Array} commands - Lista de comandas para renderizar
 */
function renderCommandsList(commands = appState.filteredCommands) {
  const container = elements.commandsList;
  const emptyState = elements.emptyState;

  if (commands.length === 0) {
    container.innerHTML = "";
    emptyState.style.display = "block";
    return;
  }

  emptyState.style.display = "none";

  container.innerHTML = commands
    .map(
      (command) => `
        <div class="command-card" data-id="${command.id}">
            <div class="command-header">
                <div class="command-client">${sanitizeText(
                  command.clientName
                )}</div>
                ${
                  command.tableNumber
                    ? `<div class="command-table">Mesa ${sanitizeText(
                        command.tableNumber
                      )}</div>`
                    : ""
                }
            </div>
            <div class="command-items">
                <span class="command-items-count">${
                  command.items.length
                }</span> 
                ${command.items.length === 1 ? "item" : "itens"}
                ${
                  command.total
                    ? ` • <strong>${formatCurrency(command.total)}</strong>`
                    : ""
                }
            </div>
            <div class="command-time">${formatDateTime(command.createdAt)}</div>
        </div>
    `
    )
    .join("");

  // Adiciona event listeners nos cards
  container.querySelectorAll(".command-card").forEach((card) => {
    card.addEventListener("click", () => {
      const id = parseInt(card.dataset.id);
      viewCommand(id);
    });
  });
}

/**
 * Filtra comandas por termo de busca
 * @param {string} searchTerm - Termo de busca
 */
function filterCommands(searchTerm) {
  const term = searchTerm.toLowerCase().trim();

  if (term === "") {
    appState.filteredCommands = [...appState.commands];
  } else {
    appState.filteredCommands = appState.commands.filter(
      (command) =>
        command.clientName.toLowerCase().includes(term) ||
        (command.tableNumber &&
          command.tableNumber.toLowerCase().includes(term)) ||
        command.items.some((item) => item.text.toLowerCase().includes(term))
    );
  }

  renderCommandsList();
}

/**
 * Carrega e exibe todas as comandas
 */
async function loadCommands() {
  try {
    appState.commands = await getAllCommands();
    appState.filteredCommands = [...appState.commands];
    renderCommandsList();
    updateStats();
  } catch (error) {
    console.error("Erro ao carregar comandas:", error);
    showToast("Erro ao carregar comandas", "error");
  }
}

// GERENCIAMENTO DE PRODUTOS

/**
 * Inicializa o select de categorias
 */
function initializeCategorySelect() {
  if (!elements.categorySelect) return;

  elements.categorySelect.innerHTML =
    '<option value="">Selecione uma categoria</option>';

  Object.keys(CARDAPIO).forEach((categoryKey) => {
    const category = CARDAPIO[categoryKey];
    const option = document.createElement("option");
    option.value = categoryKey;
    option.textContent = category.nome;
    elements.categorySelect.appendChild(option);
  });
}

/**
 * Atualiza lista de produtos baseada na categoria selecionada
 */
function updateProductSelect() {
  if (!elements.categorySelect || !elements.productSelect) return;

  const selectedCategory = elements.categorySelect.value;
  elements.productSelect.innerHTML =
    '<option value="">Selecione um produto</option>';

  if (selectedCategory && CARDAPIO[selectedCategory]) {
    CARDAPIO[selectedCategory].produtos.forEach((produto) => {
      const option = document.createElement("option");
      option.value = produto.id;
      option.textContent = `${produto.nome} - ${formatCurrency(produto.preco)}`;
      option.dataset.price = produto.preco;
      option.dataset.name = produto.nome;
      elements.productSelect.appendChild(option);
    });
  }
}

/**
 * Adiciona produto selecionado à lista de itens
 */
function addSelectedProduct() {
  const categoryKey = elements.categorySelect?.value;
  const productId = elements.productSelect?.value;
  const quantity = parseInt(elements.productQuantity?.value || 1);
  const observation = elements.productObservation?.value.trim();

  if (!categoryKey || !productId || quantity < 1) {
    showToast("Selecione uma categoria, produto e quantidade válida", "error");
    return;
  }

  // Encontrar produto no cardápio
  const category = CARDAPIO[categoryKey];
  const product = category.produtos.find((p) => p.id === productId);

  if (!product) {
    showToast("Produto não encontrado", "error");
    return;
  }

  // Criar item do pedido
  const item = {
    id: generateId(),
    produtoId: product.id,
    nome: product.nome,
    preco: product.preco,
    quantidade: quantity,
    observacao: observation,
    categoria: category.nome,
    subtotal: product.preco * quantity,
  };

  // Se estamos editando, adiciona ao currentCommand
  if (appState.isEditing && appState.currentCommand) {
    appState.currentCommand.items.push(item);
    renderItemsList(appState.currentCommand.items);
    updateOrderTotal(appState.currentCommand.items);
  } else {
    // Para nova comanda, usar lista temporária
    if (!appState.tempItems) appState.tempItems = [];
    appState.tempItems.push(item);
    renderItemsList(appState.tempItems);
    updateOrderTotal(appState.tempItems);
  }

  // Limpar seleção
  elements.productSelect.value = "";
  elements.productQuantity.value = "1";
  elements.productObservation.value = "";

  showToast("Produto adicionado ao pedido", "success");
}

/**
 * Atualiza o total do pedido
 * @param {Array} items - Lista de itens
 */
function updateOrderTotal(items) {
  if (!elements.orderTotal) return;

  const total = calculateTotal(items);
  elements.orderTotal.textContent = formatCurrency(total);
}

// GERENCIAMENTO DE COMANDAS

/**
 * Abre tela para criar nova comanda
 */
function createNewCommand() {
  appState.currentCommand = null;
  appState.isEditing = false;

  elements.formTitle.textContent = "Nova Comanda";
  elements.clientName.value = "";
  elements.tableNumber.value = "";

  // Limpar seleção de produtos
  if (elements.categorySelect) {
    elements.categorySelect.value = "";
    elements.productSelect.innerHTML =
      '<option value="">Selecione uma categoria primeiro</option>';
    elements.productQuantity.value = "1";
    elements.productObservation.value = "";
  }

  // Limpar lista de itens
  elements.itemsList.innerHTML = "";
  elements.newItem.value = "";
  appState.tempItems = [];
  updateOrderTotal([]);

  navigateToScreen("form");
}

/**
 * Atualiza lista de produtos baseada na categoria selecionada
 */
function updateProductSelect() {
  if (!elements.categorySelect || !elements.productSelect) return;

  const selectedCategory = elements.categorySelect.value;
  elements.productSelect.innerHTML =
    '<option value="">Selecione um produto</option>';

  if (selectedCategory && CARDAPIO[selectedCategory]) {
    CARDAPIO[selectedCategory].produtos.forEach((produto) => {
      const option = document.createElement("option");
      option.value = produto.id;
      option.textContent = `${produto.nome} - ${formatCurrency(produto.preco)}`;
      option.dataset.price = produto.preco;
      option.dataset.name = produto.nome;
      elements.productSelect.appendChild(option);
    });
  }
}

/**
 * Adiciona produto selecionado à lista de itens
 */
function addSelectedProduct() {
  const categoryKey = elements.categorySelect?.value;
  const productId = elements.productSelect?.value;
  const quantity = parseInt(elements.productQuantity?.value || 1);
  const observation = elements.productObservation?.value.trim();

  if (!categoryKey || !productId || quantity < 1) {
    showToast("Selecione uma categoria, produto e quantidade válida", "error");
    return;
  }

  // Encontrar produto no cardápio
  const category = CARDAPIO[categoryKey];
  const product = category.produtos.find((p) => p.id === productId);

  if (!product) {
    showToast("Produto não encontrado", "error");
    return;
  }

  // Criar item do pedido
  const item = {
    id: generateId(),
    produtoId: product.id,
    nome: product.nome,
    preco: product.preco,
    quantidade: quantity,
    observacao: observation,
    categoria: category.nome,
    subtotal: product.preco * quantity,
  };

  // Adicionar à lista atual
  const currentItems = getCurrentItems();
  currentItems.push(item);

  // Se estamos editando, adiciona ao currentCommand
  if (appState.isEditing && appState.currentCommand) {
    appState.currentCommand.items = currentItems;
  }

  // Renderizar lista atualizada
  renderItemsList(currentItems);
  updateOrderTotal(currentItems);

  // Limpar seleção
  elements.productSelect.value = "";
  elements.productQuantity.value = "1";
  elements.productObservation.value = "";

  showToast("Produto adicionado ao pedido", "success");
}

/**
 * Atualiza o total do pedido
 * @param {Array} items - Lista de itens
 */
function updateOrderTotal(items) {
  if (!elements.orderTotal) return;

  const total = calculateTotal(items);
  elements.orderTotal.textContent = formatCurrency(total);
}

/**
 * Visualiza uma comanda específica
 * @param {number} id - ID da comanda
 */
async function viewCommand(id) {
  try {
    const command = await getCommand(id);
    if (!command) {
      showToast("Comanda não encontrada", "error");
      return;
    }

    appState.currentCommand = command;
    renderCommandDetails(command);
    navigateToScreen("view");
  } catch (error) {
    console.error("Erro ao carregar comanda:", error);
    showToast("Erro ao carregar comanda", "error");
  }
}

/**
 * Abre comanda para edição
 */
function editCommand() {
  if (!appState.currentCommand) return;

  appState.isEditing = true;

  elements.formTitle.textContent = "Editar Comanda";
  elements.clientName.value = appState.currentCommand.clientName;
  elements.tableNumber.value = appState.currentCommand.tableNumber || "";

  // Limpar seleção de produtos
  if (elements.categorySelect) {
    elements.categorySelect.value = "";
    elements.productSelect.innerHTML =
      '<option value="">Selecione uma categoria primeiro</option>';
    elements.productQuantity.value = "1";
    elements.productObservation.value = "";
  }

  elements.newItem.value = "";

  // Renderizar itens existentes
  renderItemsList(appState.currentCommand.items);
  updateOrderTotal(appState.currentCommand.items);

  navigateToScreen("form");
}

/**
 * Remove uma comanda após confirmação
 */
async function removeCommand() {
  if (!appState.currentCommand) return;

  const confirmed = await showConfirmModal(
    "Excluir Comanda",
    `Tem certeza que deseja excluir a comanda de ${appState.currentCommand.clientName}?`
  );

  if (confirmed) {
    try {
      await deleteCommand(appState.currentCommand.id);
      showToast("Comanda excluída com sucesso", "success");
      await loadCommands();
      navigateToScreen("list");
    } catch (error) {
      console.error("Erro ao excluir comanda:", error);
      showToast("Erro ao excluir comanda", "error");
    }
  }
}

/**
 * Renderiza detalhes de uma comanda
 * @param {Object} command - Dados da comanda
 */
function renderCommandDetails(command) {
  const itemsHtml =
    command.items.length > 0
      ? `<ul class="detail-items-list">
        ${command.items
          .map((item) => {
            if (item.text && !item.nome) {
              // Item antigo (só texto)
              return `<li>${sanitizeText(item.text)}</li>`;
            }
            // Item com estrutura de produto
            const obsText = item.observacao
              ? ` <em>(${sanitizeText(item.observacao)})</em>`
              : "";
            return `<li>
            <div class="detail-item-header">
              <span class="detail-item-name">${sanitizeText(item.nome)}</span>
              <span class="detail-item-price">${formatCurrency(
                item.subtotal
              )}</span>
            </div>
            <div class="detail-item-info">
              ${formatCurrency(item.preco)} × ${item.quantidade}${obsText}
            </div>
          </li>`;
          })
          .join("")}
       </ul>`
      : '<p style="color: #999; font-style: italic;">Nenhum item adicionado</p>';

  elements.commandDetails.innerHTML = `
        <div class="detail-header">
            <div class="detail-client">${sanitizeText(command.clientName)}</div>
            <div class="detail-info">
                ${
                  command.tableNumber
                    ? `<div class="detail-table">🏷️ Mesa ${sanitizeText(
                        command.tableNumber
                      )}</div>`
                    : ""
                }
                <div class="detail-time">🕒 ${formatDateTime(
                  command.createdAt
                )}</div>
            </div>
        </div>
        <div class="detail-items">
            <h3>Itens do Pedido (${command.items.length})</h3>
            ${itemsHtml}
            ${
              command.total
                ? `<div class="detail-total">Total: ${formatCurrency(
                    command.total
                  )}</div>`
                : ""
            }
        </div>
    `;
}

// GERENCIAMENTO DE ITENS

/**
 * Adiciona novo item à lista
 */
function addItem() {
  const itemText = elements.newItem.value.trim();
  if (!itemText) return;

  const item = {
    id: generateId(),
    text: itemText,
  };

  // Se estamos editando, adiciona ao currentCommand
  if (appState.isEditing && appState.currentCommand) {
    appState.currentCommand.items.push(item);
    renderItemsList(appState.currentCommand.items);
    updateOrderTotal(appState.currentCommand.items);
  } else {
    // Senão, adiciona à lista temporária
    if (!appState.tempItems) appState.tempItems = [];
    appState.tempItems.push(item);
    renderItemsList(appState.tempItems);
    updateOrderTotal(appState.tempItems);
  }

  elements.newItem.value = "";
  elements.newItem.focus();
}

/**
 * Edita quantidade de um item
 * @param {string} itemId - ID do item
 */
function editItemQuantity(itemId) {
  const currentItems =
    appState.isEditing && appState.currentCommand
      ? appState.currentCommand.items
      : getCurrentItems();

  const item = currentItems.find((item) => item.id === itemId);
  if (!item || !item.preco) return; // Só funciona para itens com preço

  const newQty = prompt(
    `Alterar quantidade de "${item.nome}"\nQuantidade atual: ${item.quantidade}`,
    item.quantidade
  );
  const quantity = parseInt(newQty);

  if (isNaN(quantity) || quantity < 1) {
    showToast("Quantidade inválida", "error");
    return;
  }

  // Atualizar item
  item.quantidade = quantity;
  item.subtotal = item.preco * quantity;

  // Renderizar lista atualizada
  if (appState.isEditing && appState.currentCommand) {
    renderItemsList(appState.currentCommand.items);
    updateOrderTotal(appState.currentCommand.items);
  } else {
    renderItemsList(appState.tempItems);
    updateOrderTotal(appState.tempItems);
  }
}

/**
 * Remove item da lista
 * @param {string} itemId - ID do item
 */
function removeItem(itemId) {
  if (appState.isEditing && appState.currentCommand) {
    appState.currentCommand.items = appState.currentCommand.items.filter(
      (item) => item.id !== itemId
    );
    renderItemsList(appState.currentCommand.items);
    updateOrderTotal(appState.currentCommand.items);
  } else {
    appState.tempItems = (appState.tempItems || []).filter(
      (item) => item.id !== itemId
    );
    renderItemsList(appState.tempItems);
    updateOrderTotal(appState.tempItems);
  }
}

/**
 * Edita texto de um item
 * @param {string} itemId - ID do item
 * @param {string} newText - Novo texto
 */
function editItem(itemId, newText) {
  if (!newText.trim()) return;

  const currentItems =
    appState.isEditing && appState.currentCommand
      ? appState.currentCommand.items
      : appState.tempItems || [];

  const item = currentItems.find((item) => item.id === itemId);
  if (item && item.text) {
    item.text = newText.trim();
  }

  // Renderizar novamente
  if (appState.isEditing && appState.currentCommand) {
    renderItemsList(appState.currentCommand.items);
  } else {
    renderItemsList(appState.tempItems);
  }
}

/**
 * Obtém itens atuais do formulário
 * @returns {Array}
 */
function getCurrentItems() {
  if (appState.isEditing && appState.currentCommand) {
    return appState.currentCommand.items;
  }

  return appState.tempItems || [];
}

/**
 * Renderiza lista de itens no formulário
 * @param {Array} items - Lista de itens
 */
function renderItemsList(items) {
  if (!items || items.length === 0) {
    elements.itemsList.innerHTML =
      '<p style="color: #999; font-style: italic; text-align: center; padding: 1rem;">Nenhum item adicionado</p>';
    updateOrderTotal([]);
    return;
  }

  elements.itemsList.innerHTML = items
    .map((item) => {
      // Se o item tem estrutura antiga (só texto), converte
      if (item.text && !item.nome) {
        return `
        <div class="item-row" data-id="${item.id}">
          <div class="item-details">
            <div class="item-name" contenteditable="true" data-id="${
              item.id
            }">${sanitizeText(item.text)}</div>
            <div class="item-info">Item personalizado</div>
          </div>
          <div class="item-actions">
            <button type="button" class="btn btn-danger btn-sm remove-item" data-id="${
              item.id
            }" title="Remover item">🗑️</button>
          </div>
        </div>
      `;
      }

      // Item com estrutura de produto
      const observacaoHtml = item.observacao
        ? `<div class="item-observation">Obs: ${sanitizeText(
            item.observacao
          )}</div>`
        : "";

      return `
      <div class="item-row product-item" data-id="${item.id}">
        <div class="item-details">
          <div class="item-header">
            <div class="item-name">${sanitizeText(item.nome)}</div>
            <div class="item-subtotal">${formatCurrency(item.subtotal)}</div>
          </div>
          <div class="item-info">
            <span class="item-category">${sanitizeText(item.categoria)}</span>
            <span class="item-price-qty">${formatCurrency(item.preco)} × ${
        item.quantidade
      }</span>
          </div>
          ${observacaoHtml}
        </div>
        <div class="item-actions">
          <button type="button" class="btn btn-secondary btn-sm edit-qty" data-id="${
            item.id
          }" title="Alterar quantidade">📝</button>
          <button type="button" class="btn btn-danger btn-sm remove-item" data-id="${
            item.id
          }" title="Remover item">🗑️</button>
        </div>
      </div>
    `;
    })
    .join("");

  // Event listeners para edição inline (itens antigos)
  elements.itemsList
    .querySelectorAll('[contenteditable="true"]')
    .forEach((element) => {
      element.addEventListener("blur", (e) => {
        const itemId = e.target.dataset.id;
        const newText = e.target.textContent.trim();
        if (newText) {
          editItem(itemId, newText);
        }
      });

      element.addEventListener("keypress", (e) => {
        if (e.key === "Enter") {
          e.preventDefault();
          e.target.blur();
        }
      });
    });

  // Event listeners para remoção
  elements.itemsList.querySelectorAll(".remove-item").forEach((button) => {
    button.addEventListener("click", (e) => {
      const itemId = e.target.dataset.id;
      removeItem(itemId);
    });
  });

  // Event listeners para edição de quantidade
  elements.itemsList.querySelectorAll(".edit-qty").forEach((button) => {
    button.addEventListener("click", (e) => {
      const itemId = e.target.dataset.id;
      editItemQuantity(itemId);
    });
  });

  // Atualizar total após renderizar
  updateOrderTotal(items);
}

// FORMULÁRIO DE COMANDA

/**
 * Manipula submissão do formulário
 * @param {Event} e - Evento do formulário
 */
async function handleFormSubmit(e) {
  e.preventDefault();

  const clientName = elements.clientName.value.trim();
  const tableNumber = elements.tableNumber.value.trim();
  const items = getCurrentItems();

  if (!clientName) {
    showToast("Nome do cliente é obrigatório", "error");
    elements.clientName.focus();
    return;
  }

  if (items.length === 0) {
    showToast("Adicione pelo menos um item ao pedido", "error");
    return;
  }

  // Calcular total do pedido
  const totalPedido = calculateTotal(items);

  const command = {
    clientName,
    tableNumber: tableNumber || null,
    items,
    total: totalPedido,
    createdAt: appState.isEditing
      ? appState.currentCommand.createdAt
      : new Date().toISOString(),
    updatedAt: new Date().toISOString(),
  };

  // Se estamos editando, mantém o ID
  if (appState.isEditing && appState.currentCommand) {
    command.id = appState.currentCommand.id;
  }

  try {
    await saveCommand(command);
    const message = appState.isEditing
      ? "Comanda atualizada com sucesso"
      : "Comanda criada com sucesso";
    showToast(message, "success");

    // Limpar lista temporária
    appState.tempItems = [];

    await loadCommands();
    navigateToScreen("list");
  } catch (error) {
    console.error("Erro ao salvar comanda:", error);
    showToast("Erro ao salvar comanda", "error");
  }
}

// FUNCIONALIDADE WHATSAPP

/**
 * Copia comanda formatada para área de transferência
 */
async function copyCommandToClipboard() {
  if (!appState.currentCommand) return;

  const command = appState.currentCommand;
  let text = `Cliente: ${command.clientName}\n`;

  if (command.tableNumber) {
    text += `Mesa: ${command.tableNumber}\n`;
  }

  text += `Pedido:\n`;

  if (command.items.length > 0) {
    command.items.forEach((item) => {
      if (item.text && !item.nome) {
        // Item antigo
        text += `- ${item.text}\n`;
      } else {
        // Item com preço
        text += `- ${item.quantidade}x ${item.nome} - ${formatCurrency(
          item.subtotal
        )}\n`;
        if (item.observacao) {
          text += `  Obs: ${item.observacao}\n`;
        }
      }
    });

    if (command.total) {
      text += `\nTotal: ${formatCurrency(command.total)}\n`;
    }
  } else {
    text += `- Nenhum item\n`;
  }

  text += `\nHorário: ${formatDateTime(command.createdAt)}`;

  try {
    await navigator.clipboard.writeText(text);
    showToast("Pedido copiado para área de transferência!", "success");
  } catch (error) {
    console.error("Erro ao copiar:", error);

    // Fallback para navegadores mais antigos
    const textArea = document.createElement("textarea");
    textArea.value = text;
    textArea.style.position = "fixed";
    textArea.style.left = "-999999px";
    textArea.style.top = "-999999px";
    document.body.appendChild(textArea);
    textArea.focus();
    textArea.select();

    try {
      document.execCommand("copy");
      showToast("Pedido copiado para área de transferência!", "success");
    } catch (fallbackError) {
      showToast("Não foi possível copiar. Tente manualmente.", "error");
    }

    document.body.removeChild(textArea);
  }
}

// CONFIGURAÇÕES E ESTATÍSTICAS

/**
 * Atualiza estatísticas na tela de configurações
 */
function updateStats() {
  elements.totalCommands.textContent = appState.commands.length;
  elements.todayCommands.textContent = countTodayCommands(appState.commands);
}

/**
 * Remove todas as comandas após confirmação
 */
async function deleteAllCommandsConfirm() {
  const confirmed = await showConfirmModal(
    "Apagar Todas as Comandas",
    "Esta ação não pode ser desfeita! Tem certeza que deseja apagar todas as comandas?"
  );

  if (confirmed) {
    try {
      await deleteAllCommands();
      showToast("Todas as comandas foram apagadas", "success");
      await loadCommands();
      navigateToScreen("list");
    } catch (error) {
      console.error("Erro ao apagar comandas:", error);
      showToast("Erro ao apagar comandas", "error");
    }
  }
}

// EVENT LISTENERS

/**
 * Configura todos os event listeners da aplicação
 */
function setupEventListeners() {
  // Navegação
  elements.settingsBtn?.addEventListener("click", () => {
    updateStats();
    navigateToScreen("settings");
  });

  elements.backFromFormBtn?.addEventListener("click", () =>
    navigateToScreen("list")
  );
  elements.backFromViewBtn?.addEventListener("click", () =>
    navigateToScreen("list")
  );
  elements.backFromSettingsBtn?.addEventListener("click", () =>
    navigateToScreen("list")
  );

  // Lista de comandas
  elements.newCommandBtn?.addEventListener("click", createNewCommand);

  // Busca com debounce
  if (elements.searchInput) {
    const debouncedFilter = debounce((e) => {
      filterCommands(e.target.value);
    }, CONFIG.debounceDelay);

    elements.searchInput.addEventListener("input", debouncedFilter);
  }

  // Formulário
  elements.commandForm?.addEventListener("submit", handleFormSubmit);
  elements.addItemBtn?.addEventListener("click", addItem);

  // Seleção de produtos
  elements.categorySelect?.addEventListener("change", updateProductSelect);
  elements.addProductBtn?.addEventListener("click", addSelectedProduct);

  // Permite adicionar item com Enter
  elements.newItem?.addEventListener("keypress", (e) => {
    if (e.key === "Enter") {
      e.preventDefault();
      addItem();
    }
  });

  // Visualização de comanda
  elements.editCommandBtn?.addEventListener("click", editCommand);
  elements.deleteCommandBtn?.addEventListener("click", removeCommand);
  elements.copyCommandBtn?.addEventListener("click", copyCommandToClipboard);

  // Configurações
  elements.deleteAllBtn?.addEventListener("click", deleteAllCommandsConfirm);

  // Modal (fechar clicando no overlay)
  elements.overlay?.addEventListener("click", (e) => {
    if (e.target === elements.overlay) {
      elements.overlay.classList.remove("active");
    }
  });

  // Tecla ESC para fechar modal
  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape" && elements.overlay.classList.contains("active")) {
      elements.overlay.classList.remove("active");
    }
  });
}

// INICIALIZAÇÃO

/**
 * Inicializa a aplicação
 */
async function initApp() {
  try {
    console.log("Iniciando aplicação...");

    // Inicializa banco de dados
    await initDB();
    console.log("Banco de dados inicializado");

    // Configura event listeners
    setupEventListeners();
    console.log("Event listeners configurados");

    // Carrega comandas
    await loadCommands();
    console.log("Comandas carregadas");

    // Mostra tela inicial
    navigateToScreen("list");

    console.log("Aplicação iniciada com sucesso");
  } catch (error) {
    console.error("Erro ao inicializar aplicação:", error);
    showToast("Erro ao inicializar aplicação. Recarregue a página.", "error");
  }
}

// SERVICE WORKER

/**
 * Registra o service worker para funcionalidade PWA
 */
async function registerServiceWorker() {
  if ("serviceWorker" in navigator) {
    try {
      const registration = await navigator.serviceWorker.register("./sw.js");
      console.log("Service Worker registrado:", registration);
    } catch (error) {
      console.error("Erro ao registrar Service Worker:", error);
    }
  }
}

// INICIALIZAÇÃO DA APLICAÇÃO

// Aguarda DOM ser carregado completamente
document.addEventListener("DOMContentLoaded", async () => {
  await initApp();
  await registerServiceWorker();
});

// Previne zoom no iOS em inputs
document.addEventListener("touchstart", (e) => {
  if (e.touches.length > 1) {
    e.preventDefault();
  }
});

// Melhora experiência em dispositivos móveis
let lastTouchEnd = 0;
document.addEventListener(
  "touchend",
  (e) => {
    const now = new Date().getTime();
    if (now - lastTouchEnd <= 300) {
      e.preventDefault();
    }
    lastTouchEnd = now;
  },
  false
);

// Exporta funções para debug (apenas em desenvolvimento)
if (
  window.location.hostname === "localhost" ||
  window.location.hostname === "127.0.0.1"
) {
  window.ComandaApp = {
    appState,
    loadCommands,
    initDB,
    CONFIG,
  };
}
