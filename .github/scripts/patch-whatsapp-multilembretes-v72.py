from pathlib import Path
import re

idx=Path('index.html')
sw=Path('service-worker.js')
html=idx.read_text(encoding='utf-8')

if 'simpla-whatsapp-multilembretes-v72' in html:
    raise SystemExit('v72 ja aplicada')

marker='</body>'
if marker not in html:
    raise SystemExit('body nao encontrado')

block=r'''
<style id="simpla-whatsapp-multilembretes-v72-css">
  #wa-rule-card-lembrete{display:none!important}
  .simpla-wa-reminders-v72{grid-column:1/-1;border:1px solid #e2e8f0;border-radius:10px;background:#f8fafc;padding:13px}
  .simpla-wa-reminders-v72-head{display:flex;justify-content:space-between;gap:12px;align-items:flex-start;flex-wrap:wrap}
  .simpla-wa-reminders-v72-title{font-size:12px;font-weight:900;color:#2d3748;text-transform:none}
  .simpla-wa-reminders-v72-desc{font-size:9px;color:#718096;line-height:1.4;margin-top:2px;text-transform:none}
  .simpla-wa-reminders-v72-add{border:0;border-radius:7px;padding:9px 11px;background:#2d3748;color:#fff;font-size:9px;font-weight:900;cursor:pointer}
  .simpla-wa-reminders-v72-list{display:grid;gap:9px;margin-top:11px}
  .simpla-wa-reminder-v72{border:1px solid #dbe4ee;border-radius:9px;background:#fff;padding:11px}
  .simpla-wa-reminder-v72-top{display:flex;justify-content:space-between;gap:10px;align-items:center;margin-bottom:9px}
  .simpla-wa-reminder-v72-name{font-size:10px;font-weight:900;color:#4a5568;text-transform:none}
  .simpla-wa-reminder-v72-fields{display:grid;grid-template-columns:1.2fr 1fr 1fr 1fr;gap:8px}
  .simpla-wa-reminder-v72-field label{display:block;font-size:8px;font-weight:900;color:#718096;margin-bottom:4px;text-transform:uppercase}
  .simpla-wa-reminder-v72-field select,.simpla-wa-reminder-v72-field input{width:100%;padding:8px;border:1px solid #cbd5e0;border-radius:6px;background:#fff;font-size:11px;text-transform:none}
  .simpla-wa-reminder-v72-actions{display:flex;justify-content:space-between;gap:8px;align-items:center;flex-wrap:wrap;margin-top:9px}
  .simpla-wa-reminder-v72-actions-left{display:flex;gap:7px;align-items:center;flex-wrap:wrap}
  .simpla-wa-reminder-v72-save,.simpla-wa-reminder-v72-delete{border:0;border-radius:6px;padding:7px 9px;font-size:8px;font-weight:900;cursor:pointer}
  .simpla-wa-reminder-v72-save{background:#1a1c23;color:#fff}
  .simpla-wa-reminder-v72-delete{background:#fff5f5;color:#c53030}
  .simpla-wa-reminder-v72-msg{font-size:9px;color:#718096;text-transform:none}
  .simpla-wa-reminders-v72-empty{padding:12px;border:1px dashed #cbd5e0;border-radius:8px;text-align:center;color:#718096;font-size:10px;text-transform:none}
  .simpla-wa-reminders-v72-note{margin-top:9px;font-size:9px;color:#718096;line-height:1.4;text-transform:none}
  @media(max-width:900px){.simpla-wa-reminder-v72-fields{grid-template-columns:1fr 1fr}}
  @media(max-width:560px){.simpla-wa-reminder-v72-fields{grid-template-columns:1fr}}
</style>

<script id="simpla-whatsapp-multilembretes-v72">
(function(){
  let lembretes=[];

  const OPCOES=[
    [15,'15 minutos antes'],
    [30,'30 minutos antes'],
    [60,'1 hora antes'],
    [120,'2 horas antes'],
    [360,'6 horas antes'],
    [720,'12 horas antes'],
    [1440,'24 horas antes'],
    [2880,'48 horas antes'],
    [4320,'3 dias antes'],
    [10080,'7 dias antes']
  ];

  function esc(v){return String(v??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]))}

  function garantir(){
    const grid=document.getElementById('simpla-wa-rules-v68-grid');
    if(!grid)return null;
    let box=document.getElementById('simpla-wa-reminders-v72');
    if(box)return box;

    box=document.createElement('section');
    box.id='simpla-wa-reminders-v72';
    box.className='simpla-wa-reminders-v72';
    box.innerHTML='<div class="simpla-wa-reminders-v72-head"><div><div class="simpla-wa-reminders-v72-title">Lembretes do agendamento</div><div class="simpla-wa-reminders-v72-desc">Crie quantos lembretes forem necessários, cada um com antecedência e janela de envio próprias.</div></div><button type="button" class="simpla-wa-reminders-v72-add" onclick="adicionarLembreteWhatsAppV72()">+ Adicionar lembrete</button></div><div id="simpla-wa-reminders-v72-list" class="simpla-wa-reminders-v72-list"></div><div class="simpla-wa-reminders-v72-note">Cada lembrete enviado conta individualmente na franquia mensal do WhatsApp.</div>';

    const old=document.getElementById('wa-rule-card-lembrete');
    if(old)old.insertAdjacentElement('afterend',box);else grid.appendChild(box);
    return box;
  }

  function labelAntecedencia(min){
    const o=OPCOES.find(x=>x[0]===Number(min));
    return o?o[1]:String(min)+' minutos antes';
  }

  function options(v){
    const valor=Number(v||1440);
    const arr=[...OPCOES];
    if(!arr.some(x=>x[0]===valor))arr.unshift([valor,valor+' minutos antes']);
    return arr.map(([n,t])=>'<option value="'+n+'" '+(n===valor?'selected':'')+'>'+t+'</option>').join('');
  }

  function render(){
    const list=document.getElementById('simpla-wa-reminders-v72-list');if(!list)return;
    if(!lembretes.length){
      list.innerHTML='<div class="simpla-wa-reminders-v72-empty">Nenhum lembrete configurado. Clique em “+ Adicionar lembrete”.</div>';
      return;
    }
    list.innerHTML=lembretes.map((r,i)=>{
      const key=r.id||('novo-'+i);
      return '<div class="simpla-wa-reminder-v72" data-key="'+esc(key)+'">'+
        '<div class="simpla-wa-reminder-v72-top"><div class="simpla-wa-reminder-v72-name">Lembrete '+(i+1)+' · '+esc(labelAntecedencia(r.antecedencia_minutos))+'</div><label style="display:flex;align-items:center;gap:7px;font-size:9px;color:#4a5568;text-transform:none"><input id="wa72-ativo-'+i+'" type="checkbox" '+(r.ativo!==false?'checked':'')+'> Ativo</label></div>'+
        '<div class="simpla-wa-reminder-v72-fields">'+
          '<div class="simpla-wa-reminder-v72-field"><label>Antecedência</label><select id="wa72-ant-'+i+'">'+options(r.antecedencia_minutos)+'</select></div>'+
          '<div class="simpla-wa-reminder-v72-field"><label>Início da janela</label><input id="wa72-ini-'+i+'" type="time" value="'+esc(String(r.horario_inicio||'08:00').slice(0,5))+'"></div>'+
          '<div class="simpla-wa-reminder-v72-field"><label>Fim da janela</label><input id="wa72-fim-'+i+'" type="time" value="'+esc(String(r.horario_fim||'20:00').slice(0,5))+'"></div>'+
          '<div class="simpla-wa-reminder-v72-field"><label>Evitar duplicidade</label><select id="wa72-dup-'+i+'"><option value="true" '+(r.bloquear_duplicidade!==false?'selected':'')+'>Sim</option><option value="false" '+(r.bloquear_duplicidade===false?'selected':'')+'>Não</option></select></div>'+
        '</div>'+
        '<div class="simpla-wa-reminder-v72-actions"><div class="simpla-wa-reminder-v72-actions-left"><button type="button" class="simpla-wa-reminder-v72-save" onclick="salvarLembreteWhatsAppV72('+i+')">Salvar lembrete</button>'+(r.id?'<button type="button" class="simpla-wa-reminder-v72-delete" onclick="excluirLembreteWhatsAppV72('+i+')">Excluir</button>':'')+'</div><span id="wa72-msg-'+i+'" class="simpla-wa-reminder-v72-msg"></span></div>'+
      '</div>';
    }).join('');
  }

  async function permitido(){
    if(typeof CloudDB==='undefined'||!CloudDB||typeof empresaAtual==='undefined'||!empresaAtual?.id)return false;
    const {data:perfil}=await CloudDB.rpc('perfil_na_empresa',{p_empresa_id:empresaAtual.id});
    if(String(perfil||'').toUpperCase()!=='ADMIN')return false;
    return typeof empresaPodeUsarRecurso==='function'?await empresaPodeUsarRecurso('whatsapp_operacional'):false;
  }

  async function carregar(){
    garantir();
    if(!await permitido())return;
    try{
      const {data,error}=await CloudDB.from('whatsapp_lembretes_agendamento')
        .select('id,ativo,antecedencia_minutos,horario_inicio,horario_fim,bloquear_duplicidade,ordem')
        .eq('empresa_id',empresaAtual.id)
        .order('ordem',{ascending:true})
        .order('antecedencia_minutos',{ascending:false});
      if(error)throw error;
      lembretes=Array.isArray(data)?data:[];
      render();
    }catch(err){
      console.error('Lembretes WhatsApp v72:',err);
      const list=document.getElementById('simpla-wa-reminders-v72-list');
      if(list)list.innerHTML='<div class="simpla-wa-reminders-v72-empty">Não foi possível carregar os lembretes agora.</div>';
    }
  }

  window.carregarLembretesWhatsAppV72=carregar;

  window.adicionarLembreteWhatsAppV72=function(){
    garantir();
    const usados=new Set(lembretes.map(x=>Number(x.antecedencia_minutos)));
    const padrao=OPCOES.find(x=>!usados.has(x[0]))?.[0]||1440;
    lembretes.push({id:null,ativo:true,antecedencia_minutos:padrao,horario_inicio:'08:00',horario_fim:'20:00',bloquear_duplicidade:true,ordem:lembretes.length+1});
    render();
    setTimeout(()=>document.querySelector('#simpla-wa-reminders-v72-list .simpla-wa-reminder-v72:last-child')?.scrollIntoView({behavior:'smooth',block:'center'}),50);
  };

  window.salvarLembreteWhatsAppV72=async function(i){
    const r=lembretes[i];if(!r)return;
    const msg=document.getElementById('wa72-msg-'+i);
    try{
      if(!await permitido())return;
      const ant=Number(document.getElementById('wa72-ant-'+i)?.value||1440);
      const ini=document.getElementById('wa72-ini-'+i)?.value;
      const fim=document.getElementById('wa72-fim-'+i)?.value;
      const ativo=!!document.getElementById('wa72-ativo-'+i)?.checked;
      const dup=document.getElementById('wa72-dup-'+i)?.value==='true';
      if(!ini||!fim||ini===fim){alert('Informe uma janela de envio válida.');return}
      msg.textContent='Salvando...';
      const {data,error}=await CloudDB.rpc('salvar_lembrete_whatsapp',{
        p_id:r.id||null,
        p_empresa_id:empresaAtual.id,
        p_ativo:ativo,
        p_antecedencia_minutos:ant,
        p_horario_inicio:ini,
        p_horario_fim:fim,
        p_bloquear_duplicidade:dup
      });
      if(error)throw error;
      msg.textContent='Salvo.';
      await carregar();
      if(typeof carregarMonitorWhatsAppV67==='function')setTimeout(()=>carregarMonitorWhatsAppV67(),100);
    }catch(err){
      console.error('Salvar lembrete v72:',err);
      msg.textContent='Erro ao salvar.';
      alert(err?.message||'Não foi possível salvar o lembrete.');
    }
  };

  window.excluirLembreteWhatsAppV72=async function(i){
    const r=lembretes[i];if(!r?.id)return;
    if(!confirm('Excluir este lembrete? As mensagens pendentes vinculadas a ele serão canceladas.'))return;
    try{
      if(!await permitido())return;
      const {error}=await CloudDB.rpc('excluir_lembrete_whatsapp',{p_id:r.id,p_empresa_id:empresaAtual.id});
      if(error)throw error;
      await carregar();
      if(typeof carregarMonitorWhatsAppV67==='function')setTimeout(()=>carregarMonitorWhatsAppV67(),100);
    }catch(err){
      console.error('Excluir lembrete v72:',err);
      alert(err?.message||'Não foi possível excluir o lembrete.');
    }
  };

  function instalar(){garantir();setTimeout(carregar,600)}
  if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',()=>setTimeout(instalar,5900));else setTimeout(instalar,5900);
  document.addEventListener('click',e=>{
    const b=e.target.closest?.('.cfg-v2-nav button');
    if(b&&b.dataset.cat==='WhatsApp e Automações')setTimeout(carregar,120);
  },true);
  setTimeout(instalar,8000);
})();
</script>
'''

html=html.replace(marker,block+'\n'+marker,1)
idx.write_text(html,encoding='utf-8')

swtxt=sw.read_text(encoding='utf-8')
swtxt,n=re.subn(r"const CACHE_VERSION = '[^']+';","const CACHE_VERSION = 'simpla-shell-v72-whatsapp-multilembretes';",swtxt,count=1)
if n!=1: raise SystemExit('cache version nao encontrada')
sw.write_text(swtxt,encoding='utf-8')
