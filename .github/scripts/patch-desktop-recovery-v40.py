from pathlib import Path
import re

p=Path('index.html')
s=p.read_text(encoding='utf-8')
marker='<!-- SIMPLA desktop recovery v40 -->'

# Corrige especificamente o bloco antigo de switches de configuração que foi
# salvo com sequências literais de quebra de linha (\\n / \\\\n) dentro do JS.
# O navegador interpreta isso como token inválido logo no início do script.
script_pat=re.compile(r'(<script(?:\s[^>]*)?>)(.*?)(</script>)',re.S|re.I)
partes=[]
pos=0
corrigidos=0
for m in script_pat.finditer(s):
    corpo=m.group(2)
    novo=corpo
    if 'simpla-mobile-switch-row' in corpo:
        novo=re.sub(r'\\+n', '\n', novo)
        novo=re.sub(r'\\+t', '\t', novo)
        if novo!=corpo:
            corrigidos+=1
    partes.append(s[pos:m.start(2)])
    partes.append(novo)
    pos=m.end(2)
partes.append(s[pos:])
s=''.join(partes)

if marker not in s:
    s=s.replace('</body>', marker+'\n</body>',1)

p.write_text(s,encoding='utf-8')

sw=Path('service-worker.js')
t=sw.read_text(encoding='utf-8')
t=re.sub(r"const CACHE_VERSION = ['\"][^'\"]+['\"]", "const CACHE_VERSION = 'simpla-shell-v40-desktop-recovery'", t, count=1)
sw.write_text(t,encoding='utf-8')
print('scripts corrigidos:',corrigidos)
print('v40 desktop recovery aplicada')
