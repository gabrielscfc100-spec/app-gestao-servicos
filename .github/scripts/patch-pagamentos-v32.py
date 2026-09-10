from pathlib import Path

p = Path('index.html')
s = p.read_text(encoding='utf-8')

anchor = """            const totalVal = carrinho.reduce((acc, i) => acc + Number(i.preco || 0), 0);\n            if(pagamentoVal === 'DIVIDIDO') {\n                try { pagamentoVal = montarPagamentoDividido(totalVal); }\n                catch(err) { alert(err.message); return; }\n            }\n"""
replacement = anchor + """            let pagamentosDetalhadosV32 = null;\n            try {\n                if(typeof montarPagamentosDetalhadosV32 === 'function') pagamentosDetalhadosV32 = montarPagamentosDetalhadosV32(totalVal);\n            } catch(err) {\n                alert(err.message || 'Revise as formas de pagamento.');\n                return;\n            }\n"""
assert anchor in s, 'ponto de captura dos pagamentos nao encontrado'
s = s.replace(anchor, replacement, 1)

anchor2 = """                    novaEntrada = entradaCloudParaLocal(at, itensSalvos || []);\n"""
replacement2 = """                    if(Array.isArray(pagamentosDetalhadosV32) && pagamentosDetalhadosV32.length) {\n                        const pagamentosPayload = pagamentosDetalhadosV32.map(pg => ({\n                            empresa_id: empresaAtual.id,\n                            atendimento_id: at.id,\n                            forma: pg.forma,\n                            valor: Number(pg.valor || 0),\n                            valor_recebido: pg.valorRecebido == null ? null : Number(pg.valorRecebido),\n                            troco: pg.troco == null ? null : Number(pg.troco)\n                        }));\n                        const { error: pagamentosErro } = await CloudDB.from('pagamentos_atendimento').insert(pagamentosPayload);\n                        if(pagamentosErro) throw pagamentosErro;\n                    }\n                    novaEntrada = entradaCloudParaLocal(at, itensSalvos || []);\n"""
assert anchor2 in s, 'ponto de persistencia do atendimento nao encontrado'
s = s.replace(anchor2, replacement2, 1)

addon = r'''
<style id="simpla-pagamentos-v32">
#pagamento-dinheiro-v32{display:none;margin-top:10px;padding:12px;border:1px solid #dbe4ee;border-radius:8px;background:#f8fafc;text-transform:none}
#pagamento-dinheiro-v32 *{text-transform:none}
#pagamento-dinheiro-v32 .dinheiro-grid-v32{display:grid;grid-template-columns:1fr 1fr;gap:10px}
#pagamento-dinheiro-v32 label{display:block;font-size:12px;font-weight:700;color:#4a5568;margin-bottom:5px}
#pagamento-dinheiro-v32 input{width:100%;min-height:42px}
#pagamento-troco-v32{margin-top:9px;font-size:13px;font-weight:700;color:#2d3748}
@media(max-width:768px){#pagamento-dinheiro-v32 .dinheiro-grid-v32{grid-template-columns:1fr}}
</style>
<script id="simpla-pagamentos-v32-script">
(function(){
  function moeda(v){return Number(v||0).toLocaleString('pt-BR',{style:'currency',currency:'BRL'});}
  function garantirOpcao(sel, valor, texto){
    if(!sel || Array.from(sel.options).some(o=>o.value===valor || o.textContent.trim()===texto)) return;
    const o=document.createElement('option');o.value=valor;o.textContent=texto;sel.appendChild(o);
  }
  function totalAtual(){try{return typeof totalCarrinhoAtual==='function'?Number(totalCarrinhoAtual()||0):0;}catch(_){return 0;}}
  function valorDinheiroDevido(){
    const principal=document.getElementById('pag-entrada'); if(!principal) return 0;
    if(principal.value==='DINHEIRO') return totalAtual();
    if(principal.value!=='DIVIDIDO') return 0;
    let soma=0;
    for(const n of [1,2]){
      const f=document.getElementById('pag-div-forma-'+n)?.value;
      const v=Number(document.getElementById('pag-div-valor-'+n)?.value||0);
      if(f==='DINHEIRO') soma+=v;
    }
    return soma;
  }
  function atualizarDinheiro(){
    const box=document.getElementById('pagamento-dinheiro-v32'); if(!box) return;
    const devido=valorDinheiroDevido();
    box.style.display=devido>0?'block':'none';
    const devidoEl=document.getElementById('pag-dinheiro-devido-v32'); if(devidoEl) devidoEl.value=devido.toFixed(2);
    const recebido=Number(document.getElementById('pag-dinheiro-recebido-v32')?.value||0);
    const troco=Math.max(0,recebido-devido);
    const r=document.getElementById('pagamento-troco-v32');
    if(r) r.textContent=recebido>0 ? (recebido<devido ? 'Valor recebido insuficiente: faltam '+moeda(devido-recebido) : 'Troco: '+moeda(troco)) : 'Informe quanto foi recebido em dinheiro para calcular o troco.';
  }
  function montarUI(){
    const principal=document.getElementById('pag-entrada'); if(!principal) return;
    garantirOpcao(principal,'TRANSFERÊNCIA','TRANSFERÊNCIA');
    garantirOpcao(principal,'OUTRO','OUTRO');
    for(const n of [1,2]){
      const sel=document.getElementById('pag-div-forma-'+n);
      garantirOpcao(sel,'TRANSFERÊNCIA','TRANSFERÊNCIA');
      garantirOpcao(sel,'OUTRO','OUTRO');
    }
    if(!document.getElementById('pagamento-dinheiro-v32')){
      const box=document.createElement('div');box.id='pagamento-dinheiro-v32';
      box.innerHTML='<div class="dinheiro-grid-v32"><div><label>Valor devido em dinheiro</label><input id="pag-dinheiro-devido-v32" type="number" step="0.01" readonly></div><div><label>Valor recebido</label><input id="pag-dinheiro-recebido-v32" type="number" min="0" step="0.01" placeholder="R$ 0,00"></div></div><div id="pagamento-troco-v32">Informe quanto foi recebido em dinheiro para calcular o troco.</div>';
      const split=document.getElementById('pagamento-dividido-box');
      (split?.parentElement || principal.parentElement)?.appendChild(box);
      document.getElementById('pag-dinheiro-recebido-v32')?.addEventListener('input',atualizarDinheiro);
    }
    atualizarDinheiro();
  }
  window.montarPagamentosDetalhadosV32=function(total){
    montarUI();
    const principal=document.getElementById('pag-entrada')?.value||'';
    const pagamentos=[];
    if(principal==='DIVIDIDO'){
      const f1=document.getElementById('pag-div-forma-1')?.value||'';
      const f2=document.getElementById('pag-div-forma-2')?.value||'';
      const v1=Number(document.getElementById('pag-div-valor-1')?.value||0);
      const v2=Number(document.getElementById('pag-div-valor-2')?.value||0);
      if(!f1||!f2||f1===f2) throw new Error('Escolha duas formas de pagamento diferentes.');
      if(v1<=0||v2<=0) throw new Error('Informe valores maiores que zero para as duas formas de pagamento.');
      if(Math.abs((v1+v2)-Number(total||0))>=0.01) throw new Error('A soma do pagamento dividido deve ser igual ao total do atendimento.');
      pagamentos.push({forma:f1,valor:v1},{forma:f2,valor:v2});
    }else{
      if(!principal) throw new Error('Selecione a forma de pagamento.');
      pagamentos.push({forma:principal,valor:Number(total||0)});
    }
    const cashDue=pagamentos.filter(p=>p.forma==='DINHEIRO').reduce((a,p)=>a+Number(p.valor||0),0);
    if(cashDue>0){
      const recebido=Number(document.getElementById('pag-dinheiro-recebido-v32')?.value||0);
      if(recebido<=0) throw new Error('Informe o valor recebido em dinheiro.');
      if(recebido+0.009<cashDue) throw new Error('O valor recebido em dinheiro é menor que o valor devido.');
      let restanteRecebido=recebido;
      pagamentos.forEach(p=>{
        if(p.forma!=='DINHEIRO') return;
        p.valorRecebido=restanteRecebido;
        p.troco=Math.max(0,restanteRecebido-p.valor);
        restanteRecebido=0;
      });
    }
    return pagamentos;
  };
  document.addEventListener('change',e=>{if(['pag-entrada','pag-div-forma-1','pag-div-forma-2'].includes(e.target?.id)){montarUI();atualizarDinheiro();}});
  document.addEventListener('input',e=>{if(['pag-div-valor-1','pag-div-valor-2'].includes(e.target?.id)) atualizarDinheiro();});
  document.addEventListener('DOMContentLoaded',montarUI);
  setTimeout(montarUI,900);
})();
</script>
'''
assert '</body>' in s, 'body final nao encontrado'
s = s.replace('</body>', addon + '\n</body>', 1)
p.write_text(s, encoding='utf-8')
print('v32 aplicado')
