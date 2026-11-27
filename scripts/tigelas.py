"""As 8 tigelas do Portal Educação e família (diretiva do David, 27-11-2026, 12:29).

Uma só fonte para o desenho das tigelas, o palco azul abissal, a luz pêssego ao toque e as línguas.
O gerador do menu (scripts/gerar_menu.py) importa este módulo.

Regras da diretiva: cerâmica com rebordo pintado, um símbolo simples e distinto em cada tigela,
legível em botões pequenos; ao toque, o interior acende com luz pêssego (#FF9E7D / #FFB088)
sobre azul abissal (#0B192C), com vibração e transição fluida. Sem verde (regra da casa).
Tudo em SVG e CSS dentro da página: nada vem de fora, abre em modo avião e em file://.
"""
import json
import os

PESSEGO = "#FF9E7D"
PESSEGO_CLARO = "#FFB088"
ABISSAL = "#0B192C"

# Símbolos numa grelha de 24x24, pintados no bojo da tigela. Traço grosso: lê-se em botões pequenos.
SIMBOLOS = {
    "livro": '<path d="M12 7.2C10 5.8 7.4 5.2 4.6 5.2v12.1c2.8 0 5.4.6 7.4 2 2-1.4 4.6-2 7.4-2V5.2c-2.8 0-5.4.6-7.4 2z" fill="none" stroke-width="2.3" stroke-linejoin="round"/><path d="M12 7.2v12" fill="none" stroke-width="2.3" stroke-linecap="round"/>',
    "pergunta": '<path d="M8.6 8.9a3.5 3.5 0 1 1 4.9 3.2c-.9.4-1.5 1.3-1.5 2.3v.7" fill="none" stroke-width="2.6" stroke-linecap="round"/><circle cx="12" cy="19" r="1.7" stroke="none"/>',
    "estrela": '<path d="m12 2.8 2.75 5.6 6.15.9-4.45 4.35 1.05 6.1L12 16.85l-5.5 2.9 1.05-6.1L3.1 9.3l6.15-.9z" stroke-width="1.2" stroke-linejoin="round"/>',
    "filme": '<path d="M8.4 5.6c0-.9 1-1.5 1.8-1l8.6 5.6c.7.5.7 1.5 0 2l-8.6 5.6c-.8.5-1.8-.1-1.8-1z" stroke="none"/>',
    "contas": '<path d="M12 4.6v14.8M4.6 12h14.8" fill="none" stroke-width="3.1" stroke-linecap="round"/>',
    "musica": '<path d="M9 17.2V6.4l10-2.2v10.8" fill="none" stroke-width="2.3" stroke-linecap="round" stroke-linejoin="round"/><ellipse cx="6.6" cy="17.4" rx="2.8" ry="2.2" stroke="none"/><ellipse cx="16.6" cy="15.2" rx="2.8" ry="2.2" stroke="none"/>',
    "globo": '<circle cx="12" cy="12" r="8.2" fill="none" stroke-width="2.2"/><path d="M3.8 12h16.4M12 3.8c2.7 2.7 2.7 13.7 0 16.4M12 3.8c-2.7 2.7-2.7 13.7 0 16.4" fill="none" stroke-width="1.9"/>',
    "bussola": '<circle cx="12" cy="12" r="8.2" fill="none" stroke-width="2.2"/><path d="m15.6 8.4-2.2 5-5 2.2 2.2-5z" stroke-width="1" stroke-linejoin="round"/>',
    "toque": '<circle cx="12" cy="12" r="3.4" stroke="none"/><circle cx="12" cy="12" r="6.6" fill="none" stroke-width="1.9"/><circle cx="12" cy="12" r="9.8" fill="none" stroke-width="1.4" opacity=".55"/>',
}

# As 8 tigelas: símbolo, vidrado (claro, meio, escuro), rebordo pintado (cor, sombra) e cor do símbolo.
# A ordem segue as atividades do portal; «Primeiros passos» é a entrada grande, não é tigela.
TIGELAS = {
    "Tutor-Girafinha-offline.html": ("livro", ("#FBF3E8", "#EAD6BF", "#B98F6B"), ("#2F6FB2", "#1D4A7E"), "#245C9A"),
    "kcp_family_quiz.html": ("pergunta", ("#E6F1FC", "#B7D5F3", "#6E98C9"), ("#F08A5D", "#B95B33"), "#D0592C"),
    "sala_natal_girafinhas.html": ("estrela", ("#FFC7B0", "#F08A5D", "#A2552F"), ("#F4F7FA", "#D5DDE8"), "#FFE2CF"),
    "estudio_video_criancas.html": ("filme", ("#E9EFF7", "#9FB3C8", "#4A6688"), ("#FFB088", "#D9784F"), "#FFE3D2"),
    "executor_criancas.html": ("contas", ("#FFF1E6", "#F7C9A9", "#C98A63"), ("#26436F", "#152A4B"), "#26436F"),
    "kcp_art_music_studio.html": ("musica", ("#F5F8FC", "#C9D6E6", "#6F86A6"), ("#3A63B5", "#243F7A"), "#2F55A3"),
    "regua_do_planeta.html": ("globo", ("#CFE7F8", "#7FB7E2", "#356FA8"), ("#FFE2CF", "#DC8C5F"), "#FFF1E6"),
    "neverland_family_quest.html": ("bussola", ("#F7C9A9", "#DC8C5F", "#A2552F"), ("#FFF4E6", "#D8C2A6"), "#FFF4E6"),
}
ENTRADA = "girafinhas_criancas_facil.html"

# Chave curta de cada atividade nos ficheiros locales/{iso}.json.
CHAVES = {
    "girafinhas_criancas_facil.html": "girafinhas",
    "Tutor-Girafinha-offline.html": "tutor",
    "kcp_family_quiz.html": "quiz",
    "sala_natal_girafinhas.html": "natal",
    "estudio_video_criancas.html": "video",
    "executor_criancas.html": "contas",
    "kcp_art_music_studio.html": "arte",
    "regua_do_planeta.html": "regua",
    "neverland_family_quest.html": "aventura",
}


def svg_tigela(n, simbolo, vidrado, rebordo, cor_simbolo):
    """Uma tigela em 3/4, vista de cima: sombra no palco, bojo vidrado, lábio grosso pintado, interior
    (onde acende a luz) e o símbolo pintado no bojo. n numera os gradientes (ids únicos na página)."""
    claro, meio, escuro = vidrado
    cor, sombra_cor = rebordo
    g = "tg%d" % n
    return (
        '<svg class="tg" viewBox="0 0 120 104" aria-hidden="true" focusable="false">'
        '<defs>'
        # bojo: luz de cima à esquerda, sombra em baixo à direita
        '<radialGradient id="{g}c" cx=".28" cy=".05" r="1.05" fx=".24" fy="0"><stop offset="0" stop-color="{claro}"/>'
        '<stop offset=".5" stop-color="{meio}"/><stop offset="1" stop-color="{escuro}"/></radialGradient>'
        # oclusão junto ao pé
        '<linearGradient id="{g}o" x1="0" y1="0" x2="0" y2="1"><stop offset=".55" stop-color="#000" stop-opacity="0"/>'
        '<stop offset="1" stop-color="#000" stop-opacity=".3"/></linearGradient>'
        # lábio pintado: mais claro atrás à esquerda
        '<linearGradient id="{g}r" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{cor}"/>'
        '<stop offset="1" stop-color="{sombra_cor}"/></linearGradient>'
        # interior: sombra fina do lábio atrás, parede de trás com luz, fundo e frente mais escuros
        '<linearGradient id="{g}i" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{escuro}"/>'
        '<stop offset=".16" stop-color="{claro}"/><stop offset=".62" stop-color="{meio}"/>'
        '<stop offset="1" stop-color="{escuro}"/></linearGradient>'
        # luz pêssego do interior (acende ao toque)
        '<radialGradient id="{g}l" cx=".5" cy=".6" r=".62"><stop offset="0" stop-color="#FFF6EE"/>'
        '<stop offset=".3" stop-color="#FFB088"/><stop offset=".7" stop-color="#FF9E7D" stop-opacity=".75"/>'
        '<stop offset="1" stop-color="#FF9E7D" stop-opacity="0"/></radialGradient>'
        # brilho do vidrado
        '<linearGradient id="{g}b" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fff" stop-opacity=".9"/>'
        '<stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>'
        '<clipPath id="{g}k"><path d="M12 44C12 73 33 91 60 91S108 73 108 44A48 16 0 0 1 12 44z"/></clipPath>'
        '</defs>'
        # sombra de contacto no palco
        '<ellipse class="tg-chao" cx="60" cy="93" rx="43" ry="8.5" fill="url(#tgsombra)"/>'
        # bojo
        '<path d="M12 44C12 73 33 91 60 91S108 73 108 44A48 16 0 0 1 12 44z" fill="url(#{g}c)"/>'
        '<g clip-path="url(#{g}k)">'
        '<rect x="0" y="40" width="120" height="56" fill="url(#{g}o)"/>'
        # o interior aceso ilumina o bojo por dentro (porcelana)
        '<ellipse class="tg-calor" cx="60" cy="56" rx="46" ry="19" fill="#FFB088"/>'
        # luz fria do palco no lado direito
        '<path d="M106.4 47C104.7 70 86 88.5 61 90.6" fill="none" stroke="#9CCBFF" stroke-width="2.6" stroke-opacity=".5" stroke-linecap="round"/>'
        # brilho grande à esquerda
        '<path d="M19.4 54C21.5 67 29.6 77.8 40.4 83.6" fill="none" stroke="url(#{g}b)" stroke-width="5.4" stroke-linecap="round" opacity=".6"/>'
        '<circle cx="24.6" cy="58.6" r="1.9" fill="#fff" opacity=".85"/>'
        '</g>'
        # símbolo pintado no bojo, com relevo de vidrado (sombra por baixo, brilho por cima)
        '<g transform="translate(46 61.6) scale(1.17)" stroke-linecap="round" stroke-linejoin="round">'
        '<g transform="translate(0 .7)" fill="#000" stroke="#000" opacity=".22">{simbolo}</g>'
        '<g fill="{cs}" stroke="{cs}">{simbolo}</g>'
        '</g>'
        # lábio grosso e pintado: a face de fora, depois o topo
        '<ellipse cx="60" cy="45.8" rx="48" ry="16" fill="{sombra_cor}"/>'
        '<ellipse cx="60" cy="44" rx="48" ry="16" fill="url(#{g}r)"/>'
        '<path d="M15.6 41.4A46 13.6 0 0 1 72 30.6" fill="none" stroke="#fff" stroke-width="1.7" stroke-linecap="round" opacity=".55"/>'
        # interior
        '<ellipse cx="60" cy="45" rx="41.2" ry="12.2" fill="url(#{g}i)"/>'
        '<ellipse class="tg-luz" cx="60" cy="46.2" rx="38.5" ry="10.6" fill="url(#{g}l)"/>'
        '<ellipse class="tg-aro" cx="60" cy="45" rx="41.2" ry="12.2" fill="none" stroke="#FFB088" stroke-width="1.6"/>'
        '<g class="tg-faiscas" fill="#FFE2CF"><circle cx="49" cy="40" r="1.3"/><circle cx="63" cy="38" r="1"/><circle cx="72" cy="41" r="1.2"/></g>'
        '</svg>'
    ).format(g=g, claro=claro, meio=meio, escuro=escuro, cor=cor, sombra_cor=sombra_cor, cs=cor_simbolo,
             simbolo=SIMBOLOS[simbolo])


# Gradiente partilhado da sombra de contacto (um só por página).
DEFS_PARTILHADAS = ('<svg width="0" height="0" style="position:absolute" aria-hidden="true" focusable="false"><defs>'
                    '<radialGradient id="tgsombra" cx=".5" cy=".5" r=".5"><stop offset="0" stop-color="#000" stop-opacity=".6"/>'
                    '<stop offset=".6" stop-color="#000" stop-opacity=".22"/><stop offset="1" stop-color="#000" stop-opacity="0"/>'
                    '</radialGradient></defs></svg>')


def svg_entrada():
    """O ícone da entrada grande («Primeiros passos»): um toque que acende."""
    return ('<svg class="tg-toque" viewBox="0 0 24 24" aria-hidden="true" focusable="false" fill="#FFB088" stroke="#FFB088">'
            + SIMBOLOS["toque"] + '</svg>')


# ---------------------------------------------------------------------------------------------
# Línguas: os textos do portal vivem em locales/{iso}.json (protocolo de 27-11). O português é a
# origem. Todas as línguas têm de ter as mesmas chaves, sem nenhuma vazia; se não, o gerador para.

def ler_linguas(repo):
    pasta = os.path.join(repo, "locales")
    linguas = {}
    for nome in sorted(os.listdir(pasta)):
        if not nome.endswith(".json"):
            continue
        with open(os.path.join(pasta, nome), encoding="utf-8") as f:
            dados = json.load(f)
        meta = dados.get("_meta") or {}
        codigo = nome[:-5]
        if meta.get("codigo") != codigo or meta.get("dir") not in ("ltr", "rtl") or not meta.get("nome"):
            raise SystemExit("locales/%s: _meta incompleto" % nome)
        linguas[codigo] = dados
    if "pt" not in linguas:
        raise SystemExit("falta locales/pt.json (o texto de origem)")
    chaves = sorted(k for k in linguas["pt"] if not k.startswith("_"))
    for codigo, dados in linguas.items():
        ks = sorted(k for k in dados if not k.startswith("_"))
        if ks != chaves:
            raise SystemExit("locales/%s.json: chaves diferentes das do português" % codigo)
        vazias = [k for k in ks if not str(dados[k]).strip()]
        if vazias:
            raise SystemExit("locales/%s.json: chaves vazias %s" % (codigo, vazias))
    if len(linguas) < 57:
        raise SystemExit("o protocolo pede 57 línguas ou mais; há %d" % len(linguas))
    return linguas


def dados_linguas(linguas):
    """O JSON que vai dentro da página (só lido quando alguém muda de língua)."""
    saida = {}
    for codigo, d in linguas.items():
        m = d["_meta"]
        saida[codigo] = {"n": m["nome"], "np": m["nome_pt"], "d": m["dir"],
                         "s": {k: v for k, v in d.items() if not k.startswith("_")}}
    # «</» nunca aparece dentro do bloco: um texto não pode fechar a etiqueta script
    return json.dumps(saida, ensure_ascii=False, separators=(",", ":"), sort_keys=True).replace("</", "<\\/")


def _bdi(chave, texto):
    return '<bdi data-k="%s">%s</bdi>' % (chave, texto)


def secao_familia(itens, pt, esc):
    """O portal Educação e família: a entrada grande e as tigelas. itens = [(href, ...)] já filtrados.
    pt = textos em português (locales/pt.json); esc = função de escape de HTML."""
    partes = ['<section class="portal portal-familia" id="p-fam" role="tabpanel" aria-labelledby="t-fam" lang="pt" dir="ltr">',
              '<div class="fam-topo"><div class="fam-tit">',
              '<h2>%s</h2><p class="sub">%s</p>' % (_bdi("fam.titulo", esc(pt["fam.titulo"])), _bdi("fam.sub", esc(pt["fam.sub"]))),
              '</div><button type="button" class="fam-lingua" id="famLingua" aria-haspopup="dialog" aria-expanded="false" aria-controls="famLinguas">'
              '<bdi class="fam-lingua-r" data-k="fam.lingua">%s</bdi> <bdi class="fam-lingua-n" lang="pt">Português</bdi></button></div>' % esc(pt["fam.lingua"]),
              '<div class="fam-linguas" id="famLinguas" role="dialog" aria-label="%s" hidden>' % esc(pt["fam.lingua"]),
              '<input id="famLinguaProcura" type="search" autocomplete="off" enterkeyhint="search" placeholder="%s" data-kp="fam.procurar_lingua">' % esc(pt["fam.procurar_lingua"]),
              '<ul id="famLinguaLista"></ul></div>',
              '<div class="grid">']
    n = 0
    for href in itens:
        chave = CHAVES[href]
        t, d = esc(pt["fam.%s.t" % chave]), esc(pt["fam.%s.d" % chave])
        if href == ENTRADA:
            partes.append('<a class="card entrada" href="%s" data-tg="%s"><span class="ico" aria-hidden="true">%s</span>'
                          '<b>%s</b><span class="d">%s <span class="fam-comeca">%s</span></span></a>'
                          % (href, chave, svg_entrada(), _bdi("fam.%s.t" % chave, t), _bdi("fam.%s.d" % chave, d),
                             _bdi("fam.comeca", esc(pt["fam.comeca"]))))
            continue
        simbolo, vidrado, rebordo, cor_simbolo = TIGELAS[href]
        n += 1
        partes.append('<a class="card tigela" href="%s" data-tg="%s"><span class="ico" aria-hidden="true">%s</span>'
                      '<b>%s</b><span class="d">%s</span></a>'
                      % (href, chave, svg_tigela(n, simbolo, vidrado, rebordo, cor_simbolo),
                         _bdi("fam.%s.t" % chave, t), _bdi("fam.%s.d" % chave, d)))
    partes += ['</div>', '</section>']
    return "".join(partes), n


CSS_FAMILIA = """
/* Portal Educação e família: palco azul abissal e as tigelas (diretiva de 27-11, 12:29).
   Contraste AAA (ordem de 27-11, 12:16): todo o texto a 7:1 ou mais, medido em píxeis no ensaio. */
.portal-familia{position:relative;margin-top:24px;padding:20px 14px 18px;border-radius:22px;color:#E9EFF7;background:radial-gradient(130% 75% at 50% -8%,#1B3A66 0%,#0F2240 38%,#0B192C 72%) #0B192C;box-shadow:inset 0 1px 0 rgb(255 255 255 / .07),0 18px 40px -24px rgb(11 25 44 / .9)}
.portal-familia h2{color:#F5F8FC}
.portal-familia .sub{margin:4px 0 0;color:#D5DDE8}
.fam-topo{display:flex;align-items:flex-start;justify-content:space-between;gap:12px;margin:0 2px 16px}
.fam-tit{min-width:0}
.fam-lingua{flex:none;max-width:48%;min-height:44px;padding:5px 14px;border:1px solid rgb(255 255 255 / .2);border-radius:18px;background:rgb(255 255 255 / .04);color:#F5F8FC;font:600 .875rem/1.2 var(--letra);cursor:pointer;text-align:center;overflow-wrap:anywhere}
.fam-lingua-r{display:block;color:#D5DDE8;font-weight:500;font-size:.75rem}
.fam-lingua-n{display:block}
.fam-lingua:focus-visible,.fam-linguas button:focus-visible,.fam-linguas input:focus-visible{outline:2px solid #FFB088;outline-offset:2px}
.fam-linguas{margin:-4px 0 14px;padding:10px;border-radius:16px;background:#10223D;border:1px solid rgb(255 255 255 / .12)}
.fam-linguas input{width:100%;min-height:44px;padding:0 12px;border-radius:10px;border:1px solid rgb(255 255 255 / .2);background:#0B192C;color:#F5F8FC;font:400 1rem/1.2 var(--letra)}
.fam-linguas input::placeholder{color:#B9C6D7}
.fam-linguas ul{list-style:none;margin:8px 0 0;padding:0;max-height:264px;overflow:auto;overscroll-behavior:contain;display:grid;grid-template-columns:repeat(auto-fill,minmax(148px,1fr));gap:4px}
.fam-linguas button{width:100%;min-height:44px;padding:6px 10px;border:0;border-radius:10px;background:transparent;color:#F5F8FC;text-align:start;font:600 .9375rem/1.2 var(--letra);cursor:pointer}
.fam-linguas button small{display:block;margin-top:2px;color:#D5DDE8;font-size:.75rem;font-weight:400}
.fam-linguas button:hover{background:rgb(255 255 255 / .06)}
.fam-linguas button[aria-current=true]{background:rgb(255 176 136 / .1);box-shadow:inset 0 0 0 1px rgb(255 176 136 / .55)}
.portal-familia .grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:4px 10px;border:0;border-radius:0;background:transparent;overflow:visible}
@media (min-width:640px){.portal-familia .grid{grid-template-columns:repeat(4,minmax(0,1fr))}}
.portal-familia .card{position:relative;display:flex;flex-direction:column;align-items:center;gap:2px;min-height:0;padding:4px 6px 14px;border:0;border-radius:18px;text-align:center;color:#E9EFF7;background:transparent;-webkit-tap-highlight-color:transparent;touch-action:manipulation}
.portal-familia .card[hidden],.portal-familia .card.entrada[hidden]{display:none}
.portal-familia .card:hover{background:transparent}
.portal-familia .card:active{background:rgb(255 255 255 / .035)}
.portal-familia .card:focus-visible{outline:2px solid #FFB088;outline-offset:-2px;border-radius:18px}
.portal-familia .card b{margin-top:2px;font-size:1rem;line-height:1.25;font-weight:650;color:#F5F8FC}
.portal-familia .card .d{font-size:.8125rem;line-height:1.35;color:#D5DDE8}
.portal-familia .card.tigela b,.portal-familia .card.tigela .d{align-self:stretch}
.portal-familia .card .ico{position:relative;display:block;width:100%;max-width:150px;height:auto;aspect-ratio:120/104;border-radius:0;background:transparent;color:inherit;isolation:isolate}
.portal-familia .card .ico svg.tg{display:block;width:100%;height:100%;overflow:visible;fill:none;stroke:none;transform-origin:50% 82%;transition:transform .24s cubic-bezier(.2,.8,.2,1)}
.tg-luz,.tg-aro,.tg-calor,.tg-faiscas{opacity:0;transition:opacity .18s ease-out}
/* a coluna de luz que sobe da tigela e o brilho no palco */
.portal-familia .card .ico::before{content:"";position:absolute;z-index:1;left:14%;right:14%;top:-72%;bottom:46%;pointer-events:none;background:radial-gradient(48% 62% at 50% 100%,rgb(255 204 170 / .95),rgb(255 158 125 / .34) 52%,rgb(255 158 125 / 0) 76%);mix-blend-mode:screen;opacity:0;transform:scaleY(.5);transform-origin:50% 100%;transition:opacity .2s ease-out,transform .26s cubic-bezier(.2,.8,.2,1)}
.portal-familia .card .ico::after{content:"";position:absolute;z-index:-1;left:-8%;right:-8%;top:6%;bottom:-12%;pointer-events:none;background:radial-gradient(52% 46% at 50% 54%,rgb(255 158 125 / .5),rgb(255 158 125 / 0) 72%);opacity:0;transition:opacity .2s ease-out}
.portal-familia .card.acesa .tg-luz{opacity:1;transition-duration:0s} /* ao toque a luz acende no mesmo quadro, mesmo com a aurora a correr (PR #20) */
.portal-familia .card.acesa .tg-aro{opacity:.9}
.portal-familia .card.acesa .tg-calor{opacity:.3}
.portal-familia .card.acesa .tg-faiscas{opacity:1}
.portal-familia .card.acesa .ico::before{opacity:1;transform:none}
.portal-familia .card.acesa .ico::after{opacity:1}
.portal-familia .card.acesa svg.tg{transform:translateY(-3px) scale(1.045)}
.portal-familia .card.escolhida:not(.acesa) .tg-luz{opacity:.45}
.portal-familia .card.escolhida:not(.acesa) .ico::after{opacity:.45}
.portal-familia .card:focus-visible .tg-luz{opacity:.8}
@media (hover:hover){.portal-familia .card:hover{background:rgb(255 255 255 / .035)}.portal-familia .card:hover .tg-luz{opacity:.35}.portal-familia .card:hover svg.tg{transform:translateY(-2px)}}
.tg-faiscas circle{transform-box:fill-box;transform-origin:center}
.portal-familia .card.acesa .tg-faiscas circle{animation:tg-sobe 1.1s ease-out infinite}
.portal-familia .card.acesa .tg-faiscas circle:nth-child(2){animation-delay:.25s}
.portal-familia .card.acesa .tg-faiscas circle:nth-child(3){animation-delay:.5s}
@keyframes tg-sobe{from{transform:translateY(0);opacity:1}to{transform:translateY(-18px);opacity:0}}
/* a entrada grande: «Primeiros passos» */
.portal-familia .card.entrada{grid-column:1/-1;display:grid;grid-template-columns:64px minmax(0,1fr);grid-template-areas:"ico t" "ico d";column-gap:14px;align-items:center;margin:0 0 8px;padding:14px 16px;text-align:start;background:linear-gradient(135deg,rgb(255 176 136 / .11),rgb(255 158 125 / .04));box-shadow:inset 0 0 0 1px rgb(255 176 136 / .3)}
.portal-familia .card.entrada b{grid-area:t;align-self:end;margin:0}
.portal-familia .card.entrada .d{grid-area:d;align-self:start}
.portal-familia .card.entrada .ico{grid-area:ico;width:64px;max-width:64px;aspect-ratio:1;border-radius:50%;display:grid;place-items:center;background:radial-gradient(closest-side,rgb(255 176 136 / .34),rgb(255 158 125 / .08) 70%,rgb(255 158 125 / 0)),#13294A;box-shadow:inset 0 0 0 1px rgb(255 176 136 / .38)}
.portal-familia .card.entrada .ico svg.tg-toque{width:34px;height:34px;fill:#FFB088;stroke:#FFB088;transition:transform .24s cubic-bezier(.2,.8,.2,1)}
.portal-familia .card.entrada .ico::before{left:-10%;right:-10%;top:-40%;bottom:30%}
.portal-familia .card.entrada.acesa .ico svg.tg-toque{transform:scale(1.12)}
.fam-comeca{display:inline-block;margin:6px 0 0;padding:2px 10px;border-radius:999px;background:#FFB088;color:#2A1408;font-size:.75rem;font-weight:700;line-height:1.5;white-space:nowrap}
@media (prefers-reduced-motion:reduce){
 .portal-familia .card svg,.tg-luz,.tg-aro,.tg-calor,.tg-faiscas,.portal-familia .card .ico::before,.portal-familia .card .ico::after{transition:none}
 .portal-familia .card.acesa svg.tg,.portal-familia .card:hover svg.tg,.portal-familia .card.entrada.acesa .ico svg.tg-toque{transform:none}
 .portal-familia .card .ico::before{transform:none}
 .tg-faiscas{display:none}
}
"""

JS_FAMILIA = r"""
// Portal Educação e família: a tigela tocada acende (luz pêssego), vibra e abre; e as 62 línguas.
(function(){
 var sec=document.getElementById('p-fam');if(!sec)return;
 var cartoes=[].slice.call(sec.querySelectorAll('a.card'));
 var reduz=!!(window.matchMedia&&matchMedia('(prefers-reduced-motion: reduce)').matches);
 function acender(a){cartoes.forEach(function(c){if(c!==a)c.classList.remove('acesa')});a.classList.add('acesa')}
 function apagar(){cartoes.forEach(function(c){c.classList.remove('acesa')})}
 cartoes.forEach(function(a){
  a.addEventListener('pointerdown',function(e){if(e.button>0)return;acender(a)});
  a.addEventListener('pointercancel',apagar);
  a.addEventListener('click',function(e){
   if(e.defaultPrevented||e.button>0||e.metaKey||e.ctrlKey||e.shiftKey||e.altKey)return;
   acender(a);
   try{sessionStorage.setItem('konfirmu_tigela',a.getAttribute('href'))}catch(_){}
   if(e.detail===0||reduz)return; /* teclado ou menos movimento: abre logo */
   if(navigator.vibrate)try{navigator.vibrate(12)}catch(_){}
   e.preventDefault();var url=a.href;setTimeout(function(){location.href=url},200);
  });
 });
 /* ao voltar (também da cache de retrocesso do navegador): nenhuma acesa, a última escolhida com um brilho leve */
 function marcar(){var u=null;try{u=sessionStorage.getItem('konfirmu_tigela')}catch(_){}
  cartoes.forEach(function(c){c.classList.toggle('escolhida',!!u&&c.getAttribute('href')===u)})}
 marcar();
 window.addEventListener('pageshow',function(){apagar();marcar()});
 // Línguas
 var botao=document.getElementById('famLingua'),painel=document.getElementById('famLinguas'),
     campo=document.getElementById('famLinguaProcura'),lista=document.getElementById('famLinguaLista'),
     fonte=document.getElementById('famDados'),dados=null,atual='pt';
 if(!botao||!painel||!fonte)return;
 function ler(){if(!dados){try{dados=JSON.parse(fonte.textContent)}catch(_){dados={}}}return dados}
 function norm(t){return String(t).normalize('NFD').replace(/[̀-ͯ]/g,'').toLowerCase()}
 function aplicar(cod,guardar){
  var d=ler()[cod];if(!d)return;atual=cod;
  [].forEach.call(document.querySelectorAll('[data-k]'),function(el){var v=d.s[el.getAttribute('data-k')];if(v)el.textContent=v});
  [].forEach.call(document.querySelectorAll('[data-kp]'),function(el){var v=d.s[el.getAttribute('data-kp')];if(v)el.placeholder=v});
  sec.lang=cod;sec.dir=d.d;
  var tab=document.getElementById('t-fam');if(tab){var b=tab.querySelector('bdi');if(b){b.lang=cod;b.dir=d.d}}
  var n=botao.querySelector('.fam-lingua-n');n.textContent=d.n;n.lang=cod;n.dir=d.d;
  painel.setAttribute('aria-label',d.s['fam.lingua']);
  [].forEach.call(lista.querySelectorAll('button'),function(b){b.setAttribute('aria-current',b.getAttribute('data-l')===cod?'true':'false')});
  if(guardar)try{localStorage.setItem('konfirmu_lingua_familia',cod)}catch(_){}
 }
 function montar(){
  if(lista.childNodes.length)return;var d=ler();
  var cods=Object.keys(d).sort(function(a,b){return a==='pt'?-1:b==='pt'?1:d[a].np.localeCompare(d[b].np,'pt')});
  cods.forEach(function(c){
   var li=document.createElement('li'),b=document.createElement('button'),nome=document.createElement('bdi'),pt=document.createElement('small');
   b.type='button';b.setAttribute('data-l',c);b.setAttribute('data-procura',norm(d[c].n+' '+d[c].np+' '+c));
   b.setAttribute('aria-current',c===atual?'true':'false');
   nome.textContent=d[c].n;nome.lang=c;nome.dir=d[c].d;pt.textContent=d[c].np;
   b.appendChild(nome);b.appendChild(pt);b.addEventListener('click',function(){aplicar(c,true);fechar(true)});
   li.appendChild(b);lista.appendChild(li);
  });
 }
 function filtrar(){var q=norm(campo.value.trim());[].forEach.call(lista.querySelectorAll('li'),function(li){li.hidden=!!q&&li.firstChild.getAttribute('data-procura').indexOf(q)<0})}
 function abrir(){montar();painel.hidden=false;botao.setAttribute('aria-expanded','true');campo.value='';filtrar();campo.focus()}
 function fechar(foco){painel.hidden=true;botao.setAttribute('aria-expanded','false');if(foco)botao.focus()}
 botao.addEventListener('click',function(){painel.hidden?abrir():fechar(true)});
 campo.addEventListener('input',filtrar);
 painel.addEventListener('keydown',function(e){if(e.key==='Escape'){e.preventDefault();fechar(true)}});
 document.addEventListener('pointerdown',function(e){if(!painel.hidden&&!painel.contains(e.target)&&!botao.contains(e.target))fechar(false)});
 var guardada=null;try{guardada=localStorage.getItem('konfirmu_lingua_familia')}catch(_){}
 if(guardada&&guardada!=='pt')aplicar(guardada,false);
 window.KFAM={aplicar:function(c){aplicar(c,true)},atual:function(){return atual},linguas:function(){return Object.keys(ler()).length}};
})();
"""
