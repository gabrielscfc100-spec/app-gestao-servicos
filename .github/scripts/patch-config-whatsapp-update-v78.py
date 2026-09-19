from pathlib import Path
import re

idx=Path('index.html')
sw=Path('service-worker.js')
html=idx.read_text(encoding='utf-8')

# Remove bootstrap v77 separado: a categoria passará a nascer dentro do próprio layout de Configurações.
html,n=re.subn(
    r'\n?<script id="simpla-whatsapp-lazy-v77">.*?</script>\s*',
    '\n',
    html,
    count=1,
    flags=re.S
)
if n!=1:
    raise SystemExit('bootstrap v77 nao encontrado')

# Insere helper lazy dentro do IIFE do layout nativo.
anchor="""  function sincronizarSwitches(){document.querySelectorAll('#configuracoes select[data-cfg-switch="1"]').forEach(s=>s._cfgSync&&s._cfgSync());}
  function montar(){"""
replacement="""  function sincronizarSwitches(){document.querySelectorAll('#configuracoes select[data-cfg-switch="1"]').forEach(s=>s._cfgSync&&s._cfgSync());}

  let waLazyPromise=null;
  function carregarWhatsAppConfigLazy(container){
    if(!container) return;
    if(window.SimplAWhatsAppV77){
      Promise.resolve(window.SimplAWhatsAppV77.mount(container)).catch(console.error);
      return;
    }
    if(waLazyPromise) return;
    container.innerHTML='<div style="padding:24px;text-align:center;color:#718096;font-size:12px;text-transform:none">Carregando WhatsApp e Automações...</div>';
    waLazyPromise=new Promise((resolve,reject)=>{
      const s=document.createElement('script');
      s.src='./whatsapp-automacoes-v77.js?v=78';
      s.async=true;
      s.onload=()=>{
        if(!window.SimplAWhatsAppV77) return reject(new Error('Módulo WhatsApp não inicializado.'));
        Promise.resolve(window.SimplAWhatsAppV77.mount(container)).then(resolve,reject);
      };
      s.onerror=()=>reject(new Error('Falha ao carregar o módulo WhatsApp.'));
      document.head.appendChild(s);
    }).catch(err=>{
      console.error('SimplA WhatsApp lazy:',err);
      container.innerHTML='<div style="padding:24px;text-align:center;color:#c53030;font-size:12px;text-transform:none">Não foi possível carregar esta área agora.</div>';
      waLazyPromise=null;
    });
  }

  function montar(){"""
if anchor not in html:
    raise SystemExit('anchor sincronizarSwitches nao encontrado')
html=html.replace(anchor,replacement,1)

# Adiciona categoria diretamente no layout antes de montar shell.
anchor2="""    grupos.forEach((lista,cat)=>{
      const b=document.createElement('button'); b.type='button'; b.dataset.cat=cat; b.innerHTML='<span>'+cat+'</span><span>›</span>'; b.onclick=()=>ativar(cat); nav.appendChild(b);
      const g=document.createElement('section'); g.className='cfg-v2-group'; g.dataset.cat=cat;
      const h=document.createElement('h2'); h.textContent=cat; const d=document.createElement('p'); d.className='cfg-v2-desc'; d.textContent=descricao(cat); g.append(h,d);
      lista.forEach(sec=>{const box=document.createElement('div');box.className='cfg-v2-section';sec.nodes.forEach(n=>{if(n.nodeType===1&&n.tagName==='HR') return;box.appendChild(n);});g.appendChild(box);});
      content.appendChild(g); if(idx++===0) setTimeout(()=>ativar(cat),0);
    });
    shell.append(nav,content); raiz.appendChild(shell);
  }"""
replacement2="""    grupos.forEach((lista,cat)=>{
      const b=document.createElement('button'); b.type='button'; b.dataset.cat=cat; b.innerHTML='<span>'+cat+'</span><span>›</span>'; b.onclick=()=>ativar(cat); nav.appendChild(b);
      const g=document.createElement('section'); g.className='cfg-v2-group'; g.dataset.cat=cat;
      const h=document.createElement('h2'); h.textContent=cat; const d=document.createElement('p'); d.className='cfg-v2-desc'; d.textContent=descricao(cat); g.append(h,d);
      lista.forEach(sec=>{const box=document.createElement('div');box.className='cfg-v2-section';sec.nodes.forEach(n=>{if(n.nodeType===1&&n.tagName==='HR') return;box.appendChild(n);});g.appendChild(box);});
      content.appendChild(g); if(idx++===0) setTimeout(()=>ativar(cat),0);
    });

    // WhatsApp nasce junto com o menu nativo, mas seu conteúdo continua 100% lazy.
    const waCat='WhatsApp e Automações';
    const waBtn=document.createElement('button');
    waBtn.type='button'; waBtn.dataset.cat=waCat;
    waBtn.innerHTML='<span>'+waCat+'</span><span>›</span>';

    const waGroup=document.createElement('section');
    waGroup.className='cfg-v2-group'; waGroup.dataset.cat=waCat;
    waGroup.innerHTML='<h2>'+waCat+'</h2><p class="cfg-v2-desc">Conexão com a Meta, mensagens operacionais, lembretes, franquia e automações.</p><div id="simpla-wa78-container"></div>';

    waBtn.onclick=()=>{
      ativar(waCat);
      carregarWhatsAppConfigLazy(waGroup.querySelector('#simpla-wa78-container'));
    };

    const geralBtn=[...nav.querySelectorAll('button')].find(b=>b.dataset.cat==='Geral e Aparência');
    const geralGroup=content.querySelector('.cfg-v2-group[data-cat="Geral e Aparência"]');
    if(geralBtn) nav.insertBefore(waBtn,geralBtn); else nav.appendChild(waBtn);
    if(geralGroup) content.insertBefore(waGroup,geralGroup); else content.appendChild(waGroup);

    shell.append(nav,content); raiz.appendChild(shell);
  }"""
if anchor2 not in html:
    raise SystemExit('bloco grupos nao encontrado')
html=html.replace(anchor2,replacement2,1)

# Para o polling eterno do layout assim que a estrutura já estiver montada.
old_timer="""  const timer=setInterval(()=>{const tela=document.getElementById('configuracoes');if(tela?.classList.contains('active')){montar();sincronizarSwitches();}},700);
  window.addEventListener('beforeunload',()=>clearInterval(timer));"""
new_timer="""  let tentativasLayout=0;
  const timer=setInterval(()=>{
    tentativasLayout++;
    const tela=document.getElementById('configuracoes');
    if(tela?.classList.contains('active')){montar();sincronizarSwitches();}
    const raiz=document.getElementById('sec-config-geral');
    if(raiz?.dataset.layoutV2==='1' || tentativasLayout>60) clearInterval(timer);
  },700);"""
if old_timer not in html:
    raise SystemExit('timer config nao encontrado')
html=html.replace(old_timer,new_timer,1)

# Hotfix do update manager: fallback para reload caso controllerchange demore.
old_update="""  function aplicarAtualizacao(){
    const worker = registroPWA?.waiting;
    if(worker){
      const btn = document.getElementById('simpla-update-btn');
      if(btn){ btn.disabled = true; btn.textContent = 'Atualizando...'; }
      worker.postMessage({tipo:'SKIP_WAITING'});
      return;
    }
    window.location.reload();
  }"""
new_update="""  function aplicarAtualizacao(){
    const btn = document.getElementById('simpla-update-btn');
    if(btn){ btn.disabled = true; btn.textContent = 'Aplicando atualização...'; }

    const worker = registroPWA?.waiting;
    if(worker){
      worker.postMessage({tipo:'SKIP_WAITING'});
      // Alguns navegadores demoram ou não disparam controllerchange prontamente.
      // O reload com cache-buster garante que a nova navegação busque o HTML atual.
      setTimeout(()=>{
        if(recarregando) return;
        const u=new URL(window.location.href);
        u.searchParams.set('_simpla_update',Date.now().toString());
        window.location.replace(u.toString());
      },1800);
      return;
    }

    const u=new URL(window.location.href);
    u.searchParams.set('_simpla_update',Date.now().toString());
    window.location.replace(u.toString());
  }"""
if old_update not in html:
    raise SystemExit('aplicarAtualizacao nao encontrado')
html=html.replace(old_update,new_update,1)

idx.write_text(html,encoding='utf-8')

swtxt=sw.read_text(encoding='utf-8')
swtxt,n=re.subn(
    r"const CACHE_VERSION = '[^']+';",
    "const CACHE_VERSION = 'simpla-shell-v78-config-update-fix';",
    swtxt,
    count=1
)
if n!=1:
    raise SystemExit('cache version nao encontrada')
sw.write_text(swtxt,encoding='utf-8')
