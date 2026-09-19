from pathlib import Path
import re

idx=Path('index.html')
sw=Path('service-worker.js')
html=idx.read_text(encoding='utf-8')
swtxt=sw.read_text(encoding='utf-8')

old_manager=re.search(r'<script>\s*\(function simplaGerenciadorAtualizacaoPWA\(\)\{.*?</script>',html,re.S)
if not old_manager:
    raise SystemExit('gerenciador PWA nao encontrado')

new_manager=r'''<script>
(function simplaGerenciadorAtualizacaoPWA(){
  if(!('serviceWorker' in navigator)) return;

  const STORAGE_KEY='simpla_pwa_update_aplicado';
  let registroPWA=null;
  let recarregando=false;
  let versaoEmEspera=null;

  try{
    const u=new URL(window.location.href);
    if(u.searchParams.has('_simpla_update')){
      u.searchParams.delete('_simpla_update');
      history.replaceState(null,'',u.pathname+u.search+u.hash);
    }
  }catch(_){}

  function obterBanner(){
    let banner=document.getElementById('simpla-update-banner');
    if(banner) return banner;
    banner=document.createElement('div');
    banner.id='simpla-update-banner';
    banner.className='simpla-update-banner';
    banner.setAttribute('role','status');
    banner.setAttribute('aria-live','polite');
    banner.innerHTML='<div class="simpla-update-texto"><strong>Nova versão do SimplA disponível</strong><span>Atualize agora para receber as correções e melhorias mais recentes.</span></div><button type="button" class="simpla-update-btn" id="simpla-update-btn">Atualizar agora</button>';
    document.body.appendChild(banner);
    banner.querySelector('#simpla-update-btn').addEventListener('click',aplicarAtualizacao);
    return banner;
  }

  function esconderAtualizacao(){
    const banner=document.getElementById('simpla-update-banner');
    if(banner) banner.classList.remove('show');
  }

  function obterVersaoWorker(worker){
    return new Promise(resolve=>{
      if(!worker) return resolve(null);
      try{
        const canal=new MessageChannel();
        const timer=setTimeout(()=>resolve(null),1200);
        canal.port1.onmessage=e=>{
          clearTimeout(timer);
          resolve(e?.data?.versao||null);
        };
        worker.postMessage({tipo:'GET_VERSION'},[canal.port2]);
      }catch(_){resolve(null)}
    });
  }

  async function avaliarWaiting(registro){
    const waiting=registro?.waiting;
    if(!waiting || !navigator.serviceWorker.controller){
      esconderAtualizacao();
      return;
    }

    const [vWaiting,vAtiva]=await Promise.all([
      obterVersaoWorker(waiting),
      obterVersaoWorker(navigator.serviceWorker.controller)
    ]);

    versaoEmEspera=vWaiting||null;
    const jaAplicada=localStorage.getItem(STORAGE_KEY);

    if(vWaiting && vAtiva && vWaiting===vAtiva){
      esconderAtualizacao();
      return;
    }

    if(vWaiting && jaAplicada===vWaiting){
      esconderAtualizacao();
      waiting.postMessage({tipo:'SKIP_WAITING'});
      return;
    }

    obterBanner().classList.add('show');
  }

  async function aplicarAtualizacao(){
    const btn=document.getElementById('simpla-update-btn');
    if(btn){btn.disabled=true;btn.textContent='Aplicando atualização...';}

    const worker=registroPWA?.waiting;
    if(worker){
      const alvo=versaoEmEspera || await obterVersaoWorker(worker);
      if(alvo) localStorage.setItem(STORAGE_KEY,alvo);
      esconderAtualizacao();
      worker.postMessage({tipo:'SKIP_WAITING'});

      setTimeout(()=>{
        if(recarregando) return;
        recarregando=true;
        const u=new URL(window.location.href);
        u.searchParams.set('_simpla_update',Date.now().toString());
        window.location.replace(u.toString());
      },1800);
      return;
    }

    esconderAtualizacao();
    window.location.reload();
  }

  function observarInstalacao(registro){
    avaliarWaiting(registro);
    registro.addEventListener('updatefound',()=>{
      const novo=registro.installing;
      if(!novo) return;
      novo.addEventListener('statechange',()=>{
        if(novo.state==='installed' && navigator.serviceWorker.controller){
          setTimeout(()=>avaliarWaiting(registro),50);
        }
      });
    });
  }

  navigator.serviceWorker.addEventListener('controllerchange',async()=>{
    if(recarregando) return;
    recarregando=true;

    try{
      const ativa=navigator.serviceWorker.controller;
      const vAtiva=await obterVersaoWorker(ativa);
      const jaAplicada=localStorage.getItem(STORAGE_KEY);
      if(vAtiva && jaAplicada===vAtiva) localStorage.removeItem(STORAGE_KEY);
    }catch(_){}

    window.location.reload();
  });

  window.addEventListener('load',async()=>{
    try{
      registroPWA=await navigator.serviceWorker.getRegistration('./')
        || await navigator.serviceWorker.register('./service-worker.js',{scope:'./'});

      observarInstalacao(registroPWA);
      await registroPWA.update().catch(()=>{});
      await avaliarWaiting(registroPWA);

      const ativa=navigator.serviceWorker.controller;
      const vAtiva=await obterVersaoWorker(ativa);
      const jaAplicada=localStorage.getItem(STORAGE_KEY);
      if(vAtiva && jaAplicada===vAtiva){
        localStorage.removeItem(STORAGE_KEY);
        esconderAtualizacao();
      }

      setInterval(()=>registroPWA?.update().then(()=>avaliarWaiting(registroPWA)).catch(()=>{}),5*60*1000);

      document.addEventListener('visibilitychange',()=>{
        if(document.visibilityState==='visible'){
          registroPWA?.update().then(()=>avaliarWaiting(registroPWA)).catch(()=>{});
        }
      });
    }catch(err){
      console.warn('SimplA PWA: falha ao verificar atualização.',err);
    }
  });
})();
</script>'''

html=html[:old_manager.start()]+new_manager+html[old_manager.end():]

# Service Worker: expõe sua versão ao gerenciador.
old_msg="""self.addEventListener('message', event => {
  if(event.data === 'SKIP_WAITING' || event.data?.tipo === 'SKIP_WAITING') {
    self.skipWaiting();
  }
});"""
new_msg="""self.addEventListener('message', event => {
  if(event.data === 'SKIP_WAITING' || event.data?.tipo === 'SKIP_WAITING') {
    self.skipWaiting();
    return;
  }

  if(event.data?.tipo === 'GET_VERSION') {
    try {
      event.ports?.[0]?.postMessage({ versao: CACHE_VERSION });
    } catch (_) {}
  }
});"""
if old_msg not in swtxt:
    raise SystemExit('listener message SW nao encontrado')
swtxt=swtxt.replace(old_msg,new_msg,1)

swtxt,n=re.subn(
    r"const CACHE_VERSION = '[^']+';",
    "const CACHE_VERSION = 'simpla-shell-v80-update-stable';",
    swtxt,
    count=1
)
if n!=1: raise SystemExit('cache version nao encontrada')

idx.write_text(html,encoding='utf-8')
sw.write_text(swtxt,encoding='utf-8')
