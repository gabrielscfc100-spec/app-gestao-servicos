from pathlib import Path

p = Path('index.html')
s = p.read_text(encoding='utf-8')
marker = '</head>'
block = r'''
<style id="simpla-mobile-two-blocks-final-v11">
@media (max-width:768px){
  /* Serviços e durações: reserva física suficiente para o switch */
  #configuracoes .profissional-servico-item{
    display:grid!important;
    grid-template-columns:92px minmax(0,1fr) 88px!important;
    column-gap:10px!important;
    align-items:center!important;
    padding:12px!important;
    min-width:0!important;
  }
  #configuracoes .profissional-servico-item > input[type="checkbox"]{
    position:static!important;
    grid-column:1!important;
    grid-row:1!important;
    justify-self:start!important;
    margin:0!important;
    transform:none!important;
  }
  #configuracoes .profissional-servico-item > span{
    grid-column:2!important;
    grid-row:1!important;
    min-width:0!important;
    margin:0!important;
    padding:0!important;
    font-size:11px!important;
    line-height:1.2!important;
    overflow-wrap:anywhere!important;
  }
  #configuracoes .profissional-servico-item > span b,
  #configuracoes .profissional-servico-item > span strong{
    display:block!important;
    margin:0 0 4px!important;
    font-size:11.5px!important;
    line-height:1.15!important;
  }
  #configuracoes .profissional-servico-item > span small{
    display:block!important;
    font-size:10px!important;
    line-height:1.15!important;
  }
  #configuracoes .profissional-servico-item > input[type="number"]{
    grid-column:3!important;
    grid-row:1!important;
    width:88px!important;
    min-width:88px!important;
    max-width:88px!important;
    justify-self:end!important;
    font-size:12px!important;
  }

  /* Comissões individuais */
  #configuracoes .profissional-comissoes-linha-final{
    display:grid!important;
    grid-template-columns:minmax(0,1fr) minmax(0,1fr)!important;
    gap:10px!important;
    align-items:end!important;
    width:100%!important;
  }
  #configuracoes .profissional-comissoes-linha-final > .form-group{
    width:100%!important;
    max-width:none!important;
    min-width:0!important;
    margin:0!important;
  }
  #configuracoes .profissional-comissoes-linha-final > .form-group label{
    display:block!important;
    font-size:11px!important;
    line-height:1.2!important;
    margin-bottom:5px!important;
    white-space:normal!important;
    word-break:normal!important;
  }
  #configuracoes .profissional-comissoes-linha-final > .form-group input{
    width:100%!important;
    min-width:0!important;
    font-size:12px!important;
  }
  #configuracoes .profissional-comissoes-linha-final > button{
    grid-column:1/-1!important;
    width:100%!important;
    margin-top:2px!important;
    padding:9px 10px!important;
    font-size:11.5px!important;
  }
}
@media (max-width:420px){
  #configuracoes .profissional-servico-item{
    grid-template-columns:88px minmax(0,1fr) 82px!important;
    column-gap:8px!important;
  }
  #configuracoes .profissional-servico-item > input[type="number"]{
    width:82px!important;
    min-width:82px!important;
    max-width:82px!important;
  }
}
</style>
<script id="simpla-mobile-two-blocks-final-v11-script">
(function(){
  function aplicar(){
    const raiz=document.getElementById('configuracoes');
    if(!raiz) return;

    raiz.querySelectorAll('input[id^="prof-comissao-servicos-"]').forEach(inp=>{
      const grupo=inp.closest('.form-group');
      const linha=grupo && grupo.parentElement;
      if(!linha) return;
      linha.classList.add('profissional-comissoes-linha-final');
    });

    raiz.querySelectorAll('.profissional-servico-item').forEach(card=>{
      const cb=card.querySelector(':scope > input[type="checkbox"]');
      const texto=card.querySelector(':scope > span');
      const num=card.querySelector(':scope > input[type="number"]');
      if(!cb || !texto || !num) return;
      card.style.setProperty('display','grid','important');
      card.style.setProperty('grid-template-columns', window.innerWidth <= 420 ? '88px minmax(0,1fr) 82px' : '92px minmax(0,1fr) 88px','important');
      card.style.setProperty('column-gap', window.innerWidth <= 420 ? '8px' : '10px','important');
      cb.style.setProperty('position','static','important');
      cb.style.setProperty('grid-column','1','important');
      cb.style.setProperty('margin','0','important');
      texto.style.setProperty('grid-column','2','important');
      texto.style.setProperty('padding','0','important');
      texto.style.setProperty('margin','0','important');
      num.style.setProperty('grid-column','3','important');
    });
  }
  document.addEventListener('DOMContentLoaded',()=>setTimeout(aplicar,50));
  window.addEventListener('resize',aplicar);
  const obs=new MutationObserver(()=>{ clearTimeout(window.__simplaTwoBlocksTimer); window.__simplaTwoBlocksTimer=setTimeout(aplicar,30); });
  document.addEventListener('DOMContentLoaded',()=>{ const r=document.getElementById('configuracoes'); if(r) obs.observe(r,{childList:true,subtree:true}); });
  setInterval(aplicar,1200);
})();
</script>
'''
if 'simpla-mobile-two-blocks-final-v11' not in s:
    s = s.replace(marker, block + '\n' + marker)
p.write_text(s, encoding='utf-8')

sw = Path('service-worker.js')
w = sw.read_text(encoding='utf-8')
w = w.replace("const CACHE_VERSION = 'simpla-shell-v10-switches-forcados';", "const CACHE_VERSION = 'simpla-shell-v11-dois-blocos-mobile';")
w = w.replace("const CACHE_VERSION = 'simpla-shell-v9-switches-texto-deslocado';", "const CACHE_VERSION = 'simpla-shell-v11-dois-blocos-mobile';")
if "simpla-shell-v11-dois-blocos-mobile" not in w:
    import re
    w = re.sub(r"const CACHE_VERSION = '[^']+';", "const CACHE_VERSION = 'simpla-shell-v11-dois-blocos-mobile';", w, count=1)
sw.write_text(w, encoding='utf-8')
