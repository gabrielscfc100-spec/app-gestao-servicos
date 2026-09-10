from pathlib import Path

path = Path('index.html')
text = path.read_text(encoding='utf-8')
marker = 'simpla-pwa-update-manager-v1'
if marker in text:
    raise SystemExit('patch already applied')

insert = r'''
<style id="simpla-pwa-update-manager-v1">
.simpla-update-banner{position:fixed;left:50%;bottom:22px;transform:translateX(-50%);z-index:3000;width:min(560px,calc(100vw - 28px));background:#1f3b56;color:#fff;border-radius:12px;box-shadow:0 14px 38px rgba(0,0,0,.28);padding:14px 16px;display:none;align-items:center;justify-content:space-between;gap:14px;text-transform:none!important}
.simpla-update-banner.show{display:flex}
.simpla-update-banner *{text-transform:none!important}
.simpla-update-texto{min-width:0;line-height:1.35}
.simpla-update-texto strong{display:block;font-size:14px;margin-bottom:3px}
.simpla-update-texto span{display:block;font-size:12px;opacity:.9}
.simpla-update-btn{border:0;border-radius:8px;background:#fff;color:#1f3b56;font-weight:700;font-size:12px;padding:10px 13px;white-space:nowrap;cursor:pointer}
@media(max-width:520px){.simpla-update-banner{bottom:14px;align-items:stretch;flex-direction:column}.simpla-update-btn{width:100%;font-size:13px}}
</style>
<script>
(function simplaGerenciadorAtualizacaoPWA(){
  if(!('serviceWorker' in navigator)) return;

  let registroPWA = null;
  let recarregando = false;

  function obterBanner(){
    let banner = document.getElementById('simpla-update-banner');
    if(banner) return banner;
    banner = document.createElement('div');
    banner.id = 'simpla-update-banner';
    banner.className = 'simpla-update-banner';
    banner.setAttribute('role','status');
    banner.setAttribute('aria-live','polite');
    banner.innerHTML = '<div class="simpla-update-texto"><strong>Nova versão do SimplA disponível</strong><span>Atualize agora para receber as correções e melhorias mais recentes.</span></div><button type="button" class="simpla-update-btn" id="simpla-update-btn">Atualizar agora</button>';
    document.body.appendChild(banner);
    banner.querySelector('#simpla-update-btn').addEventListener('click', aplicarAtualizacao);
    return banner;
  }

  function mostrarAtualizacao(){
    const banner = obterBanner();
    banner.classList.add('show');
  }

  function aplicarAtualizacao(){
    const worker = registroPWA?.waiting;
    if(worker){
      const btn = document.getElementById('simpla-update-btn');
      if(btn){ btn.disabled = true; btn.textContent = 'Atualizando...'; }
      worker.postMessage({tipo:'SKIP_WAITING'});
      return;
    }
    window.location.reload();
  }

  function observarInstalacao(registro){
    if(registro.waiting && navigator.serviceWorker.controller) mostrarAtualizacao();
    registro.addEventListener('updatefound', () => {
      const novo = registro.installing;
      if(!novo) return;
      novo.addEventListener('statechange', () => {
        if(novo.state === 'installed' && navigator.serviceWorker.controller){
          mostrarAtualizacao();
        }
      });
    });
  }

  navigator.serviceWorker.addEventListener('controllerchange', () => {
    if(recarregando) return;
    recarregando = true;
    window.location.reload();
  });

  window.addEventListener('load', async () => {
    try{
      registroPWA = await navigator.serviceWorker.getRegistration('./') || await navigator.serviceWorker.register('./service-worker.js', {scope:'./'});
      observarInstalacao(registroPWA);
      await registroPWA.update().catch(()=>{});

      // Verifica novamente enquanto o app fica aberto.
      setInterval(() => registroPWA?.update().catch(()=>{}), 5 * 60 * 1000);

      // Ao retornar para o app no iPhone/PWA, força nova verificação.
      document.addEventListener('visibilitychange', () => {
        if(document.visibilityState === 'visible') registroPWA?.update().catch(()=>{});
      });
    }catch(err){
      console.warn('SimplA PWA: falha ao verificar atualização.', err);
    }
  });
})();
</script>
'''

if '</body>' not in text:
    raise SystemExit('body closing tag not found')
text = text.replace('</body>', insert + '\n</body>', 1)
path.write_text(text, encoding='utf-8')
print('patched', marker)
