from pathlib import Path

path = Path('index.html')
text = path.read_text(encoding='utf-8')
original = text

old = '''        function verificarBloqueioSlot(dataStr, horarioStr, profissionalId='') {
            const dataAtual = new Date(dataStr + 'T00:00:00');

            return bloqueios.find(b => {
                if(b.ativo === false) return false;

                // Bloqueios configuráveis v2
                if(bloqueioEhConfiguravel(b)) {
                    if(!bloqueioConfiguradoAplicaProfissional(b, profissionalId)) return false;
                    if(!bloqueioConfiguradoAplicaData(b, dataStr)) return false;
                    return bloqueioConfiguradoAplicaHorario(b, horarioStr);
                }

                // Compatibilidade com os bloqueios legados já existentes.
                if (b.horario !== horarioStr) return false;

                // Sem profissional = bloqueio global. Com profissional = aplica somente àquele profissional.
                if(b.profissionalId && (!profissionalId || String(b.profissionalId) !== String(profissionalId))) {
                    return false;
                }

                if (b.tipo === 'permanente') return true;

                const dataBloqueio = new Date(b.data + 'T00:00:00');

                if (b.tipo === 'dia') {
                    return b.data === dataStr;
                }

                if (b.tipo === 'semana') {
                    const [anoA, semA] = obterNumeroSemana(dataAtual);
                    const [anoB, semB] = obterNumeroSemana(dataBloqueio);
                    return anoA === anoB && semA === semB;
                }

                if (b.tipo === 'mes') {
                    return dataAtual.getFullYear() === dataBloqueio.getFullYear() &&
                           dataAtual.getMonth() === dataBloqueio.getMonth();
                }

                return false;
            });
        }'''

new = '''        function verificarBloqueioSlot(dataStr, horarioStr, profissionalId='') {
            const dataAtual = new Date(dataStr + 'T00:00:00');

            const bloqueioParaProfissional = (idProfissional='') => bloqueios.find(b => {
                if(b.ativo === false) return false;

                // Bloqueios configuráveis v2
                if(bloqueioEhConfiguravel(b)) {
                    if(!bloqueioConfiguradoAplicaProfissional(b, idProfissional)) return false;
                    if(!bloqueioConfiguradoAplicaData(b, dataStr)) return false;
                    return bloqueioConfiguradoAplicaHorario(b, horarioStr);
                }

                // Compatibilidade com os bloqueios legados já existentes.
                if (b.horario !== horarioStr) return false;

                // Sem profissional = bloqueio global. Com profissional = aplica somente àquele profissional.
                if(b.profissionalId && (!idProfissional || String(b.profissionalId) !== String(idProfissional))) {
                    return false;
                }

                if (b.tipo === 'permanente') return true;

                const dataBloqueio = new Date(b.data + 'T00:00:00');

                if (b.tipo === 'dia') {
                    return b.data === dataStr;
                }

                if (b.tipo === 'semana') {
                    const [anoA, semA] = obterNumeroSemana(dataAtual);
                    const [anoB, semB] = obterNumeroSemana(dataBloqueio);
                    return anoA === anoB && semA === semB;
                }

                if (b.tipo === 'mes') {
                    return dataAtual.getFullYear() === dataBloqueio.getFullYear() &&
                           dataAtual.getMonth() === dataBloqueio.getMonth();
                }

                return false;
            });

            // Quando um profissional está filtrado, mantém a regra individual normal.
            if(profissionalId) return bloqueioParaProfissional(profissionalId);

            // Na agenda geral, um bloqueio global continua prevalecendo.
            const bloqueioGlobal = bloqueioParaProfissional('');
            if(bloqueioGlobal) return bloqueioGlobal;

            // Se TODOS os profissionais ativos estiverem bloqueados no mesmo slot,
            // a agenda geral também deve mostrar o horário como bloqueado.
            const profissionaisAtivos = profissionais.filter(p => p.ativo !== false);
            if(!profissionaisAtivos.length) return null;

            const bloqueiosIndividuais = profissionaisAtivos.map(p => bloqueioParaProfissional(p.id));
            if(bloqueiosIndividuais.every(Boolean)) {
                return bloqueiosIndividuais[0] || null;
            }

            return null;
        }'''

if old not in text:
    raise SystemExit('Função verificarBloqueioSlot esperada não encontrada; nenhuma alteração aplicada.')

text = text.replace(old, new, 1)

if text == original:
    raise SystemExit('Nenhuma alteração gerada.')

path.write_text(text, encoding='utf-8')

final = path.read_text(encoding='utf-8')
required = [
    "const bloqueioParaProfissional = (idProfissional='') => bloqueios.find",
    "if(profissionalId) return bloqueioParaProfissional(profissionalId);",
    "const profissionaisAtivos = profissionais.filter(p => p.ativo !== false);",
    "if(bloqueiosIndividuais.every(Boolean))",
]
missing = [x for x in required if x not in final]
if missing:
    raise SystemExit(f'Validação falhou. Ausentes: {missing}')

print('Renderização da agenda geral corrigida para bloqueio de todos os profissionais.')
