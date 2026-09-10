from pathlib import Path

p=Path('index.html')
s=p.read_text(encoding='utf-8')
marker='simpla-mobile-switch-force-v10'
if marker not in s:
    block=r'''
<script id="simpla-mobile-switch-force-v10">
(function(){
  function aplicar(){
    if (window.innerWidth > 768) return;
    const raiz=document.getElementById('configuracoes');
    if(!raiz) return;

    raiz.querySelectorAll('label').forEach(label=>{
      const cb=label.querySelector(':scope > input[type="checkbox"]');
      if(!cb) return;
      if(label.classList.contains('profissional-servico-item')) return;
      if(label.classList.contains('cfg-switch')) return;
      if(label.querySelector('.cfg-switch-track')) return;

      label.classList.remove('simpla-mobile-switch-row');
      label.style.setProperty('position','relative','important');
      label.style.setProperty('display','block','important');
      label.style.setProperty('width','100%','important');
      label.style.setProperty('min-width','0','important');
      label.style.setProperty('min-height','34px','important');
      label.style.setProperty('padding-left','68px','important');
      label.style.setProperty('padding-right','4px','important');
      label.style.setProperty('margin-top','8px','important');
      label.style.setProperty('margin-bottom','8px','important');
      label.style.setProperty('font-size','11.5px','important');
      label.style.setProperty('line-height','1.35','important');
      label.style.setProperty('white-space','normal','important');
      label.style.setProperty('overflow-wrap','anywhere','important');

      cb.style.setProperty('position','absolute','important');
      cb.style.setProperty('left','8px','important');
      cb.style.setProperty('top','50%','important');
      cb.style.setProperty('transform','translateY(-50%)','important');
      cb.style.setProperty('margin','0','important');
      cb.style.setProperty('width','42px','important');
      cb.style.setProperty('min-width','42px','important');
      cb.style.setProperty('max-width','42px','important');
      cb.style.setProperty('height','24px','important');
      cb.style.setProperty('z-index','2','important');
    });
  }

  function agendar(){ requestAnimationFrame(()=>requestAnimationFrame(aplicar)); }
  document.addEventListener('DOMContentLoaded',()=>{
    aplicar();
    const raiz=document.getElementById('configuracoes');
    if(raiz){
      const obs=new MutationObserver(agendar);
      obs.observe(raiz,{childList:true,subtree:true});
    }
  });
  window.addEventListener('resize',agendar);
  document.addEventListener('click',e=>{
    if(e.target.closest('[data-config-tab], .cfg-nav-btn, .menu-btn')) setTimeout(aplicar,50);
  },true);
  setTimeout(aplicar,300);
  setTimeout(aplicar,1000);
})();
</script>
'''
    s=s.replace('</body>',block+'\n</body>')
    p.write_text(s,encoding='utf-8')

sw=Path('service-worker.js')
ss=sw.read_text(encoding='utf-8')
import re
ss2=re.sub(r"const CACHE_VERSION = '[^']+';", "const CACHE_VERSION = 'simpla-shell-v10-switches-forcados';", ss, count=1)
if ss2!=ss:
    sw.write_text(ss2,encoding='utf-8')
