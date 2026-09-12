from pathlib import Path
import re

idx=Path('index.html')
sw=Path('service-worker.js')
html=idx.read_text(encoding='utf-8')

if 'simpla-sugestoes-ociosidade-v61' in html:
    raise SystemExit('v61 ja aplicada')

# Expor as janelas detectadas pela v54 para uso seguro por módulos posteriores.
old="function carregar(){garantir();try{itens=detectar();document.getElementById('ocio-v54-total').textContent=String(itens.length);"
new="function carregar(){garantir();try{itens=detectar();window.simplaOportunidadesAgendaV54Rows=itens;document.getElementById('ocio-v54-total').textContent=String(itens.length);"
if old not in html:
    raise SystemExit('carregar v54 nao encontrado')
html=html.replace(old,new,1)

# Adicionar ação de sugestões ao lado de Ver agenda.
oldbtn='<button class="dash-ocio-v54-acao" type="button" onclick="abrirOportunidadeAgendaV54(${i})">Ver agenda</button>'
newbtn='<div style="display:flex;gap:5px;flex-wrap:wrap;justify-content:flex-end"><button class="dash-ocio-v54-acao" type="button" onclick="abrirSugestoesOciosidadeV61(${i})">Sugerir clientes</button><button class="dash-ocio-v54-acao" type="button" onclick="abrirOportunidadeAgendaV54(${i})">Ver agenda</button></div>'
if oldbtn not in html:
    raise SystemExit('botao v54 nao encontrado')
html=html.replace(oldbtn,newbtn,1)

marker='</body>'
block=r'''
<style id="simpla-sugestoes-ociosidade-v61-css">
  .simpla-v61-backdrop{position:fixed;inset:0;z-index:9990;background:rgba(15,23,42,.48);display:none;align-items:center;justify-content:center;padding:18px}
  .simpla-v61-modal{width:min(760px,96vw);max-height:88vh;overflow:auto;background:#fff;border-radius:14px;box-shadow:0 24px 70px rgba(15,23,42,.28);padding:18px;text-transform:none}
  .simpla-v61-head{display:flex;justify-content:space-between;gap:12px;align-items:flex-start;border-bottom:1px solid #edf2f7;padding-bottom:12px;margin-bottom:12px}.simpla-v61-head h3{margin:0;font-size:17px}.simpla-v61-head p{margin:5px 0 0;font-size:11px;color:#718096;line-height:1.45;text-transform:none}.simpla-v61-fechar{border:0;background:#edf2f7;border-radius:7px;padding:7px 10px;cursor:pointer;font-weight:900}
  .simpla-v61-contexto{display:flex;gap:7px;flex-wrap:wrap;margin-bottom:12px}.simpla-v61-chip{padding:6px 8px;border-radius:999px;background:#f7fafc;border:1px solid #e2e8f0;font-size:9px;font-weight:800;color:#4a5568}
  .simpla-v61-list{display:grid;gap:8px}.simpla-v61-item{display:grid;grid-template-columns:minmax(0,1fr) 150px;gap:12px;align-items:center;padding:11px;border:1px solid #e2e8f0;border-radius:9px}.simpla-v61-item h4{margin:0 0 4px;font-size:13px;color:#1a202c}.simpla-v61-item p{margin:0;font-size:10px;color:#718096;line-height:1.45;text-transform:none}.simpla-v61-score{display:inline-flex;margin-top:6px;padding:4px 7px;border-radius:999px;background:#ebf8ff;color:#2b6cb0;font-size:8px;font-weight:900}.simpla-v61-actions{display:flex;gap:6px;justify-content:flex-end;flex-wrap:wrap}.simpla-v61-btn{border:0;border-radius:7px;padding:8px 9px;background:#1a202c;color:#fff;font-size:8px;font-weight:900;cursor:pointer}.simpla-v61-btn.sec{background:#edf2f7;color:#2d3748}.simpla-v61-empty{padding:18px;border:1px dashed #cbd5e0;border-radius:9px;text-align:center;color:#718096;font-size:11px;line-height:1.5;text-transform:none}.simpla-v61-foot{margin-top:11px;font-size:9px;color:#718096;line-height:1.5;text-transform:none}
  @media(max-width:650px){.simpla-v61-item{grid-template-columns:1fr}.simpla-v61-actions{justify-content:flex-start}}
</style>
<div id="simpla-v61-backdrop" class="simpla-v61-backdrop" onclick="if(event.target===this)fecharSugestoesOciosidadeV61()"><div class="simpla-v61-modal"><div class="simpla-v61-head"><div><h3>Clientes com potencial para este horário</h3><p>Ranking administrativo baseado apenas no histórico de agenda e nos retornos já calculados pelo SimplA.</p></div><button class="simpla-v61-fechar" type="button" onclick="fecharSugestoesOciosidadeV61()">×</button></div><div id="simpla-v61-contexto" class="simpla-v61-contexto"></div><div id="simpla-v61-list" class="simpla-v61-list"></div><div class="simpla-v61-foot">Estas são sugestões de gestão, não garantia de interesse ou disponibilidade. Nenhuma mensagem é enviada e nenhum agendamento é criado automaticamente.</div></div></div>
<script id="simpla-sugestoes-ociosidade-v61">
(function(){
  let atuais=[];let janelaAtual=null;
  function arr(nome){try{return Array.isArray(window[nome])?window[nome]:eval(`typeof ${nome}!=='undefined'&&Array.isArray(${nome})?${nome}:[]`)}catch(_){return []}}
  function data(a){return String(a.data||a.data_agendamento||'').slice(0,10)}
  function status(a){return String(a.status||a.situacao||'AGENDADO').toUpperCase()}
  function cli(a){return a.clienteId||a.cliente_id||null}
  function nome(a){return a.clienteNome||a.cliente_nome||'Cliente'}
  function tel(a){return a.telefone||a.whatsapp||''}
  function servId(a){return a.servicoId||a.servico_id||null}
  function servNome(a){return a.servico||a.servicoNome||a.servico_nome||'Serviço'}
  function prof(a){return a.profissionalId||a.profissional_id||null}
  function horaMin(v){const [h,m]=String(v||'00:00').split(':').map(Number);return (h||0)*60+(m||0)}
  function inicio(a){return horaMin(a.horario||a.hora_inicio||a.horaInicio||'00:00')}
  function hoje(){try{return typeof obterHojeLocal==='function'?obterHojeLocal():new Date().toISOString().slice(0,10)}catch(_){return new Date().toISOString().slice(0,10)}}
  function dow(d){const [y,m,dd]=String(d).split('-').map(Number);return new Date(y,m-1,dd).getDay()}
  function br(d){const p=String(d||'').split('-');return p.length===3?`${p[2]}/${p[1]}/${p[0]}`:d}
  function futuroAtivo(clienteId){const h=hoje();return arr('agendamentos').some(a=>String(cli(a)||'')===String(clienteId)&&data(a)>=h&&!['CANCELADO','NAO_COMPARECEU','CONCLUIDO'].includes(status(a)))}
  function mapaRadar(){const m=new Map();const rows=Array.isArray(window.simplaRadarRetornosV51Rows)?window.simplaRadarRetornosV51Rows:[];rows.forEach(r=>{const id=r.cliente_id||r.clienteId;if(!id)return;const s=String(r.situacao||'').toUpperCase();const bonus=s==='ATRASADO'?5:s==='HOJE'?4:s==='PROXIMO'?2:0;m.set(String(id),Math.max(m.get(String(id))||0,bonus))});return m}
  function gerar(j){
    const todos=arr('agendamentos').filter(a=>cli(a)&&data(a)&&data(a)<j.data&&['CONCLUIDO','AGENDADO','SOLICITADO',''].includes(status(a)));
    const servicosDoProf=new Set(todos.filter(a=>String(prof(a)||'')===String(j.profissional_id)).map(a=>String(servId(a)||'')).filter(Boolean));
    const alvoMin=horaMin(j.inicio), radar=mapaRadar(), agrup=new Map();
    todos.forEach(a=>{
      const id=String(cli(a));if(futuroAtivo(id))return;
      const mesmoProf=String(prof(a)||'')===String(j.profissional_id);
      const servComp=servId(a)&&servicosDoProf.has(String(servId(a)));
      if(!mesmoProf&&!servComp)return;
      let score=0, motivos=[];
      if(mesmoProf){score+=5;motivos.push('já atendido por este profissional')}
      if(servComp){score+=3;motivos.push('serviço compatível com o histórico do profissional')}
      if(dow(data(a))===dow(j.data)){score+=3;motivos.push('costuma vir neste dia da semana')}
      const dif=Math.abs(inicio(a)-alvoMin);if(dif<=60){score+=4;motivos.push('horário histórico semelhante')}else if(dif<=120){score+=2;motivos.push('faixa de horário próxima')}
      if(status(a)==='CONCLUIDO')score+=1;
      score+=radar.get(id)||0;if((radar.get(id)||0)>=4)motivos.push('retorno vencido ou previsto para hoje');else if((radar.get(id)||0)>0)motivos.push('retorno próximo');
      const ant=agrup.get(id);const item={cliente_id:cli(a),cliente_nome:nome(a),telefone:tel(a),servico_id:servId(a),servico_nome:servNome(a),score,motivos:[...new Set(motivos)],ultima_data:data(a)};
      if(!ant||item.score>ant.score||(item.score===ant.score&&item.ultima_data>ant.ultima_data))agrup.set(id,item);
    });
    return [...agrup.values()].filter(x=>x.score>=5).sort((a,b)=>b.score-a.score||b.ultima_data.localeCompare(a.ultima_data)).slice(0,12);
  }
  function fechar(){const b=document.getElementById('simpla-v61-backdrop');if(b)b.style.display='none'}window.fecharSugestoesOciosidadeV61=fechar;
  window.abrirSugestoesOciosidadeV61=function(i){
    const rows=Array.isArray(window.simplaOportunidadesAgendaV54Rows)?window.simplaOportunidadesAgendaV54Rows:[];const j=rows[Number(i)];if(!j)return alert('Atualize as oportunidades de agenda e tente novamente.');janelaAtual=j;atuais=gerar(j);
    const ctx=document.getElementById('simpla-v61-contexto');if(ctx)ctx.innerHTML=`<span class="simpla-v61-chip">${j.profissional_nome}</span><span class="simpla-v61-chip">${br(j.data)}</span><span class="simpla-v61-chip">${j.inicio}–${j.fim}</span><span class="simpla-v61-chip">${atuais.length} sugestão(ões)</span>`;
    const list=document.getElementById('simpla-v61-list');if(list){if(!atuais.length)list.innerHTML='<div class="simpla-v61-empty">Ainda não há histórico suficiente para sugerir clientes com segurança para esta janela.</div>';else list.innerHTML=atuais.map((x,n)=>`<div class="simpla-v61-item"><div><h4>${x.cliente_nome}</h4><p>${x.servico_nome} • último histórico em ${br(x.ultima_data)}<br>${x.motivos.slice(0,3).join(' • ')}</p><span class="simpla-v61-score">Compatibilidade ${x.score} pts</span></div><div class="simpla-v61-actions"><button class="simpla-v61-btn sec" onclick="verHistoricoSugestaoV61(${n})">Histórico</button><button class="simpla-v61-btn" onclick="prepararAgendamentoSugestaoV61(${n})">Preparar agendamento</button></div></div>`).join('')}
    const b=document.getElementById('simpla-v61-backdrop');if(b)b.style.display='flex';
  };
  window.verHistoricoSugestaoV61=function(i){const x=atuais[Number(i)];if(!x)return;fechar();try{if(typeof abrirHistoricoCliente==='function')return abrirHistoricoCliente(x.cliente_id)}catch(_){ }try{if(typeof mudarTela==='function')mudarTela('clientes')}catch(_){ }};
  window.prepararAgendamentoSugestaoV61=function(i){const x=atuais[Number(i)];const j=janelaAtual;if(!x||!j)return;fechar();try{if(typeof mudarTela==='function')mudarTela('agenda')}catch(_){ }const d=document.getElementById('agenda-data-filtro');if(d){d.value=j.data;d.dispatchEvent(new Event('change',{bubbles:true}))}const p=document.getElementById('agenda-profissional-filtro');if(p){const opt=[...p.options].find(o=>String(o.value)===String(j.profissional_id));if(opt){p.value=opt.value;p.dispatchEvent(new Event('change',{bubbles:true}))}}setTimeout(()=>{try{if(typeof abrirModalAgendamento==='function')abrirModalAgendamento(j.inicio,j.data,j.profissional_id)}catch(_){ }setTimeout(()=>{try{if(typeof selecionarClienteBusca==='function')selecionarClienteBusca('agenda',x.cliente_id)}catch(_){ }const s=document.getElementById('agenda-servico')||document.getElementById('ag-servico')||document.querySelector('#modal-agendamento select[id*=servico]');if(s&&x.servico_id){const op=[...s.options].find(o=>String(o.value)===String(x.servico_id));if(op)s.value=op.value}},180)},180)};
})();
</script>
'''
if marker not in html:
    raise SystemExit('body nao encontrado')
html=html.replace(marker,block+'\n'+marker,1)
idx.write_text(html,encoding='utf-8')

swtxt=sw.read_text(encoding='utf-8')
swtxt,n=re.subn(r"const CACHE_VERSION = '[^']+';","const CACHE_VERSION = 'simpla-shell-v61-sugestoes-ociosidade';",swtxt,count=1)
if n!=1: raise SystemExit('cache nao encontrado')
sw.write_text(swtxt,encoding='utf-8')
