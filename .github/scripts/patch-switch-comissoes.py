from pathlib import Path
p=Path('index.html')
s=p.read_text(encoding='utf-8')
marker='simpla-switch-comissoes-contrast-v1'
if marker not in s:
    css='''\n<style id="simpla-switch-comissoes-contrast-v1">\n#configuracoes .cfg-switch-line{justify-content:flex-start!important;gap:14px!important;}\n#configuracoes .cfg-switch{width:50px!important;height:28px!important;flex:0 0 50px!important;}\n#configuracoes .cfg-switch-track{width:50px!important;height:28px!important;background:#8f9eac!important;border:1px solid #758594!important;box-shadow:inset 0 0 0 1px rgba(255,255,255,.16)!important;}\n#configuracoes .cfg-switch-track:after{width:22px!important;height:22px!important;left:2px!important;top:2px!important;box-shadow:0 1px 4px rgba(0,0,0,.30)!important;}\n#configuracoes .cfg-switch input:checked + .cfg-switch-track{background:#2f5f88!important;border-color:#244b6d!important;}\n#configuracoes .cfg-switch input:checked + .cfg-switch-track:after{transform:translateX(22px)!important;}\n#box-cfg-comissoes .cfg-switch-line{max-width:420px!important;align-items:center!important;}\n#box-cfg-comissoes .cfg-switch-state{color:#56697b!important;font-weight:600!important;}\n</style>\n'''
    s=s.replace('</head>',css+'\n</head>',1)
    p.write_text(s,encoding='utf-8')
    print('contraste dos interruptores atualizado')
else:
    print('patch ja aplicado')
