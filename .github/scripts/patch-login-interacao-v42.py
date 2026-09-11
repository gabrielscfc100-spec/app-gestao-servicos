from pathlib import Path
import re
p=Path('index.html')
s=p.read_text(encoding='utf-8')
# A camada de recovery nunca deve capturar mouse/teclado.
s=s.replace('#simpla-boot-recovery-v41{display:none;position:fixed;inset:0;z-index:20000;background:#f4f5f7;align-items:center;justify-content:center;padding:24px;text-transform:none}',
            '#simpla-boot-recovery-v41{display:none;position:fixed;inset:0;z-index:19000;background:#f4f5f7;align-items:center;justify-content:center;padding:24px;text-transform:none;pointer-events:none!important}')
marker='<!-- SIMPLA login interaction recovery v42 -->'
if marker not in s:
    bloco=r'''
<!-- SIMPLA login interaction recovery v42 -->
<style id="simpla-login-interaction-v42-style">
.cloud-auth-overlay:not(.hidden){z-index:30000!important;pointer-events:auto!important;}
.cloud-auth-overlay:not(.hidden) .cloud-auth-card,
.cloud-auth-overlay:not(.hidden) .cloud-auth-body,
.cloud-auth-overlay:not(.hidden) .cloud-auth-panel.active,
.cloud-auth-overlay:not(.hidden) input,
.cloud-auth-overlay:not(.hidden) select,
.cloud-auth-overlay:not(.hidden) button{pointer-events:auto!important;}
.cloud-auth-overlay.hidden{pointer-events:none!important;}
</style>
<script id="simpla-login-interaction-v42-script">
(function(){
  function liberarLogin(){
    const auth=document.getElementById('cloud-auth-overlay');
    if(!auth || auth.classList.contains('hidden')) return;
    const rescue=document.getElementById('simpla-boot-recovery-v41');
    if(rescue) rescue.style.display='none';
    auth.style.setProperty('z-index','30000','important');
    auth.style.setProperty('pointer-events','auto','important');
    auth.querySelectorAll('input,select').forEach(el=>{
      el.style.setProperty('pointer-events','auto','important');
      if(el.hasAttribute('readonly') && !el.dataset.simplaReadonlyOriginal){ el.removeAttribute('readonly'); }
      if(el.disabled && !el.dataset.simplaDisabledOriginal){ el.disabled=false; }
    });
  }
  const iniciar=()=>{
    liberarLogin();
    const auth=document.getElementById('cloud-auth-overlay');
    if(auth){
      new MutationObserver(liberarLogin).observe(auth,{attributes:true,attributeFilter:['class','style'],subtree:false});
    }
    setInterval(liberarLogin,1000);
  };
  if(document.readyState==='loading') document.addEventListener('DOMContentLoaded',iniciar,{once:true});
  else iniciar();
  window.addEventListener('pageshow',()=>setTimeout(liberarLogin,100));
})();
</script>
'''
    s=s.replace('</body>',bloco+'\n</body>',1)
p.write_text(s,encoding='utf-8')
sw=Path('service-worker.js')
t=sw.read_text(encoding='utf-8')
t=re.sub(r"const CACHE_VERSION = ['\"][^'\"]+['\"]", "const CACHE_VERSION = 'simpla-shell-v42-login-interacao'", t, count=1)
sw.write_text(t,encoding='utf-8')
print('v42 aplicada')
