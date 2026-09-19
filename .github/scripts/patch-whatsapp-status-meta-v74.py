from pathlib import Path
import re

idx=Path('index.html')
sw=Path('service-worker.js')
html=idx.read_text(encoding='utf-8')

if 'simpla-whatsapp-status-meta-v74' in html:
    raise SystemExit('v74 ja aplicada')

marker='</body>'
if marker not in html:
    raise SystemExit('body nao encontrado')

block=r'''
<style id="simpla-whatsapp-status-meta-v74-css">
  .wa-meta-v74{display:inline-flex;padding:4px 7px;border-radius:999px;background:#edf2f7;color:#4a5568;font-size:8px;font-weight:900;text-transform:uppercase}
  .wa-meta-v74.sent{background:#ebf8ff;color:#2b6cb0}
  .wa-meta-v74.delivered{background:#f0fff4;color:#2f855a}
  .wa-meta-v74.read{background:#e6fffa;color:#2c7a7b}
  .wa-meta-v74.failed{background:#fff5f5;color:#c53030}
</style>
<script id="simpla-whatsapp-status-meta-v74">
(function(){
  function esc(v){return String(v??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]))}
  function data(v){if(!v)return '—';try{return new Date(v).toLocaleString('pt-BR')}catch(_){return '—'}}
  function local(v){if(!v)return '—';const s=String(v).replace('T',' ');return esc(s.slice(0,16))}
  function telefone(v){
    const d=String(v||'').replace(/\D/g,'');
    if(d.length<6)return '—';
    return d.slice(0,2)+'•••••'+d.slice(-3);
  }
  function metaLabel(s){
    const x=String(s||'').toLowerCase();
    return ({sent:'Enviado',delivered:'Entregue',read:'Lido',failed:'Falhou'})[x]||'—';
  }
  function detalhe(r){
    const partes=[];
    if(r.entregue_em) partes.push('Entregue: '+data(r.entregue_em));
    if(r.lido_em) partes.push('Lido: '+data(r.lido_em));
    if(r.falhou_em) partes.push('Falhou: '+data(r.falhou_em));
    if(r.provider_erro_codigo) partes.push('Código Meta: '+esc(r.provider_erro_codigo));
    if(r.erro) partes.push(esc(r.erro));
    if(!partes.length && r.provider_message_id) partes.push('ID Meta: '+esc(String(r.provider_message_id).slice(-14)));
    return partes.length?partes.join('<br>'):'—';
  }
  async function admin(){
    if(typeof CloudDB==='undefined'||!CloudDB||typeof empresaAtual==='undefined'||!empresaAtual?.id)return false;
    const {data}=await CloudDB.rpc('perfil_na_empresa',{p_empresa_id:empresaAtual.id});
    return String(data||'').toUpperCase()==='ADMIN';
  }
  async function carregar(){
    if(!document.getElementById('simpla-wa-monitor-v67')||!await admin())return;
    try{
      const table=document.querySelector('#simpla-wa-monitor-v67 .simpla-wa-monitor-v67-table');
      if(table){
        const head=table.querySelector('thead tr');
        if(head && !head.querySelector('[data-meta-v74]')){
          const th=document.createElement('th');
          th.dataset.metaV74='1';
          th.textContent='Status Meta';
          head.insertBefore(th,head.lastElementChild);
        }
      }

      const {data:rows,error}=await CloudDB.from('whatsapp_mensagens_operacionais')
        .select('id,tipo,destino,status,origem_automacao,processar_em_local,provider_message_id,provider_status,entregue_em,lido_em,falhou_em,provider_erro_codigo,erro,criado_em')
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
      if(!body)return;
      if(!lista.length){
        body.innerHTML='<tr><td colspan="8"><div class="simpla-wa-monitor-v67-empty">A fila ainda está vazia. Novos eventos de agenda aparecerão aqui quando houver regras e templates ativos.</div></td></tr>';
        return;
      }

      body.innerHTML=lista.map(r=>{
        const ps=String(r.provider_status||'').toLowerCase();
        return '<tr>'+
          '<td>'+data(r.criado_em)+'</td>'+
          '<td>'+esc(r.tipo)+'</td>'+
          '<td>'+telefone(r.destino)+'</td>'+
          '<td><span class="simpla-wa-monitor-v67-badge '+esc(r.status)+'">'+esc(r.status)+'</span></td>'+
          '<td>'+(r.origem_automacao?'Automação':'Manual')+'</td>'+
          '<td>'+local(r.processar_em_local)+'</td>'+
          '<td><span class="wa-meta-v74 '+esc(ps)+'">'+metaLabel(ps)+'</span></td>'+
          '<td>'+detalhe(r)+'</td>'+
        '</tr>';
      }).join('');
    }catch(err){
      console.error('Status Meta WhatsApp v74:',err);
    }
  }

  window.carregarStatusMetaWhatsAppV74=carregar;

  const instalar=function(){
    const old=window.carregarMonitorWhatsAppV67;
    if(typeof old==='function' && !old.__v74){
      const wrapped=async function(){
        try{await old.apply(this,arguments)}catch(_){}
        await carregar();
      };
      wrapped.__v74=true;
      window.carregarMonitorWhatsAppV67=wrapped;
    }
    setTimeout(carregar,300);
  };

  if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',()=>setTimeout(instalar,6500));
  else setTimeout(instalar,6500);

  document.addEventListener('click',e=>{
    const b=e.target.closest?.('.cfg-v2-nav button');
    if(b&&b.dataset.cat==='WhatsApp e Automações')setTimeout(carregar,180);
  },true);

  setTimeout(instalar,8500);
})();
</script>
'''

html=html.replace(marker,block+'\n'+marker,1)
idx.write_text(html,encoding='utf-8')

swtxt=sw.read_text(encoding='utf-8')
swtxt,n=re.subn(r"const CACHE_VERSION = '[^']+';","const CACHE_VERSION = 'simpla-shell-v74-whatsapp-status-meta';",swtxt,count=1)
if n!=1: raise SystemExit('cache version nao encontrada')
sw.write_text(swtxt,encoding='utf-8')
