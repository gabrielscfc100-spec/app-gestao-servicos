from pathlib import Path
import re

idx=Path('index.html')
sw=Path('service-worker.js')
html=idx.read_text(encoding='utf-8')

if 'simpla-dashboard-servicos-v49' in html:
    raise SystemExit('v49 ja aplicada')

# Dashboard/Gestao exclusivo do ADMIN na matriz de perfis.
def restringir_bloco(nome, texto):
    padrao=re.compile(rf"({nome}:\s*\{{)(.*?)(\n\s*\}},)", re.S)
    m=padrao.search(texto)
    if not m:
        raise SystemExit(f'bloco {nome} nao encontrado')
    corpo=m.group(2)
    corpo,n1=re.subn(r"telas:\s*\[([^\]]*)\]", lambda x: "telas: [" + ",".join([p for p in x.group(1).split(',') if "'dashboard'" not in p and '"dashboard"' not in p]) + "]", corpo, count=1)
    corpo,n2=re.subn(r"dashboard:\s*true", "dashboard: false", corpo, count=1)
    if n1!=1 or n2!=1:
        raise SystemExit(f'nao foi possivel restringir dashboard em {nome}')
    return texto[:m.start()] + m.group(1) + corpo + m.group(3) + texto[m.end():]

html=restringir_bloco('GESTOR',html)
html=restringir_bloco('FINANCEIRO',html)

# Atualiza descricoes antigas da matriz visual, se presentes.
html=html.replace('Dashboard, clientes, financeiro, agenda e catálogo; sem Configurações e gestão de usuários.','Clientes, financeiro, agenda e catálogo; sem Gestão/Dashboard, Configurações e gestão de usuários.')
html=html.replace('Dashboard e financeiro completos; clientes e agenda somente para consulta; sem catálogo ou Configurações.','Financeiro completo; clientes e agenda somente para consulta; sem Gestão/Dashboard, catálogo ou Configurações.')

marker='</body>'
if marker not in html:
    raise SystemExit('body nao encontrado')

block=r'''
<style id="simpla-dashboard-servicos-v49-css">
  .dash-serv-v49{margin:0 0 24px;background:#fff;border:1px solid #e2e8f0;border-radius:10px;padding:16px;box-shadow:0 2px 4px rgba(0,0,0,.04)}
  .dash-serv-v49-head{display:flex;justify-content:space-between;align-items:flex-start;gap:12px;flex-wrap:wrap;margin-bottom:12px}
  .dash-serv-v49-head h3{margin:0;font-size:15px;color:#1a1c23}
  .dash-serv-v49-head p{margin:4px 0 0;font-size:11px;color:#718096;text-transform:none}
  .dash-serv-v49-wrap{overflow-x:auto;border:1px solid #e2e8f0;border-radius:8px}
  .dash-serv-v49-table{width:100%;min-width:700px;margin:0;border-collapse:collapse}
  .dash-serv-v49-table th{font-size:9px;color:#718096;background:#f8fafc;padding:10px;text-align:left;white-space:nowrap}
  .dash-serv-v49-table td{font-size:11px;color:#2d3748;padding:10px;border-top:1px solid #edf2f7;white-space:nowrap}
  .dash-serv-v49-table td:first-child{font-weight:800;color:#1a1c23}
  .dash-serv-v49-table .valor{font-weight:800;color:#2f855a}
  .dash-serv-v49-barra{width:110px;height:7px;border-radius:99px;background:#edf2f7;overflow:hidden;display:inline-block;vertical-align:middle;margin-right:6px}
  .dash-serv-v49-barra i{display:block;height:100%;background:var(--cor-accent);border-radius:99px}
  .dash-serv-v49-vazio{padding:16px;font-size:11px;color:#718096;text-transform:none}
  @media(max-width:600px){.dash-serv-v49{padding:12px}.dash-serv-v49-head p{font-size:10px}}
</style>
<script id="simpla-dashboard-servicos-v49">
(function(){
  function admin(){try{return typeof obterPerfilAtual==='function'&&String(obterPerfilAtual()).toUpperCase()==='ADMIN'}catch(_){return false}}
  function moeda(v){return Number(v||0).toLocaleString('pt-BR',{style:'currency',currency:'BRL'})}
  function esc(v){return String(v??'').replace(/[&<>"']/g,m=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[m]))}

  function aplicarAcessoAdmin(){
    if(typeof obterPerfilAtual!=='function')return;
    const ehAdmin=admin();
    const btn=document.getElementById('menu-btn-dashboard');
    if(btn)btn.style.display=ehAdmin?'':'none';
    const dash=document.getElementById('dashboard');
    if(!ehAdmin&&dash?.classList.contains('active')){
      dash.classList.remove('active');
      const destino=document.getElementById('clientes')||document.getElementById('agenda')||document.getElementById('financeiro');
      if(destino)destino.classList.add('active');
      document.querySelectorAll('.menu-btn').forEach(x=>x.classList.remove('active'));
      const b=document.getElementById(destino?.id==='clientes'?'menu-btn-clientes':destino?.id==='agenda'?'menu-btn-agenda':'menu-btn-financeiro');
      if(b)b.classList.add('active');
    }
  }

  function garantir(){
    if(!admin())return null;
    const dash=document.getElementById('dashboard');
    if(!dash)return null;
    let box=document.getElementById('dash-serv-v49');
    if(box)return box;
    box=document.createElement('div');box.id='dash-serv-v49';box.className='dash-serv-v49';
    box.innerHTML=`<div class="dash-serv-v49-head"><div><h3>Desempenho por Serviço</h3><p>Quantidade realizada, faturamento, ticket médio e participação no faturamento de serviços no período.</p></div></div><div class="dash-serv-v49-wrap"><table class="dash-serv-v49-table"><thead><tr><th>SERVIÇO</th><th>QUANTIDADE</th><th>FATURAMENTO</th><th>TICKET MÉDIO</th><th>PARTICIPAÇÃO</th></tr></thead><tbody id="dash-serv-v49-body"><tr><td colspan="5" class="dash-serv-v49-vazio">Carregando dados...</td></tr></tbody></table></div>`;
    const prof=document.getElementById('dash-prof-v48');
    if(prof)prof.insertAdjacentElement('afterend',box);
    else document.getElementById('dash-agenda-v47')?.insertAdjacentElement('afterend',box);
    return box;
  }

  function normalizarItem(i){
    const tipo=String(i.tipo||i.type||'').toUpperCase();
    return {tipo,nome:i.nome||i.name||'SERVIÇO',qtd:Number(i.quantidade||i.qtd||1),valor:Number(i.valor_total||i.valorTotal||i.total||0)};
  }

  async function buscar(ini,fim){
    if(typeof CloudDB!=='undefined'&&CloudDB&&typeof empresaAtual!=='undefined'&&empresaAtual?.cloud&&empresaAtual?.id){
      try{
        const aRes=await CloudDB.from('atendimentos').select('id,data').eq('empresa_id',empresaAtual.id).gte('data',ini).lte('data',fim);
        if(aRes.error)throw aRes.error;
        const ids=(aRes.data||[]).map(x=>x.id);
        if(!ids.length)return [];
        const iRes=await CloudDB.from('itens_atendimento').select('atendimento_id,tipo,nome,quantidade,valor_total').eq('empresa_id',empresaAtual.id).in('atendimento_id',ids);
        if(iRes.error)throw iRes.error;
        return (iRes.data||[]).map(normalizarItem).filter(i=>i.tipo==='SERVICO'||i.tipo==='SERVIÇO');
      }catch(e){console.warn('Dashboard servicos v49: fallback local',e)}
    }
    const ent=(typeof entradas!=='undefined'&&Array.isArray(entradas))?entradas:[];
    const itens=[];
    ent.filter(e=>e.data&&e.data>=ini&&e.data<=fim).forEach(e=>{
      const lista=Array.isArray(e.itens)?e.itens:[];
      lista.forEach(i=>{const n=normalizarItem(i);if(n.tipo==='SERVICO'||n.tipo==='SERVIÇO')itens.push(n)});
    });
    return itens;
  }

  async function atualizar(){
    aplicarAcessoAdmin();
    if(!admin()||!garantir()||typeof obterIntervalosDashboard!=='function')return;
    const {ini,fim}=obterIntervalosDashboard();
    const itens=await buscar(ini,fim);
    const mapa=new Map();
    itens.forEach(i=>{
      const k=String(i.nome||'SERVIÇO').trim().toUpperCase()||'SERVIÇO';
      if(!mapa.has(k))mapa.set(k,{nome:k,qtd:0,fat:0});
      const x=mapa.get(k);x.qtd+=Number(i.qtd||1);x.fat+=Number(i.valor||0);
    });
    const rows=[...mapa.values()].sort((a,b)=>b.fat-a.fat||b.qtd-a.qtd||a.nome.localeCompare(b.nome,'pt-BR'));
    const total=rows.reduce((s,x)=>s+x.fat,0);
    const body=document.getElementById('dash-serv-v49-body');if(!body)return;
    if(!rows.length){body.innerHTML='<tr><td colspan="5" class="dash-serv-v49-vazio">Nenhum serviço concluído no período.</td></tr>';return}
    body.innerHTML=rows.map(x=>{
      const ticket=x.qtd?x.fat/x.qtd:0,part=total?x.fat/total*100:0;
      return `<tr><td>${esc(x.nome)}</td><td>${x.qtd}</td><td class="valor">${moeda(x.fat)}</td><td>${moeda(ticket)}</td><td><span class="dash-serv-v49-barra"><i style="width:${Math.min(100,part).toFixed(1)}%"></i></span>${part.toFixed(1)}%</td></tr>`;
    }).join('');
  }

  function instalar(){
    aplicarAcessoAdmin();garantir();
    if(typeof mudarTela==='function'&&!mudarTela.__adminDashboardV49){
      const anterior=mudarTela;
      const w=function(tela){if(String(tela)==='dashboard'&&!admin()){aplicarAcessoAdmin();return false}return anterior.apply(this,arguments)};
      w.__adminDashboardV49=true;window.mudarTela=w;try{mudarTela=w}catch(_){}
    }
    if(typeof aplicarPermissoesPerfil==='function'&&!aplicarPermissoesPerfil.__adminDashboardV49){
      const anteriorP=aplicarPermissoesPerfil;
      const wp=function(){const r=anteriorP.apply(this,arguments);Promise.resolve().then(aplicarAcessoAdmin);return r};
      wp.__adminDashboardV49=true;window.aplicarPermissoesPerfil=wp;try{aplicarPermissoesPerfil=wp}catch(_){}
    }
    if(typeof renderizarDashboard==='function'&&!renderizarDashboard.__v49){
      const anteriorR=renderizarDashboard;
      const wr=function(){if(!admin())return;const r=anteriorR.apply(this,arguments);Promise.resolve(r).finally(()=>atualizar());return r};
      wr.__v49=true;window.renderizarDashboard=wr;try{renderizarDashboard=wr}catch(_){}
    }
    if(admin())setTimeout(atualizar,0);
  }
  if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',()=>setTimeout(instalar,2050));else setTimeout(instalar,2050);
})();
</script>
'''

html=html.replace(marker,block+'\n'+marker,1)
idx.write_text(html,encoding='utf-8')

swtxt=sw.read_text(encoding='utf-8')
swtxt,n=re.subn(r"const CACHE_VERSION = '[^']+';","const CACHE_VERSION = 'simpla-shell-v49-dashboard-servicos-admin';",swtxt,count=1)
if n!=1:raise SystemExit('cache version nao encontrada')
sw.write_text(swtxt,encoding='utf-8')
