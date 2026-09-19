from pathlib import Path
import re

idx=Path('index.html')
sw=Path('service-worker.js')
html=idx.read_text(encoding='utf-8')

if 'simpla-whatsapp-fix-multilembretes-v73' in html:
    raise SystemExit('v73 ja aplicada')

marker='</body>'
if marker not in html:
    raise SystemExit('body nao encontrado')

block=r'''
<style id="simpla-whatsapp-fix-multilembretes-v73-css">
  #wa-rule-card-lembrete{display:none!important}
</style>

<script id="simpla-whatsapp-fix-multilembretes-v73">
(function(){
  function reposicionar(){
    const grid=document.getElementById('simpla-wa-rules-v68-grid');
    if(!grid)return false;

    const antigo=document.getElementById('wa-rule-card-lembrete');
    if(antigo) antigo.remove();

    let box=document.getElementById('simpla-wa-reminders-v72');
    if(!box && typeof carregarLembretesWhatsAppV72==='function'){
      try{ carregarLembretesWhatsAppV72(); }catch(_){}
      box=document.getElementById('simpla-wa-reminders-v72');
    }

    if(box && box.parentElement!==grid) grid.appendChild(box);
    if(box && box.parentElement===grid) grid.appendChild(box);

    return !!box;
  }

  function instalarHooks(){
    const original=window.carregarRegrasWhatsAppV68;
    if(typeof original==='function' && !original.__v73){
      const wrapped=async function(){
        const out=await original.apply(this,arguments);
        setTimeout(()=>{
          reposicionar();
          try{
            if(typeof carregarLembretesWhatsAppV72==='function') carregarLembretesWhatsAppV72();
          }catch(_){}
        },50);
        return out;
      };
      wrapped.__v73=true;
      window.carregarRegrasWhatsAppV68=wrapped;
    }
  }

  function garantir(){
    instalarHooks();
    reposicionar();
    try{
      if(typeof carregarLembretesWhatsAppV72==='function') carregarLembretesWhatsAppV72();
    }catch(_){}
  }

  const observer=new MutationObserver(()=>{
    const grid=document.getElementById('simpla-wa-rules-v68-grid');
    if(!grid)return;
    if(!document.getElementById('simpla-wa-reminders-v72')){
      setTimeout(garantir,30);
    }else{
      reposicionar();
    }
  });

  function iniciar(){
    const rules=document.getElementById('simpla-wa-rules-v68');
    if(rules) observer.observe(rules,{childList:true,subtree:true});
    garantir();
  }

  document.addEventListener('click',e=>{
    const b=e.target.closest?.('.cfg-v2-nav button');
    if(b&&b.dataset.cat==='WhatsApp e Automações') setTimeout(garantir,100);
  },true);

  if(document.readyState==='loading') document.addEventListener('DOMContentLoaded',()=>setTimeout(iniciar,6200));
  else setTimeout(iniciar,6200);

  setTimeout(iniciar,8200);
})();
</script>
'''

html=html.replace(marker,block+'\n'+marker,1)
idx.write_text(html,encoding='utf-8')

swtxt=sw.read_text(encoding='utf-8')
swtxt,n=re.subn(r"const CACHE_VERSION = '[^']+';","const CACHE_VERSION = 'simpla-shell-v73-fix-multilembretes';",swtxt,count=1)
if n!=1: raise SystemExit('cache version nao encontrada')
sw.write_text(swtxt,encoding='utf-8')
