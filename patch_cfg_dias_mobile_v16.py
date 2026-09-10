from pathlib import Path
import re

p=Path('index.html')
s=p.read_text(encoding='utf-8')
marker='simpla-cfg-dias-mobile-v16'

# 1) Excluir dias de funcionamento das rotinas genéricas de labels/checkboxes
repls = [
    ("if(label.classList.contains('profissional-servico-item')) return;", "if(label.classList.contains('profissional-servico-item')) return;\n      if(label.classList.contains('cfg-dia-label') || cb.classList.contains('cfg-dia-funcionamento')) return;"),
    ("if(label.classList.contains('cfg-switch')) return;", "if(label.classList.contains('cfg-switch')) return;\n      if(label.classList.contains('cfg-dia-label') || cb.classList.contains('cfg-dia-funcionamento')) return;"),
]
# aplica sem duplicar excessivamente; basta garantir ao menos exclusão nas rotinas presentes
for old,new in repls:
    if old in s and new not in s:
        s=s.replace(old,new)

if marker not in s:
    block=r'''
<style id="simpla-cfg-dias-mobile-v16">
/* Dias de funcionamento: interação dedicada no mobile */
#configuracoes .cfg-dia-label{
  position:relative!important;
  display:block!important;
  cursor:pointer!important;
  touch-action:manipulation!important;
  -webkit-tap-highlight-color:transparent!important;
  user-select:none!important;
  -webkit-user-select:none!important;
}
#configuracoes .cfg-dia-label > .cfg-dia-funcionamento{
  position:absolute!important;
  opacity:0!important;
  width:1px!important;
  height:1px!important;
  pointer-events:none!important;
}
#configuracoes .cfg-dia-pill{
  position:relative!important;
  z-index:2!important;
  pointer-events:auto!important;
  touch-action:manipulation!important;
}
@media(max-width:768px){
  #configuracoes .cfg-dias-grid{
    grid-template-columns:repeat(4,minmax(0,1fr))!important;
    gap:8px!important;
  }
  #configuracoes .cfg-dia-label{
    min-width:0!important;
    padding:0!important;
    margin:0!important;
    display:block!important;
  }
  #configuracoes .cfg-dia-pill{
    min-height:44px!important;
    width:100%!important;
    font-size:12px!important;
  }
}
@media(max-width:420px){
  #configuracoes .cfg-dias-grid{
    grid-template-columns:repeat(2,minmax(0,1fr))!important;
  }
}
</style>
<script id="simpla-cfg-dias-mobile-v16-script">
(function(){
  function prepararDias(){
    const raiz=document.getElementById('configuracoes');
    if(!raiz) return;
    raiz.querySelectorAll('.cfg-dia-label').forEach(label=>{
      const input=label.querySelector('.cfg-dia-funcionamento');
      const pill=label.querySelector('.cfg-dia-pill');
      if(!input || !pill) return;
      // remove classes herdadas dos patches genéricos
      label.classList.remove('simpla-mobile-switch-row','simpla-switch-row-v7','simpla-switch-offset-row','simpla-switch-forcado-row');
      label.style.paddingLeft='0';
      label.style.minHeight='0';
      if(label.dataset.diaMobileV16==='1') return;
      label.dataset.diaMobileV16='1';
      const acionar=(ev)=>{
        ev.preventDefault();
        ev.stopPropagation();
        input.checked=!input.checked;
        input.dispatchEvent(new Event('change',{bubbles:true}));
      };
      pill.addEventListener('click',acionar,{passive:false});
      pill.addEventListener('touchend',acionar,{passive:false});
    });
  }
  const iniciar=()=>{
    prepararDias();
    const raiz=document.getElementById('configuracoes');
    if(raiz){
      new MutationObserver(prepararDias).observe(raiz,{childList:true,subtree:true});
    }
  };
  if(document.readyState==='loading') document.addEventListener('DOMContentLoaded',iniciar);
  else iniciar();
  window.addEventListener('load',prepararDias);
})();
</script>
'''
    s=s.replace('</head>',block+'\n</head>',1)

p.write_text(s,encoding='utf-8')

# bump service worker
sw=Path('service-worker.js')
t=sw.read_text(encoding='utf-8')
t=re.sub(r"const CACHE_VERSION = '[^']+';", "const CACHE_VERSION = 'simpla-shell-v16-dias-mobile';", t, count=1)
sw.write_text(t,encoding='utf-8')
