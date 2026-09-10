from pathlib import Path

p=Path('index.html')
s=p.read_text(encoding='utf-8')
marker='simpla-bottom-nav-v17'
if marker not in s:
    bloco=r'''
<style id="simpla-bottom-nav-v17">
.simpla-bottom-nav{display:none;}
@media(max-width:768px){
  body{padding-bottom:calc(76px + env(safe-area-inset-bottom))!important;}
  .simpla-bottom-nav{
    position:fixed;
    left:0;right:0;bottom:0;
    z-index:1290;
    display:grid;
    grid-template-columns:repeat(4,minmax(0,1fr));
    gap:2px;
    padding:6px 8px calc(6px + env(safe-area-inset-bottom));
    background:rgba(255,255,255,.98);
    border-top:1px solid #dfe5ec;
    box-shadow:0 -6px 22px rgba(15,23,42,.08);
    backdrop-filter:blur(12px);
    -webkit-backdrop-filter:blur(12px);
  }
  .simpla-bottom-nav-btn{
    appearance:none;
    -webkit-appearance:none;
    border:0;
    background:transparent;
    min-width:0;
    min-height:56px;
    padding:5px 3px;
    border-radius:10px;
    color:#718096;
    display:flex;
    flex-direction:column;
    align-items:center;
    justify-content:center;
    gap:4px;
    cursor:pointer;
    font-size:10px;
    font-weight:700;
    line-height:1.1;
    text-transform:none;
    -webkit-tap-highlight-color:transparent;
    touch-action:manipulation;
  }
  .simpla-bottom-nav-btn svg{
    width:22px;height:22px;
    fill:none;
    stroke:currentColor;
    stroke-width:1.9;
    stroke-linecap:round;
    stroke-linejoin:round;
    pointer-events:none;
  }
  .simpla-bottom-nav-btn span{pointer-events:none;text-transform:none;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;max-width:100%;}
  .simpla-bottom-nav-btn.active{
    color:#1a1c23;
    background:#f1f5f9;
  }
  .simpla-bottom-nav-btn.active svg{color:var(--cor-accent);}
  .simpla-bottom-nav-btn[hidden]{display:none!important;}
}
</style>
<script id="simpla-bottom-nav-v17-script">
(function(){
  const itens=[
    ['dashboard','menu-btn-dashboard','Painel','<svg viewBox="0 0 24 24" aria-hidden="true"><rect x="3" y="3" width="7" height="7" rx="1"></rect><rect x="14" y="3" width="7" height="7" rx="1"></rect><rect x="3" y="14" width="7" height="7" rx="1"></rect><rect x="14" y="14" width="7" height="7" rx="1"></rect></svg>'],
    ['clientes','menu-btn-clientes','Clientes','<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"></path><circle cx="9" cy="7" r="4"></circle><path d="M22 21v-2a4 4 0 0 0-3-3.87"></path><path d="M16 3.13a4 4 0 0 1 0 7.75"></path></svg>'],
    ['financeiro','menu-btn-financeiro','Financeiro','<svg viewBox="0 0 24 24" aria-hidden="true"><rect x="3" y="5" width="18" height="14" rx="2"></rect><path d="M3 10h18"></path><path d="M7 15h2"></path></svg>'],
    ['agenda','menu-btn-agenda','Agenda','<svg viewBox="0 0 24 24" aria-hidden="true"><rect x="3" y="5" width="18" height="16" rx="2"></rect><path d="M16 3v4"></path><path d="M8 3v4"></path><path d="M3 11h18"></path></svg>']
  ];
  function criar(){
    if(document.querySelector('.simpla-bottom-nav')) return;
    const nav=document.createElement('nav');
    nav.className='simpla-bottom-nav';
    nav.setAttribute('aria-label','Navegação principal');
    nav.innerHTML=itens.map(([tela,origem,label,icone])=>`<button type="button" class="simpla-bottom-nav-btn" data-tela="${tela}" data-origem="${origem}" aria-label="${label}">${icone}<span>${label}</span></button>`).join('');
    nav.addEventListener('click',e=>{
      const btn=e.target.closest('.simpla-bottom-nav-btn');
      if(!btn || btn.hidden) return;
      const tela=btn.dataset.tela;
      if(typeof window.mudarTela==='function') window.mudarTela(tela,e);
      if(typeof window.fecharMenuMobile==='function') window.fecharMenuMobile();
      setTimeout(sincronizar,30);
    });
    document.body.appendChild(nav);
    sincronizar();
  }
  function sincronizar(){
    const nav=document.querySelector('.simpla-bottom-nav');
    if(!nav) return;
    nav.querySelectorAll('.simpla-bottom-nav-btn').forEach(btn=>{
      const origem=document.getElementById(btn.dataset.origem);
      let oculto=false;
      if(origem){
        const estilo=getComputedStyle(origem);
        oculto=origem.hidden || estilo.display==='none' || estilo.visibility==='hidden';
      }
      btn.hidden=oculto;
      const tela=document.getElementById(btn.dataset.tela);
      const ativa=!!(tela && tela.classList.contains('active'));
      btn.classList.toggle('active',ativa);
      btn.setAttribute('aria-current',ativa?'page':'false');
    });
    const visiveis=[...nav.querySelectorAll('.simpla-bottom-nav-btn:not([hidden])')].length;
    nav.style.gridTemplateColumns=`repeat(${Math.max(visiveis,1)},minmax(0,1fr))`;
  }
  function iniciar(){
    criar();
    const obs=new MutationObserver(sincronizar);
    obs.observe(document.body,{subtree:true,attributes:true,attributeFilter:['class','style','hidden']});
    window.addEventListener('resize',sincronizar,{passive:true});
    document.addEventListener('visibilitychange',()=>{if(!document.hidden) sincronizar();});
    setInterval(sincronizar,2000);
  }
  if(document.readyState==='loading') document.addEventListener('DOMContentLoaded',iniciar);
  else iniciar();
})();
</script>
'''
    s=s.replace('</body>',bloco+'\n</body>')
    p.write_text(s,encoding='utf-8')

sw=Path('service-worker.js')
if sw.exists():
    t=sw.read_text(encoding='utf-8')
    import re
    t=re.sub(r"const CACHE_VERSION = '[^']+';","const CACHE_VERSION = 'simpla-shell-v17-bottom-navigation';",t,count=1)
    sw.write_text(t,encoding='utf-8')
