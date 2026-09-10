from pathlib import Path
import re

p=Path('index.html')
s=p.read_text(encoding='utf-8')
if 'simpla-atendimento-pix-final-v30' in s:
    raise SystemExit('v30 ja aplicada')

# 1) Torna visível e clara a ação de excluir itens do carrinho.
old='''<button onclick="removerDoCarrinho(${idx})" style="background: none; border: none; color: #e53e3e; cursor: pointer; font-weight: bold;"></button>'''
new='''<button type="button" class="btn-remover-item-atendimento-v30" aria-label="Excluir ${item.nome}" onclick="removerDoCarrinho(${idx})">Excluir</button>'''
assert old in s, 'botao vazio de remover item nao encontrado'
s=s.replace(old,new,1)

# 2) O botão principal passa pelo fluxo de destaque do PIX.
old_btn='''<button class="btn-salvar fin-btn-full" onclick="lancarEntrada()">Finalizar recebimento</button>'''
new_btn='''<button class="btn-salvar fin-btn-full" onclick="finalizarRecebimentoComPixV30()">Finalizar recebimento</button>'''
assert old_btn in s, 'botao finalizar recebimento nao encontrado'
s=s.replace(old_btn,new_btn,1)

block=r'''
<style id="simpla-atendimento-pix-final-v30">
.btn-remover-item-atendimento-v30{
  border:1px solid #feb2b2;
  background:#fff5f5;
  color:#c53030;
  border-radius:7px;
  padding:6px 9px;
  cursor:pointer;
  font-size:11px;
  font-weight:700;
  text-transform:none!important;
}
.btn-remover-item-atendimento-v30:hover{background:#fed7d7}
#pix-final-modal-v30 .modal-balao{width:min(520px,calc(100vw - 24px));max-height:92dvh;overflow-y:auto;text-align:center;padding:22px}
#pix-final-modal-v30 .pix-final-qr-v30{width:320px;min-height:320px;max-width:100%;margin:14px auto;background:#fff;border:1px solid #e2e8f0;border-radius:12px;padding:10px;display:flex;align-items:center;justify-content:center}
#pix-final-modal-v30 .pix-final-qr-v30 img,#pix-final-modal-v30 .pix-final-qr-v30 canvas{width:300px!important;height:300px!important;max-width:100%!important}
#pix-final-modal-v30 .pix-final-valor-v30{font-size:22px;font-weight:800;color:#1f3b56;margin:6px 0 2px;text-transform:none!important}
#pix-final-modal-v30 .pix-final-help-v30{font-size:12px;color:#718096;line-height:1.45;text-transform:none!important}
#pix-final-modal-v30 .pix-final-actions-v30{display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-top:16px}
#pix-final-modal-v30 .pix-final-actions-v30 button{min-height:44px;border:0;border-radius:8px;font-weight:700;cursor:pointer;text-transform:none!important}
#pix-final-modal-v30 .pix-final-copiar-v30{background:#edf2f7;color:#2d3748}
#pix-final-modal-v30 .pix-final-confirmar-v30{background:#2f855a;color:#fff}
#pix-final-modal-v30 .pix-final-cancelar-v30{grid-column:1/-1;background:#fff5f5;color:#c53030;border:1px solid #feb2b2!important}
@media(max-width:768px){
  #lista-carrinho>div{gap:10px!important;align-items:flex-start!important}
  #lista-carrinho>div>span:first-child{min-width:0;flex:1;overflow-wrap:anywhere}
  #lista-carrinho>div>div{gap:7px!important;flex-wrap:wrap;justify-content:flex-end}
  .btn-remover-item-atendimento-v30{padding:7px 10px;font-size:11px}
  #pix-final-modal-v30 .pix-final-qr-v30{width:min(300px,100%);min-height:280px}
  #pix-final-modal-v30 .pix-final-qr-v30 img,#pix-final-modal-v30 .pix-final-qr-v30 canvas{width:280px!important;height:280px!important}
  #pix-final-modal-v30 .pix-final-actions-v30{grid-template-columns:1fr}
  #pix-final-modal-v30 .pix-final-cancelar-v30{grid-column:auto}
}
</style>
<div id="pix-final-modal-v30" class="modal-overlay" style="z-index:6200;">
  <div class="modal-balao">
    <h3 style="text-transform:none;margin-bottom:4px;">Pagamento via Pix</h3>
    <div id="pix-final-valor-v30" class="pix-final-valor-v30"></div>
    <p class="pix-final-help-v30">Apresente o QR Code ao cliente. Confirme o recebimento do Pix antes de finalizar o atendimento.</p>
    <div id="pix-final-qr-v30" class="pix-final-qr-v30"></div>
    <div class="pix-final-actions-v30">
      <button type="button" class="pix-final-copiar-v30" onclick="copiarPixFinalV30()">Copiar Pix</button>
      <button type="button" class="pix-final-confirmar-v30" onclick="confirmarFinalizacaoPixV30()">Pagamento recebido · Finalizar</button>
      <button type="button" class="pix-final-cancelar-v30" onclick="fecharPixFinalV30()">Voltar ao atendimento</button>
    </div>
  </div>
</div>
<script id="simpla-atendimento-pix-final-v30">
(function(){
  let finalizandoPix=false;

  function totalAtualV30(){
    try{return typeof totalCarrinhoAtual==='function'?Number(totalCarrinhoAtual()||0):0}catch(_){return 0}
  }
  function moedaV30(v){return Number(v||0).toLocaleString('pt-BR',{style:'currency',currency:'BRL'})}

  window.fecharPixFinalV30=function(){document.getElementById('pix-final-modal-v30')?.classList.remove('active')};

  window.copiarPixFinalV30=async function(){
    const payload=document.getElementById('pix-copia-v27')?.value||'';
    if(!payload){alert('Pix copia e cola indisponível.');return;}
    try{await navigator.clipboard.writeText(payload);alert('Pix copia e cola copiado.');}
    catch(_){
      const ta=document.createElement('textarea');ta.value=payload;document.body.appendChild(ta);ta.select();document.execCommand('copy');ta.remove();alert('Pix copia e cola copiado.');
    }
  };

  async function abrirPixFinalV30(){
    if(typeof atualizarPixUI==='function') await atualizarPixUI(true);
    const payload=document.getElementById('pix-copia-v27')?.value||'';
    if(!payload){
      const status=document.getElementById('pix-status-v27')?.textContent||'Configure os dados Pix antes de finalizar.';
      alert(status);
      return false;
    }
    const qr=document.getElementById('pix-final-qr-v30');
    if(!qr) return false;
    qr.innerHTML='';
    if(typeof QRCode==='undefined'){
      alert('Não foi possível carregar o gerador de QR Code. Tente atualizar o aplicativo.');
      return false;
    }
    new QRCode(qr,{text:payload,width:300,height:300,correctLevel:QRCode.CorrectLevel.M});
    const valor=document.getElementById('pix-final-valor-v30');
    if(valor) valor.textContent=moedaV30(totalAtualV30());
    document.getElementById('pix-final-modal-v30')?.classList.add('active');
    return true;
  }

  window.finalizarRecebimentoComPixV30=async function(){
    if(finalizandoPix) return;
    const forma=document.getElementById('pag-entrada')?.value||'';
    if(forma!=='PIX'){
      if(typeof lancarEntrada==='function') await lancarEntrada();
      return;
    }
    if(totalAtualV30()<=0){
      if(typeof lancarEntrada==='function') await lancarEntrada();
      return;
    }
    await abrirPixFinalV30();
  };

  window.confirmarFinalizacaoPixV30=async function(){
    if(finalizandoPix) return;
    finalizandoPix=true;
    const btn=document.querySelector('#pix-final-modal-v30 .pix-final-confirmar-v30');
    if(btn){btn.disabled=true;btn.textContent='Finalizando...';}
    try{
      window.fecharPixFinalV30();
      if(typeof lancarEntrada==='function') await lancarEntrada();
    }finally{
      finalizandoPix=false;
      if(btn){btn.disabled=false;btn.textContent='Pagamento recebido · Finalizar';}
    }
  };
})();
</script>
'''
s=s.replace('</body>',block+'\n</body>',1)
p.write_text(s,encoding='utf-8')

sw=Path('service-worker.js')
t=sw.read_text(encoding='utf-8')
t,n=re.subn(r"const CACHE_VERSION = '[^']+';", "const CACHE_VERSION = 'simpla-shell-v30-itens-pix-final';", t, count=1)
assert n==1, 'CACHE_VERSION nao encontrado'
sw.write_text(t,encoding='utf-8')
