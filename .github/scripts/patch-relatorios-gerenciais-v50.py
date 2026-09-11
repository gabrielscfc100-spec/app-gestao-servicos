from pathlib import Path
import re

idx=Path('index.html')
sw=Path('service-worker.js')
html=idx.read_text(encoding='utf-8')

if 'simpla-relatorios-gerenciais-v50' in html:
    raise SystemExit('v50 ja aplicada')
marker='</body>'
if marker not in html:
    raise SystemExit('body nao encontrado')

block=r'''
<style id="simpla-relatorios-gerenciais-v50-css">
  .dash-rel-v50{margin:0 0 24px;background:#fff;border:1px solid #e2e8f0;border-radius:10px;padding:16px;box-shadow:0 2px 4px rgba(0,0,0,.04)}
  .dash-rel-v50-head{display:flex;justify-content:space-between;align-items:flex-start;gap:12px;flex-wrap:wrap;margin-bottom:12px}
  .dash-rel-v50-head h3{margin:0;font-size:15px;color:#1a1c23}
  .dash-rel-v50-head p{margin:4px 0 0;font-size:11px;color:#718096;text-transform:none}
  .dash-rel-v50-actions{display:flex;gap:8px;flex-wrap:wrap}
  .dash-rel-v50-actions button{padding:8px 11px;border-radius:6px;border:1px solid #cbd5e0;background:#fff;cursor:pointer;font-size:10px;font-weight:800;color:#2d3748}
  .dash-rel-v50-actions button.primary{background:#1a1c23;color:#fff;border-color:#1a1c23}
  .dash-rel-v50-grid{display:grid;grid-template-columns:repeat(6,minmax(0,1fr));gap:9px;margin-bottom:14px}
  .dash-rel-v50-kpi{padding:10px;border:1px solid #e2e8f0;border-radius:8px;background:#f8fafc}
  .dash-rel-v50-kpi span{display:block;font-size:8px;font-weight:900;color:#718096;margin-bottom:4px}
  .dash-rel-v50-kpi strong{font-size:15px;color:#1a1c23}
  .dash-rel-v50-meta{font-size:10px;color:#718096;text-transform:none;border-top:1px solid #edf2f7;padding-top:10px;line-height:1.5}
  @media(max-width:1100px){.dash-rel-v50-grid{grid-template-columns:repeat(3,minmax(0,1fr))}}
  @media(max-width:600px){.dash-rel-v50-grid{grid-template-columns:1fr 1fr}.dash-rel-v50{padding:12px}.dash-rel-v50-actions{width:100%}.dash-rel-v50-actions button{flex:1}}
</style>
<script id="simpla-relatorios-gerenciais-v50">
(function(){
  function admin(){try{return typeof obterPerfilAtual==='function'&&String(obterPerfilAtual()).toUpperCase()==='ADMIN'}catch(_){return false}}
  function texto(id,def='0'){return String(document.getElementById(id)?.textContent||def).trim()}
  function moeda(v){return Number(v||0).toLocaleString('pt-BR',{style:'currency',currency:'BRL'})}
  function valorMoeda(t){const s=String(t||'').replace(/[^0-9,.-]/g,'').replace(/\./g,'').replace(',','.');return Number(s)||0}
  function garantir(){
    if(!admin())return null;
    const dash=document.getElementById('dashboard');if(!dash)return null;
    let box=document.getElementById('dash-rel-v50');if(box)return box;
    box=document.createElement('div');box.id='dash-rel-v50';box.className='dash-rel-v50';
    box.innerHTML=`<div class="dash-rel-v50-head"><div><h3>Central de Relatórios Gerenciais</h3><p>Consolidação do período selecionado no Dashboard, com exportação em Excel e PDF.</p></div><div class="dash-rel-v50-actions"><button onclick="atualizarRelatorioGerencialV50()">Atualizar</button><button class="primary" onclick="exportarRelatorioGerencialExcelV50()">Exportar Excel</button><button class="primary" onclick="exportarRelatorioGerencialPDFV50()">Gerar PDF</button></div></div><div class="dash-rel-v50-grid">
      <div class="dash-rel-v50-kpi"><span>FATURAMENTO</span><strong id="dash-rel-v50-fat">R$ 0,00</strong></div>
      <div class="dash-rel-v50-kpi"><span>LUCRO LÍQUIDO</span><strong id="dash-rel-v50-lucro">R$ 0,00</strong></div>
      <div class="dash-rel-v50-kpi"><span>ATENDIMENTOS</span><strong id="dash-rel-v50-at">0</strong></div>
      <div class="dash-rel-v50-kpi"><span>AGENDAMENTOS</span><strong id="dash-rel-v50-ag">0</strong></div>
      <div class="dash-rel-v50-kpi"><span>NÃO COMPARECEU</span><strong id="dash-rel-v50-no">0</strong></div>
      <div class="dash-rel-v50-kpi"><span>TAXA NO-SHOW</span><strong id="dash-rel-v50-taxa">0%</strong></div>
    </div><div class="dash-rel-v50-meta" id="dash-rel-v50-meta">Relatório ainda não atualizado.</div>`;
    const serv=document.getElementById('dash-serv-v49');
    if(serv)serv.insertAdjacentElement('afterend',box);else dash.appendChild(box);
    return box;
  }
  function dados(){
    return {
      periodo:texto('dash-periodo-label','Período não informado'),
      faturamento:texto('dash-faturamento','R$ 0,00'),
      despesas:texto('dash-despesas','R$ 0,00'),
      lucro:texto('dash-lucro','R$ 0,00'),
      atendimentos:texto('dash-atendimentos','0'),
      ticket:texto('dash-ticket','R$ 0,00'),
      novos:texto('dash-novos-clientes','0'),
      agendamentos:texto('dash-ag-v47-total','0'),
      concluidos:texto('dash-ag-v47-concl','0'),
      cancelados:texto('dash-ag-v47-canc','0'),
      noshow:texto('dash-ag-v47-noshow','0'),
      taxaNo:texto('dash-ag-v47-taxa-no','0%'),
      taxaComp:texto('dash-ag-v47-taxa-comp','0%')
    };
  }
  function tabela(id){
    const t=document.querySelector(id);if(!t)return [];
    return [...t.querySelectorAll('tr')].map(tr=>[...tr.querySelectorAll('th,td')].map(td=>String(td.textContent||'').replace(/\s+/g,' ').trim())).filter(r=>r.length&&r.some(Boolean));
  }
  async function atualizar(){
    if(!admin()||!garantir())return;
    if(typeof renderizarDashboard==='function')try{renderizarDashboard()}catch(_){}
    await new Promise(r=>setTimeout(r,120));
    const d=dados();
    const set=(id,v)=>{const e=document.getElementById(id);if(e)e.textContent=v};
    set('dash-rel-v50-fat',d.faturamento);set('dash-rel-v50-lucro',d.lucro);set('dash-rel-v50-at',d.atendimentos);set('dash-rel-v50-ag',d.agendamentos);set('dash-rel-v50-no',d.noshow);set('dash-rel-v50-taxa',d.taxaNo);
    set('dash-rel-v50-meta',`Período: ${d.periodo} · Atualizado em ${new Date().toLocaleString('pt-BR')}. Os dados refletem os registros disponíveis no SimplA para o período selecionado.`);
  }
  window.atualizarRelatorioGerencialV50=atualizar;
  window.exportarRelatorioGerencialExcelV50=async function(){
    if(!admin())return;await atualizar();
    if(typeof XLSX==='undefined'){alert('Biblioteca de Excel indisponível.');return}
    const d=dados(),wb=XLSX.utils.book_new();
    const resumo=[['RELATÓRIO GERENCIAL SIMPLA'],['PERÍODO',d.periodo],[],['INDICADOR','VALOR'],['Faturamento',d.faturamento],['Despesas efetivas',d.despesas],['Lucro líquido',d.lucro],['Atendimentos',d.atendimentos],['Ticket médio',d.ticket],['Novos clientes',d.novos],['Agendamentos',d.agendamentos],['Concluídos',d.concluidos],['Cancelados',d.cancelados],['Não compareceu',d.noshow],['Taxa de no-show',d.taxaNo],['Taxa de comparecimento',d.taxaComp]];
    XLSX.utils.book_append_sheet(wb,XLSX.utils.aoa_to_sheet(resumo),'Resumo');
    const prof=tabela('#dash-prof-v48 table');if(prof.length)XLSX.utils.book_append_sheet(wb,XLSX.utils.aoa_to_sheet(prof),'Profissionais');
    const serv=tabela('#dash-serv-v49 table');if(serv.length)XLSX.utils.book_append_sheet(wb,XLSX.utils.aoa_to_sheet(serv),'Serviços');
    XLSX.writeFile(wb,`Relatorio_Gerencial_SimplA_${new Date().toISOString().slice(0,10)}.xlsx`);
  };
  window.exportarRelatorioGerencialPDFV50=async function(){
    if(!admin())return;await atualizar();
    if(!window.jspdf?.jsPDF){alert('Biblioteca de PDF indisponível.');return}
    const {jsPDF}=window.jspdf,doc=new jsPDF(),d=dados();let y=16;
    const linha=(txt,size=10,bold=false)=>{if(y>282){doc.addPage();y=16}doc.setFontSize(size);doc.setFont(undefined,bold?'bold':'normal');const parts=doc.splitTextToSize(String(txt),180);doc.text(parts,15,y);y+=parts.length*(size*0.42)+3};
    linha('RELATÓRIO GERENCIAL SIMPLA',16,true);linha(`Período: ${d.periodo}`,9);y+=2;
    [['Faturamento',d.faturamento],['Despesas efetivas',d.despesas],['Lucro líquido',d.lucro],['Atendimentos',d.atendimentos],['Ticket médio',d.ticket],['Novos clientes',d.novos],['Agendamentos',d.agendamentos],['Concluídos',d.concluidos],['Cancelados',d.cancelados],['Não compareceu',d.noshow],['Taxa de no-show',d.taxaNo],['Taxa de comparecimento',d.taxaComp]].forEach(([a,b])=>linha(`${a}: ${b}`,10,a==='Faturamento'||a==='Lucro líquido'));
    const adicionarTabela=(titulo,rows)=>{if(!rows.length)return;y+=4;linha(titulo,12,true);rows.slice(0,25).forEach((r,i)=>linha((i===0?'':`${i}. `)+r.join(' | '),8,i===0));if(rows.length>25)linha(`... e mais ${rows.length-25} linhas. Consulte o Excel para o detalhamento completo.`,8)};
    adicionarTabela('DESEMPENHO POR PROFISSIONAL',tabela('#dash-prof-v48 table'));
    adicionarTabela('DESEMPENHO POR SERVIÇO',tabela('#dash-serv-v49 table'));
    doc.save(`Relatorio_Gerencial_SimplA_${new Date().toISOString().slice(0,10)}.pdf`);
  };
  function instalar(){if(!admin())return;garantir();setTimeout(atualizar,0)}
  if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',()=>setTimeout(instalar,2150));else setTimeout(instalar,2150);
})();
</script>
'''
html=html.replace(marker,block+'\n'+marker,1)
idx.write_text(html,encoding='utf-8')

swtxt=sw.read_text(encoding='utf-8')
swtxt,n=re.subn(r"const CACHE_VERSION = '[^']+';","const CACHE_VERSION = 'simpla-shell-v50-relatorios-gerenciais';",swtxt,count=1)
if n!=1:raise SystemExit('cache version nao encontrada')
sw.write_text(swtxt,encoding='utf-8')
