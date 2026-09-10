from pathlib import Path
import re

p=Path('index.html')
s=p.read_text(encoding='utf-8')
marker='simpla-agendamento-atendimento-v20'
if marker in s:
    raise SystemExit('v20 ja aplicada')

block=r'''
<style id="simpla-agendamento-atendimento-v20">
#atendimento .origem-atendimento-v20{background:#fff;border:1px solid #e2e8f0;border-radius:12px;padding:16px;margin:0 0 14px;box-shadow:0 2px 8px rgba(26,28,35,.04)}
#atendimento .origem-atendimento-v20 h3{margin:0 0 4px;font-size:14px;color:#1a1c23}
#atendimento .origem-atendimento-v20 .origem-ajuda{margin:0 0 12px;font-size:11px;color:#718096;text-transform:none;line-height:1.45}
#atendimento .origem-opcoes-v20{display:grid;grid-template-columns:1fr 1fr;gap:8px;margin-bottom:12px}
#atendimento .origem-opcao-v20{border:1px solid #cbd5e0;background:#fff;border-radius:9px;padding:11px 12px;cursor:pointer;font-weight:700;font-size:12px;color:#475569;text-align:left}
#atendimento .origem-opcao-v20.active{border-color:#3182ce;background:#ebf8ff;color:#2b6cb0;box-shadow:0 0 0 2px rgba(49,130,206,.08)}
#atendimento .agenda-hoje-v20{display:grid;gap:8px}
#atendimento .agenda-hoje-card-v20{display:grid;grid-template-columns:76px minmax(0,1fr) auto;gap:12px;align-items:center;border:1px solid #e2e8f0;border-radius:10px;padding:11px 12px;background:#f8fafc}
#atendimento .agenda-hoje-card-v20.selected{border-color:#3182ce;background:#ebf8ff}
#atendimento .agenda-hoje-hora-v20{font-size:16px;font-weight:800;color:#1a1c23}
#atendimento .agenda-hoje-info-v20{min-width:0}
#atendimento .agenda-hoje-info-v20 strong{display:block;font-size:12px;color:#1a1c23;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
#atendimento .agenda-hoje-info-v20 span{display:block;margin-top:3px;font-size:10px;color:#718096;text-transform:none;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
#atendimento .agenda-hoje-card-v20 button{border:0;background:#1a1c23;color:#fff;border-radius:7px;min-height:36px;padding:8px 11px;font-size:10px;font-weight:700;cursor:pointer}
#atendimento .agenda-hoje-card-v20 button:disabled{background:#cbd5e0;color:#64748b;cursor:not-allowed}
#atendimento .agenda-hoje-vazio-v20{border:1px dashed #cbd5e0;border-radius:9px;padding:14px;text-align:center;color:#718096;font-size:11px;text-transform:none}
#atendimento .agenda-hoje-resumo-v20{display:flex;justify-content:space-between;align-items:center;gap:8px;margin:0 0 8px;font-size:10px;color:#718096}
#atendimento .agenda-hoje-resumo-v20 b{color:#334155}
@media(max-width:600px){
 #atendimento .origem-atendimento-v20{padding:12px;margin-bottom:12px}
 #atendimento .origem-opcoes-v20{grid-template-columns:1fr}
 #atendimento .agenda-hoje-card-v20{grid-template-columns:64px minmax(0,1fr);gap:8px}
 #atendimento .agenda-hoje-card-v20 button{grid-column:1/-1;width:100%;min-height:42px}
}
</style>
<script id="simpla-agendamento-atendimento-v20-script">
(function(){
  let modoOrigem='agenda';

  function hoje(){
    try{return typeof obterHojeLocal==='function'?obterHojeLocal():new Date().toISOString().slice(0,10);}catch(e){return new Date().toISOString().slice(0,10);}
  }
  function jaRecebido(id){
    try{return typeof entradaJaGeradaPorAgendamento==='function'&&entradaJaGeradaPorAgendamento(id);}catch(e){return false;}
  }
  function nomeProfissional(a){
    if(a?.profissionalNome) return a.profissionalNome;
    try{return (profissionais||[]).find(p=>String(p.id)===String(a?.profissionalId||a?.profissional_id||''))?.nome||'Profissional não informado';}catch(e){return 'Profissional não informado';}
  }
  function listaHoje(){
    const data=hoje();
    try{
      return (agendamentos||[]).filter(a=>String(a.data||'')===data).sort((a,b)=>String(a.horario||'').localeCompare(String(b.horario||'')));
    }catch(e){return [];}
  }
  function escapar(v){return String(v??'').replace(/[&<>'"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;',"'":'&#39;','"':'&quot;'}[c]));}

  function garantir(){
    const tela=document.getElementById('atendimento');
    const header=tela?.querySelector('.registro-atendimento-header');
    if(!tela||!header) return null;
    let box=document.getElementById('origem-atendimento-v20');
    if(box) return box;
    box=document.createElement('section');
    box.id='origem-atendimento-v20';
    box.className='origem-atendimento-v20';
    box.innerHTML=`
      <h3>Origem do atendimento</h3>
      <p class="origem-ajuda">Use um agendamento do dia para preencher o atendimento automaticamente ou registre um atendimento sem agendamento.</p>
      <div class="origem-opcoes-v20">
        <button type="button" class="origem-opcao-v20 active" data-origem="agenda">Agendamento de hoje</button>
        <button type="button" class="origem-opcao-v20" data-origem="avulso">Atendimento sem agendamento</button>
      </div>
      <div id="agenda-hoje-area-v20">
        <div class="agenda-hoje-resumo-v20"><b>Agendamentos de hoje</b><span id="agenda-hoje-contagem-v20"></span></div>
        <div id="agenda-hoje-lista-v20" class="agenda-hoje-v20"></div>
      </div>`;
    header.insertAdjacentElement('afterend',box);
    box.querySelectorAll('[data-origem]').forEach(btn=>btn.addEventListener('click',()=>mudarModo(btn.dataset.origem)));
    return box;
  }

  function mudarModo(modo){
    modoOrigem=modo==='avulso'?'avulso':'agenda';
    const box=garantir(); if(!box) return;
    box.querySelectorAll('[data-origem]').forEach(b=>b.classList.toggle('active',b.dataset.origem===modoOrigem));
    const area=document.getElementById('agenda-hoje-area-v20');
    if(area) area.style.display=modoOrigem==='agenda'?'block':'none';
    if(modoOrigem==='avulso'){
      try{agendamentoEmRecebimentoId=null;}catch(e){}
      document.getElementById('aviso-recebimento-agenda')?.remove();
    }
    renderizar();
  }

  function renderizar(){
    const box=garantir(); if(!box) return;
    const lista=document.getElementById('agenda-hoje-lista-v20');
    const contador=document.getElementById('agenda-hoje-contagem-v20');
    if(!lista) return;
    const todos=listaHoje();
    const disponiveis=todos.filter(a=>String(a.status||'').toUpperCase()==='AGENDADO'&&!jaRecebido(a.id));
    const pendentes=todos.filter(a=>String(a.status||'').toUpperCase()==='SOLICITADO'&&!jaRecebido(a.id));
    if(contador) contador.textContent=`${disponiveis.length} disponível${disponiveis.length===1?'':'is'}`;
    const itens=[...disponiveis,...pendentes];
    if(!itens.length){
      lista.innerHTML='<div class="agenda-hoje-vazio-v20">Nenhum agendamento disponível para atendimento hoje.</div>';
      return;
    }
    lista.innerHTML=itens.map(a=>{
      const st=String(a.status||'').toUpperCase();
      const pend=st==='SOLICITADO';
      const selected=String(window.agendamentoEmRecebimentoId??agendamentoEmRecebimentoId??'')===String(a.id);
      const serv=a.servico||a.servicoNome||'Serviço não informado';
      return `<div class="agenda-hoje-card-v20 ${selected?'selected':''}" data-agendamento="${escapar(a.id)}">
        <div class="agenda-hoje-hora-v20">${escapar(String(a.horario||'').slice(0,5))}</div>
        <div class="agenda-hoje-info-v20"><strong>${escapar(a.clienteNome||'Cliente')}</strong><span>${escapar(serv)} • ${escapar(nomeProfissional(a))}${pend?' • aguardando confirmação':''}</span></div>
        <button type="button" ${pend?'disabled':''}>${selected?'Selecionado':'Usar agendamento'}</button>
      </div>`;
    }).join('');
    lista.querySelectorAll('.agenda-hoje-card-v20:not(:has(button:disabled))').forEach(card=>{
      card.querySelector('button')?.addEventListener('click',async()=>{
        const id=card.dataset.agendamento;
        if(!id||typeof iniciarRecebimentoAgendamento!=='function') return;
        modoOrigem='agenda';
        await iniciarRecebimentoAgendamento(id);
        setTimeout(renderizar,60);
      });
    });
  }

  function envolver(){
    if(typeof window.abrirRegistroAtendimento==='function'&&!window.abrirRegistroAtendimento.__v20){
      const original=window.abrirRegistroAtendimento;
      const nova=function(){const r=original.apply(this,arguments);setTimeout(()=>{garantir();renderizar();},40);return r;};
      nova.__v20=true; window.abrirRegistroAtendimento=nova;
    }
    if(typeof window.iniciarRecebimentoAgendamento==='function'&&!window.iniciarRecebimentoAgendamento.__v20){
      const original=window.iniciarRecebimentoAgendamento;
      const nova=async function(){const r=await original.apply(this,arguments);modoOrigem='agenda';setTimeout(renderizar,30);return r;};
      nova.__v20=true; window.iniciarRecebimentoAgendamento=nova;
    }
    if(typeof window.lancarEntrada==='function'&&!window.lancarEntrada.__v20){
      const original=window.lancarEntrada;
      const nova=async function(){const r=await original.apply(this,arguments);setTimeout(renderizar,80);return r;};
      nova.__v20=true; window.lancarEntrada=nova;
    }
  }

  function iniciar(){garantir();envolver();renderizar();}
  if(document.readyState==='loading') document.addEventListener('DOMContentLoaded',()=>setTimeout(iniciar,100)); else setTimeout(iniciar,100);
  window.addEventListener('focus',()=>setTimeout(renderizar,80));
  document.addEventListener('visibilitychange',()=>{if(!document.hidden)setTimeout(renderizar,80);});
  document.addEventListener('click',e=>{if(e.target.closest('#menu-btn-atendimento,.bottom-nav-atendimento,[data-tela="atendimento"]'))setTimeout(()=>{envolver();renderizar();},100);},true);
  setTimeout(envolver,700); setTimeout(envolver,1800);
})();
</script>
'''

s=s.replace('</body>',block+'\n</body>')
p.write_text(s,encoding='utf-8')

sw=Path('service-worker.js')
ss=sw.read_text(encoding='utf-8')
ss=re.sub(r"const CACHE_VERSION = '[^']+';","const CACHE_VERSION = 'simpla-shell-v20-agendamento-atendimento';",ss,count=1)
sw.write_text(ss,encoding='utf-8')
