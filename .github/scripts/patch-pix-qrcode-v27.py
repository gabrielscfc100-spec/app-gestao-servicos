from pathlib import Path
import re

p=Path('index.html')
s=p.read_text(encoding='utf-8')
if 'simpla-pix-qrcode-v27' in s:
    raise SystemExit('v27 ja aplicada')

# QRCode library
if 'qrcode.min.js' not in s:
    s=s.replace('</head>', '<script src="https://cdnjs.cloudflare.com/ajax/libs/qrcodejs/1.0.0/qrcode.min.js"></script></head>', 1)

# Ensure PIX selector also refreshes QR UI
s=s.replace('onchange="atualizarPagamentoDivididoUI()"', 'onchange="atualizarPagamentoDivididoUI(); atualizarPixUI()"', 1)

# Refresh QR when cart total changes
needle='            atualizarResumoPagamentoDividido();\n        }\n\n        function atualizarPagamentoDivididoUI()'
if needle in s:
    s=s.replace(needle, '            atualizarResumoPagamentoDividido();\n            atualizarPixUI();\n        }\n\n        function atualizarPagamentoDivididoUI()', 1)

block=r'''
<style id="simpla-pix-qrcode-v27">
.pix-recebimento-box{display:none;margin-top:10px;padding:14px;border:1px solid #dbe4ee;border-radius:10px;background:#f8fafc;text-transform:none}
.pix-recebimento-box h4,.pix-recebimento-box p,.pix-recebimento-box small,.pix-recebimento-box button,.pix-config-v27 *{text-transform:none}
.pix-qr-wrap{display:flex;gap:16px;align-items:flex-start;flex-wrap:wrap;margin-top:12px}.pix-qr-code{background:#fff;padding:10px;border-radius:8px;border:1px solid #e2e8f0;min-width:180px;min-height:180px;display:flex;align-items:center;justify-content:center}.pix-copy-area{flex:1;min-width:220px}.pix-copy-area textarea{width:100%;min-height:96px;resize:vertical;text-transform:none;font-family:monospace;font-size:12px}.pix-copy-actions{display:flex;gap:8px;margin-top:8px;flex-wrap:wrap}.pix-copy-actions button{padding:9px 12px;border:0;border-radius:6px;cursor:pointer;font-weight:600}.pix-btn-primary{background:#1a1c23;color:#fff}.pix-btn-secondary{background:#e2e8f0;color:#2d3748}.pix-status{display:block;margin-top:8px;color:#718096;line-height:1.4}.pix-config-grid{display:grid;grid-template-columns:1fr 1fr;gap:12px}.pix-config-grid .form-group{margin-bottom:0}.pix-config-v27 input{text-transform:none!important}
@media(max-width:768px){.pix-config-grid{grid-template-columns:1fr}.pix-qr-wrap{display:block}.pix-qr-code{width:200px;margin:0 auto 12px}.pix-copy-area{min-width:0}.pix-copy-actions button{width:100%}}
</style>
<script id="simpla-pix-qrcode-v27">
(function(){
  const estado={empresaId:null,carregado:false,ativo:false,chave:'',nome:'',cidade:''};
  let ultimoPayload='';
  const normTxt=v=>String(v||'').trim();
  const semAcentos=v=>normTxt(v).normalize('NFD').replace(/[\u0300-\u036f]/g,'').replace(/[^A-Za-z0-9 .\-]/g,'').toUpperCase();
  const emv=(id,val)=>id+String(val.length).padStart(2,'0')+val;
  function crc16(str){let crc=0xFFFF;for(let c=0;c<str.length;c++){crc^=str.charCodeAt(c)<<8;for(let i=0;i<8;i++)crc=(crc&0x8000)?((crc<<1)^0x1021):(crc<<1);crc&=0xFFFF;}return crc.toString(16).toUpperCase().padStart(4,'0');}
  function payloadPix(chave,nome,cidade,valor){
    chave=normTxt(chave); nome=semAcentos(nome).slice(0,25)||'RECEBEDOR'; cidade=semAcentos(cidade).slice(0,15)||'BRASIL';
    const mai=emv('00','BR.GOV.BCB.PIX')+emv('01',chave);
    let out=emv('00','01')+emv('26',mai)+emv('52','0000')+emv('53','986');
    if(Number(valor)>0) out+=emv('54',Number(valor).toFixed(2));
    out+=emv('58','BR')+emv('59',nome)+emv('60',cidade)+emv('62',emv('05','***'))+'6304';
    return out+crc16(out);
  }
  function total(){try{return typeof totalCarrinhoAtual==='function'?Number(totalCarrinhoAtual()||0):0}catch(_){return 0}}
  async function carregar(force=false){
    const eid=window.empresaAtual?.id||null;
    if(!eid) return estado;
    if(!force && estado.carregado && estado.empresaId===eid) return estado;
    estado.empresaId=eid; estado.carregado=true;
    try{
      if(window.CloudDB && window.empresaAtual?.cloud){
        const {data,error}=await CloudDB.from('configuracoes_empresa').select('pix_ativo,pix_chave,pix_nome_recebedor,pix_cidade').eq('empresa_id',eid).maybeSingle();
        if(error) throw error;
        Object.assign(estado,{ativo:!!data?.pix_ativo,chave:data?.pix_chave||'',nome:data?.pix_nome_recebedor||'',cidade:data?.pix_cidade||''});
      }else{
        const x=JSON.parse(localStorage.getItem('simpla_pix_'+eid)||'{}'); Object.assign(estado,{ativo:!!x.ativo,chave:x.chave||'',nome:x.nome||'',cidade:x.cidade||''});
      }
    }catch(e){console.warn('SimplA PIX: falha ao carregar configuração',e);}
    preencherConfig(); return estado;
  }
  function montarConfig(){
    const raiz=document.getElementById('sec-config-geral'); if(!raiz||document.getElementById('pix-config-v27')) return;
    const wrap=document.createElement('div'); wrap.id='pix-config-v27'; wrap.className='pix-config-v27';
    wrap.innerHTML=`<h3>Pagamento via Pix</h3><div class="section-box-cfg"><h4>QR Code Pix nos atendimentos</h4><p style="margin-bottom:12px;color:#718096;text-transform:none;">Cadastre os dados que serão usados para gerar o QR Code Pix com o valor do atendimento.</p><div class="form-group"><label style="display:flex;gap:8px;align-items:center;text-transform:none;"><input id="cfg-pix-ativo" type="checkbox" style="width:auto;"> Gerar QR Code ao selecionar Pix</label></div><div class="pix-config-grid"><div class="form-group"><label>Chave Pix</label><input id="cfg-pix-chave" type="text" placeholder="CPF, CNPJ, e-mail, telefone ou chave aleatória"></div><div class="form-group"><label>Nome do recebedor</label><input id="cfg-pix-nome" type="text" maxlength="25" placeholder="Nome exibido no Pix"></div><div class="form-group"><label>Cidade</label><input id="cfg-pix-cidade" type="text" maxlength="15" placeholder="RECIFE"></div></div><button type="button" class="btn-salvar" style="margin-top:12px;" onclick="salvarConfiguracaoPixV27()">Salvar dados Pix</button></div>`;
    raiz.appendChild(wrap); preencherConfig();
  }
  function preencherConfig(){
    const a=document.getElementById('cfg-pix-ativo'); if(!a) return;
    a.checked=!!estado.ativo; document.getElementById('cfg-pix-chave').value=estado.chave||''; document.getElementById('cfg-pix-nome').value=estado.nome||''; document.getElementById('cfg-pix-cidade').value=estado.cidade||'';
  }
  window.salvarConfiguracaoPixV27=async function(){
    if(typeof validarAcessoPerfil==='function' && !validarAcessoPerfil('configuracoes','Somente administradores podem alterar os dados Pix.')) return;
    const eid=window.empresaAtual?.id; if(!eid){alert('Empresa não identificada.');return;}
    const cfg={ativo:!!document.getElementById('cfg-pix-ativo')?.checked,chave:normTxt(document.getElementById('cfg-pix-chave')?.value),nome:normTxt(document.getElementById('cfg-pix-nome')?.value),cidade:normTxt(document.getElementById('cfg-pix-cidade')?.value)};
    if(cfg.ativo && (!cfg.chave||!cfg.nome||!cfg.cidade)){alert('Preencha chave Pix, nome do recebedor e cidade.');return;}
    try{
      if(window.CloudDB && window.empresaAtual?.cloud){const {error}=await CloudDB.from('configuracoes_empresa').upsert({empresa_id:eid,pix_ativo:cfg.ativo,pix_chave:cfg.chave||null,pix_nome_recebedor:cfg.nome||null,pix_cidade:cfg.cidade||null,atualizado_em:new Date().toISOString()},{onConflict:'empresa_id'});if(error)throw error;}
      localStorage.setItem('simpla_pix_'+eid,JSON.stringify(cfg)); Object.assign(estado,cfg,{empresaId:eid,carregado:true}); alert('Dados Pix salvos com sucesso.'); atualizarPixUI(true);
    }catch(e){console.error(e);alert('Não foi possível salvar os dados Pix: '+(e?.message||'erro desconhecido'));}
  };
  function montarBox(){
    const sel=document.getElementById('pag-entrada'); if(!sel||document.getElementById('pix-recebimento-box')) return;
    const box=document.createElement('div'); box.id='pix-recebimento-box'; box.className='pix-recebimento-box';
    box.innerHTML=`<h4>Pagamento via Pix</h4><p id="pix-resumo-v27" style="margin-top:4px;color:#4a5568;">O QR Code usará o valor total deste atendimento.</p><div class="pix-qr-wrap"><div id="pix-qr-v27" class="pix-qr-code"></div><div class="pix-copy-area"><label style="display:block;font-weight:600;margin-bottom:6px;">Pix copia e cola</label><textarea id="pix-copia-v27" readonly></textarea><div class="pix-copy-actions"><button type="button" class="pix-btn-primary" onclick="copiarPixV27()">Copiar Pix</button><button type="button" class="pix-btn-secondary" onclick="atualizarPixUI(true)">Atualizar QR Code</button></div><small id="pix-status-v27" class="pix-status"></small></div></div>`;
    const pg=sel.closest('.form-group'); pg?.appendChild(box);
  }
  window.copiarPixV27=async function(){const t=document.getElementById('pix-copia-v27');if(!t||!t.value)return;try{await navigator.clipboard.writeText(t.value);alert('Pix copia e cola copiado.');}catch(_){t.select();document.execCommand('copy');alert('Pix copia e cola copiado.');}};
  window.atualizarPixUI=async function(force=false){
    montarBox(); const box=document.getElementById('pix-recebimento-box'); const sel=document.getElementById('pag-entrada'); if(!box||!sel)return;
    if(sel.value!=='PIX'){box.style.display='none';return;} box.style.display='block';
    await carregar(force); const qr=document.getElementById('pix-qr-v27'); const txt=document.getElementById('pix-copia-v27'); const st=document.getElementById('pix-status-v27'); const res=document.getElementById('pix-resumo-v27'); const valor=total();
    if(!estado.ativo||!estado.chave){qr.innerHTML='';txt.value='';st.textContent='Pix ainda não configurado. Cadastre a chave em Configurações → Financeiro.';return;}
    if(valor<=0){qr.innerHTML='';txt.value='';st.textContent='Adicione um serviço ou produto para gerar o QR Code com o valor do atendimento.';return;}
    try{
      const payload=payloadPix(estado.chave,estado.nome,estado.cidade,valor); ultimoPayload=payload; txt.value=payload; qr.innerHTML='';
      if(typeof QRCode==='undefined'){st.textContent='Não foi possível carregar o gerador de QR Code. O Pix copia e cola está disponível.';return;}
      new QRCode(qr,{text:payload,width:180,height:180,correctLevel:QRCode.CorrectLevel.M});
      res.textContent='Valor do Pix: '+valor.toLocaleString('pt-BR',{style:'currency',currency:'BRL'}); st.textContent='Confirme manualmente o recebimento antes de finalizar o atendimento.';
    }catch(e){console.error(e);st.textContent='Não foi possível gerar o QR Code: '+(e?.message||'erro desconhecido');}
  };
  function boot(){montarConfig();montarBox();carregar(false).then(()=>atualizarPixUI(false));}
  document.addEventListener('DOMContentLoaded',boot);
  setInterval(()=>{if(document.getElementById('atendimento')?.classList.contains('active')) atualizarPixUI(false);},1200);
})();
</script>
'''
s=s.replace('</body>', block+'\n</body>', 1)
p.write_text(s,encoding='utf-8')

sw=Path('service-worker.js')
t=sw.read_text(encoding='utf-8')
t,n=re.subn(r"const CACHE_VERSION = '[^']+';", "const CACHE_VERSION = 'simpla-shell-v27-pix-qrcode';", t, count=1)
assert n==1, 'CACHE_VERSION nao encontrado'
sw.write_text(t,encoding='utf-8')
