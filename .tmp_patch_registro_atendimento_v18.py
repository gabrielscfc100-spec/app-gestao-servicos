from pathlib import Path

p=Path('index.html')
s=p.read_text(encoding='utf-8')
marker='simpla-registro-atendimento-v18'
if marker in s:
    raise SystemExit('v18 ja aplicada')

# Fluxo iniciado pela Agenda passa a abrir o novo modulo.
s=s.replace("mudarTela('financeiro');\n            mudarAba('aba-entradas');", "abrirRegistroAtendimento();", 1)

block=r'''
<style id="simpla-registro-atendimento-v18">
/* Teste v18: atendimento separado do Financeiro */
#atendimento .registro-atendimento-header{
  margin-bottom:16px;background:#fff;border:1px solid #e2e8f0;border-radius:12px;
  padding:18px 20px;box-shadow:0 2px 8px rgba(26,28,35,.04)
}
#atendimento .registro-atendimento-header h1{margin:0 0 5px;font-size:22px;color:#1a1c23}
#atendimento .registro-atendimento-header p{margin:0;font-size:12px;color:#718096;text-transform:none;line-height:1.45}
#atendimento #aba-entradas{display:block!important;padding:0!important}
#atendimento .fin-receita-grid{margin-top:0}
#financeiro #tab-header-entradas{display:none!important}
@media(max-width:768px){
  #atendimento{padding-bottom:86px}
  #atendimento .registro-atendimento-header{padding:14px;margin-bottom:12px}
  #atendimento .registro-atendimento-header h1{font-size:19px}
  #atendimento .fin-receita-grid{display:grid!important;grid-template-columns:1fr!important;gap:12px!important}
  #atendimento .entradas-layout{display:flex!important;flex-direction:column!important;width:100%!important}
  #atendimento .entradas-form-area,#atendimento .fin-sidebar,#atendimento #sec-fin-combos{width:100%!important;max-width:none!important}
  #atendimento input,#atendimento select,#atendimento textarea{width:100%!important;min-width:0!important;font-size:16px}
  #atendimento .combo-grid{grid-template-columns:repeat(2,minmax(0,1fr))!important}
  #atendimento #lista-carrinho + div{display:flex!important;flex-direction:column!important;align-items:stretch!important;gap:10px!important}
  #atendimento .btn-salvar{min-height:48px;white-space:normal}
}
@media(max-width:420px){#atendimento .combo-grid{grid-template-columns:1fr!important}}
</style>
<script id="simpla-registro-atendimento-v18-script">
(function(){
  function podeOperar(){
    try{
      if(typeof validarAcessoPerfil==='function') return validarAcessoPerfil('financeiroOperar','Seu perfil não pode registrar atendimentos.');
    }catch(e){}
    return true;
  }

  function garantirEstrutura(){
    const main=document.querySelector('.main-content');
    const financeiro=document.getElementById('financeiro');
    const aba=document.getElementById('aba-entradas');
    if(!main||!financeiro||!aba) return false;

    let tela=document.getElementById('atendimento');
    if(!tela){
      tela=document.createElement('div');
      tela.id='atendimento';
      tela.className='screen atendimento-screen';
      tela.innerHTML='<div class="registro-atendimento-header"><h1>Registro de Atendimento</h1><p>Registre o atendimento realizado. Ao finalizar, o recebimento será lançado automaticamente no Financeiro.</p></div><div id="registro-atendimento-host"></div>';
      financeiro.parentNode.insertBefore(tela,financeiro);
    }
    const host=document.getElementById('registro-atendimento-host');
    if(host && aba.parentNode!==host) host.appendChild(aba);

    const tabReceitas=document.getElementById('tab-header-entradas');
    if(tabReceitas) tabReceitas.style.display='none';

    let menu=document.getElementById('menu-btn-atendimento');
    const menuFin=document.getElementById('menu-btn-financeiro');
    if(!menu && menuFin){
      menu=document.createElement('button');
      menu.className='menu-btn';
      menu.id='menu-btn-atendimento';
      menu.type='button';
      menu.innerHTML='Registro de Atendimento';
      menu.onclick=function(ev){ window.abrirRegistroAtendimento(ev); };
      menuFin.parentNode.insertBefore(menu,menuFin);
    }

    // Financeiro passa a abrir em Despesas quando Receitas era a aba ativa.
    const tabSaidas=document.getElementById('tab-header-saidas');
    const abaSaidas=document.getElementById('aba-saidas');
    if(financeiro.classList.contains('active') && (!document.querySelector('#financeiro .aba-content.active'))){
      document.querySelectorAll('#financeiro .aba-content').forEach(x=>x.classList.remove('active'));
      document.querySelectorAll('#financeiro .tab').forEach(x=>x.classList.remove('active'));
      abaSaidas?.classList.add('active'); tabSaidas?.classList.add('active');
    }
    return true;
  }

  window.abrirRegistroAtendimento=function(ev){
    if(!podeOperar()) return;
    garantirEstrutura();
    if(typeof mudarTela==='function') mudarTela('atendimento',ev||null);
    const aba=document.getElementById('aba-entradas');
    if(aba) aba.classList.add('active');
    try{ renderizarCombos?.(); }catch(e){}
    try{ atualizarCarrinhoUI?.(); }catch(e){}
    try{ atualizarEspelhoClienteFinanceiro?.(); }catch(e){}
    window.scrollTo({top:0,behavior:'smooth'});
    setTimeout(sincronizarBottomNav,50);
  };

  function ajustarFinanceiro(){
    const fin=document.getElementById('financeiro');
    if(!fin?.classList.contains('active')) return;
    const ativa=fin.querySelector('.aba-content.active');
    if(!ativa){
      try{ mudarAba('aba-saidas'); }catch(e){
        document.getElementById('aba-saidas')?.classList.add('active');
        document.getElementById('tab-header-saidas')?.classList.add('active');
      }
    }
  }

  function sincronizarBottomNav(){
    const nav=document.querySelector('.simpla-bottom-nav, #simpla-bottom-nav, [data-bottom-nav]');
    if(!nav) return;
    const botoes=[...nav.querySelectorAll('button')];
    const fin=botoes.find(b=>/financeiro/i.test(b.textContent||''));
    if(fin) fin.style.display='none';
    let at=nav.querySelector('[data-tela="atendimento"], .bottom-nav-atendimento');
    if(!at){
      at=document.createElement('button');
      at.type='button'; at.className='bottom-nav-atendimento'; at.dataset.tela='atendimento';
      at.innerHTML='<span style="font-size:18px;line-height:1">+</span><small>Atender</small>';
      at.onclick=()=>window.abrirRegistroAtendimento();
      const agenda=botoes.find(b=>/agenda/i.test(b.textContent||''));
      if(agenda) nav.insertBefore(at,agenda); else nav.appendChild(at);
    }
    const ativo=document.getElementById('atendimento')?.classList.contains('active');
    at.classList.toggle('active',!!ativo);
  }

  function aplicarPermissaoMenu(){
    const menu=document.getElementById('menu-btn-atendimento');
    if(!menu) return;
    // Espelha a visibilidade operacional do antigo módulo de Receitas.
    const perfil=(typeof obterPerfilAtual==='function' ? obterPerfilAtual() : '') || '';
    const p=String(perfil).toUpperCase();
    menu.style.display=(p==='FINANCEIRO' ? 'none' : '');
  }

  function init(){
    if(!garantirEstrutura()) return;
    aplicarPermissaoMenu();
    ajustarFinanceiro();
    sincronizarBottomNav();
    const obs=new MutationObserver(()=>{ aplicarPermissaoMenu(); sincronizarBottomNav(); ajustarFinanceiro(); });
    obs.observe(document.body,{subtree:true,childList:true,attributes:true,attributeFilter:['class','style']});
  }
  if(document.readyState==='loading') document.addEventListener('DOMContentLoaded',()=>setTimeout(init,0));
  else setTimeout(init,0);
})();
</script>
'''

s=s.replace('</body>', block+'\n</body>', 1)
p.write_text(s,encoding='utf-8')

sw=Path('service-worker.js')
t=sw.read_text(encoding='utf-8')
t=t.replace("simpla-shell-v17-bottom-navigation","simpla-shell-v18-registro-atendimento")
sw.write_text(t,encoding='utf-8')
