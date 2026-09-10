const SOURCE_URL = 'https://raw.githubusercontent.com/gabrielscfc100-spec/app-gestao-servicos/main/agendar.html';

export default {
  async fetch(request) {
    const url = new URL(request.url);

    if (request.method !== 'GET' && request.method !== 'HEAD') {
      return new Response('Method Not Allowed', { status: 405 });
    }

    if (url.pathname === '/favicon.ico') {
      return new Response(null, { status: 204 });
    }

    try {
      const response = await fetch(SOURCE_URL, {
        cf: { cacheTtl: 60, cacheEverything: true }
      });

      if (!response.ok) {
        return new Response('Agendamento temporariamente indisponível.', {
          status: 503,
          headers: { 'content-type': 'text/plain; charset=utf-8' }
        });
      }

      const html = await response.text();
      return new Response(request.method === 'HEAD' ? null : html, {
        status: 200,
        headers: {
          'content-type': 'text/html; charset=utf-8',
          'cache-control': 'public, max-age=60',
          'x-content-type-options': 'nosniff',
          'referrer-policy': 'strict-origin-when-cross-origin'
        }
      });
    } catch (error) {
      return new Response('Agendamento temporariamente indisponível.', {
        status: 503,
        headers: { 'content-type': 'text/plain; charset=utf-8' }
      });
    }
  }
};
