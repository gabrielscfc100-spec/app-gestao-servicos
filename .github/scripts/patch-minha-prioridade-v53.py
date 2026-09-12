from pathlib import Path
import re

idx=Path('index.html')
sw=Path('service-worker.js')
html=idx.read_text(encoding='utf-8')

if 'simpla-minha-prioridade-v53' in html:
    raise SystemExit('v53 ja aplicada')

marker='</body>'
if marker not in html:
    raise SystemExit('body nao encontrado')

block=r'''
<style id="simpla-minha-prioridade-v53-css">
  .dash-prio-v53{margin:0 0 18px;background:#fff;border:1px solid #dbe4ee;border-radius:11px;padding:16px;box-shadow:0 2px 5px rgba(15,23,42,.05)}
  .dash-prio-v53-head{display:flex;justify-content:space-between;gap:12px;align-items:flex-start;flex-wrap:wrap;margin-bottom:12px}
  .dash-prio-v53-head h3{margin:0;font-size:16px;color:#1a1c23}
  .dash-prio-v53-head p{margin:4px 0 0;font-size:11px;color:#718096;text-transform:none;line-height:1.4}
  .dash-prio-v53-refresh{border:1px solid #cbd5e0;background:#fff;border-radius:6px;padding:8px 10px;cursor:pointer;font-size:9px;font-weight:900;color:#2d3748}
  .dash-prio-v53-kpis{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:8px;margin-bottom:12px}
  .dash-prio-v53-kpi{border:1px solid #e2e8f0;border-radius:8px;padding:9px;background:#f8fafc}
  .dash-prio-v53-kpi span{display:block;font-size:8px;font-weight:900;color:#718096;margin-bottom:3px}
  .dash-prio-v53-kpi strong{font-size:18px;color:#1a1c23}
  .dash-prio-v53-list{display:grid;gap:7px}
  .dash-prio-v53-item{display:grid;grid-template-columns:88px minmax(0,1fr) minmax(0,1fr) 92px;gap:9px;align-items:center;border:1px solid #edf2f7;border-radius:8px;padding:9px 10px;background:#fff}
  .dash-prio-v53-item b{font-size:10px;color:#2d3748}
  .dash-prio-v53-item span{font-size:9px;color:#718096;text-transform:none;line-height:1.35}
  .dash-prio-v53-tipo{display:inline-flex;justify-content:center;padding:5px 7px;border-radius:999px;font-size:8px!important;font-weight:900;text-transform:uppercase!important;background:#edf2f7;color:#4a5568!important}
  .dash-prio-v53-tipo.urgente{background:#fff5f5;color:#c53030!important}
  .dash-prio-v53-tipo.atencao{background:#fffaf0;color:#b7791f!important}
  .dash-prio-v53-tipo.info{background:#ebf8ff;color:#2b6cb0!important}
  .dash-prio-v53-acao{border:0;border-radius:6px;padding:7px 8px;background:#1a1c23;color:#fff;font-size:8px;font-weight:900;cursor:pointer}
  .dash-prio-v53-acao:hover{background:var(--cor-accent);color:#1a1c23}
  .dash-prio-v53-empty{border:1px dashed #cbd5e0;border-radius:8px;padding:14px;text-align:center;color:#718096;font-size:11px;text-transform:none}
  .dash-prio-v53-foot{margin-top:9px;color:#718096;font-size:9px;text-transform:none;line-height:1.45}
  @media(max-width:760px){.dash-prio-v53-kpis{grid-template-columns:1fr 1fr}.dash-prio-v53-item{grid-template-columns:82px minmax(0,1fr) 78px}.dash-prio-v53-item .detalhe{grid-column:2}.dash-prio-v53-acao{grid-column:3;grid-row:1/3}}
</style>
<script id="simpla-minha-prioridade-v53">
(function(){
  let carregando=false;
  let itens=[];
  const DIAS_RECENTES=7;
  function hoje(){
    if(typeof obterHojeLocal==='function')return obterHojeLocal();
    const d=new Date();return `${d.getFullYear()}-${String(d.getMonth()+1).padStart(2,'0')}-${String(d.getDate()).padStart(2,'0')}`;
  }
  function dataBR(v){if(!v)return '-';const s=String(v).slice(0,10),p=s.split('-');return p.length===3?`${p[2]}/${p[1]}/${p[0]}`:s}
  function esc(v){return String(v??'').replace(/[&<>"']/g,m=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[m]))}
  function arr(nome){try{return Array.isArray(window[nome])?window[nome]:eval(`typeof ${nome}!=='undefined'&&Array.isArray(${nome})?${nome}:[]`)}catch(_){return []}}
  function nomeAg(a){return a.clienteNome||a.cliente_nome||a.nomeCliente||'Sem identificação'}
  function clienteId(a){return a.clienteId||a.cliente_id||null}
  function servicoNome(a){return a.servico||a.servicoNome||a.servico_nome||'Serviço não informado'}
  function servicoId(a){return a.servicoId||a.servico_id||null}
  function status(a){return String(a.status||a.situacao||'AGENDADO').toUpperCase()}
  function dataAg(a){return String(a.data||a.data_agendamento||'').slice(0,10)}
  function garantia(){
    const dash=document.getElementById('dashboard');if(!dash)return null;
    let box=document.getElementById('dash-prio-v53');if(box)return box;
    box=document.createElement('div');box.id='dash-prio-v53';box.className='dash-prio-v53';
    box.innerHTML=`<div class="dash-prio-v53-head"><div><h3>Minha Prioridade Hoje</h3><p>Uma fila objetiva das situações que mais pedem atenção agora. O SimplA apenas organiza e sugere a próxima ação; nada é enviado ou confirmado automaticamente.</p></div><button class="dash-prio-v53-refresh" type="button" onclick="carregarMinhaPrioridadeV53()">↻ Atualizar</button></div><div class="dash-prio-v53-kpis"><div class="dash-prio-v53-kpi"><span>RETORNOS VENCIDOS / HOJE</span><strong id="prio-v53-ret">0</strong></div><div class="dash-prio-v53-kpi"><span>CONFIRMAÇÕES DE HOJE</span><strong id="prio-v53-sol">0</strong></div><div class="dash-prio-v53-kpi"><span>NÃO COMPARECEU · 7 DIAS</span><strong id="prio-v53-no">0</strong></div><div class="dash-prio-v53-kpi"><span>CANCELAMENTOS · 7 DIAS</span><strong id="prio-v53-can">0</strong></div></div><div id="dash-prio-v53-list" class="dash-prio-v53-list"><div class="dash-prio-v53-empty">Carregando prioridades...</div></div><div class="dash-prio-v53-foot">Itens de ausência e cancelamento aparecem como oportunidades administrativas de acompanhamento, sem presumir o motivo do cliente e sem gerar contato automático.</div>`;
    const radar=document.getElementById('dash-ret-v51');
    const kpis=document.getElementById('dash-sec-kpis');
    if(radar)radar.insertAdjacentElement('beforebegin',box);else if(kpis)kpis.insertAdjacentElement('beforebegin',box);else dash.insertAdjacentElement('afterbegin',box);
    return box;
  }
  function temAgendamentoPosterior(lista,a){
    const cid=clienteId(a);if(!cid)return false;
    const d=dataAg(a);
    return lista.some(x=>String(clienteId(x)||'')===String(cid)&&dataAg(x)>d&&!['CANCELADO','NAO_COMPARECEU'].includes(status(x)));
  }
  function abrirAgenda(data){
    try{if(typeof mudarTela==='function')mudarTela('agenda');}catch(_){document.querySelectorAll('.screen').forEach(x=>x.classList.remove('active'));document.getElementById('agenda')?.classList.add('active')}
    const campo=document.getElementById('agenda-data-filtro');if(campo){campo.value=data||hoje();campo.dispatchEvent(new Event('change',{bubbles:true}))}
    try{if(typeof renderizarAgenda==='function')renderizarAgenda()}catch(_){ }
  }
  window.acaoMinhaPrioridadeV53=function(i){
    const item=itens[Number(i)];if(!item)return;
    if(item.tipo==='RETORNO'){
      const rows=window.simplaRadarRetornosV51Rows||[];
      const idx=rows.findIndex(r=>String(r.cliente_id||'')===String(item.cliente_id||'')&&String(r.servico_id||'')===String(item.servico_id||'')&&String(r.retorno_previsto||'').slice(0,10)===String(item.data||'').slice(0,10));
      if(idx>=0&&typeof window.agendarRetornoV52==='function'){window.agendarRetornoV52(idx);return}
      abrirAgenda(hoje());return;
    }
    if(item.tipo==='SOLICITADO'){abrirAgenda(item.data||hoje());return}
    if(item.cliente_id&&typeof abrirHistoricoCliente==='function'){abrirHistoricoCliente(item.cliente_id);return}
    abrirAgenda(hoje());
  };
  function render(){
    const list=document.getElementById('dash-prio-v53-list');if(!list)return;
    if(!itens.length){list.innerHTML='<div class="dash-prio-v53-empty">Nenhuma prioridade crítica identificada para hoje.</div>';return}
    list.innerHTML=itens.slice(0,12).map((x,i)=>`<div class="dash-prio-v53-item"><span class="dash-prio-v53-tipo ${x.nivel}">${esc(x.rotulo)}</span><div><b>${esc(x.nome)}</b><br><span>${esc(x.resumo)}</span></div><div class="detalhe"><b>${esc(x.servico||'')}</b><br><span>${esc(x.detalhe||'')}</span></div><button class="dash-prio-v53-acao" type="button" onclick="acaoMinhaPrioridadeV53(${i})">${esc(x.acao)}</button></div>`).join('');
    if(itens.length>12)list.insertAdjacentHTML('beforeend',`<div class="dash-prio-v53-empty">Mostrando 12 de ${itens.length} prioridades.</div>`);
  }
  async function carregar(){
    if(carregando)return;garantia();carregando=true;
    try{
      const lista=arr('agendamentos');const h=hoje();const limite=new Date(h+'T00:00:00');limite.setDate(limite.getDate()-DIAS_RECENTES);const limiteISO=limite.toISOString().slice(0,10);
      const solicitados=lista.filter(a=>dataAg(a)===h&&status(a)==='SOLICITADO');
      const noshow=lista.filter(a=>dataAg(a)>=limiteISO&&dataAg(a)<=h&&status(a)==='NAO_COMPARECEU'&&!temAgendamentoPosterior(lista,a));
      const cancelados=lista.filter(a=>dataAg(a)>=limiteISO&&dataAg(a)<=h&&status(a)==='CANCELADO'&&!temAgendamentoPosterior(lista,a));
      let retornos=[];
      if(typeof CloudDB!=='undefined'&&CloudDB&&typeof empresaAtual!=='undefined'&&empresaAtual?.id){
        const {data,error}=await CloudDB.rpc('listar_oportunidades_retorno',{p_empresa_id:empresaAtual.id,p_horizonte_dias:0});
        if(!error)retornos=(data||[]).filter(r=>['ATRASADO','HOJE'].includes(String(r.situacao||'').toUpperCase()));
      }
      document.getElementById('prio-v53-ret').textContent=String(retornos.length);
      document.getElementById('prio-v53-sol').textContent=String(solicitados.length);
      document.getElementById('prio-v53-no').textContent=String(noshow.length);
      document.getElementById('prio-v53-can').textContent=String(cancelados.length);
      itens=[];
      solicitados.forEach(a=>itens.push({tipo:'SOLICITADO',nivel:'urgente',rotulo:'Confirmar hoje',nome:nomeAg(a),servico:servicoNome(a),resumo:`${a.horario||''} · agendamento aguardando confirmação`,detalhe:'Abra a agenda para confirmar ou ajustar.',acao:'Abrir agenda',data:dataAg(a),cliente_id:clienteId(a)}));
      retornos.forEach(r=>itens.push({tipo:'RETORNO',nivel:String(r.situacao).toUpperCase()==='ATRASADO'?'urgente':'atencao',rotulo:String(r.situacao).toUpperCase()==='ATRASADO'?'Retorno vencido':'Retorno hoje',nome:r.cliente_nome||'Sem identificação',servico:r.servico_nome||'Serviço',resumo:String(r.situacao).toUpperCase()==='ATRASADO'?`${Math.abs(Number(r.dias_para_retorno||0))} dia(s) em atraso`:'Retorno sugerido para hoje',detalhe:`Último atendimento: ${dataBR(r.ultimo_atendimento)}`,acao:'Agendar',data:r.retorno_previsto,cliente_id:r.cliente_id,servico_id:r.servico_id}));
      noshow.forEach(a=>itens.push({tipo:'NOSHOW',nivel:'atencao',rotulo:'Não compareceu',nome:nomeAg(a),servico:servicoNome(a),resumo:`Ocorrência em ${dataBR(dataAg(a))}`,detalhe:'Sem novo agendamento identificado depois da ausência.',acao:'Ver histórico',cliente_id:clienteId(a),data:dataAg(a)}));
      cancelados.forEach(a=>itens.push({tipo:'CANCELADO',nivel:'info',rotulo:'Cancelamento',nome:nomeAg(a),servico:servicoNome(a),resumo:`Cancelado em ${dataBR(dataAg(a))}`,detalhe:'Sem novo agendamento identificado depois do cancelamento.',acao:'Ver histórico',cliente_id:clienteId(a),data:dataAg(a)}));
      render();
    }catch(err){console.error('Minha Prioridade Hoje v53:',err);const list=document.getElementById('dash-prio-v53-list');if(list)list.innerHTML='<div class="dash-prio-v53-empty">Não foi possível atualizar as prioridades agora.</div>'}finally{carregando=false}
  }
  window.carregarMinhaPrioridadeV53=carregar;
  function instalar(){garantia();setTimeout(carregar,450)}
  if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',()=>setTimeout(instalar,2400));else setTimeout(instalar,2400);
})();
</script>
'''

html=html.replace(marker,block+'\n'+marker,1)
idx.write_text(html,encoding='utf-8')

swtxt=sw.read_text(encoding='utf-8')
swtxt,n=re.subn(r"const CACHE_VERSION = '[^']+';","const CACHE_VERSION = 'simpla-shell-v53-minha-prioridade';",swtxt,count=1)
if n!=1:
    raise SystemExit('cache version nao encontrada')
sw.write_text(swtxt,encoding='utf-8')
