from pathlib import Path
import re
p=Path('index.html')
s=p.read_text(encoding='utf-8')
if 'simpla-pix-empresa-bridge-v31b' in s:
    raise SystemExit('v31b ja aplicada')
block=r'''
<script id="simpla-pix-empresa-bridge-v31b">
(function(){
  function sincronizarEmpresaPix(){
    try{
      if(typeof empresaAtual !== 'undefined' && empresaAtual) window.empresaAtual = empresaAtual;
      if(typeof CloudDB !== 'undefined' && CloudDB) window.CloudDB = CloudDB;
    }catch(_){ }
  }
  sincronizarEmpresaPix();
  document.addEventListener('DOMContentLoaded', sincronizarEmpresaPix);
  document.addEventListener('click', function(e){
    if(e.target.closest('#pix-config-v27, [onclick*="salvarConfiguracaoPixV27"]')) sincronizarEmpresaPix();
  }, true);
  let tentativas=0;
  const timer=setInterval(function(){sincronizarEmpresaPix();if(++tentativas>=60)clearInterval(timer);},500);
  window.sincronizarEmpresaPixV31=sincronizarEmpresaPix;
})();
</script>
'''
s=s.replace('</body>',block+'\n</body>',1)
p.write_text(s,encoding='utf-8')
sw=Path('service-worker.js')
t=sw.read_text(encoding='utf-8')
t,n=re.subn(r"const CACHE_VERSION = '[^']+';", "const CACHE_VERSION = 'simpla-shell-v31b-pix-empresa';", t, count=1)
assert n==1
sw.write_text(t,encoding='utf-8')
