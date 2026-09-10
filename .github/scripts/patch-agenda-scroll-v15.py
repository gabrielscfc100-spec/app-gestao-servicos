from pathlib import Path
import re

p = Path('index.html')
s = p.read_text(encoding='utf-8')
marker = 'simpla-agenda-scroll-v15'

if marker not in s:
    block = r'''
<style id="simpla-agenda-scroll-v15">
/* Agenda v15 — cabeçalho fixo fora da rolagem e grade totalmente navegável */
#agenda.simpla-agenda-v14 .agenda-v14-scroll,
#agenda .agenda-scroll-area {
  overflow: visible !important;
  max-height: none !important;
  height: auto !important;
}
#agenda .agenda-v15-static-head {
  position: static !important;
  top: auto !important;
  z-index: auto !important;
  background: #fff !important;
  display: block !important;
  padding: 4px 2px 12px !important;
  margin-bottom: 12px !important;
  border-bottom: 1px solid #e2e8f0 !important;
}
#agenda .agenda-v15-static-head #agenda-subtitulo-data {
  margin: 0 !important;
  font-size: 16px !important;
  color: #1a1c23 !important;
}
#agenda #agenda-expediente-info,
#agenda .agenda-v14-legenda {
  display: none !important;
}
#agenda .agenda-v15-grid-scroll {
  overflow-y: auto !important;
  overflow-x: hidden !important;
  max-height: calc(100dvh - 470px) !important;
  min-height: 260px;
  padding-right: 6px;
  scrollbar-gutter: stable;
  overscroll-behavior: contain;
  -webkit-overflow-scrolling: touch;
}
#agenda .agenda-v15-grid-scroll::-webkit-scrollbar { width: 10px; }
#agenda .agenda-v15-grid-scroll::-webkit-scrollbar-track { background:#edf2f7; border-radius:10px; }
#agenda .agenda-v15-grid-scroll::-webkit-scrollbar-thumb { background:#a0aec0; border-radius:10px; }
#agenda .agenda-v15-grid-scroll .agenda-grid {
  margin-bottom: 12px !important;
}
@media (max-height:780px) and (min-width:601px){
  #agenda .agenda-v15-grid-scroll { max-height: calc(100dvh - 420px) !important; min-height:220px; }
}
@media (max-width:600px){
  #agenda .agenda-v15-grid-scroll {
    max-height: 58dvh !important;
    min-height: 300px;
    padding-right: 4px;
  }
  #agenda .agenda-v15-static-head { padding-bottom: 10px !important; }
}
</style>
<script id="simpla-agenda-scroll-v15-script">
(function(){
  function removerResiduosBody(){
    Array.from(document.body.childNodes).forEach(no => {
      if(no.nodeType !== Node.TEXT_NODE) return;
      const t = String(no.textContent || '');
      const limpo = t.replace(/\\[nN]/g,'').replace(/\s/g,'');
      if(!limpo) no.remove();
    });
  }

  function aplicar(){
    const agenda = document.getElementById('agenda');
    if(!agenda) return;

    removerResiduosBody();

    const container = agenda.querySelector('.agenda-v14-scroll') || agenda.querySelector('.agenda-scroll-area');
    const grid = document.getElementById('grid-horarios-agenda');
    if(!container || !grid) return;

    const cabecalho = container.querySelector(':scope > div:first-child');
    if(cabecalho){
      cabecalho.classList.add('agenda-v15-static-head');
      cabecalho.style.setProperty('position','static','important');
      cabecalho.style.setProperty('top','auto','important');
      cabecalho.style.setProperty('z-index','auto','important');
    }

    const info = document.getElementById('agenda-expediente-info');
    if(info) info.style.setProperty('display','none','important');
    agenda.querySelectorAll('.agenda-v14-legenda').forEach(el => el.remove());

    let scroll = grid.closest('.agenda-v15-grid-scroll');
    if(!scroll){
      scroll = document.createElement('div');
      scroll.className = 'agenda-v15-grid-scroll';
      grid.parentNode.insertBefore(scroll, grid);
      scroll.appendChild(grid);
    }
  }

  function agendar(){ requestAnimationFrame(()=>requestAnimationFrame(aplicar)); }

  if(document.readyState === 'loading') document.addEventListener('DOMContentLoaded', aplicar);
  else aplicar();

  window.addEventListener('load', aplicar);
  window.addEventListener('resize', agendar);
  document.addEventListener('click', e => {
    if(e.target.closest('#menu-btn-agenda, .agenda-v14-nav, #agenda-profissional-filtro')) setTimeout(aplicar, 50);
  }, true);

  const alvo = document.getElementById('agenda');
  if(alvo){
    const obs = new MutationObserver(agendar);
    obs.observe(alvo,{childList:true,subtree:true});
  }
  setTimeout(aplicar,300);
  setTimeout(aplicar,1000);
})();
</script>
'''
    s = s.replace('</body>', block + '\n</body>')
    p.write_text(s, encoding='utf-8')

sw = Path('service-worker.js')
ss = sw.read_text(encoding='utf-8')
ss2 = re.sub(r"const CACHE_VERSION = '[^']+';", "const CACHE_VERSION = 'simpla-shell-v15-agenda-scroll';", ss, count=1)
if ss2 != ss:
    sw.write_text(ss2, encoding='utf-8')
