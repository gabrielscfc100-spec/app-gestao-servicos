from pathlib import Path
import re

idx=Path('index.html')
sw=Path('service-worker.js')
html=idx.read_text(encoding='utf-8')

if 'simpla-meu-plano-v57' in html:
    raise SystemExit('v57 ja aplicada')

marker='</body>'
if marker not in html:
    raise SystemExit('body nao encontrado')

block=r'''
<style id="simpla-meu-plano-v57-css">
  .simpla-meu-plano-v57{margin:0 0 18px;border:1px solid #dbe4ee;border-radius:12px;background:#fff;padding:16px;box-shadow:0 2px 5px rgba(15,23,42,.04);text-transform:none}
  .simpla-meu-plano-v57-head{display:flex;justify-content:space-between;align-items:flex-start;gap:12px;flex-wrap:wrap;margin-bottom:14px}
  .simpla-meu-plano-v57-head h3{margin:0;font-size:16px;color:#1a1c23}.simpla-meu-plano-v57-head p{margin:4px 0 0;font-size:11px;color:#718096;line-height:1.45}
  .simpla-meu-plano-v57-badge{display:inline-flex;align-items:center;padding:6px 9px;border-radius:999px;background:#edf2f7;color:#2d3748;font-size:9px;font-weight:900;text-transform:uppercase}
  .simpla-meu-plano-v57-badge.teste{background:#ebf8ff;color:#2b6cb0}
  .simpla-meu-plano-v57-grid{display:grid;grid-template-columns:1fr 1fr 1fr;gap:9px;margin-bottom:14px}
  .simpla-meu-plano-v57-kpi{border:1px solid #e2e8f0;border-radius:9px;background:#f8fafc;padding:10px}.simpla-meu-plano-v57-kpi span{display:block;font-size:8px;font-weight:900;color:#718096;margin-bottom:4px}.simpla-meu-plano-v57-kpi strong{font-size:17px;color:#1a1c23}
  .simpla-meu-plano-v57-recursos{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:7px}.simpla-meu-plano-v57-recurso{display:flex;align-items:center;justify-content:space-between;gap:10px;border:1px solid #edf2f7;border-radius:8px;padding:8px 9px;font-size:10px;color:#475569}.simpla-meu-plano-v57-recurso b{color:#2d3748;font-size:10px}.simpla-meu-plano-v57-ok{font-weight:900;color:#2f855a}.simpla-meu-plano-v57-off{font-weight:900;color:#a0aec0}
  .simpla-meu-plano-v57-upgrade{margin-top:12px;padding:10px 11px;border-radius:8px;background:#f8fafc;border:1px solid #e2e8f0;color:#475569;font-size:10px;line-height:1.45}.simpla-meu-plano-v57-upgrade b{color:#1a1c23}
  @media(max-width:760px){.simpla-meu-plano-v57-grid{grid-template-columns:1fr}.simpla-meu-plano-v57-recursos{grid-template-columns:1fr}}
</style>
<script id="simpla-meu-plano-v57">
(function(){
  const NOMES={
    agenda:'Agenda',agenda_publica:'Agenda pública',clientes:'Clientes',profissionais:'Profissionais',servicos:'Serviços',financeiro_basico:'Financeiro básico',dashboard_basico:'Dashboard básico',portal_cliente:'Portal do cliente',recorrencia_basica:'Recorrência básica',exportacao_basica:'Exportação básica',perfis_permissoes_avancadas:'Perfis e permissões avançadas',dashboard_avancado:'Dashboard avançado',comparativo_periodos:'Comparativo de períodos',ranking_servico_profissional:'Ranking por serviço/profissional',radar_retornos_completo:'Radar de Retornos completo',minha_prioridade_hoje:'Minha Prioridade Hoje',oportunidades_agenda:'Oportunidades de Agenda',pacotes_creditos:'Pacotes e créditos',recorrencia_avancada:'Recorrência avançada',auditoria_completa:'Auditoria completa',exportacao_completa:'Exportação completa',whatsapp_operacional:'WhatsApp operacional',whatsapp_campanhas:'Campanhas por WhatsApp',simpla_ia:'SimplA IA',radar_inteligente:'Radar inteligente',reativacao_inteligente:'Reativação inteligente'
  };
  const ORDEM=['agenda','agenda_publica','clientes','profissionais','servicos','financeiro_basico','dashboard_basico','portal_cliente','recorrencia_basica','exportacao_basica','perfis_permissoes_avancadas','dashboard_avancado','comparativo_periodos','ranking_servico_profissional','radar_retornos_completo','minha_prioridade_hoje','oportunidades_agenda','pacotes_creditos','recorrencia_avancada','auditoria_completa','exportacao_completa','whatsapp_operacional','whatsapp_campanhas','simpla_ia','radar_inteligente','reativacao_inteligente'];
  function garantir(){
    let box=document.getElementById('simpla-meu-plano-v57');if(box)return box;
    const usuarios=document.getElementById('box-cfg-usuarios');
    const config=document.getElementById('configuracoes')||document.getElementById('settings');
    if(!usuarios&&!config)return null;
    box=document.createElement('section');box.id='simpla-meu-plano-v57';box.className='simpla-meu-plano-v57';
    box.innerHTML='<div class="simpla-meu-plano-v57-head"><div><h3>Meu Plano</h3><p>Veja o plano atual, utilização de acessos e recursos incluídos. Alteração de plano e cobrança serão adicionadas em uma etapa posterior.</p></div><span id="simpla-meu-plano-v57-badge" class="simpla-meu-plano-v57-badge">Carregando</span></div><div class="simpla-meu-plano-v57-grid"><div class="simpla-meu-plano-v57-kpi"><span>PLANO ATUAL</span><strong id="simpla-meu-plano-v57-nome">—</strong></div><div class="simpla-meu-plano-v57-kpi"><span>DEPENDENTES</span><strong id="simpla-meu-plano-v57-deps">—</strong></div><div class="simpla-meu-plano-v57-kpi"><span>ACESSO</span><strong id="simpla-meu-plano-v57-acesso">—</strong></div></div><div id="simpla-meu-plano-v57-recursos" class="simpla-meu-plano-v57-recursos"><div class="simpla-meu-plano-v57-recurso">Carregando recursos...</div></div><div id="simpla-meu-plano-v57-upgrade" class="simpla-meu-plano-v57-upgrade" style="display:none"></div>';
    if(usuarios)usuarios.insertAdjacentElement('beforebegin',box);else config.appendChild(box);
    return box;
  }
  function proximoPlano(c){c=String(c||'').toUpperCase();if(c==='BASICO')return 'PLUS';if(c==='PLUS')return 'PRO';return null}
  async function carregar(){
    const box=garantir();if(!box||typeof CloudDB==='undefined'||!CloudDB||typeof empresaAtual==='undefined'||!empresaAtual?.id)return;
    try{
      const [{data:status,error:e1},{data:planos,error:e2}]=await Promise.all([
        CloudDB.rpc('status_limite_dependentes_empresa',{p_empresa_id:empresaAtual.id}),
        CloudDB.from('planos_catalogo').select('codigo,nome,limite_dependentes,recursos,ativo').eq('ativo',true)
      ]);
      if(e1)throw e1;if(e2)throw e2;
      const st=Array.isArray(status)?status[0]:status;
      const todos=Array.isArray(planos)?planos:[];
      const codigo=String(st?.plano_codigo||empresaAtual.plano_codigo||'BASICO').toUpperCase();
      const atual=todos.find(p=>String(p.codigo).toUpperCase()===codigo)||{codigo,nome:codigo,limite_dependentes:st?.limite_dependentes,recursos:{}};
      const teste=!!st?.modo_teste||codigo==='TESTE'||atual.limite_dependentes==null;
      const badge=document.getElementById('simpla-meu-plano-v57-badge');badge.textContent=teste?'Conta de testes':`Plano ${atual.nome||codigo}`;badge.classList.toggle('teste',teste);
      document.getElementById('simpla-meu-plano-v57-nome').textContent=atual.nome||codigo;
      document.getElementById('simpla-meu-plano-v57-deps').textContent=teste?'Ilimitado':`${Number(st?.dependentes_ativos||0)} / ${Number(st?.limite_dependentes??atual.limite_dependentes??0)}`;
      document.getElementById('simpla-meu-plano-v57-acesso').textContent=teste?'Total':codigo==='BASICO'?'Essencial':codigo==='PLUS'?'Avançado':'Completo';
      const recursos=atual.recursos||{};const lista=document.getElementById('simpla-meu-plano-v57-recursos');
      const chaves=teste?ORDEM:ORDEM.filter(k=>Object.prototype.hasOwnProperty.call(recursos,k));
      lista.innerHTML=chaves.map(k=>{const ok=teste||recursos[k]===true;return `<div class="simpla-meu-plano-v57-recurso"><b>${NOMES[k]||k}</b><span class="${ok?'simpla-meu-plano-v57-ok':'simpla-meu-plano-v57-off'}">${ok?'Incluído':'Não incluído'}</span></div>`}).join('')||'<div class="simpla-meu-plano-v57-recurso">Nenhum recurso configurado.</div>';
      const up=document.getElementById('simpla-meu-plano-v57-upgrade');const prox=proximoPlano(codigo);
      if(teste){up.style.display='block';up.innerHTML='<b>Ambiente de desenvolvimento.</b> Esta conta ignora todas as limitações de plano para permitir testes completos do SimplA.'}
      else if(prox){const p=todos.find(x=>String(x.codigo).toUpperCase()===prox);up.style.display='block';up.innerHTML=`<b>Próximo plano: ${p?.nome||prox}.</b> A contratação ainda não está ativa. Esta área será usada futuramente para comparar recursos e solicitar upgrade.`}
      else{up.style.display='none'}
    }catch(err){console.error('Meu Plano v57:',err);const r=document.getElementById('simpla-meu-plano-v57-recursos');if(r)r.innerHTML='<div class="simpla-meu-plano-v57-recurso">Não foi possível carregar os dados do plano agora.</div>'}
  }
  window.carregarMeuPlanoV57=carregar;
  function instalar(){garantir();setTimeout(carregar,850)}
  if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',()=>setTimeout(instalar,2700));else setTimeout(instalar,2700);
})();
</script>
'''

html=html.replace(marker,block+'\n'+marker,1)
idx.write_text(html,encoding='utf-8')

swtxt=sw.read_text(encoding='utf-8')
swtxt,n=re.subn(r"const CACHE_VERSION = '[^']+';","const CACHE_VERSION = 'simpla-shell-v57-meu-plano';",swtxt,count=1)
if n!=1:
    raise SystemExit('cache version nao encontrada')
sw.write_text(swtxt,encoding='utf-8')
