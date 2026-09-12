from pathlib import Path
import re

idx = Path('index.html')
sw = Path('service-worker.js')
html = idx.read_text(encoding='utf-8')

if 'simpla-radar-retornos-v51' in html:
    raise SystemExit('v51 ja aplicada')

marker = '</body>'
if marker not in html:
    raise SystemExit('body nao encontrado')

block = r'''
<style id="simpla-radar-retornos-v51-css">
  .dash-ret-v51{margin:0 0 24px;background:#fff;border:1px solid #e2e8f0;border-radius:10px;padding:16px;box-shadow:0 2px 4px rgba(0,0,0,.04)}
  .dash-ret-v51-head{display:flex;justify-content:space-between;align-items:flex-start;gap:12px;flex-wrap:wrap;margin-bottom:12px}
  .dash-ret-v51-head h3{margin:0;font-size:15px;color:#1a1c23}
  .dash-ret-v51-head p{margin:4px 0 0;font-size:11px;color:#718096;text-transform:none}
  .dash-ret-v51-head button{padding:8px 11px;border-radius:6px;border:1px solid #cbd5e0;background:#fff;cursor:pointer;font-size:10px;font-weight:800;color:#2d3748}
  .dash-ret-v51-kpis{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:9px;margin-bottom:12px}
  .dash-ret-v51-kpi{padding:10px;border:1px solid #e2e8f0;border-radius:8px;background:#f8fafc}
  .dash-ret-v51-kpi span{display:block;font-size:8px;font-weight:900;color:#718096;margin-bottom:4px}
  .dash-ret-v51-kpi strong{font-size:17px;color:#1a1c23}
  .dash-ret-v51-list{display:grid;gap:7px}
  .dash-ret-v51-item{display:grid;grid-template-columns:minmax(0,1.3fr) minmax(0,1fr) 120px 90px;gap:10px;align-items:center;padding:9px 10px;border:1px solid #edf2f7;border-radius:7px;background:#fff}
  .dash-ret-v51-item b{font-size:11px;color:#2d3748}
  .dash-ret-v51-item span{font-size:10px;color:#718096;text-transform:none}
  .dash-ret-v51-tag{justify-self:start;padding:4px 7px;border-radius:999px;font-size:8px!important;font-weight:900;text-transform:uppercase!important;background:#edf2f7;color:#4a5568!important}
  .dash-ret-v51-tag.atrasado{background:#fff5f5;color:#c53030!important}.dash-ret-v51-tag.hoje{background:#fffaf0;color:#b7791f!important}.dash-ret-v51-tag.proximo{background:#ebf8ff;color:#2b6cb0!important}
  .dash-ret-v51-empty{padding:14px;border:1px dashed #cbd5e0;border-radius:8px;color:#718096;font-size:11px;text-transform:none;text-align:center}
  .dash-ret-v51-foot{margin-top:10px;font-size:9px;color:#718096;text-transform:none;line-height:1.45}
  @media(max-width:760px){.dash-ret-v51-kpis{grid-template-columns:1fr 1fr 1fr}.dash-ret-v51-item{grid-template-columns:1fr 90px}.dash-ret-v51-item .servico{grid-column:1/2}.dash-ret-v51-item .data{grid-column:2/3;grid-row:1/2}.dash-ret-v51-item .dash-ret-v51-tag{grid-column:2/3}}
</style>
<script id="simpla-radar-retornos-v51">
(function(){
  const HORIZONTE = 7;
  let carregando = false;
  function formatarData(v){ if(!v) return '-'; const [y,m,d]=String(v).slice(0,10).split('-'); return `${d}/${m}/${y}`; }
  function garantir(){
    const dash=document.getElementById('dashboard'); if(!dash) return null;
    let box=document.getElementById('dash-ret-v51'); if(box) return box;
    box=document.createElement('div'); box.id='dash-ret-v51'; box.className='dash-ret-v51';
    box.innerHTML=`<div class="dash-ret-v51-head"><div><h3>Radar de Retornos</h3><p>Atendimentos com retorno sugerido ou recorrência configurada e sem novo agendamento para o mesmo serviço.</p></div><button type="button" onclick="carregarRadarRetornosV51()">↻ Atualizar</button></div><div class="dash-ret-v51-kpis"><div class="dash-ret-v51-kpi"><span>ATRASADOS</span><strong id="dash-ret-v51-atrasados">0</strong></div><div class="dash-ret-v51-kpi"><span>RETORNO HOJE</span><strong id="dash-ret-v51-hoje">0</strong></div><div class="dash-ret-v51-kpi"><span>PRÓXIMOS 7 DIAS</span><strong id="dash-ret-v51-proximos">0</strong></div></div><div id="dash-ret-v51-list" class="dash-ret-v51-list"><div class="dash-ret-v51-empty">Carregando oportunidades de retorno...</div></div><div class="dash-ret-v51-foot">Este radar é administrativo. Ele não envia mensagens automaticamente e não utiliza conteúdo técnico ou clínico dos atendimentos.</div>`;
    const insights=document.getElementById('dash-sec-insights');
    if(insights) insights.insertAdjacentElement('beforebegin',box); else dash.appendChild(box);
    return box;
  }
  async function carregar(){
    if(carregando) return;
    const box=garantir(); if(!box) return;
    if(typeof CloudDB==='undefined' || !CloudDB || typeof empresaAtual==='undefined' || !empresaAtual?.id){
      const list=document.getElementById('dash-ret-v51-list'); if(list) list.innerHTML='<div class="dash-ret-v51-empty">Radar disponível quando a empresa estiver conectada à nuvem.</div>'; return;
    }
    carregando=true;
    try{
      const {data,error}=await CloudDB.rpc('listar_oportunidades_retorno',{p_empresa_id:empresaAtual.id,p_horizonte_dias:HORIZONTE});
      if(error) throw error;
      const rows=data||[];
      const atrasados=rows.filter(r=>r.situacao==='ATRASADO').length;
      const hoje=rows.filter(r=>r.situacao==='HOJE').length;
      const proximos=rows.filter(r=>r.situacao==='PROXIMO').length;
      document.getElementById('dash-ret-v51-atrasados').textContent=String(atrasados);
      document.getElementById('dash-ret-v51-hoje').textContent=String(hoje);
      document.getElementById('dash-ret-v51-proximos').textContent=String(proximos);
      const list=document.getElementById('dash-ret-v51-list');
      if(!list) return;
      if(!rows.length){ list.innerHTML='<div class="dash-ret-v51-empty">Nenhum retorno pendente identificado com as regras configuradas.</div>'; return; }
      list.innerHTML=rows.slice(0,12).map(r=>`<div class="dash-ret-v51-item"><div><b>${String(r.cliente_nome||'Sem nome')}</b><br><span>${r.telefone||'Telefone não informado'}</span></div><div class="servico"><b>${String(r.servico_nome||'Serviço')}</b><br><span>Último atendimento: ${formatarData(r.ultimo_atendimento)}</span></div><div class="data"><b>${formatarData(r.retorno_previsto)}</b><br><span>${Number(r.dias_para_retorno)<0?`${Math.abs(Number(r.dias_para_retorno))} dia(s) em atraso`:Number(r.dias_para_retorno)===0?'Hoje':`Em ${r.dias_para_retorno} dia(s)`}</span></div><span class="dash-ret-v51-tag ${String(r.situacao||'').toLowerCase()}">${r.situacao||''}</span></div>`).join('');
      if(rows.length>12) list.insertAdjacentHTML('beforeend',`<div class="dash-ret-v51-empty">Mostrando 12 de ${rows.length} oportunidades. O detalhamento completo será incorporado à Gestão à Vista em etapa posterior.</div>`);
    }catch(err){
      console.error('Radar de retornos:',err);
      const list=document.getElementById('dash-ret-v51-list'); if(list) list.innerHTML='<div class="dash-ret-v51-empty">Não foi possível carregar o Radar de Retornos.</div>';
    }finally{carregando=false;}
  }
  window.carregarRadarRetornosV51=carregar;
  function instalar(){garantir(); setTimeout(carregar,300);}
  if(document.readyState==='loading') document.addEventListener('DOMContentLoaded',()=>setTimeout(instalar,2200)); else setTimeout(instalar,2200);
})();
</script>
'''

html = html.replace(marker, block + '\n' + marker, 1)
idx.write_text(html, encoding='utf-8')

swtxt = sw.read_text(encoding='utf-8')
swtxt, n = re.subn(r"const CACHE_VERSION = '[^']+';", "const CACHE_VERSION = 'simpla-shell-v51-radar-retornos';", swtxt, count=1)
if n != 1:
    raise SystemExit('cache version nao encontrada')
sw.write_text(swtxt, encoding='utf-8')
