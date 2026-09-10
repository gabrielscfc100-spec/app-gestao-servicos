from pathlib import Path
import re

p = Path('index.html')
s = p.read_text(encoding='utf-8')
marker = 'simpla-atendimento-permissoes-v19'

# Inclui a nova tela atendimento na matriz de telas dos perfis que já podem operar financeiro.
s, c1 = re.subn(r"telas: \['dashboard','clientes','financeiro','agenda','configuracoes'\]", "telas: ['dashboard','clientes','financeiro','agenda','atendimento','configuracoes']", s, count=1)
s, c2 = re.subn(r"telas: \['dashboard','clientes','financeiro','agenda'\]", "telas: ['dashboard','clientes','financeiro','agenda','atendimento']", s, count=2)
s, c3 = re.subn(r"telas: \['clientes','financeiro','agenda'\]", "telas: ['clientes','financeiro','agenda','atendimento']", s, count=1)

if (c1, c2, c3) != (1, 2, 1):
    raise SystemExit(f'Matriz de perfis não encontrada como esperado: {(c1,c2,c3)}')

# Corrige a visibilidade do item desktop para seguir a permissão real, em vez de esconder FINANCEIRO fixamente.
s = s.replace(
    "menu.style.display=(p==='FINANCEIRO' ? 'none' : '');",
    "menu.style.display=(typeof regraPerfil==='function' && !regraPerfil('financeiroOperar')) ? 'none' : '';",
    1
)

if marker not in s:
    block = r'''
<script id="simpla-atendimento-permissoes-v19">
(function(){
  function sincronizarPermissaoAtendimento(){
    try{
      if(typeof REGRAS_PERFIL !== 'undefined'){
        Object.values(REGRAS_PERFIL).forEach(regra => {
          if(regra && regra.financeiroOperar && Array.isArray(regra.telas) && !regra.telas.includes('atendimento')){
            regra.telas.push('atendimento');
          }
        });
      }
      const pode = (typeof regraPerfil === 'function') ? !!regraPerfil('financeiroOperar') : true;
      document.querySelectorAll('#menu-btn-atendimento, [data-tela="atendimento"], .bottom-nav-atendimento').forEach(el => {
        el.style.display = pode ? '' : 'none';
      });
    }catch(e){ console.error('SimplA: falha ao sincronizar permissão de atendimento', e); }
  }
  sincronizarPermissaoAtendimento();
  if(document.readyState === 'loading') document.addEventListener('DOMContentLoaded', sincronizarPermissaoAtendimento);
  document.addEventListener('click', e => {
    if(e.target.closest('.menu-btn, .simpla-bottom-nav, #simpla-bottom-nav')) setTimeout(sincronizarPermissaoAtendimento, 20);
  }, true);
  setTimeout(sincronizarPermissaoAtendimento, 300);
  setTimeout(sincronizarPermissaoAtendimento, 1200);
})();
</script>
'''
    s = s.replace('</body>', block + '\n</body>', 1)

p.write_text(s, encoding='utf-8')

sw = Path('service-worker.js')
ss = sw.read_text(encoding='utf-8')
ss = re.sub(r"const CACHE_VERSION = '[^']+';", "const CACHE_VERSION = 'simpla-shell-v19-atendimento-permissoes';", ss, count=1)
sw.write_text(ss, encoding='utf-8')
