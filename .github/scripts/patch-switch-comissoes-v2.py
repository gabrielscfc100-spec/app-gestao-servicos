from pathlib import Path
p=Path('index.html')
s=p.read_text(encoding='utf-8')
marker='</head>'
css='''\n<style id="simpla-switch-comissoes-native-v2">\n/* Corrige especificamente o interruptor Utilizar comissões */\n#box-cfg-comissoes .cfg-switch{\n  width:50px!important;\n  height:28px!important;\n  flex:0 0 50px!important;\n  position:relative!important;\n}\n#box-cfg-comissoes .cfg-switch .cfg-switch-track{display:none!important;}\n#box-cfg-comissoes .cfg-switch input.cfg-switch-input{\n  opacity:1!important;\n  pointer-events:auto!important;\n  position:relative!important;\n  inset:auto!important;\n  display:block!important;\n  width:50px!important;\n  min-width:50px!important;\n  height:28px!important;\n  margin:0!important;\n  padding:0!important;\n  appearance:none!important;\n  -webkit-appearance:none!important;\n  border:1px solid #66788a!important;\n  border-radius:999px!important;\n  background:#7f90a1!important;\n  box-shadow:inset 0 0 0 1px rgba(255,255,255,.12)!important;\n  cursor:pointer!important;\n  transition:.18s!important;\n}\n#box-cfg-comissoes .cfg-switch input.cfg-switch-input:before{\n  content:''!important;\n  position:absolute!important;\n  width:22px!important;\n  height:22px!important;\n  left:2px!important;\n  top:2px!important;\n  border-radius:50%!important;\n  background:#fff!important;\n  box-shadow:0 1px 4px rgba(0,0,0,.34)!important;\n  transition:.18s!important;\n}\n#box-cfg-comissoes .cfg-switch input.cfg-switch-input:checked{\n  background:#2f5f88!important;\n  border-color:#244b6d!important;\n}\n#box-cfg-comissoes .cfg-switch input.cfg-switch-input:checked:before{transform:translateX(22px)!important;}\n#box-cfg-comissoes .cfg-switch-line{gap:12px!important;max-width:420px!important;}\n</style>\n'''
if 'id="simpla-switch-comissoes-native-v2"' not in s:
    if marker not in s: raise SystemExit('head nao localizado')
    s=s.replace(marker,css+marker,1)
p.write_text(s,encoding='utf-8')
print('ok')
