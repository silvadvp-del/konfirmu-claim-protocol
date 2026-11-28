#!/usr/bin/env python3
"""Constrói a pasta konfirmu/ para dpsindustrial.nl/konfirmu/ (KON-613, ordem do David de 27-11-2026, 14:53 e 15:32).

Uma só pasta, pronta a subir, feita só a partir deste repositório (main) e da cópia do que está no ar
(site_nl/fonte_ao_vivo/, conferida byte a byte com a medição do ZCode/GLM de 27-11, 12:45 UTC):

  konfirmu/index.html          a entrada que está no ar, com a paleta única (Azul Abissal, vidro, Pêssego Solar,
                               Branco Titânio), a marca inteira e as peças guardadas em konfirmu/entrada/
  konfirmu/entrada/            folhas de estilo, scripts e imagens da entrada (cópias da raiz do sítio, recoloridas)
  konfirmu/app/                a App Única: 3 portais, as 8 tigelas, Modo Criança com tranca, terminal sem rede,
                               chat de bolso (Camada 0) com a IA local só depois de um sim (Camada 1), sw.js que
                               guarda tudo para o modo avião (também com os endereços sem .html da Cloudflare Pages)
  konfirmu/manifesto.html      o manifesto corrigido (ZCode/GLM, 27-11): EUPL-1.2, sem promessas por cumprir
  konfirmu/protocolo/          KFC-0.1 (roteador frugal), as correções de referência do livro-razão (PR #1442)
  konfirmu/_anterior/          a versão anterior (entrada, app e offline.zip), num ZIP, para nada se perder
  konfirmu/SHA256SUMS.txt      o hash de cada ficheiro

Uso: python3 -I scripts/build_site_nl.py [SAIDA]     (por omissão: dist_nl)
Construir duas vezes do zero dá os mesmos bytes (o teste tests/test_site_nl.py confere).
"""
import hashlib
import html
import io
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import zipfile

AQUI = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(AQUI)
sys.path.insert(0, AQUI)
import gerar_menu  # noqa: E402
import tema_2040  # noqa: E402
import tigelas  # noqa: E402
import paleta_unica  # noqa: E402  (paleta única de 27-11, 13:14: o sítio passa pelo mesmo conversor da app)
import selo_versao  # noqa: E402  (selo de versão e data no rodapé de todas as páginas, ordem de 28-11, 04:25)

FONTE = os.path.join(REPO, "site_nl", "fonte_ao_vivo")
FAMILIA_3D = os.path.join(REPO, "familia3d", "portal_familia_dual_mode.html")  # feito por familia3d/fonte (node build.mjs)
DATA_ZIP = (2026, 11, 27, 0, 0, 0)

PAGINAS_APP = sorted(p for p in tema_2040.PAGINAS if not p.startswith("edicao-21/")) + ["economia_anti_casino.html"]
DA_EDICAO_21 = ["edicao-21/Tutor-Girafinha-offline.html", "edicao-21/kcp_family_quiz.html"]
ASSETS_APP = ["imersao.css", "imersao.js", "nacl-fast.min.js", "nacl-util.min.js", "qrcode.js",
              "konfirmu-2040.js", "kcp_ed_estrito.js", "terminal_worker.js", "ceu_vivo.js"]

# entrada: caminho na raiz do sítio → caminho no pacote
ENTRADA = {
    "/assets/konfirmu-coming-soon/page.css?v=20261027": ("assets/konfirmu-coming-soon/page.css", "entrada/page.css"),
    "/assets/dps-institucional/institucional.css": ("assets/dps-institucional/institucional.css", "entrada/institucional.css"),
    "/assets/holo/landing.css": ("assets/holo/landing.css", "entrada/landing.css"),
    "/assets/dps-institucional/engine.js": ("assets/dps-institucional/engine.js", "entrada/engine.js"),
    "/assets/dps-institucional/konfirmu.js": ("assets/dps-institucional/konfirmu.js", "entrada/konfirmu.js"),
    "/assets/dps-prism.js": ("assets/dps-prism.js", "entrada/dps-prism.js"),
    "/assets/holo/holo-window.js": ("assets/holo/holo-window.js", "entrada/holo-window.js"),
    "/assets/holo/landing.js": ("assets/holo/landing.js", "entrada/landing.js"),
    "/assets/holo/scene-bg.svg": ("assets/holo/scene-bg.svg", "entrada/scene-bg.svg"),
    "/assets/holo/scene-card.svg": ("assets/holo/scene-card.svg", "entrada/scene-card.svg"),
    "/assets/holo/scene-front.svg": ("assets/holo/scene-front.svg", "entrada/scene-front.svg"),
    "/assets/holo/scene-grid.svg": ("assets/holo/scene-grid.svg", "entrada/scene-grid.svg"),
    "/assets/marcas/konfirmu.svg": ("assets/marcas/konfirmu.svg", "entrada/konfirmu.svg"),
    "/assets/konfirmu-coming-soon/konfirmu-k3d.svg": ("assets/konfirmu-coming-soon/konfirmu-k3d.svg", "entrada/konfirmu-k3d.svg"),
    "/assets/dps-h3-license.txt": ("assets/dps-h3-license.txt", "entrada/h3-licenca-apache-2.0.txt"),
}
SETA_FORA = ("↗", "→")  # a seta «↗» (pictográfica) passa a «→»
# A entrada que está no ar é clara (fundo branco) e violeta. Passa à paleta única pelas variáveis da própria folha.
ENTRADA_ESCURA = """
/* 27-11-2026 (ordem do David, 14:53 e 15:32): paleta única — Azul Abissal, vidro, Pêssego Solar, Branco Titânio */
:root{color-scheme:dark;--u-marca:#f7b397;--kv-v:255,158,125;--kv-m:255,158,125;--kv-p:255,211,194;--kv-g:255,158,125;--kv-l:159,179,200;
--kv-bg:#0B192C;--kv-bg-deep:#0F223D;--kv-bg-top:#0F223D;--kv-text:#F4F7FA;--kv-muted:#9FB3C8;--kv-faint:#9FB3C8;
--kv-accent:#FF9E7D;--kv-accent2:#FF9E7D;--kv-ink:#0B192C;
--kv-glass:linear-gradient(160deg,rgba(15,34,61,.92),rgba(15,34,61,.72) 52%,rgba(15,34,61,.86));
--kv-card:linear-gradient(#0F223D,#13294A);--kv-line:rgba(244,247,250,.12);--kv-line2:rgba(255,158,125,.32);
--kv-cta:linear-gradient(110deg,#FF9E7D 0%,#FF9E7D 100%);--kv-orb:linear-gradient(135deg,#FF9E7D 0%,rgba(255,158,125,.8) 100%);
--kv-vivid:linear-gradient(125deg,#FF9E7D 0%,#FF9E7D 60%,#F4F7FA 100%);
--kv-edge:linear-gradient(150deg,rgba(255,158,125,.6),rgba(255,158,125,.2) 40%,rgba(244,247,250,.25) 70%,rgba(255,158,125,.5));
--kv-shadow:0 14px 40px rgba(0,0,0,.35),0 1px 0 rgba(244,247,250,.06) inset;
--kv-ring:0 0 0 2px rgba(255,158,125,.6),0 0 0 7px rgba(255,158,125,.16);--peach-start:#FF9E7D;--peach-end:#FF9E7D}
html,body{background-color:#0B192C;color:#F4F7FA}
select{background-color:#0F223D;color:#F4F7FA;border:1px solid rgba(244,247,250,.22)}
.wordmark{white-space:nowrap;word-spacing:0}.wordmark span{display:inline;margin:0;padding:0;letter-spacing:inherit;color:#FF9E7D}
html body .dps-langpick select,html body #dps-dialect{background:#0F223D;color:#F4F7FA;border-color:rgba(244,247,250,.22)}
html body .dps-live button,html body .dps-live select,html body .dps-live a{background:rgba(15,34,61,.72);color:#F4F7FA;border-color:rgba(244,247,250,.22)}
html body .dps-live button[aria-pressed="true"]{background:#FF9E7D;color:#0B192C;border-color:#FF9E7D}
html body .dps-product-brand{background:#0F223D}
html body .dps-book-hint{color:#9FB3C8}
html body .textlink{display:block;margin:6px 0}
/* 28-11-2026, 04:25 (ordem do David): o «u» de Konfirmu em #f7b397, só aí */
.wordmark span{color:var(--u-marca)}
"""


def ler(caminho, binario=False):
    with open(caminho, "rb") as f:
        b = f.read()
    return b if binario else b.decode("utf-8")


def recolorir(texto):
    return tema_2040.trocar_cores(texto, dict(tema_2040.GLOBAL))


# ---------------------------------------------------------------- a App Única (app/)
def menu_web():
    avisos = gerar_menu.avisos_pt(REPO)
    linguas = tigelas.ler_linguas(REPO)
    dados = tigelas.dados_linguas(linguas)
    menu, n = gerar_menu.pagina("web", avisos, linguas["pt"], dados)
    assert n == 23, n  # 21 atividades da edição + a economia + o terminal
    return menu, n


def manifesto_web():
    return json.dumps({"name": "Konfirmu", "short_name": "Konfirmu", "start_url": "./", "scope": "./",
                       "display": "standalone", "background_color": "#0B192C", "theme_color": "#0B192C",
                       "lang": "pt", "description": "A App Única da Konfirmu: funciona no teu aparelho, também sem rede."},
                      ensure_ascii=False, indent=1) + "\n"


def sw_web(pecas, versao):
    lista = json.dumps(["./"] + pecas, ensure_ascii=False)
    return """// sw.js da App Única em dpsindustrial.nl/konfirmu/app/ — gerado por scripts/build_site_nl.py. Não editar à mão.
// Guarda todas as peças para o modo avião. A Cloudflare Pages tira o «.html» dos endereços (307/308): cada peça
// fica guardada com o endereço pedido e com o endereço final, sem a marca de redirecionamento (o navegador recusa
// respostas redirecionadas numa navegação).
const VERSAO = "konfirmu-nl-%(versao)s";
const CACHE = VERSAO + ":" + self.registration.scope;
const PECAS = %(lista)s;
async function guardar(cache, url) {
  const r = await fetch(url, { cache: "no-cache", redirect: "follow" });
  if (!r.ok) throw new Error(url + " " + r.status);
  const corpo = await r.blob();
  const limpa = () => new Response(corpo, { status: 200, statusText: "OK", headers: r.headers });
  await cache.put(new URL(url, self.registration.scope).href, limpa());
  if (r.redirected && r.url) await cache.put(r.url, limpa());
}
async function guardarTudo(soFalta) {
  const cache = await caches.open(CACHE);
  const falhas = [];
  for (const p of PECAS) {
    const url = new URL(p, self.registration.scope).href;
    if (soFalta && await cache.match(url)) continue;
    try { await guardar(cache, url); } catch (e) { if (p !== "./") falhas.push(p); }
  }
  return falhas;
}
self.addEventListener("install", (e) => {
  e.waitUntil(guardarTudo(false).then((falhas) => { if (falhas.length) throw new Error("faltam " + falhas.join(", ")); }));
  self.skipWaiting();
});
self.addEventListener("activate", (e) => {
  const meu = ":" + self.registration.scope;
  e.waitUntil(caches.keys().then((ks) => Promise.all(ks.filter((k) => k !== CACHE && k.endsWith(meu) && k.startsWith("konfirmu-")).map((k) => caches.delete(k)))).then(() => self.clients.claim()));
});
async function responder(req) {
  const cache = await caches.open(CACHE);
  let r = await cache.match(req, { ignoreSearch: true });
  if (r) return r;
  const u = new URL(req.url);
  if (u.origin === location.origin) {
    const tentativas = [];
    if (u.pathname.endsWith("/")) tentativas.push(u.pathname + "index.html");
    else if (!u.pathname.endsWith(".html")) tentativas.push(u.pathname + ".html", u.pathname + "/index.html");
    for (const t of tentativas) { r = await cache.match(new URL(t, u.origin).href); if (r) return r; }
  }
  try { return await fetch(req); }
  catch (e) {
    if (req.mode === "navigate") { const inicio = await cache.match(new URL("./index.html", self.registration.scope).href); if (inicio) return inicio; }
    throw e;
  }
}
self.addEventListener("fetch", (e) => {
  if (e.request.method !== "GET" || new URL(e.request.url).origin !== location.origin) return;
  e.respondWith(responder(e.request));
});
// Botão «Preparar modo avião» do início: guarda o que faltar e diz quantas peças estão neste aparelho.
self.addEventListener("message", (e) => {
  if (!e.data || e.data.tipo !== "konfirmu-preparar" || !e.ports || !e.ports[0]) return;
  const porta = e.ports[0];
  e.waitUntil(guardarTudo(true).then(async () => {
    const cache = await caches.open(CACHE); const faltam = [];
    for (const p of PECAS) if (!(await cache.match(new URL(p, self.registration.scope).href))) faltam.push(p);
    porta.postMessage({ total: PECAS.length, guardadas: PECAS.length - faltam.length, faltam });
  }));
});
""" % {"versao": versao, "lista": lista}


def chat_um_so_sw(t):
    # como no empacotador offline: um só service worker para a app toda
    novo, n = re.subn(r"""serviceWorker\.register\(\s*(['"])(?:\./)?konfirmu_chat_sw\.js\1""", "serviceWorker.register('./sw.js'", t)
    return novo


def pacote_offline(saida_tmp):
    """O executável offline de duplo clique (o mesmo do fluxo do GitHub), para descarregar da página."""
    # «--base edicao-21» relativo, como no passo do GitHub: o caminho da cópia do repositório não entra no ZIP
    # (o PACOTE.json guarda o nome da base); assim o ZIP daqui é o mesmo, byte a byte, que o GitHub atesta.
    subprocess.run([sys.executable, "-I", os.path.join(AQUI, "build_pacote_offline.py"), "--edicao-21", "--base",
                    "edicao-21", "--saida", saida_tmp], check=True, stdout=subprocess.DEVNULL, cwd=REPO)
    return ler(os.path.join(saida_tmp, "KONFIRMU_EXECUTAVEL_OFFLINE_2030.zip"), True)


def paleta_estrita(destino, texto):
    """Cada cor das peças da entrada fica na paleta oficial (pêssego, azul abissal, vidro, titânio, nevoeiro).
    O portão visual (scripts/paleta_unica.py verificar) mede a pasta konfirmu/ inteira."""
    if destino.endswith(".css"):
        return paleta_unica.converter_css(texto, False)
    if destino.endswith(".js"):
        return paleta_unica.converter_js(texto, False)
    ctx = paleta_unica.Contexto(False)
    texto = re.sub(r"(<style\b[^>]*>)(.*?)(</style>)",
                   lambda m: m.group(1) + paleta_unica.converter_css(m.group(2), False) + m.group(3), texto, flags=re.S | re.I)
    texto = re.sub(r'(\s(?:fill|stroke|stop-color|flood-color|lighting-color|color)\s*=\s*")([^"]*)(")',
                   lambda m: m.group(1) + paleta_unica.trocar_cores(m.group(2), "desenho", ctx) + m.group(3), texto)
    return re.sub(r'(\sstyle\s*=\s*")([^"]*)(")',
                  lambda m: m.group(1) + paleta_unica.corpo_decls(m.group(2), ctx, {}, "inline") + m.group(3), texto)


# ---------------------------------------------------------------- a entrada (index.html)
def entrada(ficheiros):
    t = ler(os.path.join(FONTE, "konfirmu", "index.html"))
    for raiz, (fonte, destino) in ENTRADA.items():
        conteudo = ler(os.path.join(FONTE, fonte), True)
        if destino.endswith((".css", ".svg", ".js")):
            texto = conteudo.decode("utf-8")
            texto = recolorir(texto).replace(*SETA_FORA)
            if destino == "entrada/page.css":
                # a marca nunca aparece partida: «Konfirmu» numa só palavra, o «u» em pêssego, sem espaço
                texto += ENTRADA_ESCURA
            texto = paleta_estrita(destino, texto)
            conteudo = texto.encode("utf-8")
        ficheiros[destino] = conteudo
        t = t.replace('"%s"' % raiz, '"/konfirmu/%s"' % destino)
    t = paleta_unica.converter_html(recolorir(t).replace(*SETA_FORA), [])
    t = t.replace('href="/konfirmu/app/offline.zip"', 'href="/konfirmu/app/konfirmu-offline-2030.zip"')
    ancora = ('data-dt="189">What we know about Konfirmu (PDF in Portuguese)</a>')
    assert t.count(ancora) == 1, "não encontrei a ligação do PDF «What we know»"
    t = t.replace(ancora, ancora + '<a class="textlink" href="/konfirmu/manifesto.html" hreflang="pt-PT">'
                  'Manifesto Konfirmu · 27-11-2026 (PT)</a><a class="textlink" href="/konfirmu/protocolo/KFC-0.1.md" '
                  'hreflang="pt-PT">KFC-0.1 · roteador frugal (PT)</a>')
    # o selo que diz o que corre: a licença da Konfirmu é EUPL-1.2; a H3 (biblioteca de fora) é Apache-2.0
    return t


# ---------------------------------------------------------------- manifesto e protocolo
def md_para_html(md):
    out, lista = [], False
    def inline(s):
        s = html.escape(s, quote=False)
        s = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", s)
        s = re.sub(r"`([^`]+)`", r"<code>\1</code>", s)
        s = re.sub(r"«", "«", s)
        return s
    for linha in md.splitlines():
        if re.match(r"^\s*[-*] ", linha) or re.match(r"^\s*\d+\. ", linha):
            if not lista:
                out.append("<ul>"); lista = True
            out.append("<li>%s</li>" % inline(re.sub(r"^\s*(?:[-*]|\d+\.) ", "", linha)))
            continue
        if lista and linha.startswith("   ") and out and out[-1].startswith("<li>"):
            out[-1] = out[-1][:-5] + " " + inline(linha.strip()) + "</li>"
            continue
        if lista:
            out.append("</ul>"); lista = False
        if linha.startswith("# "):
            out.append("<h1>%s</h1>" % inline(linha[2:]))
        elif linha.startswith("## "):
            out.append("<h2>%s</h2>" % inline(linha[3:]))
        elif linha.strip():
            if out and out[-1].startswith("<p>") and not out[-1].endswith("</p>"):
                out[-1] += " " + inline(linha.strip())
            else:
                out.append("<p>" + inline(linha.strip()))
        else:
            if out and out[-1].startswith("<p>") and not out[-1].endswith("</p>"):
                out[-1] += "</p>"
    if lista:
        out.append("</ul>")
    if out and out[-1].startswith("<p>") and not out[-1].endswith("</p>"):
        out[-1] += "</p>"
    return "\n".join(out)


def manifesto():
    md = ler(os.path.join(REPO, "site_nl", "MANIFESTO_2026-11-27.md"))
    nota_interna = re.search(r"\*\*Rascunho interno \(nível 0\)\.\*\*.*?(?=\n\n)", md, re.S)
    if nota_interna:
        md = md.replace(nota_interna.group(0), "**Versão de 27-11-2026.** Cada frase foi conferida nessa data, contra os "
                        "repositórios públicos, as páginas no ar e as medições da casa. O que ainda não existe está "
                        "escrito como não existe.")
    corpo = md_para_html(md)
    avisos = gerar_menu.avisos_pt(REPO)
    pagina = ("<!DOCTYPE html>\n<html lang=\"pt\">\n<head>\n<meta charset=\"UTF-8\">\n"
              "<meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\">\n"
              "<title>Konfirmu · Manifesto (27-11-2026)</title>\n<style>\n"
              "body{font:17px/1.65 system-ui,-apple-system,'Segoe UI',Roboto,sans-serif;max-width:760px;margin:0 auto;padding:28px 18px 10px;background:#0B192C;color:#F4F7FA}\n"
              "h1{font-size:1.75rem;line-height:1.2;margin:0 0 14px;font-weight:700;letter-spacing:-.01em}\n"
              "h2{font-size:1.2rem;margin:28px 0 8px;color:#FF9E7D}\n"
              "p,li{color:#F4F7FA}ul{padding-left:1.2em}li{margin:4px 0}code{font:.9em ui-monospace,Menlo,monospace;color:#FF9E7D}\n"
              "b{color:#F4F7FA}.topo{margin:0 0 22px}.topo a{color:#FF9E7D}\n"
              "</style>\n</head>\n<body>\n<p class=\"topo\"><a href=\"/konfirmu/\">Konfirmu</a> · <a href=\"/konfirmu/app/\">abrir a app</a></p>\n"
              + corpo + "\n</body>\n</html>\n")
    pagina = tema_2040.injetar(pagina, "manifesto.html", "info", avisos).replace(
        '<dl aria-label="Avisos legais" hidden>', '<dl aria-label="Avisos legais">')
    # no manifesto o rodapé aponta para a app
    pagina = pagina.replace('href="./app_unica.html">Início', 'href="/konfirmu/app/">Início').replace(
        'src="./assets/konfirmu-2040.js"', 'src="/konfirmu/app/assets/konfirmu-2040.js"')
    return pagina


# ---------------------------------------------------------------- _anterior/
def zip_deterministico(entradas):
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as z:
        for nome in sorted(entradas):
            info = zipfile.ZipInfo(nome, DATA_ZIP)
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o644 << 16
            z.writestr(info, entradas[nome])
    return buf.getvalue()


def anterior():
    dentro = {
        "konfirmu/index.html": ler(os.path.join(FONTE, "konfirmu", "index.html"), True),
        "konfirmu/app/index.html": ler(os.path.join(FONTE, "konfirmu", "app", "index.html"), True),
        "konfirmu/app/offline.zip": ler(os.path.join(FONTE, "konfirmu", "app", "offline.zip"), True),
    }
    somas = "".join("%s  %s\n" % (hashlib.sha256(dentro[n]).hexdigest(), n) for n in sorted(dentro))
    leia = ("# Versão anterior de dpsindustrial.nl/konfirmu/ (guardada a 27-11-2026)\n\n"
            "O ZIP traz, byte a byte, o que estava no ar antes deste pacote: a entrada, a app (KONFIRMU OS 2030 · BETA)\n"
            "e o offline.zip dela. Copiado duas vezes do sítio às 14:12 UTC, igual nas duas, e igual à medição do\n"
            "ZCode/GLM das 12:45 UTC (sem o script que a Cloudflare acrescenta a cada resposta).\n\n"
            "Está fechado num ZIP para não ficar publicada outra vez uma página com a política antiga\n"
            "(connect-src com localhost:8790 e https: livre). Nada foi apagado.\n\n" + "```\n" + somas + "```\n")
    dentro["LEIA-ME.md"] = leia.encode("utf-8")
    return {"_anterior/konfirmu_anterior_2026-11-27.zip": zip_deterministico(dentro),
            "_anterior/LEIA-ME.md": leia.encode("utf-8"),
            "_anterior/SHA256SUMS.txt": somas.encode("utf-8")}


# ---------------------------------------------------------------- tudo
def selar_paginas(ficheiros, selo):
    """O selo de versão (r10 · commit · data) em cada página HTML do pacote; idempotente."""
    for n in sorted(ficheiros):
        if n.endswith(".html") and not n.startswith("_anterior/"):
            ficheiros[n] = selo_versao.aplicar(ficheiros[n].decode("utf-8"), selo).encode("utf-8")


def construir(saida):
    ficheiros = {}
    selo = selo_versao.ler(REPO)
    menu, _ = menu_web()
    # Entrada da app: o Modo Família 3D, com as girafinhas em 3D (ordem do David de 27-11-2026, 17:42).
    # O menu dos 3 portais fica em app_unica.html; a marca e o ícone dos portais levam lá, o «3D» do menu traz de volta.
    familia = ler(FAMILIA_3D, True)
    ficheiros["app/index.html"] = familia
    ficheiros["app/portal_familia_dual_mode.html"] = familia
    ficheiros["app/app_unica.html"] = menu.encode("utf-8")
    for p in PAGINAS_APP:
        t = ler(os.path.join(REPO, p))
        if "chat_offline" in p:
            t = chat_um_so_sw(t)
        ficheiros["app/" + p] = t.encode("utf-8")
    for p in DA_EDICAO_21:
        ficheiros["app/" + os.path.basename(p)] = ler(os.path.join(REPO, p), True)
    for a in ASSETS_APP:
        ficheiros["app/assets/" + a] = ler(os.path.join(REPO, "assets", a), True)
    ficheiros["app/manifest.json"] = manifesto_web().encode("utf-8")
    with tempfile.TemporaryDirectory() as tmp:
        zipo = pacote_offline(tmp)
    ficheiros["app/konfirmu-offline-2030.zip"] = zipo
    ficheiros["app/konfirmu-offline-2030.zip.sha256"] = ("%s  konfirmu-offline-2030.zip\n" % hashlib.sha256(zipo).hexdigest()).encode()
    selar_paginas(ficheiros, selo)  # antes da versão do sw.js: um selo novo chega a quem tinha a cache antiga
    pecas = sorted(n[4:] for n in ficheiros if n.startswith("app/") and not n.endswith((".zip", ".sha256")))
    versao = hashlib.sha256(b"".join(ficheiros["app/" + p] for p in pecas)).hexdigest()[:12]
    ficheiros["app/sw.js"] = sw_web(["./" + p for p in pecas], versao).encode("utf-8")
    ficheiros["index.html"] = entrada(ficheiros).encode("utf-8")
    ficheiros["manifesto.html"] = manifesto().encode("utf-8")
    ficheiros["MANIFESTO.md"] = ler(os.path.join(REPO, "site_nl", "MANIFESTO_2026-11-27.md"), True)
    for f in ("KFC-0.1.md", "konfirmu_frugal_router.py", "LICENSE.txt"):
        ficheiros["protocolo/" + f] = ler(os.path.join(REPO, f), True)
    for raiz, _, nomes in os.walk(os.path.join(REPO, "ferramentas", "correcoes_ledger")):
        for n in sorted(nomes):
            c = os.path.join(raiz, n)
            ficheiros["protocolo/correcoes_ledger/" + os.path.relpath(c, os.path.join(REPO, "ferramentas", "correcoes_ledger"))] = ler(c, True)
    ficheiros.update(anterior())
    selar_paginas(ficheiros, selo)  # a entrada e o manifesto também levam o selo (as da app já o têm: fica igual)
    somas = "".join("%s  %s\n" % (hashlib.sha256(ficheiros[n]).hexdigest(), n) for n in sorted(ficheiros))
    ficheiros["SHA256SUMS.txt"] = somas.encode("utf-8")
    alvo = os.path.join(saida, "konfirmu")
    if os.path.exists(alvo):
        shutil.rmtree(alvo)
    for n, c in ficheiros.items():
        d = os.path.join(alvo, n)
        os.makedirs(os.path.dirname(d), exist_ok=True)
        with open(d, "wb") as f:
            f.write(c)
        os.utime(d, (1795737600, 1795737600))  # 27-11-2026 00:00 UTC, para a pasta ser igual em qualquer máquina
    total = sum(len(c) for c in ficheiros.values())
    raiz = hashlib.sha256(ficheiros["SHA256SUMS.txt"]).hexdigest()
    print("konfirmu/: %d ficheiros · %d bytes · SHA-256 do SHA256SUMS.txt: %s" % (len(ficheiros), total, raiz))
    print("selo de versão: %s" % selo_versao.texto(selo))
    import zlib
    if "ng" in zlib.ZLIB_RUNTIME_VERSION:
        # os ZIP comprimem de outra maneira com a zlib-ng: tudo funciona, mas os bytes deixam de bater com os do GitHub
        print("AVISO: esta máquina usa %s; o GitHub usa a zlib padrão. Para bytes iguais aos do GitHub, "
              "construir com a zlib padrão (por exemplo LD_PRELOAD=/usr/lib/x86_64-linux-gnu/libz.so.1)." % zlib.ZLIB_RUNTIME_VERSION)
    return raiz


if __name__ == "__main__":
    construir(sys.argv[1] if len(sys.argv) > 1 else os.path.join(REPO, "dist_nl"))
