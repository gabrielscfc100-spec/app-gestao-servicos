from pathlib import Path
p=Path('index.html')
s=p.read_text(encoding='utf-8')
old="if(String(item.tipo || '').toUpperCase() === 'NOVO_AGENDAMENTO' && item.agendamento_id) {"
new="if(item.agendamento_id) {"
if old not in s:
    raise SystemExit('trecho alvo nao encontrado')
s=s.replace(old,new,1)
p.write_text(s,encoding='utf-8')
