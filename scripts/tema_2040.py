#!/usr/bin/env python3
"""Tema único 2040 da Konfirmu, aplicado às páginas da app (ordem do David, 27-11-2026, 14:53).

Paleta fechada: fundo Azul Abissal #0B192C, vidro rgba(15,34,61,.72), luz e assinatura Pêssego Solar #FF9E7D,
texto Branco Titânio #F4F7FA e Cinza Nevoeiro #9FB3C8. Proibidos: verde, violeta/roxo, amarelo berrante, vermelho
(o carmesim #EF4444 fica só para o alerta real 112 / 116 111) e fundos brancos crus. Zero emojis de sistema:
cada emoji passa a ícone SVG de linha 1,5 px (scripts/icones_2040.py).

O que faz em cada página (sempre o mesmo, e pode correr outra vez sem duplicar nada):
  1. troca as cores fora da paleta por cores da paleta (tabela fixa + regra por luminosidade);
  2. troca os emojis por ícones SVG (no texto) ou tira-os (títulos e atributos); os do JavaScript têm
     substituições escritas à mão, página a página, e o script para se sobrar algum;
  3. junta o bloco «tema-2040» (cores de base, foco, menos movimento, alto contraste), a política de
     segurança (só o próprio sítio: zero chamadas para fora), o rodapé com os 5 avisos legais e o script
     assets/konfirmu-2040.js (Modo Criança com tranca, pausa de movimento, alto contraste).

Uso: python3 -I scripts/tema_2040.py [CAMINHO_DO_REPOSITORIO] [--verificar]
"""
import colorsys
import html
import json
import os
import re
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
import icones_2040  # noqa: E402

ABISSAL, VIDRO_S, FUNDO2, ARESTA = "#0B192C", "#0F223D", "#13294A", "#23395B"
TITANIO, NEVOA = "#F4F7FA", "#9FB3C8"
PESSEGO, PESSEGO_C, PESSEGO_E, PESSEGO_P, TERRA = "#FF9E7D", "#FFB088", "#E8875F", "#FFD3C2", "#A2552F"

# Páginas da app e o portal de cada uma (o Modo Criança só deixa abrir as da família)
PAGINAS = {
    "verificador_offline.html": "pro", "chronolex_photo_seal.html": "pro", "ficha_campo.html": "pro",
    "chronolex_ata.html": "pro", "chronolex_verify.html": "pro", "testemunha_offline.html": "pro",
    "radio_selo.html": "pro", "webrtc_local.html": "pro",
    "konfirmu_chat_offline_v0.1.html": "cid", "konfirmu_chat_offline.html": "cid", "patient_vault_offline.html": "cid",
    "carta_selada.html": "cid", "urna_voto_offline.html": "cid",
    # economia_anti_casino.html (ZCode/GLM, PR #21) fica fora: é autocontida, sem scripts e com política fechada
    "girafinhas_criancas_facil.html": "fam", "edicao-21/Tutor-Girafinha-offline.html": "fam",
    "edicao-21/kcp_family_quiz.html": "fam", "sala_natal_girafinhas.html": "fam", "estudio_video_criancas.html": "fam",
    "executor_criancas.html": "fam", "kcp_art_music_studio.html": "fam", "regua_do_planeta.html": "fam",
    "neverland_family_quest.html": "fam",
    "avisos_legais.html": "info",
    "terminal.html": "pro",
}
OUTROS = ["assets/imersao.css", "assets/imersao.js"]

# ---- 1. cores -------------------------------------------------------------------------------------------
GLOBAL = {
    # fundos escuros
    "#0d1117": ABISSAL, "#071a12": ABISSAL, "#050d09": "#08121F", "#0a1208": ABISSAL, "#090d16": ABISSAL,
    "#121317": ABISSAL, "#14181f": ABISSAL, "#191820": ABISSAL, "#10191d": ABISSAL, "#052e16": ABISSAL,
    "#1a1200": ABISSAL, "#0f172a": ABISSAL,
    # painéis
    "#161b22": VIDRO_S, "#1c222c": VIDRO_S, "#17181d": VIDRO_S, "#0b3d2e": FUNDO2, "#123527": VIDRO_S,
    "#2e4a2e": "#16304F", "#312b33": VIDRO_S, "#1e1b4b": FUNDO2, "#171634": FUNDO2, "#281f22": VIDRO_S,
    "#12391b": VIDRO_S,
    # arestas
    "#2f3947": ARESTA, "#2a2b31": ARESTA, "#44384a": ARESTA, "#202127": ARESTA, "#40375d": ARESTA, "#356340": ARESTA,
    # texto
    "#e6edf3": TITANIO, "#eafbe9": TITANIO, "#f1efe9": TITANIO, "#eceae6": TITANIO, "#e2e8f0": TITANIO,
    "#e0f2fe": TITANIO, "#e8f5e9": TITANIO, "#bae6fd": TITANIO, "#c9d1d9": TITANIO, "#fff": TITANIO,
    "#ffffff": TITANIO, "#f8fafc": TITANIO,
    # texto fraco
    "#8b949e": NEVOA, "#a9b0bb": NEVOA, "#9aa3ad": NEVOA, "#b4b2ad": NEVOA, "#b8c7bd": NEVOA, "#aeb7c1": NEVOA,
    "#94a3b8": NEVOA, "#9e9e9e": NEVOA, "#8d7980": NEVOA, "#776e70": NEVOA, "#66595d": NEVOA,
    # realces (botões) e «confere»
    "#238636": PESSEGO, "#2e7d32": PESSEGO_E, "#4caf50": PESSEGO, "#10b981": PESSEGO, "#16a34a": PESSEGO,
    "#047857": PESSEGO, "#065f46": PESSEGO_C, "#064e3b": PESSEGO_C,
    "#3fb950": PESSEGO, "#6ee7b7": PESSEGO_C, "#a7f3d0": PESSEGO_C, "#81c784": PESSEGO_C, "#a5d6a7": PESSEGO_C,
    "#bbf7d0": PESSEGO_C,
    # amarelos e âmbares
    "#fbbf24": PESSEGO, "#ffb300": PESSEGO, "#ffd54f": PESSEGO_C, "#ffd66e": PESSEGO_C, "#e9b949": PESSEGO_P,
    "#eab308": PESSEGO_E, "#ffdf91": PESSEGO_C, "#ffd97a": PESSEGO_C, "#f59e0b": PESSEGO_E, "#ff8f00": PESSEGO_E,
    "#d97706": PESSEGO_E, "#fde68a": PESSEGO_P, "#fef3c7": PESSEGO_P, "#332409": "#2A1D17",
    # vermelhos («não confere»): pêssego claro, nunca vermelho
    "#f85149": PESSEGO_P, "#fecaca": PESSEGO_P, "#f2a9a0": "#F5B39B", "#dc2626": PESSEGO_E, "#c0392b": PESSEGO_E,
    "#7f1d1d": TERRA, "#ef4444": PESSEGO_E,
    # azul-céu e o pêssego antigo (reformado a 27-11)
    "#38bdf8": PESSEGO, "#f7b397": PESSEGO,
}
RGB_GLOBAL = {
    (10, 40, 28): (15, 34, 61), (255, 213, 79): (255, 158, 125), (129, 199, 132): (255, 176, 136),
    (16, 185, 129): (255, 158, 125), (251, 191, 36): (255, 158, 125), (255, 179, 0): (255, 158, 125),
    (76, 175, 80): (255, 158, 125), (239, 68, 68): (232, 135, 95), (10, 15, 8): (5, 12, 22),
}

# Páginas claras: passam a escuras (tabela própria antes da global)
POR_PAGINA = {
    "girafinhas_criancas_facil.html": {
        "#fef3c7": ABISSAL, "#451a03": TITANIO, "#fbbf24": VIDRO_S, "#78350f": PESSEGO, "#f59e0b": PESSEGO,
        "#fef9c3": FUNDO2, "#eab308": PESSEGO_E, "#bbf7d0": PESSEGO_C, "#16a34a": PESSEGO, "#14532d": ABISSAL,
        "#fecaca": FUNDO2, "#dc2626": TITANIO, "#7f1d1d": TITANIO, "#b45309": PESSEGO_C, "#0f172a": ABISSAL,
        # cena da girafa, de noite
        "#f5e6b8": TITANIO, "#1a1440": ABISSAL, "#ffe9a8": "#FFE2CF", "#3a2a63": FUNDO2, "#4a3578": "#1D3A60",
        "#2f4a35": "#16304F", "#27402c": FUNDO2, "#ffd97a": PESSEGO_C, "#3f6a44": "#1D3A60", "#487a4d": "#26436F",
        "#2e5236": "#16304F", "#e5b763": "#EBB08A", "#f4cd85": "#F7C9A9", "#f8dda3": "#FBE3D0", "#f2a9a0": "#F5B39B",
    },
    "chronolex_ata.html": {
        "#f8fafc": ABISSAL, "#0f172a": TITANIO, "#cbd5e1": ARESTA, "#475569": NEVOA, "#f1f5f9": FUNDO2,
        "#64748b": NEVOA, "#ecfdf5": FUNDO2,
    },
    "edicao-21/Tutor-Girafinha-offline.html": {
        "#fef9e7": ABISSAL, "#333": TITANIO, "#e8f4ea": FUNDO2, "#fdf0d5": VIDRO_S, "#ccc": ARESTA,
        "#2e7d32": PESSEGO, "#eee": FUNDO2, "#fdecea": FUNDO2, "#c0392b": PESSEGO,
    },
    "assets/imersao.css": {"#e8f5e9": TITANIO},
}


def familia(r, g, b):
    mx, mn = max(r, g, b) / 255, min(r, g, b) / 255
    if mx == 0 or ((mx - mn) < 0.06 and (mx - mn) / mx < 0.12):
        return "neutro"
    h = colorsys.rgb_to_hsv(r / 255, g / 255, b / 255)[0] * 360
    if h < 10 or h > 330: return "vermelho"
    if h <= 38: return "pessego"
    if h < 70: return "amarelo"
    if h < 165: return "verde"
    if h < 200: return "azul-petroleo"
    if h <= 240: return "azul"
    return "violeta"


def regra(r, g, b):
    """Cor fora da paleta → cor da paleta, pela luminosidade. Devolve None se a cor já serve."""
    fam = familia(r, g, b)
    if fam in ("neutro", "azul", "pessego"):
        return None
    _, l, s = colorsys.rgb_to_hls(r / 255, g / 255, b / 255)
    if l < 0.10: return "#08121F"
    if l < 0.20: return ABISSAL
    if l < 0.27: return VIDRO_S
    if l < 0.36: return "#16304F"
    if l > 0.90: return TITANIO if fam in ("verde", "azul-petroleo", "violeta") else "#FFE8DA"
    if s < 0.30: return NEVOA if l > 0.5 else "#4A6688"
    if fam in ("verde", "azul-petroleo"): return PESSEGO if l >= 0.45 else PESSEGO_E
    if fam == "violeta": return PESSEGO_C if l >= 0.6 else ("#26436F" if l < 0.45 else NEVOA)
    if fam == "amarelo": return PESSEGO_C if l >= 0.7 else (PESSEGO if l >= 0.5 else PESSEGO_E)
    return PESSEGO_P if l >= 0.75 else (PESSEGO_E if l >= 0.4 else TERRA)  # vermelho


def hex_rgb(h):
    h = h.lstrip("#")
    if len(h) in (3, 4): h = "".join(c * 2 for c in h[:3])
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


RX_HEX = re.compile(r"#([0-9a-fA-F]{8}|[0-9a-fA-F]{6}|[0-9a-fA-F]{3,4})(?![0-9a-zA-Z_-])")
RX_RGB = re.compile(r"(rgba?\(\s*)(\d{1,3})(\s*,\s*|\s+)(\d{1,3})(\s*,\s*|\s+)(\d{1,3})")
ANTES_NAO_COR = re.compile(r"(href=[\"']|&|\$\(\s*[\"']|getElementById\(\s*[\"']|querySelector(All)?\(\s*[\"'][^\"']*|url\(\s*[\"']?)$")


def trocar_cores(texto, mapa):
    def hexs(m):
        antes = texto[max(0, m.start() - 40):m.start()]
        if ANTES_NAO_COR.search(antes):
            return m.group(0)
        bruto = m.group(1)
        if len(bruto) in (3, 4):
            # #abc só conta como cor depois de «:», espaço, vírgula, «(» ou aspas (CSS e SVG)
            if not re.search(r"[:\s,(\"'=]$", antes):
                return m.group(0)
        chave = "#" + bruto.lower()
        alfa = bruto[6:8] if len(bruto) == 8 else (bruto[3] * 2 if len(bruto) == 4 else "")
        base = chave[:7] if len(bruto) == 8 else (chave if len(bruto) in (3, 6) else chave[:4])
        if base in mapa:
            novo = mapa[base]
        else:
            novo = regra(*hex_rgb(base))
            if novo is None:
                return m.group(0)
        return novo + (alfa.upper() if alfa else "")

    texto = RX_HEX.sub(hexs, texto)

    def rgbs(m):
        r, g, b = int(m.group(2)), int(m.group(4)), int(m.group(6))
        if (r, g, b) in RGB_GLOBAL:
            nr, ng, nb = RGB_GLOBAL[(r, g, b)]
        else:
            novo = regra(min(r, 255), min(g, 255), min(b, 255))
            if novo is None:
                return m.group(0)
            nr, ng, nb = hex_rgb(novo)
        return "%s%d%s%d%s%d" % (m.group(1), nr, m.group(3), ng, m.group(5), nb)

    return RX_RGB.sub(rgbs, texto)


def luminancia(cor):
    def canal(c):
        c = c / 255
        return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
    r, g, b = hex_rgb(cor)
    return 0.2126 * canal(r) + 0.7152 * canal(g) + 0.0722 * canal(b)


RX_REGRA = re.compile(r"([^{}]*)\{([^{}]*)\}")


def texto_escuro_em_fundo_claro(css):
    """Onde o fundo passou a pêssego (claro) e a letra ficou clara, a letra passa a Azul Abissal."""
    def uma(m):
        corpo = m.group(2)
        fundo = re.search(r"background(?:-color)?\s*:\s*([^;]*)", corpo)
        letra = re.search(r"(?<![-\w])color\s*:\s*(#[0-9a-fA-F]{3,8})", corpo)
        if not fundo or not letra:
            return m.group(0)
        cores = re.findall(r"#[0-9a-fA-F]{6}", fundo.group(1))
        if not cores or min(luminancia(c) for c in cores) < 0.35:
            return m.group(0)
        if luminancia(letra.group(1)[:7] if len(letra.group(1)) >= 7 else letra.group(1)) > 0.5:
            corpo = corpo[:letra.start(1)] + ABISSAL + corpo[letra.end(1):]
        return m.group(1) + "{" + corpo + "}"
    return RX_REGRA.sub(uma, css)


def estilos_inline(texto):
    def uma(m):
        return m.group(1) + texto_escuro_em_fundo_claro("x{" + m.group(2) + "}")[2:-1] + m.group(3)
    return re.sub(r'(style=")([^"]*)(")', uma, texto)


# ---- 2. emojis ------------------------------------------------------------------------------------------
def e_pict(ch):
    cp = ord(ch)
    if cp in (0x00A9, 0x00AE, 0x2122):
        return False
    return icones_varrer.e_pict(cp)


class _Varrer:
    """Partilha a definição de emoji com a verificação (ferramentas/verificar_pacote.py)."""
    def __init__(self):
        sys.path.insert(0, os.path.join(os.path.dirname(AQUI), "ferramentas"))
        import verificar_pacote
        self.v = verificar_pacote

    def e_pict(self, cp):
        return self.v.e_pict(cp)


icones_varrer = None

BANDEIRAS = {"\U0001F1F5\U0001F1F9": "PT", "\U0001F1EC\U0001F1E7": "EN"}


def grupos_emoji(texto):
    """Devolve [(início, fim, grupo)] de cada emoji (com seletores, ZWJ, tons de pele e bandeiras)."""
    out, i, n = [], 0, len(texto)
    while i < n:
        ch = texto[i]; cp = ord(ch)
        if 0x1F1E6 <= cp <= 0x1F1FF and i + 1 < n and 0x1F1E6 <= ord(texto[i + 1]) <= 0x1F1FF:
            out.append((i, i + 2, texto[i:i + 2])); i += 2; continue
        if e_pict(ch) or cp in (0xFE0F, 0x20E3):
            j = i + 1
            while j < n:
                c = ord(texto[j])
                if c in (0xFE0F, 0x20E3) or 0x1F3FB <= c <= 0x1F3FF:
                    j += 1
                elif c == 0x200D and j + 1 < n and e_pict(texto[j + 1]):
                    j += 2
                else:
                    break
            out.append((i, j, texto[i:j])); i = j; continue
        i += 1
    return out


def icone_de(grupo):
    base = grupo.replace("️", "").split("‍")[0]
    return icones_2040.EMOJI_PARA_ICONE.get(base)


def trocar_emojis_texto(seg, onde):
    partes, ultimo = [], 0
    for a, b, g in grupos_emoji(seg):
        partes.append(seg[ultimo:a])
        if g in BANDEIRAS:
            partes.append(BANDEIRAS[g])
        else:
            nome = icone_de(g)
            if not nome:
                raise SystemExit("%s: emoji sem ícone: %r" % (onde, g))
            partes.append(icones_2040.svg(nome))
        ultimo = b
        # tira o espaço logo a seguir ao ícone (o ícone já tem margem)
        if ultimo < len(seg) and seg[ultimo] == " " and nome_ok(g):
            ultimo += 1
    partes.append(seg[ultimo:])
    return "".join(partes)


def nome_ok(g):
    return g not in BANDEIRAS


def tirar_emojis(seg):
    out, ultimo = [], 0
    for a, b, g in grupos_emoji(seg):
        out.append(seg[ultimo:a])
        if g in BANDEIRAS:
            out.append(BANDEIRAS[g])
        ultimo = b
        while ultimo < len(seg) and seg[ultimo] == " " and (not out or not out[-1] or out[-1].endswith((" ", ">", '"'))):
            ultimo += 1
    out.append(seg[ultimo:])
    return "".join(out)


RX_PEDACOS = re.compile(r"(<script\b[^>]*>.*?</script>|<style\b[^>]*>.*?</style>|<!--.*?-->|<title>.*?</title>|<[^>]+>)", re.S | re.I)


def trocar_emojis_html(texto, onde):
    pedacos = RX_PEDACOS.split(texto)
    out = []
    for p in pedacos:
        if not p:
            continue
        baixo = p[:8].lower()
        if baixo.startswith("<script") or baixo.startswith("<style") or p.startswith("<!--"):
            out.append(p)
        elif baixo.startswith("<title>"):
            out.append(tirar_emojis(p))
        elif p.startswith("<"):
            out.append(tirar_emojis(p))
        else:
            out.append(trocar_emojis_texto(p, onde))
    return "".join(out)


def ki(nome, classe="ki"):
    """Ícone em texto JavaScript (aspas simples escapadas não são precisas: o SVG só usa aspas duplas)."""
    return icones_2040.svg(nome, classe)


# Substituições escritas à mão (texto exato → texto novo, quantas vezes tem de aparecer)
def substituicoes():
    G, F, FL, T, C = ki("girafa"), ki("folha"), ki("flor"), ki("tigela", "ki ki-g"), ki("coracao", "ki ki-g")
    S = {
        "girafinhas_criancas_facil.html": [
            (".speak-btn { background: #fff;", ".speak-btn { background: #13294A; color: #F4F7FA;", 1),
            (".game-card { background: #fff;", ".game-card { background: rgba(15,34,61,.72);", 1),
            (".bowl.counted { background: #bbf7d0; border-color: #16a34a; }",
             ".bowl.counted { background: #bbf7d0; border-color: #16a34a; color: #0B192C; box-shadow: 0 0 22px rgba(255,158,125,.55); }", 1),
            (".bowl { font-size: 2.1rem;", ".bowl { color: #FFB088; font-size: 2.1rem;", 1),
            (".ruler-diff { background: #fecaca; border: 4px solid #dc2626;", ".ruler-diff { background: #fecaca; border: 4px dashed #dc2626;", 1),
            ("btn.textContent = idx===7 ? '🥣💙' : '🥣';",
             "btn.setAttribute('aria-label','Tigela '+(idx+1)); btn.innerHTML = idx===7 ? '%s%s' : '%s';" % (T, C, T), 1),
            ("counted + ' de 8 ⭐'", "counted + ' de 8'", 1),
            ("box.innerHTML='🦒🌿 = 🦒🌿<br>IGUAL!'", "box.innerHTML='%s%s = %s%s<br>IGUAL!'" % (G, F, G, F), 1),
            ("box.innerHTML='🦒🌿 ≠ 🦒🌸<br>DIFERENTE!'", "box.innerHTML='%s%s ≠ %s%s<br>DIFERENTE!'" % (G, F, G, FL), 1),
            ("toca em cada tigela amarela para contar até oito", "toca em cada tigela para contar até oito", 1),
            ("toca no botão azul para ver", "toca no botão grande para ver", 1),
        ],
        "chronolex_ata.html": [
            (".doc{width:100%;max-width:780px;background:#fff;", ".doc{width:100%;max-width:780px;background:rgba(15,34,61,.72);", 1),
            (".btn-add{background:#0f172a;color:#fff}", ".btn-add{background:#FF9E7D;color:#0B192C}", 1),
            (".btn-seal{background:#047857;color:#fff;", ".btn-seal{background:#047857;color:#0B192C;", 1),
            ("border-bottom:2px solid #0f172a", "border-bottom:2px solid #FF9E7D", 1),
            ("@media print{.no-print{display:none}.doc{box-shadow:none;border:none}}",
             "@media print{.no-print{display:none}.doc{box-shadow:none;border:none}html,body,.doc,.entry,.seal-box{background:#FFFFFF!important;color:#000000!important}}", 1),
        ],
        "edicao-21/Tutor-Girafinha-offline.html": [
            ("button{background:#2e7d32;color:#fff;", "button{background:#2e7d32;color:#0B192C;", 1),
            ("#ajuda{background:#8b321e;", "#ajuda{background:#8b321e;color:#F4F7FA;", 1),
        ],
        "carta_selada.html": [('style="background:#111;color:#fff"', 'style="background:#0F223D;color:#F4F7FA;border:1px solid #FF9E7D"', 1)],
        "edicao-21/kcp_family_quiz.html": [
            ("\'<text x=\"\'+(x?72:20)+\'\" y=\"\'+(y?78:32)+\'\" font-size=\"16\">★</text>\'",
             "\'<path transform=\"translate(\'+(x?72:20)+\' \'+(y?66:20)+\')\" d=\"m6 0 1.8 3.9 4.2.5-3.1 2.9.8 4.2L6 9.4l-3.7 2.1.8-4.2L0 4.4l4.2-.5z\" fill=\"#FF9E7D\"/>\'", 1),
        ],
        "konfirmu_chat_offline.html": [
            ("l.textContent='📞 '+n;", "l.textContent='Ligar '+n;", 1),
            ("bolha('eu','♪ '+m);", "bolha('eu','Pelo som: '+m);", 1),
        ],
        "konfirmu_chat_offline_v0.1.html": [
            ("l.textContent='📞 '+n;", "l.textContent='Ligar '+n;", 1),
            ("bolha('eu','♪ '+m);", "bolha('eu','Pelo som: '+m);", 1),
        ],
        "executor_criancas.html": [
            ('"☀️ CHEGA (com sol a mais!)"', '"CHEGA (com sol a mais!)"', 1),
            ('"🌧️ NÃO CHEGA', '"NÃO CHEGA', 1),
        ],
        "regua_do_planeta.html": [
            ('t1: "🌱 Régua do Planeta"', 't1: "Régua do Planeta"', 1),
            ('btnPlant: "🌍 Plantar e calcular!"', 'btnPlant: "Plantar e calcular!"', 1),
            ('t1: "🌱 Planet Ruler"', 't1: "Planet Ruler"', 1),
            ('btnPlant: "🌍 Plant and calculate!"', 'btnPlant: "Plant and calculate!"', 1),
            ('.toISOString().slice(0,10) + " 🎉"', '.toISOString().slice(0,10)', 1),
        ],
        "neverland_family_quest.html": [
            ('title: "🧭 Ilha 1:', 'title: "Ilha 1:', 1),
            ('title: "🧚 Ilha 2:', 'title: "Ilha 2:', 1),
            ('title: "🌿 Ilha 3:', 'title: "Ilha 3:', 1),
            ('title: "⏰ Ilha 4:', 'title: "Ilha 4:', 1),
            ('title: "📸 Ilha 5:', 'title: "Ilha 5:', 1),
            ('(idx < currentIdx ? "✔ " : "")', '(idx < currentIdx ? "Feito · " : "")', 1),
            ('linhas.push("✔ " + c.step', 'linhas.push("Feito: " + c.step', 1),
            (">🎵 Dó</button>", ">%sDó</button>" % ki("nota"), 1),
            (">✨ Mi</button>", ">%sMi</button>" % ki("brilho"), 1),
            (">🌟 Sol</button>", ">%sSol</button>" % ki("estrela"), 1),
            (">🧚 Dó Alto</button>", ">%sDó Alto</button>" % ki("varinha"), 1),
            ('">🏆 Selar Aventura e Abrir Diploma!</button>', '">%sSelar Aventura e Abrir Diploma!</button>' % ki("taca"), 1),
        ],
    }
    return S


def substituir_jogos_natal(texto):
    """Sala de Natal: memória e jogo do galo deixam de usar emojis como peças; passam a ícones SVG."""
    simbolos = ["girafa", "globo", "gota", "sol", "radio", "escudo"]
    lista = ",".join("'%s'" % ki(n, "ki ki-peca") for n in simbolos)
    trocas = [
        ('var emojis=["🦒","🌍","💧","☀️","📻","🛡️"]', "var emojis=[%s]" % lista, 1),
        ('b.textContent="❓";', 'b.innerHTML=\'%s\';' % ki("pergunta", "ki ki-peca"), 1),
        ('botoes[a].textContent="❓"; botoes[c].textContent="❓";',
         'botoes[a].innerHTML=\'%s\'; botoes[c].innerHTML=\'%s\';' % (ki("pergunta", "ki ki-peca"), ki("pergunta", "ki ki-peca")), 1),
        ('vez="🦒";', 'vez="girafa";', 2),
        ('textContent="joga a 🦒"', 'textContent="joga a girafa"', 1),
        ('"GANHOU "+tab[w[0]]+"! 🎉"', '"GANHOU A "+tab[w[0]].toUpperCase()+"!"', 1),
        ('vez = vez==="🦒"?"🌙":"🦒";', 'vez = vez==="girafa"?"lua":"girafa";', 1),
    ]
    for antigo, novo, n in trocas:
        if texto.count(antigo) != n:
            raise SystemExit("sala_natal_girafinhas.html: esperava %d× %r, encontrei %d" % (n, antigo, texto.count(antigo)))
        texto = texto.replace(antigo, novo)
    return texto


# ---- 3. bloco do tema, segurança e rodapé --------------------------------------------------------------
CSS_TEMA = """:root{color-scheme:dark;--k-abissal:#0B192C;--k-vidro:rgba(15,34,61,.72);--k-vidro-s:#0F223D;--k-pessego:#FF9E7D;--k-pessego-c:#FFB088;--k-titanio:#F4F7FA;--k-nevoa:#9FB3C8;--k-aresta:rgba(244,247,250,.14)}
html{background:#0B192C;-webkit-text-size-adjust:100%}
body{background-color:#0B192C;color:#F4F7FA}
a{color:#FF9E7D}a:visited{color:#FFB088}
:focus-visible{outline:2px solid #FF9E7D;outline-offset:2px}
::selection{background:rgba(255,158,125,.35);color:#F4F7FA}
input:not([type]),input[type=text],input[type=search],input[type=number],input[type=password],input[type=email],input[type=tel],input[type=url],textarea,select{background-color:#0B192C;color:#F4F7FA;border:1px solid rgba(244,247,250,.22);border-radius:8px}
input::placeholder,textarea::placeholder{color:#9FB3C8;opacity:1}
.ki{display:inline-block;width:1.1em;height:1.1em;vertical-align:-.17em;margin-inline-end:.35em;flex:none}
h1 .ki,h2 .ki,h3 .ki,b>.ki,strong>.ki,.card-label .ki{color:#FF9E7D}
.ki-g{width:1.35em;height:1.35em;margin:0}.ki-peca{width:62%;height:62%;margin:0;vertical-align:middle}
.k-rodape{max-width:760px;margin:28px auto 8px;padding:14px 16px 10px;border-top:1px solid rgba(244,247,250,.14);color:#9FB3C8;font:400 .8125rem/1.5 system-ui,-apple-system,"Segoe UI",Roboto,sans-serif;text-align:start}
.k-rodape .k-acoes{display:flex;flex-wrap:wrap;gap:8px;margin:0 0 10px}
.k-rodape .k-acoes button,.k-rodape .k-acoes a{min-height:40px;padding:0 14px;border:1px solid rgba(244,247,250,.2);border-radius:10px;background:rgba(15,34,61,.72);color:#F4F7FA;font:600 .8125rem/40px system-ui,sans-serif;text-decoration:none;cursor:pointer;margin:0}
.k-rodape .k-acoes button[aria-pressed="true"]{border-color:#FF9E7D;color:#FF9E7D}
.k-rodape dl{margin:0;display:grid;gap:2px 10px}.k-rodape dt{color:#F4F7FA;font-weight:650}.k-rodape dd{margin:0 0 6px}
.k-rodape .k-marca{margin:8px 0 0}.k-rodape .k-marca b{color:#F4F7FA}.k-rodape .k-marca b span{color:#FF9E7D}
@media (prefers-reduced-motion:reduce){*,*::before,*::after{animation-duration:.001ms!important;animation-iteration-count:1!important;transition-duration:.001ms!important;scroll-behavior:auto!important}}
html.k-sem-movimento *,html.k-sem-movimento *::before,html.k-sem-movimento *::after{animation-play-state:paused!important;transition:none!important}
html.k-contraste{--k-nevoa:#E6ECF3}html.k-contraste body{background-color:#050C16;color:#FFFFFF}html.k-contraste .k-rodape{color:#E6ECF3}
html.k-contraste a{color:#FFC2A8}html.k-contraste .aviso,html.k-contraste .hash,html.k-contraste .meta{color:#E6ECF3!important}"""

CSP_BASE = ("default-src 'self'; script-src 'self' 'unsafe-inline' blob:%s; style-src 'self' 'unsafe-inline'; "
            "img-src 'self' data: blob:; media-src 'self' data: blob: mediastream:; connect-src 'self' blob: data:; "
            "worker-src 'self' blob:; font-src 'self' data:; frame-src 'self' blob:; object-src 'none'; "
            "base-uri 'none'; form-action 'none'")


def csp(caminho):
    # a IA local do chat (Camada 1, só com consentimento) compila WebAssembly
    extra = " 'wasm-unsafe-eval'" if "chat_offline" in caminho else ""
    politica = CSP_BASE % extra
    if caminho == "terminal.html":  # o terminal não fala com a rede, nem com o próprio sítio
        politica = politica.replace("connect-src 'self' blob: data:", "connect-src 'none'").replace("worker-src 'self' blob:", "worker-src 'self'")
    return politica


def bloco_cabeca(caminho, portal):
    return ("<!-- tema-2040:inicio -->\n"
            '<meta name="color-scheme" content="dark">\n'
            '<meta name="theme-color" content="#0B192C">\n'
            '<meta name="konfirmu-portal" content="%s">\n'
            '<meta http-equiv="Content-Security-Policy" content="%s">\n'
            '<style id="tema-2040">\n%s\n</style>\n'
            "<!-- tema-2040:fim -->" % (portal, csp(caminho), CSS_TEMA))


def rodape(avisos, prefixo):
    linhas = ['<!-- rodape-2040:inicio -->', '<footer class="k-rodape" id="k-rodape">',
              '<div class="k-acoes" id="k-acoes"><a href="%sapp_unica.html">Início</a></div>' % prefixo,
              '<dl aria-label="Avisos legais">']
    for t, d in avisos:
        linhas.append("<dt>%s</dt><dd>%s</dd>" % (html.escape(t), html.escape(d)))
    linhas += ['</dl>',
               '<p class="k-marca"><b>Konfirmu</b> · DPS Industrial &amp; Maritime Services · código aberto EUPL-1.2</p>',
               '</footer>', '<script defer src="%sassets/konfirmu-2040.js"></script>' % prefixo, '<!-- rodape-2040:fim -->']
    return "\n".join(linhas)


RX_BLOCO_CAB = re.compile(r"<!-- tema-2040:inicio -->.*?<!-- tema-2040:fim -->", re.S)
RX_BLOCO_ROD = re.compile(r"<!-- rodape-2040:inicio -->.*?<!-- rodape-2040:fim -->", re.S)


def injetar(texto, caminho, portal, avisos):
    # a CSP antiga sai (fica a nova, que só deixa o próprio sítio)
    texto = re.sub(r'<meta http-equiv="Content-Security-Policy" content="[^"]*">\s*', "", texto) if "tema-2040:inicio" not in texto else texto
    cab = bloco_cabeca(caminho, portal)
    if RX_BLOCO_CAB.search(texto):
        texto = RX_BLOCO_CAB.sub(lambda m: cab, texto, count=1)
    else:
        i = texto.lower().rfind("</head>")
        if i < 0:
            # páginas sem <head> escrito (o navegador cria-o): o bloco entra antes do primeiro <style> ou <script>
            m = re.search(r"<(style|script)\b", texto, re.I)
            if not m:
                raise SystemExit("%s: sem </head> nem <style>" % caminho)
            i = m.start()
        texto = texto[:i] + cab + "\n" + texto[i:]
    prefixo = "../" if "/" in caminho and not caminho.startswith("assets/") else "./"
    prefixo = "./"  # no pacote todas as páginas ficam na mesma pasta
    rod = rodape(avisos, prefixo)
    if portal == "info":
        rod = rod.replace('<dl aria-label="Avisos legais">', '<dl aria-label="Avisos legais" hidden>')
    if RX_BLOCO_ROD.search(texto):
        texto = RX_BLOCO_ROD.sub(lambda m: rod, texto, count=1)
    else:
        i = texto.lower().rfind("</body>")
        if i < 0:
            i = texto.lower().rfind("</html>")
        if i < 0:
            raise SystemExit("%s: sem </body> nem </html>" % caminho)
        texto = texto[:i] + rod + "\n" + texto[i:]
    return texto


def aplicar(repo, caminho, avisos):
    p = os.path.join(repo, caminho)
    texto = open(p, encoding="utf-8").read()
    original = texto
    primeira = "tema-2040:inicio" not in texto  # as substituições à mão só correm na primeira vez
    for antigo, novo, n in (substituicoes().get(caminho, []) if primeira else []):
        if n and texto.count(antigo) != n and novo not in texto:
            raise SystemExit("%s: esperava %d× %r, encontrei %d" % (caminho, n, antigo, texto.count(antigo)))
        texto = texto.replace(antigo, novo)
    if caminho == "sala_natal_girafinhas.html" and "ki-peca" not in texto:
        texto = substituir_jogos_natal(texto)
    mapa = dict(GLOBAL)
    mapa.update(POR_PAGINA.get(caminho, {}))
    texto = trocar_cores(texto, mapa)
    if caminho.endswith((".html", ".css")):
        texto = re.sub(r"<style\b[^>]*>.*?</style>", lambda m: texto_escuro_em_fundo_claro(m.group(0)), texto, flags=re.S) if caminho.endswith(".html") else texto_escuro_em_fundo_claro(texto)
        texto = estilos_inline(texto)
    if caminho.endswith(".html"):
        texto = trocar_emojis_html(texto, caminho)
        texto = injetar(texto, caminho, PAGINAS[caminho], avisos)
    restam = grupos_emoji(texto)
    if restam:
        raise SystemExit("%s: ficaram emojis: %r" % (caminho, [g for _, _, g in restam][:10]))
    if texto != original:
        with open(p, "w", encoding="utf-8") as f:
            f.write(texto)
    return texto != original


def main():
    global icones_varrer
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    repo = args[0] if args else os.path.dirname(AQUI)
    icones_varrer = _Varrer()
    import gerar_menu
    avisos = gerar_menu.avisos_pt(repo)
    mudou = 0
    for caminho in list(PAGINAS) + OUTROS:
        if aplicar(repo, caminho, avisos):
            mudou += 1
            print("tema 2040:", caminho)
    print("páginas mudadas: %d de %d" % (mudou, len(PAGINAS) + len(OUTROS)))


if __name__ == "__main__":
    main()
