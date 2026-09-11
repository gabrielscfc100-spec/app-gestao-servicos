from pathlib import Path
import re

p = Path('index.html')
s = p.read_text(encoding='utf-8')
marker = '<!-- SIMPLA clientes duplicidade v38 -->'

if marker not in s:
    bloco = r'''
<!-- SIMPLA clientes duplicidade v38 -->
<style id="simpla-clientes-duplicidade-v38-style">
#simpla-duplicidade-hint-v38{display:none;margin-top:6px;padding:8px 10px;border:1px solid #fbd38d;background:#fffaf0;color:#975a16;border-radius:6px;font-size:12px;line-height:1.4;text-transform:none}
#simpla-duplicidade-hint-v38.ativo{display:block}
</style>
<script id="simpla-clientes-duplicidade-v38-script">
(function(){
  let clienteDuplicadoV38 = null;

  function listaClientes(){
    try { return Array.isArray(clientes) ? clientes : []; } catch(_) { return []; }
  }
  function normTel(v){ return String(v || '').replace(/\D/g,''); }
  function normEmail(v){ return String(v || '').trim().toLowerCase(); }
  function localizar(telefone,email,ignorarId){
    const tel = normTel(telefone), mail = normEmail(email);
    if(!tel && !mail) return null;
    return listaClientes().find(c => {
      if(ignorarId && String(c.id) === String(ignorarId)) return false;
      const mesmoTel = !!tel && normTel(c.telefone) === tel;
      const mesmoEmail = !!mail && normEmail(c.email) === mail;
      return mesmoTel || mesmoEmail;
    }) || null;
  }
  function motivo(c,telefone,email){
    const itens=[];
    if(normTel(telefone) && normTel(c.telefone) === normTel(telefone)) itens.push('mesmo telefone');
    if(normEmail(email) && normEmail(c.email) === normEmail(email)) itens.push('mesmo e-mail');
    return itens.join(' e ');
  }
  function abrirModal(c,telefone,email){
    clienteDuplicadoV38 = c;
    const modal=document.getElementById('modal-cliente-duplicado');
    const texto=document.getElementById('texto-cliente-duplicado');
    if(!modal || !texto){
      alert('Já existe um cliente com o mesmo telefone ou e-mail. Abra o cadastro existente antes de continuar.');
      return;
    }
    const nome=((c.nome||'')+' '+(c.sobrenome||'')).trim();
    texto.innerHTML = `Já existe um cliente cadastrado com <b>${motivo(c,telefone,email)}</b>:<br><br><b>${nome || 'Cliente'}</b>${c.codigo ? ` · ${c.codigo}` : ''}<br>${c.telefone ? `Telefone: ${c.telefone}<br>` : ''}${c.email ? `E-mail: ${c.email}<br>` : ''}<br>Para manter todo o histórico em um único perfil, o SimplA não criará outro cadastro com esses dados.`;
    const botoes=modal.querySelector('.modal-botoes');
    if(botoes){
      botoes.innerHTML = '<button class="btn-cancelar-modal" type="button" onclick="fecharDuplicidadeClienteV38()">Voltar ao cadastro</button><button class="btn-salvar" type="button" style="background:#3182ce;color:white" onclick="abrirClienteDuplicadoV38()">Ver cliente existente</button>';
    }
    const titulo=modal.querySelector('h3'); if(titulo) titulo.textContent='Cliente já cadastrado';
    modal.classList.add('active');
  }
  window.fecharDuplicidadeClienteV38=function(){
    document.getElementById('modal-cliente-duplicado')?.classList.remove('active');
  };
  window.abrirClienteDuplicadoV38=function(){
    const id=clienteDuplicadoV38?.id;
    document.getElementById('modal-cliente-duplicado')?.classList.remove('active');
    if(id && typeof abrirHistoricoCliente === 'function') abrirHistoricoCliente(id);
  };

  function criarHint(){
    const tel=document.getElementById('cli-telefone');
    const email=document.getElementById('cli-email');
    if(!tel || document.getElementById('simpla-duplicidade-hint-v38')) return;
    const box=document.createElement('div');
    box.id='simpla-duplicidade-hint-v38';
    (email?.closest('.form-group') || tel.closest('.form-group'))?.appendChild(box);
    const atualizar=()=>{
      const c=localizar(tel.value,email?.value||'',null);
      if(c){
        box.classList.add('ativo');
        box.textContent=`Possível duplicidade: ${((c.nome||'')+' '+(c.sobrenome||'')).trim()} já possui ${motivo(c,tel.value,email?.value||'')}.`;
      } else {
        box.classList.remove('ativo'); box.textContent='';
      }
    };
    tel.addEventListener('input',atualizar); email?.addEventListener('input',atualizar);
  }

  function instalar(){
    criarHint();
    if(typeof cadastrarCliente === 'function' && !cadastrarCliente.__v38){
      const original=cadastrarCliente;
      const wrapper=async function(){
        const telefone=document.getElementById('cli-telefone')?.value||'';
        const email=document.getElementById('cli-email')?.value||'';
        const dup=localizar(telefone,email,null);
        if(dup){ abrirModal(dup,telefone,email); return; }
        return await original.apply(this,arguments);
      };
      wrapper.__v38=true;
      window.cadastrarCliente=wrapper;
      try{ cadastrarCliente=wrapper; }catch(_){ }
    }
    if(typeof salvarEdicaoCliente === 'function' && !salvarEdicaoCliente.__v38){
      const originalEdit=salvarEdicaoCliente;
      const wrapperEdit=async function(){
        const id=document.getElementById('edit-cli-id')?.value||'';
        const telefone=document.getElementById('edit-cli-telefone')?.value||'';
        const email=document.getElementById('edit-cli-email')?.value||'';
        const dup=localizar(telefone,email,id);
        if(dup){ abrirModal(dup,telefone,email); return; }
        return await originalEdit.apply(this,arguments);
      };
      wrapperEdit.__v38=true;
      window.salvarEdicaoCliente=wrapperEdit;
      try{ salvarEdicaoCliente=wrapperEdit; }catch(_){ }
    }
  }

  if(document.readyState==='loading') document.addEventListener('DOMContentLoaded',()=>setTimeout(instalar,300));
  else setTimeout(instalar,300);
  setTimeout(instalar,1200);
})();
</script>
'''
    if '</body>' not in s:
        raise SystemExit('body nao encontrado')
    s = s.replace('</body>', bloco + '\n</body>', 1)
    p.write_text(s, encoding='utf-8')

sw = Path('service-worker.js')
t = sw.read_text(encoding='utf-8')
t = re.sub(r"const CACHE_VERSION = ['\"][^'\"]+['\"]", "const CACHE_VERSION = 'simpla-shell-v38-clientes-duplicidade'", t, count=1)
sw.write_text(t, encoding='utf-8')
print('v38 aplicada')
