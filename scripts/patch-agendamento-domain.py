from pathlib import Path

p = Path('index.html')
s = p.read_text(encoding='utf-8')
old = "return `https://gabrielscfc100-spec.github.io/agendamento-simpla/?empresa=${encodeURIComponent(slug)}`;"
new = "return `https://agendamento-simpla.simpla.workers.dev/${encodeURIComponent(slug)}`;"
if old not in s:
    raise SystemExit('URL antiga não encontrada; patch não aplicado')
s2 = s.replace(old, new, 1)
p.write_text(s2, encoding='utf-8')
print('OK: domínio do agendamento externo atualizado')
