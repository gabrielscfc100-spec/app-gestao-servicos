from pathlib import Path
p=Path('index.html')
s=p.read_text(encoding='utf-8')
marker='simpla-mobile-config-structural-v3'
if marker in s:
    raise SystemExit('patch já aplicado')
block=r'''
<style id="simpla-mobile-config-structural-v3">
@media (max-width:768px){
  #configuracoes label.simpla-mobile-switch-row{
    display:grid!important;
    grid-template-columns:42px minmax(0,1fr)!important;
    column-gap:14px!important;
    align-items:center!important;
    width:100%!important;
    min-width:0!important;
    font-size:12px!important;
    line-height:1.3!important;
    white-space:normal!important;
    overflow-wrap:anywhere!important;
  }
  #configuracoes label.simpla-mobile-switch-row > input[type="checkbox"]{
    grid-column:1!important;
    width:42px!important;
    min-width:42px!important;
    max-width:42px!important;
    height:24px!important;
    margin:0!important;
    position:relative!important;
    left:auto!important;
    right:auto!important;
    top:auto!important;
    transform:none!important;
    justify-self:start!important;
  }
  #configuracoes label.simpla-mobile-switch-row > span,
  #configuracoes label.simpla-mobile-switch-row > strong,
  #configuracoes label.simpla-mobile-switch-row > b{
    grid-column:2!important;
    min-width:0!important;
    margin:0!important;
    font-size:12px!important;
    line-height:1.3!important;
    overflow-wrap:anywhere!important;
  }
  #configuracoes .profissional-servico-item{
    display:grid!important;
    grid-template-columns:42px minmax(0,1fr) 82px!important;
    column-gap:14px!important;
    row-gap:6px!important;
    align-items:center!important;
    padding:12px!important;
    min-width:0!important;
  }
  #configuracoes .profissional-servico-item > input[type="checkbox"]{
    grid-column:1!important;
    grid-row:1!important;
    width:42px!important;
    min-width:42px!important;
    max-width:42px!important;
    margin:0!important;
    position:relative!important;
    left:auto!important;
    top:auto!important;
    transform:none!important;
    justify-self:start!important;
  }
  #configuracoes .profissional-servico-item > span{
    grid-column:2!important;
    grid-row:1!important;
    min-width:0!important;
    margin:0!important;
    padding:0!important;
    font-size:11.5px!important;
    line-height:1.25!important;
    overflow-wrap:anywhere!important;
  }
  #configuracoes .profissional-servico-item > span b,
  #configuracoes .profissional-servico-item > span strong{
    display:block!important;
    font-size:12px!important;
    line-height:1.2!important;
    margin:0 0 2px!important;
  }
  #configuracoes .profissional-servico-item > span small{
    display:block!important;
    font-size:10.5px!important;
    line-height:1.2!important;
  }
  #configuracoes .profissional-servico-item > input[type="number"]{
    grid-column:3!important;
    grid-row:1!important;
    width:82px!important;
    min-width:82px!important;
    max-width:82px!important;
    padding:8px 6px!important;
    font-size:12px!important;
    text-align:center!important;
    margin:0!important;
    justify-self:end!important;
  }
  #configuracoes .section-box-cfg h4{font-size:13px!important;line-height:1.25!important}
  #configuracoes .section-box-cfg p{font-size:11.5px!important;line-height:1.35!important}
}
@media (max-width:420px){
  #configuracoes label.simpla-mobile-switch-row{
    grid-template-columns:40px minmax(0,1fr)!important;
    column-gap:12px!important;
    font-size:11.5px!important;
  }
  #configuracoes label.simpla-mobile-switch-row > input[type="checkbox"]{
    width:40px!important;min-width:40px!important;max-width:40px!important;
  }
  #configuracoes .profissional-servico-item{
    grid-template-columns:40px minmax(0,1fr) 76px!important;
    column-gap:12px!important;
    padding:10px!important;
  }
  #configuracoes .profissional-servico-item > input[type="checkbox"]{
    width:40px!important;min-width:40px!important;max-width:40px!important;
  }
  #configuracoes .profissional-servico-item > input[type="number"]{
    width:76px!important;min-width:76px!important;max-width:76px!important;font-size:11.5px!important;
  }
}
</style>
<script id="simpla-mobile-config-structural-v3-script">
(function(){
  function aplicarEstruturaMobileConfiguracoes(){
    const raiz=document.getElementById('configuracoes');
    if(!raiz) return;
    raiz.querySelectorAll('label').forEach(label=>{
      const cb=label.querySelector('input[type="checkbox"]');
      if(!cb) return;
      if(label.classList.contains('cfg-switch')) return;
      if(label.querySelector('.cfg-switch-track')) return;
      label.classList.add('simpla-mobile-switch-row');
    });
  }
  document.addEventListener('DOMContentLoaded',()=>{
    aplicarEstruturaMobileConfiguracoes();
    const raiz=document.getElementById('configuracoes');
    if(raiz){
      const obs=new MutationObserver(()=>aplicarEstruturaMobileConfiguracoes());
      obs.observe(raiz,{childList:true,subtree:true});
    }
  });
  window.addEventListener('load',aplicarEstruturaMobileConfiguracoes);
})();
</script>
'''
needle='</head>'
if needle not in s: raise SystemExit('head não encontrado')
s=s.replace(needle,block+'\n'+needle,1)
p.write_text(s,encoding='utf-8')
