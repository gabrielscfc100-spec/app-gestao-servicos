from pathlib import Path
import re
p=Path('index.html')
s=p.read_text(encoding='utf-8')
if 'simpla-pix-empresa-v31' in s:
    raise SystemExit('v31 ja aplicada')

old1="""    const eid=window.empresaAtual?.id||null;
    if(!eid) return estado;"""
new1="""    const emp=(typeof empresaAtual!=='undefined' && empresaAtual) ? empresaAtual : window.empresaAtual;
    const eid=emp?.id||null;
    if(!eid) return estado;"""
assert old1 in s, 'empresa no carregar pix nao encontrada'
s=s.replace(old1,new1,1)

old2="""      if(window.CloudDB && window.empresaAtual?.cloud){
        const {data,error}=await CloudDB.from('configuracoes_empresa').select('pix_ativo,pix_chave,pix_nome_recebedor,pix_cidade').eq('empresa_id',eid).maybeSingle();"""
new2="""      if(typeof CloudDB!=='undefined' && emp?.cloud){
        const {data,error}=await CloudDB.from('configuracoes_empresa').select('pix_ativo,pix_chave,pix_nome_recebedor,pix_cidade').eq('empresa_id',eid).maybeSingle();"""
assert old2 in s, 'cloud carregar pix nao encontrado'
s=s.replace(old2,new2,1)

old3="""    const eid=window.empresaAtual?.id; if(!eid){alert('Empresa não identificada.');return;}"""
new3="""    const emp=(typeof empresaAtual!=='undefined' && empresaAtual) ? empresaAtual : window.empresaAtual;
    const eid=emp?.id; if(!eid){alert('Empresa não identificada.');return;}"""
assert old3 in s, 'empresa salvar pix nao encontrada'
s=s.replace(old3,new3,1)

old4="""      if(window.CloudDB && window.empresaAtual?.cloud){const {error}=await CloudDB.from('configuracoes_empresa').upsert({empresa_id:eid,pix_ativo:cfg.ativo,pix_chave:cfg.chave||null,pix_nome_recebedor:cfg.nome||null,pix_cidade:cfg.cidade||null,atualizado_em:new Date().toISOString()},{onConflict:'empresa_id'});if(error)throw error;}"""
new4="""      if(typeof CloudDB!=='undefined' && emp?.cloud){const {error}=await CloudDB.from('configuracoes_empresa').upsert({empresa_id:eid,pix_ativo:cfg.ativo,pix_chave:cfg.chave||null,pix_nome_recebedor:cfg.nome||null,pix_cidade:cfg.cidade||null,atualizado_em:new Date().toISOString()},{onConflict:'empresa_id'});if(error)throw error;}"""
assert old4 in s, 'cloud salvar pix nao encontrado'
s=s.replace(old4,new4,1)

s=s.replace('</body>', '<script id="simpla-pix-empresa-v31">/* Corrige a resolucao da empresa ativa no modulo Pix. */</script>\n</body>',1)
p.write_text(s,encoding='utf-8')

sw=Path('service-worker.js')
t=sw.read_text(encoding='utf-8')
t,n=re.subn(r"const CACHE_VERSION = '[^']+';", "const CACHE_VERSION = 'simpla-shell-v31-pix-empresa';", t, count=1)
assert n==1
sw.write_text(t,encoding='utf-8')
