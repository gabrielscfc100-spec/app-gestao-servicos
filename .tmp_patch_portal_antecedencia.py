from pathlib import Path
p=Path('index.html')
s=p.read_text(encoding='utf-8')
repls=[]
repls.append(("        let whatsappEmpresa = DataStore.getText('simpla_whatsapp_empresa', '');\n", "        let whatsappEmpresa = DataStore.getText('simpla_whatsapp_empresa', '');\n        let cancelamentoPortalAntecedenciaMinutos = 60;\n"))
repls.append(("            if(row.mensagem_aniversario_mes != null) mensagemAniversarioMes = row.mensagem_aniversario_mes;\n            if(row.whatsapp_empresa != null) {", "            if(row.mensagem_aniversario_mes != null) mensagemAniversarioMes = row.mensagem_aniversario_mes;\n            if(row.cancelamento_portal_antecedencia_minutos != null) cancelamentoPortalAntecedenciaMinutos = Math.max(0, Number(row.cancelamento_portal_antecedencia_minutos || 0));\n            if(row.whatsapp_empresa != null) {"))
repls.append(("                    whatsapp_empresa: whatsappEmpresa || null,\n", "                    whatsapp_empresa: whatsappEmpresa || null,\n                    cancelamento_portal_antecedencia_minutos: Math.max(0, Number(cancelamentoPortalAntecedenciaMinutos || 0)),\n"))
repls.append(("        function atualizarUIConfiguracoesCloud() {\n            carregarConfigExpedienteUI();", "        function atualizarUIConfiguracoesCloud() {\n            carregarConfigExpedienteUI();\n            const portalAntecedenciaEl = document.getElementById('cfg-portal-antecedencia');\n            if(portalAntecedenciaEl) portalAntecedenciaEl.value = String(Math.max(0, Number(cancelamentoPortalAntecedenciaMinutos || 0)));"))
anchor="</p></div><button class=\"btn-salvar\" style=\"margin-bottom:24px;\" onclick=\"salvarConfigConfirmacaoAutomatica()\"> Salvar Confirmação e WhatsApp</button><hr style=\"border:0;border-top:1px solid #e2e8f0;margin:24px 0;\"><h3 style=\"color: var(--cor-accent);\">Comissões</h3>"
insert="</p></div><button class=\"btn-salvar\" style=\"margin-bottom:24px;\" onclick=\"salvarConfigConfirmacaoAutomatica()\"> Salvar Confirmação e WhatsApp</button><div class=\"section-box-cfg\" style=\"margin-top:12px;\"><h4>Cancelamento e reagendamento pelo Portal</h4><div class=\"form-group\" style=\"margin-bottom:8px;max-width:360px;\"><label>Antecedência mínima (minutos)</label><input type=\"number\" id=\"cfg-portal-antecedencia\" min=\"0\" step=\"1\" value=\"60\"></div><p style=\"font-size:11px;color:#718096;margin:0 0 12px;text-transform:none;\">Define até quantos minutos antes do atendimento o cliente poderá cancelar ou reagendar pelo Portal. Use 0 para permitir até o horário do atendimento.</p><button class=\"btn-salvar\" type=\"button\" onclick=\"salvarConfigPortalAntecedencia()\">Salvar regra do Portal</button></div><hr style=\"border:0;border-top:1px solid #e2e8f0;margin:24px 0;\"><h3 style=\"color: var(--cor-accent);\">Comissões</h3>"
repls.append((anchor,insert))
fn_anchor="        function rotuloStatusAgendamento(status) {"
fn="""        async function salvarConfigPortalAntecedencia() {
            if(!validarAcessoPerfil('configuracoes','Somente administradores podem alterar as Configurações.')) return;
            const el = document.getElementById('cfg-portal-antecedencia');
            let valor = Number(el?.value ?? 60);
            if(!Number.isFinite(valor) || valor < 0) valor = 60;
            valor = Math.floor(valor);
            cancelamentoPortalAntecedenciaMinutos = valor;
            if(el) el.value = String(valor);
            salvarStorage();
            await persistirConfiguracoesCloud();
            await registrarAuditoria('CONFIGURACOES','ANTECEDENCIA_PORTAL_ALTERADA',empresaAtual.id,{minutos:valor});
            alert(`Regra do Portal salva: cancelamento e reagendamento permitidos até ${valor} minuto${valor === 1 ? '' : 's'} antes do atendimento.`);
        }

"""+fn_anchor
repls.append((fn_anchor,fn))
for old,new in repls:
    if old not in s:
        raise SystemExit('ANCHOR_NOT_FOUND: '+old[:120])
    s=s.replace(old,new,1)
# sanity checks
for needle in ['cfg-portal-antecedencia','salvarConfigPortalAntecedencia','cancelamento_portal_antecedencia_minutos: Math.max']:
    if needle not in s: raise SystemExit('VALIDATION_FAILED '+needle)
p.write_text(s,encoding='utf-8')
