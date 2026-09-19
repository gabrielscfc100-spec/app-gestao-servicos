from pathlib import Path
import re

idx=Path('index.html')
sw=Path('service-worker.js')
html=idx.read_text(encoding='utf-8')

# Remove todos os blocos visuais/JS do WhatsApp v62-v74.
patterns=[
    r'\n?<style id="simpla-whatsapp-[^"]+-css">.*?</style>\s*',
    r'\n?<script id="simpla-whatsapp-[^"]+">.*?</script>\s*'
]

total=0
for pat in patterns:
    html,n=re.subn(pat,'\n',html,flags=re.S)
    total+=n

if total < 20:
    raise SystemExit(f'Esperava remover pelo menos 20 blocos, removidos={total}')

# Remove possíveis resíduos de containers antigos já estáticos, se houver.
html=re.sub(r'\n{3,}','\n\n',html)

idx.write_text(html,encoding='utf-8')

swtxt=sw.read_text(encoding='utf-8')
swtxt,n=re.subn(
    r"const CACHE_VERSION = '[^']+';",
    "const CACHE_VERSION = 'simpla-shell-v76-emergency-stability';",
    swtxt,
    count=1
)
if n!=1:
    raise SystemExit('cache version nao encontrada')
sw.write_text(swtxt,encoding='utf-8')
