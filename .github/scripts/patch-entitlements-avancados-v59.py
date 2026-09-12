from pathlib import Path
import re

idx=Path('index.html')
sw=Path('service-worker.js')
html=idx.read_text(encoding='utf-8')

if 'simpla-entitlements-avancados-v59' in html:
    raise SystemExit('v59 ja aplicada')

marker='</body>'
if marker not in html:
    raise SystemExit('body nao encontrado')

block=r'''
<style id="simpla-entitlements-avancados-v59-css">
  .simpla-entitlement-lock-v59{position:relative!important;overflow:hidden}
  .simpla-entitlement-lock-v59>.simpla-entitlement-overlay-v59{position:absolute;inset:0;z-index:52;display:flex;align-items:center;justify-content:center;padding:16px;background:rgba(248,250,252,.95);backdrop-filter:blur(2px);text-align:center;text-transform:none}
  .simpla-entitlement-overlay-v59-card{max-width:390px;padding:17px;border:1px solid #dbe4ee;border-radius:12px;background:#fff;box-shadow:0 8px 26px rgba(15,23,42,.10)}
  .simpla-entitlement-overlay-v59-tag{display:inline-flex;padding:5px 8px;border-radius:999px;background:#ebf8ff;color:#2b6cb0;font-size:8px;font-weight:900;text-transform:uppercase;margin-bottom:8px}
  .simpla-entitlement-overlay-v59-card h4{margin:0 0 6px;font-size:14px;color:#1a1c23}.simpla-entitlement-overlay-v59-card p{margin:0 0 11px;font-size:10px;line-height:1.5;color:#718096;text-transform:none}
  .simpla-entitlement-overlay-v59-card button{border:0;border-radius:7px;padding:8px 11px;background:#1a1c23;color:#fff;font-size:9px;font-weight:900;cursor:pointer}
  .simpla-entitlement-overlay-v59-card button:hover{background:var(--cor-accent);color:#1a1c23}
  #box-cfg-usuarios.simpla-entitlement-lock-v59{min-height:180px}
  #dash-rel-v50.simpla-entitlement-lock-v59,#dash-prof-v48.simpla-entitlement-lock-v59,#dash-serv-v49.simpla-entitlement-lock-v59{min-height:170px}
</style>
<script id="simpla-entitlements-avancados-v59">
(function(){
  const ITENS=[
    {id:'dash-sec-fluxo',recurso:'dashboard_avancado',plano:'Plus',titulo:'Análise financeira avançada',texto:'Acompanhe a evolução de faturamento e despesas com uma visão analítica do período.'},
    {id:'dash-sec-composicao',recurso:'dashboard_avancado',plano:'Plus',titulo:'Composição do faturamento',texto:'Entenda a participação dos serviços e produtos na receita do negócio.'},
    {id:'dash-sec-servicos',recurso:'ranking_servico_profissional',plano:'Plus',titulo:'Ranking de serviços',texto:'Compare os serviços com maior volume e participação no faturamento.'},
    {id:'dash-sec-comparativo',recurso:'comparativo_periodos',plano:'Plus',titulo:'Comparativo de períodos',texto:'Compare o desempenho atual com períodos anteriores e identifique variações.'},
    {id:'dash-sec-vip',recurso:'dashboard_avancado',plano:'Plus',titulo:'Clientes VIP',texto:'Identifique os clientes com maior relacionamento financeiro no período.'},
    {id:'dash-sec-insights',recurso:'dashboard_avancado',plano:'Plus',titulo:'Insights do negócio',texto:'Receba sinais automáticos baseados nos dados administrativos disponíveis.'},
    {id:'dash-prof-v48',recurso:'ranking_servico_profissional',plano:'Plus',titulo:'Desempenho por profissional',texto:'Compare atendimentos, faturamento, ticket médio e no-show por profissional.'},
    {id:'dash-serv-v49',recurso:'ranking_servico_profissional',plano:'Plus',titulo:'Desempenho por serviço',texto:'Veja quantidade, faturamento, ticket médio e participação por serviço.'},
    {id:'dash-rel-v50',recurso:'dashboard_avancado',plano:'Plus',titulo:'Central de Relatórios Gerenciais',texto:'Consolide indicadores e gere relatórios gerenciais em uma única área.'},
    {id:'box-cfg-usuarios',recurso:'perfis_permissoes_avancadas',plano:'Plus',titulo:'Usuários e permissões avançadas',texto:'Crie acessos adicionais e organize os perfis e permissões da equipe.'}
  ];
  let aplicando=false;

  function teste(){try{return !!empresaAtual?.modo_teste||String(empresaAtual?.plano_codigo||'').toUpperCase()==='TESTE'}catch(_){return false}}
  function abrirPlano(){
    try{if(typeof mudarTela==='function')mudarTela('configuracoes')}catch(_){ }
    setTimeout(()=>{const el=document.getElementById('simpla-meu-plano-v57');if(el)el.scrollIntoView({behavior:'smooth',block:'start'})},250);
  }
  window.abrirMeuPlanoV59=abrirPlano;

  function unlock(el){el.classList.remove('simpla-entitlement-lock-v59');el.querySelector(':scope > .simpla-entitlement-overlay-v59')?.remove()}
  function lock(el,cfg){
    if(el.querySelector(':scope > .simpla-entitlement-overlay-v59'))return;
    el.classList.add('simpla-entitlement-lock-v59');
    const ov=document.createElement('div');ov.className='simpla-entitlement-overlay-v59';
    ov.innerHTML=`<div class="simpla-entitlement-overlay-v59-card"><span class="simpla-entitlement-overlay-v59-tag">Disponível no ${cfg.plano}</span><h4>${cfg.titulo}</h4><p>${cfg.texto}</p><button type="button" onclick="abrirMeuPlanoV59()">Ver planos</button></div>`;
    el.appendChild(ov);
  }

  async function aplicar(){
    if(aplicando)return;aplicando=true;
    try{
      if(teste()){ITENS.forEach(c=>{const el=document.getElementById(c.id);if(el)unlock(el)});return}
      if(typeof empresaPodeUsarRecurso!=='function')return;
      await Promise.all(ITENS.map(async c=>{const el=document.getElementById(c.id);if(!el)return;const ok=await empresaPodeUsarRecurso(c.recurso);ok?unlock(el):lock(el,c)}));
    }catch(err){console.warn('Entitlements avançados v59:',err)}finally{aplicando=false}
  }
  window.aplicarEntitlementsAvancadosV59=aplicar;

  function protegerExportacao(nome,recurso){
    const original=window[nome];if(typeof original!=='function'||original.__simplaV59)return;
    const wrapper=async function(){
      if(teste())return original.apply(this,arguments);
      if(typeof empresaPodeUsarRecurso==='function'){
        const ok=await empresaPodeUsarRecurso(recurso);
        if(!ok){abrirPlano();alert('A exportação gerencial completa está disponível a partir do plano Plus.');return}
      }
      return original.apply(this,arguments);
    };
    wrapper.__simplaV59=true;window[nome]=wrapper;
  }
  function protegerFuncoes(){
    protegerExportacao('exportarRelatorioGerencialExcelV50','exportacao_completa');
    protegerExportacao('exportarRelatorioGerencialPDFV50','exportacao_completa');
  }

  const observer=new MutationObserver(()=>{clearTimeout(window.__simplaV59T);window.__simplaV59T=setTimeout(()=>{protegerFuncoes();aplicar()},170)});
  function instalar(){observer.observe(document.body,{childList:true,subtree:true});protegerFuncoes();setTimeout(aplicar,700);setTimeout(()=>{protegerFuncoes();aplicar()},2300);setTimeout(()=>{protegerFuncoes();aplicar()},4500)}
  if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',instalar);else instalar();
})();
</script>
'''

html=html.replace(marker,block+'\n'+marker,1)
idx.write_text(html,encoding='utf-8')

swtxt=sw.read_text(encoding='utf-8')
swtxt,n=re.subn(r"const CACHE_VERSION = '[^']+';","const CACHE_VERSION = 'simpla-shell-v59-entitlements-avancados';",swtxt,count=1)
if n!=1:
    raise SystemExit('cache version nao encontrada')
sw.write_text(swtxt,encoding='utf-8')
