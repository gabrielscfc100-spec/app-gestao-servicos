from pathlib import Path
import re

idx=Path('index.html')
sw=Path('service-worker.js')
html=idx.read_text(encoding='utf-8')

if 'simpla-whatsapp-categoria-v65' in html:
    raise SystemExit('v65 ja aplicada')

marker='</body>'
if marker not in html:
    raise SystemExit('body nao encontrado')

block=r'''
<style id="simpla-whatsapp-categoria-v65-css">
  .simpla-wa-roadmap-v65{margin-top:16px;border:1px dashed #cbd5e0;border-radius:10px;padding:14px;background:#f8fafc;text-transform:none}
  .simpla-wa-roadmap-v65 h3{margin:0 0 5px;font-size:13px;color:#2d3748;text-transform:none}
  .simpla-wa-roadmap-v65 p{margin:0;font-size:10px;line-height:1.5;color:#718096;text-transform:none}
  .simpla-wa-roadmap-v65-grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:8px;margin-top:11px}
  .simpla-wa-roadmap-v65-item{padding:10px;border-radius:8px;background:#fff;border:1px solid #e2e8f0}
  .simpla-wa-roadmap-v65-item b{display:block;font-size:9px;color:#4a5568;margin-bottom:3px;text-transform:none}
  .simpla-wa-roadmap-v65-item span{font-size:9px;color:#a0aec0;text-transform:none}
  @media(max-width:760px){.simpla-wa-roadmap-v65-grid{grid-template-columns:1fr}}
</style>
<script id="simpla-whatsapp-categoria-v65">
(function(){
  const CAT='WhatsApp e Automações';

  function ehAdmin(){
    try{
      if(typeof usuarioEhAdmin==='function') return !!usuarioEhAdmin();
      return String(window.usuarioAtual?.perfil||window.empresaAtual?.perfil||'').toUpperCase()==='ADMIN';
    }catch(_){return false}
  }

  function descricao(){
    return 'Conexão com a Meta, mensagens operacionais, templates e futuras regras de automação.';
  }

  function criarRoadmap(container){
    if(document.getElementById('simpla-wa-roadmap-v65')) return;
    const box=document.createElement('div');
    box.id='simpla-wa-roadmap-v65';
    box.className='simpla-wa-roadmap-v65';
    box.innerHTML='<h3>Próximas configurações</h3><p>Esta área já está reservada para as próximas etapas do WhatsApp operacional. Os controles serão liberados conforme forem implementados e testados.</p><div class="simpla-wa-roadmap-v65-grid"><div class="simpla-wa-roadmap-v65-item"><b>Regras de envio</b><span>Antecedência, horários permitidos e prevenção de duplicidade.</span></div><div class="simpla-wa-roadmap-v65-item"><b>Automações</b><span>Confirmação, lembrete, cancelamento e reagendamento automáticos.</span></div><div class="simpla-wa-roadmap-v65-item"><b>Histórico e monitoramento</b><span>Enviados, pendentes, erros e reenvios.</span></div></div>';
    container.appendChild(box);
  }

  function ordenarBotao(nav, btn){
    const geral=[...nav.querySelectorAll('button')].find(b=>String(b.dataset.cat||'')==='Geral e Aparência');
    if(geral) nav.insertBefore(btn,geral);
    else {
      const usuarios=[...nav.querySelectorAll('button')].find(b=>String(b.dataset.cat||'')==='Usuários e Segurança');
      if(usuarios) nav.insertBefore(btn,usuarios);
      else nav.appendChild(btn);
    }
  }

  function ativar(nav,content){
    nav.querySelectorAll('button').forEach(b=>b.classList.toggle('ativo',b.dataset.cat===CAT));
    content.querySelectorAll('.cfg-v2-group').forEach(g=>g.classList.toggle('ativo',g.dataset.cat===CAT));
    setTimeout(()=>{
      try{ if(typeof carregarWhatsAppConfigV62==='function') carregarWhatsAppConfigV62(); }catch(_){}
      try{ if(typeof carregarTemplatesWhatsAppV63==='function') carregarTemplatesWhatsAppV63(); }catch(_){}
      try{ if(typeof carregarEmbeddedSignupV64==='function') carregarEmbeddedSignupV64(); }catch(_){}
    },80);
  }

  function montar(){
    const shell=document.querySelector('#configuracoes .cfg-v2-shell');
    if(!shell) return false;
    const nav=shell.querySelector('.cfg-v2-nav');
    const content=shell.querySelector('.cfg-v2-content');
    if(!nav||!content) return false;

    let group=content.querySelector('.cfg-v2-group[data-cat="'+CAT+'"]');
    let btn=[...nav.querySelectorAll('button')].find(b=>b.dataset.cat===CAT);

    if(!ehAdmin()){
      if(btn) btn.style.display='none';
      if(group) group.style.display='none';
      return true;
    }

    if(!btn){
      btn=document.createElement('button');
      btn.type='button';
      btn.dataset.cat=CAT;
      btn.innerHTML='<span>'+CAT+'</span><span>›</span>';
      btn.onclick=()=>ativar(nav,content);
      ordenarBotao(nav,btn);
    }
    btn.style.display='';

    if(!group){
      group=document.createElement('section');
      group.className='cfg-v2-group';
      group.dataset.cat=CAT;
      const h=document.createElement('h2'); h.textContent=CAT;
      const d=document.createElement('p'); d.className='cfg-v2-desc'; d.textContent=descricao();
      const area=document.createElement('div'); area.id='simpla-wa-categoria-v65-content'; area.className='cfg-v2-section';
      group.append(h,d,area);

      const geral=content.querySelector('.cfg-v2-group[data-cat="Geral e Aparência"]');
      if(geral) content.insertBefore(group,geral); else content.appendChild(group);
    }
    group.style.display='';

    const area=group.querySelector('#simpla-wa-categoria-v65-content') || group;
    const status=document.getElementById('simpla-wa-v62');
    const templates=document.getElementById('simpla-wa-tpl-v63');

    if(status && status.parentElement!==area) area.appendChild(status);
    if(templates && templates.parentElement!==area) area.appendChild(templates);
    criarRoadmap(area);

    return true;
  }

  function instalar(){
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
  }

  document.addEventListener('click',e=>{
    const b=e.target.closest?.('.cfg-v2-nav button');
    if(b && b.dataset.cat===CAT) setTimeout(()=>montar(),20);
  },true);

  if(document.readyState==='loading') document.addEventListener('DOMContentLoaded',()=>setTimeout(instalar,500));
  else setTimeout(instalar,500);
  setTimeout(montar,2500);
  setTimeout(montar,5000);
})();
</script>
'''

html=html.replace(marker,block+'\n'+marker,1)
idx.write_text(html,encoding='utf-8')

swtxt=sw.read_text(encoding='utf-8')
swtxt,n=re.subn(r"const CACHE_VERSION = '[^']+';","const CACHE_VERSION = 'simpla-shell-v65-whatsapp-categoria';",swtxt,count=1)
if n!=1: raise SystemExit('cache version nao encontrada')
sw.write_text(swtxt,encoding='utf-8')
