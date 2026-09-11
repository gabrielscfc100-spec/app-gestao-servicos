from pathlib import Path
import re
p=Path('index.html')
s=p.read_text(encoding='utf-8')
marker='<!-- SIMPLA boot recovery v41 -->'
if marker not in s:
    bloco=r'''
<!-- SIMPLA boot recovery v41 -->
<style id="simpla-boot-recovery-v41-style">
#simpla-boot-recovery-v41{display:none;position:fixed;inset:0;z-index:20000;background:#f4f5f7;align-items:center;justify-content:center;padding:24px;text-transform:none}
#simpla-boot-recovery-v41 .box{width:min(420px,100%);background:#fff;border:1px solid #e2e8f0;border-radius:12px;padding:22px;box-shadow:0 16px 45px rgba(26,28,35,.16);text-align:center}
#simpla-boot-recovery-v41 strong{display:block;font-size:18px;color:#23364d;text-transform:none;margin-bottom:7px}
#simpla-boot-recovery-v41 span{display:block;font-size:12px;line-height:1.5;color:#718096;text-transform:none}
</style>
<div id="simpla-boot-recovery-v41"><div class="box"><strong>Restaurando o SimplA</strong><span>A sessão está sendo recuperada. Se necessário, a tela de acesso será exibida automaticamente.</span></div></div>
<script id="simpla-boot-recovery-v41-script">
(function(){
  let tentativas=0;
  function visivel(el){
    if(!el) return false;
    const st=getComputedStyle(el);
    return st.display!=='none' && st.visibility!=='hidden' && st.opacity!=='0';
  }
  function recuperar(){
    const body=document.body;
    const auth=document.getElementById('cloud-auth-overlay');
    const empresa=document.getElementById('cloud-empresa-overlay');
    const sidebar=document.querySelector('.sidebar');
    const main=document.querySelector('.main-content');
    const rescue=document.getElementById('simpla-boot-recovery-v41');
    if(!body||!rescue) return;

    const appOk=visivel(sidebar)||visivel(main);
    const authOk=visivel(auth)||visivel(empresa);
    if(appOk||authOk){ rescue.style.display='none'; return; }

    rescue.style.display='flex';
    body.style.setProperty('background','#f4f5f7','important');
    tentativas++;

    if(tentativas>=2){
      try{
        body.classList.add('auth-pending');
        if(auth){ auth.classList.remove('hidden'); auth.style.removeProperty('display'); }
        if(empresa) empresa.classList.add('hidden');
        if(typeof exibirMensagemCloud==='function'){
          exibirMensagemCloud('cloud-auth-message','A sessão anterior não concluiu a abertura. Estamos recuperando o acesso.','info');
        }
        rescue.style.display='none';
      }catch(e){console.error('Falha no recovery visual do boot',e)}
    }

    if(tentativas===3 && typeof inicializarAutenticacaoCloud==='function'){
      try{ inicializarAutenticacaoCloud(); }catch(e){ console.error('Falha ao reiniciar autenticação',e); }
    }
  }
  const iniciar=()=>{
    setTimeout(recuperar,1800);
    setTimeout(recuperar,3800);
    setTimeout(recuperar,6500);
  };
  if(document.readyState==='loading') document.addEventListener('DOMContentLoaded',iniciar,{once:true});
  else iniciar();
  window.addEventListener('pageshow',()=>setTimeout(recuperar,1200));
})();
</script>
'''
    s=s.replace('</body>',bloco+'\n</body>',1)
p.write_text(s,encoding='utf-8')
sw=Path('service-worker.js')
t=sw.read_text(encoding='utf-8')
t=re.sub(r"const CACHE_VERSION = ['\"][^'\"]+['\"]", "const CACHE_VERSION = 'simpla-shell-v41-boot-recovery'", t, count=1)
sw.write_text(t,encoding='utf-8')
print('v41 aplicada')
