#!/usr/bin/env python3
"""Paleta única da Konfirmu — ordem do David de 27-11-2026, 13:14 (decisão cromática fechada).

Cor oficial e exclusiva: Pêssego Solar #FF9E7D sobre Azul Abissal #0B192C, texto Branco Titânio #F4F7FA
e Cinza Nevoeiro #9FB3C8, vidro rgba(15, 34, 61, 0.72). O #f7b397 está reformado. Carmesim #EF4444 só no
alerta real 112 / 116 111. Zero verde, zero violeta, zero amarelo berrante, zero fundos brancos crus,
um só tema escuro. Zero emojis de sistema: ícones de linha 1,5 px (scripts/icones_linha.py).

Uso (só a biblioteca padrão; o portão usa o módulo «regex» se existir, para a propriedade Extended_Pictographic):
  python3 -I scripts/paleta_unica.py aplicar [RAIZ]          converte as páginas estáticas (idempotente)
  python3 -I scripts/paleta_unica.py verificar [RAIZ|ZIP]    portão visual; sai com 1 se houver falhas

As páginas feitas pelos geradores (app_unica.html, edicao-21/app_unica.html, edicao-21/index.html) não se
convertem aqui: a cor está na fonte (scripts/gerar_menu.py e scripts/tigelas.py). O portão verifica todas.
"""
from __future__ import annotations

import io
import json
import os
import re
import sys
import zipfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from icones_linha import ICONES  # noqa: E402

# ---------------------------------------------------------------- paleta
A = (11, 25, 44)      # Azul Abissal  #0B192C — fundo
V = (15, 34, 61)      # vidro ótico   rgba(15, 34, 61, 0.72)
P = (255, 158, 125)   # Pêssego Solar #FF9E7D — assinatura e luz
T = (244, 247, 250)   # Branco Titânio #F4F7FA — texto
N = (159, 179, 200)   # Cinza Nevoeiro #9FB3C8 — texto secundário e linhas
C = (239, 68, 68)     # Carmesim #EF4444 — só no alerta real 112 / 116 111
OFICIAIS = {A, V, P, T, N, C}
HEX = {A: "#0B192C", P: "#FF9E7D", T: "#F4F7FA", N: "#9FB3C8", C: "#EF4444"}
ALFA_VIDRO = 0.72
ALFA_LINHA = 0.24
ALFA_BOTAO = 0.16

GERADAS = {"app_unica.html", "edicao-21/app_unica.html", "edicao-21/index.html"}
NOMEADAS = {"white": (255, 255, 255), "black": (0, 0, 0), "red": (255, 0, 0), "green": (0, 128, 0),
            "lime": (0, 255, 0), "yellow": (255, 255, 0), "gold": (255, 215, 0), "orange": (255, 165, 0),
            "purple": (128, 0, 128), "violet": (238, 130, 238), "blue": (0, 0, 255), "navy": (0, 0, 128),
            "gray": (128, 128, 128), "grey": (128, 128, 128), "silver": (192, 192, 192), "pink": (255, 192, 203),
            "magenta": (255, 0, 255), "cyan": (0, 255, 255), "teal": (0, 128, 128), "brown": (165, 42, 42),
            "darkgreen": (0, 100, 0), "lightgreen": (144, 238, 144), "limegreen": (50, 205, 50),
            "goldenrod": (218, 165, 32), "crimson": (220, 20, 60), "tomato": (255, 99, 71)}

RE_HEX = re.compile(r"#(?:[0-9a-fA-F]{8}|[0-9a-fA-F]{6}|[0-9a-fA-F]{4}|[0-9a-fA-F]{3})(?![0-9a-zA-Z_-])")
RE_FUNC = re.compile(r"rgba?\(\s*([^()]*?)\s*\)", re.I)
RE_NOMEADA = re.compile(r"(?<![\w#.-])(" + "|".join(sorted(NOMEADAS, key=len, reverse=True)) + r")(?![\w-])", re.I)
RE_COR = re.compile(RE_HEX.pattern + "|" + RE_FUNC.pattern, re.I)


def _lin(c):
    c /= 255
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4


def luminancia(rgb):
    r, g, b = (_lin(x) for x in rgb)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contraste(a, b):
    la, lb = luminancia(a), luminancia(b)
    if la < lb:
        la, lb = lb, la
    return (la + 0.05) / (lb + 0.05)


def compor(frente, alfa, fundo):
    return tuple(round(f * alfa + b * (1 - alfa)) for f, b in zip(frente, fundo))


def matiz(rgb):
    r, g, b = (x / 255 for x in rgb)
    mx, mn = max(r, g, b), min(r, g, b)
    if mx == mn:
        return 0.0
    d = mx - mn
    if mx == r:
        h = ((g - b) / d) % 6
    elif mx == g:
        h = (b - r) / d + 2
    else:
        h = (r - g) / d + 4
    return h * 60


def cromatico(rgb):
    return max(rgb) - min(rgb) >= 60 and max(rgb) >= 70


def vermelho(rgb):
    h = matiz(rgb)
    return cromatico(rgb) and (h >= 340 or h < 14) and rgb[0] > 150


# ---------------------------------------------------------------- ler e escrever cores
def ler_hex(tok):
    h = tok[1:]
    if len(h) in (3, 4):
        h = "".join(c * 2 for c in h)
    rgb = tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))
    alfa = int(h[6:8], 16) / 255 if len(h) == 8 else 1.0
    return rgb, alfa


def ler_func(corpo):
    """rgb(1,2,3) · rgba(1,2,3,.5) · rgb(1 2 3 / .5) · percentagens. Devolve (rgb, alfa, sintaxe_espaco)."""
    espaco = "," not in corpo
    if espaco:
        partes = corpo.replace("/", " / ").split()
        alfa_txt = None
        if "/" in partes:
            i = partes.index("/")
            alfa_txt = partes[i + 1] if i + 1 < len(partes) else None
            partes = partes[:i]
    else:
        partes = [p.strip() for p in corpo.split(",")]
        alfa_txt = partes[3] if len(partes) > 3 else None
        partes = partes[:3]
    if len(partes) != 3:
        return None

    def canal(p):
        return round(float(p[:-1]) * 2.55) if p.endswith("%") else round(float(p))

    try:
        rgb = tuple(max(0, min(255, canal(p))) for p in partes)
        alfa = 1.0
        if alfa_txt is not None:
            alfa = float(alfa_txt[:-1]) / 100 if alfa_txt.endswith("%") else float(alfa_txt)
    except ValueError:
        return None
    return rgb, alfa, espaco


def escrever(rgb, alfa, espaco=False):
    alfa = round(alfa, 3)
    if alfa >= 0.999 and rgb in HEX:
        return HEX[rgb]
    a = ("%g" % alfa)
    if a.startswith("0."):
        a = a[1:]
    if espaco:
        return "rgb(%d %d %d / %s)" % (rgb[0], rgb[1], rgb[2], a)
    return "rgba(%d,%d,%d,%s)" % (rgb[0], rgb[1], rgb[2], a)


# ---------------------------------------------------------------- mapa por papel
class Contexto:
    def __init__(self, pagina_clara=False, nivel_pagina=False, prop=""):
        self.pagina_clara = pagina_clara
        self.nivel_pagina = nivel_pagina
        self.prop = prop
        self.botao = False   # a regra ganhou fundo de botão pêssego
        self.escureceu = False  # o fundo era claro e passou a escuro
        self.texto_escuro = False  # a regra escreve texto escuro (ex.: botão pêssego com letra azul abissal)
        self.pessego_cheio = False  # … e o fundo dela é pêssego cheio: a letra escura fica azul abissal


def mapear(rgb, alfa, papel, ctx):
    """Devolve (rgb, alfa) oficiais para uma cor, conforme o papel: fundo, texto, linha, acento, desenho."""
    if rgb in OFICIAIS and rgb != C:
        return rgb, alfa
    # o carmesim #EF4444 nunca nasce da conversão: só se escreve à mão no alerta real 112 / 116 111
    y = luminancia(rgb)
    if papel == "acento":
        return P, alfa
    if papel == "fundo_var":
        # --papel, --painel, --azulejo…: fundo pelo nome; claro ou escuro, fica sempre escuro (um só tema)
        pagina = bool(re.search(r"papel|pagina|fundo|bg|back|ceu|sky|paper", ctx.prop or ""))
        if y < 0.03:
            return A, alfa
        if cromatico(rgb) or y < 0.35:
            return V, ALFA_VIDRO * alfa
        return (A, alfa) if pagina else (V, ALFA_VIDRO * alfa)
    if papel == "variavel":
        # --variável: cor-base que pode servir de fundo e de texto; o fundo de botão faz-se no uso (var() em background)
        if cromatico(rgb):
            return P, alfa
        if y < 0.03:
            return A, alfa
        if y < 0.2:
            return V, ALFA_VIDRO * alfa
        return (N, alfa) if y < 0.62 else (T, alfa)
    if papel == "fundo":
        if ctx.texto_escuro and cromatico(rgb) and not vermelho(rgb) and 0.10 <= y <= 0.60:
            # botão já desenhado com letra escura sobre tons de pêssego: fica pêssego cheio, a letra
            # azul abissal mantém-se (8,8:1, AAA)
            return P, alfa
        if cromatico(rgb) and 0.10 <= y <= 0.60 and alfa > 0.5:
            ctx.botao = True
            return P, ALFA_BOTAO * alfa
        if y < 0.03:
            return A, alfa
        if y < 0.35:
            return V, ALFA_VIDRO * alfa
        return (A, alfa) if ctx.nivel_pagina else (V, ALFA_VIDRO * alfa)
    if papel == "texto":
        if ctx.pessego_cheio and y < 0.05:
            return A, alfa
        if cromatico(rgb):
            return (T, alfa) if vermelho(rgb) else (P, alfa)
        if y >= 0.62 or y < 0.05:
            return T, alfa
        return N, alfa
    if papel == "sombra":
        return A, alfa
    if papel == "linha":
        if cromatico(rgb):
            return (N, alfa) if vermelho(rgb) else (P, alfa)
        forte = (ctx.pagina_clara and y < 0.2) or (not ctx.pagina_clara and y > 0.45)
        return (N, alfa) if forte else (N, ALFA_LINHA * alfa)
    # desenho: fill, stroke, stop-color, canvas
    if cromatico(rgb):
        # tons escuros de um desenho (manchas, contornos, sombras pintadas) ficam vidro escuro, para o desenho
        # continuar a ler-se por cima do pêssego; os tons médios e claros ficam pêssego
        return (V, alfa) if y < 0.35 else (P, alfa)
    if y < 0.03:
        return A, alfa
    if y < 0.2:
        return V, ALFA_VIDRO * alfa
    if y < 0.62:
        return N, alfa
    return T, alfa


def papel_de(prop, nome_var_papeis=None):
    p = prop.strip().lower()
    if p.startswith("--"):
        pelo_nome = papel_var_pelo_nome(p)
        if pelo_nome == "fundo":
            return "fundo_var"
        return pelo_nome if pelo_nome in ("linha", "texto") else "variavel"
    if p in ("background", "background-color", "background-image"):
        return "fundo"
    if p in ("color", "caret-color", "-webkit-text-fill-color", "text-decoration-color", "column-rule-color"):
        return "texto"
    if p == "accent-color":
        return "acento"
    if p in ("box-shadow", "text-shadow", "filter", "-webkit-filter"):
        return "sombra"
    if p.startswith("border") or p.startswith("outline") or p.startswith("column-rule") or p == "text-decoration":
        return "linha"
    return "desenho"


def papel_var_pelo_nome(nome):
    n = nome.lower()
    if re.search(r"pagina|fundo|bg|back|painel|panel|card|azulejo|surface|superf|sky|ceu|paper|papel", n):
        return "fundo"
    if re.search(r"tinta|texto|text|fg|ink|letra-cor|muted|sub", n):
        return "texto"
    if re.search(r"linha|borda|border|line|rule", n):
        return "linha"
    if re.search(r"(^--u$)|acento|accent|destaque|ok|verde|green|sucesso|link|marca|brand|ouro|gold|warn|amarelo", n):
        return "acento"
    return "desenho"


def trocar_cores(valor, papel, ctx):
    """Troca todas as cores de um valor CSS/atributo (hex, rgb[a](), nomes)."""
    if papel == "sombra" and ctx.prop in ("filter", "-webkit-filter") and "drop-shadow" not in valor:
        return valor

    def por_hex(m):
        rgb, alfa = ler_hex(m.group(0))
        r, a = mapear(rgb, alfa, papel, ctx)
        if (r, round(a, 3)) == (rgb, round(alfa, 3)):
            return m.group(0)  # a cor já era oficial: fica escrita como estava
        return escrever(r, a)

    def por_func(m):
        lido = ler_func(m.group(1))
        if not lido:
            return m.group(0)
        rgb, alfa, espaco = lido
        r, a = mapear(rgb, alfa, papel, ctx)
        if (r, round(a, 3)) == (rgb, round(alfa, 3)):
            return m.group(0)
        return escrever(r, a, espaco)

    def por_nome(m):
        rgb = NOMEADAS[m.group(1).lower()]
        r, a = mapear(rgb, 1.0, papel, ctx)
        return escrever(r, a)

    v = RE_HEX.sub(por_hex, valor)
    v = RE_FUNC.sub(por_func, v)
    if not re.search(r"url\(|['\"]", v):
        v = RE_NOMEADA.sub(por_nome, v)
    return v


# ---------------------------------------------------------------- CSS
RE_REGRA = re.compile(r"([^{}]*)\{([^{}]*)\}")
RE_DECL = re.compile(r"(?P<prop>--[\w-]+|[a-zA-Z-]+)\s*:\s*(?P<val>[^;{}]*)")


def papeis_das_variaveis(css):
    """Papel de cada --variável pelo uso: var(--x) em background → fundo, em color → texto, etc."""
    usos = {}
    for m in RE_DECL.finditer(css):
        prop, val = m.group("prop"), m.group("val")
        if prop.startswith("--"):
            continue
        for v in re.findall(r"var\(\s*(--[\w-]+)", val):
            usos.setdefault(v.lower(), []).append(papel_de(prop))
    papeis = {}
    for v, lista in usos.items():
        papeis[v] = max(set(lista), key=lista.count)
    return papeis


VARS_CROMATICAS = set()  # preenchido por converter_css: --variáveis cujo valor original é uma cor cromática média


def corpo_decls(corpo, ctx_base, papeis_var, seletor=""):
    nivel = bool(re.search(r"(^|[\s,>])(html|body|:root)(?![\w-])", seletor))
    ctx = Contexto(ctx_base.pagina_clara, nivel)
    texto_pintado = bool(re.search(r"background-clip\s*:\s*text", corpo))  # gradiente dentro das letras
    mc = re.search(r"(?<![\w-])color\s*:\s*([^;}]+)", corpo)
    if mc:
        for mm in RE_COR.finditer(mc.group(1)):
            tok = mm.group(0)
            lido = ler_hex(tok) if tok.startswith("#") else ler_func(mm.group(1))
            if lido and luminancia(lido[0]) < 0.05 and lido[1] > 0.5:
                ctx.texto_escuro = True
    if ctx.texto_escuro:
        for mb in re.finditer(r"(?<![\w-])background(?:-color|-image)?\s*:\s*([^;}]+)", corpo):
            for mm in RE_COR.finditer(mb.group(1)):
                tok = mm.group(0)
                lido = ler_hex(tok) if tok.startswith("#") else ler_func(mm.group(1))
                if lido and lido[1] > 0.5 and (lido[0] == P or (cromatico(lido[0]) and not vermelho(lido[0])
                                                                 and 0.10 <= luminancia(lido[0]) <= 0.60)):
                    ctx.pessego_cheio = True
    novos = []
    pos = 0
    tem_cor = False
    tem_borda = False
    for m in RE_DECL.finditer(corpo):
        prop, val = m.group("prop"), m.group("val")
        pl = prop.lower()
        if pl == "color-scheme":
            val2 = re.sub(r"\blight\b\s*", "", val).strip() or "dark"
            if "dark" not in val2:
                val2 = "dark"
            novos.append((m.start("val"), m.end("val"), val2))
            continue
        if pl == "color":
            tem_cor = True
        if pl in ("border", "border-color", "border-width", "border-style"):
            tem_borda = True
        papel = papel_de(prop, papeis_var)
        if texto_pintado and papel == "fundo":
            papel = "desenho"
        ctx.prop = pl
        val2 = trocar_cores(val, papel, ctx)
        if nivel and pl == "background" and "gradient(" in val2 and not re.search(r"\)\s*#0B192C\s*$", val2):
            # fundo da página só em gradiente: as paragens translúcidas mostravam o branco do ecrã por baixo
            val2 = val2.rstrip() + " #0B192C"
        if papel == "fundo" and not texto_pintado:
            for v in re.findall(r"var\(\s*(--[\w-]+)\s*\)", val2):
                if v.lower() in VARS_CROMATICAS:
                    val2 = val2.replace("var(%s)" % v, escrever(P, ALFA_BOTAO))
                    ctx.botao = True
            if not ctx.botao and fundo_claro_original(val):
                ctx.escureceu = True
        if val2 != val:
            novos.append((m.start("val"), m.end("val"), val2))
    saida = []
    for a, b, txt in novos:
        saida.append(corpo[pos:a])
        saida.append(txt)
        pos = b
    saida.append(corpo[pos:])
    corpo2 = "".join(saida)
    if getattr(ctx, "escureceu", False) and not ctx.botao and not tem_cor and seletor != "inline":
        corpo2 = corpo2.rstrip().rstrip(";") + ";color:#F4F7FA"
    if ctx.botao:
        # fundo de botão em vidro pêssego: texto titânio e aro pêssego (ícones pêssego continuam a ver-se)
        if tem_cor:
            corpo2 = re.sub(r"((?:^|;|\s)color\s*:\s*)[^;}]*", r"\1#F4F7FA", corpo2)
        else:
            corpo2 = corpo2.rstrip().rstrip(";") + ";color:#F4F7FA"
        if re.search(r"(?:^|;|\s)border\s*:\s*(0|none)\s*(?=;|$)", corpo2):
            corpo2 = re.sub(r"((?:^|;|\s)border\s*:\s*)(0|none)\s*(?=;|$)", r"\g<1>1px solid #FF9E7D", corpo2)
        elif not tem_borda:
            corpo2 = corpo2.rstrip().rstrip(";") + ";border:1px solid #FF9E7D"
    return corpo2


def fundo_claro_original(valor):
    """O valor original de um fundo era claro (o texto por omissão, preto, deixava de se ler no escuro)?"""
    for m in RE_COR.finditer(valor):
        tok = m.group(0)
        lido = ler_hex(tok) if tok.startswith("#") else ler_func(m.group(1))
        if lido and luminancia(lido[0]) > 0.35 and lido[1] > 0.5:
            return True
    return bool(re.search(r"(?<![\w-])white(?![\w-])", valor))


BASE_CSS = (":root{color-scheme:dark}"
            "input:not([type=range]):not([type=checkbox]):not([type=radio]):not([type=color]),select,textarea,button"
            "{color:#F4F7FA;background-color:rgba(15,34,61,.72)}"
            "input,select,textarea,button{border-color:rgba(159,179,200,.24)}"
            "::placeholder{color:#9FB3C8;opacity:1}"
            "::file-selector-button{color:#F4F7FA;background:rgba(15,34,61,.72);border:1px solid #FF9E7D;border-radius:8px}"
            "input[type=range],input[type=checkbox],input[type=radio],progress{accent-color:#FF9E7D}"
            "option{background:#0B192C;color:#F4F7FA}")


def converter_css(css, pagina_clara):
    VARS_CROMATICAS.clear()
    for m in RE_DECL.finditer(css):
        if m.group("prop").startswith("--"):
            c = RE_COR.fullmatch(m.group("val").strip())
            if c:
                lido = ler_hex(c.group(0)) if c.group(0).startswith("#") else ler_func(c.group(1))
                if lido and cromatico(lido[0]) and 0.10 <= luminancia(lido[0]) <= 0.75:
                    VARS_CROMATICAS.add(m.group("prop").lower())
    papeis_var = papeis_das_variaveis(css)
    base = Contexto(pagina_clara)

    def regra(m):
        seletor, corpo = m.group(1), m.group(2)
        if seletor.strip().startswith("@") and not corpo.strip():
            return m.group(0)
        return seletor + "{" + corpo_decls(corpo, base, papeis_var, seletor) + "}"

    # várias passagens para regras dentro de @media (a regex só apanha o nível mais interior)
    anterior, atual = None, css
    marcado = RE_REGRA.sub(lambda m: regra(m).replace("{", "\x00").replace("}", "\x01"), atual)
    return marcado.replace("\x00", "{").replace("\x01", "}") if anterior is None else marcado


def pagina_e_clara(html):
    m = re.search(r"(?:^|[}\s])(?:html|body)\s*\{([^}]*)\}", html)
    if not m:
        return False
    d = re.search(r"background(?:-color)?\s*:\s*([^;}]+)", m.group(1))
    if not d:
        return False
    c = RE_COR.search(d.group(1))
    if not c:
        return bool(re.search(r"\bwhite\b", d.group(1)))
    tok = c.group(0)
    rgb = ler_hex(tok)[0] if tok.startswith("#") else (ler_func(c.group(1)) or ((0, 0, 0),))[0]
    return luminancia(rgb) > 0.5


# ---------------------------------------------------------------- emojis → ícones
try:
    import regex as _rx
    RE_PICTO = _rx.compile(r"(?:\p{Extended_Pictographic}|\p{Regional_Indicator})(?:️|⃣|‍(?:\p{Extended_Pictographic})️?)*️?")
except ImportError:  # sem «regex»: intervalos principais
    _rx = None
    RE_PICTO = re.compile("(?:[©®‼⁉™ℹ↔-↙↩↪⌚⌛⌨⏏"
                          "⏩-⏳⏸-⏺Ⓜ▪▫▶◀◻-◾☀-★☇-☒"
                          "☔-⚅⚐-✅✈-✒✔✖✝✡✨✳✴❄❇"
                          "❌❎❓-❕❗❣-❧➕-➗➡➰➿⤴⤵"
                          "⬅-⬇⬛⬜⭐⭕〰〽㊗㊙\U0001F000-\U0001FAFF])"
                          "(?:️|‍[☀-➿\U0001F000-\U0001FAFF]️?)*️?")
# Setas tipográficas (← → ↔) e outros sinais de texto ficam: não são emojis de apresentação.
SETAS_DE_TEXTO = set("←↑→↓↔↕↖↗↘↙©®™")

EMOJI_ICONE = {
    "✉": "mail", "🔒": "lock", "🖨": "printer", "✍": "pen-line", "✔": "check", "✓": "check", "✗": "x",
    "💾": "save", "📷": "camera", "📸": "camera", "🔎": "search", "🔍": "search", "🎬": "clapperboard",
    "🎥": "video", "⏹": "square", "▶": "play", "🤖": "bot", "☀": "sun", "💡": "lightbulb", "🌧": "cloud-rain",
    "📋": "clipboard-list", "🦒": "girafa", "🔊": "volume-2", "🥣": "soup", "📏": "ruler", "🌿": "leaf",
    "👆": "pointer", "💙": "heart", "⭐": "star", "🌟": "star", "★": "star", "🌸": "flower", "🎨": "palette",
    "🎵": "music", "🎶": "music", "📞": "phone", "✨": "sparkles", "🧭": "compass", "🏴": "flag",
    "🏆": "trophy", "🧚": "wand-sparkles", "⏰": "alarm-clock", "🩺": "stethoscope", "📻": "radio",
    "🎙": "mic", "🤝": "handshake", "🗳": "vote", "📥": "inbox", "🔓": "lock-open", "📡": "radio-tower",
    "🌱": "sprout", "🧒": "baby", "🌍": "earth", "🌎": "earth", "🌏": "earth", "🎉": "party-popper",
    "🎄": "tree-pine", "🧠": "brain", "⭕": "circle", "💧": "droplet", "🛡": "shield", "🌙": "moon",
    "❓": "circle-question-mark", "🔏": "file-lock",
}
CSS_ICONE = ".ki{display:inline-block;width:1.15em;height:1.15em;vertical-align:-.18em;color:#FF9E7D;flex:none}"


def base_emoji(cluster):
    return cluster.replace("️", "").split("‍")[0]


def svg_icone(nome):
    return ('<svg class="ki" viewBox="0 0 24 24" aria-hidden="true" focusable="false" fill="none" stroke="currentColor" '
            'stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">' + ICONES[nome] + "</svg>")


def picto(ch):
    return ch not in SETAS_DE_TEXTO


def emojis_no_html(html, relatorio):
    """Texto HTML: emoji → ícone SVG. <title> e atributos: emoji sai (com o espaço a seguir)."""
    html = re.sub(r"(<(option|textarea)\b[^>]*>)(.*?)(</\2>)",
                  lambda m: m.group(1) + RE_PICTO.sub(lambda e: "" if picto(e.group(0)) else e.group(0), m.group(3)).lstrip() + m.group(4),
                  html, flags=re.S | re.I)
    partes = re.split(r"(<script\b.*?</script>|<style\b.*?</style>|<!--.*?-->|<title>.*?</title>|<[^>]+>)", html, flags=re.S | re.I)
    usados = 0
    for i, p in enumerate(partes):
        if not p:
            continue
        if p.startswith("<script") or p.startswith("<style") or p.startswith("<!--"):
            continue
        if p.lower().startswith("<title>"):
            partes[i] = RE_PICTO.sub(lambda m: "" if picto(m.group(0)) else m.group(0), p).replace("<title> ", "<title>")
            continue
        if p.startswith("<"):
            partes[i] = RE_PICTO.sub(lambda m: "" if picto(m.group(0)) else m.group(0), p)
            continue

        def troca(m):
            nonlocal usados
            if not picto(m.group(0)):
                return m.group(0)
            nome = EMOJI_ICONE.get(base_emoji(m.group(0)))
            if not nome:
                relatorio.append("emoji sem ícone, retirado: %r" % m.group(0))
                return ""
            usados += 1
            return svg_icone(nome)

        partes[i] = RE_PICTO.sub(troca, p)
    return "".join(partes), usados


# ---------------------------------------------------------------- HTML inteiro
RE_ATR_COR = re.compile(r'(?P<a>\s(?:fill|stroke|stop-color|flood-color|lighting-color|color)\s*=\s*)(?P<q>["\'])(?P<v>[^"\']*)(?P=q)', re.I)
RE_STYLE_ATR = re.compile(r'(?P<a>\sstyle\s*=\s*)(?P<q>["\'])(?P<v>.*?)(?P=q)', re.I | re.S)
RE_META_TEMA = re.compile(r'(<meta\s+name=["\']theme-color["\'][^>]*content=["\'])([^"\']*)(["\'])', re.I)
RE_META_CS = re.compile(r'(<meta\s+name=["\']color-scheme["\'][^>]*content=["\'])([^"\']*)(["\'])', re.I)
RE_STR_JS = re.compile(r"""(?P<q>['"])(?P<s>(?:\\.|(?!(?P=q))[^\\\n])*)(?P=q)""")


def converter_js(js, pagina_clara):
    base = Contexto(pagina_clara)

    def literal(m):
        q, s = m.group("q"), m.group("s")
        antes = js[max(0, m.start() - 40):m.start()]
        alvo = s
        mp = re.search(r"\.style\.([a-zA-Z]+)\s*=\s*$", antes)
        if RE_COR.fullmatch(s.strip()) or (s.strip().lower() in NOMEADAS and re.search(r"(Style|style\.\w+)\s*=\s*$", antes)):
            if mp:
                prop = re.sub(r"([A-Z])", lambda x: "-" + x.group(1).lower(), mp.group(1))
                papel = papel_de(prop)
            elif re.search(r"(fillStyle|strokeStyle|shadowColor)\s*=\s*$", antes):
                papel = "desenho"
            else:
                papel = "desenho"
            ctx = Contexto(pagina_clara)
            alvo = trocar_cores(s, papel, ctx)
        elif RE_COR.search(s):
            # HTML dentro de strings: style="..." e atributos de SVG
            def st(mm):
                corpo = mm.group("v").replace('\\"', '"')
                novo = corpo_decls(corpo, base, {}, "inline")
                if q == '"':
                    novo = novo.replace('"', '\\"')
                return mm.group("a") + mm.group("q") + novo + mm.group("q")
            alvo = re.sub(r'(?P<a>style\s*=\s*)(?P<q>\\?["\'])(?P<v>.*?)(?P=q)', st, alvo)
            alvo = re.sub(r'(?P<a>(?:fill|stroke|stop-color)\s*=\s*)(?P<q>\\?["\'])(?P<v>[^"\'\\]*)(?P=q)',
                          lambda mm: mm.group("a") + mm.group("q") + trocar_cores(mm.group("v"), "desenho", Contexto(pagina_clara)) + mm.group("q"),
                          alvo)
            # declarações soltas (ex.: 'background:#fff;color:#000' passadas a cssText)
            if re.fullmatch(r"\s*(?:[a-z-]+\s*:\s*[^;]+;?\s*)+", alvo) and ":" in alvo:
                alvo = corpo_decls(alvo, base, {}, "inline")
            elif alvo == s and re.search(r"gradient\(|,\s*transparent|^\s*%\s*,", s):
                # pedaço de um gradiente montado por partes ('…%, #ffefbf24, transparent 53%)')
                alvo = trocar_cores(s, "desenho", Contexto(pagina_clara))
        return q + alvo + q

    return RE_STR_JS.sub(literal, js)


def converter_html(html, relatorio):
    clara = pagina_e_clara(html)
    if BASE_CSS not in html:
        html = re.sub(r"(<style\b[^>]*>)", lambda m: m.group(1) + BASE_CSS, html, count=1, flags=re.I)
    # CSS em <style>
    html = re.sub(r"(<style\b[^>]*>)(.*?)(</style>)", lambda m: m.group(1) + converter_css(m.group(2), clara) + m.group(3),
                  html, flags=re.S | re.I)
    # JS em <script> (só cores; emojis em JS têm correções próprias por página)
    html = re.sub(r"(<script\b[^>]*>)(.*?)(</script>)", lambda m: m.group(1) + converter_js(m.group(2), clara) + m.group(3),
                  html, flags=re.S | re.I)
    # atributos style="" e cores de SVG, fora de <script>/<style>
    partes = re.split(r"(<script\b.*?</script>|<style\b.*?</style>)", html, flags=re.S | re.I)
    base = Contexto(clara)
    for i, p in enumerate(partes):
        if p.startswith("<script") or p.startswith("<style"):
            continue
        p = RE_STYLE_ATR.sub(lambda m: m.group("a") + m.group("q") + corpo_decls(m.group("v"), base, {}, "inline") + m.group("q"), p)
        p = RE_ATR_COR.sub(lambda m: m.group("a") + m.group("q") + trocar_cores(m.group("v"), "texto" if m.group("a").strip().lower().startswith("color") else "desenho", Contexto(clara)) + m.group("q"), p)
        p = RE_META_TEMA.sub(lambda m: m.group(1) + "#0B192C" + m.group(3), p)
        # cor inicial dos seletores de cor (pincel do estúdio): começa no pêssego; a criança escolhe a que quiser
        p = re.sub(r'(<input\b[^>]*type=["\']color["\'][^>]*value=["\'])(#[0-9a-fA-F]{6})', lambda m: m.group(1) + "#FF9E7D", p)
        p = RE_META_CS.sub(lambda m: m.group(1) + "dark" + m.group(3), p)
        partes[i] = p
    html = "".join(partes)
    html, usados = emojis_no_html(html, relatorio)
    if usados and CSS_ICONE not in html:
        if re.search(r"</style>", html, re.I):
            html = re.sub(r"</style>", CSS_ICONE + "</style>", html, count=1, flags=re.I)
        else:
            html = re.sub(r"</head>", "<style>" + CSS_ICONE + "</style></head>", html, count=1, flags=re.I)
    if MARCA not in html:
        if re.search(r"<head\b", html, re.I):
            html = re.sub(r"(<head\b[^>]*>)", lambda m: m.group(1) + MARCA, html, count=1, flags=re.I)
        else:  # página sem <head> explícito (ex.: o quiz): a marca vai logo a seguir ao charset
            html = re.sub(r"(<meta charset=[^>]*>)", lambda m: m.group(1) + MARCA, html, count=1, flags=re.I)
    if (usados or "KI." in html or "KI[" in html) and "Ícones: Lucide (ISC)" not in html:
        html = re.sub(r"(<head\b[^>]*>)", r"\1<!-- Ícones: Lucide (ISC), ver assets/LICENCA-ICONES-LUCIDE.txt -->", html, count=1, flags=re.I)
    return html


def ki_js(nomes):
    """Objeto KI com os ícones usados por uma página no seu JavaScript («alcunha=nome» dá outro nome à chave)."""
    itens = []
    for n in nomes:
        chave, nome = n.split("=") if "=" in n else (n.replace("-", "_"), n)
        itens.append("%s:%s" % (json.dumps(chave), json.dumps(svg_icone(nome))))
    return "var KI={%s};" % ",".join(itens)


# ---------------------------------------------------------------- correções de JavaScript por página
# Cada troca tem de existir tal e qual (senão o programa pára): nada fica meio convertido em silêncio.
CORRECOES_JS = {
    "girafinhas_criancas_facil.html": (["soup", "heart", "girafa", "leaf", "flower"], [
        ("btn.textContent = idx===7 ? '🥣💙' : '🥣';", "btn.innerHTML = idx===7 ? KI.soup+KI.heart : KI.soup;"),
        ("counted + ' de 8 ⭐'", "counted + ' de 8'"),
        ("box.innerHTML='🦒🌿 = 🦒🌿<br>IGUAL!'", "box.innerHTML=KI.girafa+KI.leaf+' = '+KI.girafa+KI.leaf+'<br>IGUAL!'"),
        ("box.innerHTML='🦒🌿 ≠ 🦒🌸<br>DIFERENTE!'", "box.innerHTML=KI.girafa+KI.leaf+' ≠ '+KI.girafa+KI.flower+'<br>DIFERENTE!'"),
    ]),
    "sala_natal_girafinhas.html": (["girafa", "terra=earth", "gota=droplet", "sol=sun", "radio", "escudo=shield", "carta=circle-question-mark", "lua=moon", "festa=party-popper"], [
        ('var emojis=["🦒","🌍","💧","☀️","📻","🛡️"];', 'var emojis=["girafa","terra","gota","sol","radio","escudo"];'),
        ('b.className="mcard"; b.textContent="❓";', 'b.className="mcard"; b.innerHTML=KI.carta; b.setAttribute("aria-label","carta virada para baixo");'),
        ("botoes[i].textContent=cartas[i];", "botoes[i].innerHTML=KI[cartas[i]]; botoes[i].setAttribute(\"aria-label\",cartas[i]);"),
        ('botoes[a].textContent="❓"; botoes[c].textContent="❓";', 'botoes[a].innerHTML=KI.carta; botoes[c].innerHTML=KI.carta;'),
        ('var tab=["","","","","","","","",""], vez="🦒";', 'var tab=["","","","","","","","",""], vez="girafa";'),
        ('tab=["","","","","","","","",""]; vez="🦒";', 'tab=["","","","","","","","",""]; vez="girafa";'),
        ('document.getElementById("galoMsg").textContent="joga a 🦒";', 'document.getElementById("galoMsg").innerHTML="joga a "+KI.girafa;'),
        ("el.textContent=vez;", "el.innerHTML=KI[vez]; el.setAttribute(\"aria-label\",vez);"),
        ('document.getElementById("galoMsg").textContent="GANHOU "+tab[w[0]]+"! 🎉";', 'document.getElementById("galoMsg").innerHTML="GANHOU "+KI[tab[w[0]]]+"! "+KI.festa;'),
        ('vez = vez==="🦒"?"🌙":"🦒";', 'vez = vez==="girafa"?"lua":"girafa";'),
        ('document.getElementById("galoMsg").textContent="joga o "+vez;', 'document.getElementById("galoMsg").innerHTML="joga a "+KI[vez];'),
    ]),
    "neverland_family_quest.html": (["compass", "wand-sparkles", "leaf", "alarm-clock", "camera", "check", "music", "sparkles", "star", "trophy"], [
        ('title: "🧭 Ilha 1: A Bússola das Estrelas"', 'ico: "compass", title: "Ilha 1: A Bússola das Estrelas"'),
        ('title: "🧚 Ilha 2: A Melodia Mágica da Sininho"', 'ico: "wand_sparkles", title: "Ilha 2: A Melodia Mágica da Sininho"'),
        ('title: "🌿 Ilha 3: O Segredo dos Meninos Perdidos"', 'ico: "leaf", title: "Ilha 3: O Segredo dos Meninos Perdidos"'),
        ('title: "⏰ Ilha 4: O Enigma do Crocodilo Tic-Tac"', 'ico: "alarm_clock", title: "Ilha 4: O Enigma do Crocodilo Tic-Tac"'),
        ('title: "📸 Ilha 5: O Retrato da Tripulação Vitoriosa"', 'ico: "camera", title: "Ilha 5: O Retrato da Tripulação Vitoriosa"'),
        ('document.getElementById("islandTitle").textContent = isl.title;',
         'var tIlha=document.getElementById("islandTitle"); tIlha.textContent = isl.title; if(isl.ico) tIlha.insertAdjacentHTML("afterbegin", KI[isl.ico]+" ");'),
        ('d.textContent = (idx < currentIdx ? "✔ " : "") + isl.short;',
         'd.textContent = isl.short; if(idx < currentIdx) d.insertAdjacentHTML("afterbegin", KI.check+" ");'),
        (">🎵 Dó</button>", ">'+KI.music+' Dó</button>"),
        (">✨ Mi</button>", ">'+KI.sparkles+' Mi</button>"),
        (">🌟 Sol</button>", ">'+KI.star+' Sol</button>"),
        (">🧚 Dó Alto</button>", ">'+KI.wand_sparkles+' Dó Alto</button>"),
        (">🏆 Selar Aventura e Abrir Diploma!</button>", ">'+KI.trophy+' Selar Aventura e Abrir Diploma!</button>"),
        ('linhas.push("✔ " + c.step + ": " + c.summary);', 'linhas.push("- " + c.step + ": " + c.summary);'),
    ]),
    "regua_do_planeta.html": ([], [
        ('<h1 id="t1">🌱 Régua do Planeta</h1>', '<h1>🌱 <span id="t1">Régua do Planeta</span></h1>'),
        ('id="btnPlant">🌍 Plantar e calcular!</button>', '>🌍 <span id="btnPlant">Plantar e calcular!</span></button>'),
        ('t1: "🌱 Régua do Planeta"', 't1: "Régua do Planeta"'),
        ('btnPlant: "🌍 Plantar e calcular!"', 'btnPlant: "Plantar e calcular!"'),
        ('t1: "🌱 Planet Ruler"', 't1: "Planet Ruler"'),
        ('btnPlant: "🌍 Plant and calculate!"', 'btnPlant: "Plant and calculate!"'),
        ('fim.toISOString().slice(0,10) + " 🎉";', 'fim.toISOString().slice(0,10);'),
    ]),
    "executor_criancas.html": ([], [
        ('(suficiente?"☀️ CHEGA (com sol a mais!)":"🌧️ NÃO CHEGA — precisas de mais sol ou menos casas")',
         '(suficiente?"CHEGA (com sol a mais!)":"NÃO CHEGA — precisas de mais sol ou menos casas")'),
    ]),
    "chronolex_verify.html": ([], [
        ('rep.linhas.push((ok ? "✓ " : "✗ ") + txt);', 'rep.linhas.push((ok ? "Confere — " : "Não confere — ") + txt);'),
        ('(rep.ok ? "VERDE — documento íntegro" : "VERMELHO — documento adulterado ou inválido");',
         '(rep.ok ? "CONFERE — documento íntegro" : "NÃO CONFERE — documento adulterado ou inválido");'),
    ]),
    "verificador_offline.html": ([], [
        ('igual ? "✓ CONFERE" :', 'igual ? "CONFERE" :'),
    ]),
    "chronolex_photo_seal.html": ([], [
        ('(okH && okS ? "VERDE — fotografia íntegra" : "VERMELHO — adulterada");',
         '(okH && okS ? "CONFERE — fotografia íntegra" : "NÃO CONFERE — adulterada"); el.style.color = (okH && okS) ? "#FF9E7D" : "#F4F7FA";'),
    ]),
    "ficha_campo.html": ([], [
        ('(okM && okS ? "VERDE — ficha íntegra" : "VERMELHO — adulterada");',
         '(okM && okS ? "CONFERE — ficha íntegra" : "NÃO CONFERE — adulterada"); document.getElementById("verif").style.color = (okM && okS) ? "#FF9E7D" : "#F4F7FA";'),
    ]),
    "kcp_art_music_studio.html": ([], [
        ('(okH && okS ? "VERDE — obra íntegra" : "VERMELHO — adulterada");',
         '(okH && okS ? "CONFERE — obra íntegra" : "NÃO CONFERE — adulterada"); document.getElementById("verif").style.color = (okH && okS) ? "#FF9E7D" : "#F4F7FA";'),
    ]),
    "patient_vault_offline.html": ([], [
        ('(okM && okS ? "VERDE — carteira íntegra" : "VERMELHO — carteira adulterada");',
         '(okM && okS ? "CONFERE — carteira íntegra" : "NÃO CONFERE — carteira adulterada"); document.getElementById("verif").style.color = (okM && okS) ? "#FF9E7D" : "#F4F7FA";'),
    ]),
    "testemunha_offline.html": ([], [
        ('var estado = (okA && okB) ? "VERDE — 2/2 assinaturas válidas" : "VERMELHO — assinatura inválida";',
         'var estado = (okA && okB) ? "CONFERE — 2/2 assinaturas válidas" : "NÃO CONFERE — assinatura inválida"; document.getElementById("saidaB").style.color = (okA && okB) ? "#FF9E7D" : "#F4F7FA";'),
    ]),
    "konfirmu_chat_offline.html": (["phone"], [
        ("l.textContent='📞 '+n;", "l.innerHTML=KI.phone+' ';l.appendChild(document.createTextNode(n));"),
        (".v{display:inline-block;font-weight:700;border-radius:6px;padding:1px 8px;margin-bottom:4px;color:#14181f}",
         ".v{display:inline-block;font-weight:700;border-radius:6px;padding:1px 8px;margin-bottom:4px;color:#F4F7FA;border:1px solid #9FB3C8}"),
        (".v.ok{background:var(--pessego)}", ".v.ok{color:#FF9E7D;border-color:#FF9E7D}"),
        (".v.ns{background:var(--ambar)}", ".v.ns{color:#9FB3C8;border-style:dashed}"),
        (".v.veto{background:var(--cinza)}", ".v.veto{color:#F4F7FA}"),
        (".v.ia{background:#c9d2e3}", ".v.ia{color:#9FB3C8}"),
    ]),
    "konfirmu_chat_offline_v0.1.html": (["phone"], [
        ("l.textContent='📞 '+n;", "l.innerHTML=KI.phone+' ';l.appendChild(document.createTextNode(n));"),
        (".v{display:inline-block;font-weight:700;border-radius:6px;padding:1px 8px;margin-bottom:4px;color:#14181f}",
         ".v{display:inline-block;font-weight:700;border-radius:6px;padding:1px 8px;margin-bottom:4px;color:#F4F7FA;border:1px solid #9FB3C8}"),
        (".v.ok{background:var(--pessego)}", ".v.ok{color:#FF9E7D;border-color:#FF9E7D}"),
        (".v.ns{background:var(--ambar)}", ".v.ns{color:#9FB3C8;border-style:dashed}"),
        (".v.veto{background:var(--cinza)}", ".v.veto{color:#F4F7FA}"),
        (".v.ia{background:#c9d2e3}", ".v.ia{color:#9FB3C8}"),
    ]),
    "edicao-21/kcp_family_quiz.html": ([], [
        ("font-size=\"16\">★</text>", "font-size=\"16\">*</text>"),
    ]),
}


MARCA = '<meta name="konfirmu-paleta" content="unica-2026-11-27">'

# depois da conversão: texto que já não se lia na página de origem (medido pela régua AAA do teste)
CORRECOES_POS = {
    "kcp_art_music_studio.html": [
        (".notas button{background:#0B192C;width:44px;padding:10px 0}",
         ".notas button{background:#0B192C;color:#F4F7FA;border:1px solid #FF9E7D;width:44px;padding:10px 0}"),
    ],
    "neverland_family_quest.html": [
        ("background:rgba(255,158,125,.18);color:#FF9E7D;border:1px solid rgba(255,158,125,.4)}",
         "background:rgba(255,158,125,.18);color:#F4F7FA;border:1px solid rgba(255,158,125,.4)}"),
        # o rodapé dos avisos ficava ao lado do jogo, numa segunda coluna estreita, no telemóvel
        ("min-height:100vh;padding:16px;display:flex;justify-content:center;margin:0}",
         "min-height:100vh;padding:16px;display:flex;flex-wrap:wrap;justify-content:center;margin:0}"
         "body>.k-rodape{width:100%;box-sizing:border-box}"),
    ],
    "chronolex_ata.html": [
        ("margin:0;padding:24px 16px;display:flex;justify-content:center}",
         "margin:0;padding:24px 16px;display:flex;flex-wrap:wrap;justify-content:center}"
         "body>.k-rodape{width:100%;box-sizing:border-box}"),
    ],
}


def aplicar_pos(rel, html):
    for antes, depois in CORRECOES_POS.get(rel, []):
        if html.count(depois):
            continue
        if html.count(antes) != 1:
            print("AVISO %s: correção depois da conversão não encontrada: %r" % (rel, antes[:50]))
            continue
        html = html.replace(antes, depois)
    return html


def aplicar_correcoes(rel, html):
    if MARCA in html:
        return html  # já convertida: as trocas de JavaScript não se repetem
    nomes, trocas = CORRECOES_JS.get(rel, ([], []))
    for antes, depois in trocas:
        n = html.count(antes)
        if n != 1:
            if html.count(depois) >= 1:
                continue  # já aplicada (idempotente)
            if n == 0:
                # a página já mudou por outro caminho (ex.: o tema 2040 do main); o portão visual,
                # que corre a seguir, apanha o que tiver ficado fora da paleta ou com emoji
                print("AVISO %s: troca não encontrada, a página já mudou: %r" % (rel, antes[:50]))
                continue
            raise SystemExit("PARADO: %s — esperava 1 ocorrência de %r, encontrei %d" % (rel, antes[:70], n))
        html = html.replace(antes, depois)
    if nomes and "var KI={" not in html:
        html = re.sub(r"(<script\b(?![^>]*\bsrc=)[^>]*>)", lambda m: m.group(1) + ki_js(nomes), html, count=1, flags=re.I)
    return html


def paginas(raiz):
    raiz = Path(raiz)
    lista = sorted(p for p in raiz.glob("*.html")) + sorted((raiz / "edicao-21").glob("*.html"))
    return [p for p in lista if p.is_file()]


def aplicar(raiz):
    raiz = Path(raiz)
    rel_total = []
    mudou = 0
    for p in paginas(raiz):
        rel = p.relative_to(raiz).as_posix()
        if rel in GERADAS:
            continue
        orig = p.read_text(encoding="utf-8")
        html = aplicar_correcoes(rel, orig)
        rel_pag = []
        html = aplicar_pos(rel, converter_html(html, rel_pag))
        if html != orig:
            p.write_text(html, encoding="utf-8")
            mudou += 1
        rel_total += ["%s: %s" % (rel, r) for r in rel_pag]
    css = raiz / "assets" / "imersao.css"
    if css.exists():
        orig = css.read_text(encoding="utf-8")
        novo = converter_css(orig, False)
        if novo != orig:
            css.write_text(novo, encoding="utf-8")
            mudou += 1
    for man in (raiz / "manifest.json", raiz / "edicao-21" / "manifest.json"):
        if man.exists():
            orig = man.read_text(encoding="utf-8")
            novo = re.sub(r'("(?:theme|background)_color"\s*:\s*")[^"]*(")', r"\g<1>#0B192C\2", orig)
            if novo != orig:
                man.write_text(novo, encoding="utf-8")
                mudou += 1
    for r in rel_total:
        print("AVISO", r)
    print("aplicar: %d ficheiros mudaram" % mudou)


# ---------------------------------------------------------------- portão (verificar)
def cores_do_texto(txt):
    for m in RE_COR.finditer(txt):
        tok = m.group(0)
        if tok.startswith("#"):
            # «#» de ids e âncoras (#memo, #t1) não são cores: só conta hex depois de :, =, aspas, vírgula ou (
            antes = txt[max(0, m.start() - 1):m.start()]
            if antes and antes not in ":=\"' ,(\n\t" and not antes.isspace():
                continue
            rgb, alfa = ler_hex(tok)
        else:
            lido = ler_func(m.group(1))
            if not lido:
                continue
            rgb, alfa = lido[0], lido[1]
        yield m.start(), tok, rgb, alfa


def verificar_texto(nome, txt, falhas):
    ehtml = nome.endswith(".html")
    # 1. cores fora da paleta
    sem_comentarios = re.sub(r"<!--.*?-->", "", txt, flags=re.S)
    # ids/âncoras do tipo href="#add" não são cores
    sem_ancoras = re.sub(r'(href|xlink:href|url\()\s*=?\s*["\']?#[\w-]+', "", sem_comentarios)
    sem_ancoras = re.sub(r"getElementById\([^)]*\)|querySelector(All)?\([^)]*\)", "", sem_ancoras)
    for pos, tok, rgb, alfa in cores_do_texto(sem_ancoras):
        if rgb in OFICIAIS:
            if rgb == C:
                viz = sem_ancoras[max(0, pos - 1500):pos + 1500]
                if not re.search(r"112|116\s?111|emerg", viz, re.I):
                    falhas.append("%s: carmesim %s fora do alerta 112/116 111" % (nome, tok))
            continue
        if alfa == 0:
            continue  # transparente: não pinta nada
        falhas.append("%s: cor fora da paleta %s" % (nome, tok))
    if "f7b397" in txt.lower():
        falhas.append("%s: #f7b397 reformado ainda presente" % nome)
    # 2. nomes de cores proibidas, só dentro de CSS (blocos <style>, atributos style="" e ficheiros .css)
    blocos = re.findall(r"<style\b[^>]*>(.*?)</style>", sem_comentarios, re.S | re.I) + \
        re.findall(r'\sstyle\s*=\s*["\']([^"\']*)', sem_comentarios, re.I)
    if nome.endswith(".css"):
        blocos.append(sem_comentarios)
    for bloco in blocos:
        for m in RE_DECL.finditer(bloco):
            if m.group("prop").lower() in ("white-space", "font", "font-family", "content", "animation", "transition"):
                continue
            mm = re.search(r"(?<![\w-])(green|lime|limegreen|darkgreen|purple|violet|yellow|gold|white)(?![\w-])", m.group("val"), re.I)
            if mm and "url(" not in m.group("val"):
                falhas.append("%s: cor por nome %r em %s" % (nome, mm.group(1), m.group("prop")))
    # 3. tema claro
    if re.search(r"prefers-color-scheme\s*:\s*light", txt) or re.search(r"color-scheme\s*:\s*light", txt):
        falhas.append("%s: tema claro (só existe o escuro)" % nome)
    # 4. emojis de sistema (fora de comentários)
    if ehtml or nome.endswith(".js"):
        for m in RE_PICTO.finditer(sem_comentarios):
            if picto(m.group(0)):
                falhas.append("%s: emoji %r" % (nome, m.group(0)))
                break


def verificar(alvo):
    alvo = Path(alvo)
    falhas = []
    ficheiros = {}
    if alvo.suffix == ".zip":
        with zipfile.ZipFile(alvo) as z:
            for n in z.namelist():
                if n.endswith((".html", ".css", ".js", ".json")) and "locales/" not in n:
                    ficheiros[n] = z.read(n).decode("utf-8", "replace")
    else:
        for p in paginas(alvo):
            ficheiros[p.relative_to(alvo).as_posix()] = p.read_text(encoding="utf-8")
        for extra in ("assets/imersao.css", "assets/imersao.js", "sw.js", "konfirmu_chat_sw.js", "manifest.json",
                      "edicao-21/manifest.json"):
            if (alvo / extra).exists():
                ficheiros[extra] = (alvo / extra).read_text(encoding="utf-8")
        for p in sorted((alvo / "assets").glob("*.js")) + sorted((alvo / "assets").glob("*.css")):
            ficheiros.setdefault(p.relative_to(alvo).as_posix(), p.read_text(encoding="utf-8"))
        if not (alvo / "edicao-21").is_dir():
            # outra pasta (ex.: o sítio dpsindustrial.nl/konfirmu/): tudo o que se mostra, menos a versão anterior
            for p in sorted(alvo.rglob("*")):
                rel = p.relative_to(alvo).as_posix()
                if (p.is_file() and p.suffix in (".html", ".css", ".js", ".json", ".svg")
                        and not rel.startswith("_anterior/") and "/locales/" not in "/" + rel):
                    ficheiros.setdefault(rel, p.read_text(encoding="utf-8", errors="replace"))
    for nome, txt in sorted(ficheiros.items()):
        if nome.endswith(".min.js") or nome.endswith("qrcode.js"):
            continue  # bibliotecas de terceiros sem cores de interface
        verificar_texto(nome, txt, falhas)
    return ficheiros, falhas


def main(argv):
    if len(argv) < 2 or argv[1] not in ("aplicar", "verificar"):
        print(__doc__)
        return 2
    raiz = argv[2] if len(argv) > 2 else str(Path(__file__).resolve().parents[1])
    if argv[1] == "aplicar":
        aplicar(raiz)
        return 0
    ficheiros, falhas = verificar(raiz)
    for f in falhas:
        print("FALHA", f)
    print("portão visual: %d ficheiros, %d falhas" % (len(ficheiros), len(falhas)))
    return 1 if falhas else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
