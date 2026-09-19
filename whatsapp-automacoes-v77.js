(function(){
  'use strict';
  if(window.SimplAWhatsAppV77) return;

  const state={mounted:false, loading:false, reminders:[]};
  const TIPOS=[
    {tipo:'CONFIRMACAO',titulo:'Confirmação de agendamento'},
    {tipo:'CANCELAMENTO',titulo:'Cancelamento'},
    {tipo:'REAGENDAMENTO',titulo:'Reagendamento'}
  ];
  const ANT=[[15,'15 minutos'],[30,'30 minutos'],[60,'1 hora'],[120,'2 horas'],[360,'6 horas'],[720,'12 horas'],[1440,'24 horas'],[2880,'48 horas'],[4320,'3 dias'],[10080,'7 dias']];
  const FUSOS=[
    ['America/Recife','Recife / Brasília (Nordeste)'],
    ['America/Sao_Paulo','São Paulo / Brasília'],
    ['America/Fortaleza','Fortaleza'],
    ['America/Bahia','Salvador / Bahia'],
    ['America/Manaus','Manaus / Amazonas'],
    ['America/Belem','Belém / Pará'],
    ['America/Cuiaba','Cuiabá / Mato Grosso'],
    ['America/Campo_Grande','Campo Grande / MS'],
    ['America/Rio_Branco','Rio Branco / Acre'],
    ['America/Noronha','Fernando de Noronha']
  ];

  function esc(v){return String(v??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]))}
  function fmt(v){if(!v)return '—';try{return new Date(v).toLocaleString('pt-BR')}catch(_){return '—'}}
  function phone(v){const d=String(v||'').replace(/\D/g,'');return d.length<6?'—':d.slice(0,2)+'•••••'+d.slice(-3)}
  function slug(t){return t.toLowerCase()}
  function empresaId(){return window.empresaAtual?.id||null}
  function db(){return window.CloudDB}

  async function isAdmin(){
    if(!db()||!empresaId())return false;
    const {data}=await db().rpc('perfil_na_empresa',{p_empresa_id:empresaId()});
    return String(data||'').toUpperCase()==='ADMIN';
  }
  async function allowed(){
    if(!await isAdmin()) return false;
    if(typeof window.empresaPodeUsarRecurso!=='function') return true;
    return await window.empresaPodeUsarRecurso('whatsapp_operacional');
  }

  function injectCss(){
    if(document.getElementById('simpla-wa77-css'))return;
    const st=document.createElement('style');st.id='simpla-wa77-css';
    st.textContent=`
    .wa77{display:grid;gap:14px}.wa77-card{border:1px solid #dfe6ed;border-radius:10px;background:#fff;padding:16px;box-shadow:0 1px 3px rgba(31,47,65,.04);text-transform:none}
    .wa77-card h3{margin:0 0 4px!important;font-size:15px!important;color:#23364d!important;text-transform:none!important}.wa77-card p{margin:0;color:#718096;font-size:10px;line-height:1.5;text-transform:none}
    .wa77-head{display:flex;justify-content:space-between;gap:10px;align-items:flex-start;flex-wrap:wrap}.wa77-badge{padding:5px 8px;border-radius:999px;background:#edf2f7;color:#526579;font-size:8px;font-weight:900;text-transform:uppercase}
    .wa77-kpis{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:8px;margin-top:12px}.wa77-kpi{background:#f8fafc;border:1px solid #e2e8f0;border-radius:8px;padding:10px}.wa77-kpi span{display:block;font-size:8px;font-weight:900;color:#718096;text-transform:uppercase}.wa77-kpi b{display:block;font-size:17px;color:#2d3748;margin-top:3px}
    .wa77-bar{height:10px;background:#edf2f7;border-radius:999px;overflow:hidden;margin-top:10px}.wa77-fill{height:100%;width:0;background:#345a7d;transition:.2s}
    .wa77-grid2{display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-top:12px}.wa77-rule{background:#f8fafc;border:1px solid #e2e8f0;border-radius:8px;padding:12px}.wa77-fields{display:grid;grid-template-columns:1fr 1fr;gap:8px;margin-top:9px}.wa77-field label{display:block;font-size:8px;font-weight:900;color:#718096;margin-bottom:4px;text-transform:uppercase}.wa77 input[type=time],.wa77 input[type=text],.wa77 select{width:100%;padding:8px;border:1px solid #cbd5e0;border-radius:6px;background:#fff;font-size:11px;text-transform:none;box-sizing:border-box}
    .wa77-btn{border:0;border-radius:7px;padding:9px 11px;background:#1a1c23;color:#fff;font-size:9px;font-weight:900;cursor:pointer}.wa77-btn.alt{background:#edf2f7;color:#2d3748}.wa77-btn.danger{background:#fff5f5;color:#c53030}.wa77-actions{display:flex;gap:8px;align-items:center;flex-wrap:wrap;margin-top:10px}
    .wa77-msg{font-size:9px;color:#718096}.wa77-vars{display:grid;gap:6px;margin-top:9px}.wa77-var-row{display:grid;grid-template-columns:42px minmax(0,1fr) auto auto auto;gap:6px;align-items:center}.wa77-var-pos{font-size:9px;font-weight:900;color:#718096;text-align:center}.wa77-var-btn{border:0;border-radius:6px;padding:7px 8px;background:#edf2f7;color:#4a5568;font-size:9px;font-weight:900;cursor:pointer}.wa77-var-btn.remove{background:#fff5f5;color:#c53030}.wa77-list{display:grid;gap:8px;margin-top:10px}.wa77-rem{border:1px solid #dbe4ee;border-radius:8px;padding:10px;background:#fff}.wa77-rem-head{display:flex;justify-content:space-between;gap:8px;align-items:center}.wa77-switch{display:flex;align-items:center;gap:7px;font-size:9px;color:#4a5568;text-transform:none}
    .wa77-table-wrap{overflow:auto;margin-top:10px}.wa77-table{width:100%;min-width:760px;border-collapse:collapse}.wa77-table th,.wa77-table td{padding:8px;border-bottom:1px solid #edf2f7;font-size:9px;text-align:left;text-transform:none}.wa77-table th{background:#f8fafc;font-size:8px;color:#718096;text-transform:uppercase}
    .wa77-note{margin-top:10px;padding:9px;border-radius:7px;background:#fffaf0;border:1px solid #f6e05e;color:#744210;font-size:9px;line-height:1.4}.wa77-empty{padding:12px;text-align:center;color:#718096;font-size:10px}
    .wa77-status{font-weight:900}.wa77-status.ENVIADO,.wa77-status.delivered,.wa77-status.read{color:#2f855a}.wa77-status.ERRO,.wa77-status.failed{color:#c53030}.wa77-status.PENDENTE{color:#975a16}
    @media(max-width:800px){.wa77-grid2,.wa77-fields{grid-template-columns:1fr}.wa77-kpis{grid-template-columns:1fr 1fr}.wa77-var-row{grid-template-columns:36px minmax(0,1fr) auto auto auto}}
    `;
    document.head.appendChild(st);
  }

  function baseHtml(){
    return `
    <div class="wa77" id="wa77-root">
      <section class="wa77-card" id="wa77-quota"><div class="wa77-head"><div><h3>Franquia mensal do WhatsApp</h3><p>Consumo mensal de mensagens operacionais.</p></div><span class="wa77-badge" id="wa77-plan">—</span></div><div class="wa77-bar"><div class="wa77-fill" id="wa77-fill"></div></div><div class="wa77-kpis"><div class="wa77-kpi"><span>Enviadas</span><b id="wa77-sent">0</b></div><div class="wa77-kpi"><span>Processando</span><b id="wa77-processing">0</b></div><div class="wa77-kpi"><span>Restantes</span><b id="wa77-remaining">—</b></div><div class="wa77-kpi"><span>Limite mensal</span><b id="wa77-limit">—</b></div></div><div class="wa77-actions"><span class="wa77-msg" id="wa77-quota-msg"></span><button class="wa77-btn alt" data-act="refresh-quota">Atualizar consumo</button></div></section>

      <section class="wa77-card"><div class="wa77-head"><div><h3>Conexão com a Meta</h3><p>Conecte o WhatsApp oficial da empresa sem expor tokens no navegador.</p></div><span class="wa77-badge" id="wa77-conn-badge">Não configurado</span></div><div class="wa77-kpis"><div class="wa77-kpi"><span>Provedor</span><b id="wa77-provider">Meta Cloud API</b></div><div class="wa77-kpi"><span>Número</span><b id="wa77-number">—</b></div><div class="wa77-kpi"><span>Validação</span><b id="wa77-validation" style="font-size:11px">—</b></div><div class="wa77-kpi"><span>Automação</span><b id="wa77-auto-state" style="font-size:11px">Desativada</b></div></div><div class="wa77-actions"><button class="wa77-btn" data-act="connect-meta" id="wa77-connect">Conectar WhatsApp com a Meta</button><button class="wa77-btn alt" data-act="validate-meta">Validar conexão</button><button class="wa77-btn alt" data-act="toggle-auto" data-value="true">Ativar automação</button><button class="wa77-btn alt" data-act="toggle-auto" data-value="false">Desativar</button><span class="wa77-msg" id="wa77-conn-msg"></span></div></section>

      <section class="wa77-card"><h3>Fuso horário da empresa</h3><p>Necessário para calcular lembretes e janelas de envio.</p><div class="wa77-grid2"><div class="wa77-field"><label>Fuso horário</label><select id="wa77-timezone"></select></div><div class="wa77-actions" style="align-items:end"><button class="wa77-btn" data-act="save-timezone">Salvar fuso</button><span class="wa77-msg" id="wa77-timezone-msg"></span></div></div></section>

      <section class="wa77-card"><h3>Templates operacionais</h3><p>Nomes dos templates aprovados na Meta.</p><div class="wa77-grid2" id="wa77-templates"></div></section>

      <section class="wa77-card"><h3>Regras de envio por mensagem</h3><p>Confirmação, cancelamento e reagendamento possuem regras próprias.</p><div class="wa77-grid2" id="wa77-rules"></div></section>

      <section class="wa77-card"><div class="wa77-head"><div><h3>Lembretes do agendamento</h3><p>Crie mais de um lembrete, cada um com antecedência e janela próprias.</p></div><button class="wa77-btn" data-act="add-reminder">+ Adicionar lembrete</button></div><div class="wa77-list" id="wa77-reminders"></div><div class="wa77-note">Cada lembrete enviado conta individualmente na franquia mensal.</div></section>

      <section class="wa77-card"><div class="wa77-head"><div><h3>Histórico e monitoramento</h3><p>Últimas mensagens da fila operacional.</p></div><button class="wa77-btn alt" data-act="refresh-monitor">Atualizar</button></div><div class="wa77-table-wrap"><table class="wa77-table"><thead><tr><th>Criada</th><th>Tipo</th><th>Destino</th><th>Status</th><th>Meta</th><th>Programada</th><th>Detalhe</th></tr></thead><tbody id="wa77-monitor"></tbody></table></div></section>
    </div>`;
  }

  function ruleHtml(tipo,title,r={}){
    const s=slug(tipo);
    return `<div class="wa77-rule"><div class="wa77-head"><div><b>${esc(title)}</b></div><label class="wa77-switch"><input type="checkbox" id="wa77-rule-active-${s}" ${r.ativo?'checked':''}> Ativo</label></div><div class="wa77-fields"><div class="wa77-field"><label>Início da janela</label><input type="time" id="wa77-rule-start-${s}" value="${esc(String(r.horario_inicio||'08:00').slice(0,5))}"></div><div class="wa77-field"><label>Fim da janela</label><input type="time" id="wa77-rule-end-${s}" value="${esc(String(r.horario_fim||'20:00').slice(0,5))}"></div><div class="wa77-field" style="grid-column:1/-1"><label>Evitar duplicidade</label><select id="wa77-rule-dup-${s}"><option value="true" ${r.bloquear_duplicidade!==false?'selected':''}>Sim</option><option value="false" ${r.bloquear_duplicidade===false?'selected':''}>Não</option></select></div></div><div class="wa77-actions"><button class="wa77-btn" data-act="save-rule" data-tipo="${tipo}">Salvar</button><span class="wa77-msg" id="wa77-rule-msg-${s}"></span></div></div>`;
  }

  function reminderHtml(r,i){
    const opts=ANT.map(([v,n])=>`<option value="${v}" ${Number(r.antecedencia_minutos||1440)===v?'selected':''}>${n}</option>`).join('');
    return `<div class="wa77-rem"><div class="wa77-rem-head"><b>Lembrete ${i+1}</b><label class="wa77-switch"><input type="checkbox" id="wa77-rem-active-${i}" ${r.ativo!==false?'checked':''}> Ativo</label></div><div class="wa77-fields"><div class="wa77-field"><label>Antecedência</label><select id="wa77-rem-ant-${i}">${opts}</select></div><div class="wa77-field"><label>Início</label><input type="time" id="wa77-rem-start-${i}" value="${esc(String(r.horario_inicio||'08:00').slice(0,5))}"></div><div class="wa77-field"><label>Fim</label><input type="time" id="wa77-rem-end-${i}" value="${esc(String(r.horario_fim||'20:00').slice(0,5))}"></div><div class="wa77-field"><label>Evitar duplicidade</label><select id="wa77-rem-dup-${i}"><option value="true" ${r.bloquear_duplicidade!==false?'selected':''}>Sim</option><option value="false" ${r.bloquear_duplicidade===false?'selected':''}>Não</option></select></div></div><div class="wa77-actions"><button class="wa77-btn" data-act="save-reminder" data-i="${i}">Salvar lembrete</button>${r.id?`<button class="wa77-btn danger" data-act="delete-reminder" data-i="${i}">Excluir</button>`:''}<span class="wa77-msg" id="wa77-rem-msg-${i}"></span></div></div>`;
  }

  async function loadQuota(){
    const {data,error}=await db().rpc('status_cota_whatsapp_empresa',{p_empresa_id:empresaId()}); if(error) throw error;
    const r=Array.isArray(data)?data[0]:data; if(!r)return;
    const test=!!r.modo_teste||String(r.plano_codigo).toUpperCase()==='TESTE';
    document.getElementById('wa77-plan').textContent='Plano '+r.plano_codigo;
    document.getElementById('wa77-sent').textContent=r.enviadas_mes||0;
    document.getElementById('wa77-processing').textContent=r.em_processamento||0;
    if(test){document.getElementById('wa77-remaining').textContent='Ilimitadas';document.getElementById('wa77-limit').textContent='Ilimitado';document.getElementById('wa77-fill').style.width='0%';document.getElementById('wa77-quota-msg').textContent='Conta de testes sem limite comercial.';return}
    if(!r.limite_definido){document.getElementById('wa77-remaining').textContent='A definir';document.getElementById('wa77-limit').textContent='A definir';document.getElementById('wa77-fill').style.width='0%';document.getElementById('wa77-quota-msg').textContent='Franquia comercial ainda não definida.';return}
    document.getElementById('wa77-remaining').textContent=r.restantes??0;document.getElementById('wa77-limit').textContent=r.limite_mensal??0;document.getElementById('wa77-fill').style.width=Math.min(100,Number(r.percentual_consumido||0))+'%';document.getElementById('wa77-quota-msg').textContent=(r.percentual_consumido||0)+'% utilizado.';
  }

  async function loadConnection(){
    const {data,error}=await db().from('whatsapp_integracoes').select('provedor,numero_exibicao,status,ativo,ultima_validacao_em').eq('empresa_id',empresaId()).maybeSingle(); if(error)throw error;
    document.getElementById('wa77-provider').textContent=data?.provedor==='META_CLOUD_API'?'Meta Cloud API':(data?.provedor||'Meta Cloud API');
    document.getElementById('wa77-number').textContent=data?.numero_exibicao||'Não conectado';
    document.getElementById('wa77-validation').textContent=fmt(data?.ultima_validacao_em);
    const b=document.getElementById('wa77-conn-badge');b.textContent=data?.ativo&&data?.status==='ATIVO'?'Conectado':(data?.status||'Não configurado');
    const {data:auto}=await db().from('whatsapp_automacao_config').select('envios_automaticos_ativos').eq('empresa_id',empresaId()).maybeSingle();
    document.getElementById('wa77-auto-state').textContent=auto?.envios_automaticos_ativos?'Ativada':'Desativada';
  }

  async function loadTimezone(){
    const {data,error}=await db().from('empresas').select('fuso_horario').eq('id',empresaId()).maybeSingle();if(error)throw error;
    const sel=document.getElementById('wa77-timezone');const detected=Intl.DateTimeFormat().resolvedOptions().timeZone||'';
    const items=[...FUSOS]; if(detected&&!items.some(x=>x[0]===detected))items.unshift([detected,'Detectado pelo navegador']);
    sel.innerHTML='<option value="">Selecione</option>'+items.map(([v,n])=>`<option value="${esc(v)}">${esc(n)} · ${esc(v)}</option>`).join('');
    if(data?.fuso_horario){if(![...sel.options].some(o=>o.value===data.fuso_horario)){const o=document.createElement('option');o.value=data.fuso_horario;o.textContent=data.fuso_horario;sel.appendChild(o)}sel.value=data.fuso_horario}else if(detected)sel.value=detected;
  }

  const TEMPLATE_VARS=[
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

  async function loadTemplates(){
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
  }

  async function loadRules(){
    const {data,error}=await db().from('whatsapp_regras_mensagem').select('tipo,ativo,horario_inicio,horario_fim,bloquear_duplicidade').eq('empresa_id',empresaId());if(error)throw error;
    const map=new Map((data||[]).map(r=>[r.tipo,r]));
    document.getElementById('wa77-rules').innerHTML=TIPOS.map(x=>ruleHtml(x.tipo,x.titulo,map.get(x.tipo)||{})).join('');
  }

  async function loadReminders(){
    const {data,error}=await db().from('whatsapp_lembretes_agendamento').select('id,ativo,antecedencia_minutos,horario_inicio,horario_fim,bloquear_duplicidade,ordem').eq('empresa_id',empresaId()).order('ordem',{ascending:true});if(error)throw error;
    state.reminders=Array.isArray(data)?data:[];
    renderReminders();
  }
  function renderReminders(){document.getElementById('wa77-reminders').innerHTML=state.reminders.length?state.reminders.map(reminderHtml).join(''):'<div class="wa77-empty">Nenhum lembrete configurado.</div>'}

  async function loadMonitor(){
    const {data,error}=await db().from('whatsapp_mensagens_operacionais').select('tipo,destino,status,provider_status,processar_em_local,provider_message_id,erro,criado_em').eq('empresa_id',empresaId()).order('criado_em',{ascending:false}).limit(50);if(error)throw error;
    const rows=data||[];document.getElementById('wa77-monitor').innerHTML=rows.length?rows.map(r=>`<tr><td>${fmt(r.criado_em)}</td><td>${esc(r.tipo)}</td><td>${phone(r.destino)}</td><td class="wa77-status ${esc(r.status)}">${esc(r.status)}</td><td class="wa77-status ${esc(r.provider_status||'')}">${esc(r.provider_status||'—')}</td><td>${esc(String(r.processar_em_local||'—').replace('T',' ').slice(0,16))}</td><td>${esc(r.erro||(r.provider_message_id?'ID Meta: '+String(r.provider_message_id).slice(-12):'—'))}</td></tr>`).join(''):'<tr><td colspan="7" class="wa77-empty">Fila vazia.</td></tr>';
  }

  async function refreshAll(){
    if(state.loading)return;state.loading=true;
    try{await Promise.all([loadQuota(),loadConnection(),loadTimezone(),loadTemplates(),loadRules(),loadReminders(),loadMonitor()])}
    catch(e){console.error('SimplA WhatsApp v77:',e)}
    finally{state.loading=false}
  }

  async function saveRule(tipo){
    const s=slug(tipo),msg=document.getElementById('wa77-rule-msg-'+s);msg.textContent='Salvando...';
    const {error}=await db().rpc('salvar_regra_whatsapp_mensagem',{p_empresa_id:empresaId(),p_tipo:tipo,p_ativo:document.getElementById('wa77-rule-active-'+s).checked,p_antecedencia_minutos:null,p_horario_inicio:document.getElementById('wa77-rule-start-'+s).value,p_horario_fim:document.getElementById('wa77-rule-end-'+s).value,p_bloquear_duplicidade:document.getElementById('wa77-rule-dup-'+s).value==='true'});if(error)throw error;msg.textContent='Salvo.';
  }
  async function saveReminder(i){
    const r=state.reminders[i],msg=document.getElementById('wa77-rem-msg-'+i);msg.textContent='Salvando...';
    const {error}=await db().rpc('salvar_lembrete_whatsapp',{p_id:r.id||null,p_empresa_id:empresaId(),p_ativo:document.getElementById('wa77-rem-active-'+i).checked,p_antecedencia_minutos:Number(document.getElementById('wa77-rem-ant-'+i).value),p_horario_inicio:document.getElementById('wa77-rem-start-'+i).value,p_horario_fim:document.getElementById('wa77-rem-end-'+i).value,p_bloquear_duplicidade:document.getElementById('wa77-rem-dup-'+i).value==='true'});if(error)throw error;await loadReminders();await loadMonitor();
  }

  async function handle(e){
    const b=e.target.closest('[data-act]');if(!b)return;const a=b.dataset.act;
    try{
      if(a==='refresh-quota')await loadQuota();
      if(a==='refresh-monitor')await loadMonitor();
      if(a==='save-timezone'){const f=document.getElementById('wa77-timezone').value;if(!f)return alert('Selecione o fuso.');const {error}=await db().rpc('salvar_fuso_horario_empresa',{p_empresa_id:empresaId(),p_fuso_horario:f});if(error)throw error;document.getElementById('wa77-timezone-msg').textContent='Fuso salvo.'}
      if(a==='toggle-auto'){const on=b.dataset.value==='true';if(on&&!confirm('Ativar os envios automáticos?'))return;const {error}=await db().rpc('salvar_automacao_whatsapp_operacional',{p_empresa_id:empresaId(),p_envios_automaticos_ativos:on});if(error)throw error;await loadConnection()}
      if(a==='validate-meta'){document.getElementById('wa77-conn-msg').textContent='Validando...';const {data,error}=await db().functions.invoke('whatsapp-validar-integracao',{body:{empresa_id:empresaId()}});if(error)throw error;document.getElementById('wa77-conn-msg').textContent=data?.ok?'Conexão validada.':'Validação não concluída.';await loadConnection()}
      if(a==='connect-meta'){await startEmbedded()}
      if(a==='add-template-var'){
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
      }
      if(a==='save-rule')await saveRule(b.dataset.tipo);
      if(a==='add-reminder'){const used=new Set(state.reminders.map(x=>Number(x.antecedencia_minutos)));const d=ANT.find(x=>!used.has(x[0]))?.[0]||1440;state.reminders.push({id:null,ativo:true,antecedencia_minutos:d,horario_inicio:'08:00',horario_fim:'20:00',bloquear_duplicidade:true});renderReminders()}
      if(a==='save-reminder')await saveReminder(Number(b.dataset.i));
      if(a==='delete-reminder'){const i=Number(b.dataset.i),r=state.reminders[i];if(!r?.id||!confirm('Excluir este lembrete?'))return;const {error}=await db().rpc('excluir_lembrete_whatsapp',{p_id:r.id,p_empresa_id:empresaId()});if(error)throw error;await loadReminders();await loadMonitor()}
    }catch(err){console.error(err);alert(err?.message||'Não foi possível concluir a ação.')}
  }

  let embeddedCfg=null, embeddedData={};
  async function loadFacebook(appId,version){if(window.FB)return;await new Promise((resolve,reject)=>{window.fbAsyncInit=()=>{FB.init({appId:String(appId),cookie:true,xfbml:false,version:String(version)});resolve()};const s=document.createElement('script');s.src='https://connect.facebook.net/pt_BR/sdk.js';s.async=true;s.onerror=reject;document.head.appendChild(s)})}
  async function startEmbedded(){
    const {data,error}=await db().functions.invoke('whatsapp-embedded-config',{body:{empresa_id:empresaId()}});if(error)throw error;if(!data?.ready)throw new Error('Configuração Meta pendente no backend.');embeddedCfg=data;embeddedData={};await loadFacebook(data.app_id,data.graph_version);
    FB.login(resp=>{if(resp?.authResponse?.code){embeddedData.code=resp.authResponse.code;tryFinalize()}},{config_id:String(data.config_id),response_type:'code',override_default_response_type:true,extras:{setup:{}}});
  }
  async function tryFinalize(){if(!embeddedData.code||!embeddedData.waba_id||!embeddedData.phone_number_id)return;const {error}=await db().functions.invoke('whatsapp-embedded-finalizar',{body:{empresa_id:empresaId(),code:embeddedData.code,waba_id:embeddedData.waba_id,phone_number_id:embeddedData.phone_number_id,business_id:embeddedData.business_id||null}});if(error)throw error;await loadConnection()}
  window.addEventListener('message',e=>{try{if(!/facebook\.com$/i.test(new URL(e.origin).hostname))return;let d=typeof e.data==='string'?JSON.parse(e.data):e.data;if(d?.type!=='WA_EMBEDDED_SIGNUP')return;if(/^FINISH/.test(d.event||'')){embeddedData.waba_id=String(d.data?.waba_id||d.data?.wabaId||'');embeddedData.phone_number_id=String(d.data?.phone_number_id||d.data?.phoneNumberId||'');embeddedData.business_id=String(d.data?.business_id||d.data?.businessId||'');tryFinalize()}}catch(_){}},false);

  async function mount(container){
    if(state.mounted){await refreshAll();return}
    if(!container)return;
    injectCss();container.innerHTML=baseHtml();container.addEventListener('click',handle);state.mounted=true;
    if(!await isAdmin()){container.innerHTML='<div class="wa77-card"><div class="wa77-empty">Apenas administradores podem acessar estas configurações.</div></div>';return}
    if(!await allowed()){container.innerHTML='<div class="wa77-card"><h3>WhatsApp e Automações</h3><p>Este recurso está disponível a partir do plano Plus.</p></div>';return}
    await refreshAll();
  }

  window.SimplAWhatsAppV77={mount,refresh:refreshAll};
})();