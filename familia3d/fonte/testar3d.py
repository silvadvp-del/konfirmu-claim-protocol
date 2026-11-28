#!/usr/bin/env python3
"""Testes do Modo Família 3D num Chromium real (motor 3D por software), sem rede. Escreve PASTA/provas/TESTES.txt e as capturas.
O relatório não leva horas nem números ao acaso: duas corridas iguais dão o mesmo ficheiro. Uso: python3 testar3d.py PASTA"""
import base64, colorsys, hashlib, json, os, re, struct, subprocess, sys
from PIL import Image
from playwright.sync_api import sync_playwright

PASTA = os.path.abspath(sys.argv[1]); PROVAS = os.path.join(PASTA, "provas")
PORTAL = os.path.join(PASTA, "portal_familia_dual_mode.html"); URL = "file://" + PORTAL
ARGS = ["--use-angle=swiftshader", "--enable-unsafe-swiftshader", "--ignore-gpu-blocklist", "--font-render-hinting=none",
        "--disable-lcd-text", "--force-color-profile=srgb", "--hide-scrollbars"]
UE = "bg cs da de el en es et fi fr ga hr hu it lt lv mt nl pl pt ro sk sl sv".split()
CHAVE = "konfirmu_familia_v1"
CSP_JS = "window.__csp=[];document.addEventListener('securitypolicyviolation',function(e){window.__csp.push(e.violatedDirective)});"
R = []
FONTE = os.path.join(PASTA, "fonte")
TX = json.load(open(os.path.join(FONTE, "textos.json"), encoding="utf-8"))
S = {c: dict(zip(TX["chaves"], v["s"])) for c, v in TX["linguas"].items()}
MENU_PT = json.load(open(os.path.join(FONTE, "locales", "pt.json"), encoding="utf-8"))
CENAS = json.load(open(os.path.join(FONTE, "cenas.json"), encoding="utf-8"))


def ok(nome, cond, det=""):
    R.append(("PASS" if cond else "FALHA") + " — " + nome + ("" if cond or not det else " (" + str(det)[:220] + ")"))
    return bool(cond)


def ctx_de(b, locale="pt-PT", w=390, h=844, dsf=2, movel=True):
    return b.new_context(locale=locale, viewport={"width": w, "height": h}, device_scale_factor=dsf, is_mobile=movel, has_touch=movel, reduced_motion="reduce")


def abrir(ctx, q="", relogio=False):
    pg = ctx.new_page(); ped, err = [], []
    pg.on("request", lambda r: ped.append(r.url)); pg.on("pageerror", lambda e: err.append(str(e)))
    pg.on("console", lambda m: err.append(m.text) if m.type == "error" else None)
    pg.add_init_script(CSP_JS)
    if relogio:
        pg.clock.install()
    pg.goto(URL + "?quadros=1" + q); avancar(pg, 3)
    return pg, ped, err


def avancar(pg, s):
    pg.evaluate("function(s){ window.__t = (window.__t || 0) + s; window.__quadro(window.__t); return new Promise(function(r){ requestAnimationFrame(function(){ requestAnimationFrame(r); }); }); }", s)


def foto(pg, nome):
    d = os.path.join(PROVAS, nome); pg.screenshot(path=d); Image.open(d).save(d, "PNG", optimize=True)


def estado(pg):
    raw = pg.evaluate("localStorage.getItem('%s')" % CHAVE) or "{}"
    return raw, json.loads(raw)


def k3d(pg): return pg.evaluate("window.__k3d.estado()")


def digitar(pg, pin):
    for d in pin:
        pg.click('#teclado [data-d="%s"]' % d)
    pg.click("#teclado .tecla.ok"); pg.wait_for_timeout(350)


def em_crianca(pg): return pg.evaluate("document.body.classList.contains('modo-crianca')")
def sem_transbordo(pg): return pg.evaluate("document.documentElement.scrollWidth <= window.innerWidth")
def pequenos(pg): return pg.evaluate("Array.from(document.querySelectorAll('button,select,a.abrir,a.entrada')).filter(function(e){var r=e.getBoundingClientRect(),s=getComputedStyle(e);return r.width>0&&r.height>0&&s.visibility!=='hidden'&&r.height<44}).map(function(e){return e.id||e.className})")


def externos(ped): return [u for u in ped if not u.startswith("data:") and not u.startswith("blob:") and u.split("?")[0] != URL]


def esperar(pg, js, s=6.0):
    for _ in range(int(s * 10)):
        if pg.evaluate(js):
            return True
        pg.wait_for_timeout(100)
    return False


def memoria(ctx, pg):
    c = ctx.new_cdp_session(pg); c.send("Performance.enable")
    m = {x["name"]: x["value"] for x in c.send("Performance.getMetrics")["metrics"]}
    return m.get("JSHeapUsedSize", 0) / 1048576.0


def fluxo(b):
    ctx = ctx_de(b); pg, ped, err = abrir(ctx, relogio=True); pt = S["pt"]
    ok("3D ligado (WebGL) com o motor three.js embutido", pg.evaluate("window.__k3d.webgl") is True)
    ok("abre sem nenhum pedido de rede", not externos(ped), externos(ped))
    ok("sem erros na consola", not err, err)
    ok("sem violações da CSP", pg.evaluate("window.__csp.length") == 0, pg.evaluate("window.__csp"))
    ok("língua do aparelho pt-PT → pt-PT", pg.evaluate("document.documentElement.lang") == "pt-PT")
    val = pg.eval_on_selector_all("#sel-lingua option", "function(o){return o.map(function(x){return x.value})}")
    ok("62 línguas no menu (as da outra janela)", len(val) == 62, len(val))
    ok("as 24 línguas oficiais da UE estão todas", set(UE) <= set(val), sorted(set(UE) - set(val)))
    ok("8 tigelas no ecrã (zonas de toque)", pg.locator(".tig").count() == 8)
    ok("cartão da tigela 1: «%s» e liga a Tutor-Girafinha-offline.html" % MENU_PT["fam.tutor.t"],
       pg.text_content("#c-titulo") == MENU_PT["fam.tutor.t"] and pg.get_attribute("#c-abrir", "href") == "Tutor-Girafinha-offline.html")
    ok("«Começa aqui» liga a girafinhas_criancas_facil.html", pg.get_attribute("#entrada", "href") == "girafinhas_criancas_facil.html")
    foto(pg, "familia_telemovel.png")
    ok("telemóvel sem transbordo lateral (família)", sem_transbordo(pg))
    ok("toques com 44 px ou mais (família)", not pequenos(pg), pequenos(pg))
    pg.click("#b-seg"); avancar(pg, 2)
    ok("seta → roda o carrossel para a tigela 2 (Quiz)", k3d(pg)["foco"] == 1 and pg.text_content("#c-titulo") == MENU_PT["fam.quiz.t"])
    pg.click(".tig >> nth=0"); avancar(pg, 2)
    ok("tocar numa tigela põe-na à frente", k3d(pg)["foco"] == 0)
    ok("biometria escondida fora de https", pg.is_hidden("#b-bio"))
    pg.click("#b-entrar")
    ok("«Entrar no Modo Criança» pede um PIN novo", pg.is_visible("#pin") and pg.text_content("#pin-titulo") == pt["definir_pin"])
    foto(pg, "pin_telemovel.png")
    ok("toques com 44 px ou mais (teclado do PIN)", not pequenos(pg), pequenos(pg))
    digitar(pg, "12"); ok("PIN curto recusado", pg.text_content("#pin-erro") == pt["pin_curto"])
    digitar(pg, "1234"); digitar(pg, "9999")
    ok("PIN diferente obriga a recomeçar", pg.text_content("#pin-titulo") == pt["definir_pin"] and pg.text_content("#pin-erro") == pt["pin_diferente"])
    digitar(pg, "2580"); digitar(pg, "2580"); esperar(pg, "document.body.classList.contains('modo-crianca')"); avancar(pg, 3)
    ok("PIN confirmado abre o Modo Criança", em_crianca(pg) and k3d(pg)["modo"] == "crianca" and pg.is_visible("#crianca"))
    raw, est = estado(pg); pin = est.get("pin") or {}
    ok("o PIN não fica guardado: só o hash com sal", pin.get("hash") == hashlib.sha256((pin.get("sal", "") + ":2580").encode()).hexdigest() and len(pin.get("sal", "")) == 32 and '"2580"' not in raw)
    ok("o Modo Criança fica guardado no aparelho", est.get("crianca") is True)
    for _ in range(4):
        pg.click(".tig >> nth=2")
    avancar(pg, 1)
    ok("tigela 3 leva 3 pêssegos e não passa disso", k3d(pg)["cheias"][2] == 3 and pg.get_attribute(".tig >> nth=2", "data-cheia") == "1")
    ok("leitor de ecrã: «Tigela 3: 3 de 3»", pg.get_attribute(".tig >> nth=2", "aria-label") == "Tigela 3: 3 de 3", pg.get_attribute(".tig >> nth=2", "aria-label"))
    pg.click(".tig >> nth=0"); pg.click(".tig >> nth=1"); avancar(pg, 2)
    foto(pg, "crianca_telemovel.png")
    ok("telemóvel sem transbordo lateral (criança)", sem_transbordo(pg))
    ok("toques com 44 px ou mais (criança)", not pequenos(pg), pequenos(pg))
    for k in range(8):
        for _ in range((k + 1) - k3d(pg)["cheias"][k]):
            pg.click(".tig >> nth=%d" % k)
    avancar(pg, 1)
    ok("as 8 tigelas cheias mostram o fim", pg.is_visible("#final") and sum(k3d(pg)["cheias"]) == 36)
    pg.click("#b-denovo"); avancar(pg, 1)
    ok("«Outra vez» recomeça do zero", sum(k3d(pg)["cheias"]) == 0 and pg.is_hidden("#final"))
    pg.evaluate("history.back()"); esperar(pg, "!document.getElementById('aviso').hidden", 4)
    ok("o botão Voltar não sai do Modo Criança", em_crianca(pg) and pg.text_content("#aviso") == pt["pede_adulto"])
    pg.reload(); esperar(pg, "document.body.classList.contains('modo-crianca')", 6); avancar(pg, 2)
    ok("recarregar a página não sai do Modo Criança", em_crianca(pg) and k3d(pg)["modo"] == "crianca")
    pg.click("#b-sair")
    ok("«Sair» pede o PIN de adulto", pg.is_visible("#pin") and pg.text_content("#pin-titulo") == pt["desbloquear"])
    digitar(pg, "0000"); ok("PIN errado não sai", em_crianca(pg) and pg.text_content("#pin-erro") == pt["pin_errado"])
    for _ in range(4):
        digitar(pg, "0000")
    ok("5 PIN errados param o teclado 30 s", pg.evaluate("document.getElementById('teclado').classList.contains('parado')") and pg.text_content("#pin-erro").startswith(pt["pede_adulto"]))
    pg.keyboard.type("2580"); pg.keyboard.press("Enter"); pg.wait_for_timeout(300)
    ok("teclado parado: nem o PIN certo entra", em_crianca(pg))
    pg.clock.fast_forward(31000); esperar(pg, "!document.getElementById('teclado').classList.contains('parado')", 4)
    pg.keyboard.type("2580"); pg.keyboard.press("Enter"); esperar(pg, "!document.body.classList.contains('modo-crianca')", 4); avancar(pg, 2)
    ok("passados 30 s, o PIN certo (teclado físico) sai do Modo Criança", not em_crianca(pg) and k3d(pg)["modo"] == "familia")
    ok("ao sair, fica guardado o Modo Família", estado(pg)[1].get("crianca") is False)
    mem = memoria(ctx, pg)
    ok("memória JavaScript abaixo de 64 MB depois de todo o percurso", mem < 64, "%.1f MB" % mem)
    am = ["", "abc", "sal:1234", "0123456789abcdef0123456789abcdef:999999"]
    ok("SHA-256 de reserva (sem crypto.subtle) igual ao do Python",
       [pg.evaluate("function(s){return window.__k3d.sha256js(s)}", s) for s in am] == [hashlib.sha256(s.encode()).hexdigest() for s in am])
    pg.click("#b-filme"); avancar(pg, 15)
    ok("o filme abre com as personagens 3D e a legenda da cena 2", k3d(pg)["modo"] == "filme" and k3d(pg)["cena"] == 1 and pg.text_content("#legenda") == CENAS[1]["legenda"])
    avancar(pg, 100)
    cor = pg.evaluate("getComputedStyle(document.querySelector('#marca-filme .u')).color")
    ok("cena 12: a marca Konfirmu com o «u» Pêssego Solar", k3d(pg)["cena"] == 11 and pg.is_visible("#marca-filme") and cor == "rgb(255, 158, 125)", cor)
    pg.click("#b-fechar"); avancar(pg, 1)
    ok("fechar o filme volta à Família", k3d(pg)["modo"] == "familia")
    pg.select_option("#sel-lingua", "de"); mudou = pg.text_content("[data-t=entrar]") == S["de"]["entrar"]
    pg.reload(); esperar(pg, "document.documentElement.lang === 'de'", 6)
    ok("escolher a língua muda o texto e fica guardada", mudou and pg.evaluate("document.documentElement.lang") == "de")
    ok("tradução por IA leva a marca «por rever» (alemão)", pg.is_visible("#marca-ia") and pg.text_content("#marca-ia") == S["de"]["traducao_ia"], pg.text_content("#marca-ia"))
    txt = pg.evaluate("document.body.innerText")
    ok("zero emojis no texto do ecrã", not re.search("[\U0001F000-\U0001FAFF☀-➿️]", txt))
    ctx.close()


def linguas(b):
    marcas = []
    for loc, lang, dr in (("pt-BR", "pt-BR", "ltr"), ("nl-NL", "nl", "ltr"), ("ar", "ar", "rtl"), ("zh-TW", "zh-Hant", "ltr"), ("eu-ES", "pt-PT", "ltr")):
        ctx = ctx_de(b, locale=loc); pg, _, err = abrir(ctx)
        cod = "pt" if lang == "pt-PT" else lang
        menu = json.load(open(os.path.join(FONTE, "locales", cod + ".json"), encoding="utf-8"))
        certo = pg.evaluate("document.documentElement.lang") == lang and pg.evaluate("document.documentElement.dir") == dr and pg.text_content("[data-m='fam.titulo']") == menu["fam.titulo"]
        ok("aparelho em %s → %s (%s)" % (loc, lang, dr) if loc != "eu-ES" else "língua sem tradução (eu-ES) → pt-PT, a de reserva", certo and not err, (pg.evaluate("document.documentElement.lang"), err))
        marcas.append((lang, pg.is_visible("#marca-ia") == (lang != "pt-PT")))
        if loc == "ar":
            foto(pg, "rtl_arabe_telemovel.png"); ok("árabe sem transbordo lateral", sem_transbordo(pg))
        ctx.close()
    ok("a marca «tradução por IA» aparece nas línguas traduzidas e não no português de origem", all(x for _, x in marcas), marcas)
    ctx = ctx_de(b, w=1280, h=800, dsf=1, movel=False); pg, _, _ = abrir(ctx); foto(pg, "familia_computador.png"); ctx.close()


def biometria(b):
    ctx = ctx_de(b, dsf=1); corpo = open(PORTAL, "rb").read()
    ctx.route("https://konfirmu.test/**", lambda r: r.fulfill(status=200, content_type="text/html; charset=utf-8", body=corpo) if r.request.url.startswith("https://konfirmu.test/portal.html") else r.fulfill(status=404, body=""))
    pg = ctx.new_page(); erros = []
    cdp = ctx.new_cdp_session(pg); cdp.send("WebAuthn.enable", {"enableUI": False})
    cdp.send("WebAuthn.addVirtualAuthenticator", {"options": {"protocol": "ctap2", "transport": "internal", "hasResidentKey": True, "hasUserVerification": True, "isUserVerified": True, "automaticPresenceSimulation": True}})
    pg.goto("https://konfirmu.test/portal.html?quadros=1"); avancar(pg, 3)
    pg.click("#b-entrar"); digitar(pg, "2580"); digitar(pg, "2580"); esperar(pg, "document.body.classList.contains('modo-crianca')")
    pg.click("#b-sair"); digitar(pg, "2580"); avancar(pg, 1)
    ok("biometria: o botão aparece por https, depois de haver PIN", pg.evaluate("window.isSecureContext") and not em_crianca(pg) and pg.is_visible("#b-bio"))
    reg = saiu = False
    try:
        pg.click("#b-bio"); reg = esperar(pg, "!!(JSON.parse(localStorage.getItem('%s')||'{}')).cred" % CHAVE)
        pg.click("#b-entrar"); esperar(pg, "document.body.classList.contains('modo-crianca')"); avancar(pg, 2)
        pg.click("#b-sair"); pg.click("#b-pin-bio"); saiu = esperar(pg, "!document.body.classList.contains('modo-crianca')")
    except Exception as e:  # noqa: BLE001
        erros.append(str(e).splitlines()[0])
    ok("biometria: fica registada no aparelho (autenticador virtual do Chromium)", reg, erros)
    ok("biometria: sai do Modo Criança sem PIN", saiu, erros)
    ctx.close()


def verde_violeta_amarelo(r, g, bb):
    h, l, s = colorsys.rgb_to_hls(r / 255.0, g / 255.0, bb / 255.0); h *= 360
    if s < 0.25 or l < 0.12 or l > 0.9:
        return None
    if 75 <= h <= 165: return "verde"
    if 255 <= h <= 320: return "violeta"
    if 45 <= h < 75 and s > 0.5 and l > 0.35: return "amarelo"
    return None


def estaticos():
    html = open(PORTAL, encoding="utf-8").read()
    meta = re.search(r'Content-Security-Policy" content="([^"]+)"', html).group(1)
    css = html[html.index("<style>") + 7:html.index("</style>")]
    js = html[html.rindex("<script>") + 8:html.rindex("</script>")]
    h = lambda s: "sha256-" + base64.b64encode(hashlib.sha256(s.encode()).digest()).decode()
    ok("CSP fechada por hash (estilo e script), sem 'unsafe' e sem rede (connect-src 'none')", "'%s'" % h(css) in meta and "'%s'" % h(js) in meta and "unsafe" not in meta and "connect-src 'none'" in meta and "default-src 'none'" in meta)
    meu = open(os.path.join(FONTE, "src", "main.js"), encoding="utf-8").read()
    ok("o nosso código não chama a rede (fetch, XHR, WebSocket, sendBeacon)", not re.search(r"\bfetch\(|XMLHttpRequest|WebSocket|sendBeacon|EventSource", meu))
    dados = html[html.index('id="dados">') + 11:html.index("</script>", html.index('id="dados">'))]
    ok("zero emojis no código e nos textos das 62 línguas", not re.search("[\U0001F000-\U0001FAFF☀-➿️]", meu + css + json.loads(dados).__repr__()))
    perm = {"0b192c", "ff9e7d", "f4f7fa", "9fb3c8", "0f223d", "ef4444"}
    usadas = set(x.lower() for x in re.findall(r"#([0-9a-fA-F]{6})\b", css + meu)) | set(x.lower() for x in re.findall(r"0x([0-9a-fA-F]{6})\b", meu))
    rgbs = set(re.findall(r"rgba?\((\d+),\s*(\d+),\s*(\d+)", css + meu))
    trip = {("255", "158", "125"), ("244", "247", "250"), ("11", "25", "44"), ("15", "34", "61"), ("159", "179", "200")}
    ok("só as cores da paleta no nosso código (Azul Abissal, vidro, Pêssego Solar, Branco Titânio, Cinza Nevoeiro)", usadas <= perm and rgbs <= trip, (sorted(usadas - perm), sorted(rgbs - trip)))
    maus = {}
    for raiz, _, fs in os.walk(PASTA):
        for f in sorted(fs):
            if f.endswith((".png", ".jpg")):
                im = Image.open(os.path.join(raiz, f)).convert("RGB").resize((200, 200)); dd = im.tobytes()
                for i in range(0, len(dd), 3):
                    c = verde_violeta_amarelo(dd[i], dd[i + 1], dd[i + 2])
                    if c: maus[f + ":" + c] = maus.get(f + ":" + c, 0) + 1
    graves = {k: v for k, v in maus.items() if v > 40}
    ok("sem verde, violeta nem amarelo berrante nos píxeis das imagens (no máximo 0,1 %)", not graves, graves)
    tam = []
    for n in range(1, 9):
        p = os.path.join(PASTA, "tigelas", "tigela_%02d.png" % n)
        if os.path.exists(p):
            tam.append(struct.unpack(">II", open(p, "rb").read(24)[16:24]))
    if tam:
        ok("8 retratos 3D das tigelas com 1024×1024", len(tam) == 8 and all(t == (1024, 1024) for t in tam), tam)
    grandes = [f for raiz, _, fs in os.walk(PASTA) for f in fs if os.path.getsize(os.path.join(raiz, f)) > 1048576]
    ok("nenhum ficheiro passa de 1 MB (regra das 12:42)", not grandes, grandes)
    v = os.path.join(PASTA, "filme", "filme_manifesto_3d.mp4")
    if os.path.exists(v):
        r = subprocess.run(["/usr/local/bin/ffmpeg", "-hide_banner", "-i", v, "-map", "0:v:0", "-c", "copy", "-f", "framemd5", "-"], capture_output=True, text=True)
        n = sum(1 for x in r.stdout.splitlines() if x and not x.startswith("#"))
        ok("filme 3D: 120 s, 1280×720, 24 imagens por segundo (2880)", n == 2880 and "1280x720" in r.stderr and " 24 fps" in r.stderr, n)


def main():
    os.makedirs(PROVAS, exist_ok=True)
    with sync_playwright() as p:
        b = p.chromium.launch(args=ARGS); versao = b.version
        fluxo(b); linguas(b); biometria(b); b.close()
    estaticos()
    passou = sum(1 for r in R if r.startswith("PASS"))
    with open(os.path.join(PROVAS, "TESTES.txt"), "w", encoding="utf-8", newline="\n") as fh:
        fh.write("Testes do Modo Família 3D (tigelas, tranca de adulto e filme) — 27-11-2026\n")
        fh.write("Navegador: Chromium %s (Playwright), 3D por software (SwiftShader), sem rede. Telemóvel: 390×844.\n\n" % versao)
        fh.write("\n".join(R) + "\n\nResultado: %d de %d PASS\n" % (passou, len(R)))
    print("\n".join(r for r in R if not r.startswith("PASS"))); print("Resultado: %d de %d PASS" % (passou, len(R)))


if __name__ == "__main__":
    main()
