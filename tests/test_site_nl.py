#!/usr/bin/env python3
"""Ensaio do pacote para dpsindustrial.nl/konfirmu/ num Chrome de verdade (Playwright).

Serve a pasta em /konfirmu/ como a Cloudflare Pages a serve (tira o «.html»: 308 de x.html para x, e 307 de
index.html para a pasta) e confere:
  A. varredura estática: 0 emojis, 0 verde/violeta/amarelo/vermelho, 0 fundos brancos, 0 cargas de fora, 0 localhost:8790;
  B. cada página abre sem erros, sem um único pedido para fora, com a memória JavaScript abaixo de 64 MB;
  C. modo avião: depois da primeira visita, com a rede cortada, todas as páginas da app abrem (com e sem «.html»);
  D. Modo Criança: só as tigelas; páginas de adultos ficam fechadas; sair pede o PIN (errado não abre, certo abre);
     ligações para fora ficam travadas;
  E. terminal: selftest 4/4, bigint-test 10/10, sha256 de «abc», e a caixa de trabalho não tem rede;
  F. capturas de ecrã de telemóvel (390 × 844) em CAPTURAS/.
Uso: python3 tests/test_site_nl.py PASTA_QUE_TEM_konfirmu [CAPTURAS]
"""
import functools
import json
import os
import re
import subprocess
import sys
import threading
import time
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from playwright.sync_api import sync_playwright

RAIZ = os.path.abspath(sys.argv[1])
CAPTURAS = os.path.abspath(sys.argv[2]) if len(sys.argv) > 2 else None
PASTA = os.path.join(RAIZ, "konfirmu")
AQUI = os.path.dirname(os.path.abspath(__file__))
bons, maus = [], []


def prova(nome, cond, extra=""):
    (bons if cond else maus).append(nome)
    print(("PASSA " if cond else "FALHA ") + nome + (" — %s" % extra if extra != "" else ""))


class ComoCloudflare(SimpleHTTPRequestHandler):
    def log_message(self, *a):
        pass

    def end_headers(self):
        self.send_header("Cache-Control", "public, max-age=0, must-revalidate")
        super().end_headers()

    def do_GET(self):
        caminho = self.path.split("?")[0]
        if caminho.endswith("/index.html"):
            self.send_response(307); self.send_header("Location", caminho[:-10]); self.end_headers(); return
        if caminho.endswith(".html"):
            self.send_response(308); self.send_header("Location", caminho[:-5]); self.end_headers(); return
        disco = os.path.join(RAIZ, caminho.lstrip("/"))
        # como a Cloudflare Pages: o caminho exato; se não houver, o mesmo caminho com «.html»
        if not caminho.endswith("/") and not os.path.isfile(disco) and os.path.isfile(disco + ".html"):
            self.path = caminho + ".html"
        return super().do_GET()


def servidor():
    s = ThreadingHTTPServer(("127.0.0.1", 0), functools.partial(ComoCloudflare, directory=RAIZ))
    threading.Thread(target=s.serve_forever, daemon=True).start()
    return s


def memoria_mb(page):
    cdp = page.context.new_cdp_session(page)
    cdp.send("Performance.enable")
    m = {x["name"]: x["value"] for x in cdp.send("Performance.getMetrics")["metrics"]}
    cdp.detach()
    return m.get("JSHeapUsedSize", 0) / 1048576


def main():
    # A. varredura estática
    r = subprocess.run([sys.executable, "-I", os.path.join(AQUI, "..", "ferramentas", "verificar_pacote.py"), PASTA, "--json", "--estrito"],
                       capture_output=True, text=True)
    tot = json.loads(r.stdout)["total"]
    prova("varredura: 0 emojis", tot["emojis"] == 0, tot["emojis"])
    prova("varredura: 0 verde, 0 violeta, 0 amarelo, 0 vermelho", tot["verde"] + tot["violeta"] + tot["amarelo"] + tot["vermelho"] == 0, tot)
    prova("varredura: 0 fundos brancos e 0 cargas de fora", tot["fundos_brancos"] == 0 and tot["fora"] == 0, tot)
    local = subprocess.run(["grep", "-rIl", "--exclude-dir=_anterior", "localhost:8790", PASTA], capture_output=True, text=True).stdout.strip()
    prova("varredura: 0 «localhost:8790» no pacote", local == "", local)

    srv = servidor()
    base = "http://127.0.0.1:%d" % srv.server_port
    paginas_app = sorted(f for f in os.listdir(os.path.join(PASTA, "app")) if f.endswith(".html"))
    TEL = dict(viewport={"width": 390, "height": 844}, device_scale_factor=2, is_mobile=True, has_touch=True)
    with sync_playwright() as pw:
        b = pw.chromium.launch(executable_path=os.environ.get("CHROME", "/usr/bin/google-chrome"))
        # B. cada página: sem erros, sem pedidos para fora, memória < 64 MB
        ctx = b.new_context(**TEL)
        fora, erros = [], []
        ctx.on("request", lambda q: fora.append(q.url) if not q.url.startswith(base) and not q.url.startswith(("data:", "blob:")) else None)
        pior = (0, "")
        for alvo in ["/konfirmu/", "/konfirmu/manifesto.html", "/konfirmu/app/"] + ["/konfirmu/app/" + p for p in paginas_app]:
            page = ctx.new_page()
            page.on("pageerror", lambda e, a=alvo: erros.append("%s: %s" % (a, e)))
            resp = page.goto(base + alvo, wait_until="load")
            page.wait_for_timeout(350)
            mb = memoria_mb(page)
            if mb > pior[0]:
                pior = (mb, alvo)
            if resp is None or resp.status >= 400:
                erros.append("%s: estado %s" % (alvo, resp.status if resp else "sem resposta"))
            page.close()
        prova("todas as páginas abrem sem erros (%d páginas)" % (len(paginas_app) + 3), not erros, erros[:4])
        prova("nem um pedido para fora do sítio", not fora, fora[:4])
        prova("memória JavaScript abaixo de 64 MB em cada página", pior[0] < 64, "pior %.1f MB (%s)" % pior)
        ctx.close()

        # C. modo avião
        ctx = b.new_context(**TEL)
        page = ctx.new_page()
        page.goto(base + "/konfirmu/app/")
        pronto = page.evaluate("""async()=>{const r=await navigator.serviceWorker.ready;return !!r.active}""")
        page.reload(); page.wait_for_timeout(500)
        guardadas = page.evaluate("""async()=>{const ks=await caches.keys();let n=0;for(const k of ks){const c=await caches.open(k);n+=(await c.keys()).length}return {ks,n}}""")
        controla = page.evaluate("()=>!!navigator.serviceWorker.controller")
        prova("o service worker da app está ativo e manda na página", pronto and controla, guardadas["ks"])
        ctx.set_offline(True)
        falham = []
        for p in ["", "index.html"] + paginas_app + [p[:-5] for p in paginas_app]:
            pg = ctx.new_page()
            errs = []
            pg.on("pageerror", lambda e: errs.append(str(e)))
            try:
                rr = pg.goto(base + "/konfirmu/app/" + p, wait_until="load", timeout=15000)
                ok = rr is not None and rr.ok and pg.evaluate("document.body && document.body.innerText.length>40")
            except Exception as e:
                ok = False; errs.append(str(e)[:80])
            if not ok or errs:
                falham.append((p or "./", errs[:1]))
            pg.close()
        total = 2 + 2 * len(paginas_app)
        prova("modo avião: %d de %d endereços abrem sem rede (com e sem «.html»)" % (total - len(falham), total), not falham, falham[:5])
        ctx.close()

        # D. Modo Criança e Tranca Parental (no menu: a entrada /konfirmu/app/ é o Modo Família 3D desde 27-11, ordem das 17:42)
        ctx = b.new_context(**TEL)
        page = ctx.new_page()
        page.goto(base + "/konfirmu/app/app_unica.html"); page.wait_for_timeout(400)
        page.get_by_role("button", name="Modo Criança").click()
        def pin(p):
            for d in p:
                page.locator(".k-teclado button[data-d='%s']" % d).click()
            page.wait_for_timeout(450)
        pin("1234"); pin("1234")
        page.wait_for_timeout(600)
        estado = page.evaluate("""()=>({crianca:document.documentElement.classList.contains('k-crianca'),
            pro:getComputedStyle(document.getElementById('t-pro')).display, cid:getComputedStyle(document.getElementById('t-cid')).display,
            fam:document.getElementById('t-fam').getAttribute('aria-selected')})""")
        prova("Modo Criança: só o portal da família fica à vista", estado["crianca"] and estado["pro"] == "none" and estado["cid"] == "none" and estado["fam"] == "true", estado)
        tranca = page.evaluate("()=>JSON.parse(localStorage.getItem('konfirmu.tranca'))")
        prova("a tranca guarda só a derivação PBKDF2 (o PIN não fica escrito)", tranca and "1234" not in json.dumps(tranca) and tranca["voltas"] == 150000, {k: tranca[k] for k in ("v", "voltas")} if tranca else None)
        page.goto(base + "/konfirmu/app/terminal.html"); page.wait_for_timeout(500)
        fechado = page.locator(".k-veu[data-bloqueio]").count() == 1 and page.evaluate("document.querySelector('#saida').closest('[inert]')!==null")
        prova("Modo Criança: o terminal (página de adultos) fica fechado", fechado)
        page.goto(base + "/konfirmu/app/girafinhas_criancas_facil.html"); page.wait_for_timeout(400)
        page.evaluate("()=>{const a=document.createElement('a');a.href='https://example.org/';a.id='fora';a.textContent='fora';document.body.prepend(a)}")
        antes = page.url
        page.click("#fora"); page.wait_for_timeout(400)
        prova("Modo Criança: uma ligação para fora não sai da app", page.url == antes and page.locator(".k-aviso-crianca").count() >= 1, page.url)
        page.goto(base + "/konfirmu/app/terminal.html"); page.wait_for_timeout(400)
        page.locator(".k-veu[data-bloqueio] button[data-k='adulto']").click(); page.wait_for_timeout(300)
        pin("0000")
        errado = page.locator(".k-msg").last.inner_text()
        prova("PIN errado não abre o Modo Adulto", "errado" in errado.lower() and page.evaluate("localStorage.getItem('konfirmu.modoCrianca')") == "1", errado)
        pin("1234"); page.wait_for_timeout(600)
        prova("PIN certo abre o Modo Adulto e solta a página", page.evaluate("localStorage.getItem('konfirmu.modoCrianca')") is None and page.locator(".k-veu").count() == 0)
        ctx.close()

        # E. terminal
        ctx = b.new_context(**TEL)
        page = ctx.new_page()
        page.goto(base + "/konfirmu/app/terminal.html"); page.wait_for_timeout(400)
        def correr(c):
            page.evaluate("c=>window.KonfirmuTerminal.correr(c)", c)
            page.wait_for_timeout(300)
            return page.locator("#saida").inner_text()
        out = correr("selftest")
        prova("terminal: selftest 4 de 4 (SHA-256 NIST e a caixa sem rede)", "selftest: 4 de 4" in out, out[-160:])
        out = correr("bigint-test")
        prova("terminal: bigint-test 10 de 10", "bigint-test: 10 de 10 certos" in out, out[-120:])
        out = correr("sha256 abc")
        prova("terminal: sha256 abc = ba7816bf…", "ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad" in out)
        out = correr("verify ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad abc")
        prova("terminal: verify confirma igual", "IGUAL" in out)
        out = correr("verify 0000000000000000000000000000000000000000000000000000000000000000 abc")
        prova("terminal: verify apanha diferente", "DIFERENTE" in out)
        ctx.close()

        # F. capturas
        if CAPTURAS:
            os.makedirs(CAPTURAS, exist_ok=True)
            ctx = b.new_context(**TEL)
            for nome, alvo, antes_js in [("01_entrada", "/konfirmu/", None), ("02_app_inicio", "/konfirmu/app/", None),
                                         ("03_app_familia_tigelas", "/konfirmu/app/app_unica.html", "document.getElementById('t-fam').click()"),
                                         ("04_terminal", "/konfirmu/app/terminal.html", "window.KonfirmuTerminal.correr('selftest')"),
                                         ("05_girafinhas", "/konfirmu/app/girafinhas_criancas_facil.html", None),
                                         ("06_chat_de_bolso", "/konfirmu/app/konfirmu_chat_offline_v0.1.html", None),
                                         ("07_verificar_ata", "/konfirmu/app/chronolex_verify.html", None),
                                         ("08_manifesto", "/konfirmu/manifesto.html", None)]:
                page = ctx.new_page()
                page.goto(base + alvo); page.wait_for_timeout(700)
                if antes_js:
                    page.evaluate(antes_js); page.wait_for_timeout(700)
                page.screenshot(path=os.path.join(CAPTURAS, nome + ".png"))
                page.close()
            ctx.close()
        b.close()
    srv.shutdown()
    print("\n%d PASSA, %d FALHA" % (len(bons), len(maus)))
    return 1 if maus else 0


if __name__ == "__main__":
    sys.exit(main())
