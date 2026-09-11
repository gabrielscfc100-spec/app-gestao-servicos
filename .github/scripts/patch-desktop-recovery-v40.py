from pathlib import Path
import re

p=Path('index.html')
s=p.read_text(encoding='utf-8')
marker='<!-- SIMPLA desktop recovery v40 -->'

# Corrige um bloco antigo de configuração que foi gravado com os caracteres
# literais "\\n" no início/fim das linhas, tornando aquele <script> inválido.
pat=re.compile(r'(<script[^>]*>)(.*?simpla-mobile-switch-row.*?)(</script>)',re.S|re.I)
m=pat.search(s)
if m:
    corpo=m.group(2)
    if '\\n' in corpo:
        corpo=corpo.replace('\\n','\n')
        s=s[:m.start(2)]+corpo+s[m.end(2):]

if marker not in s:
    s=s.replace('</body>', marker+'\n</body>',1)

p.write_text(s,encoding='utf-8')

sw=Path('service-worker.js')
t=sw.read_text(encoding='utf-8')
t=re.sub(r"const CACHE_VERSION = ['\"][^'\"]+['\"]", "const CACHE_VERSION = 'simpla-shell-v40-desktop-recovery'", t, count=1)
sw.write_text(t,encoding='utf-8')
print('v40 desktop recovery aplicada')
