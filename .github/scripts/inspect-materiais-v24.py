from pathlib import Path
import re
s=Path('index.html').read_text(encoding='utf-8')
for m in re.finditer(r'materiais?', s, flags=re.I):
    a=max(0,m.start()-2500); b=min(len(s),m.end()+4500)
    print('\n--- OCCURRENCE ---\n')
    print(s[a:b])
