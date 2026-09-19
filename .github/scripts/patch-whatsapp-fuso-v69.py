from pathlib import Path
import re

idx=Path('index.html')
sw=Path('service-worker.js')
html=idx.read_text(encoding='utf-8')

if 'simpla-whatsapp-fuso-v69' in html:
    raise SystemExit('v69 ja aplicada')

marker='</body>'
if marker not in html:
    raise SystemExit('body nao encontrado')

block=r'''
<style id="simpla-whatsapp-fuso-v69-css">
  .simpla-wa-fuso-v69{margin-top:16px;border:1px solid #dbe4ee;border-radius:12px;background:#fff;padding:16px;box-shadow:0 2px 5px rgba(15,23,42,.04);text-transform:none}
  .simpla-wa-fuso-v69 h3{margin:0;font-size:16px;color:#1a1c23;text-transform:none}
  .simpla-wa-fuso-v69 p{margin:4px 0 0;font-size:10px;color:#718096;line-height:1.5;text-transform:none}
  .simpla-wa-fuso-v69-row{display:grid;grid-template-columns:minmax(0,1fr) auto;gap:10px;align-items:end;margin-top:12px}
  .simpla-wa-fuso-v69-field label{display:block;font-size:8px;font-weight:900;color:#718096;margin-bottom:4px;text-transform:uppercase}
  .simpla-wa-fuso-v69-field select{width:100%;padding:9px;border:1px solid #cbd5e0;border-radius:6px;background:#fff;font-size:11px;text-transform:none}
  .simpla-wa-fuso-v69-save{border:0;border-radius:7px;padding:10px 13px;background:#1a1c23;color:#fff;font-size:9px;font-weight:900;cursor:pointer}
  .simpla-wa-fuso-v69-msg{margin-top:9px;font-size:10px;color:#718096;text-transform:none}
  .simpla-wa-fuso-v69-warn{margin-top:10px;padding:10px;border-radius:8px;background:#fffaf0;border:1px solid #f6e05e;color:#744210;font-size:10px;line-height:1.5;text-transform:none}
  @media(max-width:760px){.simpla-wa-fuso-v69-row{grid-template-columns:1fr}}
</style>

<script id="simpla-whatsapp-fuso-v69">
(function(){
  const FUSOS=[
    ['America/Recife','Recife / Brasília (Nordeste)'],
    ['America/Sao_Paulo','São Paulo / Brasília (Sudeste/Sul)'],
    ['America/Fortaleza','Fortaleza'],
    ['America/Bahia','Salvador / Bahia'],
    ['America/Manaus','Manaus / Amazonas'],
    ['America/Belem','Belém / Pará'],
    ['America/Cuiaba','Cuiabá / Mato Grosso'],
    ['America/Campo_Grande','Campo Grande / Mato Grosso do Sul'],
    ['America/Rio_Branco','Rio Branco / Acre'],
    ['America/Noronha','Fernando de Noronha']
  ];

  function garantir(){
    let box=document.getElementById('simpla-wa-fuso-v69'); if(box)return box;
    const area=document.getElementById('simpla-wa-categoria-v65-content'); if(!area)return null;

    box=document.createElement('section');
    box.id='simpla-wa-fuso-v69';
    box.className='simpla-wa-fuso-v69';
    box.innerHTML='<h3>Fuso horário da empresa</h3><p>Usado para calcular corretamente lembretes e demais automações. O navegador pode sugerir um valor, mas o fuso oficial é salvo pelo ADMIN.</p><div class="simpla-wa-fuso-v69-row"><div class="simpla-wa-fuso-v69-field"><label>Fuso horário</label><select id="wa-fuso-v69"></select></div><button type="button" class="simpla-wa-fuso-v69-save" onclick="salvarFusoWhatsAppV69()">Salvar fuso</button></div><div id="wa-fuso-v69-msg" class="simpla-wa-fuso-v69-msg"></div><div id="wa-fuso-v69-warn" class="simpla-wa-fuso-v69-warn">Enquanto o fuso não estiver configurado, o SimplA não programará mensagens automáticas.</div>';

    const rules=document.getElementById('simpla-wa-rules-v68');
    if(rules&&rules.parentElement===area) area.insertBefore(box,rules); else area.prepend(box);
    preencherOpcoes();
    return box;
  }

  function preencherOpcoes(){
    const sel=document.getElementById('wa-fuso-v69');if(!sel)return;
    const detectado=Intl.DateTimeFormat().resolvedOptions().timeZone||'';
    const conhecidos=new Set(FUSOS.map(x=>x[0]));
    const itens=[...FUSOS];
    if(detectado&&!conhecidos.has(detectado)) itens.unshift([detectado,'Detectado pelo navegador']);
    sel.innerHTML='<option value="">Selecione o fuso da empresa</option>'+itens.map(([v,n])=>'<option value="'+v+'">'+n+' · '+v+'</option>').join('');
    if(detectado) sel.dataset.detectado=detectado;
  }

  async function ehAdmin(){
    if(typeof CloudDB==='undefined'||!CloudDB||typeof empresaAtual==='undefined'||!empresaAtual?.id)return false;
    const {data:perfil}=await CloudDB.rpc('perfil_na_empresa',{p_empresa_id:empresaAtual.id});
    return String(perfil||'').toUpperCase()==='ADMIN';
  }

  async function carregar(){
    const box=garantir(); if(!box||!await ehAdmin())return;
    const msg=document.getElementById('wa-fuso-v69-msg');
    try{
      const {data,error}=await CloudDB.from('empresas').select('fuso_horario').eq('id',empresaAtual.id).maybeSingle();
      if(error)throw error;
      const sel=document.getElementById('wa-fuso-v69');
      if(data?.fuso_horario){
        if(![...sel.options].some(o=>o.value===data.fuso_horario)){
          const opt=document.createElement('option');opt.value=data.fuso_horario;opt.textContent=data.fuso_horario;sel.appendChild(opt);
        }
        sel.value=data.fuso_horario;
        msg.textContent='Fuso configurado: '+data.fuso_horario;
        document.getElementById('wa-fuso-v69-warn').style.display='none';
      }else{
        const det=sel.dataset.detectado||'';
        if(det&&[...sel.options].some(o=>o.value===det)) sel.value=det;
        msg.textContent=det?'Sugestão do navegador: '+det+'. Salve para ativar a programação automática.':'Selecione e salve o fuso horário.';
        document.getElementById('wa-fuso-v69-warn').style.display='block';
      }
    }catch(err){
      console.error('Fuso WhatsApp v69:',err);
      msg.textContent='Não foi possível carregar o fuso horário agora.';
    }
  }

  window.carregarFusoWhatsAppV69=carregar;

  window.salvarFusoWhatsAppV69=async function(){
    const msg=document.getElementById('wa-fuso-v69-msg');
    try{
      if(!await ehAdmin())return;
      const fuso=document.getElementById('wa-fuso-v69')?.value||'';
      if(!fuso){alert('Selecione o fuso horário da empresa.');return}
      msg.textContent='Salvando...';
      const {error}=await CloudDB.rpc('salvar_fuso_horario_empresa',{p_empresa_id:empresaAtual.id,p_fuso_horario:fuso});
      if(error)throw error;
      msg.textContent='Fuso salvo com sucesso.';
      await carregar();
    }catch(err){
      console.error('Salvar fuso v69:',err);
      msg.textContent='Não foi possível salvar o fuso.';
      alert(err?.message||'Erro ao salvar fuso horário.');
    }
  };

  function instalar(){garantir();setTimeout(carregar,700)}
  if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',()=>setTimeout(instalar,5400));else setTimeout(instalar,5400);
  document.addEventListener('click',e=>{
    const b=e.target.closest?.('.cfg-v2-nav button');
    if(b&&b.dataset.cat==='WhatsApp e Automações')setTimeout(carregar,130);
  },true);
  setTimeout(instalar,7600);
})();
</script>
'''

html=html.replace(marker,block+'\n'+marker,1)
idx.write_text(html,encoding='utf-8')

swtxt=sw.read_text(encoding='utf-8')
swtxt,n=re.subn(r"const CACHE_VERSION = '[^']+';","const CACHE_VERSION = 'simpla-shell-v69-whatsapp-fuso';",swtxt,count=1)
if n!=1: raise SystemExit('cache version nao encontrada')
sw.write_text(swtxt,encoding='utf-8')
