from pathlib import Path
import re

idx=Path('index.html')
sw=Path('service-worker.js')
html=idx.read_text(encoding='utf-8')

if 'simpla-whatsapp-cota-v71' in html:
    raise SystemExit('v71 ja aplicada')

marker='</body>'
if marker not in html:
    raise SystemExit('body nao encontrado')

block=r'''
<style id="simpla-whatsapp-cota-v71-css">
  .simpla-wa-cota-v71{margin:0 0 16px;border:1px solid #dbe4ee;border-radius:12px;background:#fff;padding:16px;box-shadow:0 2px 5px rgba(15,23,42,.04);text-transform:none}
  .simpla-wa-cota-v71-head{display:flex;justify-content:space-between;gap:12px;align-items:flex-start;flex-wrap:wrap}
  .simpla-wa-cota-v71 h3{margin:0;font-size:16px;color:#1a1c23;text-transform:none}
  .simpla-wa-cota-v71 p{margin:4px 0 0;font-size:10px;color:#718096;line-height:1.5;text-transform:none}
  .simpla-wa-cota-v71-plan{display:inline-flex;align-items:center;padding:6px 9px;border-radius:999px;background:#edf2f7;color:#4a5568;font-size:9px;font-weight:900;text-transform:uppercase}
  .simpla-wa-cota-v71-progress-wrap{margin-top:14px}
  .simpla-wa-cota-v71-progress-top{display:flex;justify-content:space-between;gap:10px;align-items:center;margin-bottom:6px;font-size:9px;color:#718096;text-transform:none}
  .simpla-wa-cota-v71-bar{height:12px;border-radius:999px;background:#edf2f7;overflow:hidden}
  .simpla-wa-cota-v71-fill{height:100%;width:0%;background:#2d3748;border-radius:999px;transition:width .3s ease}
  .simpla-wa-cota-v71-grid{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:8px;margin-top:12px}
  .simpla-wa-cota-v71-kpi{border:1px solid #e2e8f0;border-radius:9px;background:#f8fafc;padding:10px}
  .simpla-wa-cota-v71-kpi span{display:block;font-size:8px;font-weight:900;color:#718096;margin-bottom:4px;text-transform:uppercase}
  .simpla-wa-cota-v71-kpi b{display:block;font-size:18px;color:#2d3748;text-transform:none}
  .simpla-wa-cota-v71-foot{display:flex;justify-content:space-between;gap:10px;align-items:center;flex-wrap:wrap;margin-top:10px}
  .simpla-wa-cota-v71-note{font-size:9px;color:#718096;line-height:1.4;text-transform:none}
  .simpla-wa-cota-v71-btn{border:0;border-radius:7px;padding:8px 10px;background:#edf2f7;color:#2d3748;font-size:8px;font-weight:900;cursor:pointer}
  .simpla-wa-cota-v71-alert{margin-top:10px;padding:9px 10px;border-radius:8px;background:#fffaf0;border:1px solid #f6e05e;color:#744210;font-size:10px;line-height:1.4;text-transform:none;display:none}
  @media(max-width:760px){.simpla-wa-cota-v71-grid{grid-template-columns:1fr 1fr}}
</style>

<script id="simpla-whatsapp-cota-v71">
(function(){
  function garantir(){
    let box=document.getElementById('simpla-wa-cota-v71');if(box)return box;
    const area=document.getElementById('simpla-wa-categoria-v65-content');if(!area)return null;

    box=document.createElement('section');
    box.id='simpla-wa-cota-v71';
    box.className='simpla-wa-cota-v71';
    box.innerHTML='<div class="simpla-wa-cota-v71-head"><div><h3>Franquia mensal do WhatsApp</h3><p>Acompanhe o consumo de mensagens operacionais deste mês antes de configurar ou ativar automações.</p></div><span id="wa-cota-plan-v71" class="simpla-wa-cota-v71-plan">Carregando</span></div><div class="simpla-wa-cota-v71-progress-wrap"><div class="simpla-wa-cota-v71-progress-top"><span id="wa-cota-periodo-v71">Período atual</span><b id="wa-cota-percent-v71">—</b></div><div class="simpla-wa-cota-v71-bar"><div id="wa-cota-fill-v71" class="simpla-wa-cota-v71-fill"></div></div></div><div class="simpla-wa-cota-v71-grid"><div class="simpla-wa-cota-v71-kpi"><span>Enviadas no mês</span><b id="wa-cota-enviadas-v71">0</b></div><div class="simpla-wa-cota-v71-kpi"><span>Em processamento</span><b id="wa-cota-processando-v71">0</b></div><div class="simpla-wa-cota-v71-kpi"><span>Restantes</span><b id="wa-cota-restantes-v71">—</b></div><div class="simpla-wa-cota-v71-kpi"><span>Limite mensal</span><b id="wa-cota-limite-v71">—</b></div></div><div id="wa-cota-alert-v71" class="simpla-wa-cota-v71-alert"></div><div class="simpla-wa-cota-v71-foot"><span id="wa-cota-note-v71" class="simpla-wa-cota-v71-note"></span><button type="button" class="simpla-wa-cota-v71-btn" onclick="carregarCotaWhatsAppV71()">Atualizar consumo</button></div>';

    area.insertBefore(box,area.firstChild);
    return box;
  }

  function fmtPeriodo(ini,fim){
    try{
      const a=new Date(ini), b=new Date(fim);
      const mes=a.toLocaleDateString('pt-BR',{month:'long',year:'numeric'});
      return mes.charAt(0).toUpperCase()+mes.slice(1)+' · renova em '+b.toLocaleDateString('pt-BR');
    }catch(_){return 'Período mensal atual'}
  }

  async function admin(){
    if(typeof CloudDB==='undefined'||!CloudDB||typeof empresaAtual==='undefined'||!empresaAtual?.id)return false;
    const {data}=await CloudDB.rpc('perfil_na_empresa',{p_empresa_id:empresaAtual.id});
    return String(data||'').toUpperCase()==='ADMIN';
  }

  function render(r){
    const teste=!!r?.modo_teste||String(r?.plano_codigo||'').toUpperCase()==='TESTE';
    const definido=!!r?.limite_definido;
    const limite=Number(r?.limite_mensal??0);
    const enviadas=Number(r?.enviadas_mes||0);
    const processando=Number(r?.em_processamento||0);
    const restantes=r?.restantes;
    const perc=Number(r?.percentual_consumido||0);

    document.getElementById('wa-cota-plan-v71').textContent='Plano '+String(r?.plano_codigo||'—');
    document.getElementById('wa-cota-enviadas-v71').textContent=String(enviadas);
    document.getElementById('wa-cota-processando-v71').textContent=String(processando);
    document.getElementById('wa-cota-periodo-v71').textContent=fmtPeriodo(r?.periodo_inicio,r?.periodo_fim);

    const alert=document.getElementById('wa-cota-alert-v71');
    const note=document.getElementById('wa-cota-note-v71');

    if(teste){
      document.getElementById('wa-cota-restantes-v71').textContent='Ilimitadas';
      document.getElementById('wa-cota-limite-v71').textContent='Ilimitado';
      document.getElementById('wa-cota-percent-v71').textContent='Conta de testes';
      document.getElementById('wa-cota-fill-v71').style.width='0%';
      note.textContent='A conta TESTE não consome franquia comercial durante o desenvolvimento.';
      alert.style.display='none';
      return;
    }

    if(!definido){
      document.getElementById('wa-cota-restantes-v71').textContent='A definir';
      document.getElementById('wa-cota-limite-v71').textContent='A definir';
      document.getElementById('wa-cota-percent-v71').textContent='Franquia comercial pendente';
      document.getElementById('wa-cota-fill-v71').style.width='0%';
      note.textContent='O limite mensal deste plano ainda será definido na etapa de precificação.';
      alert.style.display='none';
      return;
    }

    document.getElementById('wa-cota-restantes-v71').textContent=String(Math.max(0,Number(restantes||0)));
    document.getElementById('wa-cota-limite-v71').textContent=String(limite);
    document.getElementById('wa-cota-percent-v71').textContent=(limite===0?'100':String(perc||0))+'% utilizado';
    document.getElementById('wa-cota-fill-v71').style.width=Math.max(0,Math.min(100,limite===0?100:perc))+'%';
    note.textContent='A franquia considera apenas mensagens realmente enviadas e reservas atualmente em processamento.';

    if(limite===0){
      alert.textContent='Este plano não possui franquia de WhatsApp operacional.';
      alert.style.display='block';
    }else if(Number(restantes||0)<=0){
      alert.textContent='A franquia mensal foi atingida. Novos envios ficam bloqueados até a renovação ou alteração do plano.';
      alert.style.display='block';
    }else if(perc>=80){
      alert.textContent='A franquia está próxima do limite mensal.';
      alert.style.display='block';
    }else{
      alert.style.display='none';
    }
  }

  async function carregar(){
    const box=garantir();if(!box||!await admin())return;
    try{
      const {data,error}=await CloudDB.rpc('status_cota_whatsapp_empresa',{p_empresa_id:empresaAtual.id});
      if(error)throw error;
      const r=Array.isArray(data)?data[0]:data;
      if(!r)throw new Error('Status da franquia indisponível.');
      render(r);
    }catch(err){
      console.error('Cota WhatsApp v71:',err);
      document.getElementById('wa-cota-note-v71').textContent='Não foi possível consultar a franquia agora.';
    }
  }

  window.carregarCotaWhatsAppV71=carregar;

  function instalar(){garantir();setTimeout(carregar,500)}
  if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',()=>setTimeout(instalar,4300));else setTimeout(instalar,4300);

  document.addEventListener('click',e=>{
    const b=e.target.closest?.('.cfg-v2-nav button');
    if(b&&b.dataset.cat==='WhatsApp e Automações')setTimeout(carregar,100);
  },true);

  const originalMonitor=window.carregarMonitorWhatsAppV67;
  if(typeof originalMonitor==='function'){
    window.carregarMonitorWhatsAppV67=async function(){
      const r=await originalMonitor.apply(this,arguments);
      setTimeout(carregar,80);
      return r;
    };
  }

  setTimeout(instalar,7200);
})();
</script>
'''

html=html.replace(marker,block+'\n'+marker,1)
idx.write_text(html,encoding='utf-8')

swtxt=sw.read_text(encoding='utf-8')
swtxt,n=re.subn(r"const CACHE_VERSION = '[^']+';","const CACHE_VERSION = 'simpla-shell-v71-whatsapp-cota';",swtxt,count=1)
if n!=1: raise SystemExit('cache version nao encontrada')
sw.write_text(swtxt,encoding='utf-8')
