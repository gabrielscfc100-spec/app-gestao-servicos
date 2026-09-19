from pathlib import Path
import re

idx=Path('index.html')
sw=Path('service-worker.js')
html=idx.read_text(encoding='utf-8')

if 'simpla-whatsapp-automacao-v70' in html:
    raise SystemExit('v70 ja aplicada')

marker='</body>'
if marker not in html:
    raise SystemExit('body nao encontrado')

block=r'''
<style id="simpla-whatsapp-automacao-v70-css">
  .simpla-wa-auto-v70{margin-top:16px;border:1px solid #dbe4ee;border-radius:12px;background:#fff;padding:16px;box-shadow:0 2px 5px rgba(15,23,42,.04);text-transform:none}
  .simpla-wa-auto-v70-head{display:flex;justify-content:space-between;gap:14px;align-items:center;flex-wrap:wrap}
  .simpla-wa-auto-v70 h3{margin:0;font-size:16px;color:#1a1c23;text-transform:none}
  .simpla-wa-auto-v70 p{margin:4px 0 0;font-size:10px;color:#718096;line-height:1.5;text-transform:none}
  .simpla-wa-auto-v70-state{font-size:10px;font-weight:900;padding:6px 9px;border-radius:999px;background:#edf2f7;color:#4a5568}
  .simpla-wa-auto-v70-state.on{background:#f0fff4;color:#2f855a}
  .simpla-wa-auto-v70-actions{display:flex;gap:8px;align-items:center;margin-top:12px;flex-wrap:wrap}
  .simpla-wa-auto-v70-btn{border:0;border-radius:7px;padding:10px 13px;font-size:9px;font-weight:900;cursor:pointer}
  .simpla-wa-auto-v70-on{background:#1a1c23;color:#fff}.simpla-wa-auto-v70-off{background:#edf2f7;color:#2d3748}
  .simpla-wa-auto-v70-msg{font-size:10px;color:#718096;text-transform:none}
  .simpla-wa-auto-v70-note{margin-top:10px;padding:10px;border-radius:8px;background:#fffaf0;border:1px solid #f6e05e;color:#744210;font-size:10px;line-height:1.5;text-transform:none}
</style>
<script id="simpla-whatsapp-automacao-v70">
(function(){
  function garantir(){
    let box=document.getElementById('simpla-wa-auto-v70');if(box)return box;
    const area=document.getElementById('simpla-wa-categoria-v65-content');if(!area)return null;
    box=document.createElement('section');box.id='simpla-wa-auto-v70';box.className='simpla-wa-auto-v70';
    box.innerHTML='<div class="simpla-wa-auto-v70-head"><div><h3>Automação de envios</h3><p>Controle mestre para permitir que o processador envie automaticamente as mensagens preparadas pela agenda.</p></div><span id="wa-auto-state-v70" class="simpla-wa-auto-v70-state">Desativado</span></div><div class="simpla-wa-auto-v70-actions"><button type="button" class="simpla-wa-auto-v70-btn simpla-wa-auto-v70-on" onclick="alterarAutomacaoWhatsAppV70(true)">Ativar automação</button><button type="button" class="simpla-wa-auto-v70-btn simpla-wa-auto-v70-off" onclick="alterarAutomacaoWhatsAppV70(false)">Desativar</button><span id="wa-auto-msg-v70" class="simpla-wa-auto-v70-msg"></span></div><div class="simpla-wa-auto-v70-note">A ativação só é permitida quando o fuso horário e a integração oficial com a Meta estiverem configurados e válidos.</div>';
    const monitor=document.getElementById('simpla-wa-monitor-v67');
    if(monitor&&monitor.parentElement===area) area.insertBefore(box,monitor);else area.appendChild(box);
    return box;
  }
  async function admin(){
    if(typeof CloudDB==='undefined'||!CloudDB||typeof empresaAtual==='undefined'||!empresaAtual?.id)return false;
    const {data}=await CloudDB.rpc('perfil_na_empresa',{p_empresa_id:empresaAtual.id});
    return String(data||'').toUpperCase()==='ADMIN';
  }
  function render(on){
    const s=document.getElementById('wa-auto-state-v70');if(!s)return;
    s.textContent=on?'Ativado':'Desativado';s.className='simpla-wa-auto-v70-state'+(on?' on':'');
  }
  async function carregar(){
    const box=garantir();if(!box||!await admin())return;
    try{
      const {data,error}=await CloudDB.from('whatsapp_automacao_config').select('envios_automaticos_ativos').eq('empresa_id',empresaAtual.id).maybeSingle();
      if(error)throw error;render(!!data?.envios_automaticos_ativos);
    }catch(err){console.error('Automação WhatsApp v70:',err)}
  }
  window.carregarAutomacaoWhatsAppV70=carregar;
  window.alterarAutomacaoWhatsAppV70=async function(ativo){
    const msg=document.getElementById('wa-auto-msg-v70');
    try{
      if(!await admin())return;
      if(ativo&&!confirm('Ativar os envios automáticos do WhatsApp para esta empresa?'))return;
      msg.textContent=ativo?'Validando pré-requisitos...':'Desativando...';
      const {error}=await CloudDB.rpc('salvar_automacao_whatsapp_operacional',{p_empresa_id:empresaAtual.id,p_envios_automaticos_ativos:!!ativo});
      if(error)throw error;
      render(!!ativo);msg.textContent=ativo?'Automação ativada.':'Automação desativada.';
    }catch(err){
      console.error('Alterar automação v70:',err);
      msg.textContent='Não foi possível alterar.';
      alert(err?.message||'Não foi possível alterar a automação.');
      await carregar();
    }
  };
  function instalar(){garantir();setTimeout(carregar,700)}
  if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',()=>setTimeout(instalar,5600));else setTimeout(instalar,5600);
  document.addEventListener('click',e=>{const b=e.target.closest?.('.cfg-v2-nav button');if(b&&b.dataset.cat==='WhatsApp e Automações')setTimeout(carregar,140)},true);
  setTimeout(instalar,7800);
})();
</script>
'''
html=html.replace(marker,block+'\n'+marker,1)
idx.write_text(html,encoding='utf-8')

swtxt=sw.read_text(encoding='utf-8')
swtxt,n=re.subn(r"const CACHE_VERSION = '[^']+';","const CACHE_VERSION = 'simpla-shell-v70-whatsapp-automacao';",swtxt,count=1)
if n!=1: raise SystemExit('cache version nao encontrada')
sw.write_text(swtxt,encoding='utf-8')
