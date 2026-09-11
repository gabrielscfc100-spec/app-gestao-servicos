from pathlib import Path

index = Path('index.html')
html = index.read_text(encoding='utf-8')
marker = '<!-- SIMPLA agenda conflitos v37 -->'
if marker in html:
    print('v37 already applied')
else:
    insert = r'''
<!-- SIMPLA agenda conflitos v37 -->
<style id="simpla-agenda-conflitos-v37">
#agenda-validacao-horario-v37{margin:-4px 0 14px;padding:10px 12px;border-radius:6px;font-size:12px;line-height:1.45;text-transform:none;background:#edf2f7;color:#4a5568;border:1px solid #e2e8f0}
#agenda-validacao-horario-v37.ok{background:#f0fff4;color:#276749;border-color:#9ae6b4}
#agenda-validacao-horario-v37.erro{background:#fff5f5;color:#9b2c2c;border-color:#feb2b2}
#agenda-validacao-horario-v37.aviso{background:#fffaf0;color:#975a16;border-color:#fbd38d}
</style>
<script>
(function(){
  function minHora(v){ if(!v) return null; const p=String(v).slice(0,5).split(':').map(Number); return p[0]*60+p[1]; }
  function fmtMin(m){ m=((m%1440)+1440)%1440; return String(Math.floor(m/60)).padStart(2,'0')+':'+String(m%60).padStart(2,'0'); }
  function durAg(a){ return Number(a?.duracao || a?.duracaoMin || a?.duracao_min || (window.configExpediente?.intervalo) || 45); }
  function statusAtivo(a){ const s=String(a?.status||'AGENDADO').toUpperCase(); return !['CANCELADO','NAO_COMPARECEU'].includes(s); }
  function obterDataModal(){ return document.getElementById('agenda-data-filtro')?.value || ''; }
  function validarAgendaV37(){
    const box=document.getElementById('agenda-validacao-horario-v37');
    const btn=document.getElementById('btn-salvar-agendamento');
    if(!box||!btn) return true;
    const hora=document.getElementById('agenda-hora-inicio')?.value||'';
    const dur=Number(document.getElementById('agenda-duracao-min')?.value||0);
    const prof=document.getElementById('agenda-profissional')?.value||'';
    const data=obterDataModal();
    const idEd=document.getElementById('agenda-edicao-id')?.value||'';
    if(!hora||!dur||!prof||!data){ box.className=''; box.textContent='Preencha horário, duração e profissional para validar a disponibilidade.'; btn.disabled=false; return true; }
    const ini=minHora(hora), fim=ini+dur;
    const abertura=minHora(window.configExpediente?.abertura || '08:00');
    const fechamento=minHora(window.configExpediente?.fechamento || '18:00');
    if((abertura!==null && ini<abertura)||(fechamento!==null && fim>fechamento)){
      box.className='erro'; box.textContent=`O atendimento terminaria às ${fmtMin(fim)}, fora do expediente (${fmtMin(abertura)} às ${fmtMin(fechamento)}).`; btn.disabled=true; return false;
    }
    const lista=Array.isArray(window.agendamentos)?window.agendamentos:(typeof agendamentos!=='undefined'?agendamentos:[]);
    const conflito=lista.find(a=>{
      if(!statusAtivo(a)) return false;
      if(String(a.id||'')===String(idEd)) return false;
      if(String(a.data||'')!==String(data)) return false;
      if(String(a.profissionalId||a.profissional_id||'')!==String(prof)) return false;
      const ai=minHora(a.horario); if(ai===null) return false;
      const af=ai+durAg(a);
      return ini<af && fim>ai;
    });
    if(conflito){
      const ci=minHora(conflito.horario), cf=ci+durAg(conflito);
      const nome=conflito.clienteNome||conflito.cliente_nome||'outro cliente';
      box.className='erro'; box.textContent=`Conflito: este atendimento ocuparia ${hora}–${fmtMin(fim)}, mas ${nome} já ocupa ${fmtMin(ci)}–${fmtMin(cf)}.`; btn.disabled=true; return false;
    }
    box.className='ok'; box.textContent=`Horário disponível. Atendimento previsto de ${hora} até ${fmtMin(fim)} (${dur} min).`; btn.disabled=false; return true;
  }
  function preparar(){
    const modal=document.getElementById('modal-agendamento'); if(!modal) return;
    let box=document.getElementById('agenda-validacao-horario-v37');
    if(!box){
      box=document.createElement('div'); box.id='agenda-validacao-horario-v37'; box.textContent='Preencha horário, duração e profissional para validar a disponibilidade.';
      const tipo=document.getElementById('agenda-tipo-cliente')?.closest('.form-group');
      if(tipo) tipo.parentNode.insertBefore(box,tipo);
    }
    ['agenda-hora-inicio','agenda-duracao-min','agenda-profissional','agenda-servico'].forEach(id=>{
      const el=document.getElementById(id); if(el && !el.dataset.v37){ el.dataset.v37='1'; el.addEventListener('input',()=>setTimeout(validarAgendaV37,0)); el.addEventListener('change',()=>setTimeout(validarAgendaV37,0)); }
    });
    const obs=new MutationObserver(()=>{ if(modal.classList.contains('active')) setTimeout(validarAgendaV37,0); });
    obs.observe(modal,{attributes:true,attributeFilter:['class']});
    window.validarAgendaConflitoV37=validarAgendaV37;
  }
  if(document.readyState==='loading') document.addEventListener('DOMContentLoaded',preparar); else preparar();
})();
</script>
'''
    html = html.replace('</body>', insert + '\n</body>')
    index.write_text(html, encoding='utf-8')

sw=Path('service-worker.js')
if sw.exists():
    s=sw.read_text(encoding='utf-8')
    import re
    s=re.sub(r"const CACHE_VERSION = ['\"][^'\"]+['\"]", "const CACHE_VERSION = 'simpla-shell-v37-agenda-conflitos'", s, count=1)
    sw.write_text(s, encoding='utf-8')
print('v37 applied')
