#!/usr/bin/env python3
"""Auditoria final do pacote dpsindustrial.nl/konfirmu/ (ordem do David de 27-11-2026, 15:53, regra 5).

Um só script, uma só resposta. Constrói o pacote do sítio duas vezes do zero e confere, ao mesmo tempo:

  1. prova 2×        as duas construções dão os mesmos bytes (SHA256SUMS.txt e o ZIP final iguais)
  2. paleta única    0 cores fora da paleta oficial, 0 verde, 0 violeta, 0 emojis, sem tema claro
                     (scripts/paleta_unica.py verificar: no repositório, no sítio e no executável offline)
  3. a marca         0 «Konfirm u» partido: nos ficheiros e no texto que o navegador mostra
  4. a rede          0 localhost:8790 / 127.0.0.1:8790 nas páginas, scripts e estilos publicados
  5. modo avião      23/23 páginas do executável offline abrem sem rede (tests/test_imersao_offline.py)
  6. memória         cada página publicada abre com menos de 64 MB de memória JavaScript e 0 erros

A pasta _anterior/ (a versão que estava no ar, guardada num ZIP para nada se perder) não conta para 3 e 4:
não é servida como página.

Uso: python3 -I scripts/auditoria_final_nl.py SAIDA
Escreve em SAIDA: KONFIRMU_FINAL_NL.zip (a pasta konfirmu/, pronta a subir) e AUDITORIA_FINAL_NL.txt.
Sai com 0 só se tudo passar.
"""
import functools
import hashlib
import os
import re
import subprocess
import sys
import tempfile
import threading
import zipfile
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer

AQUI = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(AQUI)
sys.path.insert(0, AQUI)
import build_site_nl  # noqa: E402
import paleta_unica  # noqa: E402

LIMITE_MB = 64
RX_PARTIDA = re.compile(r"Konfirm[\s ​]+u\b", re.I)
RX_PORTA = re.compile(r"(?:localhost|127\.0\.0\.1):8790")
TEXTO = (".html", ".js", ".css", ".json", ".svg", ".txt", ".webmanifest")


def sha(b):
    return hashlib.sha256(b).hexdigest()


def construir(pasta):
    subprocess.run([sys.executable, "-I", os.path.join(AQUI, "build_site_nl.py"), pasta], check=True,
                   stdout=subprocess.DEVNULL, cwd=REPO)
    raiz = os.path.join(pasta, "konfirmu")
    entradas = {}
    for d, _, fs in os.walk(raiz):
        for f in fs:
            p = os.path.join(d, f)
            entradas["konfirmu/" + os.path.relpath(p, raiz).replace(os.sep, "/")] = open(p, "rb").read()
    return raiz, build_site_nl.zip_deterministico(entradas)


def publicados(raiz):
    for d, _, fs in os.walk(raiz):
        for f in sorted(fs):
            p = os.path.join(d, f)
            rel = os.path.relpath(p, raiz).replace(os.sep, "/")
            if not rel.startswith("_anterior/"):
                yield rel, p


def varrer(raiz):
    """«Konfirm u» e a porta 8790 nos ficheiros de texto publicados e dentro do executável offline."""
    partidas, portas = [], []
    for rel, p in publicados(raiz):
        if rel.endswith(".zip"):
            with zipfile.ZipFile(p) as z:
                for n in z.namelist():
                    if n.endswith(TEXTO):
                        t = z.read(n).decode("utf-8", "replace")
                        partidas += ["%s!%s" % (rel, n)] if RX_PARTIDA.search(t) else []
                        portas += ["%s!%s" % (rel, n)] if RX_PORTA.search(t) else []
        elif rel.endswith(TEXTO):
            t = open(p, encoding="utf-8", errors="replace").read()
            partidas += [rel] if RX_PARTIDA.search(t) else []
            portas += [rel] if RX_PORTA.search(t) else []
    return partidas, portas


class Calado(SimpleHTTPRequestHandler):
    def log_message(self, *a):
        pass

    def send_head(self):
        # como a Cloudflare Pages: /konfirmu/manifesto serve manifesto.html
        caminho = self.translate_path(self.path)
        if not os.path.exists(caminho) and os.path.exists(caminho + ".html"):
            self.path = self.path.split("?")[0] + ".html"
        return super().send_head()


def navegador(pasta_site, raiz):
    """Abre cada página publicada: memória JavaScript, erros e o texto que se vê (a marca inteira)."""
    from playwright.sync_api import sync_playwright
    srv = ThreadingHTTPServer(("127.0.0.1", 0), functools.partial(Calado, directory=pasta_site))
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    base = "http://127.0.0.1:%d/konfirmu/" % srv.server_port
    paginas = [rel for rel, _ in publicados(raiz) if rel.endswith(".html")]
    medidas, erros, partidas = {}, {}, []
    with sync_playwright() as pw:
        b = pw.chromium.launch()
        for rel in paginas:
            ctx = b.new_context(viewport={"width": 390, "height": 844}, service_workers="block")
            page = ctx.new_page()
            errs = []
            page.on("pageerror", lambda e, errs=errs: errs.append(str(e)[:120]))
            page.goto(base + rel, wait_until="load")
            page.wait_for_timeout(700)
            cdp = ctx.new_cdp_session(page)
            cdp.send("Performance.enable")
            m = {x["name"]: x["value"] for x in cdp.send("Performance.getMetrics")["metrics"]}
            medidas[rel] = m.get("JSHeapUsedSize", 0) / 1048576
            if errs:
                erros[rel] = errs
            if RX_PARTIDA.search(page.evaluate("document.body ? document.body.innerText : ''")):
                partidas.append(rel)
            ctx.close()
        b.close()
    srv.shutdown()
    return medidas, erros, partidas


def main(argv):
    if len(argv) != 2:
        print(__doc__)
        return 2
    saida = os.path.abspath(argv[1])
    os.makedirs(saida, exist_ok=True)
    linhas, falhou = [], False

    def prova(nome, ok, detalhe=""):
        nonlocal falhou
        falhou |= not ok
        linhas.append("%s %s%s" % ("PASSA" if ok else "FALHA", nome, (" — " + detalhe) if detalhe else ""))
        print(linhas[-1], flush=True)

    with tempfile.TemporaryDirectory() as tmp:
        a, b = os.path.join(tmp, "a"), os.path.join(tmp, "b")
        raiz, zip_a = construir(a)
        raiz_b, zip_b = construir(b)
        somas_a = open(os.path.join(raiz, "SHA256SUMS.txt"), "rb").read()
        somas_b = open(os.path.join(raiz_b, "SHA256SUMS.txt"), "rb").read()
        prova("1. prova 2×: duas construções do zero, os mesmos bytes", somas_a == somas_b and zip_a == zip_b,
              "ZIP %s" % sha(zip_a))
        n_fich = sum(1 for _ in publicados(raiz))

        alvos = [("repositório", REPO), ("sítio konfirmu/", raiz),
                 ("executável offline", os.path.join(raiz, "app", "konfirmu-offline-2030.zip"))]
        resumo = []
        total_falhas = 0
        for nome, alvo in alvos:
            ficheiros, falhas = paleta_unica.verificar(alvo)
            total_falhas += len(falhas) + (0 if ficheiros else 1)  # pasta vazia também é falha
            resumo.append("%s %d ficheiros, %d falhas" % (nome, len(ficheiros), len(falhas)))
            if falhas:
                resumo[-1] += " (" + "; ".join(falhas[:3]) + ")"
        prova("2. paleta única: 0 fora da paleta, 0 verde, 0 violeta, 0 emojis, sem tema claro",
              total_falhas == 0, " · ".join(resumo))

        partidas, portas = varrer(raiz)
        medidas, erros, partidas_vistas = navegador(a, raiz)
        prova("3. a marca: 0 «Konfirm u» partido (ficheiros e texto no ecrã)", not partidas and not partidas_vistas,
              ", ".join(partidas + partidas_vistas) or "%d ficheiros e %d páginas no navegador" % (n_fich, len(medidas)))
        prova("4. a rede: 0 localhost:8790 nas páginas, scripts e estilos publicados", not portas,
              ", ".join(portas) or "%d ficheiros, executável offline incluído" % n_fich)

        zip_off = os.path.join(raiz, "app", "konfirmu-offline-2030.zip")
        r = subprocess.run([sys.executable, os.path.join(REPO, "tests", "test_imersao_offline.py"), zip_off,
                            "--atividades", "21"], capture_output=True, text=True, cwd=REPO)
        m = re.search(r"Modo avião: (\d+)/(\d+)", r.stdout)
        prova("5. modo avião: o executável offline abre sem rede", r.returncode == 0 and m and m.group(1) == m.group(2),
              m.group(0) if m else (r.stdout + r.stderr)[-200:])

        pior = max(medidas, key=medidas.get)
        prova("6. memória: cada página publicada abaixo de %d MB, 0 erros" % LIMITE_MB,
              medidas[pior] < LIMITE_MB and not erros,
              "%d páginas, a mais pesada %s com %.1f MB%s" % (len(medidas), pior, medidas[pior],
                                                              ("; erros: %s" % erros) if erros else ""))

        open(os.path.join(saida, "KONFIRMU_FINAL_NL.zip"), "wb").write(zip_a)
        commit = subprocess.run(["git", "-C", REPO, "rev-parse", "HEAD"], capture_output=True, text=True).stdout.strip()
        sujo = subprocess.run(["git", "-C", REPO, "status", "--porcelain"], capture_output=True, text=True).stdout.strip()
        cab = ["Auditoria final · dpsindustrial.nl/konfirmu/",
               "commit %s%s" % (commit, " (com alterações por gravar)" if sujo else ""),
               "KONFIRMU_FINAL_NL.zip  %s  %d bytes" % (sha(zip_a), len(zip_a)),
               "SHA256SUMS.txt do sítio  %s" % sha(somas_a), ""]
        rel = "\n".join(cab + linhas + ["", "resultado: %s" % ("TUDO PASSA" if not falhou else "HÁ FALHAS")]) + "\n"
        open(os.path.join(saida, "AUDITORIA_FINAL_NL.txt"), "w", encoding="utf-8").write(rel)
        print("resultado: %s · ZIP %s" % ("TUDO PASSA" if not falhou else "HÁ FALHAS", sha(zip_a)))
    return 1 if falhou else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
