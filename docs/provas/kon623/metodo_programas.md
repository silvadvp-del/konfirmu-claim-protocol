# Método das medições — os programas usados (KON-623, 27-11-2026)

Correm com Python 3, Playwright e o Chrome do sistema (`/usr/bin/google-chrome`), com `--enable-unsafe-swiftshader --use-angle=swiftshader` (sem GPU).
Servem a pasta num servidor local (127.0.0.1), sem rede para fora. Cada programa vai inteiro, com o SHA-256 do ficheiro original.

## medir_memoria.py

cenário padrão (carregar, 4 s parado, 8 toques, setas, lista de línguas). SHA-256 `a66b924cc6eb21168abbc04abc0870f892e8007d1367f647e7c5ae8e8f84ecc4`

```python
#!/usr/bin/env python3
"""Mede a memória física de pico da página (processo renderer do Chrome), com WebGL.

Uso: python3 -I medir_memoria.py PASTA PAGINA SAIDA.json [cenario]
- Serve PASTA num servidor local (127.0.0.1), abre PAGINA sem rede para fora.
- Perfis: telemóvel (Pixel 7, 412x915, DPR 2,625) e computador (1280x800).
- Amostra a cada 100 ms a memória privada (Private_Dirty), o PSS e o RSS do processo da página (/proc/PID/smaps_rollup)
  e o do processo da GPU; guarda o pico. Limite da casa: memória privada < 64 000 000 bytes.
- Cenário: carregar, esperar 4 s, tocar/rodar o que existir, abrir a lista de línguas, esperar 3 s.
"""
import http.server
import json
import socketserver
import sys
import threading
import time
from pathlib import Path

from playwright.sync_api import sync_playwright

pasta = Path(sys.argv[1]).resolve()
pagina = sys.argv[2]
saida = Path(sys.argv[3])
LIMITE = 64_000_000


def ler_mem(pid):
    try:
        d = {}
        for linha in Path(f"/proc/{pid}/smaps_rollup").read_text().splitlines():
            partes = linha.split()
            if len(partes) >= 2 and partes[0] in ("Rss:", "Pss:", "Private_Dirty:"):
                d[partes[0][:-1]] = int(partes[1]) * 1024
        for linha in Path(f"/proc/{pid}/status").read_text().splitlines():
            if linha.startswith("VmHWM:"):
                d["VmHWM"] = int(linha.split()[1]) * 1024
        return d
    except Exception:
        return None


class Silencioso(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *a, **k):
        super().__init__(*a, directory=str(pasta), **k)

    def log_message(self, *a):
        pass


srv = socketserver.ThreadingTCPServer(("127.0.0.1", 0), Silencioso)
porta = srv.server_address[1]
threading.Thread(target=srv.serve_forever, daemon=True).start()
url = f"http://127.0.0.1:{porta}/{pagina}"

res = {"pasta": str(pasta), "pagina": pagina, "limite_pss_bytes": LIMITE, "perfis": []}
with sync_playwright() as p:
    for nome, opts in [("telemovel", dict(**p.devices["Pixel 7"])),
                       ("computador", dict(viewport={"width": 1280, "height": 800}))]:
        b = p.chromium.launch(executable_path="/usr/bin/google-chrome", args=[
            "--enable-unsafe-swiftshader", "--use-angle=swiftshader", "--ignore-gpu-blocklist",
            "--disable-features=SpareRendererForSitePerProcess", "--no-first-run",
            "--proxy-server=http://127.0.0.1:9", "--proxy-bypass-list=127.0.0.1"])
        bcdp = b.new_browser_cdp_session()
        ctx = b.new_context(**opts)
        pg = ctx.new_page()
        erros, fora = [], []
        pg.on("pageerror", lambda e: erros.append("pageerror: " + str(e)))
        pg.on("console", lambda m: erros.append("console: " + m.text) if m.type == "error" else None)
        pg.on("request", lambda r: fora.append(r.url) if not r.url.startswith((f"http://127.0.0.1:{porta}", "data:", "blob:")) else None)
        picos = {"renderer": {}, "gpu": {}}
        fases = []
        def marca(nome_fase):
            soma = 0
            for pid in list(pids["renderer"]):
                m = ler_mem(pid)
                if m: soma += m.get("Private_Dirty", 0)
            fases.append((nome_fase, round(soma / 1e6, 1), round(picos["renderer"].get("Private_Dirty", 0) / 1e6, 1)))
        parar = threading.Event()
        pids = {"renderer": set(), "gpu": set()}

        def atualizar_pids():
            info = bcdp.send("SystemInfo.getProcessInfo")["processInfo"]
            pids["renderer"] = {x["id"] for x in info if x["type"] == "renderer"}
            pids["gpu"] = {x["id"] for x in info if x["type"] == "GPU"}

        def amostrar():
            while not parar.is_set():
                for tipo in ("renderer", "gpu"):
                    soma = {}
                    for pid in list(pids[tipo]):
                        m = ler_mem(pid)
                        if m:
                            for k, v in m.items():
                                soma[k] = soma.get(k, 0) + v
                    for k, v in soma.items():
                        picos[tipo][k] = max(picos[tipo].get(k, 0), v)
                time.sleep(0.1)

        pg.goto("about:blank")
        atualizar_pids()
        t = threading.Thread(target=amostrar, daemon=True)
        t.start()
        pg.goto(url, wait_until="load")
        atualizar_pids()
        marca("carregou")
        time.sleep(4)
        marca("4s parado")
        webgl = pg.evaluate("() => { try { const c = document.createElement('canvas'); return !!(c.getContext('webgl2') || c.getContext('webgl')); } catch (e) { return false; } }")
        canvases = pg.evaluate("() => document.querySelectorAll('canvas').length")
        # interações: tocar nos primeiros botões visíveis (portais, tigelas, setas), sem sair da página
        tocados = pg.evaluate("""() => {
          const els = [...document.querySelectorAll('button, [role=tab], .tigela, [data-tigela]')]
            .filter(e => e.offsetParent !== null && !/sair|exit|pin|crian|filme|film/i.test(e.textContent + ' ' + (e.id||'') + ' ' + (e.className||'')));
          let n = 0;
          for (const e of els.slice(0, 8)) { try { e.click(); n++; } catch (_) {} }
          return n;
        }""")
        time.sleep(2)
        marca("depois dos toques")
        for _ in range(3):
            pg.keyboard.press("ArrowRight")
            time.sleep(0.4)
        marca("depois das setas")
        sel = pg.query_selector("select, [aria-haspopup=listbox], #lingua, #idioma, .lingua button")
        if sel:
            try:
                sel.click(timeout=1500)
            except Exception:
                pass
        time.sleep(3)
        marca("lista de línguas")
        atualizar_pids()
        time.sleep(1)
        parar.set()
        t.join()
        perfil = {"perfil": nome, "webgl": webgl, "canvases": canvases, "toques": tocados,
                  "fases": fases, "pico_renderer": picos["renderer"], "pico_gpu": picos["gpu"],
                  "erros": erros, "pedidos_para_fora": fora,
                  "passa": picos["renderer"].get("Private_Dirty", 10**12) < LIMITE and not erros and not fora}
        res["perfis"].append(perfil)
        ctx.close()
        b.close()
srv.shutdown()
res["resultado"] = "PASSA" if all(x["passa"] for x in res["perfis"]) else "FALHA"
saida.parent.mkdir(parents=True, exist_ok=True)
saida.write_text(json.dumps(res, ensure_ascii=False, indent=1), encoding="utf-8")
for x in res["perfis"]:
    r, g = x["pico_renderer"], x["pico_gpu"]
    print(f'{pagina:34} {x["perfil"]:10} página privada {r.get("Private_Dirty",0)/1e6:6.1f} MB · PSS {r.get("Pss",0)/1e6:6.1f} MB (RSS {r.get("Rss",0)/1e6:6.1f}, '
          f'pico RSS {r.get("VmHWM",0)/1e6:6.1f}) · GPU PSS {g.get("Pss",0)/1e6:6.1f} MB · webgl {x["webgl"]} · '
          f'telas {x["canvases"]} · toques {x["toques"]} · erros {len(x["erros"])} · fora {len(x["pedidos_para_fora"])}')
    print("    fases (agora, pico):", "; ".join(f"{a} {b}/{c}" for a, b, c in x["fases"]))
    for e in x["erros"][:3]:
        print("   ", e[:160])
print("RESULTADO:", res["resultado"])
```

## curva_longa.py

página parada durante N segundos, amostra a cada 5 s. SHA-256 `89881282934000290e545cacfbdfb9113a16d512afe0ce0fd0fda60e7b8049b0`

```python
#!/usr/bin/env python3
"""Curva longa: memória privada do processo da página a cada 5 s, durante N segundos.

Uso: python3 -I curva_longa.py PASTA PAGINA perfil segundos modo [css_extra] [init_extra]
modo: parado | rato (rato a mexer sempre) | tudo (imersão + rato + separadores em ciclo)
"""
import http.server, socketserver, threading, time, sys
from pathlib import Path
from playwright.sync_api import sync_playwright

pasta = Path(sys.argv[1]); pagina = sys.argv[2]; perfil = sys.argv[3]
segundos = int(sys.argv[4]); modo = sys.argv[5]
css_extra = sys.argv[6] if len(sys.argv) > 6 and sys.argv[6] != "-" else None
init_extra = sys.argv[7] if len(sys.argv) > 7 and sys.argv[7] != "-" else None


class H(http.server.SimpleHTTPRequestHandler):
    def __init__(s, *a, **k): super().__init__(*a, directory=str(pasta), **k)
    def log_message(s, *a): pass


srv = socketserver.ThreadingTCPServer(("127.0.0.1", 0), H); porta = srv.server_address[1]
threading.Thread(target=srv.serve_forever, daemon=True).start()


def priv(pids):
    t = 0
    for pid in pids:
        try:
            for l in Path(f"/proc/{pid}/smaps_rollup").read_text().splitlines():
                if l.startswith("Private_Dirty:"): t += int(l.split()[1]) * 1024
        except Exception: pass
    return t


with sync_playwright() as p:
    b = p.chromium.launch(executable_path="/usr/bin/google-chrome", args=[
        "--enable-unsafe-swiftshader", "--use-angle=swiftshader", "--ignore-gpu-blocklist",
        "--disable-features=SpareRendererForSitePerProcess", "--no-first-run",
        "--proxy-server=http://127.0.0.1:9", "--proxy-bypass-list=127.0.0.1"])
    bc = b.new_browser_cdp_session()
    opts = dict(**p.devices["Pixel 7"]) if perfil == "telemovel" else dict(viewport={"width": 1280, "height": 800})
    ctx = b.new_context(**opts); pg = ctx.new_page()
    if init_extra: pg.add_init_script(Path(init_extra).read_text())
    erros = []
    pg.on("pageerror", lambda e: erros.append(str(e)))
    pg.goto(f"http://127.0.0.1:{porta}/{pagina}", wait_until="load")
    pids = {x["id"] for x in bc.send("SystemInfo.getProcessInfo")["processInfo"] if x["type"] == "renderer"}
    if css_extra: pg.add_style_tag(content=Path(css_extra).read_text())
    w, h = (1280, 800) if perfil == "computador" else (412, 839)
    pg.evaluate("""() => { const t = [...document.querySelectorAll('[role=tab]')].filter(e => e.offsetParent !== null); t.forEach((e, i) => e.setAttribute('data-s', i)); }""")
    if modo == "tudo":
        pg.evaluate("() => document.getElementById('im3d') && document.getElementById('im3d').click()")
    t0 = time.time(); pico = 0; prox = 0; i = 0; linha = []
    while time.time() - t0 < segundos:
        if modo in ("rato", "tudo"):
            pg.mouse.move(w * ((i % 7) + 0.5) / 7, h * ((i % 5) + 0.5) / 5)
        if modo == "tudo" and i % 40 == 0:
            n = (i // 40) % 3
            pg.evaluate(f"() => {{ const e = document.querySelector('[data-s=\"{n}\"]'); if (e) e.click(); }}")
        i += 1
        time.sleep(0.1)
        v = priv(pids); pico = max(pico, v)
        if time.time() - t0 >= prox:
            linha.append(f"{int(time.time() - t0):3d}s {v / 1e6:5.1f}"); prox += 5
    print(f"{pagina} · {perfil} · {modo} · {segundos}s · css={css_extra} · init={init_extra} · erros={len(erros)}")
    print("   " + " | ".join(linha))
    print(f"   PICO {pico / 1e6:.1f} MB")
    b.close()
srv.shutdown()
```

## uso_real.py

passeio contínuo (MOVER=8 PASSEIO=8). SHA-256 `4c165b1197e18dcea7975927b983a7ff3232e4dbffb0971fce5206a141ea3134`

```python
#!/usr/bin/env python3
"""Pico de memória da página em uso real, no Chrome (processo da página: memória privada, Private_Dirty).

Uso: python3 -I uso_real.py PASTA PAGINA SAIDA.json [perfil ...]
Perfis: computador (1280x800, rato) e telemovel (Pixel 7, toque e inclinação contínua do aparelho).
Cenário (cerca de 75 s): carregar e esperar 4 s; percorrer o ecrã; abrir os 3 separadores; ligar a Imersão 3D;
mexer 25 s (rato ou inclinação a 60 Hz com tremor da mão); rolar a página; abrir a lista de línguas;
desligar a imersão; esperar 10 s. Amostra a cada 100 ms. Limite da casa: 64 000 000 bytes.
"""
import http.server, json, math, os, socketserver, sys, threading, time
from pathlib import Path
from playwright.sync_api import sync_playwright

pasta = Path(sys.argv[1]).resolve(); pagina = sys.argv[2]; saida = Path(sys.argv[3])
perfis = sys.argv[4:] or ["telemovel", "computador"]
MOVER = float(os.environ.get("MOVER", "25"))  # segundos de movimento contínuo em imersão
PASSEIO = int(os.environ.get("PASSEIO", "20"))  # pontos do passeio do rato antes da imersão
LIMITE = 64_000_000


class H(http.server.SimpleHTTPRequestHandler):
    def __init__(s, *a, **k): super().__init__(*a, directory=str(pasta), **k)
    def log_message(s, *a): pass


srv = socketserver.ThreadingTCPServer(("127.0.0.1", 0), H); porta = srv.server_address[1]
threading.Thread(target=srv.serve_forever, daemon=True).start()
url = f"http://127.0.0.1:{porta}/{pagina}"


def priv(pids):
    t = 0
    for pid in pids:
        try:
            for l in Path(f"/proc/{pid}/smaps_rollup").read_text().splitlines():
                if l.startswith("Private_Dirty:"): t += int(l.split()[1]) * 1024
        except Exception: pass
    return t


res = {"pagina": pagina, "metodo": "Chrome for Testing: memória privada (Private_Dirty) do processo da página, amostra a cada 100 ms",
       "limite_bytes": LIMITE, "perfis": []}
with sync_playwright() as p:
    for perfil in perfis:
        b = p.chromium.launch(executable_path="/usr/bin/google-chrome", args=[
            "--enable-unsafe-swiftshader", "--use-angle=swiftshader", "--ignore-gpu-blocklist",
            "--disable-features=SpareRendererForSitePerProcess", "--no-first-run",
            "--proxy-server=http://127.0.0.1:9", "--proxy-bypass-list=127.0.0.1"] + (["--enable-low-end-device-mode"] if os.environ.get('GAMA_BAIXA') else []))
        bc = b.new_browser_cdp_session()
        opts = dict(**p.devices["Pixel 7"]) if perfil == "telemovel" else dict(viewport={"width": 1280, "height": 800})
        if os.environ.get('REDUZIR'): opts['reduced_motion'] = 'reduce'
        if os.environ.get('GAMA_BAIXA') and perfil == 'telemovel': pass
        ctx = b.new_context(**opts); pg = ctx.new_page()
        if os.environ.get('INIT'): pg.add_init_script(Path(os.environ['INIT']).read_text())
        erros, fora = [], []
        pg.on("pageerror", lambda e: erros.append("pageerror: " + str(e)))
        pg.on("console", lambda m: erros.append("console: " + m.text) if m.type == "error" else None)
        pg.on("request", lambda r: fora.append(r.url) if not r.url.startswith((f"http://127.0.0.1:{porta}", "data:", "blob:")) else None)
        pg.goto("about:blank")
        pids = set(); pico = [0]; fases = []; parar = threading.Event()

        def amostrar():
            while not parar.is_set():
                pico[0] = max(pico[0], priv(pids)); time.sleep(0.1)

        def marca(nome):
            fases.append([nome, round(priv(pids) / 1e6, 1), round(pico[0] / 1e6, 1)])

        th = threading.Thread(target=amostrar, daemon=True); th.start()
        pg.goto(url, wait_until="load")
        pids |= {x["id"] for x in bc.send("SystemInfo.getProcessInfo")["processInfo"] if x["type"] == "renderer"}
        time.sleep(4); marca("carregou e 4 s parado")
        w, h = opts.get("viewport", {"width": 412, "height": 839}).values() if perfil == "computador" else (412, 839)
        tabs = pg.evaluate("""() => { const t = [...document.querySelectorAll('[role=tab]')].filter(e => e.offsetParent !== null);
            t.forEach((e, i) => e.setAttribute('data-uso', i)); return t.length; }""")
        if perfil == "computador":
            for i in range(PASSEIO):
                pg.mouse.move(w * (0.15 + 0.7 * ((i * 37) % 100) / 100), h * (0.1 + 0.8 * ((i * 53) % 100) / 100), steps=25)
                time.sleep(0.4)
        else:
            for i in range(4):
                pg.evaluate("() => window.scrollBy(0, 300)"); time.sleep(0.6)
            pg.evaluate("() => window.scrollTo(0, 0)"); time.sleep(0.6)
        marca("percorreu o ecrã")
        for i in range(tabs):
            el = pg.query_selector(f'[data-uso="{i}"]')
            if el:
                (el.tap if perfil == "telemovel" else el.click)(); time.sleep(1.5)
        marca(f"abriu {tabs} separadores")
        im = pg.query_selector("#im3d")
        if im:
            (im.tap if perfil == "telemovel" else im.click)(); time.sleep(1)
        marca("Imersão 3D ligada")
        if perfil == "computador":
            fim = time.time() + MOVER; i = 0
            while time.time() < fim:
                pg.mouse.move(w * (0.5 + 0.4 * math.sin(i * 0.7)), h * (0.5 + 0.4 * math.cos(i * 0.45)), steps=20); time.sleep(0.15); i += 1
        else:
            pg.evaluate("""() => new Promise(fim => { const t0 = performance.now(); const id = setInterval(() => {
                const t = (performance.now() - t0) / 1000;
                const beta = 45 + 12 * Math.sin(t * 0.9) + (Math.random() - .5) * .6, gamma = 14 * Math.sin(t * 0.6) + (Math.random() - .5) * .6;
                window.dispatchEvent(new DeviceOrientationEvent('deviceorientation', { alpha: 0, beta, gamma }));
                if (t > %s) { clearInterval(id); fim(); } }, 16); })""" % MOVER)
        marca(f"mexeu {MOVER:g} s em imersão")
        pg.evaluate("() => window.scrollTo(0, document.body.scrollHeight)"); time.sleep(1.2)
        pg.evaluate("() => window.scrollTo(0, 0)"); time.sleep(1.2)
        marca("rolou a página")
        ling = pg.query_selector(".fam-lingua, #lingua, #idioma, .lingua button, [aria-haspopup=listbox]")
        if ling and ling.is_visible():
            try: (ling.tap if perfil == "telemovel" else ling.click)(timeout=1500)
            except Exception: pass
        time.sleep(2); marca("lista de línguas")
        pg.keyboard.press("Escape"); time.sleep(10); marca("10 s parado no fim")
        parar.set(); th.join()
        r = {"perfil": perfil, "pico_bytes": pico[0], "pico_MB": round(pico[0] / 1e6, 1), "fases": fases,
             "erros": erros, "pedidos_para_fora": fora, "passa": pico[0] < LIMITE and not erros and not fora}
        res["perfis"].append(r)
        print(f"{pagina:24} {perfil:10} PICO {r['pico_MB']:5.1f} MB · erros {len(erros)} · fora {len(fora)} · {'PASSA' if r['passa'] else 'FALHA'}")
        print("    " + " | ".join(f"{a} {b_}/{c}" for a, b_, c in fases))
        for e in erros[:3]: print("    ", e[:160])
        ctx.close(); b.close()
srv.shutdown()
res["resultado"] = "PASSA" if all(x["passa"] for x in res["perfis"]) else "FALHA"
saida.parent.mkdir(parents=True, exist_ok=True)
saida.write_text(json.dumps(res, ensure_ascii=False, indent=1), encoding="utf-8")
print("RESULTADO:", res["resultado"])
```

## faisca.html

comparação píxel a píxel da faísca e do anel: Canvas 2D (antes) e WebGL (agora). SHA-256 `92a0f5ca38a8604b6a6e0374af8fc14bb4a903d37585ca59852e7822029d6d6c`

```html
<!doctype html><meta charset="utf-8"><body style="margin:0;background:#000">
<canvas id="a" width="200" height="120"></canvas><canvas id="b" width="200" height="120"></canvas>
<script>
// 2D: o desenho de antes (imagem 64x64 com o degradê, escalada; anel com stroke)
var A=document.getElementById('a'),cx=A.getContext('2d'),fa=document.createElement('canvas');fa.width=fa.height=64;
var g=fa.getContext('2d'),gr=g.createRadialGradient(32,32,0,32,32,32);
gr.addColorStop(0,'rgba(255,158,125,1)');gr.addColorStop(.3,'rgba(255,158,125,.5)');gr.addColorStop(1,'rgba(255,158,125,0)');g.fillStyle=gr;g.fillRect(0,0,64,64);
var casos=[[30,30,19.8,.2],[70,30,12,.12],[110,30,7.2,.2],[150,30,16,.066]];
casos.forEach(function(c){cx.globalAlpha=c[3];cx.drawImage(fa,c[0]-c[2]/2,c[1]-c[2]/2,c[2],c[2])});
cx.globalAlpha=1;cx.beginPath();cx.arc(100,80,30,0,6.2832);cx.strokeStyle='rgba(255,158,125,'+(.3).toFixed(3)+')';cx.lineWidth=1.125;cx.stroke();
// WebGL: o desenho novo (os mesmos shaders do menu)
var B=document.getElementById('b'),pg=B.getContext('webgl',{alpha:true,premultipliedAlpha:true,antialias:false,depth:false,stencil:false,preserveDrawingBuffer:true});
function prog(vsrc,fsrc){var v=pg.createShader(pg.VERTEX_SHADER),f=pg.createShader(pg.FRAGMENT_SHADER),o=pg.createProgram();pg.shaderSource(v,vsrc);pg.compileShader(v);pg.shaderSource(f,fsrc);pg.compileShader(f);pg.attachShader(o,v);pg.attachShader(o,f);pg.bindAttribLocation(o,0,'a');pg.linkProgram(o);return o}
var pP=prog('attribute vec4 a;uniform vec2 r;varying float al;void main(){gl_Position=vec4(a.x/r.x*2.-1.,1.-a.y/r.y*2.,0.,1.);gl_PointSize=a.z;al=a.w;}',
 'precision mediump float;varying float al;void main(){float d=length(gl_PointCoord-.5)*2.;float g=d<.3?1.-d/.3*.5:.5*(1.-d)/.7;float x=max(g,0.)*al;gl_FragColor=vec4(vec3(1.,.6196,.4902)*x,x);}');
var pA=prog('attribute vec2 a;uniform vec2 r;uniform vec3 c;varying vec2 e;varying float rz;void main(){e=a*(c.z+4.);rz=c.z;vec2 p=c.xy+e;gl_Position=vec4(p.x/r.x*2.-1.,1.-p.y/r.y*2.,0.,1.);}',
 '#ifdef GL_FRAGMENT_PRECISION_HIGH\nprecision highp float;\n#else\nprecision mediump float;\n#endif\nuniform vec2 k;varying vec2 e;varying float rz;void main(){float x=clamp(k.y*.5+.5-abs(length(e)-rz),0.,1.)*k.x;gl_FragColor=vec4(vec3(1.,.6196,.4902)*x,x);}');
window.LIGOU=[!!pg.getProgramParameter(pP,pg.LINK_STATUS),!!pg.getProgramParameter(pA,pg.LINK_STATUS)];
var D=new Float32Array(16);casos.forEach(function(c,i){D.set(c,i*4)});
var b1=pg.createBuffer();pg.bindBuffer(pg.ARRAY_BUFFER,b1);pg.bufferData(pg.ARRAY_BUFFER,D,pg.STATIC_DRAW);
pg.enableVertexAttribArray(0);pg.enable(pg.BLEND);pg.blendFunc(pg.ONE,pg.ONE_MINUS_SRC_ALPHA);pg.clearColor(0,0,0,0);pg.viewport(0,0,200,120);pg.clear(pg.COLOR_BUFFER_BIT);
pg.useProgram(pP);pg.uniform2f(pg.getUniformLocation(pP,'r'),200,120);pg.vertexAttribPointer(0,4,pg.FLOAT,false,0,0);pg.drawArrays(pg.POINTS,0,4);
var q=pg.createBuffer();pg.bindBuffer(pg.ARRAY_BUFFER,q);pg.bufferData(pg.ARRAY_BUFFER,new Float32Array([-1,-1,1,-1,-1,1,1,1]),pg.STATIC_DRAW);
pg.useProgram(pA);pg.uniform2f(pg.getUniformLocation(pA,'r'),200,120);pg.uniform3f(pg.getUniformLocation(pA,'c'),100,80,30);pg.uniform2f(pg.getUniformLocation(pA,'k'),.3,1.125);pg.vertexAttribPointer(0,2,pg.FLOAT,false,0,0);pg.drawArrays(pg.TRIANGLE_STRIP,0,4);
// os dois em RGBA pré-multiplicado, linha a linha de cima para baixo
var a=cx.getImageData(0,0,200,120).data,w=new Uint8Array(200*120*4);pg.readPixels(0,0,200,120,pg.RGBA,pg.UNSIGNED_BYTE,w);
var piorP=0,piorA=0,somaA=0,somaB=0;
for(var y=0;y<120;y++)for(var x=0;x<200;x++){var i=(y*200+x)*4,j=((119-y)*200+x)*4;
 var pa=a[i+3]/255,dif=0;for(var ch=0;ch<4;ch++){var va=ch<3?a[i+ch]*pa:a[i+3],vb=w[j+ch];var d=Math.abs(va-vb);if(d>dif)dif=d;if(ch===3){somaA+=va;somaB+=vb}}
 if(y<45){if(dif>piorP)piorP=dif}else{if(dif>piorA)piorA=dif}}
document.title=JSON.stringify({ligou:window.LIGOU,faiscas_pior:+piorP.toFixed(1),anel_pior:+piorA.toFixed(1),alfa_total_2d:Math.round(somaA),alfa_total_webgl:Math.round(somaB)});
</script>
```

## presenca.py

confirma que as faíscas estão no ecrã no menu real. SHA-256 `7da6aa90aeee54e44ef9bad5a735f419a7cd9cb7373980b1087f677296df4175`

```python
"""Faíscas presentes? Duas capturas do céu do menu com 250 ms de intervalo; conta os píxeis que mudaram e os pontos claros."""
import http.server, socketserver, threading, sys, io
from pathlib import Path
from playwright.sync_api import sync_playwright
from PIL import Image, ImageChops
pasta = Path(sys.argv[1]); perfil = sys.argv[2]
class H(http.server.SimpleHTTPRequestHandler):
    def __init__(s, *a, **k): super().__init__(*a, directory=str(pasta), **k)
    def log_message(s, *a): pass
srv = socketserver.ThreadingTCPServer(("127.0.0.1", 0), H); threading.Thread(target=srv.serve_forever, daemon=True).start()
with sync_playwright() as p:
    b = p.chromium.launch(executable_path="/usr/bin/google-chrome", args=["--enable-unsafe-swiftshader", "--use-angle=swiftshader", "--ignore-gpu-blocklist"])
    opts = dict(**p.devices["Pixel 7"]) if perfil == "telemovel" else dict(viewport={"width": 1280, "height": 800})
    ctx = b.new_context(**opts); pg = ctx.new_page(); erros = []
    pg.on("console", lambda m: erros.append(m.text) if m.type == "error" else None); pg.on("pageerror", lambda e: erros.append(str(e)))
    pg.goto(f"http://127.0.0.1:{srv.server_address[1]}/app_unica.html"); pg.wait_for_timeout(2500)
    a = Image.open(io.BytesIO(pg.screenshot())).convert("RGB"); pg.wait_for_timeout(250); c = Image.open(io.BytesIO(pg.screenshot())).convert("RGB")
    d = ImageChops.difference(a, c).convert("L"); mud = sum(1 for v in d.getdata() if v > 6)
    claros = sum(1 for (r, g, bb) in c.getdata() if r > 70 and r > bb + 25 and g > 40)
    print(f"{pasta.parent.parent.name:8s} {perfil:10s} píxeis que mudaram em 250 ms: {mud:6d} · pontos pêssego claros: {claros:6d} · erros: {len(erros)}")
    c.save(f"/home/claude/work/comparar/ceu_{pasta.parent.parent.name}_{perfil}.png"); b.close()
```
