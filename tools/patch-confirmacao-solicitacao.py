from pathlib import Path

p = Path('index.html')
s = p.read_text(encoding='utf-8')

old_prompt = "if(!confirm('Tem certeza que deseja liberar este horário (cancelar agendamento)?')) return;"
new_prompt = "const ehSolicitacao = String(agendamento?.status || '').toUpperCase() === 'SOLICITADO';\n            if(!confirm(ehSolicitacao ? 'Tem certeza que deseja recusar esta solicitação? O horário será liberado.' : 'Tem certeza que deseja liberar este horário (cancelar agendamento)?')) return;"
if old_prompt not in s:
    raise SystemExit('prompt de cancelamento alvo nao encontrado')
s = s.replace(old_prompt, new_prompt, 1)

old_button = "<button class=\"btn-excluir-tabela\" style=\"flex:1;font-size:12px;padding:6px;\" onclick=\"cancelarAgendamento('${agendamentoOcupado.id}')\">Liberar Horário</button>"
new_button = "<button class=\"btn-excluir-tabela\" style=\"flex:1;font-size:12px;padding:6px;\" onclick=\"cancelarAgendamento('${agendamentoOcupado.id}')\">${String(agendamentoOcupado.status || '').toUpperCase() === 'SOLICITADO' ? 'Recusar solicitação' : 'Liberar Horário'}</button>"
if old_button not in s:
    raise SystemExit('botao liberar horario alvo nao encontrado')
s = s.replace(old_button, new_button, 1)

p.write_text(s, encoding='utf-8')
print('patch aplicado')
