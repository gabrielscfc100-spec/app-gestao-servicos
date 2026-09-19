from pathlib import Path
import re

idx=Path('index.html')
sw=Path('service-worker.js')
html=idx.read_text(encoding='utf-8')

if 'simpla-whatsapp-regras-v66' in html:
    raise SystemExit('v66 ja aplicada')

marker='</body>'
if marker not in html:
    raise SystemExit('body nao encontrado')

block=r'''
<style id="simpla-whatsapp-regras-v66-css">
  .simpla-wa-rules-v66{margin-top:16px;border:1px solid #dbe4ee;border-radius:12px;background:#fff;padding:16px;box-shadow:0 2px 5px rgba(15,23,42,.04);text-transform:none}
  .simpla-wa-rules-v66 h3{margin:0;font-size:16px;color:#1a1c23;text-transform:none}
  .simpla-wa-rules-v66 p{margin:4px 0 0;font-size:10px;color:#718096;line-height:1.5;text-transform:none}
  .simpla-wa-rules-v66-grid{display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-top:14px}
  .simpla-wa-rules-v66-card{border:1px solid #e2e8f0;border-radius:9px;background:#f8fafc;padding:12px}
  .simpla-wa-rules-v66-card h4{margin:0 0 8px;font-size:11px;color:#2d3748;text-transform:none}
  .simpla-wa-rules-v66-switch{display:flex;align-items:center;justify-content:space-between;gap:12px;padding:8px 0;border-bottom:1px solid #edf2f7;text-transform:none}
  .simpla-wa-rules-v66-switch:last-child{border-bottom:0}
  .simpla-wa-rules-v66-switch span{font-size:10px;color:#4a5568;text-transform:none}
  .simpla-wa-rules-v66-fields{display:grid;grid-template-columns:1fr 1fr;gap:10px}
  .simpla-wa-rules-v66-field label{display:block;font-size:8px;font-weight:900;color:#718096;margin-bottom:4px;text-transform:uppercase}
  .simpla-wa-rules-v66-field select,.simpla-wa-rules-v66-field input{width:100%;padding:9px;border:1px solid #cbd5e0;border-radius:6px;background:#fff;font-size:11px;text-transform:none}
  .simpla-wa-rules-v66-actions{display:flex;align-items:center;gap:10px;flex-wrap:wrap;margin-top:14px}
  .simpla-wa-rules-v66-save{border:0;border-radius:7px;padding:10px 13px;background:#1a1c23;color:#fff;font-size:9px;font-weight:900;cursor:pointer}
  .simpla-wa-rules-v66-msg{font-size:10px;color:#718096;text-transform:none}
  .simpla-wa-rules-v66-note{margin-top:12px;padding:10px;border-radius:8px;background:#fffaf0;border:1px solid #f6e05e;color:#744210;font-size:10px;line-height:1.5;text-transform:none}
  .simpla-wa-rules-v66.locked{opacity:.78}
  .simpla-wa-rules-v66.locked input,.simpla-wa-rules-v66.locked select,.simpla-wa-rules-v66.locked button{pointer-events:none}
  @media(max-width:760px){.simpla-wa-rules-v66-grid,.simpla-wa-rules-v66-fields{grid-template-columns:1fr}}
</style>

<script id="simpla-whatsapp-regras-v66">
(function(){
  function garantir(){
    let box=document.getElementById('simpla-wa-rules-v66'); if(box) return box;
    const area=document.getElementById('simpla-wa-categoria-v65-content');
    if(!area) return null;

    box=document.createElement('section');
    box.id='simpla-wa-rules-v66';
    box.className='simpla-wa-rules-v66';
    box.innerHTML=`
      <div>
        <h3>Regras de envio</h3>
        <p>Defina quando o SimplA poderá preparar mensagens operacionais. As automações só serão executadas quando o motor de envio for ativado em uma etapa posterior.</p>
      </div>

      <div class="simpla-wa-rules-v66-grid">
        <div class="simpla-wa-rules-v66-card">
          <h4>Tipos de mensagem</h4>
          <label class="simpla-wa-rules-v66-switch"><span>Confirmação de agendamento</span><input id="wa-rule-confirmacao" type="checkbox"></label>
          <label class="simpla-wa-rules-v66-switch"><span>Lembrete de agendamento</span><input id="wa-rule-lembrete" type="checkbox"></label>
          <label class="simpla-wa-rules-v66-switch"><span>Cancelamento</span><input id="wa-rule-cancelamento" type="checkbox"></label>
          <label class="simpla-wa-rules-v66-switch"><span>Reagendamento</span><input id="wa-rule-reagendamento" type="checkbox"></label>
        </div>

        <div class="simpla-wa-rules-v66-card">
          <h4>Parâmetros</h4>
          <div class="simpla-wa-rules-v66-fields">
            <div class="simpla-wa-rules-v66-field">
              <label>Antecedência do lembrete</label>
              <select id="wa-rule-antecedencia">
                <option value="30">30 minutos</option>
                <option value="60">1 hora</option>
                <option value="120">2 horas</option>
                <option value="360">6 horas</option>
                <option value="720">12 horas</option>
                <option value="1440">24 horas</option>
                <option value="2880">48 horas</option>
                <option value="4320">3 dias</option>
                <option value="10080">7 dias</option>
              </select>
            </div>
            <div class="simpla-wa-rules-v66-field">
              <label>Evitar duplicidade</label>
              <select id="wa-rule-duplicidade">
                <option value="true">Sim</option>
                <option value="false">Não</option>
              </select>
            </div>
            <div class="simpla-wa-rules-v66-field">
              <label>Início da janela de envio</label>
              <input id="wa-rule-inicio" type="time" value="08:00">
            </div>
            <div class="simpla-wa-rules-v66-field">
              <label>Fim da janela de envio</label>
              <input id="wa-rule-fim" type="time" value="20:00">
            </div>
          </div>
        </div>
      </div>

      <div class="simpla-wa-rules-v66-actions">
        <button type="button" class="simpla-wa-rules-v66-save" onclick="salvarRegrasWhatsAppV66()">Salvar regras</button>
        <span id="simpla-wa-rules-v66-msg" class="simpla-wa-rules-v66-msg"></span>
      </div>
      <div class="simpla-wa-rules-v66-note">Estas regras ainda não disparam mensagens automaticamente. Elas serão usadas pelo motor de automação que será conectado à fila operacional nas próximas versões.</div>
    `;

    const roadmap=document.getElementById('simpla-wa-roadmap-v65');
    if(roadmap && roadmap.parentElement===area) area.insertBefore(box,roadmap); else area.appendChild(box);
    return box;
  }

  async function permitido(){
    if(typeof CloudDB==='undefined'||!CloudDB||typeof empresaAtual==='undefined'||!empresaAtual?.id) return false;
    const {data:perfil}=await CloudDB.rpc('perfil_na_empresa',{p_empresa_id:empresaAtual.id});
    if(String(perfil||'').toUpperCase()!=='ADMIN') return false;
    if(typeof empresaPodeUsarRecurso!=='function') return false;
    return await empresaPodeUsarRecurso('whatsapp_operacional');
  }

  function preencher(r){
    document.getElementById('wa-rule-confirmacao').checked=!!r?.confirmacao_ativa;
    document.getElementById('wa-rule-lembrete').checked=!!r?.lembrete_ativo;
    document.getElementById('wa-rule-cancelamento').checked=!!r?.cancelamento_ativo;
    document.getElementById('wa-rule-reagendamento').checked=!!r?.reagendamento_ativo;
    document.getElementById('wa-rule-antecedencia').value=String(r?.lembrete_antecedencia_minutos||1440);
    document.getElementById('wa-rule-inicio').value=String(r?.horario_inicio||'08:00').slice(0,5);
    document.getElementById('wa-rule-fim').value=String(r?.horario_fim||'20:00').slice(0,5);
    document.getElementById('wa-rule-duplicidade').value=String(r?.bloquear_duplicidade!==false);
  }

  async function carregar(){
    const box=garantir(); if(!box) return;
    const msg=document.getElementById('simpla-wa-rules-v66-msg');
    try{
      const ok=await permitido();
      box.classList.toggle('locked',!ok);
      if(!ok){
        msg.textContent='Disponível a partir do plano Plus.';
        return;
      }
      const {data,error}=await CloudDB.from('whatsapp_regras_operacionais')
        .select('confirmacao_ativa,lembrete_ativo,cancelamento_ativo,reagendamento_ativo,lembrete_antecedencia_minutos,horario_inicio,horario_fim,bloquear_duplicidade')
        .eq('empresa_id',empresaAtual.id).maybeSingle();
      if(error) throw error;
      preencher(data||{});
      msg.textContent=data?'Regras carregadas.':'Use os valores abaixo para criar a primeira configuração.';
    }catch(err){
      console.error('Regras WhatsApp v66:',err);
      msg.textContent='Não foi possível carregar as regras agora.';
    }
  }

  window.carregarRegrasWhatsAppV66=carregar;

  window.salvarRegrasWhatsAppV66=async function(){
    const box=garantir(); if(!box) return;
    const msg=document.getElementById('simpla-wa-rules-v66-msg');
    try{
      if(!await permitido()) return;
      const inicio=document.getElementById('wa-rule-inicio').value;
      const fim=document.getElementById('wa-rule-fim').value;
      if(!inicio||!fim||inicio===fim){alert('Informe uma janela de envio válida.');return}
      msg.textContent='Salvando...';
      const {error}=await CloudDB.rpc('salvar_regras_whatsapp_operacional',{
        p_empresa_id:empresaAtual.id,
        p_confirmacao_ativa:document.getElementById('wa-rule-confirmacao').checked,
        p_lembrete_ativo:document.getElementById('wa-rule-lembrete').checked,
        p_cancelamento_ativo:document.getElementById('wa-rule-cancelamento').checked,
        p_reagendamento_ativo:document.getElementById('wa-rule-reagendamento').checked,
        p_lembrete_antecedencia_minutos:Number(document.getElementById('wa-rule-antecedencia').value||1440),
        p_horario_inicio:inicio,
        p_horario_fim:fim,
        p_bloquear_duplicidade:document.getElementById('wa-rule-duplicidade').value==='true'
      });
      if(error) throw error;
      msg.textContent='Regras salvas com sucesso.';
      await carregar();
    }catch(err){
      console.error('Salvar regras WhatsApp v66:',err);
      msg.textContent='Não foi possível salvar as regras.';
      alert(err?.message||'Erro ao salvar regras do WhatsApp.');
    }
  };

  function instalar(){
    garantir();
    setTimeout(carregar,800);
  }
  if(document.readyState==='loading') document.addEventListener('DOMContentLoaded',()=>setTimeout(instalar,4500));
  else setTimeout(instalar,4500);

  document.addEventListener('click',e=>{
    const b=e.target.closest?.('.cfg-v2-nav button');
    if(b && b.dataset.cat==='WhatsApp e Automações') setTimeout(carregar,120);
  },true);

  setTimeout(instalar,6500);
})();
</script>
'''

html=html.replace(marker,block+'\n'+marker,1)
idx.write_text(html,encoding='utf-8')

swtxt=sw.read_text(encoding='utf-8')
swtxt,n=re.subn(r"const CACHE_VERSION = '[^']+';","const CACHE_VERSION = 'simpla-shell-v66-whatsapp-regras';",swtxt,count=1)
if n!=1: raise SystemExit('cache version nao encontrada')
sw.write_text(swtxt,encoding='utf-8')
