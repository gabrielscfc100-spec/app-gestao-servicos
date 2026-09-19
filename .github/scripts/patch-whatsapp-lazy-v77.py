from pathlib import Path
import re

idx=Path('index.html')
sw=Path('service-worker.js')
html=idx.read_text(encoding='utf-8')

if 'simpla-whatsapp-lazy-v77' in html:
    raise SystemExit('v77 ja aplicada')

marker='</body>'
if marker not in html:
    raise SystemExit('body nao encontrado')

block=r'''
<script id="simpla-whatsapp-lazy-v77">
(function(){
  const CAT='WhatsApp e Automações';
  let carregando=null;

  function ativar(nav,content){
    nav.querySelectorAll('button').forEach(b=>b.classList.toggle('ativo',b.dataset.cat===CAT));
    content.querySelectorAll('.cfg-v2-group').forEach(g=>g.classList.toggle('ativo',g.dataset.cat===CAT));
  }

  function carregarModulo(container){
    if(window.SimplAWhatsAppV77){
      window.SimplAWhatsAppV77.mount(container);
      return Promise.resolve();
    }
    if(carregando) return carregando;
    container.innerHTML='<div style="padding:24px;text-align:center;color:#718096;font-size:12px;text-transform:none">Carregando WhatsApp e Automações...</div>';
    carregando=new Promise((resolve,reject)=>{
      const s=document.createElement('script');
      s.src='./whatsapp-automacoes-v77.js';
      s.async=true;
      s.onload=()=>{
        if(window.SimplAWhatsAppV77){
          Promise.resolve(window.SimplAWhatsAppV77.mount(container)).then(resolve,reject);
        }else reject(new Error('Módulo WhatsApp não inicializado.'));
      };
      s.onerror=()=>reject(new Error('Não foi possível carregar o módulo WhatsApp.'));
      document.head.appendChild(s);
    }).catch(err=>{
      console.error('SimplA WhatsApp lazy v77:',err);
      container.innerHTML='<div style="padding:24px;text-align:center;color:#c53030;font-size:12px;text-transform:none">Não foi possível carregar as configurações do WhatsApp agora.</div>';
      carregando=null;
    });
    return carregando;
  }

  function montar(){
    const shell=document.querySelector('#configuracoes .cfg-v2-shell');
    if(!shell)return false;
    const nav=shell.querySelector('.cfg-v2-nav');
    const content=shell.querySelector('.cfg-v2-content');
    if(!nav||!content)return false;

    let btn=[...nav.querySelectorAll('button')].find(b=>b.dataset.cat===CAT);
    let group=content.querySelector('.cfg-v2-group[data-cat="'+CAT+'"]');

    if(!btn){
      btn=document.createElement('button');
      btn.type='button';
      btn.dataset.cat=CAT;
      btn.innerHTML='<span>'+CAT+'</span><span>›</span>';
      const geral=[...nav.querySelectorAll('button')].find(b=>b.dataset.cat==='Geral e Aparência');
      if(geral)nav.insertBefore(btn,geral);else nav.appendChild(btn);
    }

    if(!group){
      group=document.createElement('section');
      group.className='cfg-v2-group';
      group.dataset.cat=CAT;
      group.innerHTML='<h2>'+CAT+'</h2><p class="cfg-v2-desc">Conexão com a Meta, mensagens operacionais, lembretes, franquia e automações.</p><div id="simpla-wa77-container"></div>';
      const geral=content.querySelector('.cfg-v2-group[data-cat="Geral e Aparência"]');
      if(geral)content.insertBefore(group,geral);else content.appendChild(group);
    }

    if(!btn.dataset.lazyWa77){
      btn.dataset.lazyWa77='1';
      btn.addEventListener('click',()=>{
        ativar(nav,content);
        const container=group.querySelector('#simpla-wa77-container');
        carregarModulo(container);
      });
    }
    return true;
  }

  function instalar(){
    let tentativas=0;
    const timer=setInterval(()=>{
      tentativas++;
      if(montar()||tentativas>=12)clearInterval(timer);
    },250);
  }

  if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',()=>setTimeout(instalar,100));
  else setTimeout(instalar,100);
})();
</script>
'''
html=html.replace(marker,block+'\n'+marker,1)
idx.write_text(html,encoding='utf-8')

swtxt=sw.read_text(encoding='utf-8')
swtxt,n=re.subn(r"const CACHE_VERSION = '[^']+';","const CACHE_VERSION = 'simpla-shell-v77-whatsapp-lazy';",swtxt,count=1)
if n!=1: raise SystemExit('cache version nao encontrada')
sw.write_text(swtxt,encoding='utf-8')
