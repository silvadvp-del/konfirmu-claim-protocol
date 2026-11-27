#!/usr/bin/env python3
"""Marca de revisão jurídica nos avisos legais (KON-608; Portão Triplo de 27-11-2026, 12:10, portão legal).

Regra do David: nenhum texto legal traduzido automaticamente perde a marca de revisão jurídica até haver
validação formal. As 23 traduções são automáticas; o português é o original e também ainda não teve
revisão jurídica formal. Cada língua mostra a marca na sua própria língua, logo por baixo do título.

Uso:
  python3 -I scripts/avisos_marca_revisao.py aplicar [avisos_legais.html]
  python3 -I scripts/avisos_marca_revisao.py verificar [avisos_legais.html]   (sai com 1 se faltar alguma)
"""
import json
import re
import sys
from pathlib import Path

# As 24 línguas oficiais da UE. A frase da marca também é tradução automática (fica sob a mesma regra).
MARCA = {
    "pt": "Texto original em português. Aguarda revisão jurídica.",
    "en": "Awaiting legal review.",
    "nl": "In afwachting van juridische toetsing.",
    "de": "Rechtliche Prüfung ausstehend.",
    "fr": "En attente de validation juridique.",
    "es": "Pendiente de revisión jurídica.",
    "it": "In attesa di revisione legale.",
    "da": "Afventer juridisk gennemgang.",
    "sv": "Inväntar juridisk granskning.",
    "fi": "Odottaa oikeudellista tarkastusta.",
    "et": "Ootab õiguslikku ülevaatust.",
    "lv": "Gaida juridisko pārbaudi.",
    "lt": "Laukiama teisinės peržiūros.",
    "pl": "Oczekuje na weryfikację prawną.",
    "cs": "Čeká na právní kontrolu.",
    "sk": "Čaká na právnu kontrolu.",
    "sl": "Čaka na pravni pregled.",
    "hr": "Čeka pravnu provjeru.",
    "hu": "Jogi ellenőrzésre vár.",
    "ro": "În așteptarea revizuirii juridice.",
    "bg": "Очаква правна проверка.",
    "el": "Αναμένεται νομικός έλεγχος.",
    "mt": "Qed jistenna reviżjoni legali.",
    "ga": "Ag fanacht le hathbhreithniú dlíthiúil.",
}
CSS_NOTA = "#nota{margin:10px 0 0;padding:8px 12px;border:1px solid #FF9E7D;border-radius:10px;background:rgba(255,158,125,.08);color:#F4F7FA;font-weight:600}"


def ler_notas(html):
    return dict(re.findall(r'"([a-z]{2})":\{"nome":"[^"]*","t":"[^"]*","s":"[^"]*","n":"([^"]*)"', html))


def aplicar(caminho):
    p = Path(caminho)
    html = p.read_text(encoding="utf-8")
    notas = ler_notas(html)
    em_falta = sorted(set(MARCA) - set(notas))
    if em_falta:
        raise SystemExit("PARADO: línguas sem entrada nos avisos: %s" % ", ".join(em_falta))

    def troca(m):
        lingua, nota = m.group(1), m.group(2)
        marca = MARCA[lingua]
        if marca in nota:
            return m.group(0)
        nova = marca if lingua == "pt" else (nota.rstrip() + " " + marca).strip()
        return m.group(0)[: m.start(2) - m.start(0)] + json.dumps(nova, ensure_ascii=False)[1:-1] + m.group(0)[m.end(2) - m.start(0):]

    html2 = re.sub(r'"([a-z]{2})":\{"nome":"[^"]*","t":"[^"]*","s":"[^"]*","n":"([^"]*)"', troca, html)
    if CSS_NOTA not in html2:
        html2 = html2.replace("</style>", CSS_NOTA + "</style>", 1)
    if html2 != html:
        p.write_text(html2, encoding="utf-8")
    print("avisos legais: marca de revisão jurídica em %d de %d línguas" % (len(verificar_notas(html2)[0]), len(MARCA)))


def verificar_notas(html):
    notas = ler_notas(html)
    certas = sorted(l for l in MARCA if MARCA[l] in notas.get(l, ""))
    faltam = sorted(l for l in MARCA if l not in certas)
    return certas, faltam


def main(argv):
    acao = argv[1] if len(argv) > 1 else "verificar"
    caminho = argv[2] if len(argv) > 2 else str(Path(__file__).resolve().parents[1] / "avisos_legais.html")
    if acao == "aplicar":
        aplicar(caminho)
        return 0
    certas, faltam = verificar_notas(Path(caminho).read_text(encoding="utf-8"))
    print("marca de revisão jurídica: %d de %d línguas%s" % (len(certas), len(MARCA), (" — faltam: " + ", ".join(faltam)) if faltam else ""))
    return 1 if faltam else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
