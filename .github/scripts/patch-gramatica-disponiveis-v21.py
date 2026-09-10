from pathlib import Path

p = Path('index.html')
s = p.read_text(encoding='utf-8')
marker = 'simpla-gramatica-disponiveis-v21'
if marker not in s:
    block = r'''
<script id="simpla-gramatica-disponiveis-v21">
(function(){
  function corrigirContagemDisponiveis(root=document){
    const todos = root.querySelectorAll ? root.querySelectorAll('*') : [];
    todos.forEach(el => {
      if(el.children.length) return;
      const txt = (el.textContent || '').trim();
      if(/^1\s+DISPONÍVEIS$/i.test(txt)) el.textContent = txt.replace(/DISPONÍVEIS/i, 'DISPONÍVEL');
    });
  }
  corrigirContagemDisponiveis();
  const obs = new MutationObserver(() => corrigirContagemDisponiveis());
  obs.observe(document.body,{childList:true,subtree:true,characterData:true});
})();
</script>
'''
    s = s.replace('</body>', block + '\n</body>')
    p.write_text(s, encoding='utf-8')

sw = Path('service-worker.js')
t = sw.read_text(encoding='utf-8')
import re
t = re.sub(r"const CACHE_VERSION = 'simpla-shell-v[^']+';", "const CACHE_VERSION = 'simpla-shell-v21-gramatica-contagem';", t, count=1)
sw.write_text(t, encoding='utf-8')
