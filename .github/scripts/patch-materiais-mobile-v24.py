from pathlib import Path
import re

p = Path('index.html')
s = p.read_text(encoding='utf-8')
marker = 'simpla-materiais-mobile-v24'

if marker not in s:
    block = r'''
<style id="simpla-materiais-mobile-v24">
/* Materiais v24 — responsividade específica do formulário e listagem */
#aba-materiais,
#aba-materiais > div,
#materiais-container {
  min-width: 0 !important;
  max-width: 100% !important;
  box-sizing: border-box !important;
}

@media (max-width: 768px) {
  #aba-materiais > div:first-child {
    padding: 12px !important;
    margin-bottom: 16px !important;
    overflow: hidden !important;
  }

  #aba-materiais > div:first-child > div {
    display: grid !important;
    grid-template-columns: minmax(0, 1fr) !important;
    gap: 10px !important;
    align-items: stretch !important;
    width: 100% !important;
    min-width: 0 !important;
  }

  #aba-materiais .form-group {
    width: 100% !important;
    min-width: 0 !important;
    margin-bottom: 0 !important;
  }

  #aba-materiais input,
  #aba-materiais select,
  #aba-materiais textarea {
    display: block !important;
    width: 100% !important;
    max-width: 100% !important;
    min-width: 0 !important;
    box-sizing: border-box !important;
  }

  #aba-materiais > div:first-child > div > .btn {
    width: 100% !important;
    max-width: 100% !important;
    min-width: 0 !important;
    height: 44px !important;
  }

  #materiais-container .materiais-v24-table {
    display: block !important;
    width: 100% !important;
    max-width: 100% !important;
    border: 0 !important;
  }

  #materiais-container .materiais-v24-table thead {
    display: none !important;
  }

  #materiais-container .materiais-v24-table tbody {
    display: block !important;
    width: 100% !important;
  }

  #materiais-container .materiais-v24-table tr {
    display: block !important;
    width: 100% !important;
    margin: 0 0 12px !important;
    padding: 10px 12px !important;
    border: 1px solid #e2e8f0 !important;
    border-radius: 8px !important;
    background: #fff !important;
    box-sizing: border-box !important;
  }

  #materiais-container .materiais-v24-table td {
    display: flex !important;
    align-items: flex-start !important;
    justify-content: space-between !important;
    gap: 12px !important;
    width: 100% !important;
    min-width: 0 !important;
    padding: 9px 0 !important;
    border: 0 !important;
    border-bottom: 1px solid #edf2f7 !important;
    text-align: right !important;
    white-space: normal !important;
    overflow-wrap: anywhere !important;
    box-sizing: border-box !important;
  }

  #materiais-container .materiais-v24-table td:last-child {
    border-bottom: 0 !important;
  }

  #materiais-container .materiais-v24-table td::before {
    content: attr(data-label);
    flex: 0 0 42%;
    text-align: left !important;
    font-weight: 700 !important;
    color: #4a5568 !important;
    white-space: normal !important;
  }

  #materiais-container .materiais-v24-table td.col-material-acoes,
  #materiais-container .materiais-v24-table td[data-label="AÇÕES"],
  #materiais-container .materiais-v24-table td[data-label="Ações"] {
    display: block !important;
    text-align: left !important;
    padding-top: 11px !important;
  }

  #materiais-container .materiais-v24-table td.col-material-acoes::before,
  #materiais-container .materiais-v24-table td[data-label="AÇÕES"]::before,
  #materiais-container .materiais-v24-table td[data-label="Ações"]::before {
    display: none !important;
  }

  #materiais-container .materiais-v24-table td .btn {
    width: 100% !important;
    max-width: 100% !important;
  }
}
</style>
<script id="simpla-materiais-mobile-v24-script">
(function(){
  function aplicarMateriaisMobile(){
    const container = document.getElementById('materiais-container');
    if(!container) return;

    container.querySelectorAll('table').forEach(table => {
      table.classList.add('materiais-v24-table');
      const cabecalhos = Array.from(table.querySelectorAll('thead th')).map(th => (th.textContent || '').trim());
      table.querySelectorAll('tbody tr').forEach(tr => {
        Array.from(tr.children).forEach((td, i) => {
          if(td.tagName !== 'TD') return;
          if(!td.dataset.label) td.dataset.label = cabecalhos[i] || '';
        });
      });
    });
  }

  if(document.readyState === 'loading') document.addEventListener('DOMContentLoaded', aplicarMateriaisMobile);
  else aplicarMateriaisMobile();

  const alvo = document.getElementById('materiais-container');
  if(alvo) new MutationObserver(aplicarMateriaisMobile).observe(alvo, {childList:true, subtree:true});
  document.addEventListener('click', e => {
    if(e.target.closest('#tab-btn-materiais')) setTimeout(aplicarMateriaisMobile, 40);
  }, true);
  setTimeout(aplicarMateriaisMobile, 400);
})();
</script>
'''
    s = s.replace('</body>', block + '\n</body>')
    p.write_text(s, encoding='utf-8')

sw = Path('service-worker.js')
t = sw.read_text(encoding='utf-8')
t = re.sub(r"const CACHE_VERSION = '[^']+';", "const CACHE_VERSION = 'simpla-shell-v24-materiais-mobile';", t, count=1)
sw.write_text(t, encoding='utf-8')
