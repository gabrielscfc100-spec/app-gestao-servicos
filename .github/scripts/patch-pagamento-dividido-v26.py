from pathlib import Path
p=Path('index.html')
s=p.read_text(encoding='utf-8')
old='''              <select id="pag-entrada">\n                <option>PIX</option>\n                <option>DINHEIRO</option>\n                <option>CARTÃO CRÉDITO</option>\n                <option>CARTÃO DÉBITO</option>\n              </select>'''
new='''              <select id="pag-entrada" onchange="atualizarPagamentoDivididoUI()">\n                <option>PIX</option>\n                <option>DINHEIRO</option>\n                <option>CARTÃO CRÉDITO</option>\n                <option>CARTÃO DÉBITO</option>\n                <option value="DIVIDIDO">PAGAMENTO DIVIDIDO</option>\n              </select>\n              <div id="pagamento-dividido-box" class="pagamento-dividido-box" style="display:none;">\n                <div class="pagamento-dividido-linha">\n                  <select id="pag-div-forma-1" onchange="atualizarResumoPagamentoDividido()">\n                    <option>PIX</option><option>DINHEIRO</option><option>CARTÃO CRÉDITO</option><option>CARTÃO DÉBITO</option>\n                  </select>\n                  <input type="number" id="pag-div-valor-1" min="0.01" step="0.01" placeholder="R$ 0,00" oninput="atualizarResumoPagamentoDividido()">\n                </div>\n                <div class="pagamento-dividido-linha">\n                  <select id="pag-div-forma-2" onchange="atualizarResumoPagamentoDividido()">\n                    <option>DINHEIRO</option><option>PIX</option><option>CARTÃO CRÉDITO</option><option>CARTÃO DÉBITO</option>\n                  </select>\n                  <input type="number" id="pag-div-valor-2" min="0.01" step="0.01" placeholder="R$ 0,00" oninput="atualizarResumoPagamentoDividido()">\n                </div>\n                <small id="pag-div-resumo">Informe duas formas de pagamento. A soma deve ser igual ao total do atendimento.</small>\n              </div>'''
assert old in s, 'bloco de pagamento nao encontrado'
s=s.replace(old,new,1)
marker='''        function localizarClienteUniversal(valor) {'''
helper=r'''        function atualizarPagamentoDivididoUI() {
            const sel = document.getElementById('pag-entrada');
            const box = document.getElementById('pagamento-dividido-box');
            if(!sel || !box) return;
            box.style.display = sel.value === 'DIVIDIDO' ? 'block' : 'none';
            atualizarResumoPagamentoDividido();
        }

        function totalCarrinhoAtual() {
            return carrinho.reduce((acc, i) => acc + Number(i.preco || 0), 0);
        }

        function atualizarResumoPagamentoDividido() {
            const box = document.getElementById('pagamento-dividido-box');
            const resumo = document.getElementById('pag-div-resumo');
            if(!box || box.style.display === 'none' || !resumo) return;
            const v1 = Number(document.getElementById('pag-div-valor-1')?.value || 0);
            const v2 = Number(document.getElementById('pag-div-valor-2')?.value || 0);
            const total = totalCarrinhoAtual();
            const soma = v1 + v2;
            const dif = total - soma;
            resumo.textContent = Math.abs(dif) < 0.01
                ? `Pagamento fechado em R$ ${soma.toFixed(2)}.`
                : `Informado: R$ ${soma.toFixed(2)} • Total do atendimento: R$ ${total.toFixed(2)} • Diferença: R$ ${dif.toFixed(2)}`;
        }

        function montarPagamentoDividido(total) {
            const f1 = document.getElementById('pag-div-forma-1')?.value || '';
            const f2 = document.getElementById('pag-div-forma-2')?.value || '';
            const v1 = Number(document.getElementById('pag-div-valor-1')?.value || 0);
            const v2 = Number(document.getElementById('pag-div-valor-2')?.value || 0);
            if(!f1 || !f2 || f1 === f2) throw new Error('Escolha duas formas de pagamento diferentes.');
            if(v1 <= 0 || v2 <= 0) throw new Error('Informe valores maiores que zero para as duas formas de pagamento.');
            if(Math.abs((v1 + v2) - total) >= 0.01) throw new Error('A soma do pagamento dividido deve ser igual ao total do atendimento.');
            return `DIVIDIDO|${f1}:${v1.toFixed(2)}|${f2}:${v2.toFixed(2)}`;
        }

        function formatarPagamentoAtendimento(valor) {
            const raw = String(valor || '');
            if(!raw.startsWith('DIVIDIDO|')) return raw;
            return raw.split('|').slice(1).map(parte => {
                const pos = parte.lastIndexOf(':');
                if(pos < 0) return parte;
                const forma = parte.slice(0,pos);
                const val = Number(parte.slice(pos+1) || 0);
                return `${forma} ${val.toLocaleString('pt-BR',{style:'currency',currency:'BRL'})}`;
            }).join(' + ');
        }

        function decomporPagamentoCaixa(entrada){
            const raw = String(entrada?.pagamento || '');
            if(!raw.startsWith('DIVIDIDO|')) return [{forma:normalizarFormaPagamentoCaixa(raw), valor:Number(entrada?.total||0)}];
            return raw.split('|').slice(1).map(parte=>{
                const pos=parte.lastIndexOf(':');
                return {forma:normalizarFormaPagamentoCaixa(parte.slice(0,pos)), valor:Number(parte.slice(pos+1)||0)};
            }).filter(x=>x.forma && x.valor>0);
        }

'''
assert marker in s, 'marker helper nao encontrado'
s=s.replace(marker,helper+marker,1)
old2="""            const pagamentoVal = document.getElementById('pag-entrada').value;"""
new2="""            let pagamentoVal = document.getElementById('pag-entrada').value;"""
assert old2 in s
s=s.replace(old2,new2,1)
needle="""            const totalVal = carrinho.reduce((acc, i) => acc + Number(i.preco || 0), 0);"""
repl=needle+"""\n            if(pagamentoVal === 'DIVIDIDO') {\n                try { pagamentoVal = montarPagamentoDividido(totalVal); }\n                catch(err) { alert(err.message); return; }\n            }"""
assert needle in s
s=s.replace(needle,repl,1)
old3="""<td>${e.pagamento}</td>"""
new3="""<td>${formatarPagamentoAtendimento(e.pagamento)}</td>"""
assert old3 in s
s=s.replace(old3,new3,1)
# caixa totals
old4="""            const totalDinheiro = receitasDia.filter(e=>normalizarFormaPagamentoCaixa(e.pagamento)==='DINHEIRO').reduce((a,e)=>a+Number(e.total||0),0);\n            const totalPix = receitasDia.filter(e=>normalizarFormaPagamentoCaixa(e.pagamento)==='PIX').reduce((a,e)=>a+Number(e.total||0),0);\n            const totalCredito = receitasDia.filter(e=>normalizarFormaPagamentoCaixa(e.pagamento).includes('CRÉDITO') || normalizarFormaPagamentoCaixa(e.pagamento).includes('CREDITO')).reduce((a,e)=>a+Number(e.total||0),0);\n            const totalDebito = receitasDia.filter(e=>normalizarFormaPagamentoCaixa(e.pagamento).includes('DÉBITO') || normalizarFormaPagamentoCaixa(e.pagamento).includes('DEBITO')).reduce((a,e)=>a+Number(e.total||0),0);"""
new4="""            const parcelasPagamento = receitasDia.flatMap(decomporPagamentoCaixa);\n            const totalDinheiro = parcelasPagamento.filter(x=>x.forma==='DINHEIRO').reduce((a,x)=>a+Number(x.valor||0),0);\n            const totalPix = parcelasPagamento.filter(x=>x.forma==='PIX').reduce((a,x)=>a+Number(x.valor||0),0);\n            const totalCredito = parcelasPagamento.filter(x=>x.forma.includes('CRÉDITO') || x.forma.includes('CREDITO')).reduce((a,x)=>a+Number(x.valor||0),0);\n            const totalDebito = parcelasPagamento.filter(x=>x.forma.includes('DÉBITO') || x.forma.includes('DEBITO')).reduce((a,x)=>a+Number(x.valor||0),0);"""
assert old4 in s, 'totais caixa nao encontrados'
s=s.replace(old4,new4,1)
old5="""            receitasDia.forEach(e=>{\n                const forma=normalizarFormaPagamentoCaixa(e.pagamento);\n                if(!grupos[forma]) grupos[forma]={qtd:0,total:0};\n                grupos[forma].qtd++;\n                grupos[forma].total+=Number(e.total||0);\n            });"""
new5="""            receitasDia.forEach(e=>{\n                decomporPagamentoCaixa(e).forEach(parcela=>{\n                    const forma=parcela.forma;\n                    if(!grupos[forma]) grupos[forma]={qtd:0,total:0};\n                    grupos[forma].qtd++;\n                    grupos[forma].total+=Number(parcela.valor||0);\n                });\n            });"""
assert old5 in s
s=s.replace(old5,new5,1)
old6="""...receitasDia.map(e=>({tipo:'RECEITA',descricao:e.clienteNome||'Atendimento',forma:normalizarFormaPagamentoCaixa(e.pagamento),valor:Number(e.total||0)})),"""
new6="""...receitasDia.map(e=>({tipo:'RECEITA',descricao:e.clienteNome||'Atendimento',forma:formatarPagamentoAtendimento(e.pagamento),valor:Number(e.total||0)})),"""
assert old6 in s
s=s.replace(old6,new6,1)
# reset split fields
needle2="""                delete document.getElementById('busca-cliente').dataset.clienteId;"""
repl2=needle2+"""\n                const pagSel=document.getElementById('pag-entrada'); if(pagSel){pagSel.value='PIX'; atualizarPagamentoDivididoUI();}\n                const pv1=document.getElementById('pag-div-valor-1'); if(pv1) pv1.value='';\n                const pv2=document.getElementById('pag-div-valor-2'); if(pv2) pv2.value='';"""
assert needle2 in s
s=s.replace(needle2,repl2,1)
# keep summary fresh after cart change
needle3="""            totalSpan.innerText = `R$ ${total.toFixed(2)}`;"""
repl3=needle3+"""\n            atualizarResumoPagamentoDividido();"""
assert needle3 in s
s=s.replace(needle3,repl3,1)
# CSS append
css='''\n<style id="simpla-pagamento-dividido-v26">\n.pagamento-dividido-box{margin-top:10px;padding:12px;border:1px solid #dbe4ee;border-radius:8px;background:#f8fafc}.pagamento-dividido-linha{display:grid;grid-template-columns:minmax(0,1fr) 130px;gap:8px;margin-bottom:8px}.pagamento-dividido-box small{display:block;color:#718096;line-height:1.4;text-transform:none}@media(max-width:768px){.pagamento-dividido-linha{grid-template-columns:1fr}.pagamento-dividido-linha select,.pagamento-dividido-linha input{width:100%;min-width:0}}\n</style>\n'''
s=s.replace('</body>',css+'</body>',1)
p.write_text(s,encoding='utf-8')

sw=Path('service-worker.js')
t=sw.read_text(encoding='utf-8')
import re
t=re.sub(r"const CACHE_VERSION = '[^']+';", "const CACHE_VERSION = 'simpla-shell-v26-pagamento-dividido';", t, count=1)
sw.write_text(t,encoding='utf-8')
