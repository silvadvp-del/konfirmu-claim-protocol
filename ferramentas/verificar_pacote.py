#!/usr/bin/env python3
"""Verificação estática do pacote da Konfirmu (paleta 2040): emojis, cores fora da paleta, fundos brancos e
ligações para fora. Só biblioteca padrão, sem rede.

Uso: python3 -I ferramentas/verificar_pacote.py PASTA [--json] [--estrito]
  --estrito  sai com código 1 se houver um emoji, uma cor verde/violeta/amarela/vermelha, um fundo branco
             ou uma ligação para fora (o carmesim #EF4444 só conta como permitido nos ficheiros do alerta 112).

Paleta permitida: famílias neutra, azul (200–240°) e pêssego (10–38°). Emoji = carácter
Extended_Pictographic do Unicode (com ou sem seletor), indicadores regionais, seletor FE0F e 20E3.
"""
import colorsys, json, os, re, sys

EP = [(0x00A9,0x00A9),(0x00AE,0x00AE),(0x203C,0x203C),(0x2049,0x2049),(0x2122,0x2122),(0x2139,0x2139),
(0x2194,0x2199),(0x21A9,0x21AA),(0x231A,0x231B),(0x2328,0x2328),(0x2388,0x2388),(0x23CF,0x23CF),(0x23E9,0x23F3),
(0x23F8,0x23FA),(0x24C2,0x24C2),(0x25AA,0x25AB),(0x25B6,0x25B6),(0x25C0,0x25C0),(0x25FB,0x25FE),(0x2600,0x2605),
(0x2607,0x2612),(0x2614,0x2685),(0x2690,0x2705),(0x2708,0x2712),(0x2714,0x2714),(0x2716,0x2716),(0x271D,0x271D),
(0x2721,0x2721),(0x2728,0x2728),(0x2733,0x2734),(0x2744,0x2744),(0x2747,0x2747),(0x274C,0x274C),(0x274E,0x274E),
(0x2753,0x2755),(0x2757,0x2757),(0x2763,0x2767),(0x2795,0x2797),(0x27A1,0x27A1),(0x27B0,0x27B0),(0x27BF,0x27BF),
(0x2934,0x2935),(0x2B05,0x2B07),(0x2B1B,0x2B1C),(0x2B50,0x2B50),(0x2B55,0x2B55),(0x3030,0x3030),(0x303D,0x303D),
(0x3297,0x3297),(0x3299,0x3299),(0x1F000,0x1F0FF),(0x1F10D,0x1F10F),(0x1F12F,0x1F12F),(0x1F16C,0x1F171),
(0x1F17E,0x1F17F),(0x1F18E,0x1F18E),(0x1F191,0x1F19A),(0x1F1AD,0x1F1FF),(0x1F201,0x1F20F),(0x1F21A,0x1F21A),
(0x1F22F,0x1F22F),(0x1F232,0x1F23A),(0x1F23C,0x1F23F),(0x1F249,0x1F3FA),(0x1F400,0x1F53D),(0x1F546,0x1F64F),
(0x1F680,0x1F6FF),(0x1F774,0x1F77F),(0x1F7D5,0x1F7FF),(0x1F80C,0x1F80F),(0x1F848,0x1F84F),(0x1F85A,0x1F85F),
(0x1F888,0x1F88F),(0x1F8AE,0x1F8FF),(0x1F90C,0x1F93A),(0x1F93C,0x1F945),(0x1F947,0x1FAFF),(0x1FC00,0x1FFFD)]
TIPOGRAFIA = {0x00A9, 0x00AE, 0x2122}  # (c), (r), TM: so contam se vierem com o seletor de emoji
def e_pict(cp):
    for a, b in EP:
        if a <= cp <= b: return True
    return False

def emojis(texto):
    achados = []
    for i, ch in enumerate(texto):
        cp = ord(ch); seg = texto[i+1:i+2]
        if cp in (0xFE0F, 0x20E3):
            achados.append(ch); continue
        if e_pict(cp):
            if cp in TIPOGRAFIA and seg != "️":
                continue
            achados.append(ch)
    return achados

RX_HEX = re.compile(r"#([0-9a-fA-F]{8}|[0-9a-fA-F]{6}|[0-9a-fA-F]{3,4})(?![0-9a-fA-F])")
RX_RGB = re.compile(r"rgba?\(\s*(\d{1,3})(?:\s*,\s*|\s+)(\d{1,3})(?:\s*,\s*|\s+)(\d{1,3})")
RX_HSL = re.compile(r"hsla?\(\s*(-?\d+(?:\.\d+)?)(?:deg)?(?:\s*,\s*|\s+)(\d+(?:\.\d+)?)%(?:\s*,\s*|\s+)(\d+(?:\.\d+)?)%")
NOMES = {"green":(0,128,0),"lime":(0,255,0),"limegreen":(50,205,50),"seagreen":(46,139,87),"forestgreen":(34,139,34),
 "darkgreen":(0,100,0),"olive":(128,128,0),"teal":(0,128,128),"purple":(128,0,128),"violet":(238,130,238),
 "indigo":(75,0,130),"magenta":(255,0,255),"fuchsia":(255,0,255),"orchid":(218,112,214),"plum":(221,160,221),
 "lavender":(230,230,250),"mediumpurple":(147,112,219),"blueviolet":(138,43,226),"darkviolet":(148,0,211),
 "mediumseagreen":(60,179,113),"springgreen":(0,255,127),"lightgreen":(144,238,144),"palegreen":(152,251,152),
 "yellowgreen":(154,205,50),"chartreuse":(127,255,0),"lawngreen":(124,252,0),"darkseagreen":(143,188,143),
 "white":(255,255,255),"yellow":(255,255,0)}
RX_NOME = re.compile(r"(?<![\w-])(?:color|background|background-color|fill|stroke|border(?:-[a-z]+)?|outline|box-shadow|text-shadow|stop-color)\s*[:=]\s*['\"]?\s*(" + "|".join(sorted(NOMES, key=len, reverse=True)) + r")\b", re.I)

def familia(r, g, b):
    mx, mn = max(r, g, b)/255, min(r, g, b)/255
    if mx == 0: return "neutro"
    if (mx - mn) < 0.06 and (mx - mn)/mx < 0.12: return "neutro"
    h = colorsys.rgb_to_hsv(r/255, g/255, b/255)[0]*360
    if h < 10 or h > 330: return "vermelho"
    if h <= 38: return "pessego"
    if h < 70: return "amarelo"
    if h < 165: return "verde"
    if h < 200: return "azul-petroleo"
    if h <= 240: return "azul"
    return "violeta"

def hex_rgb(h):
    if len(h) in (3, 4): h = "".join(c*2 for c in h[:3])
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))

def cores(texto):
    out = []
    for m in RX_HEX.finditer(texto):
        # nao confundir com ancoras de URL tipo href="#abc" ou entidades
        antes = texto[max(0, m.start()-12):m.start()]
        if re.search(r"(href=[\"']|&|url\(\s*[\"']?)$", antes): continue  # ancoras e referencias url(#id), nao cores
        r, g, b = hex_rgb(m.group(1)); out.append(("#"+m.group(1).upper(), familia(r, g, b)))
    for m in RX_RGB.finditer(texto):
        r, g, b = (min(255, int(x)) for x in m.groups()); out.append(("rgb(%d,%d,%d)" % (r, g, b), familia(r, g, b)))
    for m in RX_HSL.finditer(texto):
        h, s, l = float(m.group(1)) % 360, float(m.group(2))/100, float(m.group(3))/100
        r, g, b = (int(round(x*255)) for x in colorsys.hls_to_rgb(h/360, l, s)); out.append(("hsl(%s)" % m.group(0), familia(r, g, b)))
    for m in RX_NOME.finditer(texto):
        n = m.group(1).lower(); out.append((n, familia(*NOMES[n]) if n not in ("white",) else "branco"))
    return out

RX_FUNDO_BRANCO = re.compile(r"background(?:-color)?\s*:\s*(?:#fff\b|#ffffff\b|white\b|rgb\(\s*255\s*,\s*255\s*,\s*255\s*\))", re.I)
RX_PRINT = re.compile(r"@media\s+print\s*\{(?:[^{}]*\{[^{}]*\})*[^{}]*\}", re.I)

RX_FORA = re.compile(r"""(?:src|href|action|data|poster|srcset)\s*=\s*["']\s*(?:https?:)?//|url\(\s*["']?\s*(?:https?:)?//|(?:fetch|import|importScripts|EventSource|WebSocket|sendBeacon|open)\s*\(\s*["'`]\s*(?:https?|wss?):|new\s+WebSocket\s*\(|@import\s+["']?(?:https?:)?//""", re.I)

def ficheiros(raiz):
    for d, _, fs in os.walk(raiz):
        for f in fs:
            if f.endswith((".html", ".htm", ".css", ".js", ".mjs", ".json", ".svg", ".webmanifest")):
                yield os.path.join(d, f)

def main():
    raiz = sys.argv[1]; em_json = "--json" in sys.argv
    tot = {"ficheiros": 0, "emojis": 0, "verde": 0, "violeta": 0, "vermelho": 0, "amarelo": 0, "branco": 0, "fora": 0, "fundos_brancos": 0}
    linhas = []
    for p in sorted(ficheiros(raiz)):
        rel = os.path.relpath(p, raiz)
        if "/_anterior/" in "/" + rel or rel.startswith("_anterior") or "/.git/" in "/" + rel: continue
        t = open(p, encoding="utf-8", errors="replace").read()
        # so contam CARGAS de fora (scripts, estilos, imagens, pedidos); ligacoes <a>, canonical/alternate e <meta> nao carregam nada
        sem_nav = re.sub(r"<a\b[^>]*>|<link\b[^>]*rel=[\"'](?:canonical|alternate)[\"'][^>]*>|<meta\b[^>]*>", "", t, flags=re.I)
        e = emojis(t); c = cores(t); fora = RX_FORA.findall(sem_nav)
        brancos = len(RX_FUNDO_BRANCO.findall(RX_PRINT.sub("", t)))  # na impressão, papel branco é normal
        fam = {}
        for cor, f in c: fam.setdefault(f, set()).add(cor)
        reg = {"ficheiro": rel, "emojis": len(e), "exemplos_emoji": "".join(sorted(set(e)))[:40],
               "verde": sorted(fam.get("verde", [])), "violeta": sorted(fam.get("violeta", [])),
               "vermelho": sorted(fam.get("vermelho", [])), "amarelo": sorted(fam.get("amarelo", [])),
               "branco": sorted(fam.get("branco", [])), "fora": len(fora), "fundos_brancos": brancos}
        tot["ficheiros"] += 1; tot["emojis"] += len(e); tot["fora"] += len(fora); tot["fundos_brancos"] += brancos
        for k in ("verde", "violeta", "vermelho", "amarelo", "branco"): tot[k] += len(reg[k])
        linhas.append(reg)
    if em_json:
        print(json.dumps({"total": tot, "ficheiros": linhas}, ensure_ascii=False, indent=1))
        return 1 if ("--estrito" in sys.argv and any(tot[k] for k in tot if k not in ("ficheiros", "branco"))) else 0
    for r in linhas:
        if r["emojis"] or r["verde"] or r["violeta"] or r["fora"] or r["vermelho"] or r["amarelo"] or r["branco"] or r["fundos_brancos"]:
            print("%-44s emo %4d %s | verde %s | violeta %s | verm %s | amar %s | branco %s | fora %d" % (r["ficheiro"][:44], r["emojis"], r["exemplos_emoji"], ",".join(r["verde"])[:60], ",".join(r["violeta"])[:40], ",".join(r["vermelho"])[:40], ",".join(r["amarelo"])[:30], ",".join(r["branco"])[:20], r["fora"]))
    print("TOTAL", json.dumps(tot))
    return 1 if ("--estrito" in sys.argv and any(tot[k] for k in tot if k not in ("ficheiros", "branco"))) else 0

if __name__ == "__main__":
    sys.exit(main())
