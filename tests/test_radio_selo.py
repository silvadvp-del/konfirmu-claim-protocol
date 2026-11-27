"""Ensaio da Rádio com Prova (radio_selo.html): a trama de 128 bits chega inteira ou não chega.

Corre com:
  python3 tests/test_radio_selo.py                    (raiz do repositório)
  python3 tests/test_radio_selo.py --antigo FICHEIRO  (junta a prova negativa com a versão antiga da página)

O que prova (cada linha diz PASSA ou FALHA; sai com 1 se alguma falhar):
  A. sem navegador: os tons e o formato não mudam (1200/2200 Hz, 50 bits/s, sincronia 10101010, 128 bits);
     o recetor lê a taxa real do aparelho; a escuta dura pelo menos 4,0 s; o microfone vai sem filtros de voz;
     o sw.js leva a página nova a quem já a tinha guardada.
  B. no Chrome, com o código da própria página: o SHA-256 confere com o Python; a trama é lida a 8 kHz,
     11,025, 16, 22,05, 44,1, 48 e 96 kHz, com ruído, contínua e zumbido; emissor e recetor com taxas diferentes;
     uma trama cortada é recusada sem hash; uma gravação que acaba a meio fica «em curso»; ruído sozinho nunca dá hash;
     com ruído forte pode falhar, mas nunca dá um hash errado.
  C. no Chrome, com um microfone simulado (ficheiro WAV a 48 kHz, feito aqui em Python, à parte da página):
     KON-A1 e KON-B2 chegam com os 32 caracteres certos; uma trama cortada a meio diz «incompleta» e não mostra hash.
     Com --antigo, a página antiga ouve o mesmo ficheiro e não chega ao hash certo (prova negativa).
"""
import argparse
import functools
import hashlib
import math
import os
import re
import shutil
import struct
import sys
import time
import wave
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from tempfile import TemporaryDirectory
from threading import Thread

RAIZ = Path(__file__).resolve().parents[1]
PAGINA = "radio_selo.html"
OK, FALHAS = [0], [0]
MENSAGENS = ["KON-A1", "KON-B2", "PONTO DE ÁGUA ABERTO ÀS 9H"]


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


def hash32(texto):
    return hashlib.sha256(texto.encode("utf-8")).hexdigest()[:32]


# ---------------------------------------------------------------- A. sem navegador
def parte_a():
    print("== A. formato, taxa real, janela e cache")
    html = (RAIZ / PAGINA).read_text(encoding="utf-8")
    prova("os tons não mudam: 1200/2200 Hz a 50 bits/s", "var F0 = 1200, F1 = 2200;" in html and "BAUDS = 50" in html)
    prova("a trama não muda: sincronia 10101010 e 128 bits", 'PREAMBULO = "10101010", BITS_DADOS = 128' in html)
    m = re.search(r"var ESCUTA_MAX_S = (\d+(?:\.\d+)?);", html)
    prova("a escuta dura pelo menos 4,0 s", bool(m) and float(m.group(1)) >= 4.0, m.group(1) if m else "sem ESCUTA_MAX_S")
    ouvir = html[html.index("function ouvir()"):html.index("</script>", html.index("function ouvir()"))]
    prova("o recetor lê a taxa real do aparelho (ctx.sampleRate)", "var sr = ctx.sampleRate" in ouvir and "procurarTrama(s, sr" in ouvir)
    prova("o recetor já não usa a taxa fixa de 8 kHz", re.search(r"\bSR\b", ouvir) is None)
    emitir = html[html.index("function emitir()"):html.index("var escuta")]
    prova("o emissor gera os tons à taxa real do aparelho", "sr = ctx.sampleRate" in emitir and "fskEncode(hash, sr)" in emitir)
    prova("o microfone vai sem filtros de voz (eco, ruído, ganho)",
          "echoCancellation:false" in ouvir and "noiseSuppression:false" in ouvir and "autoGainControl:false" in ouvir)
    prova("sem hash parcial: a página só mostra «hash recebido» com a trama completa",
          ouvir.count("hash recebido") == 1 and 'r.estado === "ok"' in ouvir)
    prova("a página já não diz que o som reconstrói a mensagem", "reconstrói a mensagem" not in html)
    sw = (RAIZ / "sw.js").read_text(encoding="utf-8")
    prova("o sw.js é a v10 e guarda esta página", '"konfirmu-app-unica-v10:"' in sw and '"./radio_selo.html"' in sw)


# ---------------------------------------------------------------- B. código da página, no Chrome
ENSAIO_JS = r"""
(cfg) => {
  function prng(seed){ let a = seed >>> 0; return () => { a = (a + 0x6D2B79F5) >>> 0; let t = a; t = Math.imul(t ^ (t >>> 15), t | 1); t ^= t + Math.imul(t ^ (t >>> 7), t | 61); return ((t ^ (t >>> 14)) >>> 0) / 4294967296; }; }
  function gauss(r){ let u = 0, v = 0; while(u === 0) u = r(); while(v === 0) v = r(); return Math.sqrt(-2*Math.log(u))*Math.cos(2*Math.PI*v); }
  function captura(hex, srOuve, r, o){
    o = o || {}; const srEmite = o.srEmite || srOuve; let tons = fskEncode(hex, srEmite).amostras;
    if(srEmite !== srOuve){ const n = Math.floor(tons.length*srOuve/srEmite), x = new Float32Array(n);
      for(let i=0;i<n;i++){ const p = i*srEmite/srOuve, k = Math.floor(p), f = p-k; x[i] = (tons[k]||0)*(1-f) + (tons[k+1]||0)*f; } tons = x; }
    if(o.cortar != null) tons = tons.subarray(0, Math.floor(tons.length*o.cortar));
    const antes = Math.floor(srOuve*(o.antes != null ? o.antes : 0.3 + 1.2*r())), depois = Math.floor(srOuve*(o.depois != null ? o.depois : 0.6));
    const s = new Float32Array(antes + tons.length + depois), ganho = o.ganho != null ? o.ganho : 0.02 + 0.98*r();
    for(let i=0;i<tons.length;i++) s[antes+i] = tons[i]*ganho;
    const sigma = o.snr == null ? 0 : Math.sqrt(((0.5*ganho)**2/2) / 10**(o.snr/10)), fase = r()*6.28;
    for(let i=0;i<s.length;i++) s[i] += sigma*gauss(r) + (o.dc||0) + (o.zumbido ? 0.3*ganho*Math.sin(fase + 2*Math.PI*50*i/srOuve) : 0);
    return s;
  }
  const out = {sha: cfg.msgs.map(m => shaRadio(m).slice(0,32)), matriz: 0, matrizOk: 0, errados: [], falhas: [],
               cruzado: 0, cruzadoOk: 0, cortes: 0, cortesOk: 0, emCurso: 0, emCursoOk: 0, ruido: 0, ruidoFalso: 0,
               fortes: 0, fortesOk: 0, fortesErrado: 0};
  let semente = 1;
  for(const sr of [8000, 11025, 16000, 22050, 44100, 48000, 96000]) for(const m of cfg.msgs) for(const snr of [null, 20, 10, 3]){
    const r = prng(semente++), hex = shaRadio(m).slice(0,32);
    const t = procurarTrama(captura(hex, sr, r, {snr: snr, dc: r() < 0.3 ? 0.05 : 0, zumbido: r() < 0.3}), sr);
    out.matriz++; if(t.estado === "ok" && t.hex === hex) out.matrizOk++; else if(t.estado === "ok") out.errados.push([sr, m, snr]); else out.falhas.push([sr, m, snr, t.estado]);
  }
  for(const [se, so] of [[48000, 44100], [44100, 48000]]) for(const m of cfg.msgs){
    const r = prng(semente++), hex = shaRadio(m).slice(0,32), t = procurarTrama(captura(hex, so, r, {srEmite: se, snr: 10}), so);
    out.cruzado++; if(t.estado === "ok" && t.hex === hex) out.cruzadoOk++; else if(t.estado === "ok") out.errados.push([se, so, m]);
  }
  for(const sr of [44100, 48000]) for(const corte of [0.2, 0.5, 0.9, 0.99]){
    const hex = shaRadio("KON-A1").slice(0,32);
    const t = procurarTrama(captura(hex, sr, prng(semente++), {cortar: corte, snr: 20}), sr);
    out.cortes++; if(t.estado === "incompleta" && !t.hex) out.cortesOk++;
    const t2 = procurarTrama(captura(hex, sr, prng(semente++), {cortar: corte, snr: 20, depois: 0}), sr);
    out.emCurso++; if(t2.estado === "em_curso" && !t2.hex) out.emCursoOk++;
  }
  for(let k=0;k<12;k++){
    const sr = k % 2 ? 48000 : 44100, r = prng(9000 + k), s = new Float32Array(sr*20);
    for(let i=0;i<s.length;i++) s[i] = (k % 3 === 0 ? 0 : 0.1*gauss(r)) + (k % 4 === 1 ? 0.2*Math.sin(2*Math.PI*50*i/sr) : 0);
    out.ruido++; if(procurarTrama(s, sr).estado === "ok") out.ruidoFalso++;
  }
  for(const snr of [0, -3, -6, -9, -12]) for(let k=0;k<6;k++){
    const hex = shaRadio("KON-B2").slice(0,32), t = procurarTrama(captura(hex, 48000, prng(20000 + k*31 + snr), {snr: snr}), 48000);
    out.fortes++; if(t.estado === "ok" && t.hex === hex) out.fortesOk++; else if(t.estado === "ok") out.fortesErrado++;
  }
  return out;
}
"""


def parte_b(pw, chrome, url):
    print("== B. o código da própria página, no Chrome")
    browser = pw.chromium.launch(executable_path=chrome)
    page = browser.new_page()
    erros = []
    page.on("pageerror", lambda e: erros.append(str(e)))
    page.goto(url + PAGINA)
    r = page.evaluate(ENSAIO_JS, {"msgs": MENSAGENS})
    for m, h in zip(MENSAGENS, r["sha"]):
        prova("SHA-256 da página = Python para «%s»" % m, h == hash32(m), h)
    prova("lê a trama a 7 taxas, 3 mensagens, 4 níveis de ruído", r["matrizOk"] == r["matriz"] == 84, "%d de %d; falhas %s" % (r["matrizOk"], r["matriz"], r["falhas"][:4]))
    prova("emissor a 48 kHz e recetor a 44,1 kHz (e ao contrário)", r["cruzadoOk"] == r["cruzado"] == 6, "%d de %d" % (r["cruzadoOk"], r["cruzado"]))
    prova("trama cortada: recusada como «incompleta», sem hash", r["cortesOk"] == r["cortes"] == 8, "%d de %d" % (r["cortesOk"], r["cortes"]))
    prova("gravação que acaba a meio: «em curso», sem hash", r["emCursoOk"] == r["emCurso"] == 8, "%d de %d" % (r["emCursoOk"], r["emCurso"]))
    prova("20 s de ruído, silêncio ou zumbido: nunca sai um hash", r["ruidoFalso"] == 0 and r["ruido"] == 12, "%d falsos em %d" % (r["ruidoFalso"], r["ruido"]))
    prova("nenhum hash errado em todo o ensaio", not r["errados"] and r["fortesErrado"] == 0, r["errados"][:4])
    print("      ruído forte (0 a −12 dB): %d de %d lidas, %d erradas" % (r["fortesOk"], r["fortes"], r["fortesErrado"]))
    prova("a página abre sem erros", not erros, erros[:2])
    browser.close()


# ---------------------------------------------------------------- C. microfone simulado
def wav_trama(caminho, texto, sr=48000, antes=1.0, depois=1.5, cortar=None, ganho=0.6):
    """Emissor feito à parte, em Python, só a partir do formato: 10101010 + 128 bits, 1200/2200 Hz, 50 bits/s."""
    bits = "10101010" + "".join("{:04b}".format(int(c, 16)) for c in hash32(texto))
    nb = sr / 50
    total = round(len(bits) * nb)
    if cortar is not None:
        total = int(total * cortar)
    amostras, fase = [0.0] * int(sr * antes), 0.0
    for i in range(total):
        f = 2200 if bits[min(len(bits) - 1, int(i / nb))] == "1" else 1200
        fase += 2 * math.pi * f / sr
        amostras.append(ganho * math.sin(fase))
    amostras += [0.0] * int(sr * depois)
    with wave.open(str(caminho), "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(sr)
        w.writeframes(b"".join(struct.pack("<h", int(max(-1, min(1, x)) * 32767)) for x in amostras))


def ouvir_com_microfone(pw, chrome, url, wav, pagina, esperar_por, segundos=25):
    browser = pw.chromium.launch(executable_path=chrome, args=[
        "--use-fake-ui-for-media-stream", "--use-fake-device-for-media-stream",
        "--use-file-for-fake-audio-capture=%s%%noloop" % wav, "--autoplay-policy=no-user-gesture-required"])
    page = browser.new_page()
    page.goto(url + pagina)
    page.click("text=Ouvir e reconstruir")
    texto, fim = "", time.time() + segundos
    while time.time() < fim:
        texto = page.inner_text("#recebido")
        if re.search(esperar_por, texto):
            break
        time.sleep(0.25)
    taxa = page.evaluate("audioCtx ? audioCtx.sampleRate : 0")
    browser.close()
    return texto, taxa


def parte_c(pw, chrome, url, pasta, antigo):
    print("== C. microfone simulado no Chrome (WAV a 48 kHz feito em Python)")
    for texto in ("KON-A1", "KON-B2"):
        wav = pasta / ("%s.wav" % texto)
        wav_trama(wav, texto)
        recebido, taxa = ouvir_com_microfone(pw, chrome, url, wav, PAGINA, r"hash recebido|incompleta|não ouvi|negado")
        prova("%s chega com os 32 caracteres certos (%s…)" % (texto, hash32(texto)[:8]),
              ("hash recebido: " + hash32(texto)) in recebido and "128 de 128" in recebido, recebido.replace("\n", " | ")[:160])
        prova("%s: o ecrã mostra a taxa real (%d Hz)" % (texto, taxa), taxa > 0 and ("%d Hz" % taxa) in recebido)
    wav = pasta / "KON-A1_cortada.wav"
    wav_trama(wav, "KON-A1", cortar=0.5)
    recebido, _ = ouvir_com_microfone(pw, chrome, url, wav, PAGINA, r"incompleta|hash recebido", segundos=12)
    prova("trama cortada a meio: diz «incompleta» e não mostra hash", "incompleta" in recebido and "hash recebido" not in recebido,
          recebido.replace("\n", " | ")[:160])
    if antigo:
        shutil.copy(antigo, RAIZ_SERVIDA[0] / "radio_selo_antigo.html")
        wav = pasta / "KON-A1.wav"
        recebido, _ = ouvir_com_microfone(pw, chrome, url, wav, "radio_selo_antigo.html", r"hash recebido|negado", segundos=12)
        prova("prova negativa: a página antiga ouve o mesmo KON-A1 e não chega ao hash certo",
              hash32("KON-A1") not in recebido, recebido.replace("\n", " | ")[:160])


RAIZ_SERVIDA = [RAIZ]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--antigo", help="versão antiga de radio_selo.html, para a prova negativa")
    a = ap.parse_args()
    parte_a()
    from playwright.sync_api import sync_playwright

    chrome = os.environ.get("CHROME", "/usr/bin/google-chrome")
    with TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        servida = tmp / "raiz"
        shutil.copytree(RAIZ, servida, ignore=shutil.ignore_patterns(".git", "dist", "node_modules"))
        RAIZ_SERVIDA[0] = servida
        srv, url = servidor(servida)
        try:
            with sync_playwright() as pw:
                parte_b(pw, chrome, url)
                parte_c(pw, chrome, url, tmp, a.antigo)
        finally:
            srv.shutdown()
    print("\n%d PASSA, %d FALHA" % (OK[0], FALHAS[0]))
    sys.exit(1 if FALHAS[0] else 0)


if __name__ == "__main__":
    main()
