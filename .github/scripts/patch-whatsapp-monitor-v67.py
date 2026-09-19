from pathlib import Path
import re

idx=Path('index.html')
sw=Path('service-worker.js')
html=idx.read_text(encoding='utf-8')

if 'simpla-whatsapp-monitor-v67' in html:
    raise SystemExit('v67 ja aplicada')

marker='</body>'
if marker not in html:
    raise SystemExit('body nao encontrado')

block=r'''
<style id="simpla-whatsapp-monitor-v67-css">
  .simpla-wa-monitor-v67{margin-top:16px;border:1px solid #dbe4ee;border-radius:12px;background:#fff;padding:16px;box-shadow:0 2px 5px rgba(15,23,42,.04);text-transform:none}
  .simpla-wa-monitor-v67-head{display:flex;justify-content:space-between;gap:12px;align-items:flex-start;flex-wrap:wrap}
  .simpla-wa-monitor-v67 h3{margin:0;font-size:16px;color:#1a1c23;text-transform:none}
  .simpla-wa-monitor-v67 p{margin:4px 0 0;font-size:10px;color:#718096;line-height:1.5;text-transform:none}
  .simpla-wa-monitor-v67-btn{border:0;border-radius:7px;padding:9px 11px;background:#1a1c23;color:#fff;font-size:9px;font-weight:900;cursor:pointer}
  .simpla-wa-monitor-v67-kpis{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:8px;margin-top:14px}
  .simpla-wa-monitor-v67-kpi{border:1px solid #e2e8f0;border-radius:9px;background:#f8fafc;padding:10px}
  .simpla-wa-monitor-v67-kpi span{display:block;font-size:8px;color:#718096;font-weight:900;margin-bottom:4px;text-transform:uppercase}
  .simpla-wa-monitor-v67-kpi b{font-size:18px;color:#2d3748}
  .simpla-wa-monitor-v67-table-wrap{overflow-x:auto;margin-top:12px}
  .simpla-wa-monitor-v67-table{width:100%;min-width:780px;border-collapse:collapse}
  .simpla-wa-monitor-v67-table th,.simpla-wa-monitor-v67-table td{padding:9px 8px;border-bottom:1px solid #edf2f7;font-size:10px;text-align:left;text-transform:none}
  .simpla-wa-monitor-v67-table th{font-size:8px;color:#718096;text-transform:uppercase;background:#f8fafc}
  .simpla-wa-monitor-v67-badge{display:inline-flex;padding:4px 7px;border-radius:999px;background:#edf2f7;color:#4a5568;font-size:8px;font-weight:900}
  .simpla-wa-monitor-v67-badge.ENVIADO{background:#f0fff4;color:#2f855a}
  .simpla-wa-monitor-v67-badge.ERRO{background:#fff5f5;color:#c53030}
  .simpla-wa-monitor-v67-badge.PENDENTE{background:#fffaf0;color:#975a16}
  .simpla-wa-monitor-v67-badge.CANCELADO{background:#edf2f7;color:#718096}
  .simpla-wa-monitor-v67-empty{padding:16px;text-align:center;color:#718096;font-size:10px;text-transform:none}
  .simpla-wa-monitor-v67-note{margin-top:10px;font-size:9px;color:#a0aec0;text-transform:none}
  @media(max-width:760px){.simpla-wa-monitor-v67-kpis{grid-template-columns:1fr 1fr}}
</style>
<script id="simpla-whatsapp-monitor-v67">
(function(){
  function garantir(){
    let box=document.getElementById('simpla-wa-monitor-v67'); if(box) return box;
    const area=document.getElementById('simpla-wa-categoria-v65-content'); if(!area) return null;

    box=document.createElement('section');
    box.id='simpla-wa-monitor-v67';
    box.className='simpla-wa-monitor-v67';
    box.innerHTML='<div class="simpla-wa-monitor-v67-head"><div><h3>Histórico e monitoramento</h3><p>Acompanhe o que o motor está preparando na fila operacional. Nesta fase, o painel é somente leitura.</p></div><button type="button" class="simpla-wa-monitor-v67-btn" onclick="carregarMonitorWhatsAppV67()">Atualizar histórico</button></div><div class="simpla-wa-monitor-v67-kpis"><div class="simpla-wa-monitor-v67-kpi"><span>Pendentes</span><b id="wa-mon-pendentes">0</b></div><div class="simpla-wa-monitor-v67-kpi"><span>Enviadas</span><b id="wa-mon-enviadas">0</b></div><div class="simpla-wa-monitor-v67-kpi"><span>Erros</span><b id="wa-mon-erros">0</b></div><div class="simpla-wa-monitor-v67-kpi"><span>Canceladas</span><b id="wa-mon-canceladas">0</b></div></div><div class="simpla-wa-monitor-v67-table-wrap"><table class="simpla-wa-monitor-v67-table"><thead><tr><th>Criada em</th><th>Tipo</th><th>Destino</th><th>Status</th><th>Origem</th><th>Programada</th><th>Detalhe</th></tr></thead><tbody id="wa-mon-body"></tbody></table></div><div class="simpla-wa-monitor-v67-note">O telefone é mascarado na interface. Nenhuma credencial da Meta é exibida aqui.</div>';
    const roadmap=document.getElementById('simpla-wa-roadmap-v65');
    if(roadmap && roadmap.parentElement===area) area.insertBefore(box,roadmap); else area.appendChild(box);
    return box;
  }
  function esc(v){return String(v??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]))}
  function data(v){if(!v)return '—';try{return new Date(v).toLocaleString('pt-BR')}catch(_){return '—'}}
  function local(v){if(!v)return '—';const s=String(v).replace('T',' ');return esc(s.slice(0,16))}
  function telefone(v){
    const d=String(v||'').replace(/\D/g,'');
    if(d.length<6)return '—';
    return d.slice(0,2)+'•••••'+d.slice(-3);
  }
  function detalhe(r){
    if(r.erro)return esc(r.erro);
    if(r.provider_message_id)return 'ID Meta: '+esc(String(r.provider_message_id).slice(-14));
    return '—';
  }
  async function permitido(){
    if(typeof CloudDB==='undefined'||!CloudDB||typeof empresaAtual==='undefined'||!empresaAtual?.id)return false;
    const {data:perfil}=await CloudDB.rpc('perfil_na_empresa',{p_empresa_id:empresaAtual.id});
    return String(perfil||'').toUpperCase()==='ADMIN';
  }
  async function carregar(){
    const box=garantir();if(!box||!await permitido())return;
    try{
      const {data:rows,error}=await CloudDB.from('whatsapp_mensagens_operacionais')
        .select('id,tipo,destino,status,origem_automacao,processar_em_local,provider_message_id,erro,criado_em')
        .eq('empresa_id',empresaAtual.id)
        .order('criado_em',{ascending:false})
        .limit(100);
      if(error)throw error;
      const lista=Array.isArray(rows)?rows:[];
      const n=s=>lista.filter(x=>String(x.status)===s).length;
      document.getElementById('wa-mon-pendentes').textContent=String(n('PENDENTE')+n('RASCUNHO')+n('PROCESSANDO'));
      document.getElementById('wa-mon-enviadas').textContent=String(n('ENVIADO'));
      document.getElementById('wa-mon-erros').textContent=String(n('ERRO'));
      document.getElementById('wa-mon-canceladas').textContent=String(n('CANCELADO'));
      const body=document.getElementById('wa-mon-body');
      if(!lista.length){body.innerHTML='<tr><td colspan="7"><div class="simpla-wa-monitor-v67-empty">A fila ainda está vazia. Novos eventos de agenda aparecerão aqui quando houver regras e templates ativos.</div></td></tr>';return}
      body.innerHTML=lista.map(r=>'<tr><td>'+data(r.criado_em)+'</td><td>'+esc(r.tipo)+'</td><td>'+telefone(r.destino)+'</td><td><span class="simpla-wa-monitor-v67-badge '+esc(r.status)+'">'+esc(r.status)+'</span></td><td>'+(r.origem_automacao?'Automação':'Manual')+'</td><td>'+local(r.processar_em_local)+'</td><td>'+detalhe(r)+'</td></tr>').join('');
    }catch(err){
      console.error('Monitor WhatsApp v67:',err);
      const body=document.getElementById('wa-mon-body');
      if(body)body.innerHTML='<tr><td colspan="7"><div class="simpla-wa-monitor-v67-empty">Não foi possível carregar o histórico agora.</div></td></tr>';
    }
  }
  window.carregarMonitorWhatsAppV67=carregar;
  function instalar(){garantir();setTimeout(carregar,900)}
  if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',()=>setTimeout(instalar,5000));else setTimeout(instalar,5000);
  document.addEventListener('click',e=>{
    const b=e.target.closest?.('.cfg-v2-nav button');
    if(b&&b.dataset.cat==='WhatsApp e Automações')setTimeout(carregar,150);
  },true);
  setTimeout(instalar,7000);
})();
</script>
'''

html=html.replace(marker,block+'\n'+marker,1)
idx.write_text(html,encoding='utf-8')

swtxt=sw.read_text(encoding='utf-8')
swtxt,n=re.subn(r"const CACHE_VERSION = '[^']+';","const CACHE_VERSION = 'simpla-shell-v67-whatsapp-monitor';",swtxt,count=1)
if n!=1: raise SystemExit('cache version nao encontrada')
sw.write_text(swtxt,encoding='utf-8')
