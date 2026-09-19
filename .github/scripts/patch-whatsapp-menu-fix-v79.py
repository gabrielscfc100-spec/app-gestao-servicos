from pathlib import Path
import re

idx=Path('index.html')
sw=Path('service-worker.js')
html=idx.read_text(encoding='utf-8')

# 1) WhatsApp passa a nascer com uma cfg-v2-section real, então não é considerado vazio.
old="""    waGroup.innerHTML='<h2>'+waCat+'</h2><p class="cfg-v2-desc">Conexão com a Meta, mensagens operacionais, lembretes, franquia e automações.</p><div id="simpla-wa78-container"></div>';"""
new="""    waGroup.innerHTML='<h2>'+waCat+'</h2><p class="cfg-v2-desc">Conexão com a Meta, mensagens operacionais, lembretes, franquia e automações.</p><div class="cfg-v2-section"><div id="simpla-wa78-container"></div></div>';"""
if old not in html:
    raise SystemExit('waGroup v78 nao encontrado')
html=html.replace(old,new,1)

# 2) Proteção explícita: a limpeza de categorias nunca remove o WhatsApp lazy.
old_clean="""  function limparCategoriasVazias(){
    document.querySelectorAll('#configuracoes .cfg-v2-group').forEach(g=>{
      if(!g.querySelector('.cfg-v2-section')){
        const cat=g.dataset.cat;g.remove();
        document.querySelector('#configuracoes .cfg-v2-nav button[data-cat="'+cat+'"]')?.remove();
      }
    });
  }"""
new_clean="""  function limparCategoriasVazias(){
    document.querySelectorAll('#configuracoes .cfg-v2-group').forEach(g=>{
      const cat=g.dataset.cat;
      if(cat==='WhatsApp e Automações') return;
      if(!g.querySelector('.cfg-v2-section')){
        g.remove();
        document.querySelector('#configuracoes .cfg-v2-nav button[data-cat="'+cat+'"]')?.remove();
      }
    });
  }"""
if old_clean not in html:
    raise SystemExit('limparCategoriasVazias nao encontrado')
html=html.replace(old_clean,new_clean,1)

idx.write_text(html,encoding='utf-8')

swtxt=sw.read_text(encoding='utf-8')
swtxt,n=re.subn(
    r"const CACHE_VERSION = '[^']+';",
    "const CACHE_VERSION = 'simpla-shell-v79-whatsapp-menu-fix';",
    swtxt,
    count=1
)
if n!=1:
    raise SystemExit('cache version nao encontrada')
sw.write_text(swtxt,encoding='utf-8')
