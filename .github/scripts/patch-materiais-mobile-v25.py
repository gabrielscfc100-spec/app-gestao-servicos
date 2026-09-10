from pathlib import Path

p = Path('index.html')
s = p.read_text(encoding='utf-8')

marker = '<style id="simpla-materiais-mobile-v25">'
if marker in s:
    raise SystemExit('v25 já aplicada')

css = r'''
<style id="simpla-materiais-mobile-v25">
/* Materiais v25 — corrige o formulário real .fin-inline-form no mobile */
@media (max-width: 768px) {
  #financeiro #aba-saidas .fin-despesas-top-grid {
    grid-template-columns: minmax(0, 1fr) !important;
    width: 100% !important;
    min-width: 0 !important;
  }

  #financeiro #aba-saidas .fin-despesas-top-grid > .fin-panel {
    width: 100% !important;
    min-width: 0 !important;
    max-width: 100% !important;
    box-sizing: border-box !important;
    overflow: hidden !important;
  }

  #financeiro #aba-saidas .fin-despesas-top-grid > .fin-panel:first-child .fin-inline-form {
    display: flex !important;
    flex-direction: column !important;
    align-items: stretch !important;
    justify-content: flex-start !important;
    gap: 10px !important;
    width: 100% !important;
    min-width: 0 !important;
    max-width: 100% !important;
  }

  #financeiro #aba-saidas .fin-despesas-top-grid > .fin-panel:first-child .fin-inline-form > .form-group {
    display: block !important;
    flex: 0 0 auto !important;
    width: 100% !important;
    min-width: 0 !important;
    max-width: 100% !important;
    margin: 0 !important;
  }

  #financeiro #aba-saidas .fin-despesas-top-grid > .fin-panel:first-child .fin-inline-form label {
    display: block !important;
    width: 100% !important;
    max-width: 100% !important;
    white-space: normal !important;
    word-break: normal !important;
    overflow-wrap: normal !important;
    writing-mode: horizontal-tb !important;
    margin-bottom: 6px !important;
  }

  #financeiro #aba-saidas .fin-despesas-top-grid > .fin-panel:first-child #material-nome {
    display: block !important;
    width: 100% !important;
    min-width: 0 !important;
    max-width: 100% !important;
    box-sizing: border-box !important;
  }

  #financeiro #aba-saidas .fin-despesas-top-grid > .fin-panel:first-child .fin-inline-form > .btn-salvar {
    display: block !important;
    width: 100% !important;
    min-width: 0 !important;
    max-width: 100% !important;
    margin: 0 !important;
    align-self: stretch !important;
    box-sizing: border-box !important;
  }

  #financeiro #aba-saidas #lista-materiais-cadastrados {
    width: 100% !important;
    min-width: 0 !important;
    max-width: 100% !important;
    box-sizing: border-box !important;
    margin-top: 10px !important;
  }

  #financeiro #aba-saidas #lista-materiais-cadastrados > div {
    width: 100% !important;
    min-width: 0 !important;
    max-width: 100% !important;
    box-sizing: border-box !important;
  }

  #financeiro #aba-saidas #lista-materiais-cadastrados span {
    min-width: 0 !important;
    overflow-wrap: anywhere !important;
  }
}
</style>
'''

anchor = '<style id="simpla-materiais-mobile-v24">'
if anchor in s:
    s = s.replace(anchor, css + '\n' + anchor, 1)
else:
    s = s.replace('</body>', css + '\n</body>', 1)

p.write_text(s, encoding='utf-8')

sw = Path('service-worker.js')
t = sw.read_text(encoding='utf-8')
import re
t2, n = re.subn(r"const CACHE_VERSION = '[^']+';", "const CACHE_VERSION = 'simpla-shell-v25-materiais-form-mobile';", t, count=1)
if n != 1:
    raise SystemExit('CACHE_VERSION não encontrado')
sw.write_text(t2, encoding='utf-8')
