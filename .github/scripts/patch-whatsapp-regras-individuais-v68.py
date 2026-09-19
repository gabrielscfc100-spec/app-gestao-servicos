from pathlib import Path
import re

idx=Path('index.html')
sw=Path('service-worker.js')
html=idx.read_text(encoding='utf-8')

if 'simpla-whatsapp-regras-individuais-v68' in html:
    raise SystemExit('v68 ja aplicada')

marker='</body>'
if marker not in html:
    raise SystemExit('body nao encontrado')

block=r'''
<style id="simpla-whatsapp-regras-individuais-v68-css">
  #simpla-wa-rules-v66{display:none!important}
  .simpla-wa-rules-v68{margin-top:16px;border:1px solid #dbe4ee;border-radius:12px;background:#fff;padding:16px;box-shadow:0 2px 5px rgba(15,23,42,.04);text-transform:none}
  .simpla-wa-rules-v68 h3{margin:0;font-size:16px;color:#1a1c23;text-transform:none}
  .simpla-wa-rules-v68>p{margin:4px 0 0;font-size:10px;color:#718096;line-height:1.5;text-transform:none}
  .simpla-wa-rules-v68-grid{display:grid;grid-template-columns:1fr 1fr;gap:12px;margin-top:14px}
  .simpla-wa-rule-v68-card{border:1px solid #e2e8f0;border-radius:10px;background:#f8fafc;padding:13px}
  .simpla-wa-rule-v68-head{display:flex;justify-content:space-between;gap:12px;align-items:center;margin-bottom:10px}
  .simpla-wa-rule-v68-title{font-size:12px;font-weight:900;color:#2d3748;text-transform:none}
  .simpla-wa-rule-v68-desc{font-size:9px;color:#718096;margin-top:2px;line-height:1.4;text-transform:none}
  .simpla-wa-rule-v68-fields{display:grid;grid-template-columns:1fr 1fr;gap:9px}
  .simpla-wa-rule-v68-field label{display:block;font-size:8px;font-weight:900;color:#718096;margin-bottom:4px;text-transform:uppercase}
  .simpla-wa-rule-v68-field input,.simpla-wa-rule-v68-field select{width:100%;padding:8px;border:1px solid #cbd5e0;border-radius:6px;background:#fff;font-size:11px;text-transform:none}
  .simpla-wa-rule-v68-full{grid-column:1/-1}
  .simpla-wa-rule-v68-actions{display:flex;justify-content:space-between;gap:10px;align-items:center;margin-top:11px;flex-wrap:wrap}
  .simpla-wa-rule-v68-save{border:0;border-radius:7px;padding:9px 11px;background:#1a1c23;color:#fff;font-size:9px;font-weight:900;cursor:pointer}
  .simpla-wa-rule-v68-msg{font-size:9px;color:#718096;text-transform:none}
  .simpla-wa-rule-v68-note{margin-top:12px;padding:10px;border-radius:8px;background:#ebf8ff;border:1px solid #bee3f8;color:#2c5282;font-size:10px;line-height:1.5;text-transform:none}
  .simpla-wa-rule-v68-disabled{opacity:.65}
  @media(max-width:760px){.simpla-wa-rules-v68-grid,.simpla-wa-rule-v68-fields{grid-template-columns:1fr}.simpla-wa-rule-v68-full{grid-column:auto}}
</style>

<script id="simpla-whatsapp-regras-individuais-v68">
(function(){
  const TIPOS=[
    {tipo:'CONFIRMACAO',titulo:'Confirmação de agendamento',desc:'Preparada quando o agendamento passa para AGENDADO.',antecedencia:false},
    {tipo:'LEMBRETE',titulo:'Lembrete de agendamento',desc:'Preparado antes do horário marcado conforme a antecedência definida.',antecedencia:true},
    {tipo:'CANCELAMENTO',titulo:'Cancelamento',desc:'Preparado quando o agendamento é cancelado.',antecedencia:false},
    {tipo:'REAGENDAMENTO',titulo:'Reagendamento',desc:'Preparado quando data, horário ou profissional são alterados.',antecedencia:false}
  ];

  function slug(t){return t.toLowerCase()}
  function garantir(){
    let box=document.getElementById('simpla-wa-rules-v68');if(box)return box;
    const area=document.getElementById('simpla-wa-categoria-v65-content');if(!area)return null;
    box=document.createElement('section');
    box.id='simpla-wa-rules-v68';
    box.className='simpla-wa-rules-v68';
    box.innerHTML='<h3>Regras de envio por mensagem</h3><p>Cada mensagem possui configuração própria. Isso permite, por exemplo, enviar confirmações em uma janela e lembretes em outra.</p><div id="simpla-wa-rules-v68-grid" class="simpla-wa-rules-v68-grid"></div><div class="simpla-wa-rule-v68-note">As regras controlam a preparação da fila. O disparo automático continuará desativado até ativarmos o processador final.</div>';
    const antigo=document.getElementById('simpla-wa-rules-v66');
    if(antigo&&antigo.parentElement===area) antigo.insertAdjacentElement('afterend',box);
    else {
      const monitor=document.getElementById('simpla-wa-monitor-v67');
      if(monitor&&monitor.parentElement===area) area.insertBefore(box,monitor); else area.appendChild(box);
    }
    render([]);
    return box;
  }

  function opcoesAntecedencia(v){
    const opts=[[30,'30 minutos'],[60,'1 hora'],[120,'2 horas'],[360,'6 horas'],[720,'12 horas'],[1440,'24 horas'],[2880,'48 horas'],[4320,'3 dias'],[10080,'7 dias']];
    return opts.map(([x,n])=>'<option value="'+x+'" '+(Number(v||1440)===x?'selected':'')+'>'+n+'</option>').join('');
  }

  function render(rows){
    const grid=document.getElementById('simpla-wa-rules-v68-grid');if(!grid)return;
    const map=new Map((rows||[]).map(r=>[String(r.tipo).toUpperCase(),r]));
    grid.innerHTML=TIPOS.map(cfg=>{
      const r=map.get(cfg.tipo)||{};
      const s=slug(cfg.tipo);
      const ini=String(r.horario_inicio||'08:00').slice(0,5);
      const fim=String(r.horario_fim||'20:00').slice(0,5);
      return '<div class="simpla-wa-rule-v68-card" id="wa-rule-card-'+s+'">'+
        '<div class="simpla-wa-rule-v68-head"><div><div class="simpla-wa-rule-v68-title">'+cfg.titulo+'</div><div class="simpla-wa-rule-v68-desc">'+cfg.desc+'</div></div><label style="display:flex;align-items:center;gap:7px;font-size:9px;color:#4a5568;text-transform:none"><input id="wa68-ativo-'+s+'" type="checkbox" '+(r.ativo?'checked':'')+'> Ativo</label></div>'+
        '<div class="simpla-wa-rule-v68-fields">'+
          (cfg.antecedencia?'<div class="simpla-wa-rule-v68-field simpla-wa-rule-v68-full"><label>Antecedência</label><select id="wa68-ant-'+s+'">'+opcoesAntecedencia(r.antecedencia_minutos)+'</select></div>':'')+
          '<div class="simpla-wa-rule-v68-field"><label>Início da janela</label><input id="wa68-ini-'+s+'" type="time" value="'+ini+'"></div>'+
          '<div class="simpla-wa-rule-v68-field"><label>Fim da janela</label><input id="wa68-fim-'+s+'" type="time" value="'+fim+'"></div>'+
          '<div class="simpla-wa-rule-v68-field simpla-wa-rule-v68-full"><label>Evitar duplicidade</label><select id="wa68-dup-'+s+'"><option value="true" '+(r.bloquear_duplicidade!==false?'selected':'')+'>Sim</option><option value="false" '+(r.bloquear_duplicidade===false?'selected':'')+'>Não</option></select></div>'+
        '</div>'+
        '<div class="simpla-wa-rule-v68-actions"><span id="wa68-msg-'+s+'" class="simpla-wa-rule-v68-msg"></span><button type="button" class="simpla-wa-rule-v68-save" onclick="salvarRegraWhatsAppV68(\''+cfg.tipo+'\')">Salvar '+cfg.titulo.toLowerCase()+'</button></div>'+
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
    const box=garantir();if(!box)return;
    try{
      const ok=await permitido();
      box.classList.toggle('simpla-wa-rule-v68-disabled',!ok);
      if(!ok)return;
      const {data,error}=await CloudDB.from('whatsapp_regras_mensagem')
        .select('tipo,ativo,antecedencia_minutos,horario_inicio,horario_fim,bloquear_duplicidade')
        .eq('empresa_id',empresaAtual.id);
      if(error)throw error;
      render(Array.isArray(data)?data:[]);
    }catch(err){console.error('Regras individuais WhatsApp v68:',err)}
  }

  window.carregarRegrasWhatsAppV68=carregar;

  window.salvarRegraWhatsAppV68=async function(tipo){
    const cfg=TIPOS.find(x=>x.tipo===tipo);if(!cfg)return;
    const s=slug(tipo), msg=document.getElementById('wa68-msg-'+s);
    try{
      if(!await permitido())return;
      const ini=document.getElementById('wa68-ini-'+s)?.value;
      const fim=document.getElementById('wa68-fim-'+s)?.value;
      if(!ini||!fim||ini===fim){alert('Informe uma janela de envio válida para '+cfg.titulo+'.');return}
      msg.textContent='Salvando...';
      const ant=cfg.antecedencia?Number(document.getElementById('wa68-ant-'+s)?.value||1440):null;
      const {error}=await CloudDB.rpc('salvar_regra_whatsapp_mensagem',{
        p_empresa_id:empresaAtual.id,
        p_tipo:tipo,
        p_ativo:!!document.getElementById('wa68-ativo-'+s)?.checked,
        p_antecedencia_minutos:ant,
        p_horario_inicio:ini,
        p_horario_fim:fim,
        p_bloquear_duplicidade:document.getElementById('wa68-dup-'+s)?.value==='true'
      });
      if(error)throw error;
      msg.textContent='Salvo.';
      setTimeout(()=>{if(msg)msg.textContent=''},1800);
      await carregar();
    }catch(err){
      console.error('Salvar regra WhatsApp v68:',err);
      msg.textContent='Erro ao salvar.';
      alert(err?.message||'Não foi possível salvar esta regra.');
    }
  };

  function instalar(){garantir();setTimeout(carregar,700)}
  if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',()=>setTimeout(instalar,5200));else setTimeout(instalar,5200);
  document.addEventListener('click',e=>{
    const b=e.target.closest?.('.cfg-v2-nav button');
    if(b&&b.dataset.cat==='WhatsApp e Automações')setTimeout(carregar,140);
  },true);
  setTimeout(instalar,7500);
})();
</script>
'''

html=html.replace(marker,block+'\n'+marker,1)
idx.write_text(html,encoding='utf-8')

swtxt=sw.read_text(encoding='utf-8')
swtxt,n=re.subn(r"const CACHE_VERSION = '[^']+';","const CACHE_VERSION = 'simpla-shell-v68-whatsapp-regras-individuais';",swtxt,count=1)
if n!=1: raise SystemExit('cache version nao encontrada')
sw.write_text(swtxt,encoding='utf-8')
