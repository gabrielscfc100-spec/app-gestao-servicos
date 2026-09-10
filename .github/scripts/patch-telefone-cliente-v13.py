from pathlib import Path
import re

index = Path('index.html')
s = index.read_text(encoding='utf-8')
marker = 'simpla-telefone-cliente-v13'

if marker not in s:
    modal = r'''
<!-- SIMPLA telefone ja cadastrado v13 -->
<div id="modal-telefone-cliente-existente" class="modal-overlay">
  <div class="modal-balao" style="text-align:left;width:440px;max-width:calc(100vw - 24px);">
    <h3 style="text-align:center;">Telefone já cadastrado</h3>
    <p id="telefone-cliente-existente-texto" style="font-size:13px;color:#4a5568;line-height:1.5;text-transform:none;margin-bottom:16px;"></p>
    <div style="padding:12px;border:1px solid #bee3f8;background:#ebf8ff;border-radius:7px;margin-bottom:16px;font-size:12px;color:#2c5282;line-height:1.5;text-transform:none;">
      Escolha se o agendamento pertence ao cliente já cadastrado ou se este mesmo telefone está sendo usado para outra pessoa.
    </div>
    <div class="modal-botoes" style="display:grid;grid-template-columns:1fr;gap:9px;">
      <button type="button" class="btn-salvar" onclick="usarClienteTelefoneExistente()" style="background:#3182ce;color:white;width:100%;">Usar cliente existente</button>
      <button type="button" onclick="agendarOutraPessoaTelefoneExistente()" style="padding:10px;border:0;border-radius:4px;background:#edf2f7;color:#2d3748;font-weight:bold;cursor:pointer;width:100%;">Agendar para outra pessoa</button>
      <button type="button" class="btn-cancelar-modal" onclick="fecharModalTelefoneExistente()" style="width:100%;">Voltar</button>
    </div>
  </div>
</div>
'''
    anchor = '<!-- Modal: cadastrar cliente a partir de agendamento externo -->'
    if anchor not in s:
        raise SystemExit('Anchor do modal de agendamento não encontrado')
    s = s.replace(anchor, modal + anchor, 1)

    script = r'''
<script id="simpla-telefone-cliente-v13">
(function(){
  let clienteTelefoneDetectado = null;
  let telefoneDetectadoOriginal = '';

  function normalizarTelefoneComparacao(valor){
    let digitos = String(valor || '').replace(/\D/g, '');
    if(digitos.startsWith('55') && digitos.length > 11) digitos = digitos.slice(2);
    if(digitos.length > 11) digitos = digitos.slice(-11);
    return digitos;
  }

  function nomeClienteTelefone(c){
    if(!c) return 'cliente cadastrado';
    try {
      if(typeof formatarNomeCompletoCliente === 'function') return formatarNomeCompletoCliente(c.nome, c.sobrenome);
    } catch(_) {}
    return [c.nome, c.sobrenome].filter(Boolean).join(' ') || 'cliente cadastrado';
  }

  window.fecharModalTelefoneExistente = function(){
    document.getElementById('modal-telefone-cliente-existente')?.classList.remove('active');
  };

  window.verificarTelefoneExistenteAgenda = function(){
    const campo = document.getElementById('agenda-telefone');
    if(!campo || typeof clientes === 'undefined') return;
    const numero = normalizarTelefoneComparacao(campo.value);
    if(numero.length < 10) return;

    const selecionado = (typeof obterClienteSelecionado === 'function') ? obterClienteSelecionado('agenda') : null;
    if(selecionado && normalizarTelefoneComparacao(selecionado.telefone) === numero) {
      campo.dataset.telefoneVerificado = numero;
      return;
    }
    if(campo.dataset.telefoneVerificado === numero) return;

    const encontrados = (clientes || []).filter(c => normalizarTelefoneComparacao(c.telefone) === numero);
    if(!encontrados.length) {
      delete campo.dataset.telefoneVerificado;
      return;
    }

    clienteTelefoneDetectado = encontrados[0];
    telefoneDetectadoOriginal = campo.value;
    const texto = document.getElementById('telefone-cliente-existente-texto');
    if(texto) {
      const complemento = encontrados.length > 1 ? ` Há ${encontrados.length} cadastros com este telefone; o primeiro encontrado é exibido abaixo.` : '';
      texto.innerHTML = `O telefone informado já está vinculado a <b>${nomeClienteTelefone(clienteTelefoneDetectado)}</b>.${complemento}`;
    }
    document.getElementById('modal-telefone-cliente-existente')?.classList.add('active');
  };

  window.usarClienteTelefoneExistente = function(){
    if(!clienteTelefoneDetectado) return fecharModalTelefoneExistente();
    const tipo = document.getElementById('agenda-tipo-cliente');
    const campo = document.getElementById('agenda-telefone');
    if(tipo) tipo.value = 'cadastrado';
    if(typeof alternarTipoClienteAgendamento === 'function') alternarTipoClienteAgendamento(true);
    if(typeof selecionarClienteBusca === 'function') selecionarClienteBusca('agenda', clienteTelefoneDetectado.id);
    if(campo) campo.dataset.telefoneVerificado = normalizarTelefoneComparacao(campo.value || clienteTelefoneDetectado.telefone);
    fecharModalTelefoneExistente();
  };

  window.agendarOutraPessoaTelefoneExistente = function(){
    const tipo = document.getElementById('agenda-tipo-cliente');
    const campoCliente = document.getElementById('agenda-cliente-busca');
    const campoTelefone = document.getElementById('agenda-telefone');
    if(tipo) tipo.value = 'avulso';
    if(typeof alternarTipoClienteAgendamento === 'function') alternarTipoClienteAgendamento(true);
    if(campoCliente) {
      campoCliente.value = '';
      delete campoCliente.dataset.clienteId;
    }
    if(campoTelefone) {
      campoTelefone.value = telefoneDetectadoOriginal;
      campoTelefone.dataset.telefoneVerificado = normalizarTelefoneComparacao(telefoneDetectadoOriginal);
    }
    const ajuda = document.getElementById('agenda-cliente-ajuda');
    if(ajuda) ajuda.textContent = 'Este telefone pertence a um cadastro existente, mas este agendamento será registrado para outra pessoa, sem alterar o cadastro original.';
    fecharModalTelefoneExistente();
    setTimeout(() => campoCliente?.focus(), 80);
  };

  function instalar(){
    const campo = document.getElementById('agenda-telefone');
    if(!campo || campo.dataset.verificacaoTelefoneInstalada === '1') return;
    campo.dataset.verificacaoTelefoneInstalada = '1';
    campo.addEventListener('input', () => {
      const atual = normalizarTelefoneComparacao(campo.value);
      if(campo.dataset.telefoneVerificado && campo.dataset.telefoneVerificado !== atual) delete campo.dataset.telefoneVerificado;
    });
    campo.addEventListener('blur', () => setTimeout(() => window.verificarTelefoneExistenteAgenda(), 80));
    campo.addEventListener('change', () => window.verificarTelefoneExistenteAgenda());
  }

  document.addEventListener('DOMContentLoaded', instalar);
  setTimeout(instalar, 500);
  setTimeout(instalar, 1500);
})();
</script>
'''
    if '</body>' not in s:
        raise SystemExit('body não encontrado')
    s = s.replace('</body>', script + '\n</body>', 1)
    index.write_text(s, encoding='utf-8')

sw = Path('service-worker.js')
ss = sw.read_text(encoding='utf-8')
ss2 = re.sub(r"const CACHE_VERSION = '[^']+';", "const CACHE_VERSION = 'simpla-shell-v13-telefone-cliente';", ss, count=1)
if ss2 != ss:
    sw.write_text(ss2, encoding='utf-8')
