from pathlib import Path

path = Path('index.html')
text = path.read_text(encoding='utf-8')
original = text

marker = '<input type="hidden" id="bloqueio-slot-hora"><div class="form-group"><label>Selecione o Tipo de Bloqueio *</label>'
replacement = '<input type="hidden" id="bloqueio-slot-hora"><div class="form-group" id="bloqueio-profissional-grupo" style="display:none;"><label>Profissional *</label><select id="bloqueio-profissional" style="padding:10px;border:1px solid #cbd5e0;border-radius:4px;width:100%;"><option value="">Selecione o profissional</option></select></div><div class="form-group"><label>Selecione o Tipo de Bloqueio *</label>'
if marker not in text:
    raise SystemExit('Marcador do modal de bloqueio não encontrado.')
text = text.replace(marker, replacement, 1)

old_helper = """        function obterProfissionalAgendaSelecionado() {
            return document.getElementById('agenda-profissional-filtro')?.value || '';
        }

        function preencherDuracaoPorServicoProfissional() {"""
new_helper = """        function obterProfissionalAgendaSelecionado() {
            return document.getElementById('agenda-profissional-filtro')?.value || '';
        }

        function obterProfissionalVinculadoUsuarioAtual() {
            if(!usuarioAtual?.id) return null;
            return profissionais.find(p =>
                p.ativo !== false &&
                String(p.usuarioId || '') === String(usuarioAtual.id)
            ) || null;
        }

        function prepararProfissionalBloqueio() {
            const grupo = document.getElementById('bloqueio-profissional-grupo');
            const select = document.getElementById('bloqueio-profissional');
            if(!grupo || !select) return;

            if(usuarioEhAdmin()) {
                const atual = obterProfissionalAgendaSelecionado();
                const ativos = profissionais.filter(p => p.ativo !== false);
                select.innerHTML = '<option value="">Selecione o profissional</option>' +
                    ativos.map(p => `<option value="${p.id}">${p.nome}</option>`).join('');
                if(atual && ativos.some(p => String(p.id) === String(atual))) select.value = atual;
                grupo.style.display = 'block';
            } else {
                select.innerHTML = '<option value=""></option>';
                select.value = '';
                grupo.style.display = 'none';
            }
        }

        function obterProfissionalParaBloqueio() {
            if(usuarioEhAdmin()) {
                return document.getElementById('bloqueio-profissional')?.value || '';
            }
            return obterProfissionalVinculadoUsuarioAtual()?.id || '';
        }

        function preencherDuracaoPorServicoProfissional() {"""
if old_helper not in text:
    raise SystemExit('Helper da agenda não encontrado.')
text = text.replace(old_helper, new_helper, 1)

old_open = """            document.getElementById('modal-bloqueio-horario-txt').innerText = `Horário: ${horario} em ${dataFmt}`;
            document.getElementById('modal-bloqueio').classList.add('active');"""
new_open = """            document.getElementById('modal-bloqueio-horario-txt').innerText = `Horário: ${horario} em ${dataFmt}`;
            prepararProfissionalBloqueio();
            document.getElementById('modal-bloqueio').classList.add('active');"""
if old_open not in text:
    raise SystemExit('Abertura do modal não encontrada.')
text = text.replace(old_open, new_open, 1)

old_confirm = """            const profissionalId = obterProfissionalAgendaSelecionado();
            if(!profissionalId) {
                alert('Selecione um profissional específico antes de bloquear um horário.');
                fecharModalBloqueio();
                return;
            }"""
new_confirm = """            const profissionalId = obterProfissionalParaBloqueio();
            if(!profissionalId) {
                alert(usuarioEhAdmin()
                    ? 'Selecione o profissional antes de bloquear o horário.'
                    : 'Sua conta não está vinculada a um profissional ativo. Solicite ao administrador que faça o vínculo em Configurações.');
                if(!usuarioEhAdmin()) fecharModalBloqueio();
                return;
            }"""
if old_confirm not in text:
    raise SystemExit('Validação antiga do bloqueio não encontrada.')
text = text.replace(old_confirm, new_confirm, 1)

if text == original:
    raise SystemExit('Nenhuma alteração gerada.')

path.write_text(text, encoding='utf-8')

final = path.read_text(encoding='utf-8')
required = [
    'id="bloqueio-profissional-grupo"',
    'function obterProfissionalVinculadoUsuarioAtual()',
    'function prepararProfissionalBloqueio()',
    'function obterProfissionalParaBloqueio()',
    'const profissionalId = obterProfissionalParaBloqueio();',
]
missing = [item for item in required if item not in final]
if missing:
    raise SystemExit(f'Validação falhou. Ausentes: {missing}')

print('Correção aplicada e validada no index.html.')
