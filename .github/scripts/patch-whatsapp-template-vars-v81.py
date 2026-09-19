from pathlib import Path
import re

mod=Path('whatsapp-automacoes-v77.js')
idx=Path('index.html')
sw=Path('service-worker.js')

js=mod.read_text(encoding='utf-8')
html=idx.read_text(encoding='utf-8')
swtxt=sw.read_text(encoding='utf-8')

# CSS para editor de variáveis
old_css=".wa77-msg{font-size:9px;color:#718096}.wa77-list{display:grid;gap:8px;margin-top:10px}"
new_css=".wa77-msg{font-size:9px;color:#718096}.wa77-vars{display:grid;gap:6px;margin-top:9px}.wa77-var-row{display:grid;grid-template-columns:42px minmax(0,1fr) auto auto auto;gap:6px;align-items:center}.wa77-var-pos{font-size:9px;font-weight:900;color:#718096;text-align:center}.wa77-var-btn{border:0;border-radius:6px;padding:7px 8px;background:#edf2f7;color:#4a5568;font-size:9px;font-weight:900;cursor:pointer}.wa77-var-btn.remove{background:#fff5f5;color:#c53030}.wa77-list{display:grid;gap:8px;margin-top:10px}"
if old_css not in js:
    raise SystemExit('css anchor nao encontrado')
js=js.replace(old_css,new_css,1)

old_media="@media(max-width:800px){.wa77-grid2,.wa77-fields{grid-template-columns:1fr}.wa77-kpis{grid-template-columns:1fr 1fr}}"
new_media="@media(max-width:800px){.wa77-grid2,.wa77-fields{grid-template-columns:1fr}.wa77-kpis{grid-template-columns:1fr 1fr}.wa77-var-row{grid-template-columns:36px minmax(0,1fr) auto auto auto}}"
js=js.replace(old_media,new_media,1)

# Helpers de variáveis antes de loadTemplates
anchor="  async function loadTemplates(){"
helpers=r'''  const TEMPLATE_VARS=[
    ['CLIENTE_NOME','Nome do cliente'],
    ['EMPRESA_NOME','Nome da empresa'],
    ['SERVICO_NOME','Serviço'],
    ['DATA','Data do agendamento'],
    ['HORARIO','Horário do agendamento'],
    ['PROFISSIONAL_NOME','Nome do profissional']
  ];

  function templateVarOptions(atual){
    return '<option value="">Selecione...</option>'+TEMPLATE_VARS.map(([v,n])=>'<option value="'+v+'" '+(v===atual?'selected':'')+'>'+n+'</option>').join('');
  }

  function templateVarRow(tipo,valor,pos){
    return '<div class="wa77-var-row" data-var-tipo="'+tipo+'">'+
      '<span class="wa77-var-pos">{{'+(pos+1)+'}}</span>'+
      '<select data-tpl-var="'+tipo+'">'+templateVarOptions(valor)+'</select>'+
      '<button type="button" class="wa77-var-btn" data-act="move-template-var" data-tipo="'+tipo+'" data-pos="'+pos+'" data-dir="-1" title="Subir">↑</button>'+
      '<button type="button" class="wa77-var-btn" data-act="move-template-var" data-tipo="'+tipo+'" data-pos="'+pos+'" data-dir="1" title="Descer">↓</button>'+
      '<button type="button" class="wa77-var-btn remove" data-act="remove-template-var" data-tipo="'+tipo+'" data-pos="'+pos+'" title="Remover">×</button>'+
    '</div>';
  }

  function rerenderTemplateVarPositions(tipo){
    document.querySelectorAll('[data-var-tipo="'+tipo+'"]').forEach((row,i)=>{
      row.querySelector('.wa77-var-pos').textContent='{{'+(i+1)+'}}';
      row.querySelectorAll('[data-pos]').forEach(b=>b.dataset.pos=String(i));
    });
  }

'''
if anchor not in js:
    raise SystemExit('loadTemplates anchor nao encontrado')
js=js.replace(anchor,helpers+anchor,1)

# Troca loadTemplates inteiro
start=js.index("  async function loadTemplates(){")
end=js.index("\n\n  async function loadRules(){",start)
if start<0 or end<0:
    raise SystemExit('loadTemplates bloco nao encontrado')

new_load=r'''  async function loadTemplates(){
    const {data,error}=await db().from('whatsapp_templates_operacionais')
      .select('tipo,template_codigo,language_code,status_meta,ativo,variaveis_body')
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
      return '<div class="wa77-rule">'+
        '<div class="wa77-head"><b>'+n+'</b><span class="wa77-badge">'+esc(r.status_meta||'DESCONHECIDO')+'</span></div>'+
        '<div class="wa77-fields">'+
          '<div class="wa77-field"><label>Nome na Meta</label><input type="text" id="wa77-tpl-code-'+s+'" value="'+esc(r.template_codigo||'')+'"></div>'+
          '<div class="wa77-field"><label>Idioma</label><input type="text" id="wa77-tpl-lang-'+s+'" value="'+esc(r.language_code||'pt_BR')+'"></div>'+
        '</div>'+
        '<div style="margin-top:10px"><div class="wa77-field"><label>Variáveis do corpo do template</label></div>'+
          '<p style="margin:3px 0 0">A ordem abaixo corresponde a {{1}}, {{2}}, {{3}}... do template aprovado na Meta.</p>'+
          '<div class="wa77-vars" id="wa77-tpl-vars-'+s+'">'+vars.map((v,i)=>templateVarRow(t,v,i)).join('')+'</div>'+
          '<div class="wa77-actions"><button type="button" class="wa77-btn alt" data-act="add-template-var" data-tipo="'+t+'">+ Adicionar variável</button></div>'+
        '</div>'+
        '<div class="wa77-actions"><label class="wa77-switch"><input type="checkbox" id="wa77-tpl-active-'+s+'" '+(r.ativo?'checked':'')+'> Ativo</label><button class="wa77-btn" data-act="save-template" data-tipo="'+t+'">Salvar template</button></div>'+
      '</div>';
    }).join('');
  }'''
js=js[:start]+new_load+js[end:]

# Substitui ação save-template e adiciona ações editor
old_action="if(a==='save-template'){const t=b.dataset.tipo,s=slug(t);const {error}=await db().rpc('salvar_template_whatsapp_operacional',{p_empresa_id:empresaId(),p_tipo:t,p_template_codigo:document.getElementById('wa77-tpl-code-'+s).value.trim(),p_language_code:document.getElementById('wa77-tpl-lang-'+s).value.trim()||'pt_BR',p_ativo:document.getElementById('wa77-tpl-active-'+s).checked});if(error)throw error;await loadTemplates()}"
new_action=r"""if(a==='add-template-var'){
        const t=b.dataset.tipo,s=slug(t),box=document.getElementById('wa77-tpl-vars-'+s);
        const pos=box.querySelectorAll('[data-var-tipo="'+t+'"]').length;
        if(pos>=10)return alert('Cada template pode ter no máximo 10 variáveis.');
        box.insertAdjacentHTML('beforeend',templateVarRow(t,'',pos));
      }
      if(a==='remove-template-var'){
        const t=b.dataset.tipo;
        b.closest('.wa77-var-row')?.remove();
        rerenderTemplateVarPositions(t);
      }
      if(a==='move-template-var'){
        const t=b.dataset.tipo,row=b.closest('.wa77-var-row'),dir=Number(b.dataset.dir||0);
        if(!row)return;
        if(dir<0&&row.previousElementSibling)row.parentNode.insertBefore(row,row.previousElementSibling);
        if(dir>0&&row.nextElementSibling)row.parentNode.insertBefore(row.nextElementSibling,row);
        rerenderTemplateVarPositions(t);
      }
      if(a==='save-template'){
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
if old_action not in js:
    raise SystemExit('save-template antigo nao encontrado')
js=js.replace(old_action,new_action,1)

mod.write_text(js,encoding='utf-8')

# Bump URL do módulo no HTML
html=html.replace("s.src='./whatsapp-automacoes-v77.js?v=78';","s.src='./whatsapp-automacoes-v77.js?v=81';",1)
idx.write_text(html,encoding='utf-8')

# Módulo WhatsApp: network-first porque só é carregado sob demanda.
fetch_anchor="""  if(url.pathname.endsWith('/manifest.webmanifest') || url.pathname.endsWith('/index.html')) {"""
special="""  if(url.pathname.endsWith('/whatsapp-automacoes-v77.js')) {
    event.respondWith(
      fetch(request, { cache: 'no-store' })
        .then(response => {
          if(response && response.ok) {
            const copia = response.clone();
            caches.open(CACHE_VERSION).then(cache => cache.put(request, copia));
          }
          return response;
        })
        .catch(() => caches.match(request))
    );
    return;
  }

"""
if fetch_anchor not in swtxt:
    raise SystemExit('fetch anchor SW nao encontrado')
swtxt=swtxt.replace(fetch_anchor,special+fetch_anchor,1)

swtxt,n=re.subn(
    r"const CACHE_VERSION = '[^']+';",
    "const CACHE_VERSION = 'simpla-shell-v81-template-vars';",
    swtxt,
    count=1
)
if n!=1: raise SystemExit('cache version nao encontrada')
sw.write_text(swtxt,encoding='utf-8')
