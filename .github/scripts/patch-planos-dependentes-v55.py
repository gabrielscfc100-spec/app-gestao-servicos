from pathlib import Path
import re

idx=Path('index.html')
sw=Path('service-worker.js')
html=idx.read_text(encoding='utf-8')

if 'simpla-planos-dependentes-v55' in html:
    raise SystemExit('v55 ja aplicada')

marker='</body>'
if marker not in html:
    raise SystemExit('body nao encontrado')

block=r'''
<style id="simpla-planos-dependentes-v55-css">
  .simpla-plano-v55{margin:0 0 14px;padding:11px 12px;border:1px solid #dbe4ee;border-radius:8px;background:#f8fafc;font-size:11px;color:#475569;text-transform:none;line-height:1.45}
  .simpla-plano-v55 b{color:#1a1c23}
  .simpla-plano-v55.teste{background:#ebf8ff;border-color:#bee3f8;color:#2c5282}
</style>
<script id="simpla-planos-dependentes-v55">
(function(){
  let statusPlano=null;
  async function carregarStatusPlano(){
    if(typeof CloudDB==='undefined'||!CloudDB||typeof empresaAtual==='undefined'||!empresaAtual?.id)return null;
    try{
      const {data,error}=await CloudDB.rpc('status_limite_dependentes_empresa',{p_empresa_id:empresaAtual.id});
      if(error)throw error;
      statusPlano=Array.isArray(data)?data[0]:(data||null);
      window.simplaStatusPlanoV55=statusPlano;
      renderizarStatusPlano();
      return statusPlano;
    }catch(err){console.error('Status do plano v55:',err);return null}
  }
  function renderizarStatusPlano(){
    const box=document.getElementById('box-cfg-usuarios');if(!box||!statusPlano)return;
    let el=document.getElementById('simpla-plano-v55');
    if(!el){el=document.createElement('div');el.id='simpla-plano-v55';el.className='simpla-plano-v55';box.insertAdjacentElement('afterbegin',el)}
    const teste=!!statusPlano.modo_teste||String(statusPlano.plano_codigo||'').toUpperCase()==='TESTE'||statusPlano.limite_dependentes==null;
    el.classList.toggle('teste',teste);
    if(teste){
      el.innerHTML='<b>Conta de testes</b> · sem limitações de plano, dependentes ou recursos durante o desenvolvimento.';
    }else{
      const limite=Number(statusPlano.limite_dependentes||0),ativos=Number(statusPlano.dependentes_ativos||0);
      el.innerHTML=`<b>Plano ${String(statusPlano.plano_codigo||'BASICO')}</b> · ${ativos} de ${limite} dependente(s) utilizado(s).`;
    }
  }
  window.carregarStatusPlanoV55=carregarStatusPlano;

  const original=window.criarAcessoOperacional;
  if(typeof original==='function'){
    window.criarAcessoOperacional=async function(){
      const st=await carregarStatusPlano();
      if(st){
        const teste=!!st.modo_teste||String(st.plano_codigo||'').toUpperCase()==='TESTE'||st.limite_dependentes==null;
        if(!teste&&!st.pode_adicionar){
          const plano=String(st.plano_codigo||'BASICO');
          const limite=Number(st.limite_dependentes||0);
          alert(`Seu plano ${plano} permite ${limite} dependente(s). Para criar outro acesso, será necessário fazer upgrade do plano ou contratar acesso adicional.`);
          return;
        }
      }
      const r=await original.apply(this,arguments);
      setTimeout(carregarStatusPlano,300);
      return r;
    };
  }
  function instalar(){setTimeout(carregarStatusPlano,700)}
  if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',()=>setTimeout(instalar,2500));else setTimeout(instalar,2500);
})();
</script>
'''

html=html.replace(marker,block+'\n'+marker,1)
idx.write_text(html,encoding='utf-8')

swtxt=sw.read_text(encoding='utf-8')
swtxt,n=re.subn(r"const CACHE_VERSION = '[^']+';","const CACHE_VERSION = 'simpla-shell-v55-planos-dependentes';",swtxt,count=1)
if n!=1:
    raise SystemExit('cache version nao encontrada')
sw.write_text(swtxt,encoding='utf-8')
