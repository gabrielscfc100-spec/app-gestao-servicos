from pathlib import Path
import re

idx=Path('index.html')
sw=Path('service-worker.js')
html=idx.read_text(encoding='utf-8')

if 'simpla-radar-agenda-v52' in html:
    raise SystemExit('v52 ja aplicada')

# Guarda as linhas carregadas pelo Radar para os botoes usarem indice, evitando dados de cliente em onclick.
needle="      const rows=data||[];"
if needle not in html:
    raise SystemExit('linhas do radar v51 nao encontradas')
html=html.replace(needle, needle+"\n      window.simplaRadarRetornosV51Rows=rows;",1)

# Acrescenta uma acao manual em cada oportunidade do Radar.
old="list.innerHTML=rows.slice(0,12).map(r=>`<div class=\"dash-ret-v51-item\"><div><b>${String(r.cliente_nome||'Sem nome')}</b><br><span>${r.telefone||'Telefone não informado'}</span></div><div class=\"servico\"><b>${String(r.servico_nome||'Serviço')}</b><br><span>Último atendimento: ${formatarData(r.ultimo_atendimento)}</span></div><div class=\"data\"><b>${formatarData(r.retorno_previsto)}</b><br><span>${Number(r.dias_para_retorno)<0?`${Math.abs(Number(r.dias_para_retorno))} dia(s) em atraso`:Number(r.dias_para_retorno)===0?'Hoje':`Em ${r.dias_para_retorno} dia(s)`}</span></div><span class=\"dash-ret-v51-tag ${String(r.situacao||'').toLowerCase()}\">${r.situacao||''}</span></div>`).join('');"
new="list.innerHTML=rows.slice(0,12).map((r,i)=>`<div class=\"dash-ret-v51-item\"><div><b>${String(r.cliente_nome||'Sem nome')}</b><br><span>${r.telefone||'Telefone não informado'}</span></div><div class=\"servico\"><b>${String(r.servico_nome||'Serviço')}</b><br><span>Último atendimento: ${formatarData(r.ultimo_atendimento)}</span></div><div class=\"data\"><b>${formatarData(r.retorno_previsto)}</b><br><span>${Number(r.dias_para_retorno)<0?`${Math.abs(Number(r.dias_para_retorno))} dia(s) em atraso`:Number(r.dias_para_retorno)===0?'Hoje':`Em ${r.dias_para_retorno} dia(s)`}</span></div><span class=\"dash-ret-v51-tag ${String(r.situacao||'').toLowerCase()}\">${r.situacao||''}</span><button type=\"button\" class=\"dash-ret-v52-agendar\" onclick=\"agendarRetornoV52(${i})\">Agendar</button></div>`).join('');"
if old not in html:
    raise SystemExit('renderizacao do radar v51 nao encontrada')
html=html.replace(old,new,1)

marker='</body>'
block=r'''
<style id="simpla-radar-agenda-v52-css">
  .dash-ret-v51-item{grid-template-columns:minmax(0,1.25fr) minmax(0,1fr) 120px 82px 82px!important}
  .dash-ret-v52-agendar{padding:7px 9px;border:0;border-radius:6px;background:#1a1c23;color:#fff;cursor:pointer;font-size:9px;font-weight:900;text-transform:uppercase}
  .dash-ret-v52-agendar:hover{background:var(--cor-accent);color:#1a1c23}
  .agenda-prefill-v52{margin:0 0 12px;padding:10px 12px;border:1px solid #bee3f8;background:#ebf8ff;border-radius:7px;color:#2c5282;font-size:11px;text-transform:none;line-height:1.45}
  @media(max-width:760px){.dash-ret-v51-item{grid-template-columns:minmax(0,1fr) 86px!important}.dash-ret-v52-agendar{grid-column:2;justify-self:stretch}.dash-ret-v51-item .dash-ret-v51-tag{grid-column:2}.dash-ret-v51-item .servico{grid-column:1}.dash-ret-v51-item .data{grid-column:2;grid-row:auto}}
</style>
<script id="simpla-radar-agenda-v52">
(function(){
  let prefill=null;
  function hojeLocal(){
    if(typeof obterHojeLocal==='function') return obterHojeLocal();
    const d=new Date(), y=d.getFullYear(), m=String(d.getMonth()+1).padStart(2,'0'), dia=String(d.getDate()).padStart(2,'0');
    return `${y}-${m}-${dia}`;
  }
  function abrirTelaAgenda(){
    try{ if(typeof mudarTela==='function'){ mudarTela('agenda'); return; } }catch(_){ }
    document.querySelectorAll('.screen').forEach(el=>el.classList.remove('active'));
    document.getElementById('agenda')?.classList.add('active');
  }
  function definirServico(){
    if(!prefill) return;
    const select=document.getElementById('agenda-servico');
    if(!select) return;
    const alvoId=String(prefill.servico_id||'');
    const alvoNome=String(prefill.servico_nome||'').trim().toUpperCase();
    const opcao=[...select.options].find(o=>String(o.value)===alvoId || String(o.value).trim().toUpperCase()===alvoNome || String(o.textContent||'').trim().toUpperCase()===alvoNome);
    if(opcao){
      select.value=opcao.value;
      select.dispatchEvent(new Event('change',{bubbles:true}));
    }
  }
  function aplicarPrefillNoModal(){
    if(!prefill || !document.getElementById('modal-agendamento')?.classList.contains('active')) return;
    const tipo=document.getElementById('agenda-tipo-cliente'); if(tipo) tipo.value='cadastrado';
    try{ if(typeof alternarTipoClienteAgendamento==='function') alternarTipoClienteAgendamento(true); }catch(_){ }
    if(prefill.cliente_id && typeof selecionarClienteBusca==='function'){
      selecionarClienteBusca('agenda',prefill.cliente_id);
    }else{
      const campo=document.getElementById('agenda-cliente-busca');
      if(campo) campo.value=prefill.cliente_nome||'';
      const tel=document.getElementById('agenda-telefone'); if(tel) tel.value=prefill.telefone||'';
    }
    definirServico();
    setTimeout(definirServico,80);
    const info=document.getElementById('modal-agenda-horario-txt');
    if(info && !info.dataset.retornoV52){
      info.dataset.retornoV52='1';
      const serv=prefill.servico_nome?` · ${prefill.servico_nome}`:'';
      info.innerText=`${info.innerText}${serv}`;
    }
  }
  window.agendarRetornoV52=function(indice){
    const r=(window.simplaRadarRetornosV51Rows||[])[Number(indice)];
    if(!r) return;
    prefill={
      cliente_id:r.cliente_id||null,
      cliente_nome:r.cliente_nome||'',
      telefone:r.telefone||'',
      servico_id:r.servico_id||null,
      servico_nome:r.servico_nome||'',
      retorno_previsto:r.retorno_previsto||'',
      situacao:r.situacao||''
    };
    window.simplaAgendaPrefillRetornoV52=prefill;
    abrirTelaAgenda();
    const data=document.getElementById('agenda-data-filtro');
    if(data){
      const hoje=hojeLocal();
      const prevista=String(prefill.retorno_previsto||'').slice(0,10);
      data.value=(!prevista || prevista<hoje)?hoje:prevista;
      data.dispatchEvent(new Event('change',{bubbles:true}));
    }
    try{ if(typeof renderizarAgenda==='function') renderizarAgenda(); }catch(_){ }
    let aviso=document.getElementById('agenda-prefill-v52');
    if(!aviso){
      aviso=document.createElement('div'); aviso.id='agenda-prefill-v52'; aviso.className='agenda-prefill-v52';
      const agenda=document.getElementById('agenda'); const scroll=agenda?.querySelector('.agenda-scroll-area');
      (scroll||agenda)?.insertAdjacentElement('afterbegin',aviso);
    }
    if(aviso) aviso.innerHTML=`Retorno preparado para <b>${String(prefill.cliente_nome||'cliente')}</b>${prefill.servico_nome?` — ${String(prefill.servico_nome)}`:''}. Escolha um horário disponível para concluir o agendamento.`;
    setTimeout(()=>document.getElementById('agenda')?.scrollIntoView({behavior:'smooth',block:'start'}),50);
  };

  // Reaproveita o modal atual: ele limpa os campos primeiro e, logo depois, aplicamos o retorno pendente.
  const original=window.abrirModalAgendamento;
  if(typeof original==='function'){
    window.abrirModalAgendamento=function(horario){
      const resultado=original.apply(this,arguments);
      if(prefill) setTimeout(aplicarPrefillNoModal,0);
      return resultado;
    };
  }

  // Ao salvar com sucesso o fluxo existente fecha o modal; limpamos o prefill quando o modal deixa de estar ativo.
  const obs=new MutationObserver(()=>{
    const modal=document.getElementById('modal-agendamento');
    if(prefill && modal && !modal.classList.contains('active') && document.getElementById('agenda-edicao-id')?.value===''){
      // Mantém enquanto o usuário apenas fecha/cancela; novo clique no Radar substitui. Não cria nenhum agendamento automaticamente.
    }
  });
  const modal=document.getElementById('modal-agendamento'); if(modal) obs.observe(modal,{attributes:true,attributeFilter:['class']});
})();
</script>
'''
if marker not in html: raise SystemExit('body nao encontrado')
html=html.replace(marker,block+'\n'+marker,1)
idx.write_text(html,encoding='utf-8')

swtxt=sw.read_text(encoding='utf-8')
swtxt,n=re.subn(r"const CACHE_VERSION = '[^']+';","const CACHE_VERSION = 'simpla-shell-v52-radar-agenda';",swtxt,count=1)
if n!=1: raise SystemExit('cache version nao encontrada')
sw.write_text(swtxt,encoding='utf-8')
