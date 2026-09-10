from pathlib import Path
import re

p = Path('index.html')
s = p.read_text(encoding='utf-8')
marker = 'simpla-caixa-mobile-v23'

if marker not in s:
    block = r'''
<style id="simpla-caixa-mobile-v23">
@media (max-width:700px){
  .simpla-caixa-resumo-card{overflow:hidden !important; width:100% !important; max-width:100% !important;}
  .simpla-caixa-resumo-card .simpla-caixa-cabecalho{
    display:flex !important;
    flex-direction:column !important;
    align-items:stretch !important;
    gap:14px !important;
    width:100% !important;
    min-width:0 !important;
  }
  .simpla-caixa-resumo-card .simpla-caixa-textos{
    width:100% !important;
    min-width:0 !important;
  }
  .simpla-caixa-resumo-card .simpla-caixa-data{
    width:100% !important;
    min-width:0 !important;
    max-width:100% !important;
    flex:0 0 auto !important;
    display:block !important;
  }
  .simpla-caixa-resumo-card .simpla-caixa-data label,
  .simpla-caixa-resumo-card .simpla-caixa-data *:not(input){
    white-space:normal !important;
    word-break:normal !important;
    overflow-wrap:normal !important;
    writing-mode:horizontal-tb !important;
  }
  .simpla-caixa-resumo-card .simpla-caixa-data input,
  .simpla-caixa-resumo-card .simpla-caixa-data select{
    width:100% !important;
    max-width:100% !important;
    min-width:0 !important;
    box-sizing:border-box !important;
  }
}
</style>
<script id="simpla-caixa-mobile-v23-script">
(function(){
  function aplicar(){
    const elementos = Array.from(document.querySelectorAll('h1,h2,h3,h4,strong,div,span'));
    const titulo = elementos.find(el => (el.textContent||'').trim().toUpperCase() === 'RESUMO DE CAIXA');
    if(!titulo) return;

    let card = titulo.closest('.form-container,.section-box-cfg,.card,.fin-main,[class*=caixa]');
    if(!card) card = titulo.parentElement?.parentElement || titulo.parentElement;
    if(!card) return;
    card.classList.add('simpla-caixa-resumo-card');

    let cab = titulo.parentElement;
    for(let i=0;i<4 && cab;i++){
      const txt = (cab.textContent||'').toUpperCase();
      if(txt.includes('DATA DO CAIXA')) break;
      cab = cab.parentElement;
    }
    if(cab) cab.classList.add('simpla-caixa-cabecalho');

    const textoWrap = titulo.parentElement;
    if(textoWrap) textoWrap.classList.add('simpla-caixa-textos');

    const candidatos = Array.from(card.querySelectorAll('label,div,span,strong'));
    const dataLabel = candidatos.find(el => (el.textContent||'').trim().toUpperCase() === 'DATA DO CAIXA');
    if(dataLabel){
      let dataWrap = dataLabel.parentElement;
      if(dataWrap){
        dataWrap.classList.add('simpla-caixa-data');
        dataWrap.style.setProperty('writing-mode','horizontal-tb','important');
        dataWrap.style.setProperty('word-break','normal','important');
      }
    }
  }

  if(document.readyState==='loading') document.addEventListener('DOMContentLoaded', aplicar);
  else aplicar();
  window.addEventListener('load', aplicar);
  window.addEventListener('resize', aplicar);
  document.addEventListener('click', e => {
    if(e.target.closest('.tab,#financeiro,.menu-btn')) setTimeout(aplicar,50);
  }, true);
  new MutationObserver(()=>requestAnimationFrame(aplicar)).observe(document.body,{childList:true,subtree:true});
  setTimeout(aplicar,300);
  setTimeout(aplicar,1000);
})();
</script>
'''
    s = s.replace('</body>', block + '\n</body>')
    p.write_text(s, encoding='utf-8')

sw = Path('service-worker.js')
t = sw.read_text(encoding='utf-8')
t = re.sub(r"const CACHE_VERSION = 'simpla-shell-v[^']+';", "const CACHE_VERSION = 'simpla-shell-v23-caixa-mobile';", t, count=1)
sw.write_text(t, encoding='utf-8')
