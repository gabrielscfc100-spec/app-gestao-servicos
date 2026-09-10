from pathlib import Path
import re

p = Path('index.html')
s = p.read_text(encoding='utf-8')

novo_bloco = r'''const REGRAS_PERFIL = {
            ADMIN: {
                telas: ['dashboard','clientes','financeiro','agenda','configuracoes'],
                dashboard: true,
                clientesVisualizar: true,
                clientesEditar: true,
                clientesExcluir: true,
                clientesExportar: true,
                agendaVisualizar: true,
                agendaEditar: true,
                agendaCancelar: true,
                agendaBloquear: true,
                agendaExportar: true,
                financeiroVisualizar: true,
                financeiroOperar: true,
                financeiroExcluir: true,
                financeiroExportar: true,
                financeiroRelatorios: true,
                catalogoEditar: true,
                configuracoes: true,
                usuarios: true,
                dashboardFinanceiro: true
            },
            GESTOR: {
                telas: ['dashboard','clientes','financeiro','agenda'],
                dashboard: true,
                clientesVisualizar: true,
                clientesEditar: true,
                clientesExcluir: false,
                clientesExportar: true,
                agendaVisualizar: true,
                agendaEditar: true,
                agendaCancelar: true,
                agendaBloquear: true,
                agendaExportar: true,
                financeiroVisualizar: true,
                financeiroOperar: true,
                financeiroExcluir: true,
                financeiroExportar: true,
                financeiroRelatorios: true,
                catalogoEditar: true,
                configuracoes: false,
                usuarios: false,
                dashboardFinanceiro: true
            },
            FINANCEIRO: {
                telas: ['dashboard','clientes','financeiro','agenda'],
                dashboard: true,
                clientesVisualizar: true,
                clientesEditar: false,
                clientesExcluir: false,
                clientesExportar: false,
                agendaVisualizar: true,
                agendaEditar: false,
                agendaCancelar: false,
                agendaBloquear: false,
                agendaExportar: false,
                financeiroVisualizar: true,
                financeiroOperar: true,
                financeiroExcluir: true,
                financeiroExportar: true,
                financeiroRelatorios: true,
                catalogoEditar: false,
                configuracoes: false,
                usuarios: false,
                dashboardFinanceiro: true
            },
            FUNCIONARIO: {
                telas: ['clientes','financeiro','agenda'],
                dashboard: false,
                clientesVisualizar: true,
                clientesEditar: true,
                clientesExcluir: false,
                clientesExportar: false,
                agendaVisualizar: true,
                agendaEditar: true,
                agendaCancelar: true,
                agendaBloquear: true,
                agendaExportar: false,
                financeiroVisualizar: true,
                financeiroOperar: true,
                financeiroExcluir: false,
                financeiroExportar: false,
                financeiroRelatorios: false,
                catalogoEditar: false,
                configuracoes: false,
                usuarios: false,
                dashboardFinanceiro: false
            }
        };'''

padrao = re.compile(r"const REGRAS_PERFIL = \{.*?\n        \};\n\n        function obterPerfilAtual\(\)", re.S)
m = padrao.search(s)
if not m:
    raise SystemExit('Bloco REGRAS_PERFIL não encontrado')
s = s[:m.start()] + novo_bloco + "\n\n        function obterPerfilAtual()" + s[m.end():]

antigo_resumo = "<div class=\"perfis-resumo-grid\"><div><b>ADMIN</b><span>Acesso total, configurações e usuários.</span></div><div><b>GESTOR</b><span>Operação + financeiro + Dashboard, sem funções administrativas.</span></div><div><b>OPERACIONAL</b><span>Clientes + Agenda + lançamentos financeiros, sem Dashboard e relatórios financeiros.</span></div><div><b>FINANCEIRO</b><span>Financeiro + Dashboard + consultas, sem cadastrar clientes ou alterar Agenda.</span></div></div>"
novo_resumo = "<div class=\"perfis-resumo-grid\"><div><b>ADMIN</b><span>Acesso total ao sistema, configurações, usuários, relatórios e cadastros.</span></div><div><b>GESTOR</b><span>Dashboard, clientes, financeiro, agenda e catálogo; sem Configurações e gestão de usuários.</span></div><div><b>OPERACIONAL</b><span>Clientes, própria agenda e lançamentos operacionais; sem Dashboard, relatórios, exportações ou exclusões.</span></div><div><b>FINANCEIRO</b><span>Dashboard e financeiro completos; clientes e agenda somente para consulta; sem catálogo ou Configurações.</span></div></div>"
if antigo_resumo in s:
    s = s.replace(antigo_resumo, novo_resumo, 1)

marker = 'simpla-perfis-acesso-v12'
if marker not in s:
    bloco = r'''
<script id="simpla-perfis-acesso-v12">
(function(){
  function aplicarComplementares(){
    if(typeof obterPerfilAtual !== 'function' || typeof regraPerfil !== 'function') return;
    const perfil = obterPerfilAtual();

    // Operacional pode lançar dados financeiros, mas não visualiza relatórios consolidados.
    const ocultarRelatorios = !regraPerfil('financeiroRelatorios');
    document.querySelectorAll('#financeiro .fin-summary-grid, #financeiro .chart-box').forEach(el=>{
      el.style.display = ocultarRelatorios ? 'none' : '';
    });

    // Catálogo de serviços/produtos: somente ADMIN e GESTOR podem alterar.
    document.querySelectorAll('#financeiro button').forEach(btn=>{
      const onclick = String(btn.getAttribute('onclick') || '').toLowerCase();
      const texto = String(btn.textContent || '').toLowerCase();
      const ehCatalogo = /servico|serviço|produto/.test(onclick + ' ' + texto) && /cadastrar|adicionar|editar|excluir|salvar/.test(onclick + ' ' + texto);
      if(ehCatalogo && !regraPerfil('catalogoEditar')) btn.style.display = 'none';
    });

    // Reforça leitura apenas para Financeiro nas telas Clientes e Agenda.
    if(perfil === 'FINANCEIRO') {
      document.querySelectorAll('#clientes input, #clientes textarea, #clientes select, #clientes button').forEach(el=>{
        const id = String(el.id || '');
        const onclick = String(el.getAttribute?.('onclick') || '').toLowerCase();
        const ehConsulta = id.includes('filtro') || onclick.includes('whatsapp');
        if(!ehConsulta && el.closest('#sec-cli-cadastro')) el.closest('#sec-cli-cadastro').style.display = 'none';
      });
    }
  }

  const original = window.aplicarPermissoesPerfil;
  if(typeof original === 'function') {
    window.aplicarPermissoesPerfil = function(){
      const r = original.apply(this, arguments);
      setTimeout(aplicarComplementares, 0);
      setTimeout(aplicarComplementares, 250);
      return r;
    };
  }

  document.addEventListener('DOMContentLoaded', ()=>{
    setTimeout(aplicarComplementares, 500);
    setTimeout(aplicarComplementares, 1500);
  });
  document.addEventListener('click', e=>{
    if(e.target.closest('.menu-btn, .tab, button')) setTimeout(aplicarComplementares, 80);
  }, true);
})();
</script>
'''
    s = s.replace('</body>', bloco + '\n</body>')

p.write_text(s, encoding='utf-8')

sw = Path('service-worker.js')
ss = sw.read_text(encoding='utf-8')
ss = re.sub(r"const CACHE_VERSION = '[^']+';", "const CACHE_VERSION = 'simpla-shell-v12-perfis-acesso';", ss, count=1)
sw.write_text(ss, encoding='utf-8')
