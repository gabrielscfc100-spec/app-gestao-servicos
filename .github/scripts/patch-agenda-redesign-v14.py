from pathlib import Path
import re

p = Path('index.html')
s = p.read_text(encoding='utf-8')
marker = 'simpla-agenda-redesign-v14'

if marker not in s:
    block = r'''
<style id="simpla-agenda-redesign-v14">
/* ===== SimplA Agenda v14 — remodelagem final ===== */
#agenda.simpla-agenda-v14 {
  --agenda-border:#e2e8f0;
  --agenda-soft:#f8fafc;
  --agenda-text:#1a1c23;
  --agenda-muted:#718096;
}
#agenda.simpla-agenda-v14 .agenda-v14-header {
  background:#fff;
  border:1px solid var(--agenda-border);
  border-radius:14px;
  padding:18px 20px;
  margin-bottom:14px;
  box-shadow:0 4px 14px rgba(26,28,35,.05);
}
#agenda.simpla-agenda-v14 .agenda-v14-header h1 {
  font-size:22px!important;
  letter-spacing:-.25px;
}
#agenda.simpla-agenda-v14 .agenda-v14-toolbar {
  display:flex!important;
  align-items:flex-end!important;
  justify-content:flex-end!important;
  gap:10px!important;
  flex-wrap:wrap!important;
}
#agenda.simpla-agenda-v14 .agenda-v14-toolbar > div {
  background:var(--agenda-soft);
  border:1px solid var(--agenda-border);
  border-radius:10px;
  padding:7px 9px;
}
#agenda.simpla-agenda-v14 .agenda-v14-toolbar label {
  font-size:10px!important;
  color:var(--agenda-muted)!important;
  display:block!important;
  margin:0 0 4px!important;
  line-height:1!important;
}
#agenda.simpla-agenda-v14 .agenda-v14-toolbar select,
#agenda.simpla-agenda-v14 .agenda-v14-toolbar input[type="date"] {
  border:0!important;
  background:transparent!important;
  padding:3px 2px!important;
  min-height:30px;
  font-weight:600;
}
#agenda.simpla-agenda-v14 .agenda-v14-nav {
  display:grid;
  grid-template-columns:auto minmax(170px,1fr) auto;
  align-items:center;
  gap:10px;
  margin:0 0 14px;
  background:#fff;
  border:1px solid var(--agenda-border);
  border-radius:12px;
  padding:10px 12px;
}
#agenda.simpla-agenda-v14 .agenda-v14-nav-group {
  display:flex;
  gap:7px;
  align-items:center;
}
#agenda.simpla-agenda-v14 .agenda-v14-nav-group:last-child { justify-content:flex-end; }
#agenda.simpla-agenda-v14 .agenda-v14-nav button {
  border:1px solid #cbd5e0;
  background:#fff;
  color:#334155;
  border-radius:8px;
  padding:8px 11px;
  min-height:36px;
  cursor:pointer;
  font-size:12px;
  font-weight:700;
}
#agenda.simpla-agenda-v14 .agenda-v14-nav button:hover { background:#f1f5f9; }
#agenda.simpla-agenda-v14 #agenda-v14-hoje {
  background:#1a1c23;
  color:#fff;
  border-color:#1a1c23;
}
#agenda.simpla-agenda-v14 .agenda-v14-data-central {
  text-align:center;
  min-width:0;
}
#agenda.simpla-agenda-v14 .agenda-v14-data-central strong {
  display:block;
  font-size:15px;
  color:var(--agenda-text);
  white-space:nowrap;
  overflow:hidden;
  text-overflow:ellipsis;
}
#agenda.simpla-agenda-v14 .agenda-v14-data-central span {
  display:block;
  font-size:11px;
  color:var(--agenda-muted);
  margin-top:2px;
}
#agenda.simpla-agenda-v14 .agenda-v14-resumo {
  display:grid;
  grid-template-columns:repeat(4,minmax(0,1fr));
  gap:10px;
  margin-bottom:14px;
}
#agenda.simpla-agenda-v14 .agenda-v14-kpi {
  background:#fff;
  border:1px solid var(--agenda-border);
  border-radius:12px;
  padding:13px 14px;
  min-width:0;
}
#agenda.simpla-agenda-v14 .agenda-v14-kpi span {
  display:block;
  font-size:10px;
  color:var(--agenda-muted);
  margin-bottom:5px;
}
#agenda.simpla-agenda-v14 .agenda-v14-kpi strong {
  display:block;
  font-size:20px;
  color:var(--agenda-text);
  line-height:1.1;
}
#agenda.simpla-agenda-v14 .agenda-v14-kpi small {
  display:block;
  margin-top:4px;
  font-size:10px;
  color:#94a3b8;
  text-transform:none;
}
#agenda.simpla-agenda-v14 #agenda-online-compartilhar {
  padding:13px 15px!important;
  border-radius:12px!important;
  border:1px solid var(--agenda-border)!important;
  box-shadow:none!important;
  margin-bottom:14px!important;
}
#agenda.simpla-agenda-v14 #agenda-online-compartilhar h3 { font-size:13px!important; }
#agenda.simpla-agenda-v14 #agenda-online-compartilhar p { font-size:11px!important; margin-bottom:8px!important; }
#agenda.simpla-agenda-v14 #agenda-link-publico { min-height:38px; }
#agenda.simpla-agenda-v14 .agenda-v14-scroll {
  border:1px solid var(--agenda-border)!important;
  border-radius:14px!important;
  box-shadow:none!important;
  padding:16px!important;
}
#agenda.simpla-agenda-v14 .agenda-v14-scroll > div:first-child {
  border-bottom:1px solid var(--agenda-border);
  padding:4px 2px 12px!important;
  margin-bottom:12px!important;
}
#agenda.simpla-agenda-v14 .agenda-v14-legenda {
  display:flex;
  gap:8px;
  flex-wrap:wrap;
  align-items:center;
  justify-content:flex-end;
  margin-left:auto;
}
#agenda.simpla-agenda-v14 .agenda-v14-legenda span {
  font-size:9px;
  font-weight:700;
  padding:5px 8px;
  border-radius:999px;
  border:1px solid var(--agenda-border);
  background:#fff;
  color:#475569;
}
#agenda.simpla-agenda-v14 .agenda-v14-legenda .vago { border-color:#9ae6b4; background:#f0fff4; color:#276749; }
#agenda.simpla-agenda-v14 .agenda-v14-legenda .ocupado { border-color:#90cdf4; background:#ebf8ff; color:#2b6cb0; }
#agenda.simpla-agenda-v14 .agenda-v14-legenda .bloqueado { border-color:#feb2b2; background:#fff5f5; color:#c53030; }
#agenda.simpla-agenda-v14 .agenda-grid {
  grid-template-columns:repeat(auto-fill,minmax(255px,1fr))!important;
  gap:12px!important;
  margin-top:0!important;
}
#agenda.simpla-agenda-v14 .slot-card {
  border-radius:12px!important;
  padding:14px!important;
  min-height:150px;
  box-shadow:0 2px 7px rgba(26,28,35,.04);
  border-top:1px solid var(--agenda-border)!important;
  border-right:1px solid var(--agenda-border)!important;
  border-bottom:1px solid var(--agenda-border)!important;
}
#agenda.simpla-agenda-v14 .slot-card:hover {
  transform:translateY(-1px);
  box-shadow:0 7px 16px rgba(26,28,35,.08);
}
#agenda.simpla-agenda-v14 .slot-card.vago { background:#fbfffc!important; }
#agenda.simpla-agenda-v14 .slot-card.ocupado { background:#f8fbff!important; }
#agenda.simpla-agenda-v14 .slot-card.bloqueado { background:#fffafa!important; }
#agenda.simpla-agenda-v14 .slot-header { margin-bottom:9px!important; }
#agenda.simpla-agenda-v14 .slot-horario { font-size:18px!important; }
#agenda.simpla-agenda-v14 .slot-badge { border-radius:999px!important; padding:4px 7px!important; }
#agenda.simpla-agenda-v14 .slot-body {
  font-size:12px!important;
  line-height:1.5!important;
  margin-bottom:12px!important;
  text-transform:none;
}
#agenda.simpla-agenda-v14 .slot-card button {
  border-radius:7px!important;
  min-height:34px;
  font-size:10px!important;
}
#agenda.simpla-agenda-v14 .agenda-v14-exportacoes button {
  min-height:36px;
  padding:8px 10px!important;
  font-size:10px!important;
}
@media(max-width:900px){
  #agenda.simpla-agenda-v14 .agenda-v14-header { padding:14px; }
  #agenda.simpla-agenda-v14 .agenda-v14-header { display:block!important; }
  #agenda.simpla-agenda-v14 .agenda-v14-header h1 { margin-bottom:12px!important; }
  #agenda.simpla-agenda-v14 .agenda-v14-toolbar { justify-content:stretch!important; }
  #agenda.simpla-agenda-v14 .agenda-v14-toolbar > div { flex:1 1 200px; }
  #agenda.simpla-agenda-v14 .agenda-v14-resumo { grid-template-columns:repeat(2,minmax(0,1fr)); }
}
@media(max-width:600px){
  #agenda.simpla-agenda-v14 { height:auto!important; overflow:visible!important; }
  #agenda.simpla-agenda-v14 .agenda-v14-header { margin-bottom:10px; }
  #agenda.simpla-agenda-v14 .agenda-v14-toolbar { display:grid!important; grid-template-columns:1fr!important; }
  #agenda.simpla-agenda-v14 .agenda-v14-toolbar > div { width:100%; }
  #agenda.simpla-agenda-v14 .agenda-v14-toolbar select,
  #agenda.simpla-agenda-v14 .agenda-v14-toolbar input[type="date"] { width:100%!important; min-width:0!important; }
  #agenda.simpla-agenda-v14 .agenda-v14-exportacoes { display:grid!important; grid-template-columns:1fr 1fr!important; gap:7px!important; }
  #agenda.simpla-agenda-v14 .agenda-v14-nav { grid-template-columns:1fr!important; padding:10px; }
  #agenda.simpla-agenda-v14 .agenda-v14-data-central { grid-row:1; }
  #agenda.simpla-agenda-v14 .agenda-v14-nav-group { justify-content:center!important; }
  #agenda.simpla-agenda-v14 .agenda-v14-nav-group button { flex:1; }
  #agenda.simpla-agenda-v14 .agenda-v14-resumo { gap:8px; }
  #agenda.simpla-agenda-v14 .agenda-v14-kpi { padding:11px; }
  #agenda.simpla-agenda-v14 .agenda-v14-kpi strong { font-size:18px; }
  #agenda.simpla-agenda-v14 #agenda-online-compartilhar > div:last-child { display:grid!important; grid-template-columns:1fr 1fr!important; }
  #agenda.simpla-agenda-v14 #agenda-link-publico { grid-column:1 / -1; min-width:0!important; width:100%; }
  #agenda.simpla-agenda-v14 .agenda-v14-scroll { padding:11px!important; overflow:visible!important; max-height:none!important; }
  #agenda.simpla-agenda-v14 .agenda-v14-scroll > div:first-child { display:block!important; position:static!important; }
  #agenda.simpla-agenda-v14 #agenda-expediente-info { display:block; margin-top:5px; }
  #agenda.simpla-agenda-v14 .agenda-v14-legenda { justify-content:flex-start; margin-top:9px; }
  #agenda.simpla-agenda-v14 .agenda-grid { grid-template-columns:1fr!important; }
  #agenda.simpla-agenda-v14 .slot-card { min-height:0; }
}
</style>
<script id="simpla-agenda-redesign-v14-script">
(function(){
  function pad(n){ return String(n).padStart(2,'0'); }
  function hojeLocal(){ const d=new Date(); return `${d.getFullYear()}-${pad(d.getMonth()+1)}-${pad(d.getDate())}`; }
  function moverDia(qtd){
    const campo=document.getElementById('agenda-data-filtro');
    if(!campo) return;
    const valor=campo.value || hojeLocal();
    const [a,m,d]=valor.split('-').map(Number);
    const data=new Date(a,m-1,d);
    data.setDate(data.getDate()+qtd);
    campo.value=`${data.getFullYear()}-${pad(data.getMonth()+1)}-${pad(data.getDate())}`;
    campo.dispatchEvent(new Event('change',{bubbles:true}));
    atualizarResumo();
  }
  function irHoje(){
    const campo=document.getElementById('agenda-data-filtro');
    if(!campo) return;
    campo.value=hojeLocal();
    campo.dispatchEvent(new Event('change',{bubbles:true}));
    atualizarResumo();
  }
  function formatarData(valor){
    if(!valor) return {principal:'Selecione uma data',secundario:''};
    const [a,m,d]=valor.split('-').map(Number);
    const dt=new Date(a,m-1,d);
    const principal=dt.toLocaleDateString('pt-BR',{weekday:'long',day:'2-digit',month:'long'});
    const secundario=dt.toLocaleDateString('pt-BR',{year:'numeric'});
    return {principal:principal.charAt(0).toUpperCase()+principal.slice(1),secundario};
  }
  function atualizarResumo(){
    const agenda=document.getElementById('agenda');
    if(!agenda) return;
    const campo=document.getElementById('agenda-data-filtro');
    const dt=formatarData(campo?.value || '');
    const p=document.getElementById('agenda-v14-data-principal');
    const s=document.getElementById('agenda-v14-data-secundaria');
    if(p) p.textContent=dt.principal;
    if(s) s.textContent=dt.secundario;

    const grid=document.getElementById('grid-horarios-agenda');
    if(!grid) return;
    const ocupados=grid.querySelectorAll('.slot-card.ocupado').length;
    const vagos=grid.querySelectorAll('.slot-card.vago').length;
    const bloqueados=grid.querySelectorAll('.slot-card.bloqueado').length;
    const total=ocupados+vagos+bloqueados;
    const base=ocupados+vagos;
    const ocupacao=base ? Math.round((ocupados/base)*100) : 0;
    const mapa={
      'agenda-v14-agendados':ocupados,
      'agenda-v14-livres':vagos,
      'agenda-v14-bloqueados':bloqueados,
      'agenda-v14-ocupacao':`${ocupacao}%`
    };
    Object.entries(mapa).forEach(([id,val])=>{ const el=document.getElementById(id); if(el) el.textContent=String(val); });
    const totalEl=document.getElementById('agenda-v14-total-slots');
    if(totalEl) totalEl.textContent=`${total} horário${total===1?'':'s'} exibido${total===1?'':'s'}`;
  }
  function preparar(){
    const agenda=document.getElementById('agenda');
    if(!agenda || agenda.dataset.redesignV14==='1') { atualizarResumo(); return; }
    agenda.dataset.redesignV14='1';
    agenda.classList.add('simpla-agenda-v14');

    const header=agenda.querySelector('.header');
    if(header){
      header.classList.add('agenda-v14-header');
      const toolbar=Array.from(header.children).find(el=>el.tagName==='DIV');
      if(toolbar){
        toolbar.classList.add('agenda-v14-toolbar');
        const grupos=toolbar.querySelectorAll(':scope > div');
        if(grupos[1]) grupos[1].classList.add('agenda-v14-exportacoes');
      }
      const h1=header.querySelector('h1');
      if(h1) h1.textContent='Agenda';
    }

    const online=document.getElementById('agenda-online-compartilhar');
    if(online && !document.getElementById('agenda-v14-nav')){
      const nav=document.createElement('div');
      nav.id='agenda-v14-nav';
      nav.className='agenda-v14-nav';
      nav.innerHTML=`
        <div class="agenda-v14-nav-group">
          <button type="button" id="agenda-v14-anterior" aria-label="Dia anterior">‹ Anterior</button>
          <button type="button" id="agenda-v14-hoje">Hoje</button>
        </div>
        <div class="agenda-v14-data-central">
          <strong id="agenda-v14-data-principal">Data selecionada</strong>
          <span id="agenda-v14-data-secundaria"></span>
        </div>
        <div class="agenda-v14-nav-group">
          <button type="button" id="agenda-v14-proximo">Próximo ›</button>
        </div>`;
      online.parentNode.insertBefore(nav,online);
      document.getElementById('agenda-v14-anterior')?.addEventListener('click',()=>moverDia(-1));
      document.getElementById('agenda-v14-hoje')?.addEventListener('click',irHoje);
      document.getElementById('agenda-v14-proximo')?.addEventListener('click',()=>moverDia(1));
    }

    if(online && !document.getElementById('agenda-v14-resumo')){
      const resumo=document.createElement('div');
      resumo.id='agenda-v14-resumo';
      resumo.className='agenda-v14-resumo';
      resumo.innerHTML=`
        <div class="agenda-v14-kpi"><span>Agendados</span><strong id="agenda-v14-agendados">0</strong><small>horários ocupados</small></div>
        <div class="agenda-v14-kpi"><span>Livres</span><strong id="agenda-v14-livres">0</strong><small>disponíveis no dia</small></div>
        <div class="agenda-v14-kpi"><span>Bloqueados</span><strong id="agenda-v14-bloqueados">0</strong><small>indisponibilidades</small></div>
        <div class="agenda-v14-kpi"><span>Ocupação</span><strong id="agenda-v14-ocupacao">0%</strong><small id="agenda-v14-total-slots">0 horários exibidos</small></div>`;
      online.parentNode.insertBefore(resumo,online);
    }

    const grid=document.getElementById('grid-horarios-agenda');
    const scroll=grid?.closest('.form-container');
    if(scroll){
      scroll.classList.add('agenda-v14-scroll');
      const cab=scroll.firstElementChild;
      if(cab && !cab.querySelector('.agenda-v14-legenda')){
        const legenda=document.createElement('div');
        legenda.className='agenda-v14-legenda';
        legenda.innerHTML='<span class="vago">Livre</span><span class="ocupado">Agendado</span><span class="bloqueado">Bloqueado</span>';
        cab.appendChild(legenda);
      }
    }

    document.getElementById('agenda-data-filtro')?.addEventListener('change',()=>setTimeout(atualizarResumo,100));
    document.getElementById('agenda-profissional-filtro')?.addEventListener('change',()=>setTimeout(atualizarResumo,100));
    if(grid){
      const obs=new MutationObserver(()=>requestAnimationFrame(atualizarResumo));
      obs.observe(grid,{childList:true,subtree:true,attributes:true,attributeFilter:['class']});
    }
    atualizarResumo();
  }

  if(document.readyState==='loading') document.addEventListener('DOMContentLoaded',preparar);
  else preparar();
  window.addEventListener('load',preparar);
  document.addEventListener('click',e=>{
    if(e.target.closest('#menu-btn-agenda')) setTimeout(preparar,50);
  },true);
  setTimeout(preparar,500);
  setTimeout(atualizarResumo,1200);
})();
</script>
'''
    s = s.replace('</body>', block + '\n</body>')
    p.write_text(s, encoding='utf-8')

sw = Path('service-worker.js')
ss = sw.read_text(encoding='utf-8')
ss2 = re.sub(r"const CACHE_VERSION = '[^']+';", "const CACHE_VERSION = 'simpla-shell-v14-agenda-remodelada';", ss, count=1)
if ss2 != ss:
    sw.write_text(ss2, encoding='utf-8')
