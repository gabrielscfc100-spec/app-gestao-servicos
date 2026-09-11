from pathlib import Path
import re

p=Path('index.html')
s=p.read_text(encoding='utf-8')
marker='<!-- SIMPLA clientes dependentes v39 -->'

# Carregar os novos campos do banco no cache de clientes
old_select="id,empresa_id,codigo,nome,sobrenome,telefone,aniversario,email,rua,bairro,cidade,instagram,tiktok,facebook,twitter,observacoes,criado_em,atualizado_em"
new_select="id,empresa_id,codigo,nome,sobrenome,telefone,aniversario,email,rua,bairro,cidade,instagram,tiktok,facebook,twitter,observacoes,responsavel_cliente_id,responsavel_vinculo,criado_em,atualizado_em"
s=s.replace(old_select,new_select)

# Mapear campos cloud -> local quando o objeto é carregado/recarregado
needle="""                codigo: row.codigo || '',\n                nome: row.nome || '',"""
replacement="""                codigo: row.codigo || '',\n                responsavelClienteId: row.responsavel_cliente_id || null,\n                responsavelVinculo: row.responsavel_vinculo || '',\n                nome: row.nome || '',"""
s=s.replace(needle,replacement)

if marker not in s:
    bloco=r'''
<!-- SIMPLA clientes dependentes v39 -->
<style id="simpla-clientes-dependentes-v39-style">
#simpla-dependente-v39{margin:10px 0 16px;padding:12px;border:1px solid #bee3f8;background:#ebf8ff;border-radius:8px;text-transform:none}
#simpla-dependente-v39 label{display:flex;align-items:center;gap:8px;font-size:13px;font-weight:700;color:#2c5282;text-transform:none;cursor:pointer}
#simpla-dependente-v39 input[type=checkbox]{width:18px;height:18px}
#simpla-dependente-campos-v39{display:none;margin-top:12px;gap:10px;grid-template-columns:1fr 180px}
#simpla-dependente-v39.ativo #simpla-dependente-campos-v39{display:grid}
#simpla-dependente-campos-v39 select{width:100%;padding:9px;border:1px solid #cbd5e0;border-radius:5px;background:#fff}
#simpla-modal-dependente-v39{position:fixed;inset:0;background:rgba(15,23,42,.65);z-index:10100;display:none;align-items:center;justify-content:center;padding:18px}
#simpla-modal-dependente-v39.ativo{display:flex}
#simpla-modal-dependente-v39 .box{background:#fff;width:min(470px,100%);border-radius:12px;padding:20px;box-shadow:0 24px 60px rgba(0,0,0,.25)}
#simpla-modal-dependente-v39 h3{margin:0 0 8px;font-size:19px;color:#1a202c}
#simpla-modal-dependente-v39 p{margin:0 0 15px;color:#718096;font-size:13px;line-height:1.5;text-transform:none}
#simpla-modal-dependente-v39 .acoes{display:flex;gap:10px;justify-content:flex-end;margin-top:18px;flex-wrap:wrap}
.simpla-relacao-v39{margin-top:8px;padding-top:8px;border-top:1px solid #e2e8f0;font-size:12px;color:#4a5568;text-transform:none}
@media(max-width:600px){#simpla-dependente-campos-v39{grid-template-columns:1fr}#simpla-modal-dependente-v39 .acoes{display:grid;grid-template-columns:1fr;width:100%}}
</style>
<script id="simpla-clientes-dependentes-v39-script">
(function(){
  let instalando=false;
  function lista(){try{return Array.isArray(clientes)?clientes:[]}catch(_){return []}}
  function normTel(v){return String(v||'').replace(/\D/g,'')}
  function normEmail(v){return String(v||'').trim().toLowerCase()}
  function dupAtual(){
    const tel=normTel(document.getElementById('cli-telefone')?.value||'');
    const mail=normEmail(document.getElementById('cli-email')?.value||'');
    return lista().find(c=>(tel&&normTel(c.telefone)===tel)||(mail&&normEmail(c.email)===mail))||null;
  }
  function nome(c){return ((c?.nome||'')+' '+(c?.sobrenome||'')).trim()||'Cliente'}
  function opcoes(sel,selecionado){
    if(!sel)return;
    sel.innerHTML='<option value="">Selecione o responsável</option>'+lista().map(c=>`<option value="${c.id}" ${String(c.id)===String(selecionado||'')?'selected':''}>${nome(c)}${c.codigo?' · '+c.codigo:''}</option>`).join('');
  }
  function montarCadastro(){
    if(document.getElementById('simpla-dependente-v39'))return;
    const alvo=document.getElementById('group-cli-email')||document.getElementById('group-cli-telefone');
    if(!alvo)return;
    const box=document.createElement('div');box.id='simpla-dependente-v39';
    box.innerHTML='<label><input type="checkbox" id="simpla-dependente-check-v39"> Cliente é dependente e utiliza o contato de um responsável</label><div id="simpla-dependente-campos-v39"><select id="simpla-dependente-responsavel-v39"></select><select id="simpla-dependente-vinculo-v39"><option value="">Vínculo com o responsável</option><option>MÃE</option><option>PAI</option><option>RESPONSÁVEL</option><option>AVÓ/AVÔ</option><option>TUTOR(A)</option><option>OUTRO</option></select></div>';
    alvo.insertAdjacentElement('afterend',box);
    opcoes(box.querySelector('#simpla-dependente-responsavel-v39'));
    box.querySelector('#simpla-dependente-check-v39').addEventListener('change',e=>box.classList.toggle('ativo',e.target.checked));
  }
  function montarModal(){
    let m=document.getElementById('simpla-modal-dependente-v39');if(m)return m;
    m=document.createElement('div');m.id='simpla-modal-dependente-v39';
    m.innerHTML='<div class="box"><h3>Vincular como dependente</h3><p>O cadastro será criado sem repetir o telefone/e-mail do responsável. O vínculo ficará salvo no histórico dos dois clientes.</p><div class="form-group"><label>Responsável *</label><select id="simpla-modal-responsavel-v39" style="width:100%;padding:10px;border:1px solid #cbd5e0;border-radius:5px"></select></div><div class="form-group"><label>Vínculo *</label><select id="simpla-modal-vinculo-v39" style="width:100%;padding:10px;border:1px solid #cbd5e0;border-radius:5px"><option value="">Selecione</option><option>MÃE</option><option>PAI</option><option>RESPONSÁVEL</option><option>AVÓ/AVÔ</option><option>TUTOR(A)</option><option>OUTRO</option></select></div><div class="acoes"><button class="btn-cancelar-modal" type="button" onclick="fecharModalDependenteV39()">Voltar</button><button class="btn-salvar" type="button" onclick="confirmarDependenteV39()">Criar e vincular</button></div></div>';
    document.body.appendChild(m);return m;
  }
  window.abrirModalDependenteV39=function(responsavelId){
    document.getElementById('modal-cliente-duplicado')?.classList.remove('active');
    const m=montarModal();opcoes(m.querySelector('#simpla-modal-responsavel-v39'),responsavelId||dupAtual()?.id);m.classList.add('ativo');
  };
  window.fecharModalDependenteV39=function(){document.getElementById('simpla-modal-dependente-v39')?.classList.remove('ativo')};
  function dadosForm(){
    const get=id=>document.getElementById(id)?.value?.trim?.()||'';
    return {nome:get('cli-nome'),sobrenome:get('cli-sobrenome'),telefone:'',aniversario:get('cli-aniversario'),email:'',rua:get('cli-rua'),bairro:get('cli-bairro'),cidade:get('cli-cidade'),instagram:get('cli-instagram'),tiktok:get('cli-tiktok'),facebook:get('cli-facebook'),twitter:get('cli-twitter'),obs:get('cli-obs')};
  }
  async function criarDependente(respId,vinculo){
    if(!respId){alert('Selecione o responsável.');return null}
    if(!vinculo){alert('Informe o vínculo com o responsável.');return null}
    const d=dadosForm();if(!d.nome){alert('Preencha o nome do dependente.');return null}
    if(typeof salvarNovoClienteDireto!=='function'){alert('Não foi possível acessar o cadastro de clientes.');return null}
    const novo=await salvarNovoClienteDireto(d);if(!novo)return null;
    try{
      if(typeof CloudDB!=='undefined'&&CloudDB&&typeof empresaAtual!=='undefined'&&empresaAtual?.id&&novo.id){
        const {data,error}=await CloudDB.from('clientes').update({responsavel_cliente_id:respId,responsavel_vinculo:vinculo,atualizado_em:new Date().toISOString()}).eq('id',novo.id).eq('empresa_id',empresaAtual.id).select().single();
        if(error)throw error;
      }
      novo.responsavelClienteId=respId;novo.responsavelVinculo=vinculo;
      try{salvarCacheClientesCloud?.()}catch(_){ }try{salvarStorage?.()}catch(_){ }
      try{sincronizarDadosClientesTodasAsTelas?.()}catch(_){ }
      try{await registrarAuditoria?.('CLIENTES','DEPENDENTE_VINCULADO',novo.id,{responsavel_cliente_id:respId,vinculo})}catch(_){ }
      return novo;
    }catch(e){
      console.error(e);alert('O cliente foi criado, mas não foi possível salvar o vínculo com o responsável: '+(e?.message||'erro desconhecido'));return novo;
    }
  }
  window.confirmarDependenteV39=async function(){
    const m=document.getElementById('simpla-modal-dependente-v39');
    const r=m?.querySelector('#simpla-modal-responsavel-v39')?.value||'';const v=m?.querySelector('#simpla-modal-vinculo-v39')?.value||'';
    const novo=await criarDependente(r,v);if(novo){m?.classList.remove('ativo');alert('Dependente cadastrado e vinculado ao responsável.');}
  };
  async function salvarDependenteFormulario(){
    const box=document.getElementById('simpla-dependente-v39');
    if(!box?.querySelector('#simpla-dependente-check-v39')?.checked)return false;
    const r=box.querySelector('#simpla-dependente-responsavel-v39')?.value||'';const v=box.querySelector('#simpla-dependente-vinculo-v39')?.value||'';
    const novo=await criarDependente(r,v);if(novo)alert('Dependente cadastrado e vinculado ao responsável.');return true;
  }
  function adicionarBotaoDuplicidade(){
    const modal=document.getElementById('modal-cliente-duplicado');if(!modal)return;
    const obs=new MutationObserver(()=>{
      if(!modal.classList.contains('active'))return;
      const botoes=modal.querySelector('.modal-botoes');if(!botoes||botoes.querySelector('.btn-dependente-v39'))return;
      const dup=dupAtual();if(!dup)return;
      const b=document.createElement('button');b.type='button';b.className='btn-salvar btn-dependente-v39';b.style.background='#805ad5';b.style.color='white';b.textContent='Vincular como dependente';b.onclick=()=>window.abrirModalDependenteV39(dup.id);botoes.appendChild(b);
    });obs.observe(modal,{attributes:true,attributeFilter:['class'],subtree:false});
  }
  function enriquecerHistorico(id){
    const c=lista().find(x=>String(x.id)===String(id));const det=document.getElementById('hist-cli-detalhes');if(!c||!det)return;
    det.querySelectorAll('.simpla-relacao-v39').forEach(x=>x.remove());
    const resp=c.responsavelClienteId?lista().find(x=>String(x.id)===String(c.responsavelClienteId)):null;
    const deps=lista().filter(x=>String(x.responsavelClienteId||'')===String(c.id));
    if(!resp&&!deps.length)return;
    const div=document.createElement('div');div.className='simpla-relacao-v39';
    let h='';if(resp)h+=`<b>Responsável:</b> <a href="#" onclick="abrirHistoricoCliente('${resp.id}');return false;">${nome(resp)}</a>${c.responsavelVinculo?' · '+c.responsavelVinculo:''}`;
    if(deps.length)h+=(h?'<br>':'')+'<b>Dependentes:</b> '+deps.map(d=>`<a href="#" onclick="abrirHistoricoCliente('${d.id}');return false;">${nome(d)}</a>${d.responsavelVinculo?' ('+d.responsavelVinculo+')':''}`).join(', ');
    div.innerHTML=h;det.appendChild(div);
  }
  function instalar(){
    if(instalando)return;instalando=true;try{
      montarCadastro();montarModal();adicionarBotaoDuplicidade();
      if(typeof cadastrarCliente==='function'&&!cadastrarCliente.__v39){
        const anterior=cadastrarCliente;const w=async function(){if(await salvarDependenteFormulario())return;return await anterior.apply(this,arguments)};w.__v39=true;window.cadastrarCliente=w;try{cadastrarCliente=w}catch(_){ }
      }
      if(typeof abrirHistoricoCliente==='function'&&!abrirHistoricoCliente.__v39){
        const anteriorH=abrirHistoricoCliente;const wh=function(id){const r=anteriorH.apply(this,arguments);setTimeout(()=>enriquecerHistorico(id),0);return r};wh.__v39=true;window.abrirHistoricoCliente=wh;try{abrirHistoricoCliente=wh}catch(_){ }
      }
    }finally{instalando=false}
  }
  if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',()=>setTimeout(instalar,500));else setTimeout(instalar,500);
  setTimeout(instalar,1500);
})();
</script>
'''
    s=s.replace('</body>',bloco+'\n</body>',1)

p.write_text(s,encoding='utf-8')

sw=Path('service-worker.js')
t=sw.read_text(encoding='utf-8')
t=re.sub(r"const CACHE_VERSION = ['\"][^'\"]+['\"]", "const CACHE_VERSION = 'simpla-shell-v39-clientes-dependentes'", t, count=1)
sw.write_text(t,encoding='utf-8')
print('v39 aplicada')
