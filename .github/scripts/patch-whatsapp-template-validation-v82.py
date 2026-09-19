from pathlib import Path
import re

mod=Path('whatsapp-automacoes-v77.js')
idx=Path('index.html')
sw=Path('service-worker.js')

js=mod.read_text(encoding='utf-8')
html=idx.read_text(encoding='utf-8')
swtxt=sw.read_text(encoding='utf-8')

start=js.index("  async function loadTemplates(){")
end=js.index("\n\n  async function loadRules(){",start)
if start<0 or end<0:
    raise SystemExit('loadTemplates nao encontrado')

new_load=r'''  async function loadTemplates(){
    const {data,error}=await db().from('whatsapp_templates_operacionais')
      .select('tipo,template_codigo,language_code,status_meta,ativo,variaveis_body,validacao_ok,validacao_detalhe,ultima_validacao_em,meta_category,meta_body_vars_count')
      .eq('empresa_id',empresaId());
    if(error)throw error;

    const map=new Map((data||[]).map(r=>[r.tipo,r]));
    const types=[
      ['CONFIRMACAO','Confirmação'],
      ['LEMBRETE','Lembrete'],
      ['CANCELAMENTO','Cancelamento'],
      ['REAGENDAMENTO','Reagendamento']
    ];

    document.getElementById('wa77-templates').innerHTML=types.map(([t,n])=>{
      const r=map.get(t)||{};
      const s=slug(t);
      const vars=Array.isArray(r.variaveis_body)?r.variaveis_body:[];
      const valid=!!r.validacao_ok;
      const badge=valid?'VALIDADO':(r.status_meta||'NÃO VALIDADO');
      const detalhe=r.validacao_detalhe||'Salve o template e valide na Meta antes de usar na automação.';
      const metaInfo=[
        r.meta_category?('Categoria: '+r.meta_category):null,
        Number.isFinite(Number(r.meta_body_vars_count))?('Variáveis Meta: '+Number(r.meta_body_vars_count)):null,
        r.ultima_validacao_em?('Validado em: '+fmt(r.ultima_validacao_em)):null
      ].filter(Boolean).join(' · ');

      return '<div class="wa77-rule">'+
        '<div class="wa77-head"><b>'+n+'</b><span class="wa77-badge" style="'+(valid?'background:#f0fff4;color:#2f855a':'')+'">'+esc(badge)+'</span></div>'+
        '<div class="wa77-fields">'+
          '<div class="wa77-field"><label>Nome na Meta</label><input type="text" id="wa77-tpl-code-'+s+'" value="'+esc(r.template_codigo||'')+'"></div>'+
          '<div class="wa77-field"><label>Idioma</label><input type="text" id="wa77-tpl-lang-'+s+'" value="'+esc(r.language_code||'pt_BR')+'"></div>'+
        '</div>'+
        '<div style="margin-top:10px"><div class="wa77-field"><label>Variáveis do corpo do template</label></div>'+
          '<p style="margin:3px 0 0">A ordem abaixo corresponde a {{1}}, {{2}}, {{3}}... do template aprovado na Meta.</p>'+
          '<div class="wa77-vars" id="wa77-tpl-vars-'+s+'">'+vars.map((v,i)=>templateVarRow(t,v,i)).join('')+'</div>'+
          '<div class="wa77-actions"><button type="button" class="wa77-btn alt" data-act="add-template-var" data-tipo="'+t+'">+ Adicionar variável</button></div>'+
        '</div>'+
        '<div class="wa77-note" style="'+(valid?'background:#f0fff4;border-color:#9ae6b4;color:#276749':'')+'">'+esc(detalhe)+(metaInfo?'<br>'+esc(metaInfo):'')+'</div>'+
        '<div class="wa77-actions">'+
          '<label class="wa77-switch"><input type="checkbox" id="wa77-tpl-active-'+s+'" '+(r.ativo?'checked':'')+'> Ativo</label>'+
          '<button class="wa77-btn" data-act="save-template" data-tipo="'+t+'">Salvar template</button>'+
          '<button class="wa77-btn alt" data-act="validate-template" data-tipo="'+t+'">Validar na Meta</button>'+
          '<span class="wa77-msg" id="wa77-tpl-msg-'+s+'"></span>'+
        '</div>'+
      '</div>';
    }).join('');
  }'''

js=js[:start]+new_load+js[end:]

old="""      if(a==='save-template'){
        const t=b.dataset.tipo,s=slug(t);
        const vars=[...document.querySelectorAll('[data-tpl-var="'+t+'"]')].map(x=>x.value).filter(Boolean);
        if(new Set(vars.map((v,i)=>v+'#'+i)).size!==vars.length){}
        const codigo=document.getElementById('wa77-tpl-code-'+s).value.trim();
        if(!codigo)return alert('Informe o nome do template aprovado na Meta.');
        const {error}=await db().rpc('salvar_template_whatsapp_operacional_v2',{
          p_empresa_id:empresaId(),
          p_tipo:t,
          p_template_codigo:codigo,
          p_language_code:document.getElementById('wa77-tpl-lang-'+s).value.trim()||'pt_BR',
          p_ativo:document.getElementById('wa77-tpl-active-'+s).checked,
          p_variaveis_body:vars
        });
        if(error)throw error;
        await loadTemplates();
      }"""
new=r"""      if(a==='save-template'){
        const t=b.dataset.tipo,s=slug(t);
        const vars=[...document.querySelectorAll('[data-tpl-var="'+t+'"]')].map(x=>x.value).filter(Boolean);
        const codigo=document.getElementById('wa77-tpl-code-'+s).value.trim();
        if(!codigo)return alert('Informe o nome do template aprovado na Meta.');
        const msg=document.getElementById('wa77-tpl-msg-'+s);
        if(msg)msg.textContent='Salvando...';
        const {error}=await db().rpc('salvar_template_whatsapp_operacional_v2',{
          p_empresa_id:empresaId(),
          p_tipo:t,
          p_template_codigo:codigo,
          p_language_code:document.getElementById('wa77-tpl-lang-'+s).value.trim()||'pt_BR',
          p_ativo:document.getElementById('wa77-tpl-active-'+s).checked,
          p_variaveis_body:vars
        });
        if(error)throw error;
        if(msg)msg.textContent='Salvo. Valide novamente na Meta.';
        await loadTemplates();
      }
      if(a==='validate-template'){
        const t=b.dataset.tipo,s=slug(t),msg=document.getElementById('wa77-tpl-msg-'+s);
        if(msg)msg.textContent='Validando na Meta...';
        const {data,error}=await db().functions.invoke('whatsapp-validar-template',{
          body:{empresa_id:empresaId(),tipo:t}
        });
        if(error)throw error;
        if(msg)msg.textContent=data?.ok?'Template validado.':(data?.detail||'Template não compatível.');
        await loadTemplates();
      }"""
if old not in js:
    raise SystemExit('acoes template nao encontradas')
js=js.replace(old,new,1)

mod.write_text(js,encoding='utf-8')

html=html.replace("s.src='./whatsapp-automacoes-v77.js?v=81';","s.src='./whatsapp-automacoes-v77.js?v=82';",1)
idx.write_text(html,encoding='utf-8')

swtxt,n=re.subn(
    r"const CACHE_VERSION = '[^']+';",
    "const CACHE_VERSION = 'simpla-shell-v82-template-validation';",
    swtxt,
    count=1
)
if n!=1: raise SystemExit('cache version nao encontrada')
sw.write_text(swtxt,encoding='utf-8')
