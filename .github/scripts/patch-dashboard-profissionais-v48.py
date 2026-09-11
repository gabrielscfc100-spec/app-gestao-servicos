from pathlib import Path
import re

idx=Path('index.html')
sw=Path('service-worker.js')
html=idx.read_text(encoding='utf-8')

if 'simpla-dashboard-profissionais-v48' in html:
    raise SystemExit('v48 ja aplicada')
marker='</body>'
if marker not in html:
    raise SystemExit('body nao encontrado')

block=r'''
<style id="simpla-dashboard-profissionais-v48-css">
  .dash-prof-v48{margin:0 0 24px;background:#fff;border:1px solid #e2e8f0;border-radius:10px;padding:16px;box-shadow:0 2px 4px rgba(0,0,0,.04)}
  .dash-prof-v48-head{display:flex;justify-content:space-between;align-items:flex-start;gap:12px;flex-wrap:wrap;margin-bottom:12px}
  .dash-prof-v48-head h3{margin:0;font-size:15px;color:#1a1c23}
  .dash-prof-v48-head p{margin:4px 0 0;font-size:11px;color:#718096;text-transform:none}
  .dash-prof-v48-wrap{overflow-x:auto;border:1px solid #e2e8f0;border-radius:8px}
  .dash-prof-v48-table{width:100%;min-width:820px;margin:0;border-collapse:collapse}
  .dash-prof-v48-table th{font-size:9px;color:#718096;background:#f8fafc;padding:10px;text-align:left;white-space:nowrap}
  .dash-prof-v48-table td{font-size:11px;color:#2d3748;padding:10px;border-top:1px solid #edf2f7;white-space:nowrap}
  .dash-prof-v48-table td:first-child{font-weight:800;color:#1a1c23}
  .dash-prof-v48-table .valor{font-weight:800;color:#2f855a}
  .dash-prof-v48-table .alerta{font-weight:800;color:#c53030}
  .dash-prof-v48-vazio{padding:16px;font-size:11px;color:#718096;text-transform:none}
  @media(max-width:600px){.dash-prof-v48{padding:12px}.dash-prof-v48-head p{font-size:10px}}
</style>
<script id="simpla-dashboard-profissionais-v48">
(function(){
  function moeda(v){return Number(v||0).toLocaleString('pt-BR',{style:'currency',currency:'BRL'})}
  function garantir(){
    const dash=document.getElementById('dashboard');
    if(!dash)return null;
    let box=document.getElementById('dash-prof-v48');
    if(box)return box;
    box=document.createElement('div');box.id='dash-prof-v48';box.className='dash-prof-v48';
    box.innerHTML=`<div class="dash-prof-v48-head"><div><h3>Desempenho por Profissional</h3><p>Atendimentos, faturamento, ticket médio e indicadores de no-show no período selecionado.</p></div></div><div class="dash-prof-v48-wrap"><table class="dash-prof-v48-table"><thead><tr><th>PROFISSIONAL</th><th>ATENDIMENTOS</th><th>FATURAMENTO</th><th>TICKET MÉDIO</th><th>AGENDAMENTOS</th><th>NÃO COMPARECEU</th><th>TAXA NO-SHOW</th></tr></thead><tbody id="dash-prof-v48-body"><tr><td colspan="7" class="dash-prof-v48-vazio">Carregando dados...</td></tr></tbody></table></div>`;
    const agenda=document.getElementById('dash-agenda-v47');
    if(agenda)agenda.insertAdjacentElement('afterend',box);
    else document.getElementById('dash-sec-kpis')?.insertAdjacentElement('afterend',box);
    return box;
  }
  function profLocal(){
    const lista=(typeof profissionais!=='undefined'&&Array.isArray(profissionais))?profissionais:[];
    return lista.map(p=>({id:String(p.id),nome:p.nome||'PROFISSIONAL',ativo:p.ativo!==false}));
  }
  async function buscar(ini,fim){
    let profs=profLocal(), atend=[], agenda=[];
    if(typeof CloudDB!=='undefined'&&CloudDB&&typeof empresaAtual!=='undefined'&&empresaAtual?.cloud&&empresaAtual?.id){
      try{
        const [pRes,aRes,gRes]=await Promise.all([
          CloudDB.from('profissionais').select('id,nome,ativo').eq('empresa_id',empresaAtual.id),
          CloudDB.from('atendimentos').select('profissional_id,total,data').eq('empresa_id',empresaAtual.id).gte('data',ini).lte('data',fim),
          CloudDB.from('agendamentos').select('profissional_id,status,presenca_status,data').eq('empresa_id',empresaAtual.id).gte('data',ini).lte('data',fim)
        ]);
        if(pRes.error)throw pRes.error;if(aRes.error)throw aRes.error;if(gRes.error)throw gRes.error;
        profs=(pRes.data||[]).map(p=>({id:String(p.id),nome:p.nome||'PROFISSIONAL',ativo:p.ativo!==false}));
        atend=aRes.data||[];agenda=gRes.data||[];
        return {profs,atend,agenda};
      }catch(e){console.warn('Dashboard profissionais v48: fallback local',e)}
    }
    const ent=(typeof entradas!=='undefined'&&Array.isArray(entradas))?entradas:[];
    atend=ent.filter(e=>e.data&&e.data>=ini&&e.data<=fim).map(e=>({profissional_id:e.profissionalId||e.profissional_id||null,total:e.total||0,data:e.data}));
    const ag=(typeof agendamentos!=='undefined'&&Array.isArray(agendamentos))?agendamentos:[];
    agenda=ag.filter(a=>a.data&&a.data>=ini&&a.data<=fim).map(a=>({profissional_id:a.profissionalId||a.profissional_id||null,status:a.status||'',presenca_status:a.presencaStatus||a.presenca_status||''}));
    return {profs,atend,agenda};
  }
  async function atualizar(){
    if(!garantir()||typeof obterIntervalosDashboard!=='function')return;
    const {ini,fim}=obterIntervalosDashboard();
    const {profs,atend,agenda}=await buscar(ini,fim);
    const mapa=new Map();
    profs.forEach(p=>mapa.set(String(p.id),{id:String(p.id),nome:p.nome,ativo:p.ativo,at:0,fat:0,ag:0,no:0,comp:0}));
    function item(id){
      const k=id?String(id):'__SEM__';
      if(!mapa.has(k))mapa.set(k,{id:k,nome:k==='__SEM__'?'SEM PROFISSIONAL':'PROFISSIONAL NÃO LOCALIZADO',ativo:true,at:0,fat:0,ag:0,no:0,comp:0});
      return mapa.get(k);
    }
    atend.forEach(a=>{const m=item(a.profissional_id);m.at+=1;m.fat+=Number(a.total||0)});
    agenda.forEach(a=>{
      const m=item(a.profissional_id);m.ag+=1;
      const st=String(a.status||'').toUpperCase(),pr=String(a.presenca_status||'').toUpperCase();
      if(st==='NAO_COMPARECEU'||pr==='NAO_COMPARECEU')m.no+=1;
      else if(st==='CONCLUIDO'||pr==='COMPARECEU')m.comp+=1;
    });
    const rows=[...mapa.values()].filter(x=>x.ativo||x.at||x.ag||x.fat).sort((a,b)=>b.fat-a.fat||b.at-a.at||a.nome.localeCompare(b.nome,'pt-BR'));
    const body=document.getElementById('dash-prof-v48-body');if(!body)return;
    if(!rows.length){body.innerHTML='<tr><td colspan="7" class="dash-prof-v48-vazio">Nenhum dado de profissional no período.</td></tr>';return}
    body.innerHTML=rows.map(x=>{
      const ticket=x.at?x.fat/x.at:0,dec=x.comp+x.no,taxa=dec?(x.no/dec*100):0;
      return `<tr><td>${String(x.nome||'-')}</td><td>${x.at}</td><td class="valor">${moeda(x.fat)}</td><td>${moeda(ticket)}</td><td>${x.ag}</td><td class="${x.no?'alerta':''}">${x.no}</td><td class="${taxa>0?'alerta':''}">${taxa.toFixed(1)}%</td></tr>`;
    }).join('');
  }
  function instalar(){
    garantir();
    if(typeof renderizarDashboard==='function'&&!renderizarDashboard.__v48){
      const anterior=renderizarDashboard;
      const w=function(){const r=anterior.apply(this,arguments);Promise.resolve(r).finally(()=>atualizar());return r};
      w.__v48=true;window.renderizarDashboard=w;try{renderizarDashboard=w}catch(_){}
    }
    setTimeout(atualizar,0);
  }
  if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',()=>setTimeout(instalar,2000));else setTimeout(instalar,2000);
})();
</script>
'''

html=html.replace(marker,block+'\n'+marker,1)
idx.write_text(html,encoding='utf-8')

swtxt=sw.read_text(encoding='utf-8')
swtxt,n=re.subn(r"const CACHE_VERSION = '[^']+';","const CACHE_VERSION = 'simpla-shell-v48-dashboard-profissionais';",swtxt,count=1)
if n!=1: raise SystemExit('cache version nao encontrada')
sw.write_text(swtxt,encoding='utf-8')
