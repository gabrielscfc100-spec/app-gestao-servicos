from pathlib import Path
import re

idx=Path('index.html')
sw=Path('service-worker.js')
html=idx.read_text(encoding='utf-8')

if 'simpla-oportunidades-agenda-v54' in html:
    raise SystemExit('v54 ja aplicada')

marker='</body>'
if marker not in html:
    raise SystemExit('body nao encontrado')

block=r'''
<style id="simpla-oportunidades-agenda-v54-css">
  .dash-ocio-v54{margin:0 0 18px;background:#fff;border:1px solid #dbe4ee;border-radius:11px;padding:16px;box-shadow:0 2px 5px rgba(15,23,42,.05)}
  .dash-ocio-v54-head{display:flex;justify-content:space-between;gap:12px;align-items:flex-start;flex-wrap:wrap;margin-bottom:12px}
  .dash-ocio-v54-head h3{margin:0;font-size:16px;color:#1a1c23}
  .dash-ocio-v54-head p{margin:4px 0 0;font-size:11px;color:#718096;text-transform:none;line-height:1.4}
  .dash-ocio-v54-refresh{border:1px solid #cbd5e0;background:#fff;border-radius:6px;padding:8px 10px;cursor:pointer;font-size:9px;font-weight:900;color:#2d3748}
  .dash-ocio-v54-resumo{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:8px;margin-bottom:12px}
  .dash-ocio-v54-kpi{border:1px solid #e2e8f0;border-radius:8px;padding:9px;background:#f8fafc}
  .dash-ocio-v54-kpi span{display:block;font-size:8px;font-weight:900;color:#718096;margin-bottom:3px}
  .dash-ocio-v54-kpi strong{font-size:18px;color:#1a1c23}
  .dash-ocio-v54-list{display:grid;gap:7px}
  .dash-ocio-v54-item{display:grid;grid-template-columns:100px minmax(0,1fr) minmax(0,1fr) 92px;gap:9px;align-items:center;border:1px solid #edf2f7;border-radius:8px;padding:9px 10px;background:#fff}
  .dash-ocio-v54-item b{font-size:10px;color:#2d3748}
  .dash-ocio-v54-item span{font-size:9px;color:#718096;text-transform:none;line-height:1.35}
  .dash-ocio-v54-tag{display:inline-flex;justify-content:center;padding:5px 7px;border-radius:999px;font-size:8px!important;font-weight:900;text-transform:uppercase!important;background:#edf2f7;color:#4a5568!important}
  .dash-ocio-v54-tag.alta{background:#fffaf0;color:#b7791f!important}.dash-ocio-v54-tag.media{background:#ebf8ff;color:#2b6cb0!important}
  .dash-ocio-v54-acao{border:0;border-radius:6px;padding:7px 8px;background:#1a1c23;color:#fff;font-size:8px;font-weight:900;cursor:pointer}.dash-ocio-v54-acao:hover{background:var(--cor-accent);color:#1a1c23}
  .dash-ocio-v54-empty{border:1px dashed #cbd5e0;border-radius:8px;padding:14px;text-align:center;color:#718096;font-size:11px;text-transform:none}
  .dash-ocio-v54-foot{margin-top:9px;color:#718096;font-size:9px;text-transform:none;line-height:1.45}
  @media(max-width:760px){.dash-ocio-v54-resumo{grid-template-columns:1fr 1fr 1fr}.dash-ocio-v54-item{grid-template-columns:86px minmax(0,1fr) 76px}.dash-ocio-v54-item .detalhe{grid-column:2}.dash-ocio-v54-acao{grid-column:3;grid-row:1/3}}
</style>
<script id="simpla-oportunidades-agenda-v54">
(function(){
  let itens=[];
  const HORIZONTE=7;
  function arr(nome){try{return Array.isArray(window[nome])?window[nome]:eval(`typeof ${nome}!=='undefined'&&Array.isArray(${nome})?${nome}:[]`)}catch(_){return []}}
  function pad(n){return String(n).padStart(2,'0')}
  function hoje(){if(typeof obterHojeLocal==='function')return obterHojeLocal();const d=new Date();return `${d.getFullYear()}-${pad(d.getMonth()+1)}-${pad(d.getDate())}`}
  function dataISO(base,add){const [a,m,d]=base.split('-').map(Number),dt=new Date(a,m-1,d);dt.setDate(dt.getDate()+add);return `${dt.getFullYear()}-${pad(dt.getMonth()+1)}-${pad(dt.getDate())}`}
  function dataBR(v){const p=String(v||'').slice(0,10).split('-');return p.length===3?`${p[2]}/${p[1]}/${p[0]}`:String(v||'-')}
  function min(h){const [a,b]=String(h||'00:00').split(':').map(Number);return (a||0)*60+(b||0)}
  function hora(m){m=Math.max(0,Math.min(1439,Math.round(m)));return `${pad(Math.floor(m/60))}:${pad(m%60)}`}
  function status(a){return String(a.status||a.situacao||'AGENDADO').toUpperCase()}
  function dataAg(a){return String(a.data||a.data_agendamento||'').slice(0,10)}
  function profAg(a){return a.profissionalId||a.profissional_id||null}
  function inicioAg(a){return min(a.horario||a.hora_inicio||a.horaInicio||'00:00')}
  function durAg(a){return Number(a.duracao||a.duracao_min||a.duracaoMin||((typeof configExpediente!=='undefined'&&configExpediente?.intervalo)||45))||45}
  function getProfissionais(){return arr('profissionais').filter(p=>p&&p.ativo!==false)}
  function intervalo(){return Math.max(5,Number((typeof configExpediente!=='undefined'&&configExpediente?.intervalo)||45)||45)}
  function abertura(){return min((typeof configExpediente!=='undefined'&&configExpediente?.abertura)||'08:00')}
  function fechamento(){return min((typeof configExpediente!=='undefined'&&configExpediente?.fechamento)||'18:00')}
  function bloqueia(b,data,prof,start,end){
    const bp=b.profissionalId||b.profissional_id||null;
    if(bp && String(bp)!==String(prof))return false;
    const ini=String(b.dataInicio||b.data_inicio||b.data||'').slice(0,10), fim=String(b.dataFim||b.data_fim||b.data||ini).slice(0,10);
    const rec=String(b.recorrencia||b.tipoRecorrencia||'').toUpperCase();
    let bateData=false;
    if(rec==='SEMANAL'){
      const [a,m,d]=data.split('-').map(Number),dow=new Date(a,m-1,d).getDay();
      const dia=Number(b.diaSemana??b.dia_semana??-1);
      bateData=(dia===dow)&&(!ini||data>=ini)&&(!fim||data<=fim);
    }else bateData=(!ini||data>=ini)&&(!fim||data<=fim);
    if(!bateData)return false;
    const esc=String(b.escopo||b.tipo||'').toUpperCase();
    if(esc==='DIA_INTEIRO'||(!b.horaInicio&&!b.hora_inicio&&!b.horario))return true;
    const bi=min(b.horaInicio||b.hora_inicio||b.horario||'00:00');
    const bf=min(b.horaFim||b.hora_fim||b.horarioFim||hora(bi+intervalo()));
    return start<bf && end>bi;
  }
  function ocupado(data,prof,start,end){
    const ag=arr('agendamentos').some(a=>dataAg(a)===data&&String(profAg(a)||'')===String(prof)&&!['CANCELADO','NAO_COMPARECEU'].includes(status(a))&&start<(inicioAg(a)+durAg(a))&&end>inicioAg(a));
    if(ag)return true;
    return arr('bloqueios').some(b=>bloqueia(b,data,prof,start,end));
  }
  function agoraMin(){const d=new Date();return d.getHours()*60+d.getMinutes()}
  function detectar(){
    const profs=getProfissionais(), base=hoje(), int=intervalo(), inicio=abertura(), fim=fechamento(), minimo=Math.max(60,int*2), saida=[];
    for(let dia=0;dia<HORIZONTE;dia++){
      const data=dataISO(base,dia);
      for(const p of profs){
        let blocoIni=null, ultimo=null;
        const fecharBloco=()=>{if(blocoIni==null||ultimo==null)return;const dur=ultimo-blocoIni;if(dur>=minimo)saida.push({data,profissional_id:p.id,profissional_nome:p.nome||'Profissional',inicio:hora(blocoIni),fim:hora(ultimo),duracao:dur,nivel:dur>=180?'ALTA':'MEDIA'});blocoIni=null;ultimo=null};
        for(let t=inicio;t+int<=fim;t+=int){
          if(dia===0 && t<agoraMin()) {fecharBloco();continue}
          const livre=!ocupado(data,p.id,t,t+int);
          if(livre){if(blocoIni==null)blocoIni=t;ultimo=t+int}else fecharBloco();
        }
        fecharBloco();
      }
    }
    return saida.sort((a,b)=>a.data.localeCompare(b.data)||b.duracao-a.duracao||a.inicio.localeCompare(b.inicio));
  }
  function garantir(){
    const dash=document.getElementById('dashboard');if(!dash)return null;let box=document.getElementById('dash-ocio-v54');if(box)return box;
    box=document.createElement('div');box.id='dash-ocio-v54';box.className='dash-ocio-v54';
    box.innerHTML=`<div class="dash-ocio-v54-head"><div><h3>Oportunidades de Agenda</h3><p>Janelas livres relevantes nos próximos 7 dias, calculadas a partir do expediente, agendamentos e bloqueios já registrados.</p></div><button class="dash-ocio-v54-refresh" type="button" onclick="carregarOportunidadesAgendaV54()">↻ Atualizar</button></div><div class="dash-ocio-v54-resumo"><div class="dash-ocio-v54-kpi"><span>JANELAS IDENTIFICADAS</span><strong id="ocio-v54-total">0</strong></div><div class="dash-ocio-v54-kpi"><span>3H OU MAIS</span><strong id="ocio-v54-altas">0</strong></div><div class="dash-ocio-v54-kpi"><span>HORAS LIVRES MAPEADAS</span><strong id="ocio-v54-horas">0h</strong></div></div><div id="dash-ocio-v54-list" class="dash-ocio-v54-list"><div class="dash-ocio-v54-empty">Analisando a agenda...</div></div><div class="dash-ocio-v54-foot">Oportunidade de agenda não significa demanda garantida. O SimplA apenas destaca capacidade disponível; nenhuma pessoa é contatada automaticamente.</div>`;
    const prio=document.getElementById('dash-prio-v53'),radar=document.getElementById('dash-ret-v51');if(prio)prio.insertAdjacentElement('afterend',box);else if(radar)radar.insertAdjacentElement('beforebegin',box);else dash.insertAdjacentElement('afterbegin',box);return box;
  }
  window.abrirOportunidadeAgendaV54=function(i){const x=itens[Number(i)];if(!x)return;try{if(typeof mudarTela==='function')mudarTela('agenda')}catch(_){ }const d=document.getElementById('agenda-data-filtro');if(d){d.value=x.data;d.dispatchEvent(new Event('change',{bubbles:true}))}const p=document.getElementById('agenda-profissional-filtro');if(p){const opt=[...p.options].find(o=>String(o.value)===String(x.profissional_id));if(opt){p.value=opt.value;p.dispatchEvent(new Event('change',{bubbles:true}))}}try{if(typeof renderizarAgenda==='function')renderizarAgenda()}catch(_){ }};
  function render(){const list=document.getElementById('dash-ocio-v54-list');if(!list)return;if(!itens.length){list.innerHTML='<div class="dash-ocio-v54-empty">Nenhuma janela livre relevante foi identificada nos próximos 7 dias.</div>';return}list.innerHTML=itens.slice(0,10).map((x,i)=>`<div class="dash-ocio-v54-item"><span class="dash-ocio-v54-tag ${x.nivel.toLowerCase()}">${x.nivel==='ALTA'?'Alta ociosidade':'Janela livre'}</span><div><b>${x.profissional_nome}</b><br><span>${dataBR(x.data)}</span></div><div class="detalhe"><b>${x.inicio}–${x.fim}</b><br><span>${Math.floor(x.duracao/60)}h${x.duracao%60?` ${x.duracao%60}min`:''} disponíveis em sequência</span></div><button class="dash-ocio-v54-acao" type="button" onclick="abrirOportunidadeAgendaV54(${i})">Ver agenda</button></div>`).join('');if(itens.length>10)list.insertAdjacentHTML('beforeend',`<div class="dash-ocio-v54-empty">Mostrando 10 de ${itens.length} janelas identificadas.</div>`)}
  function carregar(){garantir();try{itens=detectar();document.getElementById('ocio-v54-total').textContent=String(itens.length);document.getElementById('ocio-v54-altas').textContent=String(itens.filter(x=>x.duracao>=180).length);const horas=itens.reduce((s,x)=>s+x.duracao,0)/60;document.getElementById('ocio-v54-horas').textContent=`${horas.toFixed(horas%1?1:0)}h`;render()}catch(err){console.error('Oportunidades Agenda v54:',err);const l=document.getElementById('dash-ocio-v54-list');if(l)l.innerHTML='<div class="dash-ocio-v54-empty">Não foi possível analisar a ociosidade da agenda agora.</div>'}}
  window.carregarOportunidadesAgendaV54=carregar;
  function instalar(){garantir();setTimeout(carregar,650)}
  if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',()=>setTimeout(instalar,2600));else setTimeout(instalar,2600);
})();
</script>
'''

html=html.replace(marker,block+'\n'+marker,1)
idx.write_text(html,encoding='utf-8')

swtxt=sw.read_text(encoding='utf-8')
swtxt,n=re.subn(r"const CACHE_VERSION = '[^']+';","const CACHE_VERSION = 'simpla-shell-v54-oportunidades-agenda';",swtxt,count=1)
if n!=1:
    raise SystemExit('cache version nao encontrada')
sw.write_text(swtxt,encoding='utf-8')
