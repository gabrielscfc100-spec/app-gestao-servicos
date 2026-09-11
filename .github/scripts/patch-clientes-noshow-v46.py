from pathlib import Path

idx=Path('index.html')
sw=Path('service-worker.js')
html=idx.read_text(encoding='utf-8')

marker="<div id=\"hist-cli-kpis\" class=\"hist-cli-kpis\">"
if marker not in html:
    raise SystemExit('kpis historico nao encontrado')

html=html.replace(marker, "<div id=\"hist-cli-noshow-alerta\" style=\"display:none;margin:0 0 14px;padding:12px;border-radius:7px;border:1px solid #feb2b2;background:#fff5f5;color:#9b2c2c;font-size:12px;font-weight:700;text-transform:none;\"></div>"+marker,1)

old="""            const elOrigem = document.getElementById('hist-cli-origem');

            if(elQtd) elQtd.innerText = String(qtdAtendimentos);"""
new="""            const elOrigem = document.getElementById('hist-cli-origem');

            const agendaCliente = agendamentos.filter(a => String(a.clienteId || '') === String(c.id));
            const totalAgendaCliente = agendaCliente.length;
            const totalNoShowCliente = agendaCliente.filter(a => String(a.status || '').toUpperCase() === 'NAO_COMPARECEU').length;
            const taxaNoShowCliente = totalAgendaCliente ? (totalNoShowCliente / totalAgendaCliente) * 100 : 0;
            const alertaNoShow = document.getElementById('hist-cli-noshow-alerta');
            if(alertaNoShow) {
                if(totalNoShowCliente >= 2) {
                    alertaNoShow.style.display='block';
                    alertaNoShow.innerHTML = `⚠️ <b>Reincidência de não comparecimento:</b> ${totalNoShowCliente} falta(s) em ${totalAgendaCliente} agendamento(s) (${taxaNoShowCliente.toFixed(1)}%). Considere reforçar a confirmação antes de novos horários.`;
                } else if(totalNoShowCliente === 1) {
                    alertaNoShow.style.display='block';
                    alertaNoShow.innerHTML = `Atenção: este cliente possui 1 não comparecimento em ${totalAgendaCliente} agendamento(s) (${taxaNoShowCliente.toFixed(1)}%).`;
                } else {
                    alertaNoShow.style.display='none';
                    alertaNoShow.innerHTML='';
                }
            }

            if(elQtd) elQtd.innerText = String(qtdAtendimentos);"""
if old not in html:
    raise SystemExit('ponto historico nao encontrado')
html=html.replace(old,new,1)

# enriquecer jornada v45 com taxa de no-show se existir bloco de resumo
needle="<span>Não compareceu</span>"
if needle in html and "Taxa de no-show" not in html:
    html=html.replace(needle, needle,1)

idx.write_text(html,encoding='utf-8')

swtxt=sw.read_text(encoding='utf-8')
import re
swtxt=re.sub(r"const CACHE_VERSION = 'simpla-shell-v\d+[^']*';", "const CACHE_VERSION = 'simpla-shell-v46-clientes-noshow';", swtxt, count=1)
sw.write_text(swtxt,encoding='utf-8')
