from pathlib import Path

path = Path('index.html')
text = path.read_text(encoding='utf-8')
original = text

old_options = """                select.innerHTML = '<option value=\"\">Selecione o profissional</option>' +
                    ativos.map(p => `<option value=\"${p.id}\">${p.nome}</option>`).join('');"""
new_options = """                select.innerHTML = '<option value=\"\">Selecione o profissional</option>' +
                    '<option value=\"__todos__\">Selecionar todos os profissionais</option>' +
                    ativos.map(p => `<option value=\"${p.id}\">${p.nome}</option>`).join('');"""
if old_options not in text:
    raise SystemExit('Trecho das opções de profissionais não encontrado.')
text = text.replace(old_options, new_options, 1)

old_confirm = """        async function confirmarBloqueio() {
            const horario = document.getElementById('bloqueio-slot-hora').value;
            const data = document.getElementById('agenda-data-filtro').value;
            const profissionalId = obterProfissionalParaBloqueio();
            if(!profissionalId) {
                alert(usuarioEhAdmin()
                    ? 'Selecione o profissional antes de bloquear o horário.'
                    : 'Sua conta não está vinculada a um profissional ativo. Solicite ao administrador que faça o vínculo em Configurações.');
                if(!usuarioEhAdmin()) fecharModalBloqueio();
                return;
            }
            if (data < obterHojeLocal()) { alert('Não é possível bloquear horários em datas retroativas.'); return; }
            if(horarioJaUltrapassado(data, horario)) {
                alert('Este horário já foi ultrapassado e não pode mais ser bloqueado.');
                fecharModalBloqueio();
                renderizarAgenda();
                return;
            }
            const tipo = document.getElementById('bloqueio-tipo').value;

            try {
                if(AGENDA_CLOUD_ATIVO && CloudDB && empresaAtual?.cloud) {
                    const payload = {
                        empresa_id: empresaAtual.id,
                        data: tipo === 'permanente' ? null : data,
                        horario,
                        tipo,
                        profissional_id: profissionalId
                    };
                    const { data: row, error } = await CloudDB.from('bloqueios_agenda').insert(payload).select().single();
                    if(error) throw error;
                    bloqueios.push(bloqueioCloudParaLocal(row));
                    salvarCacheAgendaCloud();
                } else {
                    bloqueios.push({ id: Date.now(), data, horario, tipo, profissionalId });
                    salvarStorage();
                }
                fecharModalBloqueio();
                renderizarAgenda();
                const bloqueioCriado = bloqueios[bloqueios.length - 1];
                await registrarAuditoria('AGENDA','HORARIO_BLOQUEADO',bloqueioCriado?.id || null,{data:bloqueioCriado?.data || data,horario,tipo});
                alert('Horário bloqueado com sucesso!');
            } catch(err) {
                console.error(err);
                alert(`Não foi possível bloquear o horário: ${err?.message || 'erro desconhecido'}`);
            }
        }"""

new_confirm = """        async function confirmarBloqueio() {
            const horario = document.getElementById('bloqueio-slot-hora').value;
            const data = document.getElementById('agenda-data-filtro').value;
            const profissionalId = obterProfissionalParaBloqueio();
            if(!profissionalId) {
                alert(usuarioEhAdmin()
                    ? 'Selecione o profissional antes de bloquear o horário.'
                    : 'Sua conta não está vinculada a um profissional ativo. Solicite ao administrador que faça o vínculo em Configurações.');
                if(!usuarioEhAdmin()) fecharModalBloqueio();
                return;
            }

            const profissionaisAlvo = usuarioEhAdmin() && profissionalId === '__todos__'
                ? profissionais.filter(p => p.ativo !== false).map(p => p.id)
                : [profissionalId];

            if(!profissionaisAlvo.length) {
                alert('Não há profissionais ativos disponíveis para aplicar o bloqueio.');
                return;
            }

            if (data < obterHojeLocal()) { alert('Não é possível bloquear horários em datas retroativas.'); return; }
            if(horarioJaUltrapassado(data, horario)) {
                alert('Este horário já foi ultrapassado e não pode mais ser bloqueado.');
                fecharModalBloqueio();
                renderizarAgenda();
                return;
            }
            const tipo = document.getElementById('bloqueio-tipo').value;

            try {
                let bloqueiosCriados = [];

                if(AGENDA_CLOUD_ATIVO && CloudDB && empresaAtual?.cloud) {
                    const payloads = profissionaisAlvo.map(idProfissional => ({
                        empresa_id: empresaAtual.id,
                        data: tipo === 'permanente' ? null : data,
                        horario,
                        tipo,
                        profissional_id: idProfissional
                    }));
                    const { data: rows, error } = await CloudDB.from('bloqueios_agenda').insert(payloads).select();
                    if(error) throw error;
                    bloqueiosCriados = (rows || []).map(bloqueioCloudParaLocal);
                    bloqueios.push(...bloqueiosCriados);
                    salvarCacheAgendaCloud();
                } else {
                    const baseId = Date.now();
                    bloqueiosCriados = profissionaisAlvo.map((idProfissional, indice) => ({
                        id: baseId + indice,
                        data,
                        horario,
                        tipo,
                        profissionalId: idProfissional
                    }));
                    bloqueios.push(...bloqueiosCriados);
                    salvarStorage();
                }

                fecharModalBloqueio();
                renderizarAgenda();

                for(const bloqueioCriado of bloqueiosCriados) {
                    await registrarAuditoria('AGENDA','HORARIO_BLOQUEADO',bloqueioCriado?.id || null,{
                        data: bloqueioCriado?.data || data,
                        horario,
                        tipo,
                        profissionalId: bloqueioCriado?.profissionalId || null,
                        selecaoTodos: profissionalId === '__todos__'
                    });
                }

                alert(profissionalId === '__todos__'
                    ? `Horário bloqueado com sucesso para ${profissionaisAlvo.length} profissional(is)!`
                    : 'Horário bloqueado com sucesso!');
            } catch(err) {
                console.error(err);
                alert(`Não foi possível bloquear o horário: ${err?.message || 'erro desconhecido'}`);
            }
        }"""

if old_confirm not in text:
    raise SystemExit('Função confirmarBloqueio atual não encontrada.')
text = text.replace(old_confirm, new_confirm, 1)

if text == original:
    raise SystemExit('Nenhuma alteração foi produzida.')

required = [
    'Selecionar todos os profissionais',
    "profissionalId === '__todos__'",
    'const profissionaisAlvo =',
    'const payloads = profissionaisAlvo.map',
    'bloqueios.push(...bloqueiosCriados)',
]
missing = [item for item in required if item not in text]
if missing:
    raise SystemExit(f'Validação falhou. Ausentes: {missing}')

path.write_text(text, encoding='utf-8')
print('Patch de selecionar todos aplicado e validado.')
