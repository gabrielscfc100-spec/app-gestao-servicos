// SimplA Service Worker — Fundação PWA v1
const CACHE_VERSION = 'simpla-shell-v2-notificacoes';
const OFFLINE_URL = './offline.html';

const APP_SHELL = [
  './',
  './index.html',
  './manifest.webmanifest',
  './offline.html',
  './icons/icon-180.png',
  './icons/icon-192.png',
  './icons/icon-512.png',
  './icons/icon-maskable-512.png'
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
// PUSH — cada evento é tratado como notificação independente.
// Evita que dois novos agendamentos sejam fundidos/substituídos.
// -----------------------------------------------------------
self.addEventListener('push', event => {
  event.waitUntil((async () => {
    let payload = {};
    try {
      payload = event.data ? event.data.json() : {};
    } catch (err) {
      try {
        payload = { mensagem: event.data ? event.data.text() : '' };
      } catch (_) {
        payload = {};
      }
    }

    const notificacaoId = String(payload.notificacao_id || `${Date.now()}-${Math.random()}`);
    const titulo = payload.titulo || 'SimplA';
    const mensagem = payload.mensagem || 'Você recebeu uma nova notificação.';
    const url = payload.url || './';

    await self.registration.showNotification(titulo, {
      body: mensagem,
      icon: payload.icon || './icons/icon-192.png',
      badge: payload.badge || './icons/icon-192.png',
      tag: `simpla-${notificacaoId}`,
      renotify: true,
      data: {
        url,
        notificacao_id: payload.notificacao_id || null,
        agendamento_id: payload.agendamento_id || null,
        tipo: payload.tipo || 'GERAL'
      }
    });
  })());
});

self.addEventListener('notificationclick', event => {
  event.notification.close();

  event.waitUntil((async () => {
    const destino = event.notification?.data?.url || './';
    const janelas = await clients.matchAll({
      type: 'window',
      includeUncontrolled: true
    });

    for (const janela of janelas) {
      if('focus' in janela) {
        try {
          if('navigate' in janela) await janela.navigate(destino);
        } catch (_) {}
        await janela.focus();
        return;
      }
    }

    if(clients.openWindow) {
      await clients.openWindow(destino);
    }
  })());
});
