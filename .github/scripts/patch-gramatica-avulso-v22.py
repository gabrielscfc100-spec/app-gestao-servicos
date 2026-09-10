from pathlib import Path
import re

p = Path('index.html')
s = p.read_text(encoding='utf-8')

# Corrige o erro literal exibido no contador.
for errado in ['DISPONIVELIS','Disponivelis','disponivelis']:
    s = s.replace(errado, 'DISPONÍVEIS')

marker = 'simpla-cliente-avulso-v22'
if marker not in s:
    block = r'''
<style id="simpla-cliente-avulso-v22-style">
#atendimento-cliente-modo{background:#f8fafc;border:1px solid #e2e8f0;border-radius:8px;padding:14px;margin-bottom:16px}
#atendimento-cliente-modo .atendimento-modo-botoes{display:grid;grid-template-columns:1fr 1fr;gap:8px;margin-top:8px}
#atendimento-cliente-modo .atendimento-modo-btn{border:1px solid #cbd5e0;background:#fff;color:#4a5568;padding:11px 12px;border-radius:7px;font-weight:700;cursor:pointer}
#atendimento-cliente-modo .atendimento-modo-btn.active{background:#1a1c23;color:#fff;border-color:#1a1c23}
#atendimento-avulso-campos{display:none;background:#fff;border:1px solid #e2e8f0;border-radius:8px;padding:14px;margin-bottom:16px}
#atendimento-avulso-campos.active{display:block}
#atendimento-avulso-campos .avulso-grid{display:grid;grid-template-columns:1fr 1fr;gap:12px}
#atendimento-avulso-campos .form-group{margin-bottom:0}
#atendimento-avulso-campos .avulso-ajuda{font-size:11px;color:#718096;line-height:1.4;margin:10px 0 0}
@media(max-width:700px){#atendimento-cliente-modo .atendimento-modo-botoes,#atendimento-avulso-campos .avulso-grid{grid-template-columns:1fr}}
</style>
<script id="simpla-cliente-avulso-v22">
(function(){
  let modoAtendimentoCliente = 'cadastrado';
  let preparandoClienteAvulso = false;

  function normalizarContato(v){ return String(v||'').replace(/\D/g,''); }

  function atualizarModoCliente(){
    const av = document.getElementById('atendimento-avulso-campos');
    document.querySelectorAll('#atendimento-cliente-modo .atendimento-modo-btn').forEach(b=>b.classList.toggle('active', b.dataset.modo===modoAtendimentoCliente));
    av?.classList.toggle('active', modoAtendimentoCliente==='avulso');
    const busca = document.getElementById('busca-cliente');
    const grupoBusca = busca?.closest('.form-group');
    if(grupoBusca) grupoBusca.style.display = modoAtendimentoCliente==='avulso' ? 'none' : '';
  }

  function montarEscolhaCliente(){
    const area = document.querySelector('#aba-entradas .entradas-form-area');
    if(!area || document.getElementById('atendimento-cliente-modo')) return;
    const bloco = document.createElement('div');
    bloco.innerHTML = `
      <div id="atendimento-cliente-modo">
        <strong>Cliente do atendimento</strong>
        <div class="atendimento-modo-botoes">
          <button type="button" class="atendimento-modo-btn active" data-modo="cadastrado">Cliente cadastrado</button>
          <button type="button" class="atendimento-modo-btn" data-modo="avulso">Cliente avulso</button>
        </div>
      </div>
      <div id="atendimento-avulso-campos">
        <div class="avulso-grid">
          <div class="form-group"><label>Nome *</label><input id="atendimento-avulso-nome" autocomplete="name"></div>
          <div class="form-group"><label>Sobrenome</label><input id="atendimento-avulso-sobrenome"></div>
          <div class="form-group"><label>Telefone</label><input id="atendimento-avulso-telefone" inputmode="tel" autocomplete="tel"></div>
          <div class="form-group"><label>E-mail</label><input id="atendimento-avulso-email" type="email" autocomplete="email"></div>
          <div class="form-group"><label>Data de nascimento</label><input id="atendimento-avulso-aniversario" type="date"></div>
        </div>
        <p class="avulso-ajuda">Ao finalizar o atendimento, estes dados serão usados para criar automaticamente o cadastro do cliente. Se o telefone ou e-mail já estiverem vinculados a um cliente, o cadastro existente será reutilizado.</p>
      </div>`;
    while(bloco.firstChild) area.insertBefore(bloco.firstChild, area.firstChild);
    document.querySelectorAll('#atendimento-cliente-modo .atendimento-modo-btn').forEach(btn=>btn.addEventListener('click',()=>{
      modoAtendimentoCliente = btn.dataset.modo;
      if(modoAtendimentoCliente==='avulso'){
        const busca = document.getElementById('busca-cliente');
        if(busca){ busca.value=''; delete busca.dataset.clienteId; }
      }
      atualizarModoCliente();
    }));
    atualizarModoCliente();
  }

  async function obterOuCriarClienteAvulso(){
    const nome = document.getElementById('atendimento-avulso-nome')?.value.trim() || '';
    const sobrenome = document.getElementById('atendimento-avulso-sobrenome')?.value.trim() || '';
    const telefone = document.getElementById('atendimento-avulso-telefone')?.value.trim() || '';
    const email = document.getElementById('atendimento-avulso-email')?.value.trim() || '';
    const aniversario = document.getElementById('atendimento-avulso-aniversario')?.value || null;
    if(!nome){ alert('Informe o nome do cliente avulso.'); throw new Error('NOME_AVULSO_OBRIGATORIO'); }

    const telNorm = normalizarContato(telefone);
    const emailNorm = email.toLowerCase();
    let existente = Array.isArray(clientes) ? clientes.find(c =>
      (telNorm && normalizarContato(c.telefone)===telNorm) || (emailNorm && String(c.email||'').trim().toLowerCase()===emailNorm)
    ) : null;
    if(existente) return existente;

    if(FINANCEIRO_CLOUD_ATIVO && CloudDB && empresaAtual?.cloud && empresaAtual?.id){
      const { data, error } = await CloudDB.rpc('criar_cliente_atendimento', {
        p_empresa_id: empresaAtual.id,
        p_nome: nome,
        p_sobrenome: sobrenome || null,
        p_telefone: telefone || null,
        p_email: email || null,
        p_aniversario: aniversario || null
      });
      if(error) throw error;
      const row = Array.isArray(data) ? data[0] : data;
      const local = (typeof clienteCloudParaLocal==='function') ? clienteCloudParaLocal(row) : {
        id:row.id, empresaId:row.empresa_id, codigo:row.codigo||'', nome:row.nome||nome, sobrenome:row.sobrenome||sobrenome,
        telefone:row.telefone||telefone, email:row.email||email, aniversario:row.aniversario||aniversario, cloud:true
      };
      if(!clientes.some(c=>String(c.id)===String(local.id))) clientes.push(local);
      if(typeof sincronizarDadosClientesTodasAsTelas==='function') sincronizarDadosClientesTodasAsTelas();
      return local;
    }

    const local = { id:Date.now(), codigo:`AV-${String(Date.now()).slice(-8)}`, nome, sobrenome, telefone, email, aniversario, dataCadastro:new Date().toISOString() };
    clientes.push(local);
    if(typeof salvarStorage==='function') salvarStorage();
    if(typeof sincronizarDadosClientesTodasAsTelas==='function') sincronizarDadosClientesTodasAsTelas();
    return local;
  }

  function preencherBuscaComCliente(cliente){
    const busca = document.getElementById('busca-cliente');
    if(!busca || !cliente) return;
    const nomeCompleto = (typeof formatarNomeCompletoCliente==='function')
      ? formatarNomeCompletoCliente(cliente.nome, cliente.sobrenome)
      : [cliente.nome,cliente.sobrenome].filter(Boolean).join(' ');
    busca.value = cliente.codigo ? `${cliente.codigo} - ${nomeCompleto}` : nomeCompleto;
    busca.dataset.clienteId = cliente.id;
  }

  const lancarEntradaOriginalV22 = lancarEntrada;
  lancarEntrada = async function(){
    if(preparandoClienteAvulso) return;
    if(modoAtendimentoCliente !== 'avulso') return await lancarEntradaOriginalV22.apply(this, arguments);
    preparandoClienteAvulso = true;
    try{
      const cliente = await obterOuCriarClienteAvulso();
      preencherBuscaComCliente(cliente);
      const totalAntes = entradas.length;
      await lancarEntradaOriginalV22.apply(this, arguments);
      if(entradas.length > totalAntes){
        ['atendimento-avulso-nome','atendimento-avulso-sobrenome','atendimento-avulso-telefone','atendimento-avulso-email','atendimento-avulso-aniversario'].forEach(id=>{ const e=document.getElementById(id); if(e)e.value=''; });
        modoAtendimentoCliente='cadastrado';
        atualizarModoCliente();
      }
    }catch(err){
      if(err?.message !== 'NOME_AVULSO_OBRIGATORIO'){
        console.error('Falha ao preparar cliente avulso:',err);
        alert(`Não foi possível preparar o cliente avulso: ${err?.message || 'erro desconhecido'}`);
      }
    }finally{ preparandoClienteAvulso=false; }
  };

  montarEscolhaCliente();
  const obs = new MutationObserver(montarEscolhaCliente);
  obs.observe(document.body,{childList:true,subtree:true});

  function corrigirDisponiveis(){
    document.querySelectorAll('*').forEach(el=>{
      if(el.children.length) return;
      const t=(el.textContent||'').trim();
      if(/^\d+\s+DISPONIVELIS$/i.test(t)) el.textContent=t.replace(/DISPONIVELIS/i,'DISPONÍVEIS');
      if(/^1\s+DISPONÍVEIS$/i.test(el.textContent||'')) el.textContent='1 DISPONÍVEL';
    });
  }
  corrigirDisponiveis();
  new MutationObserver(corrigirDisponiveis).observe(document.body,{childList:true,subtree:true,characterData:true});
})();
</script>
'''
    s = s.replace('</body>', block + '\n</body>')

p.write_text(s, encoding='utf-8')

sw = Path('service-worker.js')
t = sw.read_text(encoding='utf-8')
t = re.sub(r"const CACHE_VERSION = 'simpla-shell-v[^']+';", "const CACHE_VERSION = 'simpla-shell-v22-cliente-avulso';", t, count=1)
sw.write_text(t, encoding='utf-8')
