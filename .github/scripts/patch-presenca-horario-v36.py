from pathlib import Path
p=Path('index.html')
s=p.read_text(encoding='utf-8')
marker='simpla-presenca-horario-v36'
if marker in s:
    raise SystemExit('v36 ja aplicada')
bloco=r'''
<style id="simpla-presenca-horario-v36">
#simpla-presenca-modal-v36{position:fixed;inset:0;background:rgba(15,23,42,.66);z-index:10050;display:none;align-items:center;justify-content:center;padding:18px}
#simpla-presenca-modal-v36.ativo{display:flex}
#simpla-presenca-modal-v36 .box{width:min(440px,100%);background:#fff;border-radius:14px;padding:22px;box-shadow:0 24px 60px rgba(0,0,0,.28)}
#simpla-presenca-modal-v36 h3{margin:0 0 8px;font-size:20px;color:#1f2937}
#simpla-presenca-modal-v36 p{margin:0 0 16px;color:#64748b;font-size:14px;text-transform:none;line-height:1.45}
#simpla-presenca-modal-v36 .dados{background:#f8fafc;border:1px solid #e2e8f0;border-radius:9px;padding:12px;margin-bottom:16px;font-size:13px;line-height:1.6}
#simpla-presenca-modal-v36 .acoes{display:grid;grid-template-columns:1fr 1fr;gap:10px}
#simpla-presenca-modal-v36 button{border:0;border-radius:8px;padding:13px 10px;font-weight:700;cursor:pointer}
#simpla-presenca-sim-v36{background:#38a169;color:#fff}
#simpla-presenca-nao-v36{background:#e53e3e;color:#fff}
@media(max-width:520px){#simpla-presenca-modal-v36 .acoes{grid-template-columns:1fr}}
</style>
<script id="simpla-presenca-horario-v36-script">
(function(){
  let atual=null, processando=false;
  const STORAGE='simpla_presenca_notificada_v36_';
  function hoje(){const d=new Date();return d.getFullYear()+'-'+String(d.getMonth()+1).padStart(2,'0')+'-'+String(d.getDate()).padStart(2,'0')}
  function minAgora(){const d=new Date();return d.getHours()*60+d.getMinutes()}
  function minHora(h){const [a,b]=String(h||'00:00').slice(0,5).split(':').map(Number);return a*60+b}
  function ags(){try{return Array.isArray(agendamentos)?agendamentos:[]}catch(_){return []}}
  function jaAvisado(id){return localStorage.getItem(STORAGE+id)==='1'}
  function marcarAvisado(id){localStorage.setItem(STORAGE+id,'1')}
  function nomeProf(id){try{const p=(Array.isArray(profissionais)?profissionais:[]).find(x=>String(x.id)===String(id));return p?.nome||''}catch(_){return ''}}
  function montarModal(){
    let m=document.getElementById('simpla-presenca-modal-v36'); if(m) return m;
    m=document.createElement('div');m.id='simpla-presenca-modal-v36';m.innerHTML='<div class="box"><h3>Horário do atendimento</h3><p>Informe se o cliente compareceu ao atendimento agendado.</p><div class="dados" id="simpla-presenca-dados-v36"></div><div class="acoes"><button id="simpla-presenca-sim-v36">Cliente compareceu</button><button id="simpla-presenca-nao-v36">Não compareceu</button></div></div>';
    document.body.appendChild(m);
    m.querySelector('#simpla-presenca-sim-v36').onclick=()=>responder('COMPARECEU');
    m.querySelector('#simpla-presenca-nao-v36').onclick=()=>responder('NAO_COMPARECEU');
    return m;
  }
  function exibir(ag){
    atual=ag; const m=montarModal(); const prof=nomeProf(ag.profissionalId||ag.profissional_id);
    document.getElementById('simpla-presenca-dados-v36').innerHTML='<b>Cliente:</b> '+(ag.clienteNome||ag.cliente_nome||'-')+'<br><b>Horário:</b> '+String(ag.horario||'').slice(0,5)+(prof?'<br><b>Profissional:</b> '+prof:'');
    m.classList.add('ativo');
    try{if('Notification' in window && Notification.permission==='granted'){new Notification('SimplA · Horário do atendimento',{body:(ag.clienteNome||ag.cliente_nome||'Cliente')+' — compareceu?',icon:'./icons/icon-192.png',tag:'presenca-'+ag.id});}}catch(_){ }
  }
  async function responder(resp){
    if(processando||!atual)return; processando=true; const ag=atual; const agora=new Date().toISOString();
    try{
      let uid=null; try{const r=await CloudDB?.auth?.getUser?.();uid=r?.data?.user?.id||null}catch(_){ }
      if(typeof CloudDB!=='undefined' && CloudDB && typeof empresaAtual!=='undefined' && empresaAtual?.id){
        const payload={comparecimento_status:resp,comparecimento_registrado_em:agora,comparecimento_registrado_por:uid,atualizado_em:agora};
        if(resp==='NAO_COMPARECEU') payload.status='NAO_COMPARECEU';
        const {error}=await CloudDB.from('agendamentos').update(payload).eq('id',ag.id).eq('empresa_id',empresaAtual.id); if(error) throw error;
      }
      ag.comparecimentoStatus=resp; ag.comparecimento_status=resp; ag.comparecimentoRegistradoEm=agora; ag.comparecimento_registrado_em=agora;
      if(resp==='NAO_COMPARECEU') ag.status='NAO_COMPARECEU';
      marcarAvisado(ag.id); document.getElementById('simpla-presenca-modal-v36')?.classList.remove('ativo'); atual=null;
      try{salvarCacheAgendaCloud?.()}catch(_){ } try{renderizarAgenda?.()}catch(_){ } try{renderizarDashboard?.()}catch(_){ }
      try{await registrarAuditoria?.('AGENDA',resp==='COMPARECEU'?'CLIENTE_COMPARECEU':'CLIENTE_NAO_COMPARECEU',ag.id,{cliente:ag.clienteNome||ag.cliente_nome,data:ag.data,horario:ag.horario})}catch(_){ }
      alert(resp==='COMPARECEU'?'Comparecimento registrado.':'Não comparecimento registrado.');
    }catch(e){console.error(e);alert('Não foi possível registrar a presença: '+(e?.message||'erro desconhecido'));}
    finally{processando=false}
  }
  function verificar(){
    if(atual) return; const data=hoje(), agora=minAgora();
    const candidatos=ags().filter(a=>String(a.data||'')===data && ['AGENDADO','CONFIRMADO'].includes(String(a.status||'').toUpperCase()) && !a.comparecimentoStatus && !a.comparecimento_status && !jaAvisado(a.id));
    candidatos.sort((a,b)=>minHora(a.horario)-minHora(b.horario));
    const ag=candidatos.find(a=>{const dif=agora-minHora(a.horario);return dif>=0&&dif<=15});
    if(ag) exibir(ag);
  }
  window.verificarPresencaAgendadaV36=verificar;
  setInterval(verificar,15000);
  document.addEventListener('visibilitychange',()=>{if(!document.hidden)verificar()});
  window.addEventListener('focus',verificar);
  setTimeout(verificar,1800);
})();
</script>
'''
if '</body>' not in s: raise SystemExit('body nao encontrado')
s=s.replace('</body>',bloco+'\n</body>',1)
p.write_text(s,encoding='utf-8')

sw=Path('service-worker.js')
t=sw.read_text(encoding='utf-8')
import re
t=re.sub(r"const CACHE_VERSION = '[^']+';", "const CACHE_VERSION = 'simpla-shell-v36-presenca-horario';", t, count=1)
sw.write_text(t,encoding='utf-8')
print('v36 aplicada')
