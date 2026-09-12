from pathlib import Path

html = Path('index.html').read_text(encoding='utf-8')
termos = [
    'function abrirModalAgendamento',
    'async function abrirModalAgendamento',
    'agenda-cliente-busca',
    'limparSelecaoCliente',
    'atualizarSugestoesCliente',
    'agenda-servico',
    'agenda-data-filtro',
    "mudarTela('agenda'",
    'selecionarCliente',
    'salvarAgendamento'
]
partes=[]
for termo in termos:
    pos=html.find(termo)
    partes.append('\n\n===== '+termo+' =====\n')
    if pos<0:
        partes.append('NAO ENCONTRADO\n')
        continue
    ini=max(0,pos-1600); fim=min(len(html),pos+5000)
    partes.append(html[ini:fim])
Path('.github/diagnostico-agenda-prefill-v52.txt').write_text(''.join(partes),encoding='utf-8')
