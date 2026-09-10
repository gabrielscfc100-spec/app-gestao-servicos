from pathlib import Path
import re

p=Path('index.html')
s=p.read_text(encoding='utf-8')

if 'simpla-pix-empresa-v30' in s:
    raise SystemExit('v30 ja aplicada')

marker='''<script id="simpla-pix-qrcode-v27">'''
idx=s.find(marker)
assert idx!=-1, 'script Pix v27 nao encontrado'
end=s.find('</script>', idx)
assert end!=-1, 'fim do script Pix v27 nao encontrado'
block=s[idx:end]

helper="""
  function obterEmpresaPix(){
    try{ if(typeof empresaAtual!=='undefined' && empresaAtual) return empresaAtual; }catch(_){ }
    return window.empresaAtual || null;
  }
  function obterCloudDBPix(){
    try{ if(typeof CloudDB!=='undefined' && CloudDB) return CloudDB; }catch(_){ }
    return window.CloudDB || null;
  }
"""
block=block.replace("  let ultimoPayload='';\n", "  let ultimoPayload='';\n"+helper,1)
block=block.replace("    const eid=window.empresaAtual?.id||null;", "    const emp=obterEmpresaPix(); const eid=emp?.id||null;",1)
block=block.replace("      if(window.CloudDB && window.empresaAtual?.cloud){", "      const db=obterCloudDBPix();\n      if(db && emp?.cloud){",1)
block=block.replace("        const {data,error}=await CloudDB.from('configuracoes_empresa')", "        const {data,error}=await db.from('configuracoes_empresa')",1)
block=block.replace("    const eid=window.empresaAtual?.id; if(!eid){alert('Empresa não identificada.');return;}", "    const emp=obterEmpresaPix(); const eid=emp?.id; if(!eid){alert('Empresa não identificada.');return;}",1)
block=block.replace("      if(window.CloudDB && window.empresaAtual?.cloud){const {error}=await CloudDB.from('configuracoes_empresa')", "      const db=obterCloudDBPix();\n      if(db && emp?.cloud){const {error}=await db.from('configuracoes_empresa')",1)

s=s[:idx]+block+s[end:]
# marker for v30
s=s.replace('</body>', '<script id="simpla-pix-empresa-v30">/* Corrige acesso à empresa/DB no módulo Pix. */</script>\n</body>',1)
p.write_text(s,encoding='utf-8')

sw=Path('service-worker.js')
t=sw.read_text(encoding='utf-8')
t,n=re.subn(r"const CACHE_VERSION = '[^']+';", "const CACHE_VERSION = 'simpla-shell-v30-pix-empresa';", t, count=1)
assert n==1, 'CACHE_VERSION nao encontrado'
sw.write_text(t,encoding='utf-8')
