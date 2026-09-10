from pathlib import Path
import re

p=Path('index.html')
s=p.read_text(encoding='utf-8')

old=r'''  function montarConfig(){
    const raiz=document.getElementById('sec-config-geral'); if(!raiz||document.getElementById('pix-config-v27')) return;
    const wrap=document.createElement('div'); wrap.id='pix-config-v27'; wrap.className='pix-config-v27';
    wrap.innerHTML=`<h3>Pagamento via Pix</h3><div class="section-box-cfg"><h4>QR Code Pix nos atendimentos</h4><p style="margin-bottom:12px;color:#718096;text-transform:none;">Cadastre os dados que serão usados para gerar o QR Code Pix com o valor do atendimento.</p><div class="form-group"><label style="display:flex;gap:8px;align-items:center;text-transform:none;"><input id="cfg-pix-ativo" type="checkbox" style="width:auto;"> Gerar QR Code ao selecionar Pix</label></div><div class="pix-config-grid"><div class="form-group"><label>Chave Pix</label><input id="cfg-pix-chave" type="text" placeholder="CPF, CNPJ, e-mail, telefone ou chave aleatória"></div><div class="form-group"><label>Nome do recebedor</label><input id="cfg-pix-nome" type="text" maxlength="25" placeholder="Nome exibido no Pix"></div><div class="form-group"><label>Cidade</label><input id="cfg-pix-cidade" type="text" maxlength="15" placeholder="RECIFE"></div></div><button type="button" class="btn-salvar" style="margin-top:12px;" onclick="salvarConfiguracaoPixV27()">Salvar dados Pix</button></div>`;
    raiz.appendChild(wrap); preencherConfig();
  }'''

new=r'''  function montarConfig(){
    const raiz=document.getElementById('sec-config-geral'); if(!raiz) return;
    let wrap=document.getElementById('pix-config-v27');
    if(!wrap){
      wrap=document.createElement('div'); wrap.id='pix-config-v27'; wrap.className='pix-config-v27 cfg-v2-section';
      wrap.innerHTML=`<h3>Pagamento via Pix</h3><div class="section-box-cfg"><h4>QR Code Pix nos atendimentos</h4><p style="margin-bottom:12px;color:#718096;text-transform:none;">Cadastre os dados que serão usados para gerar o QR Code Pix com o valor do atendimento.</p><div class="form-group"><label style="display:flex;gap:8px;align-items:center;text-transform:none;"><input id="cfg-pix-ativo" type="checkbox" style="width:auto;"> Gerar QR Code ao selecionar Pix</label></div><div class="pix-config-grid"><div class="form-group"><label>Chave Pix</label><input id="cfg-pix-chave" type="text" placeholder="CPF, CNPJ, e-mail, telefone ou chave aleatória"></div><div class="form-group"><label>Nome do recebedor</label><input id="cfg-pix-nome" type="text" maxlength="25" placeholder="Nome exibido no Pix"></div><div class="form-group"><label>Cidade</label><input id="cfg-pix-cidade" type="text" maxlength="15" placeholder="RECIFE"></div></div><button type="button" class="btn-salvar" style="margin-top:12px;" onclick="salvarConfiguracaoPixV27()">Salvar dados Pix</button></div>`;
    }

    const content=raiz.querySelector('.cfg-v2-content');
    const nav=raiz.querySelector('.cfg-v2-nav');
    if(content && nav){
      let grupo=content.querySelector('.cfg-v2-group[data-cat="Financeiro"]');
      if(!grupo){
        grupo=document.createElement('section');
        grupo.className='cfg-v2-group';
        grupo.dataset.cat='Financeiro';
        grupo.innerHTML='<h2>Financeiro</h2><p class="cfg-v2-desc">Recursos e comportamentos relacionados à gestão financeira.</p>';
        content.appendChild(grupo);
      }
      if(!nav.querySelector('button[data-cat="Financeiro"]')){
        const b=document.createElement('button');
        b.type='button'; b.dataset.cat='Financeiro'; b.innerHTML='<span>Financeiro</span><span>›</span>';
        b.onclick=()=>{
          nav.querySelectorAll('button').forEach(x=>x.classList.toggle('ativo',x===b));
          content.querySelectorAll('.cfg-v2-group').forEach(g=>g.classList.toggle('ativo',g===grupo));
        };
        nav.appendChild(b);
      }
      if(wrap.parentNode!==grupo) grupo.appendChild(wrap);
    }else if(!wrap.parentNode){
      raiz.appendChild(wrap);
    }
    preencherConfig();
  }'''

if old not in s:
    raise SystemExit('funcao montarConfig v27 nao encontrada')
s=s.replace(old,new,1)

# Ensure repeated boot after layout V2 is ready
needle="  document.addEventListener('DOMContentLoaded',boot);"
repl="  document.addEventListener('DOMContentLoaded',()=>{boot();setTimeout(montarConfig,150);setTimeout(montarConfig,800);});"
if needle in s:
    s=s.replace(needle,repl,1)

p.write_text(s,encoding='utf-8')

sw=Path('service-worker.js')
t=sw.read_text(encoding='utf-8')
t,n=re.subn(r"const CACHE_VERSION = '[^']+';", "const CACHE_VERSION = 'simpla-shell-v28-pix-config-financeiro';", t, count=1)
if n!=1: raise SystemExit('CACHE_VERSION nao encontrado')
sw.write_text(t,encoding='utf-8')
