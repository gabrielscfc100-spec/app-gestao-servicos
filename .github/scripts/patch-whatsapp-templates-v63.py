from pathlib import Path
import re

idx=Path('index.html')
sw=Path('service-worker.js')
html=idx.read_text(encoding='utf-8')

if 'simpla-whatsapp-templates-v63' in html:
    raise SystemExit('v63 ja aplicada')

marker='</body>'
if marker not in html:
    raise SystemExit('body nao encontrado')

block=r'''
<style id="simpla-whatsapp-templates-v63-css">
  .simpla-wa-tpl-v63{margin:0 0 18px;border:1px solid #dbe4ee;border-radius:12px;background:#fff;padding:16px;box-shadow:0 2px 5px rgba(15,23,42,.04);text-transform:none}
  .simpla-wa-tpl-v63 h3{margin:0;font-size:16px;color:#1a1c23}.simpla-wa-tpl-v63 p{margin:4px 0 0;font-size:11px;color:#718096;line-height:1.5;text-transform:none}
  .simpla-wa-tpl-v63-actions{display:flex;gap:8px;flex-wrap:wrap;margin:12px 0}
  .simpla-wa-tpl-v63-actions button{border:0;border-radius:7px;padding:9px 11px;cursor:pointer;font-size:9px;font-weight:900}
  .simpla-wa-tpl-v63-primary{background:#1a1c23;color:#fff}.simpla-wa-tpl-v63-secondary{background:#edf2f7;color:#2d3748}
  .simpla-wa-tpl-v63-grid{display:grid;grid-template-columns:1fr 1fr;gap:10px}
  .simpla-wa-tpl-v63-card{border:1px solid #e2e8f0;border-radius:9px;padding:12px;background:#f8fafc}
  .simpla-wa-tpl-v63-card h4{margin:0 0 8px;font-size:11px;color:#2d3748}
  .simpla-wa-tpl-v63-row{display:grid;grid-template-columns:minmax(0,2fr) 110px;gap:8px}
  .simpla-wa-tpl-v63-card label{display:block;font-size:8px;font-weight:900;color:#718096;margin-bottom:4px}
  .simpla-wa-tpl-v63-card input[type=text]{width:100%;padding:8px;border:1px solid #cbd5e0;border-radius:6px;text-transform:none;font-size:11px}
  .simpla-wa-tpl-v63-foot{margin-top:8px;display:flex;justify-content:space-between;align-items:center;gap:8px;flex-wrap:wrap}
  .simpla-wa-tpl-v63-status{font-size:9px;font-weight:900;color:#718096}.simpla-wa-tpl-v63-status.aprovado{color:#2f855a}.simpla-wa-tpl-v63-status.rejeitado{color:#c53030}
  .simpla-wa-tpl-v63-save{border:0;border-radius:6px;background:#2d3748;color:#fff;padding:7px 9px;cursor:pointer;font-size:8px;font-weight:900}
  .simpla-wa-tpl-v63-msg{font-size:10px;color:#718096;margin-top:10px;text-transform:none}
  @media(max-width:760px){.simpla-wa-tpl-v63-grid{grid-template-columns:1fr}.simpla-wa-tpl-v63-row{grid-template-columns:1fr}}
</style>
<script id="simpla-whatsapp-templates-v63">
(function(){
  const TIPOS=[
    ['CONFIRMACAO','Confirmação de agendamento'],
    ['LEMBRETE','Lembrete de agendamento'],
    ['CANCELAMENTO','Cancelamento'],
    ['REAGENDAMENTO','Reagendamento']
  ];
  function idTipo(t){return String(t).toLowerCase()}
  function garantir(){
    let box=document.getElementById('simpla-wa-tpl-v63');if(box)return box;
    const status=document.getElementById('simpla-wa-v62');
    const usuarios=document.getElementById('box-cfg-usuarios');
    const config=document.getElementById('configuracoes');
    if(!status&&!usuarios&&!config)return null;
    box=document.createElement('section');box.id='simpla-wa-tpl-v63';box.className='simpla-wa-tpl-v63';
    box.innerHTML='<div><h3>Templates operacionais do WhatsApp</h3><p>Mapeie os nomes dos templates aprovados na Meta. O SimplA não cria nem aprova templates automaticamente.</p></div><div class="simpla-wa-tpl-v63-actions"><button type="button" class="simpla-wa-tpl-v63-primary" onclick="validarConexaoWhatsAppV63()">Validar conexão</button><button type="button" class="simpla-wa-tpl-v63-secondary" onclick="carregarTemplatesWhatsAppV63()">Atualizar templates</button></div><div id="simpla-wa-tpl-v63-grid" class="simpla-wa-tpl-v63-grid"></div><div id="simpla-wa-tpl-v63-msg" class="simpla-wa-tpl-v63-msg"></div>';
    if(status)status.insertAdjacentElement('afterend',box);else if(usuarios)usuarios.insertAdjacentElement('beforebegin',box);else config.appendChild(box);
    return box;
  }
  function render(rows){
    const grid=document.getElementById('simpla-wa-tpl-v63-grid');if(!grid)return;
    const map=new Map((rows||[]).map(r=>[String(r.tipo).toUpperCase(),r]));
    grid.innerHTML=TIPOS.map(([tipo,nome])=>{
      const r=map.get(tipo)||{};const x=idTipo(tipo);const st=String(r.status_meta||'DESCONHECIDO').toUpperCase();
      return '<div class="simpla-wa-tpl-v63-card"><h4>'+nome+'</h4><div class="simpla-wa-tpl-v63-row"><div><label>NOME APROVADO NA META</label><input type="text" id="wa-tpl-'+x+'" value="'+String(r.template_codigo||'').replace(/"/g,'&quot;')+'" placeholder="ex.: simpla_confirmacao_agendamento"></div><div><label>IDIOMA</label><input type="text" id="wa-lang-'+x+'" value="'+String(r.language_code||'pt_BR').replace(/"/g,'&quot;')+'" placeholder="pt_BR"></div></div><div class="simpla-wa-tpl-v63-foot"><label style="display:flex;align-items:center;gap:7px;margin:0;font-size:9px;color:#4a5568"><input type="checkbox" id="wa-ativo-'+x+'" '+(r.ativo?'checked':'')+'> Ativo</label><span class="simpla-wa-tpl-v63-status '+st.toLowerCase()+'">'+st+'</span><button type="button" class="simpla-wa-tpl-v63-save" onclick="salvarTemplateWhatsAppV63(\''+tipo+'\')">Salvar</button></div></div>';
    }).join('');
  }
  async function pode(){
    if(typeof CloudDB==='undefined'||!CloudDB||typeof empresaAtual==='undefined'||!empresaAtual?.id)return false;
    const {data:perfil}=await CloudDB.rpc('perfil_na_empresa',{p_empresa_id:empresaAtual.id});
    if(String(perfil||'').toUpperCase()!=='ADMIN')return false;
    return typeof empresaPodeUsarRecurso==='function'?await empresaPodeUsarRecurso('whatsapp_operacional'):false;
  }
  async function carregar(){
    const box=garantir();if(!box)return;
    try{
      const ok=await pode();
      if(!ok){box.style.display='none';return}
      box.style.display='block';
      const {data,error}=await CloudDB.from('whatsapp_templates_operacionais').select('tipo,template_codigo,language_code,status_meta,ativo').eq('empresa_id',empresaAtual.id);
      if(error)throw error;render(Array.isArray(data)?data:[]);
      document.getElementById('simpla-wa-tpl-v63-msg').textContent='Os templates só serão usados após conexão ativa e aprovação na Meta.';
    }catch(err){console.error('Templates WhatsApp v63:',err);document.getElementById('simpla-wa-tpl-v63-msg').textContent='Não foi possível carregar os templates agora.'}
  }
  window.carregarTemplatesWhatsAppV63=carregar;
  window.salvarTemplateWhatsAppV63=async function(tipo){
    try{
      if(!await pode())return;
      const x=idTipo(tipo), codigo=document.getElementById('wa-tpl-'+x)?.value?.trim(), lang=document.getElementById('wa-lang-'+x)?.value?.trim()||'pt_BR', ativo=!!document.getElementById('wa-ativo-'+x)?.checked;
      const {error}=await CloudDB.rpc('salvar_template_whatsapp_operacional',{p_empresa_id:empresaAtual.id,p_tipo:tipo,p_template_codigo:codigo,p_language_code:lang,p_ativo:ativo});
      if(error)throw error;
      document.getElementById('simpla-wa-tpl-v63-msg').textContent='Template salvo. O status será validado com a Meta quando a integração estiver conectada.';
      await carregar();
    }catch(err){console.error(err);alert(err?.message||'Não foi possível salvar o template.')}
  };
  window.validarConexaoWhatsAppV63=async function(){
    const msg=document.getElementById('simpla-wa-tpl-v63-msg');
    try{
      if(!await pode())return;
      msg.textContent='Validando conexão com a Meta...';
      const {data,error}=await CloudDB.functions.invoke('whatsapp-validar-integracao',{body:{empresa_id:empresaAtual.id}});
      if(error)throw error;
      msg.textContent=data?.ok?'Conexão validada com sucesso.':'A integração ainda não está pronta para validação.';
      if(typeof carregarWhatsAppConfigV62==='function')await carregarWhatsAppConfigV62();
    }catch(err){
      console.error('Validar WhatsApp v63:',err);
      msg.textContent='A integração ainda não possui credencial Meta ativa ou a validação falhou.';
      if(typeof carregarWhatsAppConfigV62==='function')await carregarWhatsAppConfigV62();
    }
  };
  function instalar(){garantir();setTimeout(carregar,1100)}
  if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',()=>setTimeout(instalar,3300));else setTimeout(instalar,3300);
})();
</script>
'''
html=html.replace(marker,block+'\n'+marker,1)
idx.write_text(html,encoding='utf-8')

swtxt=sw.read_text(encoding='utf-8')
swtxt,n=re.subn(r"const CACHE_VERSION = '[^']+';","const CACHE_VERSION = 'simpla-shell-v63-whatsapp-templates';",swtxt,count=1)
if n!=1: raise SystemExit('cache version nao encontrada')
sw.write_text(swtxt,encoding='utf-8')
