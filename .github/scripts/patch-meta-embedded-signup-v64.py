from pathlib import Path
import re

idx=Path('index.html')
sw=Path('service-worker.js')
html=idx.read_text(encoding='utf-8')

if 'simpla-whatsapp-embedded-v64' in html:
    raise SystemExit('v64 ja aplicada')

marker='</body>'
if marker not in html:
    raise SystemExit('body nao encontrado')

block=r'''
<style id="simpla-whatsapp-embedded-v64-css">
  .simpla-wa-connect-v64{margin-top:12px;padding:12px;border:1px solid #e2e8f0;border-radius:9px;background:#f8fafc;text-transform:none}
  .simpla-wa-connect-v64-title{font-size:11px;font-weight:900;color:#2d3748;margin-bottom:4px}
  .simpla-wa-connect-v64-desc{font-size:10px;color:#718096;line-height:1.5;text-transform:none}
  .simpla-wa-connect-v64-actions{display:flex;gap:8px;flex-wrap:wrap;margin-top:10px}
  .simpla-wa-connect-v64-btn{border:0;border-radius:7px;padding:10px 12px;font-size:9px;font-weight:900;cursor:pointer;background:#1877f2;color:#fff}
  .simpla-wa-connect-v64-btn:disabled{cursor:not-allowed;background:#cbd5e0;color:#718096}
  .simpla-wa-connect-v64-status{margin-top:9px;font-size:10px;color:#4a5568;text-transform:none}
</style>
<script id="simpla-whatsapp-embedded-v64">
(function(){
  let cfg=null, sdkPromise=null, signup={code:null,waba_id:null,phone_number_id:null,business_id:null,finalizando:false};

  function garantir(){
    const box=document.getElementById('simpla-wa-v62');if(!box)return null;
    let area=document.getElementById('simpla-wa-connect-v64');if(area)return area;
    area=document.createElement('div');area.id='simpla-wa-connect-v64';area.className='simpla-wa-connect-v64';
    area.innerHTML='<div class="simpla-wa-connect-v64-title">Conexão oficial com a Meta</div><div class="simpla-wa-connect-v64-desc">A empresa conecta o próprio WhatsApp pelo fluxo oficial da Meta. Nenhum token é digitado ou exibido no SimplA.</div><div class="simpla-wa-connect-v64-actions"><button id="simpla-wa-connect-v64-btn" type="button" class="simpla-wa-connect-v64-btn" disabled onclick="iniciarEmbeddedSignupV64()">Verificando disponibilidade...</button></div><div id="simpla-wa-connect-v64-status" class="simpla-wa-connect-v64-status"></div>';
    box.appendChild(area);return area;
  }

  async function podeAdmin(){
    if(typeof CloudDB==='undefined'||!CloudDB||typeof empresaAtual==='undefined'||!empresaAtual?.id)return false;
    const {data:perfil}=await CloudDB.rpc('perfil_na_empresa',{p_empresa_id:empresaAtual.id});
    return String(perfil||'').toUpperCase()==='ADMIN';
  }

  async function carregarConfig(){
    const area=garantir();if(!area||!await podeAdmin()){if(area)area.style.display='none';return}
    area.style.display='block';
    const btn=document.getElementById('simpla-wa-connect-v64-btn');
    const st=document.getElementById('simpla-wa-connect-v64-status');
    try{
      const {data,error}=await CloudDB.functions.invoke('whatsapp-embedded-config',{body:{empresa_id:empresaAtual.id}});
      if(error)throw error;
      cfg=data||null;
      if(cfg?.ready){
        btn.disabled=false;btn.textContent='Conectar WhatsApp com a Meta';
        st.textContent='Fluxo Embedded Signup disponível para esta conta.';
      }else{
        btn.disabled=true;btn.textContent='Configuração Meta pendente';
        st.textContent='O App Meta do SimplA ainda precisa receber App ID, Config ID e versão da Graph API no backend.';
      }
    }catch(err){
      console.error('Embedded config v64:',err);
      btn.disabled=true;btn.textContent='Integração indisponível';
      st.textContent='Não foi possível carregar a configuração de conexão agora.';
    }
  }

  function carregarSDK(appId,version){
    if(window.FB)return Promise.resolve();
    if(sdkPromise)return sdkPromise;
    sdkPromise=new Promise((resolve,reject)=>{
      const timeout=setTimeout(()=>reject(new Error('Timeout ao carregar SDK da Meta')),12000);
      window.fbAsyncInit=function(){
        try{
          FB.init({appId:String(appId),cookie:true,xfbml:false,version:String(version||'v25.0')});
          clearTimeout(timeout);resolve();
        }catch(e){clearTimeout(timeout);reject(e)}
      };
      const js=document.createElement('script');js.id='facebook-jssdk';js.async=true;js.defer=true;js.crossOrigin='anonymous';
      js.src='https://connect.facebook.net/pt_BR/sdk.js';
      js.onerror=()=>{clearTimeout(timeout);reject(new Error('Falha ao carregar SDK da Meta'))};
      document.head.appendChild(js);
    });
    return sdkPromise;
  }

  async function tentarFinalizar(){
    if(signup.finalizando||!signup.code||!signup.waba_id||!signup.phone_number_id)return;
    signup.finalizando=true;
    const st=document.getElementById('simpla-wa-connect-v64-status');
    try{
      st.textContent='Finalizando conexão segura com a Meta...';
      const {data,error}=await CloudDB.functions.invoke('whatsapp-embedded-finalizar',{body:{
        empresa_id:empresaAtual.id,
        code:signup.code,
        waba_id:signup.waba_id,
        phone_number_id:signup.phone_number_id,
        business_id:signup.business_id||null
      }});
      if(error)throw error;
      if(!data?.ok)throw new Error(data?.detail||data?.error||'Falha ao concluir conexão.');
      st.textContent='WhatsApp conectado com sucesso.';
      if(typeof carregarWhatsAppConfigV62==='function')await carregarWhatsAppConfigV62();
      if(typeof carregarTemplatesWhatsAppV63==='function')await carregarTemplatesWhatsAppV63();
    }catch(err){
      console.error('Embedded finalizar v64:',err);
      st.textContent='Não foi possível concluir a conexão. Revise a configuração do App Meta e tente novamente.';
    }finally{
      signup={code:null,waba_id:null,phone_number_id:null,business_id:null,finalizando:false};
    }
  }

  window.addEventListener('message',function(event){
    if(!/facebook\.com$/i.test(new URL(event.origin||'https://invalid.local').hostname))return;
    let data=event.data;
    try{if(typeof data==='string')data=JSON.parse(data)}catch(_){return}
    if(!data||data.type!=='WA_EMBEDDED_SIGNUP')return;
    if(data.event==='FINISH'||data.event==='FINISH_WHATSAPP_BUSINESS_APP_ONBOARDING'){
      signup.waba_id=String(data.data?.waba_id||data.data?.wabaId||'')||signup.waba_id;
      signup.phone_number_id=String(data.data?.phone_number_id||data.data?.phoneNumberId||'')||signup.phone_number_id;
      signup.business_id=String(data.data?.business_id||data.data?.businessId||'')||signup.business_id;
      tentarFinalizar();
    }
  });

  window.iniciarEmbeddedSignupV64=async function(){
    const st=document.getElementById('simpla-wa-connect-v64-status');
    try{
      if(!cfg?.ready){await carregarConfig();if(!cfg?.ready)return}
      signup={code:null,waba_id:null,phone_number_id:null,business_id:null,finalizando:false};
      st.textContent='Abrindo conexão segura da Meta...';
      await carregarSDK(cfg.app_id,cfg.graph_version);
      FB.login(function(response){
        if(response?.authResponse?.code){
          signup.code=response.authResponse.code;
          st.textContent='Autorização recebida. Concluindo vínculo do número...';
          tentarFinalizar();
        }else{
          st.textContent='Conexão cancelada ou autorização não concluída.';
        }
      },{
        config_id:String(cfg.config_id),
        response_type:'code',
        override_default_response_type:true,
        extras:{setup:{}}
      });
    }catch(err){
      console.error('Embedded Signup v64:',err);
      st.textContent='Não foi possível iniciar a conexão com a Meta.';
    }
  };

  window.carregarEmbeddedSignupV64=carregarConfig;
  function instalar(){garantir();setTimeout(carregarConfig,1400)}
  if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',()=>setTimeout(instalar,3600));else setTimeout(instalar,3600);
})();
</script>
'''

html=html.replace(marker,block+'\n'+marker,1)
idx.write_text(html,encoding='utf-8')

swtxt=sw.read_text(encoding='utf-8')
swtxt,n=re.subn(r"const CACHE_VERSION = '[^']+';","const CACHE_VERSION = 'simpla-shell-v64-meta-embedded-signup';",swtxt,count=1)
if n!=1: raise SystemExit('cache version nao encontrada')
sw.write_text(swtxt,encoding='utf-8')
