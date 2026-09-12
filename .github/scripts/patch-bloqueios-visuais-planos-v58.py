from pathlib import Path
import re

idx=Path('index.html')
sw=Path('service-worker.js')
html=idx.read_text(encoding='utf-8')

if 'simpla-bloqueios-planos-v58' in html:
    raise SystemExit('v58 ja aplicada')

marker='</body>'
if marker not in html:
    raise SystemExit('body nao encontrado')

block=r'''
<style id="simpla-bloqueios-planos-v58-css">
  .simpla-entitlement-lock-v58{position:relative!important;overflow:hidden}
  .simpla-entitlement-lock-v58>.simpla-entitlement-overlay-v58{position:absolute;inset:0;z-index:50;display:flex;align-items:center;justify-content:center;padding:18px;background:rgba(248,250,252,.94);backdrop-filter:blur(2px);text-align:center;text-transform:none}
  .simpla-entitlement-overlay-v58-card{max-width:390px;padding:18px;border:1px solid #dbe4ee;border-radius:12px;background:#fff;box-shadow:0 8px 28px rgba(15,23,42,.10)}
  .simpla-entitlement-overlay-v58-tag{display:inline-flex;padding:5px 8px;border-radius:999px;background:#ebf8ff;color:#2b6cb0;font-size:8px;font-weight:900;text-transform:uppercase;margin-bottom:8px}
  .simpla-entitlement-overlay-v58-card h4{margin:0 0 6px;font-size:15px;color:#1a1c23}.simpla-entitlement-overlay-v58-card p{margin:0 0 12px;font-size:10px;line-height:1.5;color:#718096;text-transform:none}
  .simpla-entitlement-overlay-v58-card button{border:0;border-radius:7px;padding:8px 11px;background:#1a1c23;color:#fff;font-size:9px;font-weight:900;cursor:pointer}.simpla-entitlement-overlay-v58-card button:hover{background:var(--cor-accent);color:#1a1c23}
  .simpla-entitlement-lock-v58.simpla-entitlement-radar-v58{min-height:190px}
</style>
<script id="simpla-bloqueios-planos-v58">
(function(){
  const RECURSOS=[
    {id:'dash-prio-v53',recurso:'minha_prioridade_hoje',plano:'Plus',titulo:'Minha Prioridade Hoje',texto:'Organize retornos, confirmações, ausências e cancelamentos em uma fila diária de gestão.'},
    {id:'dash-ocio-v54',recurso:'oportunidades_agenda',plano:'Plus',titulo:'Oportunidades de Agenda',texto:'Identifique janelas livres relevantes e transforme capacidade ociosa em oportunidade de gestão.'},
    {id:'dash-ret-v51',recurso:'radar_retornos_completo',plano:'Plus',titulo:'Radar de Retornos completo',texto:'Veja clientes com retorno previsto, atrasado ou próximo e prepare um novo agendamento com poucos cliques.',radar:true}
  ];
  let aplicando=false;

  function modoTeste(){
    try{return !!empresaAtual?.modo_teste||String(empresaAtual?.plano_codigo||'').toUpperCase()==='TESTE'}catch(_){return false}
  }
  function abrirMeuPlano(){
    try{if(typeof mudarTela==='function')mudarTela('configuracoes')}catch(_){ }
    setTimeout(()=>{
      const el=document.getElementById('simpla-meu-plano-v57');
      if(el){el.scrollIntoView({behavior:'smooth',block:'start'});el.animate([{boxShadow:'0 0 0 0 rgba(49,130,206,0)'},{boxShadow:'0 0 0 4px rgba(49,130,206,.18)'},{boxShadow:'0 2px 5px rgba(15,23,42,.04)'}],{duration:1200})}
    },250);
  }
  window.abrirMeuPlanoV58=abrirMeuPlano;

  function removerLock(el){
    el.classList.remove('simpla-entitlement-lock-v58','simpla-entitlement-radar-v58');
    el.querySelector(':scope > .simpla-entitlement-overlay-v58')?.remove();
  }
  function aplicarLock(el,cfg){
    if(el.querySelector(':scope > .simpla-entitlement-overlay-v58'))return;
    el.classList.add('simpla-entitlement-lock-v58');
    if(cfg.radar)el.classList.add('simpla-entitlement-radar-v58');
    const ov=document.createElement('div');ov.className='simpla-entitlement-overlay-v58';
    ov.innerHTML=`<div class="simpla-entitlement-overlay-v58-card"><span class="simpla-entitlement-overlay-v58-tag">Disponível no ${cfg.plano}</span><h4>${cfg.titulo}</h4><p>${cfg.texto}</p><button type="button" onclick="abrirMeuPlanoV58()">Ver planos</button></div>`;
    el.appendChild(ov);
  }

  async function aplicar(){
    if(aplicando)return;aplicando=true;
    try{
      if(modoTeste()){
        RECURSOS.forEach(cfg=>{const el=document.getElementById(cfg.id);if(el)removerLock(el)});
        return;
      }
      if(typeof empresaPodeUsarRecurso!=='function')return;
      await Promise.all(RECURSOS.map(async cfg=>{
        const el=document.getElementById(cfg.id);if(!el)return;
        const ok=await empresaPodeUsarRecurso(cfg.recurso);
        if(ok)removerLock(el);else aplicarLock(el,cfg);
      }));
    }catch(err){console.warn('Bloqueios visuais por plano v58:',err)}finally{aplicando=false}
  }
  window.aplicarBloqueiosPlanoV58=aplicar;

  const observer=new MutationObserver(()=>{clearTimeout(window.__simplaPlanosV58T);window.__simplaPlanosV58T=setTimeout(aplicar,160)});
  function instalar(){
    observer.observe(document.body,{childList:true,subtree:true});
    setTimeout(aplicar,800);setTimeout(aplicar,2400);setTimeout(aplicar,4500);
  }
  if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',instalar);else instalar();
})();
</script>
'''

html=html.replace(marker,block+'\n'+marker,1)
idx.write_text(html,encoding='utf-8')

swtxt=sw.read_text(encoding='utf-8')
swtxt,n=re.subn(r"const CACHE_VERSION = '[^']+';","const CACHE_VERSION = 'simpla-shell-v58-bloqueios-planos';",swtxt,count=1)
if n!=1:
    raise SystemExit('cache version nao encontrada')
sw.write_text(swtxt,encoding='utf-8')
