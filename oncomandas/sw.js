/**
 * Service Worker para Sistema de Comandas PWA
 * Versão: 1.0.0
 * Funcionalidades: Cache offline, estratégias de cache, background sync
 */

"use strict";

// CONFIGURAÇÕES DO SERVICE WORKER

const SW_VERSION = "1.0.0";
const CACHE_NAME = `comandas-cache-v${SW_VERSION}`;
const DATA_CACHE_NAME = `comandas-data-cache-v${SW_VERSION}`;

// Arquivos essenciais que devem estar sempre em cache
const CORE_CACHE_FILES = [
  "./",
  "./index.html",
  "./styles.css",
  "./app.js",
  "./manifest.json",
];

// Recursos que podem ser armazenados em cache conforme necessário
const EXTENDED_CACHE_FILES = [
  // Fontes do sistema são carregadas automaticamente
  // Não incluímos arquivos externos para manter o app offline-first
];

// Configurações de cache
const CACHE_CONFIG = {
  maxAge: 30 * 24 * 60 * 60 * 1000, // 30 dias em ms
  maxEntries: 100,
  networkTimeoutSeconds: 3,
};

// EVENTOS DO SERVICE WORKER

/**
 * Evento de instalação do Service Worker
 * Faz o cache inicial dos recursos essenciais
 */
self.addEventListener("install", (event) => {
  console.log(`[SW] Instalando Service Worker v${SW_VERSION}`);

  event.waitUntil(
    caches
      .open(CACHE_NAME)
      .then((cache) => {
        console.log("[SW] Fazendo cache dos arquivos essenciais");
        return cache.addAll(CORE_CACHE_FILES);
      })
      .then(() => {
        console.log("[SW] Cache inicial criado com sucesso");
        // Força ativação imediata
        return self.skipWaiting();
      })
      .catch((error) => {
        console.error("[SW] Erro ao criar cache inicial:", error);
      })
  );
});

/**
 * Evento de ativação do Service Worker
 * Limpa caches antigos e assume controle
 */
self.addEventListener("activate", (event) => {
  console.log(`[SW] Ativando Service Worker v${SW_VERSION}`);

  event.waitUntil(
    caches
      .keys()
      .then((cacheNames) => {
        return Promise.all(
          cacheNames.map((cacheName) => {
            // Remove caches antigos
            if (cacheName !== CACHE_NAME && cacheName !== DATA_CACHE_NAME) {
              console.log("[SW] Removendo cache antigo:", cacheName);
              return caches.delete(cacheName);
            }
          })
        );
      })
      .then(() => {
        console.log("[SW] Service Worker ativado e assumiu controle");
        // Assume controle imediato de todas as páginas
        return self.clients.claim();
      })
      .catch((error) => {
        console.error("[SW] Erro na ativação:", error);
      })
  );
});

/**
 * Intercepta requisições de rede
 * Implementa estratégias de cache offline-first
 */
self.addEventListener("fetch", (event) => {
  const { request } = event;
  const url = new URL(request.url);

  // Ignora requisições não-HTTP
  if (!url.protocol.startsWith("http")) {
    return;
  }

  // Ignora requisições para outros domínios (se houver)
  if (url.origin !== location.origin) {
    return;
  }

  // Estratégia: Cache First para recursos estáticos
  if (isStaticResource(request)) {
    event.respondWith(cacheFirst(request));
    return;
  }

  // Estratégia: Network First para dados dinâmicos
  if (isDynamicRequest(request)) {
    event.respondWith(networkFirst(request));
    return;
  }

  // Estratégia padrão: Cache First
  event.respondWith(cacheFirst(request));
});

/**
 * Manipula mensagens do cliente (app principal)
 */
self.addEventListener("message", (event) => {
  const { data } = event;

  switch (data.type) {
    case "SKIP_WAITING":
      console.log("[SW] Recebida mensagem para pular espera");
      self.skipWaiting();
      break;

    case "CACHE_STATS":
      getCacheStats().then((stats) => {
        event.ports[0].postMessage({
          type: "CACHE_STATS_RESPONSE",
          data: stats,
        });
      });
      break;

    case "CLEAR_CACHE":
      clearAllCaches().then((success) => {
        event.ports[0].postMessage({
          type: "CLEAR_CACHE_RESPONSE",
          data: { success },
        });
      });
      break;

    default:
      console.log("[SW] Mensagem não reconhecida:", data.type);
  }
});

/**
 * Manipula sincronização em background (se suportado)
 */
self.addEventListener("sync", (event) => {
  console.log("[SW] Evento de sincronização:", event.tag);

  switch (event.tag) {
    case "background-sync":
      event.waitUntil(handleBackgroundSync());
      break;
  }
});

// ESTRATÉGIAS DE CACHE

/**
 * Estratégia Cache First
 * Tenta cache primeiro, depois rede como fallback
 * Ideal para recursos estáticos
 */
async function cacheFirst(request) {
  try {
    // Tenta buscar do cache primeiro
    const cachedResponse = await caches.match(request);
    if (cachedResponse) {
      console.log("[SW] Servindo do cache:", request.url);
      return cachedResponse;
    }

    // Se não estiver em cache, busca da rede
    console.log("[SW] Não encontrado no cache, buscando da rede:", request.url);
    const networkResponse = await fetchWithTimeout(request);

    // Salva no cache para próximas requisições
    if (networkResponse && networkResponse.status === 200) {
      const cache = await caches.open(CACHE_NAME);
      cache.put(request, networkResponse.clone());
    }

    return networkResponse;
  } catch (error) {
    console.error("[SW] Cache First falhou:", error);

    // Se tudo falhar e for uma navegação, retorna página offline
    if (request.destination === "document") {
      return getOfflinePage();
    }

    throw error;
  }
}

/**
 * Estratégia Network First
 * Tenta rede primeiro, cache como fallback
 * Ideal para dados dinâmicos
 */
async function networkFirst(request) {
  try {
    // Tenta buscar da rede primeiro
    console.log("[SW] Tentando rede primeiro:", request.url);
    const networkResponse = await fetchWithTimeout(request);

    // Se sucesso, atualiza cache e retorna
    if (networkResponse && networkResponse.status === 200) {
      const cache = await caches.open(DATA_CACHE_NAME);
      cache.put(request, networkResponse.clone());
      return networkResponse;
    }

    throw new Error("Resposta da rede inválida");
  } catch (error) {
    console.log("[SW] Rede falhou, tentando cache:", error.message);

    // Se rede falhar, tenta cache
    const cachedResponse = await caches.match(request);
    if (cachedResponse) {
      console.log("[SW] Servindo do cache como fallback:", request.url);
      return cachedResponse;
    }

    // Se tudo falhar
    console.error("[SW] Network First falhou completamente:", error);
    throw error;
  }
}

// FUNÇÕES AUXILIARES

/**
 * Determina se uma requisição é para recurso estático
 */
function isStaticResource(request) {
  const url = new URL(request.url);
  const pathname = url.pathname;

  return (
    pathname.endsWith(".css") ||
    pathname.endsWith(".js") ||
    pathname.endsWith(".html") ||
    pathname.endsWith(".json") ||
    pathname === "./" ||
    pathname === "/index.html"
  );
}

/**
 * Determina se uma requisição é dinâmica
 */
function isDynamicRequest(request) {
  // Para este app, todas as requisições são para recursos estáticos
  // Em futuras versões, isso pode incluir APIs
  return false;
}

/**
 * Fetch com timeout personalizado
 */
function fetchWithTimeout(
  request,
  timeout = CACHE_CONFIG.networkTimeoutSeconds * 1000
) {
  return new Promise((resolve, reject) => {
    const timeoutId = setTimeout(() => {
      reject(new Error(`Timeout de ${timeout}ms excedido`));
    }, timeout);

    fetch(request)
      .then((response) => {
        clearTimeout(timeoutId);
        resolve(response);
      })
      .catch((error) => {
        clearTimeout(timeoutId);
        reject(error);
      });
  });
}

/**
 * Retorna página offline básica
 */
async function getOfflinePage() {
  const offlineHtml = `
    <!DOCTYPE html>
    <html lang="pt-BR">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Offline - Comandas</title>
        <style>
            body {
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Arial, sans-serif;
                margin: 0;
                padding: 2rem;
                background-color: #f5f5f5;
                color: #333;
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
                min-height: 100vh;
                text-align: center;
            }
            .offline-icon {
                font-size: 4rem;
                margin-bottom: 1rem;
            }
            h1 {
                color: #2196F3;
                margin-bottom: 0.5rem;
            }
            p {
                color: #666;
                margin-bottom: 2rem;
                max-width: 400px;
            }
            .btn {
                background: #2196F3;
                color: white;
                padding: 1rem 2rem;
                border: none;
                border-radius: 8px;
                cursor: pointer;
                font-size: 1rem;
                text-decoration: none;
                display: inline-block;
            }
            .btn:hover {
                background: #1976D2;
            }
        </style>
    </head>
    <body>
        <div class="offline-icon">📋</div>
        <h1>App funcionando offline</h1>
        <p>Você está offline, mas pode continuar usando o app. Suas comandas são salvas localmente e estarão disponíveis quando voltar online.</p>
        <a href="./" class="btn">Ir para o App</a>
        
        <script>
            // Recarrega quando voltar online
            window.addEventListener('online', () => {
                window.location.href = './';
            });
        </script>
    </body>
    </html>
    `;

  return new Response(offlineHtml, {
    headers: {
      "Content-Type": "text/html; charset=utf-8",
    },
  });
}

/**
 * Obtém estatísticas do cache
 */
async function getCacheStats() {
  try {
    const cacheNames = await caches.keys();
    const stats = {
      version: SW_VERSION,
      caches: [],
      totalSize: 0,
    };

    for (const cacheName of cacheNames) {
      const cache = await caches.open(cacheName);
      const keys = await cache.keys();

      stats.caches.push({
        name: cacheName,
        entries: keys.length,
      });
    }

    return stats;
  } catch (error) {
    console.error("[SW] Erro ao obter estatísticas do cache:", error);
    return { error: error.message };
  }
}

/**
 * Limpa todos os caches
 */
async function clearAllCaches() {
  try {
    const cacheNames = await caches.keys();
    await Promise.all(cacheNames.map((cacheName) => caches.delete(cacheName)));
    console.log("[SW] Todos os caches foram limpos");
    return true;
  } catch (error) {
    console.error("[SW] Erro ao limpar caches:", error);
    return false;
  }
}

/**
 * Manipula sincronização em background
 */
async function handleBackgroundSync() {
  console.log("[SW] Executando sincronização em background");

  try {
    // Aqui poderíamos implementar:
    // - Sincronização de dados com servidor (quando houver)
    // - Limpeza de dados antigos
    // - Otimização do cache

    // Por enquanto, apenas registra o evento
    console.log("[SW] Sincronização em background concluída");
  } catch (error) {
    console.error("[SW] Erro na sincronização em background:", error);
    throw error;
  }
}

/**
 * Registra sincronização em background (se suportado)
 */
function requestBackgroundSync() {
  if (
    "serviceWorker" in navigator &&
    "sync" in window.ServiceWorkerRegistration.prototype
  ) {
    navigator.serviceWorker.ready
      .then((registration) => {
        return registration.sync.register("background-sync");
      })
      .catch((error) => {
        console.error("[SW] Erro ao registrar background sync:", error);
      });
  }
}

// LOGS E DEBUGGING

// Log quando o SW é carregado
console.log(`[SW] Service Worker v${SW_VERSION} carregado`);

// Intercepta erros não tratados
self.addEventListener("error", (event) => {
  console.error("[SW] Erro não tratado:", event.error);
});

// Intercepta promises rejeitadas
self.addEventListener("unhandledrejection", (event) => {
  console.error("[SW] Promise rejeitada não tratada:", event.reason);
  event.preventDefault();
});
