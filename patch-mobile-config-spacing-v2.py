from pathlib import Path

path = Path('index.html')
text = path.read_text(encoding='utf-8')
marker = 'simpla-mobile-config-spacing-v2'

if marker in text:
    raise SystemExit('Patch ja aplicado')

css = r'''
<style id="simpla-mobile-config-spacing-v2">
@media (max-width:768px){
  /* Opcoes com interruptor dentro das Configuracoes */
  #configuracoes .section-box-cfg label:has(> input[type="checkbox"]){
    display:flex!important;
    align-items:center!important;
    gap:12px!important;
    min-width:0!important;
    width:100%!important;
    font-size:12px!important;
    line-height:1.28!important;
    white-space:normal!important;
    overflow-wrap:anywhere!important;
  }

  #configuracoes .section-box-cfg label:has(> input[type="checkbox"]) > input[type="checkbox"]{
    flex:0 0 42px!important;
    width:42px!important;
    min-width:42px!important;
    max-width:42px!important;
    margin:0!important;
  }

  #configuracoes .section-box-cfg > div[style*="grid-template-columns"]{
    grid-template-columns:1fr!important;
    gap:11px!important;
  }

  #configuracoes .section-box-cfg h4{
    font-size:13px!important;
    line-height:1.25!important;
  }

  /* Cards de servicos por profissional */
  #configuracoes .profissional-servico-item{
    grid-template-columns:48px minmax(0,1fr) 70px!important;
    gap:10px!important;
    padding:11px!important;
    align-items:center!important;
  }

  #configuracoes .profissional-servico-item > input[type="checkbox"]{
    width:42px!important;
    min-width:42px!important;
    max-width:42px!important;
    margin:0!important;
    justify-self:start!important;
  }

  #configuracoes .profissional-servico-item > span{
    min-width:0!important;
    font-size:11.5px!important;
    line-height:1.22!important;
    overflow-wrap:anywhere!important;
  }

  #configuracoes .profissional-servico-item > span b{
    font-size:12px!important;
    line-height:1.2!important;
  }

  #configuracoes .profissional-servico-item > span small{
    font-size:10.5px!important;
    line-height:1.2!important;
  }

  #configuracoes .profissional-servico-item > input[type="number"]{
    width:70px!important;
    min-width:0!important;
    padding:7px 6px!important;
    font-size:12px!important;
  }

  /* Melhor aproveitamento do espaco no mobile */
  #configuracoes .cfg-v2-group{
    padding:14px!important;
  }

  #configuracoes .cfg-v2-group > h2,
  #configuracoes .cfg-v2-group > h3{
    line-height:1.2!important;
  }

  #configuracoes .cfg-v2-group p{
    line-height:1.35!important;
  }
}

@media (max-width:420px){
  #configuracoes .section-box-cfg label:has(> input[type="checkbox"]){
    font-size:11.5px!important;
    gap:10px!important;
  }

  #configuracoes .profissional-servico-item{
    grid-template-columns:46px minmax(0,1fr) 64px!important;
    gap:8px!important;
    padding:10px!important;
  }

  #configuracoes .profissional-servico-item > input[type="number"]{
    width:64px!important;
    font-size:11.5px!important;
  }
}
</style>
'''

needle = '</head>'
idx = text.rfind(needle)
if idx < 0:
    raise SystemExit('</head> nao encontrado')

text = text[:idx] + css + '\n' + text[idx:]
path.write_text(text, encoding='utf-8')
print('Patch aplicado')
