from pathlib import Path
import re

idx=Path('index.html')
sw=Path('service-worker.js')
html=idx.read_text(encoding='utf-8')

if 'simpla-entitlements-v56' in html:
    raise SystemExit('v56 ja aplicada')

marker='</body>'
if marker not in html:
    raise SystemExit('body nao encontrado')

block=r'''
<script id="simpla-entitlements-v56">
(function(){
  const cache=new Map();
  const RECURSOS_NUCLEO=new Set(['agenda','agenda_publica','clientes','profissionais','servicos','financeiro','dashboard','exportacoes','portal_cliente']);

  async function consultar(recurso, opts={}){
    const chave=String(recurso||'').trim();
    if(!chave) return false;

    // A conta de testes nunca deve sofrer bloqueios de plano.
    try{
      if(typeof empresaAtual!=='undefined' && empresaAtual && (empresaAtual.modo_teste===true || String(empresaAtual.plano_codigo||'').toUpperCase()==='TESTE')) return true;
    }catch(_){ }

    // Enquanto a matriz comercial detalhada nao for aprovada, o nucleo de gestao fica liberado para todos.
    if(RECURSOS_NUCLEO.has(chave)) return true;

    let empresaId=null;
    try{ empresaId=(typeof empresaAtual!=='undefined'&&empresaAtual?.id)?empresaAtual.id:null; }catch(_){ }
    if(!empresaId) return false;

    const ck=`${empresaId}:${chave}`;
    if(!opts.force && cache.has(ck)) return cache.get(ck);

    try{
      if(typeof CloudDB==='undefined' || !CloudDB) return false;
      const {data,error}=await CloudDB.rpc('empresa_pode_usar_recurso',{p_empresa_id:empresaId,p_recurso:chave});
      if(error){ console.warn('Entitlement SimplA:',chave,error); return false; }
      const permitido=data===true;
      cache.set(ck,permitido);
      return permitido;
    }catch(err){
      console.warn('Falha ao consultar entitlement:',chave,err);
      return false;
    }
  }

  window.empresaPodeUsarRecurso=consultar;
  window.limparCacheEntitlementsSimplA=function(){cache.clear();};

  window.exigirRecursoSimplA=async function(recurso,mensagem){
    const ok=await consultar(recurso);
    if(ok) return true;
    alert(mensagem || 'Este recurso não está incluído no plano atual.');
    return false;
  };

  // Exposição somente informativa para telas futuras de assinatura/planos.
  window.RECURSOS_SIMPLA={
    AGENDA:'agenda',AGENDA_PUBLICA:'agenda_publica',CLIENTES:'clientes',PROFISSIONAIS:'profissionais',SERVICOS:'servicos',
    FINANCEIRO:'financeiro',DASHBOARD:'dashboard',EXPORTACOES:'exportacoes',PORTAL_CLIENTE:'portal_cliente',
    WHATSAPP_OPERACIONAL:'whatsapp_operacional',WHATSAPP_CAMPANHAS:'whatsapp_campanhas',SIMPLA_IA:'simpla_ia'
  };
})();
</script>
'''
html=html.replace(marker,block+'\n'+marker,1)
idx.write_text(html,encoding='utf-8')

swtxt=sw.read_text(encoding='utf-8')
swtxt,n=re.subn(r"const CACHE_VERSION = '[^']+';","const CACHE_VERSION = 'simpla-shell-v56-entitlements';",swtxt,count=1)
if n!=1:
    raise SystemExit('cache version nao encontrada')
sw.write_text(swtxt,encoding='utf-8')
