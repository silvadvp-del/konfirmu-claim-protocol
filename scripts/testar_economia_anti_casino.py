#!/usr/bin/env python3
"""Testa a pagina «Economia anti-casino» e o post contra as regras da casa (27-11-2026).

Correr: python3 -I scripts/testar_economia_anti_casino.py [PASTA_DO_REPOSITORIO]

O que confere:
  - a pagina e autocontida: sem scripts, sem pedidos a rede, com a politica de seguranca fechada;
  - sem emojis; a marca escrita sempre inteira (Konfirmu);
  - nenhuma frase proibida pelas Regras Comerciais da casa (v1.0, seccao 4 e 6);
  - as garantias da casa presentes; o rotulo de prototipo visivel;
  - os numeros publicados sao os medidos; o contraste das letras cumpre AAA;
  - o post comeca como o David pediu e acaba com o significado do nome; sem enderecos;
  - o menu da raiz aponta para a pagina e o da edicao 21 nao.
So usa a biblioteca de base. Exit 0 se tudo passar, 1 se alguma verificacao falhar.
"""
import re
import sys
import unicodedata
from html.parser import HTMLParser
from pathlib import Path

PAGINA = "economia_anti_casino.html"
POST = "POST_ECONOMIA_ANTI_CASINO.md"
PRIMEIRA_LINHA = "Economia anti-casino passo a passo, só na Konfirmu!"
FECHO = "Confirma!"

PROIBIDAS = [
    r"\bresolvemos por ti\b", r"\bé simples\b", r"\bé fácil\b", r"\b100% seguro\b", r"\btotalmente seguro\b",
    r"\bgarantimos que recebes\b", r"\baconselhamos\b", r"\bmarca registada\b", r"\bcobertura europeia\b",
    r"\bparceiro oficial\b", r"\bprivacidade absoluta\b", r"\bgirafa", r"\bfisicamente impossível\b",
]
EMOJI = re.compile("[\U0001F000-\U0001FAFF\u2600-\u27BF\u2B00-\u2BFF\uFE0F\u200D]")
GARANTIAS = ["Konfirmu propõe. Tu confirmas.", "Quando não sabe, diz que não sabe."]
MEDIDOS = ["62 de 62", "13 de 13", "27 de novembro de 2026", "26 de novembro de 2026",
           "6e17169d11e984db1", "920a23d03096dd12"]


class Visivel(HTMLParser):
    """Texto que a pessoa le e os recursos que a pagina pede."""

    def __init__(self):
        super().__init__()
        self.pedacos = []
        self.recursos = []
        self.scripts = 0
        self._ignorar = 0

    def handle_starttag(self, etiqueta, atributos):
        if etiqueta in ("style", "script", "head"):
            self._ignorar += 1
        if etiqueta == "script":
            self.scripts += 1
        for nome, valor in atributos:
            if nome in ("src", "href") and valor:
                self.recursos.append(valor)
            if nome == "srcset" and valor:
                self.recursos.extend(p.strip().split(" ")[0] for p in valor.split(","))

    def handle_endtag(self, etiqueta):
        if etiqueta in ("style", "script", "head") and self._ignorar:
            self._ignorar -= 1

    def handle_data(self, dados):
        if not self._ignorar:
            self.pedacos.append(dados)


def dobrar(texto):
    return "".join(c for c in unicodedata.normalize("NFKD", texto.lower()) if not unicodedata.combining(c))


def luminancia(hexa):
    canais = [int(hexa[i:i + 2], 16) / 255 for i in (1, 3, 5)]
    linear = [c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4 for c in canais]
    return 0.2126 * linear[0] + 0.7152 * linear[1] + 0.0722 * linear[2]


def contraste(a, b):
    la, lb = sorted((luminancia(a), luminancia(b)), reverse=True)
    return (la + 0.05) / (lb + 0.05)


def main():
    repo = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parent.parent
    bons, maus = [], []

    def prova(nome, passa, detalhe=""):
        (bons if passa else maus).append(nome + ((" — " + detalhe) if detalhe and not passa else ""))

    html = (repo / PAGINA).read_text(encoding="utf-8")
    post = (repo / POST).read_text(encoding="utf-8")
    pagina = Visivel()
    pagina.feed(html)
    texto = re.sub(r"\s+", " ", " ".join(pagina.pedacos)).strip()
    post_dobrado, pagina_dobrada = dobrar(post), dobrar(texto)

    print("== pagina autocontida")
    prova("nao tem scripts", pagina.scripts == 0)
    remotos = [r for r in pagina.recursos if re.match(r"(https?:)?//", r) and "www.w3.org/2000/svg" not in r]
    prova("nenhum recurso remoto (so o icone dentro da pagina)", not remotos, ", ".join(remotos))
    prova("os links sao so para paginas locais", all(r.endswith((".html",)) for r in pagina.recursos if not r.startswith("data:")))
    csp = re.search(r'Content-Security-Policy" content="([^"]+)"', html)
    prova("politica de seguranca fechada (default-src none)", bool(csp) and "default-src 'none'" in csp.group(1))

    print("== regras da casa")
    prova("sem emojis na pagina", not EMOJI.search(html))
    prova("sem emojis no post", not EMOJI.search(post))
    for padrao in PROIBIDAS:
        prova("frase proibida ausente: " + padrao.replace("\\b", ""), not re.search(padrao, pagina_dobrada) and not re.search(padrao, post_dobrado))
    prova("a marca nunca aparece partida («Konfirm »)", not re.search(r"Konfirm\s", texto) and not re.search(r"Konfirm\s", post))
    for frase in GARANTIAS:
        prova("garantia presente na pagina: " + frase, frase in texto)
        prova("garantia presente no post: " + frase, frase in post)
    prova("rotulo de prototipo visivel", "Protótipo · só em bancada" in texto and "protótipo" in post.lower())
    prova("diz que o credito de teste nao e dinheiro", "Não é dinheiro" in texto and "não é dinheiro" in post)

    print("== numeros e factos publicados")
    for valor in MEDIDOS:
        prova("a pagina traz o valor medido: " + valor, valor in texto)
    for facto in ("1887", "Zamenhof", "Confirma!", "Esperanto"):
        prova("a pagina traz: " + facto, facto in texto)

    print("== contraste das letras (AAA = 7 ou mais)")
    for nome, primeiro, segundo, onde in [
        ("letras 4D: pesego sobre azul abissal", "#FF9E7D", "#0B192C", "--pesego:#FF9E7D;"),
        ("texto claro da faixa imersiva", "#F3F1EE", "#0B192C", "--abissal:#0B192C;"),
        ("corpo em modo claro", "#1D1D21", "#F3F1EE", "--papel:#F3F1EE;"),
        ("texto secundario em modo claro", "#4B4B52", "#FBFAF8", "--painel:#FBFAF8;"),
        ("corpo em modo escuro", "#ECEAE6", "#121317", "--papel:#121317"),
        ("texto secundario em modo escuro", "#B4B2AD", "#17181D", "--painel:#17181D"),
    ]:
        ratio = contraste(primeiro, segundo)
        prova(f"{nome}: {ratio:.1f}", ratio >= 7 and onde in html)
    prova("respeita quem pede menos movimento", "prefers-reduced-motion:reduce" in html and "animation:none" in html)

    print("== post")
    linhas = [l for l in post.splitlines() if l.strip()]
    prova("começa como o David pediu", linhas[0] == PRIMEIRA_LINHA, linhas[0])
    prova("acaba com o significado do nome, a terminar em «Confirma!»", linhas[-1].endswith(FECHO) and "Esperanto" in linhas[-1], linhas[-1][-60:])
    seccao_nome = Visivel()
    seccao_nome.feed(re.search(r'<section class="nome".*?</section>', html, re.S).group(0))
    fim = re.sub(r"\s+", " ", " ".join(seccao_nome.pedacos)).strip()
    prova("a pagina tambem acaba em «Confirma!» (antes do rodape)", fim.endswith(FECHO), fim[-60:])
    prova("explica o nome em Esperanto", "«Confirma!»" in post and "1887" in post and "Zamenhof" in post)
    prova("sete passos numerados", all(re.search(rf"^{n}\. ", post, re.M) for n in range(1, 8)))
    prova("sem endereços no post", "http" not in post.lower() and "www." not in post.lower())

    print("== menu")
    raiz = (repo / "app_unica.html").read_text(encoding="utf-8")
    edicao = (repo / "edicao-21" / "index.html").read_text(encoding="utf-8")
    prova("o menu da raiz aponta para a pagina", 'href="%s"' % PAGINA in raiz)
    prova("o cartao tem a estrutura que a imersao 3D espera", bool(re.search(r'<a class="card" href="%s"><span class="ico" aria-hidden="true"><svg [^>]*>.*?</svg></span><b>[^<]+</b><span class="d">[^<]+</span></a>' % re.escape(PAGINA), raiz)))
    prova("o menu da edicao 21 nao a traz (so aceita atividades)", PAGINA not in edicao)

    for nome in bons:
        print("OK    " + nome)
    for nome in maus:
        print("MAL   " + nome)
    print("\nresultado: %d de %d" % (len(bons), len(bons) + len(maus)))
    return 1 if maus else 0


if __name__ == "__main__":
    sys.exit(main())
