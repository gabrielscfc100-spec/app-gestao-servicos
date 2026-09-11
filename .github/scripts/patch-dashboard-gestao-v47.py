from pathlib import Path
import re

idx=Path('index.html')
sw=Path('service-worker.js')
html=idx.read_text(encoding='utf-8')

if 'simpla-dashboard-agenda-v47' in html:
    raise SystemExit('v47 ja aplicada')
marker='</body>'
if marker not in html:
    raise SystemExit('body nao encontrado')

block=r'''
<style id="simpla-dashboard-agenda-v47-css">
  .dash-agenda-v47{margin:0 0 24px;background:#fff;border:1px solid #e2e8f0;border-radius:10px;padding:16px;box-shadow:0 2px 4px rgba(0,0,0,.04)}
  .dash-agenda-v47-head{display:flex;justify-content:space-between;align-items:flex-start;gap:12px;flex-wrap:wrap;margin-bottom:12px}
  .dash-agenda-v47-head h3{margin:0;font-size:15px;color:#1a1c23}
  .dash-agenda-v47-head p{margin:4px 0 0;font-size:11px;color:#718096;text-transform:none}
  .dash-agenda-v47-grid{display:grid;grid-template-columns:repeat(6,minmax(0,1fr));gap:10px}
  .dash-agenda-v47-kpi{border:1px solid #e2e8f0;border-radius:8px;padding:11px;background:#f8fafc;min-width:0}
  .dash-agenda-v47-kpi span{display:block;font-size:9px;font-weight:800;color:#718096;margin-bottom:5px}
  .dash-agenda-v47-kpi strong{display:block;font-size:18px;color:#1a1c23;line-height:1.1}
  .dash-agenda-v47-kpi small{display:block;margin-top:5px;font-size:9px;color:#718096;text-transform:none;line-height:1.3}
  .dash-agenda-v47-kpi.alerta strong{color:#c53030}
  .dash-agenda-v47-kpi.ok strong{color:#2f855a}
  @media(max-width:1100px){.dash-agenda-v47-grid{grid-template-columns:repeat(3,minmax(0,1fr))}}
  @media(max-width:600px){.dash-agenda-v47-grid{grid-template-columns:1fr 1fr}.dash-agenda-v47{padding:12px}}
</style>
<script id="simpla-dashboard-agenda-v47">
(function(){
  function garantir(){
    const dash=document.getElementById('dashboard');
    const kpis=document.getElementById('dash-sec-kpis');
    if(!dash||!kpis)return null;
    let box=document.getElementById('dash-agenda-v47');
    if(box)return box;
    box=document.createElement('div');
    box.id='dash-agenda-v47';box.className='dash-agenda-v47';
    box.innerHTML=`<div class="dash-agenda-v47-head"><div><h3>Agenda & Comparecimento</h3><p>Indicadores do período selecionado no Dashboard, incluindo cancelamentos e no-show.</p></div></div><div class="dash-agenda-v47-grid">
      <div class="dash-agenda-v47-kpi"><span>AGENDAMENTOS</span><strong id="dash-ag-v47-total">0</strong><small>Total criado no período</small></div>
      <div class="dash-agenda-v47-kpi ok"><span>CONCLUÍDOS</span><strong id="dash-ag-v47-concl">0</strong><small>Atendimentos finalizados</small></div>
      <div class="dash-agenda-v47-kpi"><span>CANCELADOS</span><strong id="dash-ag-v47-canc">0</strong><small>Agendamentos cancelados</small></div>
      <div class="dash-agenda-v47-kpi alerta"><span>NÃO COMPARECEU</span><strong id="dash-ag-v47-noshow">0</strong><small>Faltas registradas</small></div>
      <div class="dash-agenda-v47-kpi alerta"><span>TAXA DE NO-SHOW</span><strong id="dash-ag-v47-taxa-no">0%</strong><small>Faltas ÷ presenças decididas</small></div>
      <div class="dash-agenda-v47-kpi ok"><span>TAXA DE COMPARECIMENTO</span><strong id="dash-ag-v47-taxa-comp">0%</strong><small>Comparecimentos ÷ presenças decididas</small></div>
    </div>`;
    kpis.insertAdjacentElement('afterend',box);
    return box;
  }
  function set(id,v){const e=document.getElementById(id);if(e)e.textContent=String(v)}
  function normalizar(a){
    return {
      status:String(a.status||'').toUpperCase(),
      presenca:String(a.presenca_status||a.presencaStatus||'').toUpperCase(),
      data:String(a.data||'').slice(0,10)
    };
  }
  async function buscar(ini,fim){
    if(typeof CloudDB!=='undefined'&&CloudDB&&typeof empresaAtual!=='undefined'&&empresaAtual?.cloud&&empresaAtual?.id){
      try{
        const {data,error}=await CloudDB.from('agendamentos')
          .select('id,data,status,presenca_status')
          .eq('empresa_id',empresaAtual.id)
          .gte('data',ini).lte('data',fim);
        if(error)throw error;
        return (data||[]).map(normalizar);
      }catch(e){console.warn('Dashboard Agenda v47: fallback local',e)}
    }
    const lista=(typeof agendamentos!=='undefined'&&Array.isArray(agendamentos))?agendamentos:[];
    return lista.map(normalizar).filter(a=>a.data&&a.data>=ini&&a.data<=fim);
  }
  async function atualizar(){
    if(!garantir())return;
    if(typeof obterIntervalosDashboard!=='function')return;
    const {ini,fim}=obterIntervalosDashboard();
    const rows=await buscar(ini,fim);
    const total=rows.length;
    const concl=rows.filter(a=>a.status==='CONCLUIDO').length;
    const canc=rows.filter(a=>a.status==='CANCELADO').length;
    const noShow=rows.filter(a=>a.status==='NAO_COMPARECEU'||a.presenca==='NAO_COMPARECEU').length;
    const compareceu=rows.filter(a=>a.presenca==='COMPARECEU'||a.status==='CONCLUIDO').length;
    const decididas=compareceu+noShow;
    const taxaNo=decididas?(noShow/decididas*100):0;
    const taxaComp=decididas?(compareceu/decididas*100):0;
    set('dash-ag-v47-total',total);
    set('dash-ag-v47-concl',concl);
    set('dash-ag-v47-canc',canc);
    set('dash-ag-v47-noshow',noShow);
    set('dash-ag-v47-taxa-no',`${taxaNo.toFixed(1)}%`);
    set('dash-ag-v47-taxa-comp',`${taxaComp.toFixed(1)}%`);
  }
  function instalar(){
    garantir();
    if(typeof renderizarDashboard==='function'&&!renderizarDashboard.__v47){
      const anterior=renderizarDashboard;
      const w=function(){const r=anterior.apply(this,arguments);Promise.resolve(r).finally(()=>atualizar());return r};
      w.__v47=true;window.renderizarDashboard=w;try{renderizarDashboard=w}catch(_){}
    }
    setTimeout(atualizar,0);
  }
  if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',()=>setTimeout(instalar,1900));else setTimeout(instalar,1900);
})();
</script>
'''

html=html.replace(marker,block+'\n'+marker,1)
idx.write_text(html,encoding='utf-8')

swtxt=sw.read_text(encoding='utf-8')
swtxt,n=re.subn(r"const CACHE_VERSION = '[^']+';","const CACHE_VERSION = 'simpla-shell-v47-dashboard-agenda';",swtxt,count=1)
if n!=1:
    raise SystemExit('cache version nao encontrada')
sw.write_text(swtxt,encoding='utf-8')
