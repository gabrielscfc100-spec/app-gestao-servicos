from pathlib import Path
p=Path('index.html')
s=p.read_text(encoding='utf-8')
marker='simpla-relatorio-formas-v34'
if marker in s:
    raise SystemExit('v34 ja aplicada')
bloco=r'''

<style id="simpla-relatorio-formas-v34">
#relatorio-formas-v34{margin-top:18px;background:#fff;border:1px solid #e2e8f0;border-radius:10px;padding:18px}
#relatorio-formas-v34 h3{margin:0 0 4px;font-size:16px;color:#1f2937}
#relatorio-formas-v34 .sub{margin:0 0 14px;color:#718096;font-size:13px;text-transform:none}
.rel-formas-filtros-v34{display:grid;grid-template-columns:1fr 1fr auto auto;gap:10px;align-items:end;margin-bottom:14px}
.rel-formas-filtros-v34 label{display:block;font-size:11px;font-weight:700;color:#64748b;margin-bottom:5px}
.rel-formas-filtros-v34 input{width:100%;padding:10px;border:1px solid #cbd5e0;border-radius:6px}
.rel-formas-filtros-v34 button{height:40px;padding:0 14px;border:0;border-radius:6px;font-weight:700;cursor:pointer}
#rel-formas-aplicar-v34{background:#1a1c23;color:#fff}
#rel-formas-exportar-v34{background:#edf2f7;color:#1f2937}
.rel-formas-kpis-v34{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:10px;margin-bottom:14px}
.rel-formas-kpi-v34{background:#f8fafc;border:1px solid #e2e8f0;border-radius:8px;padding:12px}
.rel-formas-kpi-v34 span{display:block;font-size:10px;color:#718096;font-weight:700;margin-bottom:4px}
.rel-formas-kpi-v34 strong{font-size:17px;color:#1f2937}
.rel-formas-table-wrap-v34{overflow-x:auto}
#rel-formas-tabela-v34{width:100%;border-collapse:collapse;margin-top:0}
#rel-formas-tabela-v34 th,#rel-formas-tabela-v34 td{padding:10px;border-bottom:1px solid #e2e8f0;font-size:12px;white-space:nowrap}
#rel-formas-tabela-v34 th{background:#f8fafc;color:#4a5568;text-align:left}
#rel-formas-tabela-v34 td:nth-child(n+2),#rel-formas-tabela-v34 th:nth-child(n+2){text-align:right}
#rel-formas-status-v34{margin-top:10px;color:#718096;font-size:11px;text-transform:none}
@media(max-width:768px){
 #relatorio-formas-v34{padding:14px}
 .rel-formas-filtros-v34{grid-template-columns:1fr 1fr}
 .rel-formas-filtros-v34 button{width:100%}
 .rel-formas-kpis-v34{grid-template-columns:1fr}
}
</style>
<script id="simpla-relatorio-formas-v34-script">
(function(){
 const formas=[['PIX','Pix'],['DINHEIRO','Dinheiro'],['CREDITO','Cartão de crédito'],['DEBITO','Cartão de débito'],['TRANSFERENCIA','Transferência'],['OUTRO','Outros']];
 const moeda=v=>Number(v||0).toLocaleString('pt-BR',{style:'currency',currency:'BRL'});
 const norm=v=>String(v||'').normalize('NFD').replace(/[\u0300-\u036f]/g,'').toUpperCase().trim();
 function categoria(v){const x=norm(v);if(x==='PIX')return'PIX';if(x.includes('DINHEIRO'))return'DINHEIRO';if(x.includes('CREDITO'))return'CREDITO';if(x.includes('DEBITO'))return'DEBITO';if(x.includes('TRANSFER'))return'TRANSFERENCIA';return'OUTRO';}
 function empresa(){try{return (typeof empresaAtual!=='undefined'&&empresaAtual)||window.empresaAtual||null}catch(_){return window.empresaAtual||null}}
 function dataISO(e){const v=String(e?.data||e?.data_atendimento||'').slice(0,10);return /^\d{4}-\d{2}-\d{2}$/.test(v)?v:'';}
 function parserLegado(e){const raw=String(e?.pagamento||e?.formaPagamento||'').trim();if(raw.toUpperCase().startsWith('DIVIDIDO|'))return raw.split('|').slice(1).map(p=>{const i=p.lastIndexOf(':');return{forma:p.slice(0,i),valor:Number(p.slice(i+1)||0)}}).filter(x=>x.valor>0);return[{forma:raw||'OUTRO',valor:Number(e?.total||0)}];}
 function receitasPeriodo(i,f){const lista=(typeof entradas!=='undefined'&&Array.isArray(entradas))?entradas:[];return lista.filter(e=>{const d=dataISO(e);return d&&(!i||d>=i)&&(!f||d<=f);});}
 function montar(){
   if(document.getElementById('relatorio-formas-v34'))return document.getElementById('relatorio-formas-v34');
   const ancora=document.getElementById('caixa-formas-v33');if(!ancora)return null;
   const hoje=new Date(),ini=new Date(hoje.getFullYear(),hoje.getMonth(),1).toISOString().slice(0,10),fim=new Date(hoje.getFullYear(),hoje.getMonth()+1,0).toISOString().slice(0,10);
   const box=document.createElement('div');box.id='relatorio-formas-v34';
   box.innerHTML='<h3>Relatório por forma de pagamento</h3><p class="sub">Analise os recebimentos por período e exporte o consolidado.</p><div class="rel-formas-filtros-v34"><div><label>Data inicial</label><input type="date" id="rel-formas-inicio-v34" value="'+ini+'"></div><div><label>Data final</label><input type="date" id="rel-formas-fim-v34" value="'+fim+'"></div><button id="rel-formas-aplicar-v34">Atualizar</button><button id="rel-formas-exportar-v34">Exportar Excel</button></div><div class="rel-formas-kpis-v34"><div class="rel-formas-kpi-v34"><span>Total recebido</span><strong id="rel-formas-total-v34">R$ 0,00</strong></div><div class="rel-formas-kpi-v34"><span>Recebimentos</span><strong id="rel-formas-qtd-v34">0</strong></div><div class="rel-formas-kpi-v34"><span>Forma principal</span><strong id="rel-formas-principal-v34">-</strong></div></div><div class="rel-formas-table-wrap-v34"><table id="rel-formas-tabela-v34"><thead><tr><th>Forma</th><th>Valor</th><th>Lançamentos</th><th>Participação</th><th>Ticket médio</th></tr></thead><tbody></tbody></table></div><div id="rel-formas-status-v34"></div>';
   ancora.insertAdjacentElement('afterend',box);
   box.querySelector('#rel-formas-aplicar-v34').onclick=atualizar;
   box.querySelector('#rel-formas-exportar-v34').onclick=exportar;
   setTimeout(atualizar,100);
   return box;
 }
 let ultimo=[];
 async function dados(){
   const i=document.getElementById('rel-formas-inicio-v34')?.value||'',f=document.getElementById('rel-formas-fim-v34')?.value||'';
   const rec=receitasPeriodo(i,f), ids=rec.map(e=>String(e?.cloudId||e?.id||'')).filter(Boolean), normalizados={};
   let banco=false;
   try{const db=(typeof CloudDB!=='undefined'?CloudDB:null),emp=empresa();if(db&&emp?.id&&ids.length){const {data,error}=await db.from('pagamentos_atendimento').select('atendimento_id,forma,valor').eq('empresa_id',emp.id).in('atendimento_id',ids);if(error)throw error;(data||[]).forEach(r=>(normalizados[String(r.atendimento_id)]||=[]).push(r));banco=true;}}catch(e){console.warn('SimplA v34: fallback relatorio pagamentos',e)}
   const parcelas=[];rec.forEach(e=>{const id=String(e?.cloudId||e?.id||'');const ps=normalizados[id]?.length?normalizados[id]:parserLegado(e);ps.forEach(p=>parcelas.push({forma:categoria(p.forma),valor:Number(p.valor||0)}));});
   return {rec,parcelas,banco,i,f};
 }
 async function atualizar(){
   const box=montar();if(!box)return;
   const {rec,parcelas,banco,i,f}=await dados();const agg={};formas.forEach(([k,n])=>agg[k]={nome:n,valor:0,qtd:0});parcelas.forEach(p=>{const a=agg[p.forma]||agg.OUTRO;a.valor+=p.valor;a.qtd+=1;});
   const total=parcelas.reduce((a,p)=>a+p.valor,0);ultimo=formas.map(([k])=>({...agg[k],participacao:total?agg[k].valor/total:0,ticket:agg[k].qtd?agg[k].valor/agg[k].qtd:0}));
   document.getElementById('rel-formas-total-v34').textContent=moeda(total);document.getElementById('rel-formas-qtd-v34').textContent=String(rec.length);const principal=[...ultimo].sort((a,b)=>b.valor-a.valor)[0];document.getElementById('rel-formas-principal-v34').textContent=principal&&principal.valor>0?principal.nome:'-';
   box.querySelector('tbody').innerHTML=ultimo.map(x=>'<tr><td>'+x.nome+'</td><td>'+moeda(x.valor)+'</td><td>'+x.qtd+'</td><td>'+(x.participacao*100).toFixed(1)+'%</td><td>'+moeda(x.ticket)+'</td></tr>').join('');
   document.getElementById('rel-formas-status-v34').textContent='Período: '+(i||'-')+' a '+(f||'-')+' · '+(banco?'Pagamentos normalizados + compatibilidade histórica.':'Compatibilidade histórica/local.');
 }
 async function exportar(){
   await atualizar();const i=document.getElementById('rel-formas-inicio-v34')?.value||'',f=document.getElementById('rel-formas-fim-v34')?.value||'';
   const rows=ultimo.map(x=>({'Forma de pagamento':x.nome,'Valor recebido':Number(x.valor.toFixed(2)),'Lançamentos':x.qtd,'Participação (%)':Number((x.participacao*100).toFixed(2)),'Ticket médio':Number(x.ticket.toFixed(2))}));
   if(window.XLSX){const ws=XLSX.utils.json_to_sheet(rows),wb=XLSX.utils.book_new();XLSX.utils.book_append_sheet(wb,ws,'Formas de pagamento');XLSX.writeFile(wb,'relatorio_formas_pagamento_'+i+'_a_'+f+'.xlsx');return;}
   const csv=['Forma;Valor;Lançamentos;Participação;Ticket médio'].concat(rows.map(r=>[r['Forma de pagamento'],r['Valor recebido'],r['Lançamentos'],r['Participação (%)'],r['Ticket médio']].join(';'))).join('\n');const a=document.createElement('a');a.href=URL.createObjectURL(new Blob([csv],{type:'text/csv;charset=utf-8'}));a.download='relatorio_formas_pagamento_'+i+'_a_'+f+'.csv';a.click();URL.revokeObjectURL(a.href);
 }
 const original=window.renderizarCaixaFinanceiro;if(typeof original==='function'){window.renderizarCaixaFinanceiro=function(){const r=original.apply(this,arguments);setTimeout(()=>{montar();atualizar();},80);return r;};}
 document.addEventListener('DOMContentLoaded',()=>setTimeout(montar,1200));setTimeout(montar,1800);
})();
</script>
'''
idx=s.rfind('</body>')
if idx<0: raise SystemExit('body final nao encontrado')
s=s[:idx]+bloco+s[idx:]
p.write_text(s,encoding='utf-8')
print('v34 aplicada')
