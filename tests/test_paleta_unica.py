"""Portão visual e técnico da paleta única (ordem do David de 27-11-2026, 13:14).

Corre com:
  python3 tests/test_paleta_unica.py                 (raiz do repositório)
  python3 tests/test_paleta_unica.py PACOTE.zip      (também confere a paleta dentro do pacote)

O que prova (cada linha diz PASSA ou FALHA; sai com 1 se alguma falhar):
  A. sem navegador: só cores da paleta (#FF9E7D, #0B192C, #F4F7FA, #9FB3C8, vidro), #f7b397 reformado, um só tema
     escuro, zero emojis de sistema; a marca de revisão jurídica nas 24 línguas dos avisos; o motor KSHA/2 igual
     ao ksha_fluxo.js em todas as páginas que o levam; nacl-util e avisos legais na cache do sw.js v10.
  B. navegador: 13 ficheiros acima de 124 KB conferem no verificador público e no verificador offline
     (SHA-256 igual ao do Python), «CONFERE» em pêssego #FF9E7D sobre azul abissal #0B192C.
  C. navegador: contraste WCAG AAA medido no ecrã de cada página (7:1; 4,5:1 em letra grande);
     memória de cada página abaixo de 64 MB; nenhum erro de página.
"""
import functools
import hashlib
import importlib.util
import os
import random
import re
import sys
import tempfile
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from threading import Thread

RAIZ = Path(__file__).resolve().parents[1]
CHROME = os.environ.get("CHROME", "/usr/bin/google-chrome")
OK, FALHAS = [0], [0]


def carregar(nome):
    spec = importlib.util.spec_from_file_location(nome, RAIZ / "scripts" / (nome + ".py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


paleta = carregar("paleta_unica")
avisos = carregar("avisos_marca_revisao")


def prova(texto, cond, extra=""):
    OK[0] += bool(cond)
    FALHAS[0] += not cond
    print(("PASSA " if cond else "FALHA ") + texto + (" — " + str(extra) if extra != "" else ""), flush=True)


def parte_a(pacote=None):
    print("== A. sem navegador")
    fich, falhas = paleta.verificar(RAIZ)
    prova("raiz: só a paleta oficial, um só tema escuro, zero emojis (%d ficheiros)" % len(fich), not falhas,
          "; ".join(falhas[:5]))
    if pacote:
        fich, falhas = paleta.verificar(pacote)
        prova("pacote: só a paleta oficial, zero emojis (%d ficheiros)" % len(fich), not falhas, "; ".join(falhas[:5]))
    certas, faltam = avisos.verificar_notas((RAIZ / "avisos_legais.html").read_text(encoding="utf-8"))
    prova("avisos legais: marca de revisão jurídica em %d de 24 línguas" % len(certas), len(certas) == 24 and not faltam,
          ", ".join(faltam))
    bloco = re.compile(r"/\* >>> KSHA: inicio \(copia exata de ksha_fluxo\.js\) \*/\n(.*?)\n/\* <<< KSHA: fim \*/", re.S)
    motor = bloco.search((RAIZ / "ksha_fluxo.js").read_text(encoding="utf-8")).group(1)
    copias = []
    for p in sorted(RAIZ.glob("*.html")):
        m = bloco.search(p.read_text(encoding="utf-8"))
        if m:
            copias.append((p.name, m.group(1) == motor))
    prova("motor KSHA/2 igual ao ksha_fluxo.js em %d páginas" % len(copias), len(copias) >= 4 and all(c for _, c in copias),
          ", ".join(n for n, c in copias if not c))
    sw = (RAIZ / "sw.js").read_text(encoding="utf-8")
    prova("sw.js v10 guarda nacl-util e os avisos legais", '"konfirmu-app-unica-v10:"' in sw and "./assets/nacl-util.min.js" in sw
          and "./avisos_legais.html" in sw)
    sem_marca = [p.name for p in RAIZ.glob("*.html") if p.name != "app_unica.html" and paleta.MARCA not in p.read_text(encoding="utf-8")]
    prova("todas as páginas estáticas passaram pela paleta única", not sem_marca, ", ".join(sem_marca))


class Calado(SimpleHTTPRequestHandler):
    def log_message(self, *a):
        pass


def servidor(pasta):
    srv = ThreadingHTTPServer(("127.0.0.1", 0), functools.partial(Calado, directory=str(pasta)))
    Thread(target=srv.serve_forever, daemon=True).start()
    return srv, "http://127.0.0.1:%d/" % srv.server_address[1]


TAMANHOS = [124 * 1024 + 1, 150_000, 200_001, 262_144, 625_000, 1_048_575, 1_048_577, 3_000_000, 8_388_608,
            16_777_215, 16_777_217, 20_000_000, 33_554_433]

AUDITORIA_AAA = r"""() => {
  const lin=v=>{v/=255;return v<=0.04045?v/12.92:Math.pow((v+0.055)/1.055,2.4)};
  const L=c=>0.2126*lin(c[0])+0.7152*lin(c[1])+0.0722*lin(c[2]);
  const ler=s=>{const m=s.match(/rgba?\(([^)]+)\)/);if(!m)return null;const p=m[1].split(/[\s,\/]+/).filter(Boolean).map(Number);return [p[0],p[1],p[2],p.length>3?p[3]:1]};
  const cores=s=>(s.match(/rgba?\([^)]+\)/g)||[]).map(ler).filter(Boolean);
  const sobre=(t,b)=>[t[0]*t[3]+b[0]*(1-t[3]),t[1]*t[3]+b[1]*(1-t[3]),t[2]*t[3]+b[2]*(1-t[3]),1];
  // fundos possíveis por baixo do texto: cor de fundo e cada paragem dos gradientes, do html até ao elemento
  const fundos=el=>{const cad=[];for(let e=el;e;e=e.parentElement)cad.push(e);let cs=[[255,255,255,1]];
    for(const x of cad.reverse()){const st=getComputedStyle(x);const b=ler(st.backgroundColor);if(b&&b[3]>0)cs=cs.map(c=>sobre(b,c));
      if(/gradient/.test(st.backgroundImage)){const ps=cores(st.backgroundImage);if(ps.length){const n=[];for(const c of cs)for(const p of ps)n.push(sobre(p,c));
        const vistos=new Set();cs=n.filter(c=>{const k=c.map(v=>Math.round(v)).join();if(vistos.has(k))return false;vistos.add(k);return true}).slice(0,24)}}}
    return cs};
  const res=[];let pior=99;
  for(const el of document.querySelectorAll('body *')){
    if(['SCRIPT','STYLE','OPTION','NOSCRIPT','TEMPLATE','svg','path'].includes(el.tagName))continue;
    const txt=[...el.childNodes].filter(n=>n.nodeType===3).map(n=>n.textContent).join('').trim();
    if(!txt)continue;
    const r=el.getBoundingClientRect(); if(!r.width||!r.height)continue;
    const cs=getComputedStyle(el); if(cs.visibility==='hidden'||+cs.opacity===0)continue;
    if(el.closest('[hidden],[aria-hidden="true"]'))continue;
    let pintado=false;for(let e=el;e;e=e.parentElement){const st=getComputedStyle(e);if((st.webkitBackgroundClip||st.backgroundClip)==='text'){pintado=true;break}}
    // no SVG a letra pinta-se com fill, não com color
    let cor=(el instanceof SVGElement && cs.fill && cs.fill.startsWith('rgb'))?ler(cs.fill):ler(cs.color); if(!cor)continue;
    if(pintado&&cor[3]===0)continue;
    let k=99;for(const bg of fundos(el)){const c=sobre(cor,bg);const l1=L(c),l2=L(bg);k=Math.min(k,(Math.max(l1,l2)+0.05)/(Math.min(l1,l2)+0.05))}
    const px=parseFloat(cs.fontSize), peso=parseInt(cs.fontWeight)||400;
    const grande=px>=24||(px>=18.66&&peso>=700); const min=grande?4.5:7;
    pior=Math.min(pior,k/min*7);
    if(k<min)res.push(el.tagName.toLowerCase()+(el.id?'#'+el.id:'')+(el.className&&typeof el.className==='string'?'.'+el.className.split(' ')[0]:'')+' '+k.toFixed(2)+':1 «'+txt.slice(0,24)+'»');
  }
  return {falhas:res.slice(0,8),n:res.length,pior:pior};
}"""


def partes_b_c():
    from playwright.sync_api import sync_playwright
    srv, base = servidor(RAIZ)
    tmp = tempfile.TemporaryDirectory()
    rnd = random.Random(20261127)
    ficheiros = []
    for i, n in enumerate(TAMANHOS):
        p = Path(tmp.name) / ("ensaio_%02d.bin" % i)
        p.write_bytes(rnd.randbytes(n))
        ficheiros.append((p, hashlib.sha256(p.read_bytes()).hexdigest()))
    with sync_playwright() as pw:
        nav = pw.chromium.launch(executable_path=CHROME, args=["--no-sandbox", "--use-fake-ui-for-media-stream",
                                                               "--use-fake-device-for-media-stream"])
        ctx = nav.new_context(viewport={"width": 390, "height": 844}, device_scale_factor=2, is_mobile=True,
                              has_touch=True, service_workers="block")
        print("== B. 13 ficheiros acima de 124 KB (%s a %s bytes)" % (TAMANHOS[0], TAMANHOS[-1]))
        pg = ctx.new_page()
        pg.goto(base + "chronolex_verify.html")
        certos, cores = 0, set()
        for p, esperado in ficheiros:
            pg.fill("#hashEsperado", esperado)
            with pg.expect_file_chooser() as fc:
                pg.click("#drop2")
            fc.value.set_files(str(p))
            pg.wait_for_function("() => /CONFERE|DIVERGE|não consegui/.test(document.getElementById('outFile').textContent)",
                                 timeout=120000)
            info = pg.evaluate("""() => {const o=document.getElementById('outFile');return {t:o.textContent,
                c:getComputedStyle(o).color,b:getComputedStyle(document.body).backgroundColor}}""")
            if "CONFERE com o esperado" in info["t"] and esperado in info["t"]:
                certos += 1
            cores.add((info["c"], info["b"]))
        prova("verificador público: %d de 13 ficheiros conferem (SHA-256 igual ao do Python)" % certos, certos == 13)
        prova("«CONFERE» em pêssego sobre azul abissal", cores == {("rgb(255, 158, 125)", "rgb(11, 25, 44)")}, cores)
        pg.close()
        pg = ctx.new_page()
        pg.goto(base + "verificador_offline.html")
        certos = 0
        for p, esperado in ficheiros:
            pg.set_input_files("#f", str(p))
            pg.click("button[onclick^='calc']")
            pg.wait_for_function("(h) => document.getElementById('out').textContent === h", arg=esperado, timeout=120000)
            certos += 1
        prova("verificador offline: %d de 13 ficheiros com o SHA-256 certo" % certos, certos == 13)
        calc = RAIZ / "konfirmu_calc.py"
        h = hashlib.sha256(calc.read_bytes()).hexdigest()
        pg.set_input_files("#f", str(calc))
        pg.click("button[onclick^='calc']")
        pg.wait_for_function("(h) => document.getElementById('out').textContent === h", arg=h, timeout=60000)
        ref = pg.evaluate("""(h) => {const tds=[...document.querySelectorAll('#referencias tr')].filter(tr=>tr.cells[1]&&tr.cells[1].textContent.trim()===h);
            if(!tds.length)return null;const td=tds[0].querySelector('td[id]');return {t:td.textContent,c:getComputedStyle(td).color}}""", h)
        if ref is None:
            print("NOTA  konfirmu_calc.py não está na tabela de referências publicadas (sem «CONFERE» a medir)")
        else:
            prova("referência publicada: «CONFERE» em pêssego", ref["t"] == "CONFERE" and ref["c"] == "rgb(255, 158, 125)", ref)
        pg.close()

        print("== C. contraste AAA, memória e erros, página a página")
        paginas = sorted(p.relative_to(RAIZ).as_posix() for p in RAIZ.glob("*.html"))
        piores = []
        for rel in paginas:
            pg = ctx.new_page()
            erros = []
            pg.on("pageerror", lambda e, erros=erros: erros.append(str(e)[:120]))
            pg.goto(base + rel, wait_until="load")
            pg.wait_for_timeout(300)
            aaa = pg.evaluate(AUDITORIA_AAA)
            cdp = ctx.new_cdp_session(pg)
            cdp.send("Performance.enable")
            met = {m["name"]: m["value"] for m in cdp.send("Performance.getMetrics")["metrics"]}
            mem = met.get("JSHeapUsedSize", 0) / 1024 / 1024
            prova("%s: contraste AAA (%d textos abaixo)" % (rel, aaa["n"]), aaa["n"] == 0, "; ".join(aaa["falhas"]))
            prova("%s: memória %.1f MB (< 64 MB) e 0 erros" % (rel, mem), mem < 64 and not erros, "; ".join(erros))
            piores.append(aaa["pior"])
            pg.close()
        print("contraste: o pior texto de todas as páginas fica a %.2f:1 da régua AAA equivalente" % min(piores))
        nav.close()
    srv.shutdown()
    tmp.cleanup()


def main():
    pacote = sys.argv[1] if len(sys.argv) > 1 else None
    parte_a(pacote)
    partes_b_c()
    print("%d PASSA, %d FALHA" % (OK[0], FALHAS[0]))
    return 1 if FALHAS[0] else 0


if __name__ == "__main__":
    sys.exit(main())
