"""Ensaio das tigelas do portal «Educação e família» (diretiva do David de 27-11-2026, 12:29).

Corre com:
  python3 tests/test_tigelas_familia.py                        (sem navegador para o pacote: só a raiz)
  python3 tests/test_tigelas_familia.py PACOTE.zip              (ou a pasta do pacote: as 8 tigelas)
  python3 tests/test_tigelas_familia.py PACOTE.zip --fotos DIR  (guarda fotos de telemóvel e de computador)

O que prova (cada linha diz PASSA ou FALHA; sai com 1 se alguma falhar):
  A. sem navegador: línguas com as mesmas chaves e nada vazio; os menus refazem-se iguais, byte a byte;
     as animações só mexem em transform e opacity; a luz é pêssego (#FF9E7D/#FFB088) no azul #0B192C;
     o sw.js da raiz é a v8 e guarda todas as atividades da família.
  B. a raiz do repositório: 6 tigelas e a entrada; modo avião pelo service worker v8.
  C. o pacote: 8 tigelas com símbolos diferentes; a tigela acende em menos de 100 ms e vibra;
     abre a atividade; ao voltar, fica marcada; teclado e «menos movimento» abrem logo;
     as 62 línguas com <bdi> e direção certa (RTL); procura de línguas e de atividades;
     memória abaixo de 64 MB; ritmo dos quadros; contraste AAA medido em píxeis;
     modo avião (service worker e file://).
"""
import argparse
import base64
import functools
import importlib.util
import json
import os
import re
import shutil
import subprocess
import sys
import time
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from tempfile import TemporaryDirectory
from threading import Thread
from zipfile import ZipFile

RAIZ = Path(__file__).resolve().parents[1]
_spec = importlib.util.spec_from_file_location("tigelas", RAIZ / "scripts" / "tigelas.py")
tigelas = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(tigelas)

TELEMOVEL = dict(viewport={"width": 390, "height": 844}, device_scale_factor=2, is_mobile=True, has_touch=True)
COMPUTADOR = dict(viewport={"width": 1280, "height": 900}, device_scale_factor=1)
LIMITE_MEMORIA = 64 * 1024 * 1024
OK, FALHAS = [0], [0]


def prova(texto, cond, extra=""):
    if cond:
        OK[0] += 1
    else:
        FALHAS[0] += 1
    print(("PASSA " if cond else "FALHA ") + texto + (" — " + str(extra) if extra != "" else ""), flush=True)


class Calado(SimpleHTTPRequestHandler):
    def log_message(self, *args):
        pass


def servidor(pasta):
    srv = ThreadingHTTPServer(("127.0.0.1", 0), functools.partial(Calado, directory=str(pasta)))
    Thread(target=srv.serve_forever, daemon=True).start()
    return srv, "http://127.0.0.1:%d/" % srv.server_port


def hrefs_familia(html):
    i = html.find('id="p-fam"')
    j = html.find("</section>", i)
    return re.findall(r'<a class="card ([^"]*)" href="([^"]+)"', html[i:j])


# ---------------------------------------------------------------- A. sem navegador
def parte_a():
    print("== A. sem navegador")
    linguas = tigelas.ler_linguas(str(RAIZ))  # pára se faltar uma chave, houver uma vazia ou menos de 57
    rtl = sorted(c for c, d in linguas.items() if d["_meta"]["dir"] == "rtl")
    prova("locales/: %d línguas, todas com as mesmas %d chaves e nenhuma vazia" % (len(linguas), len(linguas["pt"]) - 1),
          len(linguas) >= 57)
    prova("línguas da direita para a esquerda marcadas", {"ar", "he", "fa", "ur"} <= set(rtl), ", ".join(rtl))

    with TemporaryDirectory() as tmp:
        copia = Path(tmp) / "repo"
        shutil.copytree(RAIZ, copia, ignore=shutil.ignore_patterns(".git", "__pycache__", "dist"))
        subprocess.run([sys.executable, "-I", str(copia / "scripts" / "gerar_menu.py"), str(copia)],
                       check=True, capture_output=True)
        for f in ("app_unica.html", "edicao-21/app_unica.html", "edicao-21/index.html"):
            prova("o gerador refaz %s igual, byte a byte" % f, (copia / f).read_bytes() == (RAIZ / f).read_bytes())

    css = tigelas.CSS_FAMILIA
    props = set()
    for decl in re.findall(r"transition:([^;}]+)", css):
        for parte in re.sub(r"\([^)]*\)", "", decl).split(","):
            props.add(parte.strip().split()[0])
    prova("as transições só mexem em transform e opacity (fluidas a 60/120 fps)", props <= {"transform", "opacity", "none"},
          ", ".join(sorted(props)))
    quadros = re.findall(r"@keyframes[^{]+\{(.*?\})\s*\}", css, re.S)
    usados = set(re.findall(r"([a-z-]+)\s*:", "".join(quadros)))
    prova("as animações só mexem em transform e opacity", bool(quadros) and usados <= {"transform", "opacity"},
          ", ".join(sorted(usados)))
    svg = "".join(tigelas.svg_tigela(n, *v) for n, v in enumerate(tigelas.TIGELAS.values(), 1))
    prova("a luz de dentro é pêssego #FF9E7D e #FFB088", tigelas.PESSEGO in svg and tigelas.PESSEGO_CLARO in svg)
    prova("o palco é azul abissal #0B192C", "#0B192C" in css)
    simbolos = [v[0] for v in tigelas.TIGELAS.values()]
    prova("8 tigelas, cada uma com o seu símbolo", len(simbolos) == 8 and len(set(simbolos)) == 8, ", ".join(simbolos))

    sw = (RAIZ / "sw.js").read_text(encoding="utf-8")
    prova("sw.js da raiz é a v8 (o início novo chega a quem tinha a v7)", '"konfirmu-app-unica-v8:"' in sw)
    guardados = set(re.findall(r'"\./([^"]+)"', sw.split("const ASSETS", 1)[1].split("];", 1)[0]))
    raiz_fam = [h for _, h in hrefs_familia((RAIZ / "app_unica.html").read_text(encoding="utf-8"))]
    prova("o sw.js v8 guarda as %d atividades da família da raiz" % len(raiz_fam),
          bool(raiz_fam) and set(raiz_fam) <= guardados, ", ".join(sorted(set(raiz_fam) - guardados)))
    return linguas


# ---------------------------------------------------------------- ajudas do navegador
class Erros:
    """Erros da página do menu (as atividades abertas pelo caminho não contam aqui)."""

    def __init__(self):
        self.lista = []

    def ligar(self, page):
        page.on("pageerror", lambda e: self.lista.append((page.url, str(e))))
        page.on("console", lambda m: m.type == "error" and self.lista.append((page.url, m.text)))

    def do_menu(self):
        return [t for u, t in self.lista if u.split("?")[0].endswith(("app_unica.html", "index.html"))]


def abrir_familia(page, url):
    page.goto(url)
    page.click("#t-fam")
    page.wait_for_selector("#p-fam:not([hidden])")


def esperar(page, expressao, segundos=10):
    fim = time.monotonic() + segundos
    while time.monotonic() < fim:
        if page.evaluate(expressao):
            return True
        time.sleep(0.05)
    return False


SW_PRONTO = "Promise.race([navigator.serviceWorker.ready.then(r=>!!r.active),new Promise(r=>setTimeout(()=>r(false),20000))])"
VIBRA = "Navigator.prototype.vibrate=function(p){try{window.__vibrou(p)}catch(e){}return true};"


# ---------------------------------------------------------------- contraste AAA medido em píxeis
# Ordem do David de 27-11, 12:16 (artigo 2.º, n.º 3): nenhum ecrã passa sem contraste WCAG AAA.
# Mede cada linha de texto do portal: esconde o texto, fotografa o fundo e compara a cor do texto
# com o píxel de fundo mais desfavorável dessa linha (7:1; 4,5:1 para letra grande).
RECOLHER_TEXTOS = r"""()=>{const sec=document.getElementById('p-fam');const out=[];
 const w=document.createTreeWalker(sec,NodeFilter.SHOW_TEXT);let n;
 while((n=w.nextNode())){if(!n.textContent.trim())continue;const el=n.parentElement;
  if(el.closest('[hidden]')||el.closest('svg'))continue;const cs=getComputedStyle(el);
  if(cs.visibility==='hidden'||+cs.opacity===0)continue;const r=document.createRange();r.selectNodeContents(n);
  let cl={l:-1e9,t:-1e9,r:1e9,b:1e9};for(let a=el;a&&a!==document.body;a=a.parentElement){const o=getComputedStyle(a);
   if(o.overflowX!=='visible'||o.overflowY!=='visible'){const z=a.getBoundingClientRect(),zl=z.left+a.clientLeft,zt=z.top+a.clientTop;
    cl={l:Math.max(cl.l,zl),t:Math.max(cl.t,zt),r:Math.min(cl.r,zl+a.clientWidth),b:Math.min(cl.b,zt+a.clientHeight)}}}
  for(const q0 of r.getClientRects()){const q={l:Math.max(q0.left,cl.l),t:Math.max(q0.top,cl.t),r:Math.min(q0.right,cl.r),b:Math.min(q0.bottom,cl.b)};
   if(q.r-q.l<2||q.b-q.t<2)continue;
   out.push({t:n.textContent.trim().slice(0,40),cor:cs.color,px:parseFloat(cs.fontSize),peso:+cs.fontWeight,x:q.l+scrollX,y:q.t+scrollY,w:q.r-q.l,h:q.b-q.t})}}
 for(const i of sec.querySelectorAll('input')){if(i.closest('[hidden]')||i.value)continue;const q=i.getBoundingClientRect(),p=parseFloat(getComputedStyle(i).paddingLeft);
  out.push({t:'(placeholder) '+i.placeholder,cor:getComputedStyle(i,'::placeholder').color,px:parseFloat(getComputedStyle(i).fontSize),peso:400,
   x:q.left+scrollX+p,y:q.top+scrollY+8,w:Math.min(q.width-2*p,200),h:q.height-16})}
 return out}"""
ESCONDER_TEXTO = ("#p-fam *,#p-fam *::placeholder{color:transparent!important;-webkit-text-fill-color:transparent!important;"
                  "text-shadow:none!important;caret-color:transparent!important}")
MEDIR_PIXEIS = r"""async([png,caixas,esc])=>{const img=new Image();img.src='data:image/png;base64,'+png;await img.decode();
 const c=document.createElement('canvas');c.width=img.width;c.height=img.height;const g=c.getContext('2d');g.drawImage(img,0,0);
 const lin=v=>{v/=255;return v<=.04045?v/12.92:Math.pow((v+.055)/1.055,2.4)};const L=(r,gg,b)=>.2126*lin(r)+.7152*lin(gg)+.0722*lin(b);
 return caixas.map(k=>{const x=Math.max(0,Math.floor(k.x*esc)),y=Math.max(0,Math.floor(k.y*esc));
  const w=Math.max(1,Math.min(Math.floor(k.w*esc),img.width-x)),h=Math.max(1,Math.min(Math.floor(k.h*esc),img.height-y));
  const d=g.getImageData(x,y,w,h).data;let mn=1,mx=0,s=0,n=0;
  for(let i=0;i<d.length;i+=4){const l=L(d[i],d[i+1],d[i+2]);if(l<mn)mn=l;if(l>mx)mx=l;s+=l;n++}
  const m=k.cor.match(/[\d.]+/g).map(Number);const lt=L(m[0],m[1],m[2]);const claro=lt>s/n;const pior=claro?mx:mn;
  const ratio=claro?(lt+.05)/(pior+.05):(pior+.05)/(lt+.05);const grande=k.px>=24||(k.px>=18.66&&k.peso>=700);
  return {t:k.t,cor:k.cor,ratio:Math.round(ratio*100)/100,min:grande?4.5:7}})}"""


def contraste_aaa(browser, url):
    """Mede todo o texto do portal (telemóvel e computador; lista de línguas fechada e aberta; uma tigela escolhida)."""
    res = []
    for nome, opc in (("telemóvel", TELEMOVEL), ("computador", COMPUTADOR)):
        ctx = browser.new_context(**opc)
        page = ctx.new_page()
        page.goto(url)
        page.evaluate("sessionStorage.setItem('konfirmu_tigela','sala_natal_girafinhas.html')")
        page.reload()
        abrir_familia(page, url)
        time.sleep(0.4)
        for estado in ("fechada", "aberta"):
            if estado == "aberta":
                page.click("#famLingua")
                page.click('#famLinguaLista button[data-l="kea"]')
                page.click("#famLingua")
                time.sleep(0.2)
            caixas = page.evaluate(RECOLHER_TEXTOS)
            estilo = page.add_style_tag(content=ESCONDER_TEXTO)
            time.sleep(0.1)
            png = base64.b64encode(page.screenshot(full_page=True)).decode()
            page.evaluate("s=>s.remove()", estilo)
            folha = ctx.new_page()
            for x in folha.evaluate(MEDIR_PIXEIS, [png, caixas, opc["device_scale_factor"]]):
                x["onde"] = "%s, lista de línguas %s" % (nome, estado)
                res.append(x)
            folha.close()
        ctx.close()
    return res


# ---------------------------------------------------------------- B. a raiz do repositório
def parte_b(pw, chrome):
    print("== B. raiz do repositório (6 tigelas, sw.js v8)")
    srv, base = servidor(RAIZ)
    browser = pw.chromium.launch(executable_path=chrome)
    try:
        ctx = browser.new_context(**TELEMOVEL)
        page = ctx.new_page()
        erros = Erros()
        erros.ligar(page)
        abrir_familia(page, base + "app_unica.html")
        cartoes = page.eval_on_selector_all("#p-fam a.card", "as=>as.map(a=>[a.className,a.getAttribute('href')])")
        tig = [h for c, h in cartoes if "tigela" in c]
        prova("raiz: a entrada e 6 tigelas (o Tutor e o Quiz só vêm na edição de 21)",
              len(tig) == 6 and sum("entrada" in c for c, _ in cartoes) == 1
              and "Tutor-Girafinha-offline.html" not in tig and "kcp_family_quiz.html" not in tig, len(tig))
        pronto = page.evaluate(SW_PRONTO)
        page.reload()
        page.wait_for_function("navigator.serviceWorker.controller!==null")
        chaves = page.evaluate("caches.keys()")
        prova("raiz: o service worker v8 está ativo e manda na página", pronto and any(k.startswith("konfirmu-app-unica-v8:") for k in chaves),
              ", ".join(chaves))
        ctx.set_offline(True)
        abrir_familia(page, base + "app_unica.html")
        n = page.eval_on_selector_all("#p-fam a.card.tigela", "as=>as.length")
        faltam = page.evaluate("async hs=>{const f=[];for(const h of hs){if(!(await caches.match(h)))f.push(h)}return f}",
                               [h for _, h in cartoes])
        prova("raiz em modo avião: o início abre com as 6 tigelas e as 7 atividades estão guardadas", n == 6 and not faltam,
              ", ".join(faltam))
        with page.expect_navigation(wait_until="load"):
            page.tap("#p-fam a.card.tigela >> nth=0")
        prova("raiz em modo avião: tocar numa tigela abre a atividade", page.url.endswith(tig[0]), page.url)
        ctx.set_offline(False)
        prova("raiz: 0 erros na consola do início", not erros.do_menu(), " | ".join(erros.do_menu()[:3]))
    finally:
        browser.close()
        srv.shutdown()


# ---------------------------------------------------------------- C. o pacote
def pasta_do_pacote(alvo, tmp):
    alvo = Path(alvo)
    if alvo.is_file():
        with ZipFile(alvo) as z:
            z.extractall(tmp)
        alvo = Path(tmp)
    return next(p.parent for p in sorted(alvo.rglob("app_unica.html")))


def parte_c(pw, chrome, pasta, linguas, fotos):
    print("== C. pacote (%s)" % pasta.name)
    srv, base = servidor(pasta)
    url = base + "app_unica.html"
    browser = pw.chromium.launch(executable_path=chrome)
    vibrou = []
    try:
        ctx = browser.new_context(**TELEMOVEL)
        ctx.expose_binding("__vibrou", lambda origem, p: vibrou.append(p))
        ctx.add_init_script(VIBRA)
        page = ctx.new_page()
        erros = Erros()
        erros.ligar(page)
        abrir_familia(page, url)

        info = page.evaluate("""()=>{
          const tg=[...document.querySelectorAll('#p-fam a.card.tigela')];
          const simb=tg.map(a=>{const g=a.querySelector('svg.tg g[transform^="translate(46"]');return g?g.lastElementChild.innerHTML:''});
          const luz=tg.map(a=>[...a.querySelectorAll('radialGradient[id$="l"] stop')].map(s=>s.getAttribute('stop-color')).join());
          const palco=getComputedStyle(document.getElementById('p-fam')).backgroundColor;
          return {n:tg.length, entrada:document.querySelectorAll('#p-fam a.card.entrada').length, simb:new Set(simb).size,
                  vazios:simb.filter(s=>!s).length, luz:luz.every(l=>l.includes('#FFB088')&&l.includes('#FF9E7D')), palco,
                  alvo:tg.map(a=>{const r=a.getBoundingClientRect();return Math.min(r.width,r.height)})}}""")
        prova("pacote: a entrada e 8 tigelas", info["n"] == 8 and info["entrada"] == 1, info["n"])
        prova("pacote: 8 símbolos diferentes, um em cada tigela", info["simb"] == 8 and info["vazios"] == 0, info["simb"])
        prova("pacote: a luz de cada tigela é pêssego #FF9E7D/#FFB088", info["luz"])
        prova("pacote: o palco é azul abissal (rgb 11 25 44)", "11, 25, 44" in info["palco"], info["palco"])
        prova("pacote: cada tigela é um alvo de toque com 44 px ou mais", min(info["alvo"]) >= 44, round(min(info["alvo"])))

        resp = page.evaluate("""()=>new Promise(ok=>{
          const a=document.querySelectorAll('#p-fam a.card.tigela')[2];const t0=performance.now();
          a.dispatchEvent(new PointerEvent('pointerdown',{bubbles:true,pointerType:'touch',isPrimary:true,button:0}));
          const ja=a.classList.contains('acesa');
          requestAnimationFrame(()=>requestAnimationFrame(()=>ok({ja,ms:performance.now()-t0,
            luz:+getComputedStyle(a.querySelector('.tg-luz')).opacity})));})""")
        prova("pacote: ao tocar, a tigela acende no mesmo instante e já se vê no 2.º quadro (< 100 ms)",
              resp["ja"] and resp["ms"] < 100 and resp["luz"] > 0, "%.1f ms" % resp["ms"])
        time.sleep(0.35)
        fim = page.evaluate("""()=>{const a=document.querySelectorAll('#p-fam a.card.tigela')[2];
          const st=s=>getComputedStyle(a.querySelector(s));
          return {luz:+st('.tg-luz').opacity,faisca:+st('.tg-faiscas').opacity,coluna:+getComputedStyle(a.querySelector('.ico'),'::before').opacity,
                  outras:document.querySelectorAll('#p-fam a.card.acesa').length}}""")
        prova("pacote: acesa = luz por dentro, coluna de luz e faíscas; só uma de cada vez",
              fim["luz"] == 1 and fim["faisca"] == 1 and fim["coluna"] == 1 and fim["outras"] == 1, fim)

        ritmo = page.evaluate("""()=>new Promise(ok=>{const t=[];function f(x){t.push(x);if(t.length<121)requestAnimationFrame(f);
          else{const d=t.slice(1).map((v,i)=>v-t[i]).sort((a,b)=>a-b);ok({p50:d[d.length>>1],p95:d[Math.floor(d.length*.95)]})}}
          requestAnimationFrame(f)})""")
        prova("pacote: ritmo dos quadros com a tigela acesa (mediana até 20 ms, ou seja 50 fps ou mais)", ritmo["p50"] <= 20,
              "mediana %.1f ms, p95 %.1f ms" % (ritmo["p50"], ritmo["p95"]))

        # tocar: vibra, mostra a luz e abre a atividade
        alvo = page.get_attribute("#p-fam a.card.tigela >> nth=2", "href")
        antes = len(vibrou)
        t0 = time.monotonic()
        with page.expect_navigation(wait_until="commit"):
            page.tap("#p-fam a.card.tigela >> nth=2")
        dt = time.monotonic() - t0
        prova("pacote: o toque vibra (12 ms) e abre a atividade depois de mostrar a luz",
              vibrou[antes:] == [12] and page.url.endswith(alvo) and dt >= 0.18, "%s em %.2f s" % (vibrou[antes:], dt))
        page.wait_for_load_state("load")
        page.go_back(wait_until="load")
        page.wait_for_selector("#p-fam a.card.tigela", state="attached")
        volta = page.evaluate("""h=>({esc:[...document.querySelectorAll('#p-fam a.card.escolhida')].map(a=>a.getAttribute('href')),
          acesas:document.querySelectorAll('#p-fam a.card.acesa').length})""", alvo)
        prova("pacote: ao voltar, nenhuma acesa e a escolhida fica marcada", volta["esc"] == [alvo] and volta["acesas"] == 0, volta)

        # teclado: Tab até à 1.ª tigela acende por dentro; Enter abre logo, sem vibrar
        abrir_familia(page, url)
        page.focus("#famLingua")
        page.keyboard.press("Tab")
        page.keyboard.press("Tab")
        time.sleep(0.3)
        foco = page.evaluate("""()=>{const a=document.activeElement;return {tig:a.matches('#p-fam a.card.tigela'),fv:a.matches(':focus-visible'),
          luz:+getComputedStyle(a.querySelector('.tg-luz')).opacity,href:a.getAttribute('href')}}""")
        prova("pacote: escolher com o teclado acende a tigela por dentro", foco["tig"] and foco["fv"] and foco["luz"] >= 0.75, foco)
        antes = len(vibrou)
        t0 = time.monotonic()
        with page.expect_navigation(wait_until="commit"):
            page.keyboard.press("Enter")
        prova("pacote: Enter abre logo e não vibra", page.url.endswith(foco["href"]) and vibrou[antes:] == [],
              "%.2f s" % (time.monotonic() - t0))

        # as 62 línguas: textos certos, <bdi>, direção e língua
        abrir_familia(page, url)
        esperado = {c: {k: v for k, v in d.items() if k != "_meta"} for c, d in linguas.items()}
        dirs = {c: d["_meta"]["dir"] for c, d in linguas.items()}
        res = page.evaluate("""([esp,dirs])=>{const mal=[];let lento=0;const sec=document.getElementById('p-fam');
          for(const c of Object.keys(esp)){const t0=performance.now();KFAM.aplicar(c);lento=Math.max(lento,performance.now()-t0);
            if(sec.lang!==c||sec.dir!==dirs[c])mal.push(c+': lang/dir');
            for(const el of document.querySelectorAll('[data-k]')){const k=el.dataset.k;
              if(el.tagName!=='BDI')mal.push(c+': '+k+' sem bdi');if(el.textContent!==esp[c][k])mal.push(c+': '+k)}
            for(const el of document.querySelectorAll('[data-kp]'))if(el.placeholder!==esp[c][el.dataset.kp])mal.push(c+': '+el.dataset.kp);}
          KFAM.aplicar('pt');return {mal,lento,n:KFAM.linguas()}}""", [esperado, dirs])
        prova("pacote: as %d línguas mudam todos os textos, cada um num <bdi>, com a direção certa" % res["n"],
              not res["mal"] and res["n"] == len(linguas), "; ".join(res["mal"][:5]))
        prova("pacote: mudar de língua responde em menos de 100 ms", res["lento"] < 100, "pior %.1f ms" % res["lento"])

        page.click("#famLingua")
        page.fill("#famLinguaProcura", "crioulo")
        vistos = page.eval_on_selector_all("#famLinguaLista li:not([hidden]) button", "bs=>bs.map(b=>b.dataset.l)")
        prova("pacote: procurar «crioulo» na lista de línguas encontra o cabo-verdiano e o da Guiné", {"kea", "pov"} <= set(vistos),
              ", ".join(vistos))
        page.fill("#famLinguaProcura", "")
        page.click('#famLinguaLista button[data-l="ar"]')
        page.reload()
        page.click("#t-fam")
        rtl = page.evaluate("""()=>{const s=document.getElementById('p-fam');return {lang:s.lang,dir:s.dir,
          painel:document.getElementById('famLinguas').hidden,guardada:localStorage.getItem('konfirmu_lingua_familia'),
          tab:document.querySelector('#t-fam bdi').dir}}""")
        prova("pacote: a língua escolhida (árabe) fica guardada e volta da direita para a esquerda",
              rtl == {"lang": "ar", "dir": "rtl", "painel": True, "guardada": "ar", "tab": "rtl"}, rtl)
        if fotos:
            page.mouse.move(1, 1)  # o ponteiro de ensaio fora dos cartões (num telemóvel não há ponteiro)
            time.sleep(0.4)
            page.locator("#p-fam").screenshot(path=str(fotos / "telemovel_arabe.png"))
        page.evaluate("KFAM.aplicar('pt')")

        page.fill("#procura", "natal")
        proc = page.evaluate("""()=>({fam:[...document.querySelectorAll('#p-fam a.card')].filter(a=>a.offsetParent).map(a=>a.getAttribute('href')),
          sec:!document.getElementById('p-fam').hidden})""")
        prova("pacote: a procura de atividades encontra a tigela do Natal e esconde as outras", proc["sec"] and proc["fam"] == ["sala_natal_girafinhas.html"],
              proc["fam"])
        page.fill("#procura", "")

        cdp = ctx.new_cdp_session(page)
        cdp.send("Performance.enable")
        cdp.send("HeapProfiler.collectGarbage")
        m = {x["name"]: x["value"] for x in cdp.send("Performance.getMetrics")["metrics"]}
        prova("pacote: memória da página abaixo de 64 MB (depois das 62 línguas)", m["JSHeapTotalSize"] < LIMITE_MEMORIA,
              "usada %.1f MB, reservada %.1f MB" % (m["JSHeapUsedSize"] / 2**20, m["JSHeapTotalSize"] / 2**20))

        # modo avião com o service worker do pacote
        page.goto(url)
        prova("pacote: o service worker do pacote fica ativo", page.evaluate(SW_PRONTO))
        page.reload()
        page.wait_for_function("navigator.serviceWorker.controller!==null")
        hrefs = page.eval_on_selector_all("#p-fam a.card", "as=>as.map(a=>a.getAttribute('href'))")
        ctx.set_offline(True)
        abrir_familia(page, url)
        faltam = page.evaluate("async hs=>{const f=[];for(const h of hs){if(!(await caches.match(h)))f.push(h)}return f}", hrefs)
        n = page.eval_on_selector_all("#p-fam a.card.tigela", "as=>as.length")
        prova("pacote em modo avião: o início abre com as 8 tigelas e as 9 atividades estão guardadas", n == 8 and not faltam and len(hrefs) == 9,
              ", ".join(faltam))
        with page.expect_navigation(wait_until="load"):
            page.tap("#p-fam a.card.tigela >> nth=7")
        prova("pacote em modo avião: tocar numa tigela abre a atividade", page.url.endswith(hrefs[-1]), page.url)
        ctx.set_offline(False)
        prova("pacote: 0 erros na consola do início (telemóvel)", not erros.do_menu(), " | ".join(erros.do_menu()[:3]))
        ctx.close()

        # menos movimento: sem transições e abre logo, sem vibrar
        ctx = browser.new_context(reduced_motion="reduce", **TELEMOVEL)
        ctx.expose_binding("__vibrou", lambda origem, p: vibrou.append(p))
        ctx.add_init_script(VIBRA)
        page = ctx.new_page()
        abrir_familia(page, url)
        rm = page.evaluate("""()=>{const a=document.querySelector('#p-fam a.card.tigela');
          return {tr:getComputedStyle(a.querySelector('.tg-luz')).transitionDuration,fa:getComputedStyle(a.querySelector('.tg-faiscas')).display}}""")
        antes = len(vibrou)
        with page.expect_navigation(wait_until="commit"):
            page.tap("#p-fam a.card.tigela >> nth=0")
        prova("pacote, «menos movimento»: sem transições nem faíscas, abre logo e não vibra",
              rm == {"tr": "0s", "fa": "none"} and vibrou[antes:] == [], rm)
        ctx.close()

        # computador e fotos
        ctx = browser.new_context(**COMPUTADOR)
        page = ctx.new_page()
        erros2 = Erros()
        erros2.ligar(page)
        abrir_familia(page, url)
        colunas = page.evaluate("getComputedStyle(document.querySelector('#p-fam .grid')).gridTemplateColumns.split(' ').length")
        prova("pacote no computador: 4 tigelas por linha", colunas == 4, colunas)
        if fotos:
            page.mouse.move(1, 1)
            time.sleep(0.4)  # o portal aparece em 0,16 s
            page.screenshot(path=str(fotos / "computador.png"))
            page.locator("#p-fam").screenshot(path=str(fotos / "computador_familia.png"))
            ctx2 = browser.new_context(**TELEMOVEL)
            p2 = ctx2.new_page()
            abrir_familia(p2, url)
            p2.mouse.move(1, 1)
            time.sleep(0.4)
            p2.locator("#p-fam").screenshot(path=str(fotos / "telemovel_familia.png"))
            p2.dispatch_event("#p-fam a.card.tigela >> nth=2", "pointerdown")
            time.sleep(0.45)
            p2.locator("#p-fam a.card.tigela >> nth=2").screenshot(path=str(fotos / "telemovel_tigela_acesa.png"))
            ctx2.close()
        prova("pacote: 0 erros na consola do início (computador)", not erros2.do_menu(), " | ".join(erros2.do_menu()[:3]))
        ctx.close()

        medidas = contraste_aaa(browser, url)
        maus = sorted((x for x in medidas if x["ratio"] < x["min"]), key=lambda x: x["ratio"])
        prova("pacote: contraste AAA em todo o texto do portal (%d linhas medidas em píxeis, telemóvel e computador)" % len(medidas),
              len(medidas) > 100 and not maus,
              "pior %.2f:1" % min(x["ratio"] for x in medidas) if not maus else "; ".join("%.2f %s «%s»" % (x["ratio"], x["onde"], x["t"]) for x in maus[:4]))

        # file:// — abrir o ficheiro diretamente, sem servidor nem service worker
        ctx = browser.new_context(**TELEMOVEL)
        page = ctx.new_page()
        erros3 = Erros()
        erros3.ligar(page)
        abrir_familia(page, (pasta / "app_unica.html").as_uri())
        fl = page.evaluate("()=>{KFAM.aplicar('he');const s=document.getElementById('p-fam');const r={n:document.querySelectorAll('#p-fam a.card.tigela').length,dir:s.dir};KFAM.aplicar('pt');return r}")
        with page.expect_navigation(wait_until="load"):
            page.tap("#p-fam a.card.tigela >> nth=4")
        prova("pacote por file://: 8 tigelas, hebraico da direita para a esquerda, a tigela abre a atividade, 0 erros",
              fl == {"n": 8, "dir": "rtl"} and page.url.startswith("file://") and not erros3.do_menu(),
              "%s %s" % (fl, " | ".join(erros3.do_menu()[:2])))
        ctx.close()
    finally:
        browser.close()
        srv.shutdown()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("pacote", nargs="?", help="ZIP ou pasta do pacote offline (edição de 21)")
    ap.add_argument("--fotos", help="pasta onde guardar as fotos de telemóvel e de computador")
    a = ap.parse_args()
    linguas = parte_a()
    from playwright.sync_api import sync_playwright

    chrome = os.environ.get("CHROME", "/usr/bin/google-chrome")
    fotos = Path(a.fotos) if a.fotos else None
    if fotos:
        fotos.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as pw:
        parte_b(pw, chrome)
        if a.pacote:
            with TemporaryDirectory() as tmp:
                parte_c(pw, chrome, pasta_do_pacote(a.pacote, tmp), linguas, fotos)
    print("\n%d PASSA, %d FALHA" % (OK[0], FALHAS[0]))
    sys.exit(1 if FALHAS[0] else 0)


if __name__ == "__main__":
    main()
