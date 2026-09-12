from pathlib import Path
import re

idx=Path('index.html')
sw=Path('service-worker.js')
html=idx.read_text(encoding='utf-8')

if 'simpla-recorrencia-auditoria-v60' in html:
    raise SystemExit('v60 ja aplicada')

marker='</body>'
if marker not in html:
    raise SystemExit('body nao encontrado')

block=r'''
<style id="simpla-recorrencia-auditoria-v60-css">
  .simpla-entitlement-inline-v60{margin-top:8px;padding:9px 10px;border:1px solid #bee3f8;border-radius:8px;background:#ebf8ff;color:#2c5282;font-size:10px;line-height:1.45;text-transform:none}
  .simpla-entitlement-auditoria-v60{position:relative!important;overflow:hidden;min-height:185px}
  .simpla-entitlement-auditoria-v60>.simpla-entitlement-auditoria-overlay-v60{position:absolute;inset:0;z-index:55;display:flex;align-items:center;justify-content:center;padding:18px;background:rgba(248,250,252,.95);backdrop-filter:blur(2px);text-align:center;text-transform:none}
  .simpla-entitlement-auditoria-card-v60{max-width:390px;padding:18px;border:1px solid #dbe4ee;border-radius:12px;background:#fff;box-shadow:0 8px 28px rgba(15,23,42,.10)}
  .simpla-entitlement-auditoria-card-v60 span{display:inline-flex;padding:5px 8px;border-radius:999px;background:#ebf8ff;color:#2b6cb0;font-size:8px;font-weight:900;text-transform:uppercase;margin-bottom:8px}
  .simpla-entitlement-auditoria-card-v60 h4{margin:0 0 6px;font-size:15px;color:#1a1c23}.simpla-entitlement-auditoria-card-v60 p{margin:0 0 12px;font-size:10px;line-height:1.5;color:#718096;text-transform:none}
  .simpla-entitlement-auditoria-card-v60 button{border:0;border-radius:7px;padding:8px 11px;background:#1a1c23;color:#fff;font-size:9px;font-weight:900;cursor:pointer}
</style>
<script id="simpla-recorrencia-auditoria-v60">
(function(){
  let aplicando=false;
  function modoTeste(){try{return !!empresaAtual?.modo_teste||String(empresaAtual?.plano_codigo||'').toUpperCase()==='TESTE'}catch(_){return false}}
  function abrirPlano(){if(typeof abrirMeuPlanoV58==='function')return abrirMeuPlanoV58();try{if(typeof mudarTela==='function')mudarTela('configuracoes')}catch(_){}}
  async function pode(recurso){if(modoTeste())return true;if(typeof empresaPodeUsarRecurso!=='function')return true;return await empresaPodeUsarRecurso(recurso)}

  function ajustarRecorrencia(ok){
    const sel=document.getElementById('cfg-gestao-servico-recorrencia');if(!sel)return;
    const opt=[...sel.options].find(o=>String(o.value).toUpperCase()==='PERSONALIZADA');
    if(opt){opt.disabled=!ok;opt.textContent=ok?'Personalizada':'Personalizada · Plus'}
    let aviso=document.getElementById('simpla-recorrencia-avancada-v60-aviso');
    if(!ok){
      if(sel.value==='PERSONALIZADA'){sel.value='NENHUMA';try{atualizarCampoRecorrenciaPersonalizada()}catch(_){}}
      if(!aviso){aviso=document.createElement('div');aviso.id='simpla-recorrencia-avancada-v60-aviso';aviso.className='simpla-entitlement-inline-v60';aviso.innerHTML='<b>Recorrência personalizada disponível no Plus.</b> O Básico continua com as opções padrão de recorrência. <button type="button" onclick="abrirMeuPlanoV60()" style="margin-left:6px;border:0;background:none;color:#2b6cb0;font-weight:800;cursor:pointer;text-decoration:underline;">Ver planos</button>';sel.parentElement?.appendChild(aviso)}
    }else aviso?.remove();
  }

  function ajustarAuditoria(ok){
    const box=document.getElementById('box-cfg-auditoria');if(!box)return;
    const ov=box.querySelector(':scope > .simpla-entitlement-auditoria-overlay-v60');
    if(ok){box.classList.remove('simpla-entitlement-auditoria-v60');ov?.remove();return}
    if(!ov){box.classList.add('simpla-entitlement-auditoria-v60');const x=document.createElement('div');x.className='simpla-entitlement-auditoria-overlay-v60';x.innerHTML='<div class="simpla-entitlement-auditoria-card-v60"><span>Disponível no Plus</span><h4>Histórico de Auditoria</h4><p>Acompanhe ações realizadas por usuários, módulos alterados e registros afetados para ter mais controle sobre a operação.</p><button type="button" onclick="abrirMeuPlanoV60()">Ver planos</button></div>';box.appendChild(x)}
  }

  async function aplicar(){
    if(aplicando)return;aplicando=true;
    try{
      const [rec,aud]=await Promise.all([pode('recorrencia_avancada'),pode('auditoria_completa')]);
      ajustarRecorrencia(rec);ajustarAuditoria(aud);
    }catch(err){console.warn('Entitlements recorrência/auditoria v60:',err)}finally{aplicando=false}
  }
  window.abrirMeuPlanoV60=abrirPlano;window.aplicarRecorrenciaAuditoriaV60=aplicar;

  function protegerAuditoria(){
    const original=window.carregarAuditoria;if(typeof original!=='function'||original.__simplaV60)return;
    const wrapped=async function(...args){if(!(await pode('auditoria_completa'))){abrirPlano();return false}return await original.apply(this,args)};
    wrapped.__simplaV60=true;window.carregarAuditoria=wrapped;
  }
  function instalar(){protegerAuditoria();setTimeout(()=>{protegerAuditoria();aplicar()},900);setTimeout(()=>{protegerAuditoria();aplicar()},2600);setTimeout(()=>{protegerAuditoria();aplicar()},4800)}
  if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',instalar);else instalar();
})();
</script>
'''

html=html.replace(marker,block+'\n'+marker,1)
idx.write_text(html,encoding='utf-8')

swtxt=sw.read_text(encoding='utf-8')
swtxt,n=re.subn(r"const CACHE_VERSION = '[^']+';","const CACHE_VERSION = 'simpla-shell-v60-recorrencia-auditoria';",swtxt,count=1)
if n!=1:
    raise SystemExit('cache version nao encontrada')
sw.write_text(swtxt,encoding='utf-8')
