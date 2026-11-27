#!/usr/bin/env python3
"""KFC-0.1 — Konfirmu Frugal Compute: o roteador frugal (implementação de referência, EUPL-1.2).

Decide, para cada pedido, o caminho mais barato que serve, por esta ordem fixa:
  Camada 0  regras escritas e fichas com fonte, no aparelho: 0 bytes de rede, 0 €, memória baixa.
  Camada 1  modelo de IA local, no aparelho: só com consentimento explícito e com o modelo já guardado.
  Camada 2  modelo externo da UE: só com consentimento para ESTE pedido, com rede, sem dados de crianças,
            dentro do teto diário (para a 80 % do teto, como manda a Adenda II de 27-11-2026).
  Recusa    se nenhuma serve: diz que não sabe e onde confirmar. Nunca inventa.

O roteador só DECIDE: não chama nenhum modelo, não abre a rede, não lê chaves. Quem o usa faz a chamada
que a decisão permitir. Cada decisão sai com um recibo (SHA-256 do pedido e da decisão em JSON canónico),
para poder ser selada e conferida depois por qualquer pessoa.

Uso:
  python3 -I konfirmu_frugal_router.py --auto-teste
  python3 -I konfirmu_frugal_router.py decidir PEDIDO.json
Só biblioteca padrão. Especificação: KFC-0.1.md.
"""
import hashlib
import json
import sys

VERSAO = "KFC-0.1"
LIMITE_PARAGEM = 0.80  # para antes de chegar a 80 % do teto diário de gasto
RAM_CAMADA0_MB = 64
RAM_CAMADA1_MB = 165   # o modelo local precisa de mais memória: só entra com memória livre que chegue


def canonico(obj):
    return json.dumps(obj, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def sha256(texto):
    return hashlib.sha256(texto.encode("utf-8")).hexdigest()


def _num(x, nome):
    if isinstance(x, bool) or not isinstance(x, (int, float)) or x != x or x < 0:
        raise ValueError("%s tem de ser um número não negativo" % nome)
    return float(x)


def decidir(pedido):
    """Devolve a decisão (dict) para um pedido (dict). Determinística: o mesmo pedido dá a mesma decisão."""
    if not isinstance(pedido, dict):
        raise ValueError("o pedido tem de ser um objeto JSON")
    motivos = []
    c0 = pedido.get("camada0")
    consent = pedido.get("consentimento") or {}
    apar = pedido.get("aparelho") or {}
    orc = pedido.get("orcamento") or {}
    menor = bool(pedido.get("menor"))

    # Camada 0: há resposta escrita com fonte e data?
    if isinstance(c0, dict) and c0.get("texto") and c0.get("fonte") and c0.get("data"):
        return _fecho(pedido, "camada0", 0.0, ["há resposta escrita com fonte (%s, %s)" % (c0["fonte"], c0["data"])])
    motivos.append("camada 0: sem resposta escrita com fonte e data")

    # Camada 1: modelo local, só com consentimento
    if not consent.get("camada1"):
        motivos.append("camada 1: sem consentimento da pessoa")
    elif not apar.get("modelo_local"):
        motivos.append("camada 1: o modelo local não está guardado neste aparelho")
    elif _num(apar.get("ram_livre_mb", 0), "aparelho.ram_livre_mb") < RAM_CAMADA1_MB:
        motivos.append("camada 1: memória livre abaixo de %d MB" % RAM_CAMADA1_MB)
    else:
        return _fecho(pedido, "camada1", 0.0, motivos + ["modelo local com consentimento; o que disser não é conferido"])

    # Camada 2: modelo externo da UE, com consentimento para este pedido
    custo = _num(orc.get("custo_estimado_eur", 0), "orcamento.custo_estimado_eur")
    teto = _num(orc.get("teto_diario_eur", 0), "orcamento.teto_diario_eur")
    gasto = _num(orc.get("gasto_hoje_eur", 0), "orcamento.gasto_hoje_eur")
    if menor:
        motivos.append("camada 2: pedido de criança — nunca sai para fora do aparelho")
    elif not consent.get("camada2"):
        motivos.append("camada 2: sem consentimento para este pedido")
    elif not apar.get("rede"):
        motivos.append("camada 2: sem rede")
    elif teto <= 0:
        motivos.append("camada 2: sem teto diário definido (nenhum gasto sem teto)")
    elif gasto + custo > LIMITE_PARAGEM * teto:
        motivos.append("camada 2: passaria %d %% do teto diário (%.2f + %.2f > %.2f €)" % (int(LIMITE_PARAGEM * 100), gasto, custo, LIMITE_PARAGEM * teto))
    else:
        return _fecho(pedido, "camada2", custo, motivos + ["modelo externo da UE com consentimento; a resposta sai marcada como não conferida"])

    return _fecho(pedido, "recusa", 0.0, motivos + ["nenhuma camada serve: dizer que não sei e onde confirmar"])


def _fecho(pedido, rota, custo, motivos):
    decisao = {"kfc": VERSAO, "rota": rota, "custo_eur": round(custo, 4), "rede": rota == "camada2",
               "conferida": rota == "camada0", "motivos": motivos}
    recibo = {"pedido_sha256": sha256(canonico(pedido)), "decisao_sha256": sha256(canonico(decisao))}
    decisao["recibo"] = recibo
    return decisao


CASOS = [
    ("resposta escrita com fonte → camada 0",
     {"camada0": {"texto": "O subsídio de férias é 8 %.", "fonte": "wetten.overheid.nl", "data": "2026-11-02"}}, "camada0"),
    ("sem fonte e sem consentimento → recusa", {"camada0": {"texto": "talvez"}}, "recusa"),
    ("consentimento local mas sem modelo → recusa", {"consentimento": {"camada1": True}, "aparelho": {"ram_livre_mb": 900}}, "recusa"),
    ("consentimento local, modelo e memória → camada 1",
     {"consentimento": {"camada1": True}, "aparelho": {"modelo_local": True, "ram_livre_mb": 900}}, "camada1"),
    ("memória curta para o modelo local → recusa",
     {"consentimento": {"camada1": True}, "aparelho": {"modelo_local": True, "ram_livre_mb": 100}}, "recusa"),
    ("externo com consentimento, rede e teto → camada 2",
     {"consentimento": {"camada2": True}, "aparelho": {"rede": True},
      "orcamento": {"teto_diario_eur": 1.0, "gasto_hoje_eur": 0.10, "custo_estimado_eur": 0.002}}, "camada2"),
    ("externo passaria 80 % do teto → recusa",
     {"consentimento": {"camada2": True}, "aparelho": {"rede": True},
      "orcamento": {"teto_diario_eur": 1.0, "gasto_hoje_eur": 0.79, "custo_estimado_eur": 0.02}}, "recusa"),
    ("externo sem teto definido → recusa",
     {"consentimento": {"camada2": True}, "aparelho": {"rede": True}, "orcamento": {"custo_estimado_eur": 0.0}}, "recusa"),
    ("pedido de criança nunca sai → recusa",
     {"menor": True, "consentimento": {"camada2": True}, "aparelho": {"rede": True},
      "orcamento": {"teto_diario_eur": 5.0, "custo_estimado_eur": 0.001}}, "recusa"),
    ("criança com modelo local e consentimento do adulto → camada 1",
     {"menor": True, "consentimento": {"camada1": True}, "aparelho": {"modelo_local": True, "ram_livre_mb": 512}}, "camada1"),
    ("externo sem rede → recusa",
     {"consentimento": {"camada2": True}, "aparelho": {"rede": False},
      "orcamento": {"teto_diario_eur": 1.0, "custo_estimado_eur": 0.001}}, "recusa"),
]


def auto_teste(saida=print):
    bons = 0
    for nome, pedido, esperado in CASOS:
        d = decidir(pedido)
        d2 = decidir(json.loads(json.dumps(pedido)))
        ok = d["rota"] == esperado and d == d2
        bons += ok
        saida("%s  %s → %s" % ("OK " if ok else "MAL", nome, d["rota"]))
    # entradas más: tem de recusar com erro claro, nunca adivinhar
    for mau in ([], {"orcamento": {"teto_diario_eur": -1}, "consentimento": {"camada2": True}, "aparelho": {"rede": True}},
                {"orcamento": {"custo_estimado_eur": "0"}, "consentimento": {"camada2": True}, "aparelho": {"rede": True}}):
        try:
            decidir(mau)
            saida("MAL  entrada má aceite: %r" % (mau,))
        except ValueError:
            bons += 1
            saida("OK   entrada má recusada com erro claro")
    total = len(CASOS) + 3
    raiz = sha256(canonico([decidir(p) for _, p, _ in CASOS]))
    saida("%s: %d de %d · raiz das decisões %s" % (VERSAO, bons, total, raiz))
    return bons == total, raiz


def main(argv):
    if len(argv) >= 2 and argv[1] == "--auto-teste":
        ok, _ = auto_teste()
        return 0 if ok else 1
    if len(argv) == 3 and argv[1] == "decidir":
        with open(argv[2], encoding="utf-8") as f:
            pedido = json.load(f)
        try:
            print(json.dumps(decidir(pedido), ensure_ascii=False, indent=1, sort_keys=True))
        except ValueError as e:
            print("pedido recusado: %s" % e, file=sys.stderr)
            return 2
        return 0
    print(__doc__.strip().split("\n\nUso:")[0])
    print("Uso: konfirmu_frugal_router.py --auto-teste | decidir PEDIDO.json")
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv))
