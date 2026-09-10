from pathlib import Path
import re

p=Path('index.html')
s=p.read_text(encoding='utf-8')

# 1) Dias de funcionamento: carregar e salvar junto ao expediente.
old_load="""        function carregarConfigExpedienteUI() {
            document.getElementById('cfg-horario-abertura').value = configExpediente.abertura || '08:00';
            document.getElementById('cfg-horario-fechamento').value = configExpediente.fechamento || '18:00';
            document.getElementById('cfg-horario-intervalo').value = configExpediente.intervalo || 45;
            document.getElementById('agenda-intervalo-input').value = configExpediente.intervalo || 45;
        }
"""
new_load="""        function carregarConfigExpedienteUI() {
            document.getElementById('cfg-horario-abertura').value = configExpediente.abertura || '08:00';
            document.getElementById('cfg-horario-fechamento').value = configExpediente.fechamento || '18:00';
            document.getElementById('cfg-horario-intervalo').value = configExpediente.intervalo || 45;
            const agendaIntervalo = document.getElementById('agenda-intervalo-input');
            if(agendaIntervalo) agendaIntervalo.value = configExpediente.intervalo || 45;
            if(typeof carregarDiasFuncionamentoUI === 'function') carregarDiasFuncionamentoUI();
        }
"""
if old_load in s:
    s=s.replace(old_load,new_load,1)
else:
    print('aviso: carregarConfigExpedienteUI exato nao localizado')

old_save="""        async function salvarConfigExpediente() {
            if(!validarAcessoPerfil('configuracoes','Somente administradores podem alterar as Configurações.')) return;
            configExpediente.abertura = document.getElementById('cfg-horario-abertura').value || '08:00';
            configExpediente.fechamento = document.getElementById('cfg-horario-fechamento').value || '18:00';
            configExpediente.intervalo = parseInt(document.getElementById('cfg-horario-intervalo').value) || 45;
            document.getElementById('agenda-intervalo-input').value = configExpediente.intervalo;
            salvarStorage();
"""
new_save="""        async function salvarConfigExpediente() {
            if(!validarAcessoPerfil('configuracoes','Somente administradores podem alterar as Configurações.')) return;
            const diasSelecionados = [...document.querySelectorAll('.cfg-dia-funcionamento:checked')].map(el => Number(el.value));
            if(document.querySelector('.cfg-dia-funcionamento') && !diasSelecionados.length) {
                alert('Selecione pelo menos um dia de funcionamento.');
                return;
            }
            configExpediente.abertura = document.getElementById('cfg-horario-abertura').value || '08:00';
            configExpediente.fechamento = document.getElementById('cfg-horario-fechamento').value || '18:00';
            configExpediente.intervalo = parseInt(document.getElementById('cfg-horario-intervalo').value) || 45;
            if(diasSelecionados.length) configExpediente.diasFuncionamento = diasSelecionados;
            const agendaIntervalo = document.getElementById('agenda-intervalo-input');
            if(agendaIntervalo) agendaIntervalo.value = configExpediente.intervalo;
            salvarStorage();
"""
if old_save in s:
    s=s.replace(old_save,new_save,1)
else:
    print('aviso: salvarConfigExpediente inicio exato nao localizado')

# 2) Agenda interna respeita dias de funcionamento.
marker="""            let intervalo = configExpediente.intervalo || 45;
            const profissionalAtual = profissionais.find(p => String(p.id) === String(profissionalFiltro));
"""
inject="""            const diasFuncionamentoAgenda = Array.isArray(configExpediente.diasFuncionamento) && configExpediente.diasFuncionamento.length
                ? configExpediente.diasFuncionamento.map(Number)
                : [0,1,2,3,4,5,6];
            const diaSemanaAgenda = new Date(dataSelecionada + 'T12:00:00').getDay();
            if(!diasFuncionamentoAgenda.includes(diaSemanaAgenda)) {
                const infoExpediente = document.getElementById('agenda-expediente-info');
                if(infoExpediente) infoExpediente.innerText = 'Empresa fechada neste dia';
                const avisoFechado = document.createElement('div');
                avisoFechado.className = 'agenda-dia-fechado';
                avisoFechado.innerHTML = '<strong>Sem expediente</strong><span>Este dia não está configurado como dia de funcionamento.</span>';
                grid.appendChild(avisoFechado);
                return;
            }

            let intervalo = configExpediente.intervalo || 45;
            const profissionalAtual = profissionais.find(p => String(p.id) === String(profissionalFiltro));
"""
if marker in s and 'diasFuncionamentoAgenda' not in s:
    s=s.replace(marker,inject,1)

# 3) CSS final: correcoes de switches + agenda clean.
css=r'''
<style id="simpla-ux-config-agenda-v3">
/* Configurações: switches legíveis e próximos do texto */
#configuracoes .cfg-switch-line{justify-content:flex-start!important;gap:14px!important;align-items:center!important;}
#configuracoes .cfg-switch-copy{flex:0 1 auto!important;min-width:260px!important;max-width:620px!important;}
#configuracoes .cfg-switch{width:48px!important;height:28px!important;}
#configuracoes .cfg-switch-track{width:48px!important;height:28px!important;background:#8797a8!important;border:1px solid #66788a!important;box-shadow:inset 0 0 0 1px rgba(255,255,255,.16)!important;}
#configuracoes .cfg-switch-track:after{width:20px!important;height:20px!important;left:3px!important;top:3px!important;border:1px solid rgba(0,0,0,.08)!important;}
#configuracoes .cfg-switch input:checked + .cfg-switch-track{background:#2f587d!important;border-color:#274b6c!important;}
#configuracoes .cfg-switch input:checked + .cfg-switch-track:after{transform:translateX(20px)!important;}
#configuracoes input[type="checkbox"]:not(.cfg-switch-input):not(.cfg-dia-funcionamento){position:relative!important;inset:auto!important;transform:none!important;display:inline-block!important;vertical-align:middle!important;margin:0 14px 0 0!important;flex:0 0 42px!important;}
#configuracoes label:has(> input[type="checkbox"]:not(.cfg-switch-input):not(.cfg-dia-funcionamento)){display:flex!important;align-items:center!important;gap:10px!important;min-width:0!important;}

/* Dias de funcionamento */
.cfg-dias-wrap{margin:18px 0 22px;padding:16px;background:#f8fafc;border:1px solid #e1e7ec;border-radius:10px;}
.cfg-dias-titulo{font-size:13px;font-weight:700;color:#263b50;margin-bottom:4px;text-transform:none;}
.cfg-dias-desc{font-size:11px;color:#718096;margin-bottom:12px;text-transform:none;}
.cfg-dias-grid{display:grid;grid-template-columns:repeat(7,minmax(70px,1fr));gap:8px;}
.cfg-dia-label{position:relative;display:block;cursor:pointer;}
.cfg-dia-label input{position:absolute!important;opacity:0!important;pointer-events:none!important;width:1px!important;height:1px!important;}
.cfg-dia-pill{display:flex;align-items:center;justify-content:center;min-height:42px;border:1px solid #cbd5df;border-radius:8px;background:#fff;color:#526579;font-size:12px;font-weight:700;transition:.16s;text-transform:none;}
.cfg-dia-label input:checked + .cfg-dia-pill{background:#2f587d;color:#fff;border-color:#2f587d;box-shadow:0 2px 5px rgba(47,88,125,.18);}

/* Agenda clean */
#agenda>.header{background:#fff!important;border:1px solid #e3e8ed!important;border-radius:12px!important;padding:16px 18px!important;margin-bottom:12px!important;box-shadow:0 1px 3px rgba(31,47,65,.05)!important;}
#agenda>.header h1{font-size:22px!important;letter-spacing:-.3px!important;}
#agenda>.header select,#agenda>.header input[type="date"]{height:40px!important;border-radius:8px!important;border-color:#d8e0e7!important;padding:0 10px!important;}
#agenda .agenda-toolbar-nav{display:flex;gap:6px;align-items:center;}
#agenda .agenda-nav-btn{height:40px;border:1px solid #d8e0e7;background:#fff;color:#30475d;border-radius:8px;padding:0 12px;font-weight:700;cursor:pointer;}
#agenda .agenda-nav-btn:hover{background:#f4f7f9;}
#agenda #agenda-online-compartilhar{padding:12px 14px!important;border-radius:10px!important;box-shadow:none!important;border:1px solid #e3e8ed!important;background:#fbfcfd!important;}
#agenda #agenda-online-compartilhar h3{font-size:13px!important;margin:0 0 3px!important;}
#agenda #agenda-online-compartilhar p{font-size:11px!important;margin-bottom:8px!important;}
#agenda .agenda-scroll-area{border-radius:12px!important;border:1px solid #e3e8ed!important;box-shadow:0 1px 3px rgba(31,47,65,.05)!important;}
#agenda .agenda-dia-fechado{grid-column:1/-1;min-height:180px;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:6px;border:1px dashed #cbd5df;border-radius:10px;background:#f8fafc;color:#526579;text-align:center;text-transform:none;}
#agenda .agenda-dia-fechado strong{font-size:15px;color:#2d4156;}
#agenda .agenda-dia-fechado span{font-size:12px;color:#718096;}
@media(max-width:900px){.cfg-dias-grid{grid-template-columns:repeat(4,minmax(68px,1fr));}#configuracoes .cfg-switch-copy{min-width:0!important;flex:1!important;}}
@media(max-width:560px){.cfg-dias-grid{grid-template-columns:repeat(2,minmax(90px,1fr));}}
</style>
'''
if 'id="simpla-ux-config-agenda-v3"' not in s:
    s=s.replace('</head>',css+'\n</head>',1)

# 4) JS complementar: dias, remoção do tema, mover notificações e toolbar agenda.
js=r'''
<script id="simpla-ux-config-agenda-v3-js">
(function(){
  const DIAS=[['Dom',0],['Seg',1],['Ter',2],['Qua',3],['Qui',4],['Sex',5],['Sáb',6]];

  window.carregarDiasFuncionamentoUI=function(){
    const selecionados=Array.isArray(window.configExpediente?.diasFuncionamento) && window.configExpediente.diasFuncionamento.length
      ? window.configExpediente.diasFuncionamento.map(Number)
      : [0,1,2,3,4,5,6];
    document.querySelectorAll('.cfg-dia-funcionamento').forEach(el=>{el.checked=selecionados.includes(Number(el.value));});
  };

  function montarDias(){
    if(document.getElementById('cfg-dias-funcionamento')) return;
    const intervalo=document.getElementById('cfg-horario-intervalo');
    if(!intervalo) return;
    const sec=intervalo.closest('.cfg-v2-section') || intervalo.closest('.form-container') || intervalo.parentElement;
    if(!sec) return;
    const botao=[...sec.querySelectorAll('button')].find(b=>/SALVAR HORÁRIO DE FUNCIONAMENTO/i.test(b.textContent||''));
    if(!botao) return;
    const wrap=document.createElement('div');
    wrap.id='cfg-dias-funcionamento';wrap.className='cfg-dias-wrap';
    wrap.innerHTML='<div class="cfg-dias-titulo">Dias de funcionamento</div><div class="cfg-dias-desc">Selecione os dias em que a empresa atende.</div><div class="cfg-dias-grid">'+DIAS.map(([nome,val])=>'<label class="cfg-dia-label"><input class="cfg-dia-funcionamento" type="checkbox" value="'+val+'"><span class="cfg-dia-pill">'+nome+'</span></label>').join('')+'</div>';
    botao.parentNode.insertBefore(wrap,botao);
    carregarDiasFuncionamentoUI();
  }

  function removerTema(){
    document.querySelectorAll('#configuracoes .cfg-v2-section').forEach(sec=>{
      const h=sec.querySelector('h3');
      if(h && /PERSONALIZAÇÃO DE TEMA/i.test(h.textContent||'')) sec.remove();
    });
  }

  function moverNotificacoes(){
    const content=document.querySelector('#configuracoes .cfg-v2-content');
    const nav=document.querySelector('#configuracoes .cfg-v2-nav');
    if(!content||!nav) return;
    const notif=content.querySelector('.cfg-v2-group[data-cat="Notificações"]');
    if(!notif) return;
    let outros=content.querySelector('.cfg-v2-group[data-cat="Outros"]');
    if(!outros){
      notif.dataset.cat='Outros';
      const h=notif.querySelector(':scope > h2'); if(h) h.textContent='Outros';
      const d=notif.querySelector(':scope > .cfg-v2-desc'); if(d) d.textContent='Preferências complementares e recursos do sistema.';
      const b=nav.querySelector('button[data-cat="Notificações"]'); if(b){b.dataset.cat='Outros';const sp=b.querySelector('span');if(sp)sp.textContent='Outros';}
      return;
    }
    [...notif.querySelectorAll(':scope > .cfg-v2-section')].forEach(sec=>outros.appendChild(sec));
    notif.remove();
    nav.querySelector('button[data-cat="Notificações"]')?.remove();
  }

  function limparCategoriasVazias(){
    document.querySelectorAll('#configuracoes .cfg-v2-group').forEach(g=>{
      if(!g.querySelector('.cfg-v2-section')){
        const cat=g.dataset.cat;g.remove();
        document.querySelector('#configuracoes .cfg-v2-nav button[data-cat="'+cat+'"]')?.remove();
      }
    });
  }

  function alterarDiaAgenda(delta){
    const inp=document.getElementById('agenda-data-filtro'); if(!inp) return;
    const base=inp.value?new Date(inp.value+'T12:00:00'):new Date();
    base.setDate(base.getDate()+delta);
    inp.value=base.toISOString().slice(0,10);
    inp.dispatchEvent(new Event('change',{bubbles:true}));
  }
  window.simplaAgendaDiaAnterior=()=>alterarDiaAgenda(-1);
  window.simplaAgendaProximoDia=()=>alterarDiaAgenda(1);
  window.simplaAgendaHoje=()=>{const inp=document.getElementById('agenda-data-filtro');if(!inp)return;const d=new Date();inp.value=[d.getFullYear(),String(d.getMonth()+1).padStart(2,'0'),String(d.getDate()).padStart(2,'0')].join('-');inp.dispatchEvent(new Event('change',{bubbles:true}));};

  function melhorarAgenda(){
    if(document.getElementById('agenda-toolbar-nav')) return;
    const data=document.getElementById('agenda-data-filtro'); if(!data) return;
    const pai=data.parentElement;if(!pai)return;
    const nav=document.createElement('div');nav.id='agenda-toolbar-nav';nav.className='agenda-toolbar-nav';
    nav.innerHTML='<button type="button" class="agenda-nav-btn" onclick="simplaAgendaDiaAnterior()" title="Dia anterior">‹</button><button type="button" class="agenda-nav-btn" onclick="simplaAgendaHoje()">Hoje</button><button type="button" class="agenda-nav-btn" onclick="simplaAgendaProximoDia()" title="Próximo dia">›</button>';
    pai.insertBefore(nav,data);
  }

  function ajustar(){
    montarDias();
    removerTema();
    moverNotificacoes();
    limparCategoriasVazias();
    melhorarAgenda();
  }
  document.addEventListener('DOMContentLoaded',()=>setTimeout(ajustar,80));
  let tentativas=0;const t=setInterval(()=>{ajustar();if(++tentativas>30)clearInterval(t);},300);
})();
</script>
'''
if 'id="simpla-ux-config-agenda-v3-js"' not in s:
    s=s.replace('</body>',js+'\n</body>',1)

p.write_text(s,encoding='utf-8')
print('patch ux v3 aplicado')
