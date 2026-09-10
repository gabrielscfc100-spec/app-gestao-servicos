from pathlib import Path

path = Path('agendar.html')
text = path.read_text(encoding='utf-8')
old = """  const params = new URLSearchParams(window.location.search);\n  const slug = (params.get('empresa') || params.get('slug') || 'simpla-barbearia').trim().toLowerCase();"""
new = """  const params = new URLSearchParams(window.location.search);\n  const pathSlug = decodeURIComponent(window.location.pathname.split('/').filter(Boolean).pop() || '').trim().toLowerCase();\n  const slug = (params.get('empresa') || params.get('slug') || pathSlug || 'simpla-barbearia').trim().toLowerCase();"""
if old not in text:
    raise SystemExit('Trecho de slug não encontrado; nenhuma alteração aplicada.')
text = text.replace(old, new, 1)
path.write_text(text, encoding='utf-8')
final = path.read_text(encoding='utf-8')
if 'const pathSlug =' not in final:
    raise SystemExit('Validação falhou.')
print('agendar.html preparado para slug via pathname.')
