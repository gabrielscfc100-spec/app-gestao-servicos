from pathlib import Path
import re

idx=Path('index.html')
sw=Path('service-worker.js')
html=idx.read_text(encoding='utf-8')

# 1) Remove completamente o hotfix v73 que causava loop de MutationObserver.
html, n73 = re.subn(
    r'\n?<style id="simpla-whatsapp-fix-multilembretes-v73-css">.*?</script>\s*',
    '\n',
    html,
    count=1,
    flags=re.S
)
if n73 != 1:
    raise SystemExit('bloco v73 nao encontrado')

# 2) Remove LEMBRETE do renderer legado v68. Lembretes ficam exclusivamente na v72.
old_tipo = "{tipo:'LEMBRETE',titulo:'Lembrete de agendamento',desc:'Preparado antes do horário marcado conforme a antecedência definida.',antecedencia:true},"
if old_tipo not in html:
    raise SystemExit('tipo lembrete v68 nao encontrado')
html = html.replace(old_tipo, '', 1)

# 3) Preserva a seção v72 quando v68 redesenha seus cartões.
old_render = """    grid.innerHTML=TIPOS.map(cfg=>{
      const r=map.get(cfg.tipo)||{};"""
new_render = """    const reminders=document.getElementById('simpla-wa-reminders-v72');
    if(reminders && reminders.parentElement===grid) reminders.remove();
    grid.innerHTML=TIPOS.map(cfg=>{
      const r=map.get(cfg.tipo)||{};"""
if old_render not in html:
    raise SystemExit('inicio render v68 nao encontrado')
html = html.replace(old_render, new_render, 1)

old_join = """    }).join('');
  }

  async function permitido(){"""
new_join = """    }).join('');
    if(reminders){
      grid.appendChild(reminders);
    }else if(typeof carregarLembretesWhatsAppV72==='function'){
      setTimeout(()=>{ try{ carregarLembretesWhatsAppV72(); }catch(_){} },0);
    }
  }

  async function permitido(){"""
if old_join not in html:
    raise SystemExit('fim render v68 nao encontrado')
html = html.replace(old_join, new_join, 1)

# 4) Remove observer global da categoria v65; mantém apenas tentativas curtas de montagem.
old_install = """  function instalar(){
    let tentativas=0;
    const timer=setInterval(()=>{
      tentativas++;
      const ok=montar();
      if(ok || tentativas>40) clearInterval(timer);
    },200);

    const raiz=document.getElementById('configuracoes');
    if(raiz){
      const obs=new MutationObserver(()=>requestAnimationFrame(montar));
      obs.observe(raiz,{childList:true,subtree:true});
    }
  }"""
new_install = """  function instalar(){
    let tentativas=0;
    const timer=setInterval(()=>{
      tentativas++;
      const ok=montar();
      if(ok || tentativas>12) clearInterval(timer);
    },250);
  }"""
if old_install not in html:
    raise SystemExit('instalar v65 nao encontrado')
html = html.replace(old_install, new_install, 1)

# 5) Reduz recargas tardias duplicadas dos blocos mais pesados.
html = html.replace("  setTimeout(montar,5000);\n", "", 1)

idx.write_text(html,encoding='utf-8')

swtxt=sw.read_text(encoding='utf-8')
swtxt,n=re.subn(
    r"const CACHE_VERSION = '[^']+';",
    "const CACHE_VERSION = 'simpla-shell-v75-performance-whatsapp';",
    swtxt,
    count=1
)
if n!=1:
    raise SystemExit('cache version nao encontrada')
sw.write_text(swtxt,encoding='utf-8')
