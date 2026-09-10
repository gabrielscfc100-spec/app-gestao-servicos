from pathlib import Path

p = Path('index.html')
s = p.read_text(encoding='utf-8')

old = '''<div style="display: flex; gap: 8px; align-items: center;"><label style="font-size: 14px; font-weight: 500;">⏱️ Tempo Padrão (Min):</label><input type="number" id="agenda-intervalo-input" value="45" min="5" step="5" onchange="alterarIntervaloAgenda(this.value)" style="padding: 8px; border: 1px solid #cbd5e0; border-radius: 4px; width: 80px; background: white;"></div>'''
new = '''<input type="hidden" id="agenda-intervalo-input" value="45">'''
if old not in s:
    raise SystemExit('campo de tempo padrao da agenda nao localizado')
s = s.replace(old, new, 1)

css = r'''
<style id="simpla-config-layout-v2">
#configuracoes .header{margin-bottom:16px}
#configuracoes #sec-config-geral{max-width:none!important;padding:0!important;background:transparent!important;box-shadow:none!important}
.cfg-v2-shell{display:grid;grid-template-columns:220px minmax(0,1fr);gap:18px;align-items:start}
.cfg-v2-nav{position:sticky;top:0;background:#fff;border:1px solid #e2e8f0;border-radius:10px;padding:8px;box-shadow:0 1px 3px rgba(31,47,65,.06)}
.cfg-v2-nav button{width:100%;border:0;background:transparent;color:#526579;text-align:left;padding:10px 11px;border-radius:7px;cursor:pointer;font-size:12px;font-weight:700;text-transform:none;display:flex;align-items:center;justify-content:space-between;gap:8px}
.cfg-v2-nav button:hover{background:#f5f7f9;color:#23364d}
.cfg-v2-nav button.ativo{background:#edf2f6;color:#23364d}
.cfg-v2-content{min-width:0}
.cfg-v2-group{display:none;background:#fff;border:1px solid #e2e8f0;border-radius:10px;padding:22px;box-shadow:0 1px 3px rgba(31,47,65,.06)}
.cfg-v2-group.ativo{display:block}
.cfg-v2-group>h2{font-size:18px;color:#23364d;margin:0 0 4px;text-transform:none}
.cfg-v2-group>.cfg-v2-desc{font-size:12px;color:#718096;margin:0 0 20px;text-transform:none}
.cfg-v2-section{padding:18px 0;border-top:1px solid #edf1f4}
.cfg-v2-section:first-of-type{border-top:0;padding-top:4px}
.cfg-v2-section>h3{font-size:15px!important;color:#23364d!important;margin:0 0 10px!important;text-transform:none!important}
#configuracoes .section-box-cfg{background:#f8fafc;border-color:#e1e7ec;border-radius:8px}
.cfg-switch-line{display:flex;align-items:center;justify-content:space-between;gap:18px;padding:10px 0}
.cfg-switch-copy{min-width:0;flex:1}
.cfg-switch-title{font-size:13px;font-weight:700;color:#2d4156;text-transform:none}
.cfg-switch-state{font-size:11px;color:#718096;margin-top:2px;text-transform:none}
.cfg-switch{position:relative;display:inline-flex;flex:0 0 auto;width:46px;height:26px}
.cfg-switch input{position:absolute;opacity:0;pointer-events:none}
.cfg-switch-track{width:46px;height:26px;border-radius:999px;background:#cbd5df;position:relative;cursor:pointer;transition:.18s}
.cfg-switch-track:after{content:"";position:absolute;width:20px;height:20px;left:3px;top:3px;border-radius:50%;background:#fff;box-shadow:0 1px 3px rgba(0,0,0,.2);transition:.18s}
.cfg-switch input:checked + .cfg-switch-track{background:#345a7d}
.cfg-switch input:checked + .cfg-switch-track:after{transform:translateX(20px)}
#configuracoes input[type="checkbox"]:not(.cfg-switch-input){appearance:none;-webkit-appearance:none;width:42px!important;height:24px!important;border:0!important;border-radius:999px!important;background:#cbd5df!important;position:relative!important;cursor:pointer!important;vertical-align:middle!important;transition:.18s!important;padding:0!important;min-height:24px!important}
#configuracoes input[type="checkbox"]:not(.cfg-switch-input):after{content:"";position:absolute;width:18px;height:18px;left:3px;top:3px;border-radius:50%;background:#fff;box-shadow:0 1px 3px rgba(0,0,0,.2);transition:.18s}
#configuracoes input[type="checkbox"]:not(.cfg-switch-input):checked{background:#345a7d!important}
#configuracoes input[type="checkbox"]:not(.cfg-switch-input):checked:after{transform:translateX(18px)}
@media(max-width:900px){.cfg-v2-shell{grid-template-columns:1fr}.cfg-v2-nav{position:static;display:flex;overflow-x:auto;gap:6px;padding:7px}.cfg-v2-nav button{width:auto;white-space:nowrap;flex:0 0 auto}.cfg-v2-group{padding:16px}}
</style>
'''
if 'id="simpla-config-layout-v2"' not in s:
    s = s.replace('</head>', css + '\n</head>', 1)

js = r'''
<script id="simpla-config-layout-v2-js">
(function(){
  function txt(el){return String(el?.textContent||'').replace(/\s+/g,' ').trim();}
  function categoriaPorTitulo(t){
    const u=t.toUpperCase();
    if(/HORÁRIO|EXPEDIENTE|BLOQUEIO|AGENDAMENTO|PORTAL/.test(u)) return 'Agenda e Portal';
    if(/NOTIFICA/.test(u)) return 'Notificações';
    if(/COMISS/.test(u)) return 'Comissões';
    if(/CLIENT|FIDEL|ANIVERS/.test(u)) return 'Clientes';
    if(/FINANCE|PAGAMENTO|MATERIAL|CUSTO/.test(u)) return 'Financeiro';
    if(/USUÁ|USUA|PERFIL|ACESS|SENHA|SEGUR/.test(u)) return 'Usuários e Segurança';
    if(/TEMA|APAR|NOME|NEGÓCIO|NEGOCIO|EMPRESA|MARCA/.test(u)) return 'Geral e Aparência';
    return 'Outros';
  }
  function descricao(cat){
    const d={
      'Agenda e Portal':'Horários, bloqueios, confirmações e regras do agendamento online.',
      'Notificações':'Preferências e permissões para avisos do SimplA.',
      'Comissões':'Regras e percentuais utilizados nos cálculos de comissão.',
      'Clientes':'Cadastro, relacionamento e recursos disponíveis para clientes.',
      'Financeiro':'Recursos e comportamentos relacionados à gestão financeira.',
      'Usuários e Segurança':'Acessos, perfis e controles de segurança da empresa.',
      'Geral e Aparência':'Identidade, visual e preferências gerais do sistema.',
      'Outros':'Outras preferências disponíveis para a empresa.'
    }; return d[cat]||'';
  }
  function criarSwitchParaSelect(sel){
    if(!sel || sel.dataset.cfgSwitch==='1') return;
    const vals=[...sel.options].map(o=>String(o.value));
    if(vals.length!==2 || !vals.includes('true') || !vals.includes('false')) return;
    sel.dataset.cfgSwitch='1';
    sel.style.display='none';
    const form=sel.closest('.form-group')||sel.parentElement;
    if(!form) return;
    const label=form.querySelector('label');
    const titulo=txt(label)||txt(form.querySelector('h4'))||'Ativar opção';
    if(label) label.style.display='none';
    const linha=document.createElement('div'); linha.className='cfg-switch-line';
    const copy=document.createElement('div'); copy.className='cfg-switch-copy';
    const tit=document.createElement('div'); tit.className='cfg-switch-title'; tit.textContent=titulo;
    const estado=document.createElement('div'); estado.className='cfg-switch-state';
    copy.append(tit,estado);
    const lab=document.createElement('label'); lab.className='cfg-switch';
    const inp=document.createElement('input'); inp.type='checkbox'; inp.className='cfg-switch-input';
    const track=document.createElement('span'); track.className='cfg-switch-track';
    lab.append(inp,track); linha.append(copy,lab); form.insertBefore(linha,sel);
    const sync=()=>{inp.checked=sel.value!=='false';estado.textContent=inp.checked?'Ativado':'Desativado';};
    inp.addEventListener('change',()=>{sel.value=inp.checked?'true':'false';estado.textContent=inp.checked?'Ativado':'Desativado';sel.dispatchEvent(new Event('change',{bubbles:true}));});
    sel.addEventListener('change',sync); sync();
    sel._cfgSync=sync;
  }
  function sincronizarSwitches(){document.querySelectorAll('#configuracoes select[data-cfg-switch="1"]').forEach(s=>s._cfgSync&&s._cfgSync());}
  function montar(){
    const tela=document.getElementById('configuracoes');
    const raiz=document.getElementById('sec-config-geral');
    if(!tela||!raiz||raiz.dataset.layoutV2==='1') return;
    raiz.dataset.layoutV2='1';
    document.querySelectorAll('#configuracoes select').forEach(criarSwitchParaSelect);

    const orig=[...raiz.childNodes];
    const secoes=[]; let atual=null;
    orig.forEach(n=>{
      if(n.nodeType===1 && n.tagName==='H3'){
        atual={titulo:txt(n),nodes:[n]}; secoes.push(atual);
      } else if(atual){atual.nodes.push(n);}
    });
    if(!secoes.length) return;
    // Remove o conteúdo original que será realocado.
    secoes.forEach(sec=>sec.nodes.forEach(n=>{if(n.parentNode===raiz) raiz.removeChild(n);}));
    [...raiz.querySelectorAll(':scope > hr')].forEach(h=>h.remove());

    const shell=document.createElement('div'); shell.className='cfg-v2-shell';
    const nav=document.createElement('nav'); nav.className='cfg-v2-nav'; nav.setAttribute('aria-label','Categorias das configurações');
    const content=document.createElement('div'); content.className='cfg-v2-content';
    const grupos=new Map();
    secoes.forEach(sec=>{
      const cat=categoriaPorTitulo(sec.titulo);
      if(!grupos.has(cat)) grupos.set(cat,[]);
      grupos.get(cat).push(sec);
    });
    let idx=0;
    function ativar(nome){
      nav.querySelectorAll('button').forEach(b=>b.classList.toggle('ativo',b.dataset.cat===nome));
      content.querySelectorAll('.cfg-v2-group').forEach(g=>g.classList.toggle('ativo',g.dataset.cat===nome));
      sincronizarSwitches();
    }
    grupos.forEach((lista,cat)=>{
      const b=document.createElement('button'); b.type='button'; b.dataset.cat=cat; b.innerHTML='<span>'+cat+'</span><span>›</span>'; b.onclick=()=>ativar(cat); nav.appendChild(b);
      const g=document.createElement('section'); g.className='cfg-v2-group'; g.dataset.cat=cat;
      const h=document.createElement('h2'); h.textContent=cat; const d=document.createElement('p'); d.className='cfg-v2-desc'; d.textContent=descricao(cat); g.append(h,d);
      lista.forEach(sec=>{const box=document.createElement('div');box.className='cfg-v2-section';sec.nodes.forEach(n=>{if(n.nodeType===1&&n.tagName==='HR') return;box.appendChild(n);});g.appendChild(box);});
      content.appendChild(g); if(idx++===0) setTimeout(()=>ativar(cat),0);
    });
    shell.append(nav,content); raiz.appendChild(shell);
  }
  document.addEventListener('DOMContentLoaded',()=>setTimeout(montar,0));
  const timer=setInterval(()=>{const tela=document.getElementById('configuracoes');if(tela?.classList.contains('active')){montar();sincronizarSwitches();}},700);
  window.addEventListener('beforeunload',()=>clearInterval(timer));
})();
</script>
'''
if 'id="simpla-config-layout-v2-js"' not in s:
    s = s.replace('</body>', js + '\n</body>', 1)

p.write_text(s, encoding='utf-8')
print('patch aplicado')
