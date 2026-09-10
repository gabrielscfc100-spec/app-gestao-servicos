from pathlib import Path
p = Path('index.html')
s = p.read_text(encoding='utf-8')
marker = '<style id="simpla-mobile-menu-icon-v1">'
if marker not in s:
    css = '''\n<style id="simpla-mobile-menu-icon-v1">\n@media (max-width:768px){\n  .mobile-menu-toggle{\n    position:relative!important;\n    font-size:0!important;\n    color:transparent!important;\n    -webkit-appearance:none!important;\n    appearance:none!important;\n  }\n  .mobile-menu-toggle::before{\n    content:""!important;\n    position:absolute!important;\n    left:10px!important;\n    right:10px!important;\n    top:10px!important;\n    height:3px!important;\n    border-radius:999px!important;\n    background:#fff!important;\n    box-shadow:0 9px 0 #fff,0 18px 0 #fff!important;\n    opacity:1!important;\n    pointer-events:none!important;\n  }\n}\n</style>\n'''
    if '</head>' not in s:
        raise SystemExit('missing </head>')
    s = s.replace('</head>', css + '</head>', 1)
    p.write_text(s, encoding='utf-8')
print('ok')
