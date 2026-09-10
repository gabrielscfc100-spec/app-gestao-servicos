from pathlib import Path
import re

p=Path('index.html')
s=p.read_text(encoding='utf-8')
if 'simpla-config-financeiro-comissoes-v29' in s:
    raise SystemExit('v29 ja aplicada')

block=r'''
<script id="simpla-config-financeiro-comissoes-v29">
(function(){
  function obter(){
    const raiz=document.getElementById('configuracoes');
    if(!raiz) return {};
    return {
      raiz,
      nav:raiz.querySelector('.cfg-v2-nav'),
      content:raiz.querySelector('.cfg-v2-content')
    };
  }

  function criarFinanceiro(nav,content){
    let fin=content.querySelector('.cfg-v2-group[data-cat="Financeiro"]');
    if(fin) return fin;

    fin=document.createElement('section');
    fin.className='cfg-v2-group';
    fin.dataset.cat='Financeiro';
    fin.innerHTML='<h2>Financeiro</h2><p class="cfg-v2-desc">Pagamentos, Pix, comissões e demais configurações financeiras.</p>';

    const outros=content.querySelector('.cfg-v2-group[data-cat="Outros"]');
    if(outros) content.insertBefore(fin,outros); else content.appendChild(fin);

    if(!nav.querySelector('button[data-cat="Financeiro"]')){
      const b=document.createElement('button');
      b.type='button';
      b.dataset.cat='Financeiro';
      b.innerHTML='<span>Financeiro</span><span>›</span>';
      b.addEventListener('click',()=>{
        nav.querySelectorAll('button').forEach(x=>x.classList.toggle('ativo',x===b));
        content.querySelectorAll('.cfg-v2-group').forEach(g=>g.classList.toggle('ativo',g===fin));
      });
      const boutros=nav.querySelector('button[data-cat="Outros"]');
      if(boutros) nav.insertBefore(b,boutros); else nav.appendChild(b);
    }
    return fin;
  }

  function reorganizar(){
    const {nav,content}=obter();
    if(!nav||!content) return;

    const com=content.querySelector('.cfg-v2-group[data-cat="Comissões"]');
    let fin=content.querySelector('.cfg-v2-group[data-cat="Financeiro"]');
    if(com && !fin) fin=criarFinanceiro(nav,content);

    if(com && fin){
      const estavaAtiva=com.classList.contains('ativo') || nav.querySelector('button[data-cat="Comissões"]')?.classList.contains('ativo');
      [...com.querySelectorAll(':scope > .cfg-v2-section')].forEach(sec=>fin.appendChild(sec));
      com.remove();
      nav.querySelector('button[data-cat="Comissões"]')?.remove();

      const desc=fin.querySelector(':scope > .cfg-v2-desc');
      if(desc) desc.textContent='Pagamentos, Pix, comissões e demais configurações financeiras.';

      if(estavaAtiva){
        nav.querySelectorAll('button').forEach(b=>b.classList.toggle('ativo',b.dataset.cat==='Financeiro'));
        content.querySelectorAll('.cfg-v2-group').forEach(g=>g.classList.toggle('ativo',g.dataset.cat==='Financeiro'));
      }
    }

    // "Outros" sempre por último no menu e no conteúdo.
    const btnOutros=nav.querySelector('button[data-cat="Outros"]');
    if(btnOutros && btnOutros!==nav.lastElementChild) nav.appendChild(btnOutros);
    const grupoOutros=content.querySelector('.cfg-v2-group[data-cat="Outros"]');
    if(grupoOutros && grupoOutros!==content.lastElementChild) content.appendChild(grupoOutros);
  }

  function iniciar(){
    reorganizar();
    const raiz=document.getElementById('configuracoes');
    if(!raiz) return;
    let pendente=false;
    const obs=new MutationObserver(()=>{
      if(pendente) return;
      pendente=true;
      requestAnimationFrame(()=>{pendente=false;reorganizar();});
    });
    obs.observe(raiz,{childList:true,subtree:true});
  }

  if(document.readyState==='loading') document.addEventListener('DOMContentLoaded',()=>setTimeout(iniciar,120));
  else setTimeout(iniciar,120);
  document.addEventListener('click',e=>{
    if(e.target.closest('#menu-btn-configuracoes')) setTimeout(reorganizar,120);
  },true);
  setTimeout(reorganizar,700);
  setTimeout(reorganizar,1600);
})();
</script>
'''

s=s.replace('</body>', block+'\n</body>', 1)
p.write_text(s,encoding='utf-8')

sw=Path('service-worker.js')
t=sw.read_text(encoding='utf-8')
t,n=re.subn(r"const CACHE_VERSION = '[^']+';", "const CACHE_VERSION = 'simpla-shell-v29-config-financeiro';", t, count=1)
assert n==1, 'CACHE_VERSION nao encontrado'
sw.write_text(t,encoding='utf-8')
