#!/usr/bin/env python3
"""Ícones de linha da Konfirmu (paleta 2040): SVG 24×24, traço 1,5 px, cor do texto (currentColor).

Regra do David (27-11-2026, 12:49): zero emojis de sistema em títulos, botões, menus e estados;
ícones só em SVG de linha 1,5 px (pêssego ou branco titânio) ou os renders 3D oficiais.

Este ficheiro é a fonte única dos ícones que substituem os emojis nas páginas.
Uso: from icones_2040 import svg, EMOJI_PARA_ICONE
"""

ICONES = {
    "girafa": '<path d="M9.2 21v-8.6L6.6 10.3l.6-2.1 2.3.4 1.2-3.4h1.9l.7 2.6 2.4-.3.5 2.3-2.6 1.7V21"/>'
              '<path d="M11 4.9V3.2M12.9 4.9V3.2"/><circle cx="11.3" cy="13.4" r=".55"/><circle cx="12.4" cy="16.6" r=".55"/>'
              '<circle cx="11" cy="19" r=".55"/>',
    "folha": '<path d="M5 19c0-8 5-13 14-14-1 9-6 14-14 14z"/><path d="M5 19 13 11"/>',
    "flor": '<circle cx="12" cy="12" r="2"/><path d="M12 10c-2-3-2-5 0-6 2 1 2 3 0 6zM14 12c3-2 5-2 6 0-1 2-3 2-6 0zM12 14c2 3 2 5 0 6-2-1-2-3 0-6zM10 12c-3 2-5 2-6 0 1-2 3-2 6 0z"/>',
    "estrela": '<path d="m12 3 2.6 5.6 6 .7-4.5 4.1 1.2 6L12 16.4l-5.3 3 1.2-6-4.5-4.1 6-.7z"/>',
    "brilho": '<path d="M12 4c.8 4 2 5.2 6 6-4 .8-5.2 2-6 6-.8-4-2-5.2-6-6 4-.8 5.2-2 6-6z"/><path d="M19 3v3M17.5 4.5h3"/>',
    "mao": '<path d="M9 11V5a1.5 1.5 0 0 1 3 0v5"/><path d="M12 10V9a1.5 1.5 0 0 1 3 0v2M15 10.5a1.5 1.5 0 0 1 3 0V15a6 6 0 0 1-6 6h-1a6 6 0 0 1-5-2.7L4 15.5a1.5 1.5 0 0 1 2.5-1.6L9 16"/>',
    "coracao": '<path d="M12 20s-7-4.4-7-10a4 4 0 0 1 7-2.6A4 4 0 0 1 19 10c0 5.6-7 10-7 10z"/>',
    "regua": '<rect x="3" y="8" width="18" height="8" rx="1.5"/><path d="M7 8v3M10.5 8v4M14 8v3M17.5 8v4"/>',
    "som": '<path d="M4 10v4h3l5 4V6L7 10z"/><path d="M16 9a4 4 0 0 1 0 6M18.5 6.5a8 8 0 0 1 0 11"/>',
    "tigela": '<path d="M3 11h18a9 9 0 0 1-18 0z"/><path d="M8 20.5h8"/>',
    "arvore": '<path d="M12 3 6.5 10.5h3l-4 6.5h13l-4-6.5h3z"/><path d="M12 17v4"/>',
    "cerebro": '<path d="M9 4.5a3 3 0 0 0-3 3 3 3 0 0 0-2 5 3 3 0 0 0 2 4.5 3 3 0 0 0 6 1.5V5.5a3 3 0 0 0-3-1z"/>'
               '<path d="M15 4.5a3 3 0 0 1 3 3 3 3 0 0 1 2 5 3 3 0 0 1-2 4.5 3 3 0 0 1-6 1.5"/>',
    "circulo": '<circle cx="12" cy="12" r="7"/>',
    "taca": '<path d="M8 4h8v5a4 4 0 0 1-8 0z"/><path d="M8 6H5.5a3 3 0 0 0 2.8 4M16 6h2.5a3 3 0 0 1-2.8 4M12 13v4M8 20h8M9.5 17h5"/>',
    "impressora": '<path d="M7 9V4h10v5"/><rect x="4" y="9" width="16" height="7" rx="1.5"/><path d="M7 14h10v6H7z"/>',
    "globo": '<circle cx="12" cy="12" r="9"/><path d="M3 12h18"/><path d="M12 3a14 14 0 0 1 0 18M12 3a14 14 0 0 0 0 18"/>',
    "gota": '<path d="M12 3s6 6.5 6 11a6 6 0 0 1-12 0c0-4.5 6-11 6-11z"/>',
    "sol": '<circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M2 12h2M20 12h2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"/>',
    "chuva": '<path d="M7 15a4 4 0 0 1 .5-8 5 5 0 0 1 9.5 1.5A3.5 3.5 0 0 1 17 15z"/><path d="M8 18l-1 2.5M12 18l-1 2.5M16 18l-1 2.5"/>',
    "radio": '<rect x="3" y="8" width="18" height="12" rx="2"/><path d="M7 8 17 4"/><circle cx="8" cy="14" r="2.5"/><path d="M14 12.5h4M14 15.5h4"/>',
    "escudo": '<path d="M12 3 5 6v5c0 4.5 3 8.3 7 10 4-1.7 7-5.5 7-10V6z"/>',
    "lua": '<path d="M20 14.5A8 8 0 1 1 9.5 4a6.5 6.5 0 0 0 10.5 10.5z"/>',
    "pergunta": '<circle cx="12" cy="12" r="9"/><path d="M9.5 9.5a2.5 2.5 0 1 1 3.5 2.3c-.7.3-1 .9-1 1.7v.5"/><path d="M12 17h.01"/>',
    "festa": '<path d="M4 20 8.5 8.5l7 7z"/><path d="M14 4v2M18 8h2M16.5 5.5 18 4M13 9c1.5-1.5 3-1 4 0"/>',
    "envelope": '<rect x="3" y="6" width="18" height="13" rx="1.5"/><path d="m3.5 7 8.5 6.5L20.5 7"/>',
    "cadeado": '<rect x="5" y="10" width="14" height="10" rx="2"/><path d="M8 10V7a4 4 0 0 1 8 0v3"/><path d="M12 14v2.5"/>',
    "cadeado_aberto": '<rect x="5" y="10" width="14" height="10" rx="2"/><path d="M8 10V7a4 4 0 0 1 7.6-1.7"/><path d="M12 14v2.5"/>',
    "caneta": '<path d="M4 20h4L19 9l-4-4L4 16z"/><path d="M13 7l4 4"/>',
    "certo": '<path d="m5 12.5 4.5 4.5L19 7.5"/>',
    "guardar": '<path d="M5 4h11l3 3v13H5z"/><path d="M8 4v5h7V4M8 20v-6h8v6"/>',
    "camara": '<path d="M4 8h3l2-3h6l2 3h3a1 1 0 0 1 1 1v9a1 1 0 0 1-1 1H4a1 1 0 0 1-1-1V9a1 1 0 0 1 1-1z"/><circle cx="12" cy="13" r="3.5"/>',
    "lupa": '<circle cx="10.5" cy="10.5" r="6"/><path d="m15 15 5 5"/>',
    "claquete": '<rect x="3" y="9" width="18" height="11" rx="1.5"/><path d="M3 9l1.6-4.6 16 2-1 2.6M8.4 4.9 7.2 8.8M13.4 5.6l-1.2 3.6M18.2 6.2l-1 2.8"/>',
    "video": '<rect x="3" y="7" width="13" height="10" rx="1.5"/><path d="m16 11 5-3v8l-5-3z"/>',
    "parar": '<rect x="6" y="6" width="12" height="12" rx="1.5"/>',
    "tocar": '<path d="M8 5v14l11-7z"/>',
    "prancheta": '<rect x="5" y="4" width="14" height="17" rx="2"/><path d="M9 4h6v3H9z"/><path d="M8.5 11h7M8.5 14.5h7M8.5 18h4"/>',
    "estetoscopio": '<path d="M6 3v6a4 4 0 0 0 8 0V3"/><path d="M10 13v2a5 5 0 0 0 10 0v-2"/><circle cx="20" cy="11" r="2"/>',
    "microfone": '<rect x="9" y="3" width="6" height="11" rx="3"/><path d="M5 11a7 7 0 0 0 14 0M12 18v3M9 21h6"/>',
    "pessoas": '<circle cx="8.5" cy="8" r="3"/><circle cx="16" cy="9" r="2.5"/><path d="M3 19c.6-3.3 2.9-5 5.5-5s4.9 1.7 5.5 5"/><path d="M14.5 14.2c.5-.1 1-.2 1.5-.2 2.2 0 4 1.4 4.5 4.5"/>',
    "urna": '<path d="M5 11h14v9H5z"/><path d="M9 11V5h6v6"/><path d="M8 15h8"/>',
    "receber": '<path d="M4 13h4l2 3h4l2-3h4v6H4z"/><path d="M12 3v9M8.5 8.5 12 12l3.5-3.5"/>',
    "antena": '<path d="M4 20h7M7.5 20l2-5"/><path d="M5 11a7 7 0 0 0 8 8z"/><path d="M14 10l4-4M15 4a5 5 0 0 1 5 5"/>',
    "paleta": '<path d="M12 3a9 9 0 1 0 0 18c1.1 0 1.5-.8 1.5-1.6 0-.5-.2-.9-.5-1.3-.3-.4-.5-.8-.5-1.3 0-1 .8-1.8 1.8-1.8H17a4 4 0 0 0 4-4c0-4.4-4-8-9-8z"/><circle cx="7.5" cy="11" r="1"/><circle cx="10" cy="7.5" r="1"/><circle cx="14.5" cy="7.5" r="1"/>',
    "nota": '<path d="M9 18V5l11-2v13"/><circle cx="6.5" cy="18" r="2.5"/><circle cx="17.5" cy="16" r="2.5"/>',
    "lampada": '<path d="M9 18h6M10 21h4"/><path d="M12 3a6 6 0 0 0-3.5 10.9c.6.5 1 1.2 1 2.1v.5h5V16c0-.9.4-1.6 1-2.1A6 6 0 0 0 12 3z"/>',
    "robo": '<rect x="5" y="8" width="14" height="11" rx="2"/><path d="M12 4.5V8M9 13h.01M15 13h.01M9 16h6"/><circle cx="12" cy="3.5" r="1"/>',
    "rebento": '<path d="M12 21v-8"/><path d="M12 13c0-4-3-6-7-6 0 4 3 6 7 6zM12 11c0-3.5 2.5-5.5 6.5-5.5 0 3.5-2.5 5.5-6.5 5.5z"/>',
    "crianca": '<circle cx="12" cy="6" r="3"/><path d="M6 21v-3a6 6 0 0 1 12 0v3"/>',
    "bussola": '<circle cx="12" cy="12" r="9"/><path d="m15.5 8.5-2 5-5 2 2-5z"/>',
    "varinha": '<path d="M4 20 15 9"/><path d="M17 3l.8 2.2L20 6l-2.2.8L17 9l-.8-2.2L14 6l2.2-.8z"/>',
    "relogio": '<circle cx="12" cy="13" r="7"/><path d="M12 9v4l2.5 2M5 4 2.5 6.5M19 4l2.5 2.5"/>',
    "bandeira": '<path d="M5 21V4"/><path d="M5 4h12l-2 4 2 4H5"/>',
    "telefone": '<path d="M5 4h3l2 5-2.5 1.5a11 11 0 0 0 6 6L15 14l5 2v3a2 2 0 0 1-2 2A16 16 0 0 1 3 6a2 2 0 0 1 2-2z"/>',
    "aviso": '<path d="M12 4 2.5 20h19z"/><path d="M12 10v4.5M12 17.5h.01"/>',
    "terminal": '<rect x="3" y="4" width="18" height="16" rx="2"/><path d="m7 9 3 3-3 3M12.5 15H17"/>',
    "camadas": '<path d="m12 3 9 5-9 5-9-5z"/><path d="m3 13 9 5 9-5"/>',
}

# Emoji (sem o seletor de variação) → ícone. As bandeiras e os pares especiais tratam-se à parte.
EMOJI_PARA_ICONE = {
    "\U0001F992": "girafa", "\U0001F33F": "folha", "\U0001F338": "flor", "⭐": "estrela", "\U0001F31F": "estrela",
    "✨": "brilho", "\U0001F446": "mao", "\U0001F499": "coracao", "\U0001F4CF": "regua", "\U0001F50A": "som",
    "\U0001F963": "tigela", "\U0001F384": "arvore", "\U0001F9E0": "cerebro", "⭕": "circulo", "\U0001F3C6": "taca",
    "\U0001F5A8": "impressora", "\U0001F30D": "globo", "\U0001F4A7": "gota", "☀": "sol", "\U0001F327": "chuva",
    "\U0001F4FB": "radio", "\U0001F6E1": "escudo", "\U0001F319": "lua", "❓": "pergunta", "\U0001F389": "festa",
    "✉": "envelope", "\U0001F512": "cadeado", "\U0001F513": "cadeado_aberto", "✍": "caneta", "✔": "certo",
    "\U0001F4BE": "guardar", "\U0001F4F7": "camara", "\U0001F4F8": "camara", "\U0001F50E": "lupa", "\U0001F3AC": "claquete",
    "\U0001F3A5": "video", "⏹": "parar", "▶": "tocar", "\U0001F4CB": "prancheta", "\U0001FA7A": "estetoscopio",
    "\U0001F399": "microfone", "\U0001F91D": "pessoas", "\U0001F5F3": "urna", "\U0001F4E5": "receber", "\U0001F50F": "cadeado",
    "\U0001F4E1": "antena", "\U0001F3A8": "paleta", "\U0001F3B5": "nota", "♪": "nota", "\U0001F4A1": "lampada",
    "\U0001F916": "robo", "\U0001F331": "rebento", "\U0001F9D2": "crianca", "\U0001F9ED": "bussola", "\U0001F9DA": "varinha",
    "⏰": "relogio", "\U0001F3F4": "bandeira", "\U0001F4DE": "telefone", "⚠": "aviso",
}


def svg(nome, classe="ki", rotulo=None):
    """Devolve o SVG do ícone. Sem rótulo: decorativo (aria-hidden). Com rótulo: role=img e aria-label."""
    corpo = ICONES[nome]
    acess = ('role="img" aria-label="%s"' % rotulo) if rotulo else 'aria-hidden="true"'
    return ('<svg class="%s" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" '
            'stroke-linecap="round" stroke-linejoin="round" focusable="false" %s>%s</svg>' % (classe, acess, corpo))


if __name__ == "__main__":
    import sys
    falta = sorted(set(EMOJI_PARA_ICONE.values()) - set(ICONES))
    print("ícones: %d · emojis mapeados: %d · em falta: %s" % (len(ICONES), len(EMOJI_PARA_ICONE), falta or "nenhum"))
    sys.exit(1 if falta else 0)
