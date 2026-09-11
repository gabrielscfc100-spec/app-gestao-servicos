from pathlib import Path

idx = Path('index.html')
sw = Path('service-worker.js')
html = idx.read_text(encoding='utf-8')

old = """    criar();
    const obs=new MutationObserver(sincronizar);
    obs.observe(document.body,{subtree:true,attributes:true,attributeFilter:['class','style','hidden']});
    window.addEventListener('resize',sincronizar,{passive:true});
    document.addEventListener('visibilitychange',()=>{if(!document.hidden) sincronizar();});
    setInterval(sincronizar,2000);
"""

new = """    criar();
    sincronizar();
    window.addEventListener('resize',sincronizar,{passive:true});
    document.addEventListener('visibilitychange',()=>{if(!document.hidden) sincronizar();});
    document.addEventListener('click',()=>setTimeout(sincronizar,0),true);
"""

count = html.count(old)
if count < 1:
    raise SystemExit('bloco global de observacao nao encontrado')
html = html.replace(old, new)
idx.write_text(html, encoding='utf-8')

swtxt = sw.read_text(encoding='utf-8')
old_cache = "const CACHE_VERSION = 'simpla-shell-v43-login-freeze';"
new_cache = "const CACHE_VERSION = 'simpla-shell-v44-global-observer-freeze';"
if old_cache not in swtxt:
    raise SystemExit('cache v43 nao encontrado')
swtxt = swtxt.replace(old_cache, new_cache, 1)
sw.write_text(swtxt, encoding='utf-8')

print(f'blocos substituidos: {count}')
