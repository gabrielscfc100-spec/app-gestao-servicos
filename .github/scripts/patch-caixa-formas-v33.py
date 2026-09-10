from pathlib import Path

p=Path('index.html')
s=p.read_text(encoding='utf-8')
marker='simpla-caixa-formas-v33'
if marker in s:
    print('v33 already applied')
    raise SystemExit(0)

payload=r'''
<style id="simpla-caixa-formas-v33">
#caixa-formas-v33{margin-top:18px;background:#fff;border:1px solid #e2e8f0;border-radius:10px;padding:18px}
#caixa-formas-v33 h3{margin:0 0 4px;font-size:16px;color:#1f2937}
#caixa-formas-v33 .sub{margin:0 0 14px;color:#718096;font-size:13px;text-transform:none}
.caixa-formas-grid-v33{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:10px}
.caixa-forma-card-v33{border:1px solid #e2e8f0;border-radius:9px;padding:13px;background:#f8fafc;min-width:0}
.caixa-forma-card-v33 .rotulo{display:block;font-size:11px;font-weight:700;color:#64748b;margin-bottom:6px;overflow-wrap:anywhere}
.caixa-forma-card-v33 strong{display:block;font-size:18px;color:#1f2937;margin-bottom:4px}
.caixa-forma-card-v33 small{display:block;color:#718096;font-size:11px;text-transform:none}
#caixa-formas-status-v33{margin-top:10px;font-size:11px;color:#718096;text-transform:none}
@media(max-width:768px){
  #caixa-formas-v33{padding:14px;margin-top:14px}
  .caixa-formas-grid-v33{grid-template-columns:repeat(2,minmax(0,1fr));gap:8px}
  .caixa-forma-card-v33{padding:11px}
  .caixa-forma-card-v33 strong{font-size:16px}
}
</style>
<script id="simpla-caixa-formas-v33-script">
(function(){
  const formas=[
    ['PIX','Pix'],['DINHEIRO','Dinheiro'],['CREDITO','Cartão de crédito'],
    ['DEBITO','Cartão de débito'],['TRANSFERENCIA','Transferência'],['OUTRO','Outros']
  ];
  const moeda=v=>Number(v||0).toLocaleString('pt-BR',{style:'currency',currency:'BRL'});
  const semAcento=v=>String(v||'').normalize('NFD').replace(/[\u0300-\u036f]/g,'').toUpperCase();
  function cat(forma){
    const f=semAcento(forma);
    if(f.includes('PIX')) return 'PIX';
    if(f.includes('DINHEIRO')) return 'DINHEIRO';
    if(f.includes('CREDITO')) return 'CREDITO';
    if(f.includes('DEBITO')) return 'DEBITO';
    if(f.includes('TRANSFER')) return 'TRANSFERENCIA';
    return 'OUTRO';
  }
  function empresa(){
    try{ if(typeof empresaAtual!=='undefined' && empresaAtual?.id) return empresaAtual; }catch(_){ }
    return window.empresaAtual||null;
  }
  function receitasData(data){
    try{
      if(typeof entradas==='undefined' || !Array.isArray(entradas)) return [];
      return entradas.filter(e=>String(e?.data||'')===String(data||''));
    }catch(_){ return []; }
  }
  function decomporLegado(e){
    try{ if(typeof decomporPagamentoCaixa==='function') return decomporPagamentoCaixa(e); }catch(_){ }
    const raw=String(e?.pagamento||'');
    if(raw.startsWith('DIVIDIDO|')) return raw.split('|').slice(1).map(parte=>{
      const pos=parte.lastIndexOf(':'); return {forma:parte.slice(0,pos),valor:Number(parte.slice(pos+1)||0)};
    }).filter(x=>x.valor>0);
    return [{forma:raw||'OUTRO',valor:Number(e?.total||0)}];
  }
  function montar(){
    if(document.getElementById('caixa-formas-v33')) return document.getElementById('caixa-formas-v33');
    const ancora=document.getElementById('caixa-total-pix');
    if(!ancora) return null;
    let base=ancora.closest('.section-box-cfg')||ancora.closest('.form-container')||ancora.parentElement?.parentElement?.parentElement;
    if(!base) return null;
    const box=document.createElement('div'); box.id='caixa-formas-v33';
    box.innerHTML='<h3>Recebimentos por forma de pagamento</h3><p class="sub">Distribuição dos recebimentos do dia selecionado.</p><div class="caixa-formas-grid-v33">'+formas.map(([k,n])=>'<div class="caixa-forma-card-v33"><span class="rotulo">'+n+'</span><strong id="caixa-v33-'+k+'">R$ 0,00</strong><small id="caixa-v33-'+k+'-meta">0 lançamentos · 0%</small></div>').join('')+'</div><div id="caixa-formas-status-v33"></div>';
    base.insertAdjacentElement('afterend',box);
    return box;
  }
  async function atualizar(){
    const box=montar(); if(!box) return;
    const data=document.getElementById('filtro-caixa-data')?.value||'';
    const receitas=receitasData(data);
    const ids=receitas.map(e=>e?.cloudId||e?.id).filter(Boolean).map(String);
    const normalizados={};
    let usouBanco=false;
    try{
      const emp=empresa();
      const db=(typeof CloudDB!=='undefined'?CloudDB:null);
      if(db && emp?.id && ids.length){
        const {data:rows,error}=await db.from('pagamentos_atendimento').select('atendimento_id,forma,valor,valor_recebido,troco').eq('empresa_id',emp.id).in('atendimento_id',ids);
        if(error) throw error;
        (rows||[]).forEach(r=>(normalizados[String(r.atendimento_id)] ||= []).push(r));
        usouBanco=true;
      }
    }catch(e){ console.warn('SimplA v33: fallback de pagamentos',e); }
    const parcelas=[];
    receitas.forEach(e=>{
      const id=String(e?.cloudId||e?.id||'');
      const rows=normalizados[id];
      if(rows?.length) rows.forEach(r=>parcelas.push({forma:r.forma,valor:Number(r.valor||0)}));
      else decomporLegado(e).forEach(r=>parcelas.push({forma:r.forma,valor:Number(r.valor||0)}));
    });
    const totais={PIX:0,DINHEIRO:0,CREDITO:0,DEBITO:0,TRANSFERENCIA:0,OUTRO:0};
    const cont={PIX:0,DINHEIRO:0,CREDITO:0,DEBITO:0,TRANSFERENCIA:0,OUTRO:0};
    parcelas.forEach(p=>{const c=cat(p.forma);totais[c]+=Number(p.valor||0);cont[c]++;});
    const geral=Object.values(totais).reduce((a,b)=>a+b,0);
    formas.forEach(([k])=>{
      const el=document.getElementById('caixa-v33-'+k); if(el) el.textContent=moeda(totais[k]);
      const meta=document.getElementById('caixa-v33-'+k+'-meta');
      if(meta) meta.textContent=cont[k]+' '+(cont[k]===1?'lançamento':'lançamentos')+' · '+(geral>0?(totais[k]/geral*100).toFixed(1).replace('.',','):'0')+'%';
    });
    const st=document.getElementById('caixa-formas-status-v33');
    if(st) st.textContent=receitas.length ? (usouBanco?'Dados consolidados pelas formas de pagamento registradas.':'Exibindo dados compatíveis com os registros existentes.') : 'Nenhum recebimento na data selecionada.';
  }
  const original=window.renderizarCaixaFinanceiro;
  if(typeof original==='function'){
    window.renderizarCaixaFinanceiro=function(){ const r=original.apply(this,arguments); Promise.resolve(r).finally(()=>setTimeout(atualizar,0)); return r; };
  }
  document.addEventListener('change',e=>{ if(e.target?.id==='filtro-caixa-data') setTimeout(atualizar,0); });
  document.addEventListener('click',()=>setTimeout(()=>{ if(document.getElementById('filtro-caixa-data')) atualizar(); },50));
  setTimeout(atualizar,700);
})();
</script>
'''

if '</body>' not in s:
    raise SystemExit('body close not found')
s=s.replace('</body>',payload+'\n</body>',1)
p.write_text(s,encoding='utf-8')
print('applied v33')
