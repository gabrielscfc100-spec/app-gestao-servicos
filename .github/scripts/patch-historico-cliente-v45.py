from pathlib import Path

idx=Path('index.html')
sw=Path('service-worker.js')
html=idx.read_text(encoding='utf-8')

marker='</body>'
if marker not in html:
    raise SystemExit('body nao encontrado')
if 'simpla-historico-cliente-v45' in html:
    raise SystemExit('v45 ja aplicada')

block=r'''
<style id="simpla-historico-cliente-v45-css">
  .hist-agenda-v45{margin:18px 0;padding-top:14px;border-top:1px solid #e2e8f0}
  .hist-agenda-v45 h4{font-size:14px;color:#4a5568;margin:0 0 10px}
  .hist-agenda-kpis-v45{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:8px;margin-bottom:12px}
  .hist-agenda-kpi-v45{background:#f8fafc;border:1px solid #e2e8f0;border-radius:7px;padding:10px}
  .hist-agenda-kpi-v45 span{display:block;font-size:9px;font-weight:800;color:#718096;margin-bottom:4px}
  .hist-agenda-kpi-v45 strong{font-size:16px;color:#1a1c23}
  .hist-agenda-list-v45{display:flex;flex-direction:column;gap:7px;max-height:260px;overflow:auto}
  .hist-agenda-item-v45{display:grid;grid-template-columns:86px 1fr auto;gap:10px;align-items:center;border:1px solid #e2e8f0;border-radius:7px;padding:9px 10px;background:#fff}
  .hist-agenda-data-v45{font-size:11px;font-weight:800;color:#4a5568}
  .hist-agenda-desc-v45{font-size:11px;color:#2d3748;line-height:1.35;text-transform:none}
  .hist-agenda-status-v45{font-size:9px;font-weight:900;border-radius:99px;padding:4px 7px;white-space:nowrap}
  .hist-agenda-status-v45.agendado{background:#bee3f8;color:#2b6cb0}
  .hist-agenda-status-v45.concluido{background:#c6f6d5;color:#22543d}
  .hist-agenda-status-v45.cancelado{background:#fed7d7;color:#9b2c2c}
  .hist-agenda-status-v45.no-show{background:#feebc8;color:#9c4221}
  .hist-agenda-status-v45.solicitado{background:#e9d8fd;color:#553c9a}
  @media(max-width:600px){.hist-agenda-kpis-v45{grid-template-columns:1fr 1fr}.hist-agenda-item-v45{grid-template-columns:72px 1fr}.hist-agenda-status-v45{grid-column:2;justify-self:start}}
</style>
<script id="simpla-historico-cliente-v45">
(function(){
  function esc(v){return String(v??'').replace(/[&<>"']/g,m=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[m]))}
  function dataBR(v){if(!v)return '-';try{return new Date(String(v).slice(0,10)+'T00:00:00').toLocaleDateString('pt-BR')}catch(_){return String(v)}}
  function statusInfo(s){
    s=String(s||'').toUpperCase();
    if(s==='NAO_COMPARECEU')return ['Não compareceu','no-show'];
    if(s==='CANCELADO')return ['Cancelado','cancelado'];
    if(s==='CONCLUIDO')return ['Concluído','concluido'];
    if(s==='SOLICITADO')return ['Solicitado','solicitado'];
    return ['Agendado','agendado'];
  }
  function garantirBloco(){
    const modal=document.querySelector('#modal-historico-cliente .modal-balao');
    if(!modal)return null;
    let box=document.getElementById('hist-agenda-v45');
    if(box)return box;
    box=document.createElement('div');box.id='hist-agenda-v45';box.className='hist-agenda-v45';
    box.innerHTML=`<h4>Jornada na Agenda</h4><div class="hist-agenda-kpis-v45">
      <div class="hist-agenda-kpi-v45"><span>AGENDAMENTOS</span><strong id="hist-agenda-total-v45">0</strong></div>
      <div class="hist-agenda-kpi-v45"><span>CONCLUÍDOS</span><strong id="hist-agenda-concl-v45">0</strong></div>
      <div class="hist-agenda-kpi-v45"><span>CANCELADOS</span><strong id="hist-agenda-canc-v45">0</strong></div>
      <div class="hist-agenda-kpi-v45"><span>NÃO COMPARECEU</span><strong id="hist-agenda-noshow-v45">0</strong></div>
    </div><div id="hist-agenda-list-v45" class="hist-agenda-list-v45"><div style="font-size:11px;color:#718096;text-transform:none">Carregando histórico da agenda...</div></div>`;
    const tituloTabela=[...modal.querySelectorAll('h4')].find(x=>/Atendimentos na/i.test(x.textContent||''));
    if(tituloTabela)modal.insertBefore(box,tituloTabela);else modal.appendChild(box);
    return box;
  }
  async function buscar(id){
    if(typeof CloudDB!=='undefined'&&CloudDB&&typeof empresaAtual!=='undefined'&&empresaAtual?.cloud&&empresaAtual?.id){
      try{
        const {data,error}=await CloudDB.from('agendamentos').select('*').eq('empresa_id',empresaAtual.id).eq('cliente_id',id).order('data',{ascending:false}).order('horario',{ascending:false});
        if(error)throw error;return data||[];
      }catch(e){console.warn('Histórico de agenda v45: fallback local',e)}
    }
    const lista=(typeof agendamentos!=='undefined'&&Array.isArray(agendamentos))?agendamentos:[];
    return lista.filter(a=>String(a.clienteId||a.cliente_id||'')===String(id));
  }
  async function render(id){
    const box=garantirBloco();if(!box)return;
    const rows=await buscar(id);
    const normal=rows.map(a=>({
      data:a.data||'',horario:String(a.horario||'').slice(0,5),status:a.status||'AGENDADO',
      servico:a.servico_nome||a.servico||'',profissional:a.profissional_nome||'',
      motivo:a.motivo_cancelamento||a.motivoCancelamento||'',presenca:a.presenca_status||a.presencaStatus||''
    }));
    const total=normal.length, concl=normal.filter(a=>a.status==='CONCLUIDO').length,
      canc=normal.filter(a=>a.status==='CANCELADO').length,
      noShow=normal.filter(a=>a.status==='NAO_COMPARECEU'||a.presenca==='NAO_COMPARECEU').length;
    const set=(id,v)=>{const e=document.getElementById(id);if(e)e.textContent=String(v)};
    set('hist-agenda-total-v45',total);set('hist-agenda-concl-v45',concl);set('hist-agenda-canc-v45',canc);set('hist-agenda-noshow-v45',noShow);
    const list=document.getElementById('hist-agenda-list-v45');if(!list)return;
    if(!normal.length){list.innerHTML='<div style="font-size:11px;color:#718096;text-transform:none">Nenhum agendamento vinculado a este cliente.</div>';return}
    list.innerHTML=normal.map(a=>{const [rot,cl]=statusInfo(a.status);const extra=a.motivo?` · Motivo: ${esc(a.motivo)}`:'';return `<div class="hist-agenda-item-v45"><div class="hist-agenda-data-v45">${dataBR(a.data)}<br>${esc(a.horario||'')}</div><div class="hist-agenda-desc-v45"><b>${esc(a.servico||'Serviço não informado')}</b>${extra}</div><span class="hist-agenda-status-v45 ${cl}">${rot}</span></div>`}).join('');
  }
  function instalar(){
    garantirBloco();
    if(typeof abrirHistoricoCliente==='function'&&!abrirHistoricoCliente.__v45){
      const anterior=abrirHistoricoCliente;
      const w=function(id){const r=anterior.apply(this,arguments);Promise.resolve().then(()=>render(id));return r};
      w.__v45=true;window.abrirHistoricoCliente=w;try{abrirHistoricoCliente=w}catch(_){}
    }
  }
  if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',()=>setTimeout(instalar,1800));else setTimeout(instalar,1800);
})();
</script>
'''
html=html.replace(marker,block+'\n'+marker,1)
idx.write_text(html,encoding='utf-8')

swtxt=sw.read_text(encoding='utf-8')
import re
swtxt,n=re.subn(r"const CACHE_VERSION = '[^']+';","const CACHE_VERSION = 'simpla-shell-v45-historico-clientes';",swtxt,count=1)
if n!=1:raise SystemExit('cache version nao encontrada')
sw.write_text(swtxt,encoding='utf-8')
