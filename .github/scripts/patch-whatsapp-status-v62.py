from pathlib import Path
import re

idx=Path('index.html')
sw=Path('service-worker.js')
html=idx.read_text(encoding='utf-8')

if 'simpla-whatsapp-config-v62' in html:
    raise SystemExit('v62 ja aplicada')

marker='</body>'
if marker not in html:
    raise SystemExit('body nao encontrado')

block=r'''
<style id="simpla-whatsapp-config-v62-css">
  .simpla-wa-v62{margin:0 0 18px;border:1px solid #dbe4ee;border-radius:12px;background:#fff;padding:16px;box-shadow:0 2px 5px rgba(15,23,42,.04);text-transform:none}
  .simpla-wa-v62-head{display:flex;justify-content:space-between;gap:12px;align-items:flex-start;flex-wrap:wrap;margin-bottom:12px}
  .simpla-wa-v62 h3{margin:0;font-size:16px;color:#1a1c23}.simpla-wa-v62 p{margin:4px 0 0;font-size:11px;color:#718096;line-height:1.5;text-transform:none}
  .simpla-wa-v62-badge{display:inline-flex;padding:6px 9px;border-radius:999px;font-size:9px;font-weight:900;text-transform:uppercase;background:#edf2f7;color:#4a5568}
  .simpla-wa-v62-badge.ativo{background:#f0fff4;color:#2f855a}.simpla-wa-v62-badge.erro{background:#fff5f5;color:#c53030}.simpla-wa-v62-badge.lock{background:#fffaf0;color:#975a16}
  .simpla-wa-v62-grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:8px;margin-top:12px}
  .simpla-wa-v62-cell{border:1px solid #edf2f7;border-radius:8px;background:#f8fafc;padding:10px;min-width:0}
  .simpla-wa-v62-cell span{display:block;font-size:8px;color:#718096;font-weight:900;margin-bottom:4px}.simpla-wa-v62-cell b{display:block;font-size:11px;color:#2d3748;overflow-wrap:anywhere;text-transform:none}
  .simpla-wa-v62-note{margin-top:12px;padding:10px 11px;border:1px solid #bee3f8;background:#ebf8ff;border-radius:8px;color:#2c5282;font-size:10px;line-height:1.5;text-transform:none}
  .simpla-wa-v62-actions{margin-top:12px;display:flex;gap:8px;flex-wrap:wrap}.simpla-wa-v62-actions button{border:0;border-radius:7px;padding:9px 11px;cursor:pointer;font-size:9px;font-weight:900}
  .simpla-wa-v62-refresh{background:#1a1c23;color:#fff}.simpla-wa-v62-planos{background:#edf2f7;color:#2d3748}
  @media(max-width:760px){.simpla-wa-v62-grid{grid-template-columns:1fr}}
</style>
<script id="simpla-whatsapp-config-v62">
(function(){
  function garantir(){
    let box=document.getElementById('simpla-wa-v62');if(box)return box;
    const usuarios=document.getElementById('box-cfg-usuarios');
    const config=document.getElementById('configuracoes');
    if(!usuarios&&!config)return null;
    box=document.createElement('section');
    box.id='simpla-wa-v62';box.className='simpla-wa-v62';
    box.innerHTML='<div class="simpla-wa-v62-head"><div><h3>WhatsApp operacional</h3><p>Conexão oficial para confirmações, lembretes, cancelamentos e reagendamentos. Campanhas permanecem separadas.</p></div><span id="simpla-wa-v62-badge" class="simpla-wa-v62-badge">Carregando</span></div><div class="simpla-wa-v62-grid"><div class="simpla-wa-v62-cell"><span>PROVEDOR</span><b id="simpla-wa-v62-provedor">Meta Cloud API</b></div><div class="simpla-wa-v62-cell"><span>NÚMERO CONECTADO</span><b id="simpla-wa-v62-numero">—</b></div><div class="simpla-wa-v62-cell"><span>ÚLTIMA VALIDAÇÃO</span><b id="simpla-wa-v62-validacao">—</b></div></div><div id="simpla-wa-v62-note" class="simpla-wa-v62-note">Consultando status da integração...</div><div class="simpla-wa-v62-actions"><button type="button" class="simpla-wa-v62-refresh" onclick="carregarWhatsAppConfigV62()">Atualizar status</button><button type="button" class="simpla-wa-v62-planos" onclick="abrirPlanosWhatsAppV62()" style="display:none">Ver planos</button></div>';
    if(usuarios)usuarios.insertAdjacentElement('beforebegin',box);else config.appendChild(box);
    return box;
  }
  function fmtData(v){if(!v)return '—';try{return new Date(v).toLocaleString('pt-BR')}catch(_){return '—'}}
  function planos(){try{if(typeof mudarTela==='function')mudarTela('configuracoes')}catch(_){}
    setTimeout(()=>document.getElementById('simpla-meu-plano-v57')?.scrollIntoView({behavior:'smooth',block:'center'}),80)}
  window.abrirPlanosWhatsAppV62=planos;
  async function carregar(){
    const box=garantir();
    if(!box||typeof CloudDB==='undefined'||!CloudDB||typeof empresaAtual==='undefined'||!empresaAtual?.id)return;
    const badge=document.getElementById('simpla-wa-v62-badge'), note=document.getElementById('simpla-wa-v62-note'), btnPlanos=box.querySelector('.simpla-wa-v62-planos');
    try{
      const {data:perfil}=await CloudDB.rpc('perfil_na_empresa',{p_empresa_id:empresaAtual.id});
      if(String(perfil||'').toUpperCase()!=='ADMIN'){box.style.display='none';return}
      box.style.display='block';
      const permitido=typeof empresaPodeUsarRecurso==='function'?await empresaPodeUsarRecurso('whatsapp_operacional'):false;
      if(!permitido){
        badge.textContent='Disponível no Plus';badge.className='simpla-wa-v62-badge lock';
        note.innerHTML='<b>WhatsApp operacional</b> está disponível a partir do Plus. O recurso inclui mensagens transacionais ligadas à agenda; campanhas comerciais são exclusivas do Pro.';
        btnPlanos.style.display='inline-block';return;
      }
      btnPlanos.style.display='none';
      const {data,error}=await CloudDB.from('whatsapp_integracoes').select('provedor,phone_number_id,numero_exibicao,status,ativo,ultima_validacao_em,ultimo_erro').eq('empresa_id',empresaAtual.id).maybeSingle();
      if(error)throw error;
      document.getElementById('simpla-wa-v62-provedor').textContent=data?.provedor==='META_CLOUD_API'?'Meta Cloud API':(data?.provedor||'Meta Cloud API');
      document.getElementById('simpla-wa-v62-numero').textContent=data?.numero_exibicao||'Não conectado';
      document.getElementById('simpla-wa-v62-validacao').textContent=fmtData(data?.ultima_validacao_em);
      if(data?.ativo&&data?.status==='ATIVO'){
        badge.textContent='Conectado';badge.className='simpla-wa-v62-badge ativo';
        note.textContent='Integração ativa. As credenciais permanecem protegidas no backend e não são exibidas nesta tela.';
      }else if(data?.status==='ERRO'){
        badge.textContent='Erro';badge.className='simpla-wa-v62-badge erro';
        note.textContent=data?.ultimo_erro||'A integração precisa ser validada novamente.';
      }else{
        badge.textContent='Não configurado';badge.className='simpla-wa-v62-badge';
        note.textContent='A estrutura segura já está pronta. A conexão da conta Meta será realizada sem armazenar token no navegador.';
      }
    }catch(err){
      console.error('WhatsApp config v62:',err);
      badge.textContent='Indisponível';badge.className='simpla-wa-v62-badge erro';
      note.textContent='Não foi possível consultar o status da integração agora.';
    }
  }
  window.carregarWhatsAppConfigV62=carregar;
  function instalar(){garantir();setTimeout(carregar,900)}
  if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',()=>setTimeout(instalar,3000));else setTimeout(instalar,3000);
})();
</script>
'''

html=html.replace(marker,block+'\n'+marker,1)
idx.write_text(html,encoding='utf-8')

swtxt=sw.read_text(encoding='utf-8')
swtxt,n=re.subn(r"const CACHE_VERSION = '[^']+';","const CACHE_VERSION = 'simpla-shell-v62-whatsapp-status';",swtxt,count=1)
if n!=1: raise SystemExit('cache version nao encontrada')
sw.write_text(swtxt,encoding='utf-8')
