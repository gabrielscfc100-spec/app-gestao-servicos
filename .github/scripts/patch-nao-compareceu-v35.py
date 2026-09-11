from pathlib import Path

index = Path('index.html')
sw = Path('service-worker.js')
html = index.read_text(encoding='utf-8')

marker = 'simpla-nao-compareceu-v35-script'
if marker not in html:
    bloco = r'''
<style id="simpla-nao-compareceu-v35">
.btn-nao-compareceu-v35{flex:1 1 100%;font-size:12px;padding:8px;border:none;border-radius:4px;background:#4a5568;color:#fff;font-weight:700;cursor:pointer}
.btn-nao-compareceu-v35:hover{background:#2d3748}
@media(max-width:768px){.btn-nao-compareceu-v35{width:100%;min-height:40px}}
</style>
<script id="simpla-nao-compareceu-v35-script">
(function(){
  function hojeLocalV35(){
    const d=new Date();
    return [d.getFullYear(),String(d.getMonth()+1).padStart(2,'0'),String(d.getDate()).padStart(2,'0')].join('-');
  }
  function horarioJaAtingidoV35(ag){
    const data=String(ag?.data||'');
    const hoje=hojeLocalV35();
    if(!data) return false;
    if(data<hoje) return true;
    if(data>hoje) return false;
    const partes=String(ag?.horario||'00:00').split(':').map(Number);
    const agora=new Date();
    return (agora.getHours()*60+agora.getMinutes()) >= ((partes[0]||0)*60+(partes[1]||0));
  }
  function idDoBotaoV35(btn){
    const txt=String(btn?.getAttribute('onclick')||'');
    const m=txt.match(/iniciarRecebimentoAgendamento\(['\"]([^'\"]+)['\"]\)/);
    return m?m[1]:null;
  }
  window.marcarNaoCompareceuV35=async function(id){
    if(typeof validarAcessoPerfil==='function' && !validarAcessoPerfil('agendaEditar','Seu perfil possui apenas consulta da Agenda.')) return;
    const ag=(typeof agendamentos!=='undefined'?agendamentos:[]).find(a=>String(a.id)===String(id));
    if(!ag){alert('Agendamento não localizado.');return;}
    const status=String(ag.status||'AGENDADO').toUpperCase();
    if(!['AGENDADO','CONFIRMADO'].includes(status)){alert('Este agendamento não pode ser marcado como não compareceu no status atual.');return;}
    if(!horarioJaAtingidoV35(ag)){alert('O não comparecimento só pode ser registrado a partir do horário agendado.');return;}
    if(!confirm('Confirmar que o cliente NÃO COMPARECEU a este agendamento? Esse status ficará registrado para os indicadores.')) return;
    try{
      const agora=new Date().toISOString();
      if(typeof AGENDA_CLOUD_ATIVO!=='undefined' && AGENDA_CLOUD_ATIVO && typeof CloudDB!=='undefined' && CloudDB && typeof empresaAtual!=='undefined' && empresaAtual?.cloud){
        const {error}=await CloudDB.from('agendamentos').update({status:'NAO_COMPARECEU',atualizado_em:agora}).eq('id',id).eq('empresa_id',empresaAtual.id);
        if(error) throw error;
      }
      ag.status='NAO_COMPARECEU';
      ag.atualizadoEm=agora;
      if(typeof salvarCacheAgendaCloud==='function') salvarCacheAgendaCloud();
      if(typeof renderizarAgenda==='function') renderizarAgenda();
      if(typeof renderizarDashboard==='function') renderizarDashboard();
      if(typeof registrarAuditoria==='function') await registrarAuditoria('AGENDA','AGENDAMENTO_NAO_COMPARECEU',id,{cliente:ag.clienteNome||ag.cliente_nome||'',data:ag.data,horario:ag.horario,profissionalId:ag.profissionalId||ag.profissional_id||null,servico:ag.servico||ag.servicoNome||ag.servico_nome||''});
    }catch(err){
      console.error('SimplA v35 - não compareceu:',err);
      alert('Não foi possível registrar o não comparecimento: '+(err?.message||'erro desconhecido'));
    }
  };
  function injetarV35(){
    if(typeof agendamentos==='undefined') return;
    document.querySelectorAll('#agenda .slot-card').forEach(card=>{
      const finalizar=card.querySelector('button[onclick*="iniciarRecebimentoAgendamento"]');
      if(!finalizar) return;
      const id=idDoBotaoV35(finalizar); if(!id) return;
      const ag=agendamentos.find(a=>String(a.id)===String(id)); if(!ag) return;
      const status=String(ag.status||'AGENDADO').toUpperCase();
      if(status==='NAO_COMPARECEU'){
        finalizar.disabled=true;
        finalizar.textContent='NÃO COMPARECEU REGISTRADO';
        finalizar.style.background='#718096';
        finalizar.style.cursor='not-allowed';
        return;
      }
      if(!['AGENDADO','CONFIRMADO'].includes(status) || !horarioJaAtingidoV35(ag)) return;
      if(card.querySelector('.btn-nao-compareceu-v35')) return;
      const btn=document.createElement('button');
      btn.type='button';
      btn.className='btn-nao-compareceu-v35';
      btn.textContent='NÃO COMPARECEU';
      btn.onclick=()=>window.marcarNaoCompareceuV35(id);
      finalizar.insertAdjacentElement('afterend',btn);
    });
  }
  const original=typeof renderizarAgenda==='function'?renderizarAgenda:null;
  if(original){
    renderizarAgenda=function(){
      const ret=original.apply(this,arguments);
      setTimeout(injetarV35,0);
      return ret;
    };
  }
  window.addEventListener('load',()=>setTimeout(injetarV35,1200));
})();
</script>
'''
    if '</body>' not in html:
        raise SystemExit('Fechamento </body> não encontrado')
    html = html.replace('</body>', bloco + '\n</body>', 1)
    index.write_text(html, encoding='utf-8')

sw_text = sw.read_text(encoding='utf-8')
import re
sw_text, n = re.subn(r"const CACHE_VERSION = '[^']+';", "const CACHE_VERSION = 'simpla-shell-v35-nao-compareceu';", sw_text, count=1)
if n != 1:
    raise SystemExit('CACHE_VERSION não localizado')
sw.write_text(sw_text, encoding='utf-8')

print('v35 aplicada')
