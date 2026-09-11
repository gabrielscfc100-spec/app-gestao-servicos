from pathlib import Path

idx = Path('index.html')
sw = Path('service-worker.js')
html = idx.read_text(encoding='utf-8')

old_obs = "new MutationObserver(liberarLogin).observe(auth,{attributes:true,attributeFilter:['class','style'],subtree:false});"
new_obs = "new MutationObserver(liberarLogin).observe(auth,{attributes:true,attributeFilter:['class'],subtree:false});"
if old_obs not in html:
    raise SystemExit('observer v42 nao encontrado')
html = html.replace(old_obs, new_obs, 1)

old_interval = "setInterval(liberarLogin,1000);"
new_interval = "setTimeout(liberarLogin,500);\n    setTimeout(liberarLogin,2000);"
if old_interval not in html:
    raise SystemExit('interval v42 nao encontrado')
html = html.replace(old_interval, new_interval, 1)

idx.write_text(html, encoding='utf-8')

swtxt = sw.read_text(encoding='utf-8')
swtxt = swtxt.replace("const CACHE_VERSION = 'simpla-shell-v42-login-interacao';", "const CACHE_VERSION = 'simpla-shell-v43-login-freeze';")
sw.write_text(swtxt, encoding='utf-8')
