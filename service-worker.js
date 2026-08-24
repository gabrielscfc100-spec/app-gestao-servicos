// SimplA Service Worker — Web Push v1
const CACHE_VERSION = 'simpla-shell-v3';
const OFFLINE_URL = './offline.html';

const APP_SHELL = [
  './',
  './index.html',
  './manifest.webmanifest',
  './offline.html',
  './icons/icon-180.png',
  './icons/icon-192.png',
  './icons/icon-512.png',
  './icons/icon-maskable-512.png',
  './icons/logo-pwa.png'
];

self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_VERSION)
      .then(cache => cache.addAll(APP_SHELL))
      .then(() => self.skipWaiting())
  );
});

self.addEventListener('activate', event => {
  event.waitUntil(
    caches.keys()
      .then(keys => Promise.all(
        keys
          .filter(key => key.startsWith('simpla-') && key !== CACHE_VERSION)
          .map(key => caches.delete(key))
      ))
      .then(() => self.clients.claim())
  );
});

self.addEventListener('fetch', event => {
  const request = event.request;
  const url = new URL(request.url);

  if(request.method !== 'GET') return;

  // Nunca intercepta Supabase, APIs ou CDNs externas.
  if(url.origin !== self.location.origin) return;

  // HTML/navegação: prioriza sempre a versão mais nova da rede.
  if(request.mode === 'navigate') {
    event.respondWith(
      fetch(request)
        .then(response => {
          const copia = response.clone();
          caches.open(CACHE_VERSION).then(cache => cache.put(request, copia));
          return response;
        })
        .catch(async () => {
          return (await caches.match(request))
            || (await caches.match('./index.html'))
            || (await caches.match(OFFLINE_URL));
        })
    );
    return;
  }

  // Assets locais: cache primeiro, rede como fallback.
  event.respondWith(
    caches.match(request).then(cached => {
      if(cached) return cached;
      return fetch(request).then(response => {
        if(response && response.ok) {
          const copia = response.clone();
          caches.open(CACHE_VERSION).then(cache => cache.put(request, copia));
        }
        return response;
      });
    })
  );
});

self.addEventListener('message', event => {
  if(event.data === 'SKIP_WAITING') self.skipWaiting();
});


// -----------------------------------------------------------
// WEB PUSH
// -----------------------------------------------------------
self.addEventListener('push', event => {
  let payload = {};

  try {
    payload = event.data ? event.data.json() : {};
  } catch(e) {
    payload = {
      titulo: 'SimplA',
      mensagem: event.data ? event.data.text() : 'Você recebeu uma nova notificação.'
    };
  }

  const titulo = payload.titulo || payload.title || 'SimplA';
  const mensagem = payload.mensagem || payload.body || 'Você recebeu uma nova notificação.';

  const options = {
    body: mensagem,
    icon: payload.icon || './icons/icon-192.png',
    badge: payload.badge || './icons/icon-192.png',
    tag: payload.tag || (payload.notificacao_id ? `simpla-${payload.notificacao_id}` : undefined),
    renotify: !!payload.renotify,
    data: {
      url: payload.url || './',
      notificacao_id: payload.notificacao_id || null,
      agendamento_id: payload.agendamento_id || null
    }
  };

  event.waitUntil(self.registration.showNotification(titulo, options));
});

self.addEventListener('notificationclick', event => {
  event.notification.close();

  const destino = event.notification?.data?.url || './';
  const destinoAbsoluto = new URL(destino, self.registration.scope).href;

  event.waitUntil(
    clients.matchAll({ type:'window', includeUncontrolled:true }).then(janelas => {
      for(const janela of janelas) {
        if('focus' in janela) {
          try {
            janela.navigate(destinoAbsoluto);
          } catch(e) {}
          return janela.focus();
        }
      }
      return clients.openWindow ? clients.openWindow(destinoAbsoluto) : undefined;
    })
  );
});
