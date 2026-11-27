#!/usr/bin/env python3
"""Ensaio do empacotador offline e do motor v2 — Python puro, sem rede, sem navegador.
Corre com: python3 -I tests/test_build_pacote_offline.py   (o ensaio no Chrome está no relatório do pacote)"""
import hashlib
import importlib.util
import io
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
SCRIPT = REPO / "scripts" / "build_pacote_offline.py"
ZIP = "KONFIRMU_EXECUTAVEL_OFFLINE_2030.zip"
TOPO = "KONFIRMU_OFFLINE_2030/"
resultados = []


def prova(nome, ok, det=""):
    resultados.append(ok)
    print(("PASSA " if ok else "FALHA ") + nome + (f" — {det}" if det else ""))


def correr(*args):
    return subprocess.run([sys.executable, "-I", str(SCRIPT), *args], capture_output=True, text=True)


spec = importlib.util.spec_from_file_location("empacotador", SCRIPT)
E = importlib.util.module_from_spec(spec)
spec.loader.exec_module(E)

with tempfile.TemporaryDirectory() as t:
    r1, r2 = correr("--saida", f"{t}/a"), correr("--saida", f"{t}/b")
    prova("o pacote constrói-se", r1.returncode == 0 and r2.returncode == 0, r1.stderr.strip()[:200])
    z1, z2 = Path(t, "a", ZIP).read_bytes(), Path(t, "b", ZIP).read_bytes()
    prova("duas construções dão o mesmo ZIP, byte a byte", z1 == z2, hashlib.sha256(z1).hexdigest()[:16])
    prova("--verificar confere o ZIP", correr("--verificar", str(Path(t, "a", ZIP))).returncode == 0)
    z = zipfile.ZipFile(io.BytesIO(z1))
    nomes = {i.filename[len(TOPO):]: i for i in z.infolist() if not i.is_dir()}
    paginas = [n for n in nomes if n.endswith(".html")]
    prova("todas as páginas trazem a regra que bloqueia a rede (CSP)", all(b"Content-Security-Policy" in z.read(TOPO + n) for n in paginas), f"{len(paginas)} páginas")
    prova("nenhum ficheiro fala com a CDN nem com huggingface", not any(b"cdn.jsdelivr" in z.read(TOPO + n) or b"huggingface.co" in z.read(TOPO + n) for n in nomes))
    exe = ["ABRIR_KONFIRMU_OFFLINE.command", "abrir_konfirmu_offline.sh", "servidor_local.py"]
    prova("os lançadores vão executáveis no ZIP (duplo clique no Mac)", all((nomes[n].external_attr >> 16) & 0o111 for n in exe))
    menu = z.read(TOPO + "app_unica.html").decode()
    links = [l for l in E.referencias("app_unica.html", menu)[0] if l.endswith(".html")]
    prova("todas as atividades do menu estão no pacote", all(l in nomes for l in links), f"{len(links)} ligações")
    sw = z.read(TOPO + "sw.js").decode()
    prova("o service worker guarda todas as páginas", all(f'"./{p}"' in sw for p in paginas))
    for p in ("verificador_offline.html", "chronolex_verify.html", "chronolex_photo_seal.html", "estudio_video_criancas.html"):
        txt = z.read(TOPO + p).decode()
        if "fromCharCode.apply" in txt or "konfirmu_sha256.js" not in txt:
            prova(f"{p} usa o hash corrigido (KON-572)", False)
            break
    else:
        prova("as 4 páginas do KON-572 usam o hash corrigido", True)
    prova("chronolex_verify carrega o nacl-util (atas assinadas)", b"nacl-util.min.js" in z.read(TOPO + "chronolex_verify.html"))
    # Sabotagem: 1 byte mudado dentro do ZIP tem de ser apanhado
    mem = io.BytesIO()
    with zipfile.ZipFile(io.BytesIO(z1)) as zi, zipfile.ZipFile(mem, "w", zipfile.ZIP_DEFLATED) as zo:
        for i in zi.infolist():
            d = zi.read(i)
            if i.filename == TOPO + "verificador_offline.html":
                d = d.replace(b"Verificador", b"Verificad0r", 1)
            zo.writestr(i, d)
    prova("1 letra mudada numa página → --verificar recusa", E.verificar_zip(mem.getvalue()) != [])
    _, fora = E.referencias("x.html", "<script>import('https://cdn.exemplo.org/a.js')</script><img src='//x.org/i.png'>")
    prova("o detetor apanha chamadas para fora (import, //)", len(fora) == 2, str(sorted(fora)))
    rtl = E.tratar_rtl("r.html", '<html lang="ar" dir="rtl"><body><p>القيمة 6,02×10²³ و 50 %</p><script>var x=50;</script></body></html>', [])
    prova("páginas RTL: números em <bdi> só no texto, nunca dentro de <script>", rtl.count("<bdi") == 2 and "var x=50;" in rtl)

m = subprocess.run([sys.executable, "-I", str(REPO / "ferramentas" / "konfirmu_nova_geracao_2030.py"), "--auto-teste"], capture_output=True, text=True)
prova("motor Python v2: auto-teste", m.returncode == 0, m.stdout.strip().splitlines()[-1] if m.stdout.strip() else m.stderr[:200])
print(f"\n{sum(resultados)} de {len(resultados)} passam")
sys.exit(0 if all(resultados) else 1)
