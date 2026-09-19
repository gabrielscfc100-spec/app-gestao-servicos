from pathlib import Path
import re

idx=Path('index.html')
sw=Path('service-worker.js')
html=idx.read_text(encoding='utf-8')

# 1) Campos no cadastro novo
old_new='<div class="form-group" id="group-cli-telefone"><label for="cli-telefone">WhatsApp</label><input type="tel" id="cli-telefone" placeholder="00 9 1234-5678" maxlength="14" oninput="mascararWhatsapp(event)"></div>'
new_new=old_new+'''<div class="form-group" id="group-cli-whatsapp-preferencia"><label for="cli-whatsapp-preferencia">Mensagens pelo WhatsApp</label><select id="cli-whatsapp-preferencia" style="width:100%;padding:10px;border:1px solid #cbd5e0;border-radius:4px;"><option value="NAO_AUTORIZADO">Não autorizado</option><option value="AUTORIZADO">Autorizado para mensagens operacionais</option><option value="BLOQUEADO">Não enviar WhatsApp</option></select><small style="display:block;margin-top:5px;color:#718096;text-transform:none;line-height:1.4;">A automação só enviará mensagens quando houver autorização explícita. “Não enviar WhatsApp” bloqueia qualquer automação para este cliente.</small></div>'''
if old_new not in html: raise SystemExit('campo novo telefone nao encontrado')
html=html.replace(old_new,new_new,1)

# 2) Campo no modal editar
old_edit='<div class="form-group"><label>WhatsApp</label><input type="tel" id="edit-cli-telefone" placeholder="00 9 1234-5678" maxlength="14" oninput="mascararWhatsapp(event)"></div>'
new_edit=old_edit+'''<div class="form-group"><label>Mensagens pelo WhatsApp</label><select id="edit-cli-whatsapp-preferencia" style="width:100%;padding:10px;border:1px solid #cbd5e0;border-radius:4px;"><option value="NAO_AUTORIZADO">Não autorizado</option><option value="AUTORIZADO">Autorizado para mensagens operacionais</option><option value="BLOQUEADO">Não enviar WhatsApp</option></select><small id="edit-cli-whatsapp-status" style="display:block;margin-top:5px;color:#718096;text-transform:none;line-height:1.4;"></small></div>'''
if old_edit not in html: raise SystemExit('campo edit telefone nao encontrado')
html=html.replace(old_edit,new_edit,1)

# 3) Cloud -> local
old_map="""                telefone: row.telefone || '',
                aniversario: row.aniversario || '',"""
new_map="""                telefone: row.telefone || '',
                whatsappPermitido: row.whatsapp_permitido === true,
                whatsappBloqueado: row.whatsapp_bloqueado === true,
                whatsappConsentimentoEm: row.whatsapp_consentimento_em || null,
                whatsappConsentimentoOrigem: row.whatsapp_consentimento_origem || null,
                aniversario: row.aniversario || '',"""
if old_map not in html: raise SystemExit('map cloud local nao encontrado')
html=html.replace(old_map,new_map,1)

# 4) SELECT clientes
old_sel=".select('id,empresa_id,codigo,nome,sobrenome,telefone,aniversario,email,rua,bairro,cidade,instagram,tiktok,facebook,twitter,observacoes,responsavel_cliente_id,responsavel_vinculo,criado_em,atualizado_em')"
new_sel=".select('id,empresa_id,codigo,nome,sobrenome,telefone,whatsapp_permitido,whatsapp_bloqueado,whatsapp_consentimento_em,whatsapp_consentimento_origem,aniversario,email,rua,bairro,cidade,instagram,tiktok,facebook,twitter,observacoes,responsavel_cliente_id,responsavel_vinculo,criado_em,atualizado_em')"
if old_sel not in html: raise SystemExit('select clientes nao encontrado')
html=html.replace(old_sel,new_sel,1)

# 5) Captura preferência no cadastro
old_obs="""            const obs = configCampos.obs ? document.getElementById('cli-obs').value.trim() : '';

            const nomeFormatado"""
new_obs="""            const obs = configCampos.obs ? document.getElementById('cli-obs').value.trim() : '';
            const whatsappPreferencia = document.getElementById('cli-whatsapp-preferencia')?.value || 'NAO_AUTORIZADO';

            const nomeFormatado"""
if old_obs not in html: raise SystemExit('cadastro obs anchor nao encontrado')
html=html.replace(old_obs,new_obs,1)

old_dados="const dados = { nome: nomeFormatado, sobrenome: sobrenomeFormatado, telefone, aniversario, email, rua, bairro, cidade, instagram, tiktok, facebook, twitter, obs };"
new_dados="const dados = { nome: nomeFormatado, sobrenome: sobrenomeFormatado, telefone, aniversario, email, rua, bairro, cidade, instagram, tiktok, facebook, twitter, obs, whatsappPreferencia };"
if old_dados not in html: raise SystemExit('dados novo cliente nao encontrado')
html=html.replace(old_dados,new_dados,1)

# 6) Após insert, salva preferência via RPC e usa estado no objeto local
old_insert="""                    const clienteObj = clienteCloudParaLocal(data);
                    clientes.push(clienteObj);"""
new_insert="""                    const pref = dados.whatsappPreferencia || 'NAO_AUTORIZADO';
                    const permitido = pref === 'AUTORIZADO';
                    const bloqueado = pref === 'BLOQUEADO';
                    const { error: prefError } = await CloudDB.rpc('salvar_preferencia_whatsapp_cliente',{
                        p_cliente_id:data.id,
                        p_permitido:permitido,
                        p_bloqueado:bloqueado,
                        p_origem:'CADASTRO'
                    });
                    if(prefError) throw prefError;

                    const clienteObj = clienteCloudParaLocal({
                        ...data,
                        whatsapp_permitido: permitido,
                        whatsapp_bloqueado: bloqueado,
                        whatsapp_consentimento_em: permitido ? new Date().toISOString() : null,
                        whatsapp_consentimento_origem: (permitido || bloqueado) ? 'CADASTRO' : null
                    });
                    clientes.push(clienteObj);"""
if old_insert not in html: raise SystemExit('insert cliente anchor nao encontrado')
html=html.replace(old_insert,new_insert,1)

# 7) limpar form
old_clean="""            ['cli-nome', 'cli-sobrenome', 'cli-telefone', 'cli-aniversario', 'cli-email', 'cli-rua', 'cli-bairro', 'cli-cidade', 'cli-instagram', 'cli-tiktok', 'cli-facebook', 'cli-twitter', 'cli-obs'].forEach(id => {
                const el = document.getElementById(id);
                if(el) el.value = '';
            });"""
new_clean="""            ['cli-nome', 'cli-sobrenome', 'cli-telefone', 'cli-aniversario', 'cli-email', 'cli-rua', 'cli-bairro', 'cli-cidade', 'cli-instagram', 'cli-tiktok', 'cli-facebook', 'cli-twitter', 'cli-obs'].forEach(id => {
                const el = document.getElementById(id);
                if(el) el.value = '';
            });
            const pref = document.getElementById('cli-whatsapp-preferencia');
            if(pref) pref.value = 'NAO_AUTORIZADO';"""
if old_clean not in html: raise SystemExit('limpar form anchor nao encontrado')
html=html.replace(old_clean,new_clean,1)

# 8) popular edição
old_pop="""            document.getElementById('edit-cli-telefone').value = c.telefone || '';
            document.getElementById('edit-cli-aniversario').value = c.aniversario || '';"""
new_pop="""            document.getElementById('edit-cli-telefone').value = c.telefone || '';
            const prefWhatsapp = document.getElementById('edit-cli-whatsapp-preferencia');
            if(prefWhatsapp) prefWhatsapp.value = c.whatsappBloqueado ? 'BLOQUEADO' : (c.whatsappPermitido ? 'AUTORIZADO' : 'NAO_AUTORIZADO');
            const statusWhatsapp = document.getElementById('edit-cli-whatsapp-status');
            if(statusWhatsapp) {
                statusWhatsapp.textContent = c.whatsappBloqueado
                    ? 'Envios automáticos bloqueados para este cliente.'
                    : (c.whatsappPermitido
                        ? 'Autorização registrada' + (c.whatsappConsentimentoEm ? ' em ' + new Date(c.whatsappConsentimentoEm).toLocaleString('pt-BR') : '') + '.'
                        : 'Sem autorização registrada para mensagens automáticas.');
            }
            document.getElementById('edit-cli-aniversario').value = c.aniversario || '';"""
if old_pop not in html: raise SystemExit('popular edicao anchor nao encontrado')
html=html.replace(old_pop,new_pop,1)

# 9) captura edição
old_edit_obs="""                twitter: document.getElementById('edit-cli-twitter').value.trim(),
                obs: document.getElementById('edit-cli-obs').value.trim()
            };"""
new_edit_obs="""                twitter: document.getElementById('edit-cli-twitter').value.trim(),
                obs: document.getElementById('edit-cli-obs').value.trim(),
                whatsappPreferencia: document.getElementById('edit-cli-whatsapp-preferencia')?.value || 'NAO_AUTORIZADO'
            };"""
if old_edit_obs not in html: raise SystemExit('dados edit anchor nao encontrado')
html=html.replace(old_edit_obs,new_edit_obs,1)

# 10) Após update, salva preferência e ajusta local
old_update="""                    const atualizado = clienteCloudParaLocal(data);
                    const idx = clientes.findIndex(x => String(x.id) === String(id));"""
new_update="""                    const pref = dadosAtualizados.whatsappPreferencia || 'NAO_AUTORIZADO';
                    const permitido = pref === 'AUTORIZADO';
                    const bloqueado = pref === 'BLOQUEADO';
                    const { error: prefError } = await CloudDB.rpc('salvar_preferencia_whatsapp_cliente',{
                        p_cliente_id:id,
                        p_permitido:permitido,
                        p_bloqueado:bloqueado,
                        p_origem:'CADASTRO'
                    });
                    if(prefError) throw prefError;

                    const atualizado = clienteCloudParaLocal({
                        ...data,
                        whatsapp_permitido: permitido,
                        whatsapp_bloqueado: bloqueado,
                        whatsapp_consentimento_em: permitido ? new Date().toISOString() : null,
                        whatsapp_consentimento_origem: (permitido || bloqueado) ? 'CADASTRO' : null
                    });
                    const idx = clientes.findIndex(x => String(x.id) === String(id));"""
if old_update not in html: raise SystemExit('update cliente anchor nao encontrado')
html=html.replace(old_update,new_update,1)

idx.write_text(html,encoding='utf-8')

swtxt=sw.read_text(encoding='utf-8')
swtxt,n=re.subn(r"const CACHE_VERSION = '[^']+';","const CACHE_VERSION = 'simpla-shell-v83-whatsapp-consent';",swtxt,count=1)
if n!=1: raise SystemExit('cache version nao encontrada')
sw.write_text(swtxt,encoding='utf-8')
