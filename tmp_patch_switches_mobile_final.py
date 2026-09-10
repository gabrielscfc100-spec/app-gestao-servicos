from pathlib import Path

p = Path('index.html')
s = p.read_text(encoding='utf-8')
marker = '<!-- SIMPLA_SWITCHES_MOBILE_FINAL_V8 -->'
if marker in s:
    print('Patch já aplicado')
    raise SystemExit(0)

patch = r'''
<!-- SIMPLA_SWITCHES_MOBILE_FINAL_V8 -->
<style id="simpla-switches-mobile-final-v8">
@media (max-width:768px){
  /* Estrutura definitiva: uma coluna física para o switch e outra para o texto */
  #configuracoes label.simpla-switch-row-final{
    display:grid!important;
    grid-template-columns:52px minmax(0,1fr)!important;
    column-gap:14px!important;
    align-items:center!important;
    width:100%!important;
    min-width:0!important;
    margin:10px 0!important;
    padding:2px 0!important;
    position:relative!important;
    text-align:left!important;
  }
  #configuracoes label.simpla-switch-row-final > input[type="checkbox"]{
    grid-column:1!important;
    grid-row:1!important;
    width:44px!important;
    min-width:44px!important;
    max-width:44px!important;
    height:24px!important;
    margin:0!important;
    padding:0!important;
    position:static!important;
    left:auto!important;
    right:auto!important;
    top:auto!important;
    bottom:auto!important;
    transform:none!important;
    justify-self:start!important;
    align-self:center!important;
    flex:none!important;
  }
  #configuracoes label.simpla-switch-row-final > .simpla-switch-label-text-final{
    grid-column:2!important;
    grid-row:1!important;
    display:block!important;
    min-width:0!important;
    width:100%!important;
    margin:0!important;
    padding:0!important;
    font-size:12px!important;
    line-height:1.28!important;
    font-weight:500!important;
    white-space:normal!important;
    overflow-wrap:anywhere!important;
    word-break:normal!important;
    text-align:left!important;
  }

  /* Serviços/durações: layout próprio, sem receber o padrão genérico acima */
  #configuracoes .profissional-servico-item{
    display:grid!important;
    grid-template-columns:52px minmax(0,1fr) 72px!important;
    column-gap:12px!important;
    row-gap:5px!important;
    align-items:center!important;
    min-width:0!important;
    padding:11px!important;
  }
  #configuracoes .profissional-servico-item > input[type="checkbox"]{
    grid-column:1!important;
    grid-row:1!important;
    width:44px!important;
    min-width:44px!important;
    max-width:44px!important;
    height:24px!important;
    margin:0!important;
    position:static!important;
    transform:none!important;
  }
  #configuracoes .profissional-servico-item > span{
    grid-column:2!important;
    grid-row:1!important;
    min-width:0!important;
    margin:0!important;
    padding:0!important;
    font-size:11.5px!important;
    line-height:1.22!important;
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
    width:72px!important;
    min-width:72px!important;
    max-width:72px!important;
    padding:7px 6px!important;
    font-size:12px!important;
  }

  /* Tipografia secundária um pouco menor no mobile */
  #configuracoes .section-box-cfg h4{font-size:13px!important;line-height:1.25!important;}
  #configuracoes .section-box-cfg p{font-size:11.5px!important;line-height:1.35!important;}
}
@media (max-width:420px){
  #configuracoes label.simpla-switch-row-final{
    grid-template-columns:48px minmax(0,1fr)!important;
    column-gap:12px!important;
  }
  #configuracoes label.simpla-switch-row-final > input[type="checkbox"]{
    width:42px!important;min-width:42px!important;max-width:42px!important;
  }
  #configuracoes label.simpla-switch-row-final > .simpla-switch-label-text-final{
    font-size:11.5px!important;
  }
  #configuracoes .profissional-servico-item{
    grid-template-columns:48px minmax(0,1fr) 68px!important;
    column-gap:10px!important;
  }
  #configuracoes .profissional-servico-item > input[type="checkbox"]{
    width:42px!important;min-width:42px!important;max-width:42px!important;
  }
  #configuracoes .profissional-servico-item > input[type="number"]{
    width:68px!important;min-width:68px!important;max-width:68px!important;
  }
}
</style>
<script id="simpla-switches-mobile-final-v8-script">
(function(){
  function normalizarLabel(label){
    if(!label || label.dataset.simplaSwitchFinal === '1') return;
    if(label.classList.contains('cfg-switch')) return;
    if(label.classList.contains('profissional-servico-item')) return;
    if(label.querySelector('.cfg-switch-track')) return;

    const cb = Array.from(label.children).find(el => el.matches && el.matches('input[type="checkbox"]'));
    if(!cb) return;

    const span = document.createElement('span');
    span.className = 'simpla-switch-label-text-final';

    /* Move tudo que não é o checkbox para um bloco textual próprio. */
    const nos = Array.from(label.childNodes).filter(no => no !== cb);
    nos.forEach(no => span.appendChild(no));

    label.appendChild(span);
    label.classList.add('simpla-switch-row-final');
    label.classList.remove('simpla-mobile-switch-row');
    label.dataset.simplaSwitchFinal = '1';
  }

  function aplicar(){
    const raiz = document.getElementById('configuracoes');
    if(!raiz) return;
    raiz.querySelectorAll('label').forEach(normalizarLabel);
  }

  function iniciar(){
    aplicar();
    const raiz = document.getElementById('configuracoes');
    if(!raiz) return;
    const obs = new MutationObserver(() => aplicar());
    obs.observe(raiz, {childList:true, subtree:true});
    window.simplaReaplicarSwitchesMobile = aplicar;
  }

  if(document.readyState === 'loading') document.addEventListener('DOMContentLoaded', iniciar);
  else iniciar();
})();
</script>
'''

# Insere imediatamente antes de </body>, garantindo prioridade sobre CSS anteriores.
idx = s.lower().rfind('</body>')
if idx == -1:
    raise SystemExit('ERRO: </body> não encontrado')
s = s[:idx] + patch + '\n' + s[idx:]
p.write_text(s, encoding='utf-8')
print('OK: patch estrutural final v8 aplicado')
