#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# =============================================================================
# SPDX-License-Identifier: EUPL-1.2
# Licensed under the EUPL-1.2 only (decisão do David, 20-11-2026 07:35; GPLv3 fica de fora). [VALIDAR] falta o titular: a forma
# recomendada pela Comissão Europeia é «copyright <nome>, <data>, licensed under the EUPL» e o nome é decisão do David.
# KONFIRMU CALC v3.0 — A JUNÇÃO: as três linhas numa só, com a base-mãe dentro · «A UNIÃO COMPLETA — A BASE E A IRMANDADE» + A MATEMÁTICA DA ABUNDÂNCIA
# [VALIDAR] A ordem pede «v2.2.0». Esse número já tem um ficheiro selado (sha256 6980e0ae…): este sai como v2.4.0.
# v2.4: a irmandade (câmaras africanas no 3-de-5 desde o genesis) · S1 a S9 · veto de Gibbs · veto hídrico · --cerimonia ·
#       --auditoria · --verificar-externo FICHEIRO. Demo: D12 e D13.
# v2.5: índice de abundância A_d com a condição do ponto neutral · busca da lista de obras mais barata com poda pelo veto ·
#       pontuação das olimpíadas (ΔA, selo, vetos, custo físico). Demo: D14. O «teorema» fica [VALIDAR]: não está provado.
# v2.6: resposta mínima selada (5 campos + expansao_disponivel) · cache com invalidação pelo motor de diferenças · benchmark v3
#       em dois números (dentro e fora da cobertura) · --benchmark FICHEIRO.json. Demo: D15. Peça de referência para a /v1/facto.
# v2.7: enxame frugal — cache por incerteza (não por balde), esquema de 1 letra medido, pacote de rede em Base64 com contagem de SMS,
#       ganho da poda como conta. Demo: D16. Origem: «enxame_ultra_frugal.py» de outra IA, corrido e posto à prova.
# v2.8: correções do teste de ataque de 20-11-2026 — números não finitos recusados, texto normalizado (NFC) antes do hash,
#       zero absoluto no veto de Gibbs, necessidade zero ou valores negativos recusados na abundância; Ed25519 recusa pontos
#       de ordem pequena; o top-1 recusa na dúvida; a cache respeita a ordem das palavras; a verificação externa confere
#       formato, cabeça conhecida e notário conhecido; leituras comparam-se a 95% dos dois lados. Demo: D17.
# v2.9.0 a v2.9.10 (janela ZCode, 21-11-2026): P27 ponto neutral da IA · a porta --cura, --selo e --fichas · autoridade por
#       compromisso de chave · P14 selo híbrido com Lamport · FROST/1 da casa · o infinito computável · o arquivo para sempre ·
#       SOBRE/1 (COSE) · MARE/1 (águas, mar e pesca) · AUDIT/1 (certificação por eras).
# v2.5.2 a v2.6.9 (outra janela, 21-11-2026): oráculos mundiais · remessas e replantar · moeda do povo · circularidade (MCI) ·
#       estado neutro · para sempre · envelope KCP · tipologia · circulação · medida selada na origem · anticrime (Becker) ·
#       provar sem mostrar (Pedersen). Demo: D15 a D25.
# v3.0 (21-11-2026): A JUNÇÃO. As três linhas que partiram da v2.5.1 (A: v2.6 a v2.8 · B: v2.9.0 a v2.9.10 · C: v2.5.2 a v2.6.9)
#       ficam num só ficheiro, por fusão a três com a v2.5.1 por base. Nada foi tirado. As secções D15 a D17 da linha A passam a
#       D26 a D28; os pilares da linha B com o mesmo número de pilares da linha C mudam: P34→P44, P35→P45, P36→P46, P37→P47,
#       P39→P49, P40→P50. A base-mãe entra tal e qual (P51 a P54) e as suas 5 baterias correm no demo, sobre estas peças.
# Um ficheiro. Só a biblioteca-padrão do Python (3.10+; corrido em 3.11, 3.12 e 3.13). O demo não usa rede, relógio nem sorteios.
# Mesmo input -> mesmo output -> mesmo hash. Semente declarada: SEED = 20261120.
#
#     python3 konfirmu_calc.py --demo                      D1 a D11; tudo verde, ou sai com erro
#     python3 konfirmu_calc.py --testes                    v2.3: 19 testes em unittest (também: python3 -m unittest konfirmu_calc)
#     python3 konfirmu_calc.py --explica                   P23: a calculadora explica-se
#     python3 konfirmu_calc.py --kpkg                      P24: emite o pacote aberto do cenário ÁFRICA 2030
#     python3 konfirmu_calc.py --consome FICHEIRO          P24: refaz a conta de um pacote e diz se confere
#     python3 konfirmu_calc.py --ler-oraculos AAAA-MM-DD   P12: lê as fontes POR_LER (USA REDE; fora do demo) [VALIDAR]
#     python3 konfirmu_calc.py --base-mae                  v3.0: corre as 5 baterias da base-mãe sobre esta calculadora
#
# [VALIDAR] = escolha conservadora minha, à espera de quem manda.
# P1 grandezas · P2 veto físico · P3 selos · P4 ledger · P5 Shamir · P6 estados · P7 cofre · P8 homeostase ·
# P9 quórum · P10 linhagem · P11 voto anónimo em anel · P12 oráculos reais · P13 PROVA/1 · P15 ponto neutral ·
# P16 selo · P17 rastro vital · P18 prevenção · P19 veto↔escrow · P20 lâmpada · P21 constituição · P22 forks ·
# P23 professora · P24 pacotes abertos · P25 canários · MÉDICO M1 a M5.
# v2.9 a v3.0: P27 ponto neutral da IA · P33 a P43 da linha C · P44 a P47, P49 e P50 da linha B · P51 a P54 da base-mãe
#     (P51 quórum por cadeias independentes · P52 aritmética exacta do KCP · P53 FROST RFC 9591 · P54 DKG).
# Da v1.0 ficam, com letra B: B1 cálculo inverso (gargalo) · B2 banda de preço e cartel · B3 válvula vital e fundo.
# v2.3 (20-11-2026, 06:48): chegou a suite de outra IA («konfirmu-fable-os»). Foi corrida e posta à prova. O que lá tinha conta
# entrou aqui feito de verdade: teto de Carnot (P2) · L1 massa de uma carga e número de contentor · R1 energia de uma missão
# de drone com trava humana · S1 stock parado (cenário). O Shamir ficou mais duro: os coeficientes saem da semente E do segredo.
# O que lá é só texto fixo NÃO entrou. A licença e o nome do projeto são decisão do David: este ficheiro não leva nenhuma.
#
# P3  [VALIDAR] A ordem admite recurso a ECDSA puro. Não foi preciso: o Ed25519 puro confere com os vetores do RFC 8032.
# P14 (v2.9.3): o selo híbrido Ed25519 + Lamport ESTÁ feito; o ML-DSA (FIPS 204) continua por fazer. O plano original fica:
# P14 [ROADMAP — só comentário, NÃO está feito] Selo híbrido Ed25519 + ML-DSA (FIPS 204): cada selo leva as duas
#     assinaturas e só vale se as duas conferirem. A biblioteca-padrão não tem ML-DSA. «Guardar agora, decifrar depois»
#     é ameaça à cifra; para selos, a ameaça é forjar assinaturas antigas no dia em que houver computador quântico:
#     a defesa é re-selar a cadeia com o esquema novo antes desse dia (a ledger já fixa a ordem dos blocos).
# P26 [PONTE DEMOCRÁTICA — só comentário, fase futura] O protocolo de emenda de P21 (proposta selada + k votos
#     anónimos em anel + assinatura humana) é o terreno onde a caixa-urna cresce. Declarado; não está feito aqui.
# =============================================================================
from __future__ import annotations

import base64
import decimal
import hashlib
import hmac
import itertools
import json
import math
import os
import re
import secrets
import statistics
import subprocess
import sys
import tempfile
import unicodedata
import unittest
import zlib
from typing import Any, Dict, List, Optional, Sequence, Tuple

VERSAO = "3.0.0"
_PRODUCAO = [False]  # S2: em produção as chaves de demo são recusadas
SEED = 20261120  # semente declarada: tudo o que no demo parece sorteado (chaves, coeficientes de Shamir) sai daqui
CARIMBO = "CENÁRIO — visão, não previsão; futuro não é facto até acontecer com fonte"

# As 4 frases que a ordem manda dizer, letra a letra.
FRASES_OBRIGATORIAS: Dict[str, str] = {
    "prevencao": "Previne 30–50% dos cancros evitáveis (OMS/IARC); não substitui tratamento clínico; o ponto neutral é direcção de equilíbrio, não milagre.",
    "lampada": "A lâmpada mostra o que está no produto; quem decide és tu.",
    "deteccao": "Detecção ≠ acusação; anomalia ≠ culpado sem contraditório.",
    "cenario": CARIMBO + ".",
}
# [VALIDAR] A 1.ª frase não diz o mesmo que a fonte. A OMS escreve «Between 30–50% of all cancer cases are preventable.»
# (who.int/activities/preventing-cancer, lido a 20-11-2026): 30 a 50% de TODOS os casos são evitáveis. Fica a frase da
# ordem, sempre com a da OMS ao lado. Nada neste ficheiro mede que alguma coisa «previne» cancros.
OMS_PREVENCAO = "OMS, «Preventing cancer»: entre 30 e 50% de todos os casos de cancro são evitáveis (lido a 20-11-2026)"

O_QUE_NAO_GARANTE = (
    "Ed25519 em Python puro confere com o RFC 8032, mas não é de tempo constante nem pós-quântico: em produção, biblioteca auditada ou HSM.",
    "Shamir junta a chave num só ponto no momento de assinar: não é MPC. A ledger é assinada por uma só chave (o notário). As chaves do demo saem da semente declarada e de etiquetas públicas: não são segredo.",
    "O oráculo N=3 apanha 1 fonte má; 2 fontes em conluio enganam-no. A independência das fontes declara-se, não se prova em código.",
    "O grafo de atestados trava identidades inventadas; não trava membros verdadeiros em conluio.",
    "O tempo são dias lógicos dados por quem chama: sem relógio de confiança, os 15 dias não se impõem sozinhos.",
    "D6 é cenário: quase todos os inputs são ASSUMIDO; não modela dinheiro, baterias nem procura. Os limiares (85%, 2%, 15 dias, k=5) são escolhas.",
    "O cofre tem duas variantes de F2, F4, F5 e F8 (A: da v1.0; B: do outro ficheiro). Nenhuma foi conferida com o cofre da casa (F001–F005), que não se deixou ler.",
    "Voto em anel (P11): LSAG sobre Ed25519 em Python puro, sem auditoria e sem tempo constante. Esconde QUEM votou dentro do anel; não esconde que alguém do anel votou, nem protege quem vota coagido.",
    "Constituição (P21): o código impõe a emenda a quem corre ESTE motor. Quem correr outro, com outras regras, não é impedido: fica à vista, porque os hashes deixam de conferir. As chaves do eleitorado e da guardiã são de demo.",
    "Médico (M1 a M5): não prescreve nem diagnostica; só recusa o que passa do teto escrito na fonte. Tem 1 fármaco e 1 interação: é a prova do mecanismo, não uma farmacopeia. A guia da OMS com estes números foi retirada pela OMS em 2019; os mesmos números estão nas outras fontes citadas no cofre (hospital pediátrico, revista científica, regulador).",
    "Oráculos reais (P12): as fontes não assinam os seus números; assina quem os leu. A 20-11-2026, PVGIS, Open-Meteo e a API do BCE não se deixavam ler; a 21-11-2026 leram ao vivo (BCE 1,099 USD/EUR; Maputo 18,31/18,47 MJ/m2/dia em duas fontes a ~0,9%) e a grelha mundial da v2.5.2 entrou POR_LER (9 moedas do BCE, 9 cidades em 5 continentes; Lisboa com 2 fontes).",
    "Ponto neutral (P15 a P17): os limiares do piso humano e do teto ecológico-animal são ASSUMIDO, escritos de memória; o N_eq resume medições, não as substitui.",
    "Lâmpada (P20): mostra a análise selada de um lote por um laboratório registado e as leituras da rede; não prova quem causou uma diferença. O produto e os números do demo são fictícios.",
    "Logística, robótica e stock parado (L1, R1 e A1, da v2.3): prova do mecanismo com números de DEMO. A regra do número de contentor foi escrita de memória; o stock parado é cenário com fatores sem fonte; o drone só conhece a conta da energia e a assinatura humana.",
    "Imprimatur (v2.5.1): o selo diz QUEM assinou e que nada foi mexido; não diz que a fonte tem razão. Selado ≠ verdadeiro: a imprensa barateou a cópia, a verdade e a mentira por igual.",
    FRASES_OBRIGATORIAS["prevencao"] + " [VALIDAR] A fonte diz: " + OMS_PREVENCAO + ".",
    FRASES_OBRIGATORIAS["lampada"],
    FRASES_OBRIGATORIAS["deteccao"],
    FRASES_OBRIGATORIAS["cenario"],
    "O ponto neutral da IA (P27): fecha o dano por ESTRUTURA no que o código alcança (6 guardas executáveis no demo); não prova ausência de todo o dano. A energia é ASSUMIDO [VALIDAR] (o motor não lê o relógio); a taxa real de escape mede-se no distrito piloto; e nenhuma IA sela o próprio grau — o selo é de quem certifica FORA da IA (demo: chave da semente declarada; casa: Pérola Melo, 3-de-5).",
    "O selo híbrido (P14): Lamport é hash-based e imune ao Shor; ML-DSA-65 (FIPS 204) fica [IMPLEMENTAR]. O custo é real: 8 KB por assinatura e 16 KB de chave pública por selo híbrido — a imunidade quântica tem preço em bytes. Nunca promete inviolabilidade: se a matemática dos reticulados cair, R6 rotação — detetar e rodar.",
    "O infinito computável (P45): o ouroboros de 24 bits e os valores próprios usam parâmetros de manual [VALIDAR] e medem o que é medível; o ciclo do estado de 256 bits não é fechável por ninguém — «infinito» aqui é uma MEDIDA honesta, não uma promessa mística.",
    "O arquivo para sempre (P46): a re-selagem por eras mantém a PROVENIÊNCIA quando os algoritmos envelhecem, mas não ressuscita conteúdo perdido — se o ficheiro original se perder (OneDrive desidratado), o hash guarda a memória, não os bytes. Landauer é chão absoluto POR TENTATIVA e não modela máquinas ainda por inventar. A exaustão Shamir é sobre um segredo de 1 byte com aritmética mod L — a estrutura é a prova, a escala é honesta.",
    "Remessas (P33) e replantar (P35, v2.5.3): a taxa de referência do BCE e a média mundial do RPW NÃO são o preço que a pessoa vê no balcão; os fatores de replantação são ASSUMIDO até fonte selada. CENÁRIO — visão, não previsão.",
    "Moeda do povo (P36, v2.6.0): não é dinheiro legal; não promete valor, adopção nem paz mundial; contas do demo são sintéticas; emitir ao mundo real exige confirmação legal (MiCA — enxame M2) e decisão do proprietário.",
    "Para sempre (P37, v2.6.3): o Landauer mede a impossibilidade CLÁSSICA e a Shamir é incondicional; mas quântico é outro regime e nada é eterno por decreto — o que é para sempre é a POSSIBILIDADE de re-verificar: agilidade + âncoras + custódia.",
    "Incerteza (v2.8): a propagação é linear (GUM de primeira ordem). Com erro relativo grande fica errada: 1 / (1,0 ± 0,3) dá 1,0 ± 0,3, mas a simulação dá mediana 1,0 e 95% abaixo de 1,96. A mesma `fonte` = o MESMO erro: duas leituras de aparelhos diferentes nunca levam o mesmo nome.",
    "A junção (v3.0): a fusão a três prova que o texto de cada linha está cá e que o demo e as baterias dão verde; não prova que as ideias de uma linha e de outra não se contradizem fora do que o demo testa. Os pilares P34 a P40 da linha B mudaram de número (P44 a P50): os documentos antigos da linha B usam os números antigos. O FROST/1 da casa (P44) não é o RFC 9591 no fio: para falar com o resto do mundo, o P53.",
)

# Limiares declarados. São escolhas, não medidas. [VALIDAR]
REGRAS: Dict[str, Any] = {
    "quorum_k": 5, "prazo_dias": 15, "confianca_min": 0.85,
    "fundo_reparacao_pct": 2, "indemnizacao_por_mil_ao_dia": 1,
    "valvula_dominios": ["AGUA", "ALIMENTACAO", "SAUDE"], "valvula_max_em_30_dias": 2,
    "carimbos_max_em_30_dias": 4, "atestados_min": 3, "atestados_max_por_membro": 5,
    # anomalia em milésimos (inteiros): o ataque multiplica por 3/2, o lastro tira 100
    "homeostase": {"base": 100, "ataque_num": 3, "ataque_den": 2, "cura": 100, "alerta": 150, "defesa": 300},
    "niveis": {"FLUIDO": [3, 0], "ALERTA": [4, 1], "DEFESA": [5, 2]},  # [assinaturas em 5, dias de quarentena]
    "banda": {"janela": 12, "minimo_de_precos": 5, "k_sigma": 3.0, "piso_rel": 0.01},
    "cartel": {"zona_abaixo_do_teto": 0.02, "fracao": 0.60, "minimo_de_propostas": 3},
    "oraculo": {"n_min": 3, "tol_rel": 0.05, "u_fonte_rel": 0.03, "rho": 0.3},
    "shamir": {"k": 3, "n": 5},
    "k95_unilateral": 1.6448536269514722,
}


# -----------------------------------------------------------------------------
# 1. JSON CANÓNICO, HASH E CONTAS QUE DÃO O MESMO EM QUALQUER MÁQUINA
# -----------------------------------------------------------------------------
def _limpo(o: Any) -> Any:
    if isinstance(o, str):
        return unicodedata.normalize("NFC", o)  # v2.8: «é» escrito de duas maneiras dá o mesmo hash
    if o is None or isinstance(o, (bool, int)):
        return o
    if isinstance(o, float):
        if o != o or o in (float("inf"), float("-inf")):
            raise ValueError("NaN e infinito não entram num hash")
        return float(f"{o:.12g}")  # 12 algarismos: o mesmo texto em qualquer máquina
    if isinstance(o, (bytes, bytearray)):
        return bytes(o).hex()
    if isinstance(o, dict):
        return {unicodedata.normalize("NFC", str(k)): _limpo(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)):
        return [_limpo(v) for v in o]
    if isinstance(o, (set, frozenset)):
        return sorted(_limpo(v) for v in o)
    if isinstance(o, Grandeza):
        return o.dic()
    raise TypeError(f"não sei pôr em JSON canónico: {type(o).__name__}")


def canon(o: Any) -> bytes:
    """JSON canónico: chaves ordenadas, sem espaços, UTF-8."""
    return json.dumps(_limpo(o), sort_keys=True, ensure_ascii=False, separators=(",", ":")).encode("utf-8")


def h256(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def hobj(o: Any) -> str:
    return h256(canon(o))


# ln e exp pelo módulo decimal (arredondamento definido): não dependem da libm de cada máquina.
_DEC = decimal.Context(prec=40, rounding=decimal.ROUND_HALF_EVEN)


def ln(x: float) -> float:
    if x <= 0:
        raise ValueError("ln só de números positivos")
    return float(_DEC.ln(decimal.Decimal(x)))


def exp(x: float) -> float:
    return float(_DEC.exp(decimal.Decimal(x)))


def _ipot(x: float, k: int) -> float:
    r = 1.0
    for _ in range(abs(k)):
        r *= x
    return r if k >= 0 else 1.0 / r


def _n(x: float, casas: int = 2) -> str:
    return f"{x:.{casas}f}".replace(".", ",")


def _num(x: float, alg: int = 6) -> str:
    """Número legível: vírgula decimal, milhares com espaço, sem notação científica."""
    s = f"{x:.{alg}g}"
    if "e" in s:
        s = f"{float(s):.0f}" if abs(x) >= 1 else f"{x:.{alg + 4}f}".rstrip("0")
    sinal = "-" if s.startswith("-") else ""
    inteiro, _, dec = s.lstrip("-").partition(".")
    return sinal + f"{int(inteiro):,}".replace(",", " ") + ("," + dec if dec else "")


def _eur(centimos: int) -> str:
    return f"{centimos // 100:,}".replace(",", " ") + f",{centimos % 100:02d} EUR"


# -----------------------------------------------------------------------------
# 2. P1 — GRANDEZAS COM UNIDADE E INCERTEZA CORRELACIONADA (GUM, 1.ª ordem)
# -----------------------------------------------------------------------------
Dim = tuple  # pares (unidade-base, expoente), ordenados

_UNID: Dict[str, Tuple[float, Dict[str, int]]] = {
    "1": (1.0, {}), "%": (0.01, {}),
    "J": (1.0, {"J": 1}), "Wh": (3600.0, {"J": 1}), "kWh": (3.6e6, {"J": 1}),
    "W": (1.0, {"J": 1, "s": -1}), "kW": (1000.0, {"J": 1, "s": -1}),
    "s": (1.0, {"s": 1}), "h": (3600.0, {"s": 1}), "dia": (86400.0, {"s": 1}), "ano": (31557600.0, {"s": 1}),
    "m": (1.0, {"m": 1}), "m2": (1.0, {"m": 2}), "m3": (1.0, {"m": 3}),
    "kg": (1.0, {"J": 1, "s": 2, "m": -2}),  # kg = J·s²/m²: deixa a conta da água (rho·g·h) fechar em energia
    "EUR": (1.0, {"EUR": 1}), "USD": (1.0, {"USD": 1}),
    "pessoa": (1.0, {"pessoa": 1}), "painel": (1.0, {"painel": 1}), "microrrede": (1.0, {"microrrede": 1}),
    "ficha": (1.0, {"ficha": 1}), "caixa": (1.0, {"caixa": 1}),
    # v2.2
    "MJ": (1e6, {"J": 1}), "kcal": (4184.0, {"J": 1}), "min": (60.0, {"s": 1}),
    "g": (1e-3, {"J": 1, "s": 2, "m": -2}), "mg": (1e-6, {"J": 1, "s": 2, "m": -2}), "L": (1e-3, {"m": 3}), "mL": (1e-6, {"m": 3}),
    "°C": (1.0, {"°C": 1}),  # temperatura em graus Celsius: grandeza à parte, não se converte em kelvin (a escala tem origem própria)
    "Sv": (1.0, {"Sv": 1}), "mSv": (1e-3, {"Sv": 1}), "tCO2e": (1.0, {"tCO2e": 1}), "caso": (1.0, {"caso": 1}),
    "mol": (1.0, {"mol": 1}), "kJ": (1000.0, {"J": 1}),  # v2.4
    # v2.3
    "K": (1.0, {"K": 1}), "t": (1000.0, {"J": 1, "s": 2, "m": -2}), "aparelho": (1.0, {"aparelho": 1}), "kgCO2e": (1e-3, {"tCO2e": 1}),
    # v2.5.3 — remessas e replantar (o vocabulário do dinheiro e da terra)
    "ha": (1.0, {"ha": 1}), "arvore": (1.0, {"arvore": 1}),
}
_NOME_DE: Dict[Dim, str] = {}
for _nome, (_f, _d) in _UNID.items():
    if _f == 1.0:
        _NOME_DE.setdefault(tuple(sorted(_d.items())), _nome)


def _unid(txt: str) -> Tuple[float, Dim]:
    """'kWh/dia/pessoa', 'W/m2', 'pessoa*dia/kWh', 'm^2' -> (fator para a base, dimensão)."""
    f, d, s = 1.0, {}, 1
    for tok in re.split(r"([*/·])", txt.replace(" ", "")):
        if tok in ("*", "·"):
            s = 1
        elif tok == "/":
            s = -1
        else:
            nome, _, e = tok.partition("^")
            if nome not in _UNID:
                raise TypeError(f"unidade desconhecida: {nome!r}")
            fu, du = _UNID[nome]
            k = s * (int(e) if e else 1)
            f *= _ipot(fu, k)
            for b, x in du.items():
                d[b] = d.get(b, 0) + x * k
    return f, tuple(sorted((b, x) for b, x in d.items() if x))


def _dmul(a: Dim, b: Dim, s: int) -> Dim:
    d = dict(a)
    for k, x in b:
        d[k] = d.get(k, 0) + s * x
    return tuple(sorted((k, x) for k, x in d.items() if x))


def _dstr(d: Dim) -> str:
    return "·".join(k if x == 1 else f"{k}^{x}" for k, x in d) or "1"


def _mix(ca: Dict[Any, float], fa: float, cb: Dict[Any, float], fb: float) -> Dict[Any, float]:
    r = {k: x * fa for k, x in ca.items()}
    for k, x in cb.items():
        r[k] = r.get(k, 0.0) + x * fb
    return r


class Grandeza:
    """valor ± incerteza, com unidade. A incerteza guarda-se por FONTE de erro: duas grandezas
    que partilham uma fonte ficam correlacionadas sem mais nada; x − x dá 0 ± 0."""
    __slots__ = ("v", "c", "d", "rot")

    def __init__(self, v: float, c: Dict[Any, float], d: Dim, rot: str = ""):
        self.v, self.c, self.d = float(v), c, d
        if not math.isfinite(self.v) or not all(math.isfinite(x) for x in c.values()):  # v2.8
            raise ValueError("valor ou incerteza não finitos (NaN ou infinito): recusado")
        self.rot = rot or _NOME_DE.get(d) or _dstr(d)

    @property
    def u(self) -> float:
        return math.sqrt(sum(x * x for x in self.c.values()))

    def em(self, unidade: str) -> Tuple[float, float]:
        f, d = _unid(unidade)
        if d != self.d:
            raise TypeError(f"{self.rot} não se exprime em {unidade}")
        return self.v / f, self.u / f

    def txt(self, unidade: str, casas: int = 2) -> str:
        v, u = self.em(unidade)
        return f"{_n(v, casas)} ± {_n(u, casas)} {unidade}"

    def dic(self) -> Dict[str, Any]:
        return {"valor_base": self.v, "incerteza_base": self.u, "dimensao": _dstr(self.d)}

    def _par(self, o: Any, verbo: str) -> "Grandeza":
        o = o if isinstance(o, Grandeza) else Grandeza(o, {}, ())
        if o.d != self.d:
            raise TypeError(f"não se pode {verbo} {self.rot} com {o.rot}")
        return o

    def __add__(self, o: Any) -> "Grandeza":
        o = self._par(o, "somar")
        return Grandeza(self.v + o.v, _mix(self.c, 1.0, o.c, 1.0), self.d, self.rot)

    __radd__ = __add__

    def __sub__(self, o: Any) -> "Grandeza":
        o = self._par(o, "subtrair")
        return Grandeza(self.v - o.v, _mix(self.c, 1.0, o.c, -1.0), self.d, self.rot)

    def __rsub__(self, o: Any) -> "Grandeza":
        return (self * -1.0) + o

    def __mul__(self, o: Any) -> "Grandeza":
        if not isinstance(o, Grandeza):
            return Grandeza(self.v * o, {k: x * o for k, x in self.c.items()}, self.d, self.rot)
        return Grandeza(self.v * o.v, _mix(self.c, o.v, o.c, self.v), _dmul(self.d, o.d, 1))

    __rmul__ = __mul__

    def __truediv__(self, o: Any) -> "Grandeza":
        if not isinstance(o, Grandeza):
            return Grandeza(self.v / o, {k: x / o for k, x in self.c.items()}, self.d, self.rot)
        return Grandeza(self.v / o.v, _mix(self.c, 1.0 / o.v, o.c, -self.v / (o.v * o.v)), _dmul(self.d, o.d, -1))

    def __rtruediv__(self, o: Any) -> "Grandeza":
        return Grandeza(o, {}, ()) / self

    def __pow__(self, p: int) -> "Grandeza":
        if not isinstance(p, int) or isinstance(p, bool):
            raise TypeError("expoente inteiro; para expoente real usar g_exp(p * g_ln(x)) em grandezas sem dimensão")
        dv = p * _ipot(self.v, p - 1)
        return Grandeza(_ipot(self.v, p), {k: x * dv for k, x in self.c.items()}, tuple((k, x * p) for k, x in self.d) if p else ())


def g_ln(x: Grandeza) -> Grandeza:
    if x.d:
        raise TypeError(f"ln exige grandeza sem dimensão; veio {x.rot}")
    return Grandeza(ln(x.v), {k: c / x.v for k, c in x.c.items()}, ())


def g_exp(x: Grandeza) -> Grandeza:
    if x.d:
        raise TypeError(f"exp exige grandeza sem dimensão; veio {x.rot}")
    v = exp(x.v)
    return Grandeza(v, {k: c * v for k, c in x.c.items()}, ())


_SEQ = [0]


def G(valor: float, incerteza: float = 0.0, unidade: str = "1", fonte: Any = None) -> Grandeza:
    """Cria uma grandeza. `fonte` identifica a origem do erro: a mesma fonte = o mesmo erro."""
    f, d = _unid(unidade)
    if isinstance(valor, bool) or not isinstance(valor, (int, float)) or isinstance(incerteza, bool) or not isinstance(incerteza, (int, float)):
        raise TypeError("valor e incerteza têm de ser números")  # v2.8: «10» em texto ou True não passam
    if not (math.isfinite(valor) and math.isfinite(incerteza)):
        raise ValueError("valor ou incerteza não finitos (NaN ou infinito): recusado")
    if incerteza < 0:
        raise ValueError("a incerteza não pode ser negativa")
    if fonte is None:
        _SEQ[0] += 1
        fonte = ("auto", _SEQ[0])
    return Grandeza(valor * f, {fonte: incerteza * f} if incerteza else {}, d, unidade)


def lote(valor: float, incerteza: float, unidade: str, id_lote: str, rho: float, n: int) -> List[Grandeza]:
    """n peças do mesmo lote, com correlação rho (0..1) entre os erros de cada uma.
    Cada erro = parte comum ao lote (rho) + parte própria (1 − rho)."""
    return [GrandezaFisica(valor, incerteza, unidade, rho, "ASSUMIDO", id_lote) for _ in range(n)]


class GrandezaFisica(Grandeza):
    """A forma da ordem: GrandezaFisica(valor, erro, unidade, rho=0.0, etiqueta="MEDIDO", fonte="").
    Duas grandezas com a mesma `fonte` partilham a parte raiz(rho) do erro; o resto é de cada uma.
    Sem `fonte` não há com quem partilhar: o erro é todo próprio. Daí sai, sem fórmula à parte,
    a incerteza da média de N medidas iguais:  u_c = (u / raiz(N)) · raiz(1 + (N − 1) · rho).
    As contas (+ − × ÷) devolvem Grandeza; a etiqueta vive nos inputs e nas fórmulas do cofre (P7)."""
    __slots__ = ("etiqueta", "fonte")

    def __init__(self, valor: float, erro: float = 0.0, unidade: str = "1", rho: float = 0.0,
                 etiqueta: str = "MEDIDO", fonte: str = "") -> None:
        if erro < 0 or not 0.0 <= rho <= 1.0:
            raise ValueError("o erro não pode ser negativo e rho tem de estar entre 0 e 1")
        if etiqueta not in ("MEDIDO", "ASSUMIDO"):
            raise ValueError("etiqueta: MEDIDO ou ASSUMIDO")
        f, d = _unid(unidade)
        _SEQ[0] += 1
        c: Dict[Any, float] = {}
        if fonte and rho > 0.0 and erro:
            c[("fonte", fonte)] = math.sqrt(rho) * erro * f
        proprio = (math.sqrt(1.0 - rho) if fonte else 1.0) * erro * f
        if proprio:
            c[("propria", _SEQ[0])] = proprio
        super().__init__(valor * f, c, d, unidade)
        self.etiqueta, self.fonte = etiqueta, fonte


# -----------------------------------------------------------------------------
# 3. P3 — SELOS: SHA-256 + Ed25519 (RFC 8032) EM ARITMÉTICA MODULAR PURA, PRIMO 2^255 − 19
# -----------------------------------------------------------------------------
_P = 2 ** 255 - 19
_L = 2 ** 252 + 27742317777372353535851937790883648493
_D = -121665 * pow(121666, _P - 2, _P) % _P
_I = pow(2, (_P - 1) // 4, _P)
Ponto = Tuple[int, int, int, int]  # coordenadas estendidas (X, Y, Z, T)


def _ed_soma(a: Ponto, b: Ponto) -> Ponto:
    A = (a[1] - a[0]) * (b[1] - b[0]) % _P
    B = (a[1] + a[0]) * (b[1] + b[0]) % _P
    C = 2 * a[3] * b[3] * _D % _P
    Z = 2 * a[2] * b[2] % _P
    E, F, Gg, H = B - A, Z - C, Z + C, B + A
    return (E * F % _P, Gg * H % _P, F * Gg % _P, E * H % _P)


def _ed_mult(s: int, p: Ponto) -> Ponto:
    q: Ponto = (0, 1, 1, 0)
    while s > 0:
        if s & 1:
            q = _ed_soma(q, p)
        p = _ed_soma(p, p)
        s >>= 1
    return q


def _ed_igual(a: Ponto, b: Ponto) -> bool:
    return (a[0] * b[2] - b[0] * a[2]) % _P == 0 and (a[1] * b[2] - b[1] * a[2]) % _P == 0


def _ed_x(y: int, sinal: int) -> Optional[int]:
    if y >= _P:
        return None
    x2 = (y * y - 1) * pow(_D * y * y + 1, _P - 2, _P) % _P
    if x2 == 0:
        return None if sinal else 0
    x = pow(x2, (_P + 3) // 8, _P)
    if (x * x - x2) % _P != 0:
        x = x * _I % _P
    if (x * x - x2) % _P != 0:
        return None
    if (x & 1) != sinal:
        x = _P - x
    return x


_GY = 4 * pow(5, _P - 2, _P) % _P
_GX = _ed_x(_GY, 0)
_ED_G: Ponto = (_GX, _GY, 1, _GX * _GY % _P)  # type: ignore[operator]


def _ed_comp(p: Ponto) -> bytes:
    zi = pow(p[2], _P - 2, _P)
    x, y = p[0] * zi % _P, p[1] * zi % _P
    return (y | ((x & 1) << 255)).to_bytes(32, "little")


def _ed_descomp(b: bytes) -> Optional[Ponto]:
    if len(b) != 32:
        return None
    y = int.from_bytes(b, "little")
    sinal = y >> 255
    y &= (1 << 255) - 1
    x = _ed_x(y, sinal)
    return None if x is None else (x, y, 1, x * y % _P)


def _ed_h(b: bytes) -> int:
    return int.from_bytes(hashlib.sha512(b).digest(), "little") % _L


_ED_CHAVES: Dict[bytes, Tuple[int, bytes, bytes]] = {}


def _ed_expande(sk: bytes) -> Tuple[int, bytes, bytes]:
    if sk not in _ED_CHAVES:
        if len(sk) != 32:
            raise ValueError("a chave privada Ed25519 tem 32 bytes")
        h = hashlib.sha512(sk).digest()
        a = int.from_bytes(h[:32], "little")
        a &= (1 << 254) - 8
        a |= 1 << 254
        _ED_CHAVES[sk] = (a, h[32:], _ed_comp(_ed_mult(a, _ED_G)))
    return _ED_CHAVES[sk]


def ed_publica(sk: bytes) -> bytes:
    return _ed_expande(sk)[2]


def ed_assinar(sk: bytes, msg: bytes) -> bytes:
    a, prefixo, A = _ed_expande(sk)
    r = _ed_h(prefixo + msg)
    R = _ed_comp(_ed_mult(r, _ED_G))
    return R + ((r + _ed_h(R + A + msg) * a) % _L).to_bytes(32, "little")


def ed_verificar(pk: bytes, msg: bytes, sig: bytes) -> bool:
    if len(pk) != 32 or len(sig) != 64:
        return False
    A, R = _ed_descomp(pk), _ed_descomp(sig[:32])
    if A is None or R is None:
        return False
    if _ed_igual(_ed_mult(8, A), _ED_ID) or _ed_igual(_ed_mult(8, R), _ED_ID):  # v2.8: chave ou R de ordem pequena = assinatura que serve para tudo
        return False
    s = int.from_bytes(sig[32:], "little")
    if s >= _L:
        return False
    return _ed_igual(_ed_mult(s, _ED_G), _ed_soma(R, _ed_mult(_ed_h(sig[:32] + pk + msg), A)))


def selar(obj: Any, sk: bytes) -> Dict[str, str]:
    """Selo = SHA-256 do JSON canónico + assinatura Ed25519 desses bytes."""
    m = canon(obj)
    return {"alg": "Ed25519+SHA-256", "hash": h256(m), "pub": ed_publica(sk).hex(), "sig": ed_assinar(sk, m).hex()}


_SELOS_VISTOS: Dict[Tuple[str, str, str], bool] = {}


def selo_ok(obj: Any, selo: Dict[str, str], aceites: Optional[Any] = None) -> bool:
    """True só se o conteúdo é o selado, a assinatura confere e (se dado) a chave é uma das aceites."""
    try:
        m = bytes(obj) if isinstance(obj, (bytes, bytearray)) else canon(obj)
        if not hmac.compare_digest(h256(m), str(selo["hash"])) or (aceites is not None and selo["pub"] not in aceites):  # S1
            return False
        chave = (selo["hash"], selo["pub"], selo["sig"])
        if chave not in _SELOS_VISTOS:
            _SELOS_VISTOS[chave] = ed_verificar(bytes.fromhex(selo["pub"]), m, bytes.fromhex(selo["sig"]))
        return _SELOS_VISTOS[chave]
    except (KeyError, TypeError, ValueError):
        return False


# -----------------------------------------------------------------------------
# 4. P4 — LEDGER IMUTÁVEL: CADEIA DE HASHES COM BLOCOS ASSINADOS (só acrescenta; tempo = dia lógico)
# -----------------------------------------------------------------------------
def conferir_blocos(blocos: Sequence[Dict[str, Any]], pub: str, anterior: str = "0" * 64, n0: int = 0) -> bool:
    """Confere um troço de cadeia: numeração, ligação ao bloco anterior, hash de cada bloco e assinatura de quem a escreve."""
    try:
        for i, b in enumerate(blocos, n0):
            corpo = {k: v for k, v in b.items() if k not in ("hash_atual", "assinatura")}
            if b["n"] != i or b["hash_anterior"] != anterior or hobj(corpo) != b["hash_atual"]:
                return False
            m = bytes.fromhex(b["hash_atual"])
            if not selo_ok(m, {"hash": h256(m), "pub": pub, "sig": b["assinatura"]}):
                return False
            anterior = b["hash_atual"]
    except (KeyError, TypeError, ValueError, AttributeError):
        return False
    return True


class LedgerImutavel:
    """Só acrescenta. Cada bloco guarda hash_anterior, payload, hash_atual e assinatura
    (Ed25519 do notário sobre hash_atual). Mexer num byte parte a cadeia; refazer os hashes
    sem a chave do notário parte as assinaturas."""

    def __init__(self, sk_notario: bytes) -> None:
        self._sk = sk_notario
        self.pub = ed_publica(sk_notario).hex()
        self.blocos: List[Dict[str, Any]] = []
        self.respostas: List[Dict[str, Any]] = []  # P10: as respostas emitidas sobre esta ledger

    def cabeca(self) -> str:
        return self.blocos[-1]["hash_atual"] if self.blocos else "0" * 64

    def registar(self, dia: int, evento: str, payload: Any) -> str:
        corpo = {"n": len(self.blocos), "dia": dia, "evento": evento, "payload": _limpo(payload), "hash_anterior": self.cabeca()}
        atual = hobj(corpo)
        self.blocos.append(dict(corpo, hash_atual=atual, assinatura=ed_assinar(self._sk, bytes.fromhex(atual)).hex()))
        return atual

    def verificar_integridade_cadeia(self) -> bool:
        return conferir_blocos(self.blocos, self.pub)


# -----------------------------------------------------------------------------
# 5. P5 — SHAMIR k-de-n SOBRE UM PRIMO GRANDE (interpolação de Lagrange)
# -----------------------------------------------------------------------------
_PS = 2 ** 521 - 1          # por defeito: cabe lá uma chave de 256 bits inteira
PRIMO_DA_ORDEM = 2 ** 127 - 1  # o primo que a ordem dá: serve para segredos até 126 bits
# [VALIDAR] A ordem pede 2^127 − 1. A chave Ed25519 do cofre tem 256 bits e não cabe nesse corpo,
# por isso o cofre usa 2^521 − 1. O primo é parâmetro: o demo prova o mesmo código com os dois.


def _determinista(semente: bytes, rotulo: str, i: int) -> int:
    """Número pseudo-aleatório reprodutível a partir de uma semente DECLARADA.
    Em produção os coeficientes têm de vir de um gerador criptográfico e nunca se repetem. [VALIDAR]"""
    return int.from_bytes(b"".join(hashlib.sha512(semente + f"|{rotulo}|{i}|{j}".encode()).digest() for j in range(2)), "big")


def shamir_partir(segredo: int, k: int, n: int, semente: bytes, primo: int = _PS) -> List[Tuple[int, int]]:
    if not (0 <= segredo < primo and 1 < k <= n):
        raise ValueError("segredo ou limiar inválido")
    # v2.3: os coeficientes saem da semente E do próprio segredo (como o nonce do Ed25519). Com a semente e 1 parte já não se
    # tira o segredo por uma conta direta, e a mesma semente com 2 segredos já não mostra a diferença entre eles.
    # Um segredo fraco continua adivinhável: em produção, gerador criptográfico. [VALIDAR]
    mistura = semente + b"|" + segredo.to_bytes((primo.bit_length() + 7) // 8, "big") + f"|{k}|{n}|{primo}".encode()
    coef = [segredo] + [_determinista(mistura, "shamir", i) % primo for i in range(1, k)]

    def f(x: int) -> int:
        y = 0
        for a in reversed(coef):
            y = (y * x + a) % primo
        return y

    return [(x, f(x)) for x in range(1, n + 1)]


def shamir_juntar(partes: Sequence[Tuple[int, int]], primo: int = _PS) -> int:
    if len({x for x, _ in partes}) != len(partes):
        raise ValueError("partes repetidas")
    s = 0
    for i, (xi, yi) in enumerate(partes):
        num = den = 1
        for j, (xj, _) in enumerate(partes):
            if i != j:
                num = num * (-xj) % primo
                den = den * (xi - xj) % primo
        s = (s + yi * num * pow(den, primo - 2, primo)) % primo
    return s


# -----------------------------------------------------------------------------
# 6. P12 — ORÁCULO TRIANGULADO (N>=3, nunca autorrelato) E CONFIANÇA  (as leituras reais gravadas estão na secção 16)
# -----------------------------------------------------------------------------
def oraculo(leituras: Sequence[Dict], fontes: Dict[str, Dict[str, str]], unidade: str, ref: str,
            excluir_operador: Optional[str] = None, janela: Optional[Tuple[int, int]] = None) -> Dict[str, Any]:
    """Cada leitura = {"dados": {fonte, valor, unidade, ref, dia}, "selo": {alg, hash, pub, sig}} selada pela própria fonte.
    Confiança = fração das fontes válidas que concordam entre si. Menos de 3 operadores diferentes = nada.
    `janela` = (primeiro dia, último dia) em que a leitura vale."""
    R = REGRAS["oraculo"]
    validas: Dict[str, float] = {}
    rejeitadas: List[List[str]] = []
    for l in leituras:
        d = l.get("dados", {})
        f = fontes.get(d.get("fonte"))
        if f is None:
            motivo = "FONTE_DESCONHECIDA"
        elif f["operador"] == excluir_operador:
            motivo = "AUTORRELATO"
        elif d.get("ref") != ref or d.get("unidade") != unidade:
            motivo = "DE_OUTRA_OBRA_OU_UNIDADE"
        elif janela is not None and not (isinstance(d.get("dia"), int) and janela[0] <= d["dia"] <= janela[1]):
            motivo = "FORA_DO_PRAZO"  # leitura antiga reapresentada não vale
        elif not selo_ok(d, l.get("selo", {}), {f["pub"]}):
            motivo = "SELO_INVALIDO"
        else:
            validas[d["fonte"]] = float(d["valor"])
            continue
        rejeitadas.append([str(d.get("fonte")), motivo])
    base = {"n_validas": len(validas), "rejeitadas": sorted(rejeitadas), "discrepantes": []}
    if len(validas) < R["n_min"] or len({fontes[f]["operador"] for f in validas}) < R["n_min"]:
        return dict(base, estado="INSUFICIENTE", confianca=0.0)
    xs = sorted(validas.values())
    m = statistics.median(xs)
    mad = statistics.median(sorted(abs(x - m) for x in xs))
    tol = max(3 * 1.4826 * mad, R["tol_rel"] * abs(m))
    conc = sorted(f for f in validas if abs(validas[f] - m) <= tol)
    disc = sorted(f for f in validas if f not in conc)
    vc = sorted(validas[f] for f in conc)
    mc = statistics.median(vc)
    madc = statistics.median(sorted(abs(x - mc) for x in vc))
    n = len(vc)
    # incerteza do consenso com correlação entre fontes (fator GUM: raiz(1 + (n − 1)·rho) / raiz(n))
    u = max(1.4826 * madc, R["u_fonte_rel"] * abs(mc)) / math.sqrt(n) * math.sqrt(1 + (n - 1) * R["rho"])
    return dict(base, estado="DISCREPANCIA" if disc else "CONSENSO", valor=mc, incerteza=u,
                confianca=len(conc) / len(validas), concordantes=conc, discrepantes=disc)


# -----------------------------------------------------------------------------
# 7. B2 (P13 na v1.0) — BANDA DE PREÇO ROBUSTA (mediana + MAD, janela móvel) E SINAL DE CARTEL
# -----------------------------------------------------------------------------
def banda_preco(historico: Sequence[float]) -> Optional[Dict[str, float]]:
    R = REGRAS["banda"]
    h = [float(x) for x in historico][-R["janela"]:]
    if len(h) < R["minimo_de_precos"]:
        return None  # banda fraca: não serve para punir
    m = statistics.median(sorted(h))
    mad = statistics.median(sorted(abs(x - m) for x in h))
    s = max(1.4826 * mad, R["piso_rel"] * abs(m))  # desvio robusto, com piso para históricos muito juntos
    return {"mediana": m, "desvio_robusto": s, "piso": max(0.0, m - R["k_sigma"] * s), "teto": m + R["k_sigma"] * s, "n": len(h)}


def sinal_de_cartel(propostas: Sequence[float], banda: Dict[str, float]) -> Dict[str, Any]:
    """Propostas coladas ao teto: >= 60% delas nos últimos 2% abaixo do teto.
    A zona nunca desce para perto da mediana, para não confundir preço de mercado com cartel."""
    R = REGRAS["cartel"]
    teto, m = banda["teto"], banda["mediana"]
    inicio = max(teto * (1.0 - R["zona_abaixo_do_teto"]), m + 0.8 * (teto - m))
    na_zona = [p for p in propostas if inicio <= p <= teto]
    fracao = len(na_zona) / len(propostas) if propostas else 0.0
    return {"zona": [inicio, teto], "fracao_na_zona": fracao,
            "sinal": len(propostas) >= R["minimo_de_propostas"] and fracao >= R["fracao"]}


# -----------------------------------------------------------------------------
# 8. P9 — QUÓRUM k>=5 COM PSEUDÓNIMOS: GRAFO DE ATESTADOS ASSINADOS E LIMITES DECLARADOS
# -----------------------------------------------------------------------------
class Aldeia:
    def __init__(self, raizes: Dict[str, str]) -> None:
        self.membros: Dict[str, str] = dict(raizes)  # pseudónimo -> chave pública
        self.atestados: Dict[str, frozenset] = {}     # pseudónimo -> quem o atestou
        self.dados_por: Dict[str, int] = {}           # quantos atestados cada membro já deu
        self.carimbos: Dict[str, Dict[str, int]] = {}  # pseudónimo -> {obra: dia}

    def admitir(self, pseud: str, pub: str, atestados: Sequence[Dict]) -> Tuple[bool, str]:
        """Entra quem tiver 3 atestados ASSINADOS por membros já registados. Cada membro atesta no máximo 5."""
        if pseud in self.membros:
            return False, "JA_EXISTE"
        bons = set()
        for a in atestados:
            q = a.get("por")
            if (q in self.membros and q != pseud and self.dados_por.get(q, 0) < REGRAS["atestados_max_por_membro"]
                    and selo_ok({"atesto": pseud, "pub": pub}, a.get("selo", {}), {self.membros[q]})):
                bons.add(q)
        if len(bons) < REGRAS["atestados_min"]:
            return False, "ATESTADOS_INSUFICIENTES"
        for q in bons:
            self.dados_por[q] = self.dados_por.get(q, 0) + 1
        self.membros[pseud], self.atestados[pseud] = pub, frozenset(bons)
        return True, "ADMITIDO"

    def _grupos(self, ps: Sequence[str]) -> int:
        """Votantes que partilham 2 ou mais atestadores contam como UM só (o mesmo padrinho não vota 5 vezes)."""
        ps = sorted(ps)
        pai = {p: p for p in ps}

        def raiz(x: str) -> str:
            while pai[x] != x:
                x = pai[x]
            return x

        for i, a in enumerate(ps):
            for b in ps[i + 1:]:
                if len(self.atestados.get(a, frozenset()) & self.atestados.get(b, frozenset())) >= 2:
                    pai[raiz(b)] = raiz(a)
        return len({raiz(p) for p in ps})

    def contar(self, votos: Sequence[Dict], obra: str, dia: int, desde: Optional[int] = None) -> Dict[str, Any]:
        vistos: Dict[str, bool] = {}
        ignorados: List[List[str]] = []
        for v in votos:
            d = v.get("dados", {})
            p = d.get("quem")
            if p not in self.membros:
                ignorados.append([str(p), "NAO_REGISTADO"])
            elif d.get("obra") != obra or not selo_ok(d, v.get("selo", {}), {self.membros[p]}):
                ignorados.append([p, "SELO_INVALIDO"])
            elif p in vistos:
                ignorados.append([p, "VOTO_REPETIDO"])
            elif desde is not None and not (isinstance(d.get("dia"), int) and desde <= d["dia"] <= dia):
                ignorados.append([p, "FORA_DO_PRAZO"])  # voto antigo reapresentado não vale
            else:
                recentes = {o: t for o, t in self.carimbos.get(p, {}).items() if dia - t < 30}
                if obra not in recentes and len(recentes) >= REGRAS["carimbos_max_em_30_dias"]:
                    ignorados.append([p, "LIMITE_DE_CARIMBOS"])
                    continue
                recentes[obra] = dia
                self.carimbos[p] = recentes
                vistos[p] = bool(d.get("conforme"))
        return {"conformes": self._grupos([p for p in vistos if vistos[p]]),
                "desconformes": self._grupos([p for p in vistos if not vistos[p]]),
                "ignorados": sorted(ignorados)}


# -----------------------------------------------------------------------------
# 9. B3 (P14 na v1.0) — VÁLVULA VITAL (assinatura pública, no máximo 2 em 30 dias por pessoa)
# -----------------------------------------------------------------------------
class Valvula:
    def __init__(self, responsaveis: Dict[str, str]) -> None:
        self.responsaveis = dict(responsaveis)  # nome público -> chave pública
        self.usos: Dict[str, List[int]] = {}

    def acionar(self, dominio: str, hash_pedido: str, quem: Optional[str], selo: Dict, dia: int) -> Tuple[bool, str]:
        if dominio not in REGRAS["valvula_dominios"]:
            return False, "DOMINIO_NAO_VITAL"
        if quem not in self.responsaveis or not selo_ok({"valvula": hash_pedido, "dominio": dominio, "dia": dia}, selo,
                                                        {self.responsaveis[quem]}):
            return False, "ASSINATURA_INVALIDA"
        recentes = [t for t in self.usos.get(quem, []) if dia - t < 30]
        if len(recentes) >= REGRAS["valvula_max_em_30_dias"]:
            return False, "LIMITE_2_EM_30_DIAS"
        self.usos[quem] = recentes + [dia]
        return True, "ABERTA"


# -----------------------------------------------------------------------------
# 10. P2 + P7 — VETO FÍSICO E COFRE DE FÓRMULAS VERSIONADO
# -----------------------------------------------------------------------------
class VetoFisico(ValueError):
    """Rendimento que a física não deixa passar. É um ValueError: quem apanha ValueError apanha o veto."""


# Registo versionado e parametrizável dos tetos de rendimento por tecnologia (os dois valores são os da ordem).
# [VALIDAR] 33,7% é o teto de Shockley-Queisser de UMA junção no melhor material. O teto do silício é mais
# baixo (29,4% com recombinação Auger). Fica o valor da ordem, o mais permissivo: nunca veta um painel verdadeiro.
TETOS_VERSAO = "1.0.0"
TETOS_TECNOLOGIA: Dict[str, Dict[str, Any]] = {
    "silicio_juncao_unica": {"teto": 0.337, "nome": "Shockley-Queisser, junção única", "etiqueta": "MEDIDO",
                             "fonte": "Shockley e Queisser (1961); 33,7% é o limite citado para uma junção; lido a 20-11-2026"},
    "perovskite_tandem": {"teto": 0.430, "nome": "tandem de 2 junções, perovskite sobre silício", "etiqueta": "MEDIDO",
                          "fonte": "EES Solar 2025, 1, 1030 (DOI 10.1039/d5el00085h): 43,2% com silício real; lido a 20-11-2026"},
}
TETO_ABSOLUTO = 0.868  # [VALIDAR] limite termodinâmico com infinitas junções e concentração máxima


def veto_fisico(eta: Grandeza, tecnologia: str = "silicio_juncao_unica", prova_laboratorial: Any = False,
                laboratorios: Optional[Dict[str, str]] = None) -> str:
    """P2. Acima do teto da tecnologia só passa com prova laboratorial SELADA por um laboratório registado.
    [VALIDAR] A ordem fala numa flag prova_laboratorial=True. Uma flag sem selo qualquer um a liga:
    aqui True sozinho não chega (escolha conservadora). Tecnologia fora do registo = recusada."""
    v = eta.em("1")[0]
    if tecnologia not in TETOS_TECNOLOGIA:
        raise VetoFisico(f"a tecnologia «{tecnologia}» não está no registo de tetos: recusada por defeito")
    t = TETOS_TECNOLOGIA[tecnologia]
    if not 0.0 < v <= 1.0:
        raise VetoFisico(f"rendimento de {_n(v * 100, 1)}% não existe: tem de estar entre 0 e 100%")
    if v <= t["teto"]:
        return "DENTRO_DO_TETO"
    if v > TETO_ABSOLUTO:
        raise VetoFisico(f"rendimento de {_n(v * 100, 1)}% passa o limite termodinâmico ({_n(TETO_ABSOLUTO * 100, 1)}%): nenhuma prova o salva")
    p = prova_laboratorial
    if (isinstance(p, dict) and laboratorios and p.get("laboratorio") in laboratorios
            and selo_ok(p.get("dados"), p.get("selo", {}), {laboratorios[p["laboratorio"]]})
            and p["dados"].get("rendimento_medido", 0.0) >= v):
        return "ACIMA_DO_TETO_COM_PROVA_LABORATORIAL"
    porque = ("a flag prova_laboratorial=True sem selo de laboratório registado não chega" if p is True
              else "sem prova laboratorial selada, rejeitado")
    raise VetoFisico(f"rendimento de {_n(v * 100, 1)}% passa o teto de {_n(t['teto'] * 100, 1)}% ({t['nome']}) de «{tecnologia}». "
                     "Há células de várias junções acima disto em laboratório; " + porque)


# O cofre guarda DUAS variantes de F2, F4, F5 e F8. Nenhuma se deita fora; qual é a oficial decide quem manda.
#   variante A (FORMULAS)   — a da v1.0: energia; o produto fecha em pessoas; é a que o cenário de D6 usa.
#   variante B (FORMULAS_B) — as do outro konfirmu_calc.py (de outra IA, recebido a 20-11-2026 04:03), tal e
#                             qual, agora com unidades conferidas pelo motor.
# [VALIDAR] O cofre da casa (F001–F005, pedido de código #1399, KON-481) não se deixou ler a 20-11-2026:
# nenhuma das duas variantes foi conferida com ele.
FORMULAS: Dict[str, Dict[str, Any]] = {
    "F2": {"id": "F2", "versao": "1.0.0", "nome": "produção",
           "formula": "E = n · A · G_stc · eta · PR · HSP   (G_stc = 1000 W/m2, por definição)",
           "unidades": {"paineis": "painel/microrrede", "area": "m2/painel", "rendimento": "%", "pr": "1",
                        "sol_pico": "h/dia", "saida": "kWh/dia/microrrede"},
           "etiqueta": "MEDIDO", "teto_de_rendimento": "silicio_juncao_unica",
           "fonte": "física do painel em condições-padrão de ensaio (STC); PR = perdas reais do sistema",
           "o_que_nao_garante": "não dimensiona baterias, inversor nem sombras; o PR mete todas as perdas num só número"},
    "F4": {"id": "F4", "versao": "1.0.0", "nome": "dividendo demográfico",
           "formula": "I = J · a · f   (jovens que chegam à idade de trabalhar × anos × fração formada)",
           "unidades": {"jovens_por_ano": "pessoa/ano", "anos": "ano", "fracao_formada": "1", "saida": "pessoa"},
           "etiqueta": "ASSUMIDO", "fonte": "forma escolhida nesta v1.0 [VALIDAR]",
           "o_que_nao_garante": "formado não é empregado; não conta abandono nem migração"},
    "F5": {"id": "F5", "versao": "1.0.0", "nome": "alcance",
           "formula": "R = (1 − p) / c   (pessoas servidas por cada kWh/dia produzido)",
           "unidades": {"perdas": "1", "consumo_basico": "kWh/dia/pessoa", "saida": "pessoa*dia/kWh"},
           "etiqueta": "ASSUMIDO", "fonte": "forma escolhida nesta v1.0 [VALIDAR]",
           "o_que_nao_garante": "conta pessoas servidas pelo programa; não desconta quem teria luz de outra forma (linha «sem nós»)"},
    "F8": {"id": "F8", "versao": "1.0.0", "nome": "aprendizagem",
           "formula": "M = ((1 − b) · T / t1)^(1/(1 − b)),  b = −log2(1 − LR)   (lei de Wright somada no tempo)",
           "unidades": {"horas_pratica": "h", "horas_primeira": "h", "taxa_aprendizagem": "1", "saida": "microrrede/pessoa"},
           "etiqueta": "ASSUMIDO",
           "fonte": "lei de Wright (1936): cada duplicação da experiência corta o tempo por unidade em LR; aplicada aqui por analogia [VALIDAR]",
           "o_que_nao_garante": "aproximação contínua da soma; a taxa de aprendizagem de instalar microrredes não foi medida"},
}
ENTRADA_DE = {"paineis": "F2", "area": "F2", "rendimento": "F2", "pr": "F2", "sol_pico": "F2",
              "jovens_por_ano": "F4", "anos": "F4", "fracao_formada": "F4",
              "perdas": "F5", "consumo_basico": "F5",
              "horas_pratica": "F8", "horas_primeira": "F8", "taxa_aprendizagem": "F8"}
OUTRO_FICHEIRO = ("konfirmu_calc.py de outra IA, recebido a 20-11-2026 04:03, "
                  "sha256 ed9e6e23d524249a21fecda235520dceffecf4cb031a98e74c44ffb7457e6991")
FORMULAS_B: Dict[str, Dict[str, Any]] = {
    "F2": {"id": "F2", "versao": "B-1.0.0", "nome": "produção do enxame",
           "formula": "producao = capacidade × taxa_utilizacao",
           "unidades": {"capacidade": "ficha/dia", "taxa_utilizacao": "1", "saida": "ficha/dia"},
           "etiqueta": "ASSUMIDO", "fonte": OUTRO_FICHEIRO + "; diz: «parâmetros declarados (enxame permanente, 19-11-2026)»",
           "o_que_nao_garante": "a capacidade é um parâmetro declarado; a produção real mede-se no piloto"},
    "F4": {"id": "F4", "versao": "B-1.0.0", "nome": "dividendo demográfico",
           "formula": "pib_per_capita = base × (1 + dividendo × cobertura_educacao)",
           "unidades": {"base": "1", "dividendo": "1", "cobertura_educacao": "1", "saida": "1"},
           "etiqueta": "ASSUMIDO", "fonte": OUTRO_FICHEIRO + "; diz: «F4 do plano O Peso da Pedra (19-11-2026)»",
           "o_que_nao_garante": "dividendo e cobertura são assunções; o efeito real mede-se com o piloto"},
    "F5": {"id": "F5", "versao": "B-1.0.0", "nome": "alcance das caixas",
           "formula": "alcance = caixas × pessoas_por_comunidade × uptime",
           "unidades": {"caixas": "caixa", "pessoas_por_comunidade": "pessoa/caixa", "uptime": "1", "saida": "pessoa"},
           "etiqueta": "ASSUMIDO", "fonte": OUTRO_FICHEIRO + "; diz: «plano da Box (19-11-2026)»",
           "o_que_nao_garante": "todos os parâmetros são assunções até haver medição no terreno"},
    "F8": {"id": "F8", "versao": "B-1.0.0", "nome": "aprendizagem (retenção)",
           "formula": "retencao = exp(−intervalo / estabilidade)",
           "unidades": {"intervalo": "dia", "estabilidade": "dia", "saida": "1"},
           "etiqueta": "ASSUMIDO", "fonte": OUTRO_FICHEIRO + "; diz: «FSRS (revisão open source), inspiração declarada»",
           "o_que_nao_garante": "modelo simplificado; o FSRS completo usa 17 parâmetros calibrados"},
}
ENTRADAS_B: Dict[str, Dict[str, Any]] = {  # os inputs do outro ficheiro, tal e qual (ele não lhes dá incerteza)
    "capacidade": {"valor": 3000.0, "unidade": "ficha/dia", "etiqueta": "ASSUMIDO"},
    "taxa_utilizacao": {"valor": 0.6, "unidade": "1", "etiqueta": "ASSUMIDO"},
    "base": {"valor": 1.0, "unidade": "1", "etiqueta": "MEDIDO"},  # [VALIDAR] é ele que lhe chama MEDIDO
    "dividendo": {"valor": 0.02, "unidade": "1", "etiqueta": "ASSUMIDO"},
    "cobertura_educacao": {"valor": 0.4, "unidade": "1", "etiqueta": "ASSUMIDO"},
    "caixas": {"valor": 1000.0, "unidade": "caixa", "etiqueta": "ASSUMIDO"},
    "pessoas_por_comunidade": {"valor": 300.0, "unidade": "pessoa/caixa", "etiqueta": "ASSUMIDO"},
    "uptime": {"valor": 0.9, "unidade": "1", "etiqueta": "ASSUMIDO"},
    "intervalo": {"valor": 30.0, "unidade": "dia", "etiqueta": "MEDIDO"},
    "estabilidade": {"valor": 60.0, "unidade": "dia", "etiqueta": "ASSUMIDO"},
}
G_STC = G(1000.0, 0.0, "W/m2", fonte="G_stc")
UMA_MICRORREDE_POR_PESSOA = G(1.0, 0.0, "microrrede/pessoa", fonte="unidade")


def _confere(fid: str, **entradas: Grandeza) -> None:
    """Cada input tem de vir na dimensão declarada no cofre. Unidade errada = TypeError."""
    for nome, g in entradas.items():
        try:
            g.em(FORMULAS[fid]["unidades"][nome])
        except TypeError as e:
            raise TypeError(f"{fid}.{nome}: {e}") from None


def F2(paineis: Grandeza, area: Grandeza, rendimento: Grandeza, pr: Grandeza, sol_pico: Grandeza,
       prova_laboratorial: Any = False, laboratorios: Optional[Dict[str, str]] = None) -> Grandeza:
    _confere("F2", paineis=paineis, area=area, rendimento=rendimento, pr=pr, sol_pico=sol_pico)
    veto_fisico(rendimento, FORMULAS["F2"]["teto_de_rendimento"], prova_laboratorial, laboratorios)
    return paineis * area * G_STC * rendimento * pr * sol_pico


def F4(jovens_por_ano: Grandeza, anos: Grandeza, fracao_formada: Grandeza) -> Grandeza:
    _confere("F4", jovens_por_ano=jovens_por_ano, anos=anos, fracao_formada=fracao_formada)
    return jovens_por_ano * anos * fracao_formada


def F5(perdas: Grandeza, consumo_basico: Grandeza) -> Grandeza:
    _confere("F5", perdas=perdas, consumo_basico=consumo_basico)
    return (1.0 - perdas) / consumo_basico


def F8(horas_pratica: Grandeza, horas_primeira: Grandeza, taxa_aprendizagem: Grandeza) -> Grandeza:
    _confere("F8", horas_pratica=horas_pratica, horas_primeira=horas_primeira, taxa_aprendizagem=taxa_aprendizagem)
    if not 0.0 < taxa_aprendizagem.v < 1.0:
        raise ValueError("a taxa de aprendizagem tem de estar entre 0 e 1")
    um_menos_b = 1.0 + g_ln(1.0 - taxa_aprendizagem) / ln(2.0)
    x = um_menos_b * horas_pratica / horas_primeira
    return g_exp(g_ln(x) / um_menos_b) * UMA_MICRORREDE_POR_PESSOA


def calcular_cenario(entradas: Dict[str, Dict[str, Any]]) -> Tuple[Grandeza, Dict[str, Grandeza]]:
    g = {k: G(e["valor"], e.get("incerteza", 0.0), e["unidade"], fonte=("entrada", k)) for k, e in sorted(entradas.items())}
    f = {"F2": F2(g["paineis"], g["area"], g["rendimento"], g["pr"], g["sol_pico"]),
         "F4": F4(g["jovens_por_ano"], g["anos"], g["fracao_formada"]),
         "F5": F5(g["perdas"], g["consumo_basico"]),
         "F8": F8(g["horas_pratica"], g["horas_primeira"], g["taxa_aprendizagem"])}
    return f["F2"] * f["F4"] * f["F5"] * f["F8"], f


def calcular_variante_b(entradas: Dict[str, Dict[str, Any]]) -> Dict[str, Grandeza]:
    """As 4 fórmulas do outro ficheiro, pelo motor de unidades. Unidade errada = TypeError."""
    g = {k: G(e["valor"], 0.0, e["unidade"], fonte=("entrada_b", k)) for k, e in sorted(entradas.items())}
    for f in FORMULAS_B.values():
        for nome, unidade in f["unidades"].items():
            if nome != "saida":
                g[nome].em(unidade)
    return {"F2": g["capacidade"] * g["taxa_utilizacao"],
            "F4": g["base"] * (1.0 + g["dividendo"] * g["cobertura_educacao"]),
            "F5": g["caixas"] * g["pessoas_por_comunidade"] * g["uptime"],
            "F8": g_exp(-1.0 * (g["intervalo"] / g["estabilidade"]))}


def pacote_cenario(nome: str, entradas: Dict[str, Dict[str, Any]], livro: LedgerImutavel, dia: int) -> Dict[str, Any]:
    """P7 + P10: o pacote tem hash próprio, que só depende dos inputs e das fórmulas."""
    y, f = calcular_cenario(entradas)
    v, u = y.em("pessoa")  # o motor de unidades confere: o produto tem de dar pessoas
    usadas = {k: FORMULAS[k] for k in ("F2", "F4", "F5", "F8")}
    nucleo = {"cenario": nome, "carimbo": CARIMBO, "entradas": entradas,
              "formulas": {k: {"versao": x["versao"], "hash": hobj(x)} for k, x in usadas.items()},
              "fatores": {k: dict(zip(("valor", "incerteza"), f[k].em(FORMULAS[k]["unidades"]["saida"])),
                                  unidade=FORMULAS[k]["unidades"]["saida"]) for k in usadas},
              "resultado": {"valor": v, "incerteza": u, "unidade": "pessoa", "nota": "1 sigma, propagação linear"}}
    hp = hobj(nucleo)
    livro.registar(dia, "CENARIO", {"cenario": nome, "hash_pacote": hp})
    return {"pacote": nucleo, "hash_pacote": hp,
            "linhagem": {"hash_input": hobj(entradas), "hash_formula": hobj(usadas), "hash_estado_ledger": livro.cabeca()},
            "ledger": {"blocos": len(livro.blocos), "integra": livro.verificar_integridade_cadeia()}}


def gargalo(entradas: Dict[str, Dict[str, Any]], alvo: float) -> Dict[str, Any]:
    """B1 (P11 na v1.0): elasticidade (dY/dX · X/Y) e salto do resultado por +1% de esforço em cada alavanca; a maior é o gargalo.
    Depois calcula o ajuste que leva ao alvo, alavanca a alavanca, sem passar o limite físico declarado."""
    def y(ent: Dict[str, Dict[str, Any]]) -> float:
        return calcular_cenario(ent)[0].em("pessoa")[0]

    def com(ent: Dict[str, Dict[str, Any]], k: str, v: float) -> Dict[str, Dict[str, Any]]:
        novo = {a: dict(b) for a, b in ent.items()}
        novo[k]["valor"] = v
        return novo

    base = y(entradas)
    saltos = {k: (y(com(entradas, k, e["valor"] * (1.0 + 0.01 * e["esforco"]))) / base - 1.0) * 100.0
              for k, e in sorted(entradas.items()) if e.get("esforco")}
    ordem = sorted(saltos, key=lambda k: (-saltos[k], k))
    # elasticidade = dY/dX · X/Y, por diferença central de ±0,1% em cada alavanca
    elasticidades = {k: (y(com(entradas, k, entradas[k]["valor"] * 1.001)) - y(com(entradas, k, entradas[k]["valor"] * 0.999)))
                     / (0.002 * base) for k in ordem}
    atual, plano = entradas, []
    for k in ordem:
        if y(atual) >= alvo:
            break
        v0, lim = atual[k]["valor"], atual[k]["limite"]
        if y(com(atual, k, lim)) < alvo:  # nem no limite físico chega: fica no limite e passa à alavanca seguinte
            atual = com(atual, k, lim)
            plano.append({"alavanca": k, "de": v0, "para": lim, "chega": False})
            continue
        a, b = v0, lim
        for _ in range(100):
            m = (a + b) / 2.0
            if y(com(atual, k, m)) < alvo:
                a = m
            else:
                b = m
        atual = com(atual, k, b)
        plano.append({"alavanca": k, "de": v0, "para": b, "chega": True})
    return {"base": base, "alvo": alvo, "saltos_por_1pct": saltos, "elasticidades": elasticidades, "ordem": ordem, "gargalo": ordem[0],
            "formula_do_gargalo": ENTRADA_DE[ordem[0]], "plano": plano, "final": y(atual)}


# -----------------------------------------------------------------------------
# 11. P5 + P6 + P8 + P10 + B3 — O MOTOR: COFRE, ESCROW, ESTADOS, HOMEOSTASE, FUNDO
# -----------------------------------------------------------------------------
HASH_REGRAS = hobj(REGRAS)  # as regras de nascença: a versão 0 da constituição (P21)


def hash_regras() -> str:
    """P10 + P21: o hash das regras EM VIGOR neste instante. Só muda quando uma emenda é ratificada."""
    return hobj(REGRAS)

# P6: CONGELADO_15D -> {CORRIGIDO | TRIBUNAL | EXPIRACAO_ESTORNO_ORIGEM}. Nada fora desta tabela acontece.
# [VALIDAR] O nome do estado traz o prazo (15D); se REGRAS['prazo_dias'] mudar, muda-se o nome.
# [VALIDAR] Só o estado CONGELADO_15D tem prazo; ATIVO e CORRIGIDO esperam pela prova sem data-limite.
TRANSICOES: Dict[str, Sequence[str]] = {
    "ATIVO": ("LIBERTADO", "CONGELADO_15D"),
    "CONGELADO_15D": ("CORRIGIDO", "TRIBUNAL", "EXPIRACAO_ESTORNO_ORIGEM"),
    "CORRIGIDO": ("LIBERTADO", "CONGELADO_15D"),
    "LIBERTADO": (), "TRIBUNAL": (), "EXPIRACAO_ESTORNO_ORIGEM": (),
}


class Motor:
    """Dinheiro em cêntimos inteiros. Contas: reserva (cofre de origem), custódia por escrow, fundo de reparação, pago."""

    def __init__(self, reserva: int, pub_cofre: str, custodios: Dict[str, str], fontes: Dict[str, Dict[str, str]],
                 aldeia: Aldeia, juizes: Dict[str, str], valvula: Valvula, sk_motor: bytes, livro: LedgerImutavel) -> None:
        self.total0 = self.reserva = int(reserva)
        self.fundo = self.divida_do_fundo = self.n_sessoes = 0
        self.custodia: Dict[str, int] = {}
        self.pago: Dict[str, int] = {}
        self.pub_cofre, self.custodios, self.fontes = pub_cofre, custodios, fontes
        self.aldeia, self.juizes, self.valvula, self.sk_motor, self.livro = aldeia, juizes, valvula, sk_motor, livro
        self.escrows: Dict[str, Dict[str, Any]] = {}
        self.sessoes: Dict[str, Dict[str, Any]] = {}
        self.anomalia = REGRAS["homeostase"]["base"]
        self.respostas: List[Dict[str, Any]] = []
        self.constituicao: Any = None  # P21: quando está ligada, o motor só trabalha com as regras ratificadas
        if not irmandade_ok(custodios, REGRAS["shamir"]["k"]):  # v2.4: a irmandade é mecanismo, não discurso
            raise ValueError("motor recusado: os custódios têm de incluir as 3 câmaras africanas e os restantes não podem chegar ao limiar sozinhos")

    # --- P10: toda a resposta leva hash do input + hash das regras + hash do estado; P4: e a ledger conferida
    def _resp(self, estado: str, entrada: str, dia: int, **extra: Any) -> Dict[str, Any]:
        self.livro.registar(dia, estado, dict(extra, entrada=entrada))
        r = dict(extra, estado=estado,
                 linhagem={"hash_input": entrada, "hash_formula": hash_regras(), "hash_estado_ledger": self.livro.cabeca()},
                 ledger={"blocos": len(self.livro.blocos), "integra": self.livro.verificar_integridade_cadeia()})
        self.respostas.append(r)
        self.livro.respostas.append(r)
        return r

    # --- P21: regras mexidas por fora (sem emenda) = o motor pára, e os dois hashes ficam na ledger
    def _traicao(self, entrada: str, dia: int, eid: str) -> Optional[Dict[str, Any]]:
        c = self.constituicao
        if c is None or c.fiel():
            return None
        return self._resp("BLOQUEADO_REGRAS_FORA_DA_CONSTITUICAO", entrada, dia, escrow=eid, regras_da_constituicao=c.atual()["hash_regras"])

    # --- P8: homeostase por eventos (inspirada em Lotka-Volterra: o ataque alimenta a anomalia, o lastro cura-a)
    def nivel(self) -> Tuple[str, int, int]:
        h = REGRAS["homeostase"]
        nome = "DEFESA" if self.anomalia >= h["defesa"] else "ALERTA" if self.anomalia >= h["alerta"] else "FLUIDO"
        assinaturas, quarentena = REGRAS["niveis"][nome]
        return nome, assinaturas, quarentena

    def _ataque(self) -> None:
        h = REGRAS["homeostase"]
        self.anomalia = min(1000, self.anomalia * h["ataque_num"] // h["ataque_den"])

    def _lastro(self) -> None:
        h = REGRAS["homeostase"]
        self.anomalia = max(h["base"], self.anomalia - h["cura"])

    def _desfaz_ataque(self) -> None:
        h = REGRAS["homeostase"]
        self.anomalia = max(h["base"], self.anomalia * h["ataque_den"] // h["ataque_num"])

    # --- P6: só as transições da tabela
    def _mudar(self, e: Dict[str, Any], novo: str) -> None:
        if novo not in TRANSICOES[e["estado"]]:
            raise RuntimeError(f"transição proibida: {e['estado']} -> {novo}")
        e["estado"] = novo

    def conserva(self) -> bool:
        return self.reserva + self.fundo + sum(self.custodia.values()) + sum(self.pago.values()) == self.total0

    def hash_pedido(self, eid: str) -> str:
        e = self.escrows[eid]
        return hobj({"escrow": eid, "destino": e["destino"], "valor": e["valor"]})

    def criar_escrow(self, eid: str, destino: str, valor: int, dia: int, minimo: float, unidade: str,
                     dominio: str = "INFRAESTRUTURA") -> Dict[str, Any]:
        entrada = hobj({"criar": eid, "destino": destino, "valor": valor, "dia": dia, "minimo": minimo,
                        "unidade": unidade, "dominio": dominio})
        traicao = self._traicao(entrada, dia, eid)
        if traicao is not None:
            return traicao
        para_o_fundo = valor * REGRAS["fundo_reparacao_pct"] // 100  # [VALIDAR] a percentagem sai do cofre de origem, não do trabalhador
        if eid in self.escrows:
            return self._resp("RECUSADO_ESCROW_JA_EXISTE", entrada, dia, escrow=eid)
        if valor <= 0 or valor + para_o_fundo > self.reserva:  # a reserva nunca fica negativa
            return self._resp("BLOQUEADO_RESERVA_INSUFICIENTE", entrada, dia, escrow=eid, reserva=self.reserva)
        self.reserva -= valor + para_o_fundo
        self.fundo += para_o_fundo
        self.custodia[eid] = valor
        self.escrows[eid] = {"id": eid, "destino": destino, "valor": valor, "estado": "ATIVO", "criado": dia,
                             "minimo": minimo, "unidade": unidade, "dominio": dominio}
        return self._resp("ESCROW_CRIADO", entrada, dia, escrow=eid, valor_centimos=valor, fundo_centimos=para_o_fundo)

    def abrir_sessao(self, eid: str, dia: int) -> str:
        """P5: cada pedido tem uma sessão de uso único, como num banco."""
        self.n_sessoes += 1
        hp = self.hash_pedido(eid)
        sid = hobj({"pedido": hp, "n": self.n_sessoes})[:32]
        self.sessoes[sid] = {"pedido": hp, "dia": dia, "usada": False}
        self.livro.registar(dia, "SESSAO_ABERTA", {"escrow": eid, "sessao": sid})
        return sid

    def _chave_do_cofre(self, bons: Sequence[str], assinaturas: Dict[str, Dict]) -> Optional[bytes]:
        """P5: junta 3 partes de Shamir e confere contra a chave pública registada do cofre.
        A chave fica inteira em memória neste ponto: não é MPC (ver O_QUE_NAO_GARANTE)."""
        for trio in itertools.combinations(bons, REGRAS["shamir"]["k"]):
            try:
                sk = shamir_juntar([tuple(assinaturas[n]["parte"]) for n in trio]).to_bytes(32, "big")
            except (OverflowError, KeyError, TypeError, ValueError):
                continue
            if ed_publica(sk).hex() == self.pub_cofre:
                return sk
        return None

    def liquidar(self, eid: str, sid: str, dia: int, leituras: Sequence[Dict] = (), preco: Optional[Dict] = None,
                 votos: Sequence[Dict] = (), assinaturas: Optional[Dict[str, Dict]] = None,
                 emergencia: Optional[Dict] = None) -> Dict[str, Any]:
        e, hp, assinaturas = self.escrows[eid], self.hash_pedido(eid), assinaturas or {}
        entrada = hobj({"escrow": eid, "sessao": sid, "dia": dia,
                        "leituras": [l.get("selo", {}).get("hash") for l in leituras],
                        "preco": None if not preco else {"custo": preco["custo"], "propostas": list(preco["propostas"]),
                                                         "historico": preco["historico"].get("selo", {}).get("hash")},
                        "votos": [v.get("selo", {}).get("hash") for v in votos],
                        "assinantes": sorted(assinaturas), "emergencia": bool(emergencia)})

        def r(estado: str, **x: Any) -> Dict[str, Any]:
            return self._resp(estado, entrada, dia, escrow=eid, **x)

        traicao = self._traicao(entrada, dia, eid)
        if traicao is not None:
            return traicao
        s = self.sessoes.get(sid)
        if s is None or s["pedido"] != hp:
            return r("RECUSADO_SESSAO_DESCONHECIDA")
        if s["usada"]:
            return r("RECUSADO_SESSAO_JA_USADA")
        if e["estado"] not in ("ATIVO", "CORRIGIDO"):
            return r("RECUSADO_ESTADO_" + e["estado"])
        nivel, exigidas, quarentena = self.nivel()
        if emergencia:  # a válvula vital não espera, mas a custódia 3-de-5 mantém-se
            exigidas, quarentena = REGRAS["shamir"]["k"], 0
        if dia < s["dia"] + quarentena:
            return r("EM_QUARENTENA", nivel=nivel, ate_ao_dia=s["dia"] + quarentena)  # a sessão continua válida
        s["usada"] = True  # daqui em diante a sessão gasta-se, corra bem ou mal
        bons = sorted(n for n, a in assinaturas.items() if n in self.custodios
                      and selo_ok({"sessao": sid, "pedido": hp}, a.get("selo", {}), {self.custodios[n]}))

        def pagar(estado: str, extra: Dict[str, Any]) -> Dict[str, Any]:
            if len(bons) < exigidas:
                return r("BLOQUEADO_ASSINATURAS_INSUFICIENTES", validas=len(bons), exigidas=exigidas, nivel=nivel)
            sk = self._chave_do_cofre(bons, assinaturas)
            if sk is None:
                return r("BLOQUEADO_CHAVE_DO_COFRE_NAO_RECONSTRUIDA", validas=len(bons))
            valor = self.custodia.pop(eid)
            self.pago[e["destino"]] = self.pago.get(e["destino"], 0) + valor
            self._mudar(e, "LIBERTADO")
            self._lastro()
            dossie = dict(extra, escrow=eid, destino=e["destino"], valor_centimos=valor, dia=dia, assinantes=bons)
            e["dossie"] = {"dados": dossie, "selo": selar(dossie, sk)}  # selado com a chave do cofre reconstruída
            return r(estado, valor_centimos=valor, dossie=e["dossie"]["selo"]["hash"], assinantes=bons, nivel=nivel)

        if emergencia:  # B3
            if len(bons) < exigidas:
                return r("BLOQUEADO_ASSINATURAS_INSUFICIENTES", validas=len(bons), exigidas=exigidas, nivel=nivel)
            ok, motivo = self.valvula.acionar(e["dominio"], hp, emergencia.get("quem"), emergencia.get("selo", {}), dia)
            if not ok:
                return r("RECUSADO_VALVULA_" + motivo)
            return pagar("LIBERTADA_POR_VALVULA_VITAL_REVISAO_POSTERIOR",
                         {"valvula": {"quem": emergencia["quem"], "dominio": e["dominio"]}, "revisao_humana_posterior": True})

        motivos: List[str] = []  # punitivos: só com base forte
        fracos: List[str] = []   # dados fracos: nem pune nem paga (P12)
        faltas: List[str] = []   # falta confirmar: espera
        evid: Dict[str, Any] = {}
        # lastro físico, por oráculo triangulado; quem recebe o dinheiro não conta como fonte
        o = oraculo(leituras, self.fontes, e["unidade"], eid, excluir_operador=e["destino"], janela=(e["criado"], dia))
        evid["oraculo"] = {k: o.get(k) for k in ("estado", "valor", "incerteza", "confianca", "discrepantes", "rejeitadas")}
        if o["estado"] == "INSUFICIENTE":
            faltas.append("ORACULO_INSUFICIENTE")
        elif o["confianca"] < REGRAS["confianca_min"]:
            fracos.append("ORACULO_CONFIANCA_BAIXA")
        else:
            k95 = REGRAS["k95_unilateral"]
            if o["valor"] + k95 * o["incerteza"] < e["minimo"]:
                motivos.append("SEM_LASTRO_FISICO")
            elif o["valor"] - k95 * o["incerteza"] < e["minimo"]:
                fracos.append("LASTRO_INCONCLUSIVO")
        # preço: banda selada pela aferidora + sinal de cartel (B2)
        if preco:
            hist = preco["historico"]
            af = self.fontes.get(hist.get("dados", {}).get("fonte"), {})
            if not selo_ok(hist.get("dados"), hist.get("selo", {}), {af.get("pub")}):
                fracos.append("HISTORICO_DE_PRECOS_SEM_SELO")
            else:
                b = banda_preco(hist["dados"]["precos"])
                if b is None:
                    fracos.append("BANDA_FRACA")
                else:
                    c = sinal_de_cartel(preco["propostas"], b)
                    evid["banda"], evid["cartel"] = b, c
                    if not b["piso"] <= preco["custo"] <= b["teto"]:
                        motivos.append("PRECO_FORA_DA_BANDA")
                    if c["sinal"]:
                        motivos.append("CARTEL_NO_TETO")
        # cidadãos: 5 a confirmar libertam; 5 a acusar congelam (P9)
        q = self.aldeia.contar(votos, eid, dia, desde=e["criado"])
        evid["quorum"] = q
        if q["desconformes"] >= REGRAS["quorum_k"]:
            motivos.append("ALERTA_CIDADAO_K5")
        elif q["conformes"] < REGRAS["quorum_k"]:
            faltas.append("AGUARDA_QUORUM_K5")

        if motivos:  # a máquina congela e sela o dossiê; o humano julga
            self._mudar(e, "CONGELADO_15D")
            e["congelado_em"], e["prazo"] = dia, dia + REGRAS["prazo_dias"]
            self._ataque()
            dossie = {"escrow": eid, "motivos": motivos, "evidencias": evid, "congelado_no_dia": dia,
                      "prazo_dia": e["prazo"], "nota": "pagamento suspenso; a decisão é humana"}
            e["dossie"] = {"dados": dossie, "selo": selar(dossie, self.sk_motor)}
            return r("CONGELADO_15D", motivos=motivos, prazo_dia=e["prazo"], dossie=e["dossie"]["selo"]["hash"])
        if fracos:
            return r("REVISAO_HUMANA_SEM_PUNIR_NEM_PAGAR", motivos=fracos)
        if faltas:
            return r("AGUARDA", faltas=faltas)
        return pagar("LIBERTADA", {"evidencias": evid})

    def congelar_por_veto(self, eid: str, motivo: str, evidencia: Dict[str, Any], dia: int) -> Dict[str, Any]:
        """P19 + P20: um veto de fora (biofísico, lote anómalo) congela um escrow vivo. Não julga ninguém:
        abre os 15 dias para a decisão humana (P6), com o dossiê selado."""
        e = self.escrows[eid]
        entrada = hobj({"congelar": eid, "motivo": motivo, "evidencia": evidencia, "dia": dia})
        traicao = self._traicao(entrada, dia, eid)
        if traicao is not None:
            return traicao
        if e["estado"] not in ("ATIVO", "CORRIGIDO"):
            return self._resp("RECUSADO_ESTADO_" + e["estado"], entrada, dia, escrow=eid)
        self._mudar(e, "CONGELADO_15D")
        e["congelado_em"], e["prazo"] = dia, dia + REGRAS["prazo_dias"]
        self._ataque()
        dossie = {"escrow": eid, "motivos": [motivo], "evidencias": evidencia, "congelado_no_dia": dia, "prazo_dia": e["prazo"],
                  "nota": "pagamento suspenso; a decisão é humana. " + FRASES_OBRIGATORIAS["deteccao"]}
        e["dossie"] = {"dados": dossie, "selo": selar(dossie, self.sk_motor)}
        return self._resp("CONGELADO_15D", entrada, dia, escrow=eid, motivos=[motivo], prazo_dia=e["prazo"], dossie=e["dossie"]["selo"]["hash"])

    def avancar(self, dia: int) -> List[Dict[str, Any]]:
        """P6: 15 dias sem julgamento humano -> o dinheiro volta ao cofre de origem, com registo."""
        saida = []
        for eid in sorted(self.escrows):
            e = self.escrows[eid]
            if e["estado"] == "CONGELADO_15D" and dia >= e["prazo"]:
                self._mudar(e, "EXPIRACAO_ESTORNO_ORIGEM")
                valor = self.custodia.pop(eid)
                self.reserva += valor
                saida.append(self._resp("EXPIRACAO_ESTORNO_ORIGEM", hobj({"avancar": dia, "escrow": eid}), dia,
                                        escrow=eid, valor_centimos=valor, dossie=e["dossie"]["selo"]["hash"]))
        return saida

    def julgar(self, eid: str, decisao: str, juiz: str, selo: Dict, dia: int, falso_positivo: bool = False) -> Dict[str, Any]:
        e = self.escrows[eid]
        dados = {"escrow": eid, "decisao": decisao, "falso_positivo": falso_positivo, "dia": dia}
        entrada = hobj(dict(dados, juiz=juiz))

        def r(estado: str, **x: Any) -> Dict[str, Any]:
            return self._resp(estado, entrada, dia, escrow=eid, **x)

        traicao = self._traicao(entrada, dia, eid)
        if traicao is not None:
            return traicao
        if e["estado"] != "CONGELADO_15D":
            return r("RECUSADO_ESTADO_" + e["estado"])
        if dia >= e["prazo"]:
            return r("RECUSADO_PRAZO_EXPIRADO")
        if decisao not in ("CORRIGIDO", "TRIBUNAL"):
            return r("RECUSADO_DECISAO_INVALIDA")
        if juiz not in self.juizes or not selo_ok(dados, selo, {self.juizes[juiz]}):
            return r("RECUSADO_ASSINATURA_DO_JUIZ")
        self._mudar(e, decisao)
        if decisao == "TRIBUNAL":  # [VALIDAR] enquanto o tribunal decide, o dinheiro fica no cofre de origem
            valor = self.custodia.pop(eid)
            self.reserva += valor
            return r("TRIBUNAL", juiz=juiz, valor_centimos=valor, dossie=e["dossie"]["selo"]["hash"])
        extra: Dict[str, Any] = {"juiz": juiz, "falso_positivo": falso_positivo}
        if falso_positivo:  # B3: o erro do sistema paga-o o fundo, não o trabalhador
            dias = dia - e["congelado_em"]
            devido = e["valor"] * REGRAS["indemnizacao_por_mil_ao_dia"] * dias // 1000
            pago = min(devido, self.fundo)
            self.fundo -= pago
            self.divida_do_fundo += devido - pago  # se o fundo não chegar, a dívida fica escrita
            self.pago[e["destino"]] = self.pago.get(e["destino"], 0) + pago
            self._desfaz_ataque()
            extra.update(dias_parado=dias, indemnizacao_centimos=pago, em_divida_centimos=devido - pago)
        return r("CORRIGIDO", **extra)


# -----------------------------------------------------------------------------
# 12. P10 + P7 + P25 — RESPOSTA COM LINHAGEM, COFRE ÚNICO E CANÁRIOS
# -----------------------------------------------------------------------------
_HEX64 = re.compile(r"[0-9a-f]{64}")


def chave_demo(nome: str) -> bytes:
    """Chaves de DEMO: saem da semente declarada e de etiquetas públicas. NÃO são segredo."""
    if _PRODUCAO[0]:
        raise ChaveDeDemoRecusada(f"chave de demo «{nome}» recusada em modo de produção")
    return hashlib.sha256(f"KONFIRMU-CALC-DEMO/{SEED}/{nome}".encode()).digest()


def _h(o: Any) -> str:
    """Um hash de 64 hexadecimais passa tal e qual; tudo o resto fica reduzido ao hash do seu JSON canónico."""
    if isinstance(o, str) and _HEX64.fullmatch(o):
        return o
    try:
        return hobj(o)
    except (TypeError, ValueError):  # lixo que não cabe em JSON também fica com um hash: nada rebenta por causa dele
        return h256(repr(o).encode("utf-8"))


def responder(livro: LedgerImutavel, dia: int, estado: str, entrada: Any, formula: Any, **extra: Any) -> Dict[str, Any]:
    """P10: toda a saída leva hash do input + hash da fórmula (ou das regras) + hash do estado da ledger."""
    hi, hf = _h(entrada), _h(formula)
    livro.registar(dia, estado, dict(extra, entrada=hi, formula=hf))
    r = dict(extra, estado=estado,
             linhagem={"hash_input": hi, "hash_formula": hf, "hash_estado_ledger": livro.cabeca()},
             ledger={"blocos": len(livro.blocos), "integra": livro.verificar_integridade_cadeia()})
    livro.respostas.append(r)
    return r


def faixa95(g: Grandeza, unidade: str) -> Tuple[float, float]:
    """Os dois limites a 95% (valor ∓ 1,645·u), na unidade pedida."""
    v, u = g.em(unidade)
    k = REGRAS["k95_unilateral"]
    return v - k * u, v + k * u


# P25 — canários: fórmulas-isca. Nenhuma conta as usa. O hash de cada uma está pregado no código, à mão:
# quem lhes mexer, ou as citar num pacote, faz disparar o alarme. [VALIDAR] os valores-armadilha são escolha.
CANARIOS: Dict[str, Dict[str, Any]] = {
    "F0.K1": {"id": "F0.K1", "versao": "1.0.0", "nome": "canário 1 (isca)", "formula": "k1 = 0,7316 · E",
              "unidades": {"E": "kWh", "saida": "kWh"}, "etiqueta": "ASSUMIDO",
              "fonte": "isca declarada: nenhuma conta do motor usa esta fórmula",
              "o_que_nao_garante": "nada: é armadilha. Quem lhe mexe, ou a usa num pacote, denuncia-se."},
    "F0.K2": {"id": "F0.K2", "versao": "1.0.0", "nome": "canário 2 (isca)", "formula": "k2 = 41 · N + 7",
              "unidades": {"N": "pessoa", "saida": "pessoa"}, "etiqueta": "ASSUMIDO",
              "fonte": "isca declarada: nenhuma conta do motor usa esta fórmula",
              "o_que_nao_garante": "nada: é armadilha. Quem lhe mexe, ou a usa num pacote, denuncia-se."},
}
CANARIOS_SELADOS: Dict[str, str] = {
    "F0.K1": "48271e2541a02dee72fb2cf8bd35285e04aed3fa671c035e7e81f94c4a47563b",
    "F0.K2": "3a75365438e1f11829843cb7f74f521eb3b3945b287f45a5d8abd1911e14ed8e",
}


def auditar_canarios(canarios: Optional[Dict[str, Dict[str, Any]]] = None, livro: Optional[LedgerImutavel] = None,
                     dia: int = 0) -> List[Dict[str, str]]:
    """P25: compara cada canário com o hash pregado no código. Qualquer diferença = alarme com os dois hashes.
    Corre antes de emitir ou consumir pacotes, de ratificar emendas e de fazer forks (auditoria contínua)."""
    canarios = CANARIOS if canarios is None else canarios
    alarmes = []
    for fid in sorted(CANARIOS_SELADOS):
        achado = hobj(canarios[fid]) if fid in canarios else "(desapareceu)"
        if achado != CANARIOS_SELADOS[fid]:
            alarmes.append({"alarme": "ALARME_CANARIO", "canario": fid, "hash_esperado": CANARIOS_SELADOS[fid], "hash_encontrado": achado})
    if livro is not None:
        for a in alarmes:
            livro.registar(dia, "ALARME_CANARIO", a)
    return alarmes


def cofre() -> Dict[str, Dict[str, Any]]:
    """P7: o cofre inteiro numa só vista — fórmulas (variantes A e B), ponto neutral, prevenção, teorias em debate,
    normas médicas, oráculos gravados, domínios da v2.3 e canários. Cada ficha: id, versão, fórmula, unidades, etiqueta, fonte, o_que_nao_garante."""
    c: Dict[str, Dict[str, Any]] = {k + "@A": f for k, f in FORMULAS.items()}
    c.update({k + "@B": f for k, f in FORMULAS_B.items()})
    for grupo in (FORMULAS_15, FARMACOPEIA, INTERACOES, {"frio": CADEIA_DE_FRIO}, ORACULOS_GRAVADOS, FORMULAS_23, FORMULAS_24, FORMULAS_25, CANARIOS):
        c.update({f["id"]: f for f in grupo.values()})
    for d in DEBATES.values():
        c.update({t["id"]: t for t in d["teorias"]})
    return c


def hash_cofre() -> str:
    return hobj(cofre())


# -----------------------------------------------------------------------------
# 13. P11 — VOTO ANÓNIMO: ASSINATURA DE ANEL LIGÁVEL (LSAG) SOBRE Ed25519
# -----------------------------------------------------------------------------
# Liu, Wei e Wong (2004), na forma que o Monero tornou conhecida: quem assina prova que é UM dos donos das chaves
# do anel, sem dizer qual. A «imagem» I = x·H (x = chave privada; H = ponto derivado da votação e do anel) sai igual
# sempre que a mesma pessoa vota na mesma votação: apanha o voto duplo sem revelar quem votou.
# [VALIDAR] H sai de hash-para-ponto por tentativa e incremento, multiplicado pelo cofator 8 (cai no subgrupo de
# ordem prima). Não é o mapa do Monero nem o do RFC 9380, não corre em tempo constante e não foi auditado.
_ED_ID: Ponto = (0, 1, 1, 0)
_LSAG_ALG = "LSAG-Ed25519-SHA512/1"
_PONTOS_DO_ANEL: Dict[bytes, Optional[Ponto]] = {}
_BASES_LSAG: Dict[bytes, Ponto] = {}


def _ed_mult2(a: int, p: Ponto, b: int, q: Ponto) -> Ponto:
    """a·p + b·q numa só passagem (truque de Straus-Shamir)."""
    pq, r = _ed_soma(p, q), _ED_ID
    for i in range(max(a.bit_length(), b.bit_length()) - 1, -1, -1):
        r = _ed_soma(r, r)
        ba, bb = (a >> i) & 1, (b >> i) & 1
        if ba and bb:
            r = _ed_soma(r, pq)
        elif ba:
            r = _ed_soma(r, p)
        elif bb:
            r = _ed_soma(r, q)
    return r


def _ed_primo(p: Ponto) -> bool:
    """O ponto está no subgrupo de ordem prima L e não é o neutro? (fecha a porta aos pontos de ordem pequena)"""
    return not _ed_igual(p, _ED_ID) and _ed_igual(_ed_mult(_L, p), _ED_ID)


def _ponto_do_anel(pk: bytes) -> Optional[Ponto]:
    if pk not in _PONTOS_DO_ANEL:
        p = _ed_descomp(pk)
        _PONTOS_DO_ANEL[pk] = p if p is not None and _ed_primo(p) else None
    return _PONTOS_DO_ANEL[pk]


def _hs(*partes: bytes) -> int:
    """hash -> escalar; cada parte entra com o seu comprimento (a concatenação não fica ambígua)."""
    h = hashlib.sha512(_LSAG_ALG.encode())
    for p in partes:
        h.update(len(p).to_bytes(4, "big") + p)
    return int.from_bytes(h.digest(), "little") % _L


def _hp(dados: bytes) -> Ponto:
    """hash -> ponto do subgrupo de ordem prima: tentativa e incremento, depois cofator ×8."""
    i = 0
    while True:
        p = _ed_descomp(hashlib.sha512(b"KONFIRMU/Hp/1|" + i.to_bytes(4, "big") + dados).digest()[:32])
        if p is not None:
            p = _ed_mult(8, p)
            if not _ed_igual(p, _ED_ID):
                return p
        i += 1


def _cabecalho_lsag(anel: Sequence[str], contexto: str) -> Tuple[bytes, Ponto]:
    cab = hashlib.sha512(canon({"alg": _LSAG_ALG, "anel": list(anel), "contexto": contexto})).digest()
    if cab not in _BASES_LSAG:
        _BASES_LSAG[cab] = _hp(cab)
    return cab, _BASES_LSAG[cab]


def lsag_assinar(sk: bytes, anel: Sequence[str], msg: bytes, contexto: str) -> Dict[str, Any]:
    """Assina `msg` em nome do anel (lista de chaves públicas Ed25519, em hexadecimal). Só consegue quem lá está."""
    a, prefixo, A = _ed_expande(sk)
    pks = [bytes.fromhex(p) for p in anel]
    if len(pks) < 2 or len(set(pks)) != len(pks) or A not in pks:
        raise ValueError("anel inválido, ou a chave de quem assina não pertence ao anel")
    pts = [_ponto_do_anel(p) for p in pks]
    if any(p is None for p in pts):
        raise ValueError("o anel tem uma chave que não é um ponto válido de ordem prima")
    x, n, pi = a % _L, len(pks), pks.index(A)
    cab, H = _cabecalho_lsag(anel, contexto)
    I = _ed_mult(x, H)
    imagem = _ed_comp(I)
    # os «sorteios» saem do segredo, da mensagem e do anel (como no Ed25519): mesma entrada -> mesma assinatura
    alfa = _hs(b"alfa", prefixo, cab, msg)
    c, s = [0] * n, [0] * n
    i = (pi + 1) % n
    c[i] = _hs(cab, imagem, msg, _ed_comp(_ed_mult(alfa, _ED_G)), _ed_comp(_ed_mult(alfa, H)))
    while i != pi:
        s[i] = _hs(b"s", prefixo, cab, msg, i.to_bytes(4, "big"))
        c[(i + 1) % n] = _hs(cab, imagem, msg, _ed_comp(_ed_mult2(s[i], _ED_G, c[i], pts[i])),  # type: ignore[arg-type]
                             _ed_comp(_ed_mult2(s[i], H, c[i], I)))
        i = (i + 1) % n
    s[pi] = (alfa - c[pi] * x) % _L
    return {"alg": _LSAG_ALG, "anel": list(anel), "contexto": contexto, "imagem": imagem.hex(),
            "c0": format(c[0], "064x"), "s": [format(v, "064x") for v in s]}


def lsag_verificar(sig: Dict[str, Any], msg: bytes) -> bool:
    """True só se a assinatura fecha o anel: alguém do anel assinou `msg`; não se fica a saber quem."""
    try:
        anel, n = sig["anel"], len(sig["anel"])
        campos = [sig["imagem"], sig["c0"]] + list(sig["s"]) + list(anel)
        if (sig["alg"] != _LSAG_ALG or n < 2 or len(set(anel)) != n or len(sig["s"]) != n
                or not all(isinstance(v, str) and _HEX64.fullmatch(v) for v in campos)):
            return False  # só uma escrita possível para cada assinatura: 64 hexadecimais minúsculos por campo
        pts = [_ponto_do_anel(bytes.fromhex(p)) for p in anel]
        imagem = bytes.fromhex(sig["imagem"])
        I = _ed_descomp(imagem)
        c0, s = int(sig["c0"], 16), [int(v, 16) for v in sig["s"]]
        if any(p is None for p in pts) or I is None or not _ed_primo(I) or c0 >= _L or any(v >= _L for v in s):
            return False
        cab, H = _cabecalho_lsag(anel, sig["contexto"])
        c = c0
        for i in range(n):
            c = _hs(cab, imagem, msg, _ed_comp(_ed_mult2(s[i], _ED_G, c, pts[i])), _ed_comp(_ed_mult2(s[i], H, c, I)))  # type: ignore[arg-type]
        return c == c0
    except (KeyError, TypeError, ValueError, AttributeError):
        return False


class Urna:
    """P11: uma votação. Só entra voto com assinatura de anel válida sobre o eleitorado registado; a imagem da chave
    (uma por pessoa e por votação) apanha o segundo voto sem dizer de quem é."""

    def __init__(self, votacao: str, anel: Sequence[str], opcoes: Sequence[str], livro: LedgerImutavel) -> None:
        self.votacao, self.anel, self.opcoes, self.livro = votacao, list(anel), list(opcoes), livro
        self.contexto = "VOTACAO/" + votacao
        self.imagens: Dict[str, str] = {}  # imagem da chave -> opção

    def boletim(self, opcao: str) -> bytes:
        return canon({"votacao": self.votacao, "opcao": opcao})

    def votar(self, opcao: str, sig: Any, dia: int) -> Dict[str, Any]:
        if opcao not in self.opcoes:
            estado = "VOTO_RECUSADO_OPCAO_DESCONHECIDA"
        elif not isinstance(sig, dict) or sig.get("anel") != self.anel or sig.get("contexto") != self.contexto:
            estado = "VOTO_RECUSADO_ANEL_OU_VOTACAO_ERRADOS"
        elif not lsag_verificar(sig, self.boletim(opcao)):
            estado = "VOTO_RECUSADO_ASSINATURA_INVALIDA"
        elif sig["imagem"] in self.imagens:
            estado = "VOTO_RECUSADO_DUPLO"
        else:
            self.imagens[sig["imagem"]] = opcao
            estado = "VOTO_ACEITE"
        return responder(self.livro, dia, estado, sig if isinstance(sig, dict) else str(sig),
                         {"alg": _LSAG_ALG, "votacao": self.votacao, "anel": self.anel, "opcoes": self.opcoes}, votacao=self.votacao, opcao=str(opcao))

    def contagem(self) -> Dict[str, int]:
        return {o: sum(1 for x in self.imagens.values() if x == o) for o in self.opcoes}


def votar_em_anel(sk: bytes, urna: Urna, opcao: str) -> Dict[str, Any]:
    return lsag_assinar(sk, urna.anel, urna.boletim(opcao), urna.contexto)


# -----------------------------------------------------------------------------
# 14. P13 + P24 — REGISTO PROVA/1 (pré-selado) E PACOTES DE CÁLCULO ABERTOS (KPKG)
# -----------------------------------------------------------------------------
def prova1_reexecutar(fecho: Dict[str, Any], fontes: Dict[str, Dict[str, str]], pub: Optional[str] = None) -> Tuple[str, Dict[str, Any]]:
    """Refaz o veredicto de uma PROVA/1 só com o que está selado: critério pré-selado + leituras seladas.
    CUMPRIDO pede consenso de N>=3 fontes independentes, sem autorrelato, e o mínimo garantido a 95%."""
    try:
        pre = fecho["pre"]
        d = pre["dados"]
        if (d.get("prova") != "PROVA/1" or not selo_ok(d, pre["selo"], None if pub is None else {pub})
                or sorted(fecho["slots"]) != d["slots"] or any(v is None for v in fecho["slots"].values())):
            return "INVALIDA", {}
        o = oraculo(fecho["leituras"], fontes, d["unidade"], d["id"], excluir_operador=d["operador"], janela=(d["dia"], fecho["dia"]))
    except (KeyError, TypeError, ValueError, AttributeError):
        return "INVALIDA", {}
    det = {"oraculo": o.get("estado"), "valor": o.get("valor"), "incerteza": o.get("incerteza"), "confianca": o.get("confianca")}
    if o["estado"] == "INSUFICIENTE" or o["confianca"] < REGRAS["confianca_min"]:
        return "INCONCLUSIVO", det
    k95 = REGRAS["k95_unilateral"]
    if o["valor"] - k95 * o["incerteza"] >= d["minimo"]:
        return "CUMPRIDO", det
    if o["valor"] + k95 * o["incerteza"] < d["minimo"]:
        return "NAO_CUMPRIDO", det
    return "INCONCLUSIVO", det


class Prova1:
    """P13 — REGISTO PROVA/1. A pergunta, a métrica e o mínimo selam-se ANTES de haver dados; cada slot guarda só o
    hash da evidência (a fotografia fica com quem a tirou); as leituras só contam se forem posteriores ao pré-selo.
    [VALIDAR] O formato PROVA/1 da casa não se deixou ler a 20-11-2026: este é o mínimo que cumpre a ordem."""

    def __init__(self, livro: LedgerImutavel, sk: bytes, operador: str) -> None:
        self.livro, self.sk, self.operador = livro, sk, operador
        self.registos: Dict[str, Dict[str, Any]] = {}

    def pre_registar(self, pid: str, pergunta: str, metrica: str, unidade: str, minimo: float, slots: Sequence[str], dia: int) -> str:
        if pid in self.registos:
            return "RECUSADO_JA_PRE_SELADA"  # o critério não se muda depois de ver os dados
        dados = {"prova": "PROVA/1", "id": pid, "operador": self.operador, "pergunta": pergunta, "metrica": metrica,
                 "unidade": unidade, "minimo": minimo, "slots": sorted(slots), "dia": dia}
        self.registos[pid] = {"pre": {"dados": dados, "selo": selar(dados, self.sk)}, "slots": {s: None for s in sorted(slots)}, "fecho": None}
        self.livro.registar(dia, "PROVA1_PRE_SELADA", {"id": pid, "pre": self.registos[pid]["pre"]["selo"]["hash"]})
        return "PRE_SELADA"

    def preencher(self, pid: str, slot: str, evidencia: bytes, dia: int) -> str:
        r = self.registos.get(pid)
        if r is None or slot not in r["slots"]:
            return "RECUSADO_SLOT_DESCONHECIDO"
        if r["fecho"] is not None:
            return "RECUSADO_PROVA_FECHADA"
        if r["slots"][slot] is not None:
            return "RECUSADO_SLOT_JA_PREENCHIDO"
        r["slots"][slot] = h256(evidencia)  # só o hash entra; a evidência fica com quem a tem
        self.livro.registar(dia, "PROVA1_SLOT", {"id": pid, "slot": slot, "evidencia": r["slots"][slot]})
        return "PREENCHIDO"

    def fechar(self, pid: str, leituras: Sequence[Dict], fontes: Dict[str, Dict[str, str]], dia: int) -> Dict[str, Any]:
        r = self.registos[pid]
        criterio = r["pre"]["selo"]["hash"]  # a «fórmula» desta resposta é o critério pré-selado
        entrada = {"id": pid, "slots": dict(r["slots"]), "leituras": [hobj(l) for l in leituras], "dia": dia}
        if r["fecho"] is not None:
            return responder(self.livro, dia, "PROVA1_RECUSADA", entrada, criterio, resultado="RECUSADO_PROVA_FECHADA")
        vazios = sorted(s for s, v in r["slots"].items() if v is None)
        if vazios:
            return responder(self.livro, dia, "PROVA1_ABERTA", entrada, criterio, resultado="INCOMPLETO", slots_vazios=vazios)
        fecho: Dict[str, Any] = {"id": pid, "pre": r["pre"], "slots": dict(r["slots"]), "leituras": list(leituras), "dia": dia}
        resultado, det = prova1_reexecutar(fecho, fontes, ed_publica(self.sk).hex())
        if resultado in ("INCONCLUSIVO", "INVALIDA"):  # fica aberta: nem cumprido nem falhado sem prova que chegue
            return responder(self.livro, dia, "PROVA1_ABERTA", entrada, criterio, resultado=resultado, **det)
        fecho["resultado"] = resultado
        r["fecho"] = {"dados": fecho, "selo": selar(fecho, self.sk)}
        return responder(self.livro, dia, "PROVA1_FECHADA", entrada, criterio, resultado=resultado, fecho=fecho, selo=r["fecho"]["selo"], **det)

    def conferir(self, pid: str, evidencias: Dict[str, bytes], fontes: Dict[str, Dict[str, str]]) -> bool:
        """Quem tem as evidências confere tudo: selo do fecho, hash de cada evidência e o veredicto refeito de raiz."""
        f = self.registos[pid]["fecho"]
        pub = ed_publica(self.sk).hex()
        return (f is not None and selo_ok(f["dados"], f["selo"], {pub})
                and all(h256(evidencias.get(s, b"")) == h for s, h in f["dados"]["slots"].items())
                and prova1_reexecutar(f["dados"], fontes, pub)[0] == f["dados"]["resultado"])


def entradas_africa_2030(paineis: float = 4.0) -> Dict[str, Dict[str, Any]]:
    """Os inputs do cenário «ÁFRICA 2030», com etiqueta e fonte. Quase tudo é ASSUMIDO: é cenário, não facto."""
    A = "ASSUMIDO"
    return {
        # «desenho de C1» é o D1 de hoje. Não se muda uma letra: assim o pacote dá o mesmo hash que deu na v1.0.
        "paineis": {"valor": paineis, "incerteza": 0.0, "unidade": "painel/microrrede", "etiqueta": A, "fonte": "desenho de C1", "esforco": 1, "limite": 8.0},
        "area": {"valor": 1.95, "incerteza": 0.02, "unidade": "m2/painel", "etiqueta": A, "fonte": "ficha técnica típica [VALIDAR]"},
        "rendimento": {"valor": 22.0, "incerteza": 1.5, "unidade": "%", "etiqueta": A, "fonte": "valor da ordem"},
        "pr": {"valor": 0.75, "incerteza": 0.05, "unidade": "1", "etiqueta": A, "fonte": "perdas típicas [VALIDAR]", "esforco": 1, "limite": 0.90},
        "sol_pico": {"valor": 5.5, "incerteza": 0.5, "unidade": "h/dia", "etiqueta": A, "fonte": "média grosseira; por local mede-se com o oráculo (P12)"},
        "jovens_por_ano": {"valor": 11e6, "incerteza": 1e6, "unidade": "pessoa/ano", "etiqueta": "MEDIDO",
                           "fonte": "Banco Africano de Desenvolvimento, Jobs for Youth in Africa 2016-2025: 10 a 12 milhões de jovens por ano (estimativa); lido a 20-11-2026 em tralac.org"},
        "anos": {"valor": 4.0, "incerteza": 0.0, "unidade": "ano", "etiqueta": A, "fonte": "2027 a 2030"},
        "fracao_formada": {"valor": 0.001, "incerteza": 0.0002, "unidade": "1", "etiqueta": A, "fonte": "1 jovem em cada 1000 [VALIDAR]", "esforco": 1, "limite": 0.005},
        "perdas": {"valor": 0.10, "incerteza": 0.03, "unidade": "1", "etiqueta": A, "fonte": "perdas de distribuição [VALIDAR]", "esforco": -1, "limite": 0.03},
        "consumo_basico": {"valor": 0.20, "incerteza": 0.05, "unidade": "kWh/dia/pessoa", "etiqueta": A, "fonte": "cerca de 1 kWh/dia por casa de 5 pessoas [VALIDAR]"},
        "horas_pratica": {"valor": 6000.0, "incerteza": 600.0, "unidade": "h", "etiqueta": A, "fonte": "4 anos × 1500 h por instalador [VALIDAR]", "esforco": 1, "limite": 8000.0},
        "horas_primeira": {"valor": 400.0, "incerteza": 80.0, "unidade": "h", "etiqueta": A, "fonte": "horas para montar a 1.ª microrrede [VALIDAR]", "esforco": -1, "limite": 100.0},
        "taxa_aprendizagem": {"valor": 0.20, "incerteza": 0.05, "unidade": "1", "etiqueta": A, "fonte": "20% por duplicação, típico da lei de Wright [VALIDAR]"},
    }


def kpkg_emitir(cenario: str, entradas: Dict[str, Dict[str, Any]], sk: bytes) -> Dict[str, Any]:
    """P24 — pacote de cálculo aberto (KPKG/1): inputs + fórmulas (versão e hash) + resultado, em JSON canónico, com selo.
    Qualquer pessoa emite; ninguém tem de confiar em quem emitiu, porque quem recebe refaz a conta."""
    if auditar_canarios():
        raise RuntimeError("COFRE_COMPROMETIDO: há um canário tocado; deste cofre não sai pacote nenhum")
    y, _ = calcular_cenario(entradas)
    v, u = y.em("pessoa")
    corpo = {"kpkg": "KPKG/1", "motor": VERSAO, "cenario": cenario, "carimbo": CARIMBO, "entradas": entradas,
             "formulas": {k: {"versao": FORMULAS[k]["versao"], "hash": hobj(FORMULAS[k])} for k in ("F2", "F4", "F5", "F8")},
             "resultado": {"valor": v, "incerteza": u, "unidade": "pessoa"}}
    return {"corpo": corpo, "selo": selar(corpo, sk)}


def kpkg_consumir(pkg: Dict[str, Any], emissores: Optional[Any] = None) -> Dict[str, Any]:
    """P24 — quem recebe não confia: confere o selo, as fórmulas (pelo hash) e REFAZ a conta de raiz."""
    try:
        corpo, selo = pkg["corpo"], pkg["selo"]
        if corpo.get("kpkg") != "KPKG/1":
            return {"estado": "FORMATO_DESCONHECIDO"}
        if not selo_ok(corpo, selo, emissores):
            return {"estado": "SELO_INVALIDO"}
        if auditar_canarios():
            return {"estado": "COFRE_COMPROMETIDO"}  # com um canário tocado, este cofre não faz contas para ninguém
        iscas = sorted(k for k in corpo["formulas"] if k in CANARIOS)
        if iscas:
            return {"estado": "ALARME_CANARIO", "canarios": iscas}  # nenhuma conta verdadeira usa uma isca
        for k, f in sorted(corpo["formulas"].items()):
            if k not in FORMULAS or hobj(FORMULAS[k]) != f["hash"]:
                return {"estado": "FORMULA_DIFERENTE", "formula": k}
        y, _ = calcular_cenario(corpo["entradas"])
        v, u = y.em(corpo["resultado"]["unidade"])
        igual = _limpo([v, u]) == _limpo([corpo["resultado"]["valor"], corpo["resultado"]["incerteza"]])
        return {"estado": "REPRODUZIDO" if igual else "RESULTADO_DIFERENTE", "valor": v, "incerteza": u, "hash": selo["hash"],
                "hash_input": hobj(corpo["entradas"]), "hash_formula": hobj({k: FORMULAS[k] for k in sorted(corpo["formulas"])})}
    except VetoFisico as e:
        return {"estado": "VETO_FISICO", "motivo": str(e)}
    except TypeError as e:
        return {"estado": "ERRO_DE_UNIDADES", "motivo": str(e)}
    except (KeyError, ValueError, AttributeError) as e:
        return {"estado": "PACOTE_MAL_FORMADO", "motivo": f"{type(e).__name__}: {e}"}


# -----------------------------------------------------------------------------
# 15. P21 + P22 — CONSTITUIÇÃO EM CÓDIGO E FORKS
# -----------------------------------------------------------------------------
# P21. Mudar uma REGRA é a operação mais difícil do sistema: proposta selada por um membro do eleitorado +
# k >= 5 votos SIM anónimos (anel, P11) + assinatura humana de um guardião registado + versão nova. Cada versão
# guarda a prova inteira da sua emenda e o hash da anterior: a antiga fica verificável para sempre.
# Mexer nas regras por fora (sem emenda) faz o hash das regras em memória deixar de bater com a constituição:
# o motor recusa trabalhar e a diferença fica na ledger, à vista de quem quiser conferir.
# [VALIDAR] Os limites pétreos (o que nem uma emenda pode fazer) são escolha minha.
LIMITES_PETREOS: Dict[str, Tuple[float, float]] = {
    "quorum_k": (5, 99), "prazo_dias": (1, 60), "fundo_reparacao_pct": (1, 10), "confianca_min": (0.5, 1.0),
}


def _regra(regras: Dict[str, Any], caminho: str) -> Any:
    o: Any = regras
    for parte in caminho.split("."):
        if not isinstance(o, dict) or parte not in o:
            raise KeyError(caminho)
        o = o[parte]
    return o


def _regra_por(regras: Dict[str, Any], caminho: str, valor: Any) -> None:
    *pais, folha = caminho.split(".")
    alvo = _regra(regras, ".".join(pais)) if pais else regras
    alvo[folha] = valor


class Constituicao:
    def __init__(self, eleitorado: Sequence[str], guardioes: Dict[str, str], livro: LedgerImutavel, dia: int = 0) -> None:
        self.eleitorado, self.guardioes, self.livro = list(eleitorado), dict(guardioes), livro
        self.versoes: List[Dict[str, Any]] = []
        self._nova(json.loads(json.dumps(REGRAS)), None, dia)

    def _nova(self, regras: Dict[str, Any], emenda: Optional[Dict[str, Any]], dia: int) -> Dict[str, Any]:
        corpo = {"n": len(self.versoes), "regras": regras, "hash_regras": hobj(regras),
                 "hash_anterior": self.versoes[-1]["hash"] if self.versoes else "0" * 64, "emenda": emenda, "dia": dia}
        v = dict(corpo, hash=hobj(corpo))
        self.versoes.append(v)
        self.livro.registar(dia, "CONSTITUICAO_VERSAO", {k: v[k] for k in ("n", "hash", "hash_regras", "hash_anterior")})
        return v

    def atual(self) -> Dict[str, Any]:
        return self.versoes[-1]

    def fiel(self) -> bool:
        """As regras em memória são as da última versão ratificada? Se não, alguém mexeu por fora."""
        return hobj(REGRAS) == self.atual()["hash_regras"]

    def propor(self, caminho: str, valor: Any, motivo: str, sk: bytes, dia: int) -> Dict[str, Any]:
        try:
            de = _regra(self.atual()["regras"], caminho)
        except KeyError:
            de = None
        dados = {"constituicao": self.atual()["hash"], "caminho": caminho, "de": de, "para": valor, "motivo": motivo, "dia": dia}
        return {"dados": dados, "selo": selar(dados, sk)}

    def boletim(self, proposta: Dict[str, Any]) -> Tuple[bytes, str]:
        hp = proposta["selo"]["hash"]
        return canon({"emenda": hp, "voto": "SIM"}), "EMENDA/" + hp

    def _valida(self, base: Dict[str, Any], proposta: Any, votos: Sequence[Any], guardiao: Any, selo_guardiao: Any
                ) -> Tuple[str, Dict[str, Any], List[Dict[str, Any]]]:
        """Devolve (motivo, detalhe, votos válidos). motivo == '' quer dizer que a emenda cumpre tudo."""
        d = proposta.get("dados", {}) if isinstance(proposta, dict) else {}
        selo = proposta.get("selo", {}) if isinstance(proposta, dict) else {}
        if not isinstance(d, dict) or not selo_ok(d, selo, set(self.eleitorado)):
            return "PROPOSTA_SEM_SELO_DO_ELEITORADO", {}, []
        if d.get("constituicao") != base["hash"]:
            return "PROPOSTA_DE_OUTRA_VERSAO", {}, []  # uma emenda vale para UMA versão: não se reapresenta
        try:
            atual = _regra(base["regras"], str(d.get("caminho")))
        except KeyError:
            return "REGRA_DESCONHECIDA", {}, []
        para = d.get("para")
        if isinstance(atual, (dict, list)) or type(para) is not type(atual):
            return "TIPO_DIFERENTE_DO_DA_REGRA", {}, []
        lim = LIMITES_PETREOS.get(d["caminho"])
        if lim is not None and not lim[0] <= para <= lim[1]:
            return "CLAUSULA_PETREA", {"limites": list(lim)}, []
        boletim, contexto = self.boletim(proposta)
        validos: List[Dict[str, Any]] = []
        imagens = set()
        for v in votos:
            if (isinstance(v, dict) and v.get("anel") == self.eleitorado and v.get("contexto") == contexto
                    and v.get("imagem") not in imagens and lsag_verificar(v, boletim)):
                imagens.add(v["imagem"])
                validos.append(v)
        k = base["regras"]["quorum_k"]
        if len(validos) < k:
            return "SEM_QUORUM", {"votos_validos": len(validos), "exigidos": k}, validos
        if guardiao not in self.guardioes or not selo_ok({"ratifico": selo["hash"], "guardiao": guardiao}, selo_guardiao,
                                                         {self.guardioes[guardiao]}):
            return "SEM_ASSINATURA_HUMANA", {"votos_validos": len(validos)}, validos
        return "", {"votos_validos": len(validos)}, validos

    def ratificar(self, proposta: Any, votos: Sequence[Any], guardiao: Any, selo_guardiao: Any, dia: int) -> Dict[str, Any]:
        base = self.atual()
        d = proposta.get("dados", {}) if isinstance(proposta, dict) else {}
        tentativa = {"proposta": hobj(proposta), "caminho": d.get("caminho") if isinstance(d, dict) else None,
                     "para": d.get("para") if isinstance(d, dict) else None, "votos": [hobj(v) for v in votos],
                     "guardiao": str(guardiao), "dia": dia}
        if auditar_canarios():
            motivo, det, validos = "COFRE_COMPROMETIDO", {}, []
        else:
            motivo, det, validos = self._valida(base, proposta, votos, guardiao, selo_guardiao)
        if motivo:  # a tentativa fica escrita, com hash: quem tentou mudar a regra não o apaga
            return responder(self.livro, dia, "REJEITADA", tentativa, base["hash_regras"], motivo=motivo,
                             hash_tentativa=hobj(tentativa), **det)
        novas = json.loads(json.dumps(base["regras"]))
        _regra_por(novas, d["caminho"], d["para"])
        v = self._nova(novas, {"proposta": proposta, "votos": validos, "guardiao": guardiao, "selo_guardiao": selo_guardiao}, dia)
        REGRAS.clear()
        REGRAS.update(json.loads(json.dumps(novas)))  # só aqui as regras em vigor mudam
        return responder(self.livro, dia, "EMENDA_RATIFICADA", tentativa, base["hash_regras"], versao=v["n"], hash_versao=v["hash"],
                         regras_antes=base["hash_regras"], regras_depois=v["hash_regras"], **det)

    def conferir(self, versoes: Optional[Sequence[Dict[str, Any]]] = None) -> bool:
        """A cadeia de versões de raiz: hashes, ligação e, em cada emenda, proposta + votos em anel + assinatura humana."""
        versoes = self.versoes if versoes is None else versoes
        anterior = "0" * 64
        try:
            for i, v in enumerate(versoes):
                corpo = {k: x for k, x in v.items() if k != "hash"}
                if v["n"] != i or v["hash_anterior"] != anterior or hobj(corpo) != v["hash"] or hobj(v["regras"]) != v["hash_regras"]:
                    return False
                if i:
                    e, base = v["emenda"], versoes[i - 1]
                    esperadas = json.loads(json.dumps(base["regras"]))
                    _regra_por(esperadas, e["proposta"]["dados"]["caminho"], e["proposta"]["dados"]["para"])
                    if self._valida(base, e["proposta"], e["votos"], e["guardiao"], e["selo_guardiao"])[0] or hobj(esperadas) != v["hash_regras"]:
                        return False
                anterior = v["hash"]
        except (KeyError, TypeError, ValueError, AttributeError):
            return False
        return bool(versoes)


def fork_genesis(nome: str, mae: LedgerImutavel, const: Constituicao, sk_comunidade: bytes, dia: int) -> Tuple[LedgerImutavel, Dict[str, Any]]:
    """P22: uma comunidade abre a SUA cadeia a partir do cofre e da constituição da mãe, com chave própria.
    Nasce com selo B (não-selado). A fábrica é de todos; a confiança conquista-se com prova (ver selo_do_fork)."""
    if auditar_canarios():
        raise RuntimeError("COFRE_COMPROMETIDO: não se abre um fork de um cofre com canários tocados")
    filho = LedgerImutavel(sk_comunidade)
    genesis = {"fork": nome, "mae": {"pub": mae.pub, "cabeca": mae.cabeca(), "blocos": len(mae.blocos)}, "cofre": hash_cofre(),
               "constituicao": const.atual()["hash"], "regras": const.atual()["hash_regras"], "selo_de_confianca": "B"}
    hg = filho.registar(dia, "GENESIS_FORK", genesis)
    mae.registar(dia, "FORK_NASCEU", {"fork": nome, "pub": filho.pub, "genesis": hg})
    return filho, dict(genesis, hash_genesis=hg)


def selo_do_fork(filho: LedgerImutavel, fontes: Dict[str, Dict[str, str]]) -> str:
    """P22: B = nasceu e a cadeia confere, ainda sem prova; A = além disso tem pelo menos uma PROVA/1 que, refeita
    de raiz por quem verifica (critério pré-selado + leituras de 3 fontes independentes), dá CUMPRIDO.
    Escrever «CUMPRIDO» na própria cadeia não chega. [VALIDAR] os nomes dos graus (A, B) são escolha."""
    if not filho.blocos or filho.blocos[0]["evento"] != "GENESIS_FORK" or not filho.verificar_integridade_cadeia():
        return "INVALIDO"
    for b in filho.blocos:
        if b["evento"] == "PROVA1_FECHADA" and prova1_reexecutar(b["payload"].get("fecho", {}), fontes, filho.pub)[0] == "CUMPRIDO":
            return "A"
    return "B"


# -----------------------------------------------------------------------------
# 16. P12 — ORÁCULOS REAIS COM INCERTEZA: LEITURAS GRAVADAS, COM FONTE E DATA
# -----------------------------------------------------------------------------
# O demo não usa rede: lê do cofre o que foi lido na fonte, com a data em que foi lido. As fontes reais não assinam
# os seus números: sela-os quem os leu, e a prova é voltar à fonte. Fonte que não se deixou ler fica POR_LER, com o
# pedido exato; o modo --ler-oraculos faz essa leitura numa máquina com rede.
DATA_LOGICA = "2026-11-20"  # a data do demo: declarada aqui, nunca lida do relógio

ORACULOS_GRAVADOS: Dict[str, Dict[str, Any]] = {
    "irradiacao/maputo": {
        "id": "O12.irradiacao_maputo", "versao": "1.0.0", "nome": "irradiação global horizontal em Maputo, média diária do ano",
        "formula": "leitura gravada; sol de pico (h/dia) = irradiação / G_stc; com N>=3 fontes, o consenso é a mediana das concordantes",
        "unidades": {"saida": "MJ/m2/dia"}, "unidade": "MJ/m2/dia", "plausivel": [10.0, 26.0], "etiqueta": "MEDIDO",
        "fonte": "INAM (Instituto Nacional de Meteorologia de Moçambique), em «Energia na Agricultura» (2019): média diária de 17,96 MJ/m2 "
                 "e 7,8 h de sol em Maputo; lido a 20-11-2026 num resumo de pesquisa [VALIDAR: reler no artigo]",
        "leituras": [
            {"fonte": "INAM_estacao_de_Maputo", "operador": "INAM", "valor": 17.96, "incerteza": 0.90, "etiqueta": "MEDIDO",
             "nota": "o valor é MEDIDO; os ± 5% são ASSUMIDO (erro típico de um piranómetro mais a variação entre anos) [VALIDAR]"},
            {"fonte": "PVGIS_SARAH2", "operador": "JRC_Comissao_Europeia", "valor": None, "estado": "POR_LER",
             "pedido": "https://re.jrc.ec.europa.eu/api/v5_3/MRcalc?lat=-25.97&lon=32.57&horirrad=1&outputformat=json",
             "nota": "a 20-11-2026 a API recusou leitura automática"},
            {"fonte": "Open_Meteo_ERA5", "operador": "Open_Meteo", "valor": None, "estado": "POR_LER",
             "pedido": "https://archive-api.open-meteo.com/v1/archive?latitude=-25.97&longitude=32.57&start_date=2015-01-01"
                       "&end_date=2024-12-31&daily=shortwave_radiation_sum&timezone=UTC",
             "nota": "a 20-11-2026 a API recusou leitura automática"},
        ],
        "coerencia": {"minimo": 1785.0, "maximo": 2206.0, "unidade": "kWh/m2/ano",
                      "fonte": "mapa solar de Moçambique (Banco Mundial, via energypedia): 1785 a 2206 kWh/m2/ano no país; lido a 20-11-2026"},
        "o_que_nao_garante": "uma só fonte lida: serve para dimensionar com folga, não para punir ninguém. Não dá o pior mês nem o pior ano.",
    },
    "cambio/USD_por_EUR": {
        "id": "O12.cambio_USD_por_EUR", "versao": "1.0.0", "nome": "taxa de referência do euro face ao dólar",
        "formula": "leitura gravada da taxa de referência; converter: EUR = USD / taxa",
        "unidades": {"saida": "USD/EUR"}, "unidade": "USD/EUR", "plausivel": [0.5, 2.0], "etiqueta": "MEDIDO",
        "fonte": "Banco Central Europeu, série EXR.D.USD.EUR.SP00.A no portal de dados do BCE; lido a 20-11-2026 num resumo de pesquisa",
        "leituras": [
            {"fonte": "BCE_taxa_de_referencia", "operador": "Banco_Central_Europeu", "valor": 1.1787, "incerteza": 0.059, "etiqueta": "MEDIDO",
             "data": "2025-12-24", "nota": "a taxa é MEDIDO; os ± 5% são ASSUMIDO, por a leitura ser antiga [VALIDAR]"},
            {"fonte": "BCE_API_SDMX", "operador": "Banco_Central_Europeu", "valor": None, "estado": "POR_LER",
             "pedido": "https://data-api.ecb.europa.eu/service/data/EXR/D.USD.EUR.SP00.A?lastNObservations=10&format=csvdata",
             "nota": "a 20-11-2026 a API recusou leitura automática"},
        ],
        "o_que_nao_garante": "uma taxa com meses não serve para pagar, só para cenário; a do dia lê-se na fonte.",
    },

    "cambio/BRL_por_EUR": {
        "id": "O12.cambio_BRL_por_EUR", "versao": "1.0.0", "nome": "taxa de referência do euro face ao real brasileiro",
        "formula": "leitura gravada da taxa de referência; converter: EUR = BRL / taxa",
        "unidades": {"saida": "BRL/EUR"}, "unidade": "BRL/EUR", "plausivel": [3.5, 8.0], "etiqueta": "MEDIDO",
        "fonte": "Banco Central Europeu, série EXR.D.BRL.EUR.SP00.A (taxas de referência diárias); corredor NL→BR (remessas). "
                 "Faixa plausível ASSUMIDO [VALIDAR]. Entrou POR_LER na v2.5.2 (grelha mundial).",
        "leituras": [
            {"fonte": "BCE_API_SDMX_BRL", "operador": "Banco_Central_Europeu", "valor": None, "estado": "POR_LER",
             "pedido": "https://data-api.ecb.europa.eu/service/data/EXR/D.BRL.EUR.SP00.A?lastNObservations=10&format=csvdata",
             "nota": "o leitor é o mesmo do BCE (CSV SDMX); nome único por moeda"},
        ],
        "o_que_nao_garante": "a taxa de referência do BCE não é a taxa que a pessoa recebe: a margem de quem envia fica fora — é "
                             "exatamente essa diferença que o mecanismo de remessas mede. Uma taxa com dias não serve para pagar, só para cenário.",
    },
    "cambio/GBP_por_EUR": {
        "id": "O12.cambio_GBP_por_EUR", "versao": "1.0.0", "nome": "taxa de referência do euro face à libra esterlina",
        "formula": "leitura gravada da taxa de referência; converter: EUR = GBP / taxa",
        "unidades": {"saida": "GBP/EUR"}, "unidade": "GBP/EUR", "plausivel": [0.7, 1.3], "etiqueta": "MEDIDO",
        "fonte": "Banco Central Europeu, série EXR.D.GBP.EUR.SP00.A (taxas de referência diárias); corredor NL→UK. "
                 "Faixa plausível ASSUMIDO [VALIDAR]. Entrou POR_LER na v2.5.2 (grelha mundial).",
        "leituras": [
            {"fonte": "BCE_API_SDMX_GBP", "operador": "Banco_Central_Europeu", "valor": None, "estado": "POR_LER",
             "pedido": "https://data-api.ecb.europa.eu/service/data/EXR/D.GBP.EUR.SP00.A?lastNObservations=10&format=csvdata",
             "nota": "o leitor é o mesmo do BCE (CSV SDMX); nome único por moeda"},
        ],
        "o_que_nao_garante": "a taxa de referência do BCE não é a taxa que a pessoa recebe: a margem de quem envia fica fora. Uma taxa com dias não serve para pagar, só para cenário.",
    },
    "cambio/ZAR_por_EUR": {
        "id": "O12.cambio_ZAR_por_EUR", "versao": "1.0.0", "nome": "taxa de referência do euro face ao rand sul-africano",
        "formula": "leitura gravada da taxa de referência; converter: EUR = ZAR / taxa",
        "unidades": {"saida": "ZAR/EUR"}, "unidade": "ZAR/EUR", "plausivel": [12.0, 30.0], "etiqueta": "MEDIDO",
        "fonte": "Banco Central Europeu, série EXR.D.ZAR.EUR.SP00.A (taxas de referência diárias); corredor NL→ZA; proxy regional "
                 "para a Lusofonia africana (MZN e AOA não são publicadas pelo BCE — honestidade: aqui falta a moeda de Maputo e Luanda). "
                 "Faixa plausível ASSUMIDO [VALIDAR]. Entrou POR_LER na v2.5.2 (grelha mundial).",
        "leituras": [
            {"fonte": "BCE_API_SDMX_ZAR", "operador": "Banco_Central_Europeu", "valor": None, "estado": "POR_LER",
             "pedido": "https://data-api.ecb.europa.eu/service/data/EXR/D.ZAR.EUR.SP00.A?lastNObservations=10&format=csvdata",
             "nota": "o leitor é o mesmo do BCE (CSV SDMX); nome único por moeda"},
        ],
        "o_que_nao_garante": "a taxa de referência do BCE não é a taxa que a pessoa recebe: a margem de quem envia fica fora. ZAR não é MZN nem AOA: serve de cenário regional, não de conversão.",
    },
    "cambio/TRY_por_EUR": {
        "id": "O12.cambio_TRY_por_EUR", "versao": "1.0.0", "nome": "taxa de referência do euro face à lira turca",
        "formula": "leitura gravada da taxa de referência; converter: EUR = TRY / taxa",
        "unidades": {"saida": "TRY/EUR"}, "unidade": "TRY/EUR", "plausivel": [15.0, 70.0], "etiqueta": "MEDIDO",
        "fonte": "Banco Central Europeu, série EXR.D.TRY.EUR.SP00.A (taxas de referência diárias); corredor NL→TR. "
                 "Faixa plausível ASSUMIDO [VALIDAR]. Entrou POR_LER na v2.5.2 (grelha mundial).",
        "leituras": [
            {"fonte": "BCE_API_SDMX_TRY", "operador": "Banco_Central_Europeu", "valor": None, "estado": "POR_LER",
             "pedido": "https://data-api.ecb.europa.eu/service/data/EXR/D.TRY.EUR.SP00.A?lastNObservations=10&format=csvdata",
             "nota": "o leitor é o mesmo do BCE (CSV SDMX); nome único por moeda"},
        ],
        "o_que_nao_garante": "a taxa de referência do BCE não é a taxa que a pessoa recebe: a margem de quem envia fica fora. Uma taxa com dias não serve para pagar, só para cenário.",
    },
    "cambio/PHP_por_EUR": {
        "id": "O12.cambio_PHP_por_EUR", "versao": "1.0.0", "nome": "taxa de referência do euro face ao peso filipino",
        "formula": "leitura gravada da taxa de referência; converter: EUR = PHP / taxa",
        "unidades": {"saida": "PHP/EUR"}, "unidade": "PHP/EUR", "plausivel": [45.0, 85.0], "etiqueta": "MEDIDO",
        "fonte": "Banco Central Europeu, série EXR.D.PHP.EUR.SP00.A (taxas de referência diárias); corredor NL→PH. "
                 "Faixa plausível ASSUMIDO [VALIDAR]. Entrou POR_LER na v2.5.2 (grelha mundial).",
        "leituras": [
            {"fonte": "BCE_API_SDMX_PHP", "operador": "Banco_Central_Europeu", "valor": None, "estado": "POR_LER",
             "pedido": "https://data-api.ecb.europa.eu/service/data/EXR/D.PHP.EUR.SP00.A?lastNObservations=10&format=csvdata",
             "nota": "o leitor é o mesmo do BCE (CSV SDMX); nome único por moeda"},
        ],
        "o_que_nao_garante": "a taxa de referência do BCE não é a taxa que a pessoa recebe: a margem de quem envia fica fora. Uma taxa com dias não serve para pagar, só para cenário.",
    },
    "cambio/INR_por_EUR": {
        "id": "O12.cambio_INR_por_EUR", "versao": "1.0.0", "nome": "taxa de referência do euro face à rupia indiana",
        "formula": "leitura gravada da taxa de referência; converter: EUR = INR / taxa",
        "unidades": {"saida": "INR/EUR"}, "unidade": "INR/EUR", "plausivel": [70.0, 130.0], "etiqueta": "MEDIDO",
        "fonte": "Banco Central Europeu, série EXR.D.INR.EUR.SP00.A (taxas de referência diárias); corredor NL→IN. "
                 "Faixa plausível ASSUMIDO [VALIDAR]. Entrou POR_LER na v2.5.2 (grelha mundial).",
        "leituras": [
            {"fonte": "BCE_API_SDMX_INR", "operador": "Banco_Central_Europeu", "valor": None, "estado": "POR_LER",
             "pedido": "https://data-api.ecb.europa.eu/service/data/EXR/D.INR.EUR.SP00.A?lastNObservations=10&format=csvdata",
             "nota": "o leitor é o mesmo do BCE (CSV SDMX); nome único por moeda"},
        ],
        "o_que_nao_garante": "a taxa de referência do BCE não é a taxa que a pessoa recebe: a margem de quem envia fica fora. Uma taxa com dias não serve para pagar, só para cenário.",
    },
    "cambio/MXN_por_EUR": {
        "id": "O12.cambio_MXN_por_EUR", "versao": "1.0.0", "nome": "taxa de referência do euro face ao peso mexicano",
        "formula": "leitura gravada da taxa de referência; converter: EUR = MXN / taxa",
        "unidades": {"saida": "MXN/EUR"}, "unidade": "MXN/EUR", "plausivel": [12.0, 30.0], "etiqueta": "MEDIDO",
        "fonte": "Banco Central Europeu, série EXR.D.MXN.EUR.SP00.A (taxas de referência diárias); corredor NL→MX. "
                 "Faixa plausível ASSUMIDO [VALIDAR]. Entrou POR_LER na v2.5.2 (grelha mundial).",
        "leituras": [
            {"fonte": "BCE_API_SDMX_MXN", "operador": "Banco_Central_Europeu", "valor": None, "estado": "POR_LER",
             "pedido": "https://data-api.ecb.europa.eu/service/data/EXR/D.MXN.EUR.SP00.A?lastNObservations=10&format=csvdata",
             "nota": "o leitor é o mesmo do BCE (CSV SDMX); nome único por moeda"},
        ],
        "o_que_nao_garante": "a taxa de referência do BCE não é a taxa que a pessoa recebe: a margem de quem envia fica fora. Uma taxa com dias não serve para pagar, só para cenário.",
    },
    "cambio/CNY_por_EUR": {
        "id": "O12.cambio_CNY_por_EUR", "versao": "1.0.0", "nome": "taxa de referência do euro face ao yuan chinês",
        "formula": "leitura gravada da taxa de referência; converter: EUR = CNY / taxa",
        "unidades": {"saida": "CNY/EUR"}, "unidade": "CNY/EUR", "plausivel": [5.0, 11.0], "etiqueta": "MEDIDO",
        "fonte": "Banco Central Europeu, série EXR.D.CNY.EUR.SP00.A (taxas de referência diárias); corredor NL→CN. "
                 "Faixa plausível ASSUMIDO [VALIDAR]. Entrou POR_LER na v2.5.2 (grelha mundial).",
        "leituras": [
            {"fonte": "BCE_API_SDMX_CNY", "operador": "Banco_Central_Europeu", "valor": None, "estado": "POR_LER",
             "pedido": "https://data-api.ecb.europa.eu/service/data/EXR/D.CNY.EUR.SP00.A?lastNObservations=10&format=csvdata",
             "nota": "o leitor é o mesmo do BCE (CSV SDMX); nome único por moeda"},
        ],
        "o_que_nao_garante": "a taxa de referência do BCE não é a taxa que a pessoa recebe: a margem de quem envia fica fora. Uma taxa com dias não serve para pagar, só para cenário.",
    },
    "cambio/PLN_por_EUR": {
        "id": "O12.cambio_PLN_por_EUR", "versao": "1.0.0", "nome": "taxa de referência do euro face ao zloty polaco",
        "formula": "leitura gravada da taxa de referência; converter: EUR = PLN / taxa",
        "unidades": {"saida": "PLN/EUR"}, "unidade": "PLN/EUR", "plausivel": [3.0, 6.0], "etiqueta": "MEDIDO",
        "fonte": "Banco Central Europeu, série EXR.D.PLN.EUR.SP00.A (taxas de referência diárias); corredor NL→PL. "
                 "Faixa plausível ASSUMIDO [VALIDAR]. Entrou POR_LER na v2.5.2 (grelha mundial).",
        "leituras": [
            {"fonte": "BCE_API_SDMX_PLN", "operador": "Banco_Central_Europeu", "valor": None, "estado": "POR_LER",
             "pedido": "https://data-api.ecb.europa.eu/service/data/EXR/D.PLN.EUR.SP00.A?lastNObservations=10&format=csvdata",
             "nota": "o leitor é o mesmo do BCE (CSV SDMX); nome único por moeda"},
        ],
        "o_que_nao_garante": "a taxa de referência do BCE não é a taxa que a pessoa recebe: a margem de quem envia fica fora. Uma taxa com dias não serve para pagar, só para cenário.",
    },
    "irradiacao/amesterdam": {
        "id": "O12.irradiacao_amesterdam", "versao": "1.0.0", "nome": "irradiação global horizontal em Amesterdão, média diária do ano",
        "formula": "leitura gravada; sol de pico (h/dia) = irradiação / G_stc; com N>=3 fontes, o consenso é a mediana das concordantes",
        "unidades": {"saida": "MJ/m2/dia"}, "unidade": "MJ/m2/dia", "plausivel": [5.0, 14.0], "etiqueta": "MEDIDO",
        "fonte": "Open-Meteo, archive API (reanálise ERA5, cobertura global), Amesterdão 52.37N 4.90E — a casa da Konfirmu. "
                 "Faixa plausível ASSUMIDO [VALIDAR]. Entrou POR_LER na v2.5.2 (grelha mundial).",
        "leituras": [
            {"fonte": "Open_Meteo_ERA5_AMESTERDAO", "operador": "Open_Meteo", "valor": None, "estado": "POR_LER",
             "pedido": "https://archive-api.open-meteo.com/v1/archive?latitude=52.37&longitude=4.90&start_date=2015-01-01"
                       "&end_date=2024-12-31&daily=shortwave_radiation_sum&timezone=UTC",
             "nota": "o leitor é o mesmo do ERA5 (cobertura global, ao contrário do PVGIS); nome único por cidade"},
        ],
        "o_que_nao_garante": "média do ano: não dá o pior mês nem o pior ano; uma só fonte: serve para dimensionar com folga, não para punir ninguém.",
    },
    "irradiacao/lisboa": {
        "id": "O12.irradiacao_lisboa", "versao": "1.0.0", "nome": "irradiação global horizontal em Lisboa, média diária do ano",
        "formula": "leitura gravada; sol de pico (h/dia) = irradiação / G_stc; com N>=3 fontes, o consenso é a mediana das concordantes",
        "unidades": {"saida": "MJ/m2/dia"}, "unidade": "MJ/m2/dia", "plausivel": [13.0, 25.0], "etiqueta": "MEDIDO",
        "fonte": "(1) Open-Meteo, archive API (reanálise ERA5, cobertura global), Lisboa 38.72N 9.14W. (2) PVGIS-SARAH2 (JRC), "
                 "cobertura Europa/África. Faixa plausível ASSUMIDO [VALIDAR]. Entrou POR_LER na v2.5.2 (grelha mundial).",
        "leituras": [
            {"fonte": "Open_Meteo_ERA5_LISBOA", "operador": "Open_Meteo", "valor": None, "estado": "POR_LER",
             "pedido": "https://archive-api.open-meteo.com/v1/archive?latitude=38.72&longitude=-9.14&start_date=2015-01-01"
                       "&end_date=2024-12-31&daily=shortwave_radiation_sum&timezone=UTC",
             "nota": "o leitor é o mesmo do ERA5; nome único por cidade"},
            {"fonte": "PVGIS_SARAH2_LISBOA", "operador": "JRC_Comissao_Europeia", "valor": None, "estado": "POR_LER",
             "pedido": "https://re.jrc.ec.europa.eu/api/v5_3/MRcalc?lat=38.72&lon=-9.14&horirrad=1&outputformat=json",
             "nota": "segunda fonte independente (SARAH2 cobre a Europa) — N>=2 fora de Maputo pela primeira vez"},
        ],
        "o_que_nao_garante": "média do ano: não dá o pior mês nem o pior ano; com 2 fontes, sem consenso de 3: serve para dimensionar com folga.",
    },
    "irradiacao/luanda": {
        "id": "O12.irradiacao_luanda", "versao": "1.0.0", "nome": "irradiação global horizontal em Luanda, média diária do ano",
        "formula": "leitura gravada; sol de pico (h/dia) = irradiação / G_stc; com N>=3 fontes, o consenso é a mediana das concordantes",
        "unidades": {"saida": "MJ/m2/dia"}, "unidade": "MJ/m2/dia", "plausivel": [14.0, 25.0], "etiqueta": "MEDIDO",
        "fonte": "Open-Meteo, archive API (reanálise ERA5, cobertura global), Luanda 8.84S 13.23E. "
                 "Faixa plausível ASSUMIDO [VALIDAR]. Entrou POR_LER na v2.5.2 (grelha mundial).",
        "leituras": [
            {"fonte": "Open_Meteo_ERA5_LUANDA", "operador": "Open_Meteo", "valor": None, "estado": "POR_LER",
             "pedido": "https://archive-api.open-meteo.com/v1/archive?latitude=-8.84&longitude=13.23&start_date=2015-01-01"
                       "&end_date=2024-12-31&daily=shortwave_radiation_sum&timezone=UTC",
             "nota": "o leitor é o mesmo do ERA5; nome único por cidade"},
        ],
        "o_que_nao_garante": "média do ano: não dá o pior mês nem o pior ano; uma só fonte: serve para dimensionar com folga, não para punir ninguém.",
    },
    "irradiacao/brasilia": {
        "id": "O12.irradiacao_brasilia", "versao": "1.0.0", "nome": "irradiação global horizontal em Brasília, média diária do ano",
        "formula": "leitura gravada; sol de pico (h/dia) = irradiação / G_stc; com N>=3 fontes, o consenso é a mediana das concordantes",
        "unidades": {"saida": "MJ/m2/dia"}, "unidade": "MJ/m2/dia", "plausivel": [16.0, 26.0], "etiqueta": "MEDIDO",
        "fonte": "Open-Meteo, archive API (reanálise ERA5, cobertura global), Brasília 15.79S 47.88W. "
                 "Faixa plausível ASSUMIDO [VALIDAR]. Entrou POR_LER na v2.5.2 (grelha mundial).",
        "leituras": [
            {"fonte": "Open_Meteo_ERA5_BRASILIA", "operador": "Open_Meteo", "valor": None, "estado": "POR_LER",
             "pedido": "https://archive-api.open-meteo.com/v1/archive?latitude=-15.79&longitude=-47.88&start_date=2015-01-01"
                       "&end_date=2024-12-31&daily=shortwave_radiation_sum&timezone=UTC",
             "nota": "o leitor é o mesmo do ERA5; nome único por cidade"},
        ],
        "o_que_nao_garante": "média do ano: não dá o pior mês nem o pior ano; uma só fonte: serve para dimensionar com folga, não para punir ninguém.",
    },
    "irradiacao/sao_paulo": {
        "id": "O12.irradiacao_sao_paulo", "versao": "1.0.0", "nome": "irradiação global horizontal em São Paulo, média diária do ano",
        "formula": "leitura gravada; sol de pico (h/dia) = irradiação / G_stc; com N>=3 fontes, o consenso é a mediana das concordantes",
        "unidades": {"saida": "MJ/m2/dia"}, "unidade": "MJ/m2/dia", "plausivel": [13.0, 23.0], "etiqueta": "MEDIDO",
        "fonte": "Open-Meteo, archive API (reanálise ERA5, cobertura global), São Paulo 23.55S 46.63W. "
                 "Faixa plausível ASSUMIDO [VALIDAR]. Entrou POR_LER na v2.5.2 (grelha mundial).",
        "leituras": [
            {"fonte": "Open_Meteo_ERA5_SAO_PAULO", "operador": "Open_Meteo", "valor": None, "estado": "POR_LER",
             "pedido": "https://archive-api.open-meteo.com/v1/archive?latitude=-23.55&longitude=-46.63&start_date=2015-01-01"
                       "&end_date=2024-12-31&daily=shortwave_radiation_sum&timezone=UTC",
             "nota": "o leitor é o mesmo do ERA5; nome único por cidade"},
        ],
        "o_que_nao_garante": "média do ano: não dá o pior mês nem o pior ano; uma só fonte: serve para dimensionar com folga, não para punir ninguém.",
    },
    "irradiacao/manila": {
        "id": "O12.irradiacao_manila", "versao": "1.0.0", "nome": "irradiação global horizontal em Manila, média diária do ano",
        "formula": "leitura gravada; sol de pico (h/dia) = irradiação / G_stc; com N>=3 fontes, o consenso é a mediana das concordantes",
        "unidades": {"saida": "MJ/m2/dia"}, "unidade": "MJ/m2/dia", "plausivel": [14.0, 24.0], "etiqueta": "MEDIDO",
        "fonte": "Open-Meteo, archive API (reanálise ERA5, cobertura global), Manila 14.60N 120.98E. "
                 "Faixa plausível ASSUMIDO [VALIDAR]. Entrou POR_LER na v2.5.2 (grelha mundial).",
        "leituras": [
            {"fonte": "Open_Meteo_ERA5_MANILA", "operador": "Open_Meteo", "valor": None, "estado": "POR_LER",
             "pedido": "https://archive-api.open-meteo.com/v1/archive?latitude=14.60&longitude=120.98&start_date=2015-01-01"
                       "&end_date=2024-12-31&daily=shortwave_radiation_sum&timezone=UTC",
             "nota": "o leitor é o mesmo do ERA5; nome único por cidade"},
        ],
        "o_que_nao_garante": "média do ano: não dá o pior mês nem o pior ano; uma só fonte: serve para dimensionar com folga, não para punir ninguém.",
    },
    "irradiacao/istambul": {
        "id": "O12.irradiacao_istambul", "versao": "1.0.0", "nome": "irradiação global horizontal em Istambul, média diária do ano",
        "formula": "leitura gravada; sol de pico (h/dia) = irradiação / G_stc; com N>=3 fontes, o consenso é a mediana das concordantes",
        "unidades": {"saida": "MJ/m2/dia"}, "unidade": "MJ/m2/dia", "plausivel": [10.0, 20.0], "etiqueta": "MEDIDO",
        "fonte": "Open-Meteo, archive API (reanálise ERA5, cobertura global), Istambul 41.01N 28.97E. "
                 "Faixa plausível ASSUMIDO [VALIDAR]. Entrou POR_LER na v2.5.2 (grelha mundial).",
        "leituras": [
            {"fonte": "Open_Meteo_ERA5_ISTAMBUL", "operador": "Open_Meteo", "valor": None, "estado": "POR_LER",
             "pedido": "https://archive-api.open-meteo.com/v1/archive?latitude=41.01&longitude=28.97&start_date=2015-01-01"
                       "&end_date=2024-12-31&daily=shortwave_radiation_sum&timezone=UTC",
             "nota": "o leitor é o mesmo do ERA5; nome único por cidade"},
        ],
        "o_que_nao_garante": "média do ano: não dá o pior mês nem o pior ano; uma só fonte: serve para dimensionar com folga, não para punir ninguém.",
    },
    "irradiacao/cidade_do_mexico": {
        "id": "O12.irradiacao_cidade_do_mexico", "versao": "1.0.0", "nome": "irradiação global horizontal na Cidade do México, média diária do ano",
        "formula": "leitura gravada; sol de pico (h/dia) = irradiação / G_stc; com N>=3 fontes, o consenso é a mediana das concordantes",
        "unidades": {"saida": "MJ/m2/dia"}, "unidade": "MJ/m2/dia", "plausivel": [15.0, 26.0], "etiqueta": "MEDIDO",
        "fonte": "Open-Meteo, archive API (reanálise ERA5, cobertura global), Cidade do México 19.43N 99.13W. "
                 "Faixa plausível ASSUMIDO [VALIDAR]. Entrou POR_LER na v2.5.2 (grelha mundial).",
        "leituras": [
            {"fonte": "Open_Meteo_ERA5_CIDADE_DO_MEXICO", "operador": "Open_Meteo", "valor": None, "estado": "POR_LER",
             "pedido": "https://archive-api.open-meteo.com/v1/archive?latitude=19.43&longitude=-99.13&start_date=2015-01-01"
                       "&end_date=2024-12-31&daily=shortwave_radiation_sum&timezone=UTC",
             "nota": "o leitor é o mesmo do ERA5; nome único por cidade"},
        ],
        "o_que_nao_garante": "média do ano: não dá o pior mês nem o pior ano; uma só fonte: serve para dimensionar com folga, não para punir ninguém.",
    },
    "irradiacao/mumbai": {
        "id": "O12.irradiacao_mumbai", "versao": "1.0.0", "nome": "irradiação global horizontal em Mumbai, média diária do ano",
        "formula": "leitura gravada; sol de pico (h/dia) = irradiação / G_stc; com N>=3 fontes, o consenso é a mediana das concordantes",
        "unidades": {"saida": "MJ/m2/dia"}, "unidade": "MJ/m2/dia", "plausivel": [15.0, 26.0], "etiqueta": "MEDIDO",
        "fonte": "Open-Meteo, archive API (reanálise ERA5, cobertura global), Mumbai 19.08N 72.88E. "
                 "Faixa plausível ASSUMIDO [VALIDAR]. Entrou POR_LER na v2.5.2 (grelha mundial).",
        "leituras": [
            {"fonte": "Open_Meteo_ERA5_MUMBAI", "operador": "Open_Meteo", "valor": None, "estado": "POR_LER",
             "pedido": "https://archive-api.open-meteo.com/v1/archive?latitude=19.08&longitude=72.88&start_date=2015-01-01"
                       "&end_date=2024-12-31&daily=shortwave_radiation_sum&timezone=UTC",
             "nota": "o leitor é o mesmo do ERA5; nome único por cidade"},
        ],
        "o_que_nao_garante": "média do ano: não dá o pior mês nem o pior ano; uma só fonte: serve para dimensionar com folga, não para punir ninguém.",
    },

    "remessas/alvo_ODS_10c": {
        "id": "O12.remessas_alvo_ods", "versao": "1.0.0", "nome": "alvo ONU para o custo das remessas de migrantes",
        "formula": "leitura gravada do alvo; comparação: pct_total vs alvo",
        "unidades": {"saida": "%"}, "unidade": "%", "plausivel": [0.5, 6.0], "etiqueta": "MEDIDO",
        "fonte": "ONU, ODS 10, alvo 10.c: «Até 2030, reduzir para menos de 3% os custos de transação das remessas de "
                 "migrantes e eliminar corredores com custos superiores a 5%» (sdgs.un.org/goals/goal10); lido e verificado "
                 "por 2 examinadores independentes a 21-11-2026 (exame da moeda). Entrou na v2.5.3.",
        "leituras": [
            {"fonte": "ONU_SDG10c", "operador": "ONU", "valor": 3.0, "incerteza": 0.0, "etiqueta": "MEDIDO",
             "data": "2026-11-21",
             "nota": "o alvo é MEDIDO (número declarado no texto); incerteza zero porque é declaração, não medição do mundo"},
        ],
        "o_que_nao_garante": "um alvo não é o custo real: serve de régua, não de promessa. O custo de cada corredor lê-se na fonte por corredor (POR_SELAR: base RPW por descarga oficial).",
    },
    "remessas/custo_medio_global": {
        "id": "O12.remessas_custo_medio_global", "versao": "1.0.0", "nome": "custo médio mundial de envio de remessas",
        "formula": "leitura gravada da média mundial; comparação: pct_total vs média",
        "unidades": {"saida": "%"}, "unidade": "%", "plausivel": [3.0, 12.0], "etiqueta": "MEDIDO",
        "fonte": "Banco Mundial, Remittance Prices Worldwide (relatório de setembro de 2025, dados do 3.º trimestre de 2025): "
                 "«enviar remessas custa, globalmente, em média 6,36% do montante enviado» (remittanceprices.worldbank.org); "
                 "lido e verificado por 2 examinadores independentes a 21-11-2026. Fetch CRUO do site: HTTP 403 — a resposta "
                 "crua fica POR_SELAR (rota alternativa: descarga oficial da base RPW). Entrou na v2.5.3.",
        "leituras": [
            {"fonte": "Banco_Mundial_RPW_Q3_2025", "operador": "Banco_Mundial", "valor": 6.36, "incerteza": 0.32, "etiqueta": "MEDIDO",
             "data": "2025-09-01",
             "nota": "a média é MEDIDO (número do relatório); os ±5% são ASSUMIDO (variação entre trimestres) [VALIDAR]"},
            {"fonte": "RPW_site_fetch_cru", "operador": "Banco_Mundial", "valor": None, "estado": "POR_SELAR",
             "pedido": "https://remittanceprices.worldbank.org/ (HTTP 403 na tentativa de 21-11-2026)",
             "nota": "a página recusou o fetch cru; a descarga oficial da base RPW é a rota para selar a resposta"},
        ],
        "o_que_nao_garante": "a média mundial não é o custo de nenhum corredor concreto; margens cambiais ocultas ficam FORA da média oficial (o custo real é maior — VoxDev/exame). Serve de régua, não de preço.",
    },
    "terra/circularidade_mundial_pct": {
        "id": "O12.terra_circularidade_mundial", "versao": "1.0.0", "nome": "quão circular é a economia mundial",
        "formula": "leitura gravada; comparação: MCI do produto vs média mundial",
        "unidades": {"saida": "%"}, "unidade": "%", "plausivel": [3.0, 20.0], "etiqueta": "MEDIDO",
        "fonte": "Circle Economy/Deloitte, Global Circularity Gap Report 2025: a circularidade caiu de 7,2% para 6,9% "
                 "(deloitte.com/global/en/issues/climate/global-circularity-gap.html); lido pelo enxame R2 a 21-11-2026. "
                 "O 9,1% citado de relatórios antigos (2018) está DESATUALIZADO — a régua da casa é o número mais recente.",
        "leituras": [
            {"fonte": "CGR_2025_via_Deloitte", "operador": "Circle_Economy_Deloitte", "valor": 6.9, "incerteza": 0.3, "etiqueta": "MEDIDO",
             "data": "2025-01-01", "nota": "dados de 2021 publicados em 2025; ±ASSUMIDO [VALIDAR]"},
        ],
        "o_que_nao_garante": "a circularidade média mundial não é a de nenhum produto concreto: o MCI do produto calcula-se pela fórmula P34.",
    },
    "carbono/ets_eur_tCO2e": {
        "id": "O12.carbono_ets_eur", "versao": "1.0.0", "nome": "preço do carbono na UE ETS",
        "formula": "leitura gravada; valorização: carbono (tCO2e) × preço (EUR/tCO2e)",
        "unidades": {"saida": "EUR/tCO2e"}, "unidade": "EUR/tCO2e", "plausivel": [20.0, 150.0], "etiqueta": "MEDIDO",
        "fonte": "Trading Economics, EU Carbon Permits: €81,07/tCO2e a 20-11-2026 (pico ~€92 em jan-2026); "
                 "lido pelo enxame R2 a 21-11-2026. Para pagamento real: taxa fresca do dia.",
        "leituras": [
            {"fonte": "TradingEconomics_ETS", "operador": "TradingEconomics", "valor": 81.07, "incerteza": 1.0, "etiqueta": "MEDIDO",
             "data": "2026-11-20", "nota": "preço de mercado; a incerteza cobre a variação intradia [VALIDAR]"},
        ],
        "o_que_nao_garante": "preço de mercado muda ao dia; o valor CENÁRIO de carbono não é receita garantida de ninguém.",
    },
    "terra/sobrevivencia_5anos_tropical": {
        "id": "O12.terra_sobrevivencia_5anos", "versao": "1.0.0", "nome": "sobrevivência de árvores tropicais plantadas ao fim de 5 anos",
        "formula": "leitura gravada; multiplicação: árvores plantadas × sobrevivência",
        "unidades": {"saida": "1"}, "unidade": "1", "plausivel": [0.3, 0.9], "etiqueta": "MEDIDO",
        "fonte": "Banin et al. 2022 (Phil. Trans. R. Soc. B; UK CEH, comunicado de 14-11-2022): 18% das árvores tropicais "
                 "plantadas morrem no 1.º ano; 44% ao fim de 5 anos -> ~56% sobrevivem; lido pelo enxame R2 a 21-11-2026.",
        "leituras": [
            {"fonte": "Banin_2022_UK_CEH", "operador": "UK_CEH", "valor": 0.56, "incerteza": 0.05, "etiqueta": "MEDIDO",
             "data": "2022-11-14", "nota": "o ±5% é ASSUMIDO (variação entre sítios) [VALIDAR]"},
        ],
        "o_que_nao_garante": "estudo sobre plantação TROPICAL; outras florestas e outras práticas têm outras taxas.",
    },
    "terra/custo_plantacao_ha": {
        "id": "O12.terra_custo_plantacao_ha", "versao": "1.0.0", "nome": "custo de restauração por hectare (plantação)",
        "formula": "leitura gravada; multiplicação: hectares × custo/ha",
        "unidades": {"saida": "USD/ha"}, "unidade": "USD/ha", "plausivel": [100.0, 5000.0], "etiqueta": "MEDIDO",
        "fonte": "WRI: «os custos podem exceder $1.500/ha»; plantar 23 Mha/ano ≈ $34 mil milhões/ano; regeneração assistida "
                 "por agricultores no Níger < $20/ha (wri.org/insights/can-we-restore-350-million-hectares-2030); "
                 "lido pelo enxame R2 a 21-11-2026.",
        "leituras": [
            {"fonte": "WRI_plantacao", "operador": "WRI", "valor": 1500.0, "incerteza": 500.0, "etiqueta": "MEDIDO",
             "data": "2026-11-21", "nota": "o número é um CHÃO («podem exceder»); ±ASSUMIDO [VALIDAR]; câmbio USD/EUR pelo oráculo O12"},
            {"fonte": "WRI_niger_regeneracao", "operador": "WRI", "valor": 20.0, "incerteza": 5.0, "etiqueta": "MEDIDO",
             "data": "2026-11-21", "nota": "regeneração assistida: a via BARATA; não é plantação"},
        ],
        "o_que_nao_garante": "a faixa é enorme e honesta: de <$20 (Níger) a >$1500 (plantação). O cenário escolhe a via e declara-a.",
    },
    "carbono/emissoes_globais_gtCO2_ano": {
        "id": "O12.carbono_emissoes_globais", "versao": "1.0.0", "nome": "emissões globais anuais (premissa do 4 per 1000)",
        "formula": "leitura gravada; comparação: sequestro anual do plano vs emissões anuais",
        "unidades": {"saida": "GtCO2/ano"}, "unidade": "GtCO2/ano", "plausivel": [20.0, 60.0], "etiqueta": "MEDIDO",
        "fonte": "Minasny et al. 2017 («Soil carbon 4 per mille», Geoderma; PDF HAL lido pelo enxame R2): a taxa 4‰ nasce de "
                 "8,9 Gt C/ano ÷ 2400 Gt C no solo; 8,9 Gt C × 3,667 ≈ 32,6 Gt CO2/ano (a conversão C→CO2 é aritmética do "
                 "enxame, declarada). Entrou na v2.6.2.",
        "leituras": [
            {"fonte": "Minasny_2017_premissa", "operador": "Geoderma_Minasny", "valor": 32.6, "incerteza": 1.0, "etiqueta": "MEDIDO",
             "data": "2017-01-01", "nota": "é a premissa do paper; o número actual de emissões pode divergir — [VALIDAR] com fonte mais recente"},
        ],
        "o_que_nao_garante": "a premissa do paper de 2017 não é o número de hoje: atualizar com fonte corrente antes de qualquer afirmação ao público.",
    },
    "terra/perda_florestal_2024_mha": {
        "id": "O12.terra_perda_florestal_2024", "versao": "1.0.0", "nome": "perda de cobertura arbórea em 2024 (recorde)",
        "formula": "leitura gravada; contexto para a dívida com o planeta",
        "unidades": {"saida": "Mha/ano"}, "unidade": "Mha/ano", "plausivel": [5.0, 60.0], "etiqueta": "MEDIDO",
        "fonte": "WRI/Global Forest Watch (release maio-2025, lido pelo enxame R2): 2024 = recorde, ~30 Mha de perda global "
                 "de cobertura arbórea (+5%) e 6,7 Mha de floresta primária tropical (quase o dobro de 2023); fogo ≈ 50% "
                 "da perda tropical; 2025 = 4,3 Mha (−36% vs 2024, ainda +46% vs há uma década).",
        "leituras": [
            {"fonte": "WRI_GFW_2024", "operador": "WRI_Global_Forest_Watch", "valor": 30.0, "incerteza": 1.0, "etiqueta": "MEDIDO",
             "data": "2024-12-31", "nota": "perda de COBERTURA arbórea (não é sinónimo de deflorestação permanente)"},
            {"fonte": "WRI_GFW_primaria_tropical_2024", "operador": "WRI_Global_Forest_Watch", "valor": 6.7, "incerteza": 0.3, "etiqueta": "MEDIDO",
             "data": "2024-12-31", "nota": "floresta primária tropical: o subconjunto mais crítico"},
        ],
        "o_que_nao_garante": "perda de cobertura ≠ deflorestação líquida (o GFW separa os dois; a casa separa-os também).",
    },
    "terra/bonn_challenge_mha": {
        "id": "O12.terra_bonn_challenge", "versao": "1.0.0", "nome": "Bonn Challenge: o plano mundial de restauração",
        "formula": "leitura gravada; o plano de pagamento tem nome e número",
        "unidades": {"saida": "Mha"}, "unidade": "Mha", "plausivel": [100.0, 600.0], "etiqueta": "MEDIDO",
        "fonte": "bonnchallenge.org (lido pelo enxame R2): 150 Mha até 2020 e 350 Mha até 2030; 257 Mha prometidos por "
                 "75 países (77 compromissos).",
        "leituras": [
            {"fonte": "BonnChallenge_alvo", "operador": "Bonn_Challenge_IUCN", "valor": 350.0, "incerteza": 0.0, "etiqueta": "MEDIDO",
             "data": "2026-11-21", "nota": "o alvo é um número declarado (incerteza zero)"},
            {"fonte": "BonnChallenge_prometido", "operador": "Bonn_Challenge_IUCN", "valor": 257.0, "incerteza": 0.0, "etiqueta": "MEDIDO",
             "data": "2026-11-21", "nota": "prometido ≠ entregue: a casa separa promessa de facto"},
        ],
        "o_que_nao_garante": "prometido não é restaurado: a medição de entrega é outra fonte (não localizada hoje).",
    },
    "terra/dividendo_carbono_canada_usd": {
        "id": "O12.terra_dividendo_canada", "versao": "1.0.0", "nome": "o dividendo de carbono que existiu (Canadá)",
        "formula": "leitura gravada; exemplo real de fee-and-dividend a funcionar e a terminar",
        "unidades": {"saida": "USD/ano"}, "unidade": "USD/ano", "plausivel": [500.0, 4000.0], "etiqueta": "MEDIDO",
        "fonte": "canada.ca (CRA, lido pelo enxame R2): família de 4 em Alberta recebia $450/trimestre = $1.800/ano "
                 "(base, +20% rural); o programa terminou em abril-2025 (último pagamento único $228/indivíduo em "
                 "Alberta) quando a taxa federal foi removida. Entrou na v2.6.2.",
        "leituras": [
            {"fonte": "CRA_canada", "operador": "Canada_Revenue_Agency", "valor": 1800.0, "incerteza": 0.0, "etiqueta": "MEDIDO",
             "data": "2024-01-01", "nota": "número oficial do pagador; a incerteza zero é do valor declarado"},
        ],
        "o_que_nao_garante": "o programa CANADENSE terminou (2025): é o exemplo MEDIDO de que fee-and-dividend existiu de "
                             "verdade — e de que políticas podem morrer. Não é promessa para nenhum país.",
    },
    "desperdicio/roupa_camião_por_segundo": {
        "id": "O12.desperdicio_roupa_camião", "versao": "1.0.0", "nome": "camionetas do lixo de têxteis queimados ou em aterro, por segundo",
        "formula": "leitura gravada; contexto do desperdício do sistema da roupa",
        "unidades": {"saida": "1/s"}, "unidade": "1/s", "plausivel": [0.3, 2.0], "etiqueta": "MEDIDO",
        "fonte": "Ellen MacArthur Foundation, «A New Textiles Economy» (2017), p. 37: um camião do lixo de têxteis em aterro "
                 "ou incinerado CADA SEGUNDO; PDF descarregado e lido pelo enxame C1 a 21-11-2026. Entrou na v2.6.6.",
        "leituras": [
            {"fonte": "EMF_Textiles_2017", "operador": "Ellen_MacArthur_Foundation", "valor": 1.0, "incerteza": 0.0, "etiqueta": "MEDIDO",
             "data": "2017-01-01", "nota": "número declarado no relatório (incerteza zero da declaração; o relatório cita a análise)"},
        ],
        "o_que_nao_garante": "é o número de 2017 do relatório; atualizar com fonte mais recente quando existir.",
    },
    "desperdicio/roupa_perda_apos_uso_pct": {
        "id": "O12.desperdicio_roupa_perda", "versao": "1.0.0", "nome": "fibra do sistema da roupa perdida após o uso (aterro/incineração)",
        "formula": "leitura gravada; o tamanho do buraco que a troca/reuso fecha",
        "unidades": {"saida": "%"}, "unidade": "%", "plausivel": [40.0, 95.0], "etiqueta": "MEDIDO",
        "fonte": "EMF, «A New Textiles Economy» (2017), pp. 36-37: 73% landfilled or incinerated; <1% reciclado em roupa "
                 "nova; >USD 500 mil milhões perdidos/ano por subutilização e falta de recicla; utilização caiu 36% em "
                 "15 anos; lido pelo enxame C1 a 21-11-2026.",
        "leituras": [
            {"fonte": "EMF_Textiles_2017_perda", "operador": "Ellen_MacArthur_Foundation", "valor": 73.0, "incerteza": 0.0, "etiqueta": "MEDIDO", "data": "2017-01-01", "nota": "número declarado no relatório"},
            {"fonte": "EMF_Textiles_2017_reciclado_em_roupa", "operador": "Ellen_MacArthur_Foundation", "valor": 1.0, "incerteza": 0.5, "etiqueta": "MEDIDO", "data": "2017-01-01", "nota": "<1% reciclado em roupa nova (o valor 1,0 é o TETO declarado); reciclagem pós-uso pode ser <0,1%"},
        ],
        "o_que_nao_garante": "números de 2017; a economia da roupa mudou desde então — atualizar quando houver fonte mais recente.",
    },
    "desperdicio/plastico_reciclado_pct": {
        "id": "O12.desperdicio_plastico_reciclado", "versao": "1.0.0", "nome": "plástico reciclado mundialmente",
        "formula": "leitura gravada; 9% reciclado, 19% incinerado, 50% aterro, 22% mal gerido",
        "unidades": {"saida": "%"}, "unidade": "%", "plausivel": [3.0, 40.0], "etiqueta": "MEDIDO",
        "fonte": "OCDE, Global Plastics Outlook (comunicado 22-02-2022): produção 460 Mt (2019), resíduos 353 Mt; «Only 9% "
                 "of plastic waste is recycled… Another 19% is incinerated, 50% ends up in landfill and 22% evades waste "
                 "management systems»; fuga ao ambiente: 6,1 Mt em águas. Projeção 2060: uso 1.231 Mt, resíduos 1.014 Mt, "
                 "reciclagem só 17%. Lido pelo enxame C1 a 21-11-2026.",
        "leituras": [
            {"fonte": "OCDE_GPO_2022_reciclado", "operador": "OCDE", "valor": 9.0, "incerteza": 0.5, "etiqueta": "MEDIDO", "data": "2019-12-31", "nota": "dados de 2019 publicados 2022"},
            {"fonte": "OCDE_GPO_2022_malgerido", "operador": "OCDE", "valor": 22.0, "incerteza": 0.5, "etiqueta": "MEDIDO", "data": "2019-12-31", "nota": "evade waste management systems"},
        ],
        "o_que_nao_garante": "o Tratado do Plástico da ONU FALHOU por agora (INC-5.2 Genebra terminou 15-08-2025 sem consenso — UNEP): não há política mundial selada.",
    },
    "desperdicio/ewaste_recolhido_pct": {
        "id": "O12.desperdicio_ewaste_recolhido", "versao": "1.0.0", "nome": "lixo eletrónico recolhido/reciclado formalmente",
        "formula": "leitura gravada; o tesouro que fica no chão",
        "unidades": {"saida": "%"}, "unidade": "%", "plausivel": [10.0, 60.0], "etiqueta": "MEDIDO",
        "fonte": "UNITAR/ITU, Global E-waste Monitor 2024: 62 Mt gerados em 2022 (+82% vs 2010); 22,3% recolhido/reciclado "
                 "formalmente; USD 62 mil milhões em recursos recuperáveis não recolhidos; lido pelo enxame C1 a 21-11-2026.",
        "leituras": [
            {"fonte": "GEM_2024_UNITAR", "operador": "UNITAR_ITU", "valor": 22.3, "incerteza": 0.5, "etiqueta": "MEDIDO", "data": "2022-12-31", "nota": "dados de 2022 publicados 2024"},
        ],
        "o_que_nao_garante": "a recolha formal ≠ reciclagem completa; o resto vai para fluxos informais com outros riscos.",
    },
    "terra/deposito_retorno_noruega_pct": {
        "id": "O12.terra_deposito_noruega", "versao": "1.0.0", "nome": "o que FUNCIONA: taxa de retorno do depósito de garrafas (Noruega)",
        "formula": "leitura gravada; a prova de que o sistema desenhado bem recolhe quase tudo",
        "unidades": {"saida": "%"}, "unidade": "%", "plausivel": [70.0, 100.0], "etiqueta": "MEDIDO",
        "fonte": "Infinitum, Relatório Anual 2024 (PDF descarregado e lido pelo enxame C1): «In 2024, Infinitum achieved a "
                 "93 per cent deposit return rate and a total collection rate of more than 98 per cent»; PET com média de "
                 "71% de material reciclado. Alemanha (DPG, 11-09-2022): retorno 98%, reciclagem 97,4%. E: o imposto "
                 "ambiental foi ABOLIDO quando a recolha passou de 95% — o incentivo certo apaga-se a si próprio.",
        "leituras": [
            {"fonte": "Infinitum_2024", "operador": "Infinitum_Noruega", "valor": 93.0, "incerteza": 0.0, "etiqueta": "MEDIDO", "data": "2024-12-31", "nota": "número do relatório anual da operadora"},
            {"fonte": "DPG_Alemanha_2022", "operador": "DPG_Alemanha", "valor": 98.0, "incerteza": 0.0, "etiqueta": "MEDIDO", "data": "2022-09-11", "nota": "retorno do sistema Einwegpfand"},
        ],
        "o_que_nao_garante": "garrafas ≠ têxteis ≠ eletrónica: cada sector precisa do SEU desenho de recolha.",
    },
}


def _dia_civil(iso: str) -> int:
    """Dias desde 1970-01-01 de uma data AAAA-MM-DD (calendário gregoriano), sem relógio nem biblioteca de datas."""
    a, m, d = (int(x) for x in iso.split("-"))
    a -= 1 if m <= 2 else 0
    era = a // 400
    yoe = a - era * 400
    doy = (153 * (m + (-3 if m > 2 else 9)) + 2) // 5 + d - 1
    return era * 146097 + yoe * 365 + yoe // 4 - yoe // 100 + doy - 719468


def dias_entre(de: str, ate: str) -> int:
    return _dia_civil(ate) - _dia_civil(de)


def oraculo_gravado(nome: str, sk_leitor: bytes, data_logica: Optional[str] = None, validade_dias: Optional[int] = None) -> Dict[str, Any]:
    """P12 com dados reais: sela cada leitura gravada com a chave de QUEM A LEU e passa-as pelo mesmo oráculo N>=3.
    Leitura mais velha do que `validade_dias` na data lógica fica de fora. Devolve também a leitura mais
    conservadora: a menor das leituras concordantes admitidas pelo oráculo.
    Sem conjunto concordante, devolve None; nunca recupera leituras excluídas."""
    reg = ORACULOS_GRAVADOS[nome]
    pub = ed_publica(sk_leitor).hex()
    fontes: Dict[str, Dict[str, str]] = {}
    leituras, por_ler, velhas, lidas = [], [], [], []
    elegiveis_por_fonte: Dict[str, Dict[str, Any]] = {}
    for l in reg["leituras"]:
        if l.get("valor") is None:
            por_ler.append(l["fonte"])
            continue
        lidas.append(l)
        idade = dias_entre(l["data"], data_logica) if data_logica and l.get("data") else None
        if validade_dias is not None and idade is not None and idade > validade_dias:
            velhas.append([l["fonte"], idade])
            continue
        # A última leitura elegível de cada fonte é a contabilizada pelo oráculo.
        elegiveis_por_fonte[l["fonte"]] = l
        fontes[l["fonte"]] = {"pub": pub, "operador": l["operador"]}
        d = {"fonte": l["fonte"], "valor": l["valor"], "unidade": reg["unidade"], "ref": reg["id"], "dia": 0}
        leituras.append({"dados": d, "selo": selar(d, sk_leitor)})
    o = oraculo(leituras, fontes, reg["unidade"], reg["id"])
    leituras_concordantes = [elegiveis_por_fonte[f] for f in o.get("concordantes", [])]
    conservadora = (dict(min(leituras_concordantes, key=lambda l: (float(l["valor"]), l["fonte"])))
                   if leituras_concordantes else None)
    return dict(o, lidas=len(lidas), por_ler=por_ler, desatualizadas=velhas,
                conservadora=conservadora)


def _ler_pvgis(cru: bytes) -> Tuple[float, float, Dict[str, str]]:
    meses = json.loads(cru)["outputs"]["monthly"]  # H(h)_m = kWh/m2 no plano horizontal, em cada mês de cada ano
    anos: Dict[int, List[float]] = {}
    for m in meses:
        anos.setdefault(int(m["year"]), []).append(float(m["H(h)_m"]))
    medias = [sum(v) * 3.6 / 365.25 for _, v in sorted(anos.items()) if len(v) == 12]  # MJ/m2/dia, só anos completos
    return statistics.mean(medias), (statistics.stdev(medias) if len(medias) > 1 else 0.0), {"periodo": f"{min(anos)}/{max(anos)}"}


def _ler_open_meteo(cru: bytes) -> Tuple[float, float, Dict[str, str]]:
    d = json.loads(cru)["daily"]  # shortwave_radiation_sum = MJ/m2 em cada dia
    anos: Dict[str, List[float]] = {}
    for t, x in zip(d["time"], d["shortwave_radiation_sum"]):
        if x is not None:
            anos.setdefault(t[:4], []).append(float(x))
    medias = [statistics.mean(v) for _, v in sorted(anos.items()) if len(v) >= 360]
    return statistics.mean(medias), (statistics.stdev(medias) if len(medias) > 1 else 0.0), {"periodo": d["time"][0] + "/" + d["time"][-1]}


def _ler_bce(cru: bytes) -> Tuple[float, float, Dict[str, str]]:
    import csv  # só aqui: o demo nunca passa por esta função
    import io
    obs = [(l["TIME_PERIOD"], float(l["OBS_VALUE"])) for l in csv.DictReader(io.StringIO(cru.decode("utf-8"))) if l.get("OBS_VALUE")]
    return obs[-1][1], (statistics.stdev([v for _, v in obs]) if len(obs) > 1 else 0.0), {"data": obs[-1][0]}


_LEITORES = {"PVGIS_SARAH2": _ler_pvgis, "Open_Meteo_ERA5": _ler_open_meteo, "BCE_API_SDMX": _ler_bce}
# v2.5.2 — grelha mundial: os MESMOS leitores servem todas as fontes novas (nome único por cidade/moeda,
# porque a saída do --ler-oraculos se indexa pelo nome da fonte). Nomes de variáveis com prefixo _g_
# para NÃO tocar nos nomes globais do motor (ex.: _n é o formatador de números).
for _g_cidade in ("AMESTERDAO", "LISBOA", "LUANDA", "BRASILIA", "SAO_PAULO", "MANILA", "ISTAMBUL", "CIDADE_DO_MEXICO", "MUMBAI"):
    _LEITORES["Open_Meteo_ERA5_" + _g_cidade] = _ler_open_meteo
_LEITORES["PVGIS_SARAH2_LISBOA"] = _ler_pvgis
for _g_moeda in ("BRL", "GBP", "ZAR", "TRY", "PHP", "INR", "MXN", "CNY", "PLN"):
    _LEITORES["BCE_API_SDMX_" + _g_moeda] = _ler_bce


def _baixar(url: str) -> bytes:
    import urllib.request  # só aqui: o demo nunca passa por esta função
    pedido = urllib.request.Request(url, headers={"User-Agent": "konfirmu-calc/" + VERSAO})
    with urllib.request.urlopen(pedido, timeout=30) as r:
        return r.read()


def ler_oraculos(data_leitura: str, sk_leitor: bytes, baixar: Any = None) -> Dict[str, Any]:
    """P12 com rede — FORA do demo. Lê as fontes marcadas POR_LER, guarda o sha256 da resposta crua (a evidência) e
    devolve cada leitura selada por quem a leu, pronta a gravar no cofre. A incerteza é a variação entre anos (sol)
    ou entre os últimos dias (câmbio): não inclui o erro do próprio modelo ou satélite.
    [VALIDAR] Escrito pela documentação pública das três APIs e testado com respostas de exemplo nesse formato;
    NÃO foi corrido ao vivo (a rede desta sessão não chega lá). Falha fechado: resposta que não se deixe ler, ou
    valor fora da faixa plausível declarada no cofre, fica LEITURA_FALHOU com o motivo."""
    baixar = baixar or _baixar
    saida: Dict[str, Any] = {}
    for _, reg in sorted(ORACULOS_GRAVADOS.items()):
        for l in reg["leituras"]:
            if l.get("estado") != "POR_LER":
                continue
            d: Dict[str, Any] = {"oraculo": reg["id"], "fonte": l["fonte"], "operador": l["operador"], "pedido": l["pedido"],
                                 "unidade": reg["unidade"], "lido": data_leitura}
            try:
                cru = baixar(l["pedido"])
                valor, u, quando = _LEITORES[l["fonte"]](cru)
                if not reg["plausivel"][0] <= valor <= reg["plausivel"][1]:
                    raise ValueError(f"valor {valor!r} fora da faixa plausível {reg['plausivel']}")
                d.update(quando, estado="LIDO", valor=valor, incerteza=u, etiqueta="MEDIDO", sha256_resposta=h256(cru))
            except Exception as e:  # falha fechado, e diz porquê
                d.update(estado="LEITURA_FALHOU", motivo=f"{type(e).__name__}: {e}")
            saida[l["fonte"]] = {"dados": d, "selo": selar(d, sk_leitor)}
    return saida


# -----------------------------------------------------------------------------
# 16.5 REMESSAS (P33) + REPLANTAR (P35) — v2.5.3 · o dinheiro e a terra, com fonte e selo
# -----------------------------------------------------------------------------
# P33 REMESSAS — «quanto chega mesmo?»: custo total = fixo + enviado·(taxa explícita + margem cambial),
#   em frações, com incerteza propagada. Alvo ONU ODS 10.c (<3% até 2030) e média mundial do Banco
#   Mundial RPW Q3 2025 (6,36%) gravados como MEDIDO abaixo — verificados por 2 examinadores
#   independentes no exame da moeda de 21-11-2026; o fetch CRUO do site RPW devolveu HTTP 403, por
#   isso a resposta crua fica POR_SELAR (declarado; rota alternativa: descarga oficial da base).
# P35 REPLANTAR — «vamos replantar a terra!»: CENÁRIO de custo/árvores/carbono com fatores ASSUMIDO
#   [VALIDAR] até fonte selada (enxame R2 do Maestro). CENÁRIO — visão, não previsão (limite 19).
#   Nota honesta: estas funções não passam pelo _confere/ENTRADA_DE (pipeline F1-F25); usam Grandeza
#   diretamente e declaram o que garantem. Integrar ao cofre de fichas é o passo seguinte.
# P34 (RESERVADO): indicador de circularidade (MCI do EMF) — entra na v2.5.4 com a fórmula do enxame R2.

REMESSAS_MEDIA_MUNDIAL_PCT = 6.36  # Banco Mundial RPW, Q3 2025 (verificado por 2 examinadores, 21-11-2026)
REMESSAS_ALVO_ODS_PCT = 3.0        # ONU ODS 10.c: reduzir para menos de 3% até 2030


def custo_remessa(enviado: Grandeza, taxa: Grandeza, margem: Grandeza, fixo: Grandeza) -> Dict[str, Any]:
    """P33 — o custo real de enviar `enviado` EUR. total = fixo + enviado·(taxa + margem), frações.
    Veto: valores negativos; enviado nulo; taxa+margem >= 100% (o dinheiro não desaparece assim).
    Devolve custo e % do enviado em Grandeza (incerteza propagada) + comparação com alvo e média."""
    if enviado.v <= 0:
        raise ValueError("P33 veto: enviado tem de ser positivo")
    for nome, g in (("taxa", taxa), ("margem", margem), ("fixo", fixo)):
        if g.v < 0:
            raise ValueError(f"P33 veto: {nome} negativo ({g.v})")
    if taxa.v + margem.v >= 1.0:
        raise ValueError("P33 veto: taxa+margem >= 100%")
    custo = fixo + enviado * (taxa + margem)
    pct = custo / enviado
    estado = "ACIMA_DO_ALVO_ODS" if pct.v > REMESSAS_ALVO_ODS_PCT / 100.0 else "DENTRO_DO_ALVO_ODS"
    vs = "ACIMA_DA_MEDIA" if pct.v > REMESSAS_MEDIA_MUNDIAL_PCT / 100.0 else (
        "ABAIXO_DA_MEDIA" if pct.v < REMESSAS_MEDIA_MUNDIAL_PCT / 100.0 else "NA_MEDIA")
    return {"custo": custo, "pct_do_enviado": pct, "estado": estado, "vs_media_mundial": vs,
            "alvo_ods_pct": REMESSAS_ALVO_ODS_PCT, "media_mundial_pct": REMESSAS_MEDIA_MUNDIAL_PCT}


REPLANTAR_FACTORES_ASSUMIDO = {
    "arvores_por_ha": G(1100.0, 110.0, "arvore/ha", fonte="ASSUMIDO [VALIDAR] faixa comum de plantação; sem fonte selada no cofre"),
    "sobrevivencia": G(0.56, 0.05, "1", fonte="MEDIDO: Banin et al. 2022 (UK CEH) — 44% das árvores tropicais plantadas mortas ao fim de 5 anos; ±5% ASSUMIDO [VALIDAR]"),
    "custo_ha": G(1500.0, 500.0, "USD/ha", fonte="MEDIDO: WRI — os custos de restauração podem exceder $1.500/ha; a via barata (regeneração assistida, Níger) custa <$20/ha; ±ASSUMIDO [VALIDAR]"),
    "carbono_ha_t": G(10.0, 5.0, "tCO2e/ha/ano", fonte="ASSUMIDO [VALIDAR] depende de espécie e idade; sem fonte selada no cofre"),
}


def replantar(ha: Grandeza) -> Dict[str, Any]:
    """P35 — CENÁRIO de replantação de `ha` hectares com os fatores ASSUMIDO do cofre.
    CENÁRIO — visão, não previsão (limite 19); fatores ASSUMIDO até fonte selada (F6)."""
    if ha.v <= 0:
        raise ValueError("P35 veto: hectares tem de ser positivos")
    f = REPLANTAR_FACTORES_ASSUMIDO
    return {"arvores_plantadas": ha * f["arvores_por_ha"], "arvores_vivas_esperadas": ha * f["arvores_por_ha"] * f["sobrevivencia"],
            "custo": ha * f["custo_ha"], "sequestro_ano": ha * f["carbono_ha_t"],
            "carimbo": "CENARIO", "etiqueta": "MEDIDO/ASSUMIDO"}


# -----------------------------------------------------------------------------
# 16.7 CIRCULARIDADE (P34) — v2.6.1 · a fórmula EXACTA do MCI do EMF, verificada na fonte
# -----------------------------------------------------------------------------
# O enxame R2 (21-11-2026) descarregou e leu o PDF primário do EMF/Granta («Circularity
# Indicators: An Approach to Measuring Circularity», 2015/adapt. 2019). A fórmula abaixo é a
# do documento (Eq. 2.7, 2.11, 2.14, 2.12-2.13), não uma aproximação:
#   LFI = (V + W0 + W_C/2 + W_F/2) / (2M + (W_F − W_C)/2)
#   V = M·(1−F_R) · W0 = M·(1−F_U) · W_C = M·(1−E1)·F_U · W_F = M·(1−E2)·(F_R/E2)
#   X = (L/L_av)·(U/U_av) · F(X) = 0,9/X · MCI = max(0, 1 − LFI·F(X))
# Convenção do EMF: produto totalmente linear com utilidade média -> MCI = 0,1.
# Entra no demo em D17 (exemplo numérico do R2: M=10 kg, F_R=0,5, F_U=0,8, E1=E2=0,7, X=1 -> MCI 0,58).

def mci(M: float, F_R: float, F_U: float, E1: float, E2: float, X: float = 1.0) -> float:
    """P34 — Material Circularity Index 0-1 (EMF/Granta, fonte primária verificada 21-11-2026).
    Veto: entradas fora do domínio (massas/fracções/eficiências). X por defeito = 1 (utilidade média)."""
    if M <= 0 or not (0.0 <= F_R <= 1.0) or not (0.0 <= F_U <= 1.0) or not (0.0 < E1 <= 1.0) or not (0.0 < E2 <= 1.0) or X <= 0:
        raise ValueError("P34 veto: entradas fora do domínio do MCI")
    w_c = M * (1.0 - E1) * F_U
    w_f = M * (1.0 - E2) * (F_R / E2)
    v = M * (1.0 - F_R)
    w0 = M * (1.0 - F_U)
    lfi = (v + w0 + w_c / 2.0 + w_f / 2.0) / (2.0 * M + (w_f - w_c) / 2.0)
    return max(0.0, 1.0 - lfi * (0.9 / X))


# -----------------------------------------------------------------------------
# 16.8 O ESTADO NEUTRO (v2.6.2) — o Doughnut v3, a dívida com o planeta, e o plano de pagamento
# -----------------------------------------------------------------------------
# Ordem do Maestro: «a dívida que temos com o planeta TERRA vai ser PAGA! façamos justiça!».
# A resposta do motor NÃO é um hino: é aritmética com fonte. O Doughnut v3 (DEAL, imagem
# oficial 2025, lida pelo enxame R2) dá a estrutura do ESTADO NEUTRO: dentro da fundação
# social (12 dimensões) e debaixo do teto ecológico (9 limites). Os NOMES são MEDIDO; os
# LIMIARES quantitativos ficam ASSUMIDO [VALIDAR] até o paper Nature 2025 estar acessível —
# o motor não inventa limiares. E a dívida: a perda florestal 2001-2025 (~540 Mha) implica
# ~230 Gt CO2e (derivação VIA PESQUISA do R2: 230/540 ≈ 430 t/ha — ASSUMIDO, não fonte
# primária); a via de pagamento medida hoje é a restauração (WRI) e o solo (4 per 1000).
# O motor diz a verdade incómoda: replantar sozinho NÃO paga a dívida ANUAL — é parte do
# caminho, e mostra porquê com números.

DOUGHNUT_V3 = {
    "fonte": "DEAL (doughnuteconomics.org), imagem oficial Doughnut v3 de 2025, lida pelo enxame R2 a 21-11-2026; "
             "página DEAL: 22 indicadores sociais e 13 ecológicos; agregados 2022: 6 dos 9 limites transpostos (DEAL) "
             "e 7 dos 9 (Stockholm Resilience Centre, set-2025) — DIVERGÊNCIA DECLARADA, não harmonizada",
    "teto_ecologico_9": ["climate change", "ocean acidification", "chemical pollution", "nutrient pollution",
                          "freshwater disruption", "air pollution", "land conversion", "biodiversity breakdown",
                          "ozone layer depletion"],
    "fundacao_social_12": ["food", "water", "health", "education", "income & work", "peace & justice",
                            "political voice", "social cohesion", "equality", "housing", "connectivity", "energy"],
    "o_que_nao_garante": "os limiares quantitativos por dimensão ficam ASSUMIDO [VALIDAR] (Nature 2025 paywalled); "
                         "os nomes das dimensões são os do original inglês — a tradução para as 31 línguas é "
                         "trabalho da camada de línguas, não desta fórmula.",
}


def divida_planetaria(ha_perdidos: float, ha_por_restaurar: float) -> Dict[str, Any]:
    """A dívida com o planeta, computada com honestidade total.
    - carbono já emitido pela perda: ha_perdidos × 430 tCO2e/ha (ASSUMIDO, derivação VIA
      PESQUISA do R2 — 230 Gt CO2 ÷ 540 Mha; NÃO é fonte primária, declarado);
    - custo da via de pagamento: ha_por_restaurar × 1.500 ± 500 USD/ha (MEDIDO: WRI);
    - sequestro anual se restaurado: ha_por_restaurar × 10 ± 5 tCO2e/ha/ano (ASSUMIDO, P35);
    - comparação com as emissões globais anuais (MEDIDO via Minasny 2017: 8,9 Gt C/ano
      ≈ 32,6 Gt CO2/ano — a premissa do 4 per 1000, aritmética C→CO2 ×3,667 do R2).
    CENÁRIO — visão, não previsão. O estado diz a verdade: se o sequestro anual do plano
    não cobre as emissões anuais, a moeda é essa, sem anestesia."""
    if ha_perdidos < 0 or ha_por_restaurar < 0:
        raise ValueError("veto: hectares negativos")
    f = DIVIDA_TERRA_FACTORES
    # os hectares entram COM UNIDADE: sem ela, o motor não cancela o /ha nas fórmulas
    carbono_perdido = G(ha_perdidos, 0.0, "ha") * f["carbono_por_ha_perdido"]
    custo = G(ha_por_restaurar, 0.0, "ha") * f["custo_restauracao_ha"]
    sequestro_ano = G(ha_por_restaurar, 0.0, "ha") * f["sequestro_ha_ano"]
    emissoes_leitura = next(l for l in ORACULOS_GRAVADOS["carbono/emissoes_globais_gtCO2_ano"]["leituras"]
                            if l.get("valor") is not None)
    emissoes_gtCO2_ano = float(emissoes_leitura["valor"]) * 1e9
    seq_v, seq_u = sequestro_ano.em("tCO2e/ano")
    estado = ("REPLANTAR_SOZINHO_NAO_PAGA_A_DIVIDA_ANUAL" if seq_v < emissoes_gtCO2_ano
              else "COBRE_A_DIVIDA_ANUAL_NESTE_CENARIO")
    return {"carbono_perdido_tCO2e": carbono_perdido, "custo_restauracao_usd": custo,
            "sequestro_ano_tCO2e": sequestro_ano, "emissoes_globais_tCO2e_ano": emissoes_gtCO2_ano,
            "estado": estado, "carimbo": "CENARIO",
            "o_que_nao_garante": "o carbono por hectare perdido é ASSUMIDO (derivação, não fonte primária); "
                                 "o sequestro/ha é ASSUMIDO (P35); o estado NÃO declara perdão nem pagamento "
                                 "real: computa o cenário e diz o que falta"}


DIVIDA_TERRA_FACTORES = {
    "carbono_por_ha_perdido": G(430.0, 100.0, "tCO2e/ha",
                                fonte="ASSUMIDO [VALIDAR]: derivação VIA PESQUISA do enxame R2 — ~230 Gt CO2 (2001-2025) "
                                      "÷ 540 Mha perdidos; aritmética de terceiros, não fonte primária"),
    "custo_restauracao_ha": G(1500.0, 500.0, "USD/ha", fonte="MEDIDO: WRI — os custos podem exceder $1.500/ha"),
    "sequestro_ha_ano": G(10.0, 5.0, "tCO2e/ha/ano", fonte="ASSUMIDO [VALIDAR] — herdado do P35; depende de espécie e idade"),
}


# -----------------------------------------------------------------------------
# 16.9 PARA SEMPRE (P37) — v2.6.3 · o infinito, medido com honestidade
# -----------------------------------------------------------------------------
# Ordem do Maestro: «a matemática mede o para sempre» — e o motor computa essa régua:
#   1. O «PARA SEMPRE» TERMODINÂMICO: quebrar 256 bits por força bruta clássica custa
#      ≥ 2^256 × kT·ln2 joules (Landauer 1961: apagar um bit custa kT·ln2). O motor computa
#      o número e compara-o com a energia do Sol — «na prática: nunca» é uma ARITMÉTICA, não
#      uma poesia. Limite honesto [VALIDAR]: Landauer aplica-se a computação IRREVERSÍVEL;
#      computação quântica (Grover: 2^128 operações) vive noutro regime — por isso o «para
#      sempre» real da casa é a AGILIDADE de algoritmos, não a promessa de um algoritmo eterno.
#   2. O «PARA SEMPRE» DE SHANNON: a segurança INCONDICIONAL — o Shamir 1979 sobre GF(p) já
#      no motor: qualquer k−1 partilhas revelam ZERO informação (Shannon H(X|Y)=H(X)): não é
#      «difícil de quebrar», é IMPOSSÍVEL de quebrar por matemática, para sempre, mesmo com
#      computadores quânticos. O demo prova: 2 partilhas não recuperam NADA; 3 recuperam.
#   3. A AGILIDADE: re-selar um selo antigo com a alg atual (a cadeia de custódia dos
#      ALGORITMOS começa hoje — o que a casa já fez com a rotação v1→v2).
#   4. O ARQUIVO: o pacote de séculos — bytes + raiz + receita de re-verificação (o que um
#      verificador de 2126 precisa: os bytes, o algoritmo documentado, e as âncoras externas
#      [VALIDAR: OpenTimestamps/Bitcoin e RFC 3161 — pesquisa A1 do enxame a chegar]).

K_B_J_K = 1.380649e-23          # constante de Boltzmann, J/K (SI-2019, EXATA por definição)
T_PADRAO_K = 300.0              # temperatura ambiente assumida [VALIDAR: cenário]
LUMINOSIDADE_SOL_W = 3.828e26   # IAU (luminosidade solar nominal)
VIDA_SOL_S = 3.156e17           # ~10 mil milhões de anos em segundos [VALIDAR: cenário]
MASSA_OCEANOS_KG = 1.4e21       # [VALIDAR: valor corrente comum]
J_VAPOR_AGUA_KG = 2.61e6        # aquecer 15→100°C + vaporizar (c_p ~4186 e L_v ~2.256e6) [VALIDAR]


def custo_energetico_bruteforce(bits: int, kelvin: float = T_PADRAO_K) -> Dict[str, Any]:
    """P37 — o «para sempre» termodinâmico: energia mínima (Landauer) para ITERAR 2^bits
    chaves, assumindo computação irreversível ao limite físico (cada passo apaga ≥ kT·ln2).
    Nota honesta: NÃO cobre computação quântica (regime reversível/parcial) — o «para sempre»
    real da casa é a agilidade de algoritmos (re_selar) + Shamir incondicional."""
    if bits <= 0 or kelvin > 0:
        pass
    if bits <= 0:
        raise ValueError("P37 veto: bits > 0")
    if kelvin <= 0:
        raise ValueError("P37 veto: kelvin > 0")
    kTln2 = K_B_J_K * kelvin * math.log(2)
    total_J = (2 ** bits) * kTln2  # int × float: exatidão inteira no número de chaves
    sol_vida_J = LUMINOSIDADE_SOL_W * VIDA_SOL_S
    sois = total_J / sol_vida_J
    oceanos = total_J / (MASSA_OCEANOS_KG * J_VAPOR_AGUA_KG)
    return {"bits": bits, "kT_ln2_J": kTln2, "energia_J": total_J,
            "em_vidas_do_sol": sois, "em_ebulicoes_dos_oceanos": oceanos,
            "estado": "TERMODINAMICAMENTE_IMPOSSIVEL" if sois > 1e9 else "VIÁVEL_NO_LIMITE_FÍSICO",
            "o_que_nao_garante": "assumindo computação irreversível ao limite de Landauer; quântico é outro regime (Grover: 2^(bits/2) operações) [VALIDAR]"}


def re_selar(obj: Any, selo_antigo: Dict[str, str], sk_atual: bytes, algoritmo: str = "Ed25519+SHA-256") -> Dict[str, Any]:
    """P37 — AGILIDADE de algoritmos: re-sela um objeto JÁ SELADO, gravando a linhagem
    (o hash do selo antigo fica DENTRO do selo novo). A cadeia de custódia dos algoritmos
    começa hoje: quando Ed25519 envelhecer (NIST IR 8547: deprecado 2030), o selo novo leva
    o antigo consigo — nada se perde, tudo se re-verifica."""
    if not selo_ok(obj, selo_antigo):
        raise ValueError("P37 veto: o selo antigo não confere — re-selar o que está partido é falsificar")
    linhagem = {"selo_anterior_sha256": hobj(selo_antigo), "algoritmo_anterior": selo_antigo.get("alg", "?")}
    novo = selar({"objeto_sha256": hobj(obj), "linhagem": linhagem}, sk_atual)
    return dict(novo, linhagem=linhagem, algoritmo=algoritmo)


def arquivo_para_seculos(livro: LedgerImutavel) -> Dict[str, Any]:
    """P37 — o pacote de séculos: o que um verificador de 2126 precisa para re-verificar.
    Hoje: bytes (a cadeia), raiz (a âncora), algoritmos (documentados), receita (os passos).
    [VALIDAR] A âncora externa (OpenTimestamps/Bitcoin, RFC 3161) é a camada que falta ligar
    — pesquisa A1 do enxame em curso; a casa já tem o hábito OTS nas suas entregas."""
    return {"raiz_sha256": livro.cabeca(), "blocos": len(livro.blocos),
            "algoritmos": ["SHA-256 (hash)", "Ed25519 (assinatura, NIST IR 8547: deprecado 2030)"],
            "receita_de_reverificacao": [
                "1. re-computar cada hash_atual da cadeia (SHA-256, especificação pública FIPS 180-4)",
                "2. verificar cada assinatura Ed25519 (RFC 8032) com a chave pública do notário",
                "3. se o algoritmo envelheceu: usar a receita DOCUMENTADA e re-selar com o atual (re_selar)",
                "4. confrontar a raiz com as âncoras externas [VALIDAR: OTS/Bitcoin, RFC 3161 — A1]"],
            "o_que_nao_garante": "nada é para sempre por decreto: o que é para sempre é a POSSIBILIDADE de "
                                 "re-verificar — bytes + receita + custódia redundante (Shamir 3-de-5) + âncoras"}


# -----------------------------------------------------------------------------
# 16.10 ENVELOPE KCP (P38) — v2.6.4 · o facto do Gral no formato que o MUNDO lê
# -----------------------------------------------------------------------------
# RFC 9052 (COSE, verificado por fetch hoje): Sig_structure = ["Signature1", body_protected,
#   external_aad, payload] (§4.4); COSE_Sign1 = tag CBOR 18 com [protected, unprotected,
#   payload, signature] (§4.2). RFC 9053: alg EdDSA = -8 (Tabela 2); OKP = 1; Ed25519 = crv 6.
# RFC 9943 (SCITT, jun-2026 — verificado hoje): o «Signed Statement» é um COSE_Sign1 que
#   entra num log append-only e volta como «Transparent Statement»; o Receipt (RFC 9942) é a
#   prova de Merkle de inclusão — entra quando o log PROVA/1 da casa existir de verdade [VALIDAR].
# CBOR mínimo (RFC 8949) escrito de raiz, stdlib-only: ints, bstr, tstr, listas, mapas
#   canónicos (chaves ordenadas pelos bytes codificados, §4.2.1) e tag. Sem floats, sem
#   indefinidos: o que o envelope usa é o que o codificador suporta — falha fechado.

def _cbor_cabeca(major: int, n: int) -> bytes:
    if n < 24:
        return bytes([(major << 5) | n])
    if n <= 0xFF:
        return bytes([(major << 5) | 24, n])
    if n <= 0xFFFF:
        return bytes([(major << 5) | 25]) + n.to_bytes(2, "big")
    if n <= 0xFFFFFFFF:
        return bytes([(major << 5) | 26]) + n.to_bytes(4, "big")
    return bytes([(major << 5) | 27]) + n.to_bytes(8, "big")


def cbor_encode(v: Any) -> bytes:
    if isinstance(v, bool):
        raise TypeError("P38: bool não entra neste subset CBOR (o envelope não usa verdadeiros/falsos)")
    if isinstance(v, int):
        return _cbor_cabeca(0, v) if v >= 0 else _cbor_cabeca(1, -1 - v)
    if isinstance(v, (bytes, bytearray)):
        return _cbor_cabeca(2, len(v)) + bytes(v)
    if isinstance(v, str):
        return _cbor_cabeca(3, len(v.encode("utf-8"))) + v.encode("utf-8")
    if isinstance(v, list):
        return _cbor_cabeca(4, len(v)) + b"".join(cbor_encode(x) for x in v)
    if isinstance(v, dict):
        itens = sorted(((cbor_encode(k), cbor_encode(val)) for k, val in v.items()))
        return _cbor_cabeca(5, len(itens)) + b"".join(k + val for k, val in itens)
    if isinstance(v, tuple) and len(v) == 3 and v[0] == "tag":
        return _cbor_cabeca(6, v[1]) + cbor_encode(v[2])
    raise TypeError(f"P38: tipo CBOR não suportado: {type(v).__name__}")


def _cbor_cabeca_dec(b: bytes, i: int):
    ib = b[i]
    major, info = ib >> 5, ib & 0x1F
    if info < 24:
        return major, info, i + 1
    n = {24: 1, 25: 2, 26: 4, 27: 8}.get(info)
    if n is None:
        raise ValueError("P38: CBOR indefinido/float fora do subset deste envelope")
    return major, int.from_bytes(b[i + 1:i + 1 + n], "big"), i + 1 + n


def _cbor_dec(b: bytes, i: int):
    major, n, i = _cbor_cabeca_dec(b, i)
    if major == 0:
        return n, i
    if major == 1:
        return -1 - n, i
    if major == 2:
        return bytes(b[i:i + n]), i + n
    if major == 3:
        return b[i:i + n].decode("utf-8"), i + n
    if major == 4:
        out, _i = [], i
        for _ in range(n):
            v, _i = _cbor_dec(b, _i)
            out.append(v)
        return out, _i
    if major == 5:
        out, _i = {}, i
        for _ in range(n):
            k, _i = _cbor_dec(b, _i)
            val, _i = _cbor_dec(b, _i)
            out[k] = val
        return out, _i
    if major == 6:
        inner, _i = _cbor_dec(b, i)
        return ("tag", n, inner), _i
    raise ValueError("P38: major CBOR fora do subset deste envelope")


def cbor_decode(b: bytes) -> Any:
    val, fim = _cbor_dec(b, 0)
    if fim != len(b):
        raise ValueError("P38: bytes extra após o item CBOR — não é canónico")
    return val


def envelope_cose_sign1(payload: bytes, sk: bytes) -> bytes:
    """P38 — COSE_Sign1 (RFC 9052 §4.2): o facto selado do Gral no formato internacional.
    Sig_structure (§4.4): ["Signature1", protected, external_aad vazio, payload]; assinatura
    Ed25519 (alg -8). O payload é o JSON canónico da casa — a prova continua a ser a mesma."""
    protected = cbor_encode({1: -8})
    sig_structure = cbor_encode(["Signature1", protected, b"", payload])
    sig = ed_assinar(sk, sig_structure)
    return cbor_encode(("tag", 18, [protected, {}, payload, sig]))


def envelope_cose_verify1(envelope: bytes, pub_hex: str) -> Dict[str, Any]:
    """P38 — verificação falha fechado: re-constrói a Sig_structure do envelope e verifica
    Ed25519. Qualquer byte mexido -> valido False (ou recusa estrutural com motivo)."""
    dec = cbor_decode(envelope)
    if not (isinstance(dec, tuple) and len(dec) == 3 and dec[0] == "tag" and dec[1] == 18 and isinstance(dec[2], list) and len(dec[2]) == 4):
        raise ValueError("P38: não é um COSE_Sign1 (tag 18 com 4 campos)")
    protected, unprotected, payload, sig = dec[2]
    if not isinstance(protected, bytes) or not isinstance(payload, bytes) or not isinstance(sig, bytes):
        raise ValueError("P38: campos do COSE_Sign1 com tipos errados")
    sig_structure = cbor_encode(["Signature1", protected, b"", payload])
    ok = ed_verificar(bytes.fromhex(pub_hex), sig_structure, sig)
    alg = cbor_decode(protected).get(1)
    return {"valido": ok, "alg": alg, "payload_bytes": len(payload),
            "o_que_nao_garante": "o envelope prova proveniência, não verdade (limite 15); o Receipt SCITT (RFC 9942) entra quando o log existir"}


# -----------------------------------------------------------------------------
# 16.11 TIPOLOGIA (P39) — v2.6.5 · provas imutáveis e tipos nominais, stdlib-only
# -----------------------------------------------------------------------------
# Ordem do Maestro (conversa colada: «blindagem com Tipagem Estrita para auditoria»).
# Duas correções honestas ao que foi proposto pela outra janela:
#   1. «aplicar typing ao ficheiro completo mantendo o hash canónico idêntico» é IMPOSSÍVEL:
#      mudar código muda o hash — é por isso que a casa evolui por versões; a v2.5.1 adotada
#      fica INTOCADA e a tipagem entra para as superfícies NOVAS (esta secção).
#   2. mypy é ferramenta dev-time (externa): a tipagem fica PREPARADA para mypy --strict,
#      e a IMUTABILIDADE frozen é runtime (stdlib) — verificada já no demo (D21).
# A serialização proposta pela outra janela é byte-idêntica à canon() da casa (sort_keys,
# separators, ensure_ascii=False) — não se reinventa: USA-SE a da casa. E o limite da dose
# pediátrica NÃO se escreve de memória: lê-se do cofre (FARMACOPEIA, M1, com fontes).

from dataclasses import dataclass as _dataclass
from dataclasses import FrozenInstanceError as _FrozenInstanceError
from typing import Literal as _Literal, NewType as _NewType, Final as _Final

Sha256Hex = _NewType("Sha256Hex", str)
Kilograms = _NewType("Kilograms", float)
Milligrams = _NewType("Milligrams", float)
Celsius = _NewType("Celsius", float)
VeredictoP39 = _Literal["OK", "VETO", "BLOQUEADO", "REJEITADO"]

MAX_MG_KG_FONTE: _Final[float] = 15.0  # só para tipo; o VALOR real lê-se do cofre na chamada (max_mg_kg_fonte)


def max_mg_kg_fonte() -> float:
    """P39 — o limite pediátrico lido DO COFRE no momento da chamada (nunca de memória,
    nunca hardcoded): FARMACOPEIA paracetamol_oral, faixa das 4 semanas aos 18 anos."""
    return float(FARMACOPEIA["paracetamol_oral"]["faixas"][0]["mg_por_kg"])


@_dataclass(frozen=True, slots=True)
class ProvaSelada:
    """Uma prova IMUTÁVEL: os campos não se podem mudar em memória (frozen levanta
    FrozenInstanceError). Nota honesta: frozen é raso — os objetos DENTRO dos campos não
    ficam imutáveis; a imutabilidade profunda é o JSON canónico selado: os bytes é que não mudam."""
    modulo: str
    veredicto: VeredictoP39
    motivo: str
    payload_canonico: str
    digest: Sha256Hex


def prova_selada(modulo: str, veredicto: VeredictoP39, motivo: str, dados: Dict[str, Any]) -> ProvaSelada:
    """P39 — sela uma decisão num ProvaSelada frozen, com o digest pela canon() da casa
    (a MESMA serialização de sempre: sort_keys, separators, ensure_ascii=False)."""
    corpo = {"modulo": modulo, "veredicto": veredicto, "motivo": motivo, "dados": _limpo(dados)}
    canonico = canon(corpo).decode("utf-8")
    return ProvaSelada(modulo=modulo, veredicto=veredicto, motivo=motivo,
                       payload_canonico=canonico, digest=Sha256Hex(hobj(corpo)))


def prova_dose_pediatrica(peso_kg: Kilograms, incerteza_kg: float, mg_por_kg: float) -> ProvaSelada:
    """P39 — a dose pediátrica com o VETO que JÁ EXISTE no cofre (M1, farmacopeia com fontes),
    agora devolvida como ProvaSelada imutável com tipos nominais (Kilograms/Milligrams)."""
    limite = max_mg_kg_fonte()
    dose = peso_kg * mg_por_kg
    inc = incerteza_kg * mg_por_kg
    dados = {"dose_mg": round(dose, 3), "incerteza_mg": round(inc, 3),
             "limite_mg_por_kg": limite, "fonte": "FARMACOPEIA paracetamol_oral (M1, com fontes citadas)"}
    if mg_por_kg > limite:
        return prova_selada("M1_DOSING", "VETO", f"Dose {mg_por_kg} mg/kg excede o limite da fonte ({limite} mg/kg)", dados)
    return prova_selada("M1_DOSING", "OK", f"Dentro do intervalo da fonte ({limite} mg/kg)", dados)


# -----------------------------------------------------------------------------
# 16.13 MEDIDA SELADA NA ORIGEM (P41) — v2.6.7 · energia, alimentos/água, ciência
# -----------------------------------------------------------------------------
# Ordem do Maestro (as quatro fronteiras: identidade, energia, origem, ciência). As três
# medições partilham UM primitivo, agora no motor: a leitura entra no registo NO MOMENTO
# DA CAPTURA, assinada pela CHAVE DO SENSOR, com incerteza declarada — as leituras más
# ENTRAM IGUAL (a fraude vive nos dados filtrados; a ciência reprodutível guarda tudo).
#   1. ENERGIA: cada kWh produzido/trocado selado por quem o produziu (microrredes P2P;
#      a regulação UE de comunidades de energia e os pilotos reais ficam com o enxame A3).
#   2. ALIMENTOS/ÁGUA/MINERAIS: o selo na ORIGEM (balança/sensor), não no rótulo —
#      «biológico»/«carbono zero» em papel é fácil de falsificar; um bloco hash-chained não.
#   3. CIÊNCIA: pré-selada — TODAS as medições de laboratório entram antes do artigo ser
#      escrito, incluindo as que não interessam ao autor.
#   4. IDENTIDADE (nota honesta, R5): a divulgação seletiva JÁ EXISTE na EUDI (mdoc/SD-JWT
#      com salted hashes — revela o atributo, não o documento); ZK completo é pesquisa A3 do
#      enxame — a casa NÃO inventa matemática criptográfica nova (regra: usa-se o testado).

def medida_selada(livro: LedgerImutavel, sensor: str, pub_sensor_hex: str, sk_sensor: bytes,
                  valor: Grandeza, dia: int, contexto: str) -> Dict[str, Any]:
    """P41 — a medição selada na origem. Assinatura OBRIGATÓRIA da chave do sensor sobre
    a leitura (valor + incerteza + unidade + contexto); o bloco entra na cadeia na captura.
    Falha fechado: assinatura de quem não é o sensor -> RECUSADA; a leitura má entra igual."""
    leitura = {"sensor": sensor, "contexto": contexto, "valor": valor.v, "incerteza": valor.u,
               "unidade": valor.unidade if hasattr(valor, "unidade") else "1"}
    m = canon(leitura)
    if not ed_verificar(bytes.fromhex(pub_sensor_hex), m, ed_assinar(sk_sensor, m)):
        raise ValueError("P41 veto: a assinatura do SENSOR não confere — a leitura não entra")
    bloco = livro.registar(dia, "MEDIDA_SELADA", {"leitura_sha256": hobj(leitura), "sensor": sensor, "contexto": contexto})
    envelope = envelope_cose_sign1(m, sk_sensor)
    return {"ok": True, "bloco": bloco, "leitura_sha256": hobj(leitura),
            "envelope_bytes": len(envelope), "envelope_hex": envelope.hex(),
            "aviso": "a leitura entrou na cadeia INTEIRA: as leituras más entram igual — sem filtro"}


# -----------------------------------------------------------------------------
# 16.15 ANTICRIME (P42) — v2.6.8 · a fórmula que diz QUANDO o crime deixa de pagar
# -----------------------------------------------------------------------------
# Ordem do Maestro: «fórmulas desconhecidas que acabem com os crimes ambientais, marítimos
# e a pesca!». Honestidade primeiro (a régua dos exames): NENHUMA fórmula «acaba» com o
# crime — o que a evidência mostra é: **quando a DETECÇÃO INDEPENDENTE publica, o crime cai**
# (CFC-11: emissões subiram 2014-2018 às escondidas, caíram em 2019 depois da publicação —
# UNEP/WMO 1268, verificado pelo enxame R3). E Gary Becker (1968, «Crime and Punishment:
# An Economic Approach», JPE 76(2) — fonte primária a confirmar pelo enxame A4) deu a
# aritmética: **o crime paga enquanto lucro_esperado > p_detecção × sanção**.
# O motor computa a PROBABILIDADE CRÍTICA: p* = lucro ÷ sanção.
#   - p_detecção < p*: o crime PAGA (a política é discurso);
#   - p_detecção ≥ p*: o crime DEIXA de pagar (a política é um NÚMERO).
# Números reais por sector (IUU pesca, dark fleet, crimes ambientais): enxame A4 em curso;
# os valores do demo são SINTÉTICOS e declarados como tais.

def probabilidade_critica(lucro_esperado: float, sancao: float) -> Dict[str, Any]:
    """P42 — Becker 1968 simplificado: p* = lucro_esperado ÷ sanção (sem custo de enforcement
    — o modelo completo é a pesquisa A4). Acima de p*, o crime deixa de pagar: a sanção e a
    monitorização independente tornam-se o mesmo número. Veto: sanção <= 0 (sem sanção não
    há p* — é o estado do Wörgl/Kyoto: regras sem dentes)."""
    if sancao <= 0:
        raise ValueError("P42 veto: sanção <= 0 — sem sanção não há p* (regras sem dentes)")
    if lucro_esperado < 0:
        raise ValueError("P42 veto: lucro esperado negativo")
    p = lucro_esperado / sancao
    if p > 1.0:
        estado = "SANCAO_INSUFICIENTE: nem 100% de deteção paga — subir a sanção ou atacar o lucro"
    elif p == 0.0:
        estado = "JA_SEM_LUCRO"
    else:
        estado = "FECHADO_ACIMA_DE_P*: com deteção independente >= p, o crime deixa de pagar"
    return {"p_critica": p, "lucro_esperado": lucro_esperado, "sancao": sancao, "estado": estado,
            "cfc11": "a prova do mundo: emissões de CFC-11 caíram em 2019 após a publicação da deteção independente (UNEP/WMO 1268)",
            "o_que_nao_garante": "modelo de Becker simplificado (sem custo de enforcement nem heterogeneidade); "
                                 "números reais por sector: enxame A4 em curso; nada disto «acaba» com o crime — "
                                 "computa onde ele deixa de pagar"}


# -----------------------------------------------------------------------------
# 16.16 PROVAR SEM MOSTRAR (P43) — v2.6.9 · Pedersen + o □ de Pnueli sobre traços reais
# -----------------------------------------------------------------------------
# Ordem do Maestro (a peça final do mapa: provar sem expor segredos; garantir regras no tempo).
#   1. PEDERSEN (Pedersen 1991, CRYPTO'91 — fonte primária a confirmar pelo enxame A5):
#      C = g^v · h^r mod p. ESCONDER é INCONDICIONAL (Shannon de novo: r aleatório faz C variar
#      por todo o subgrupo, sem revelar v); LIGAR é computacional (DL sobre o grupo MODP
#      2048-bit do RFC 3526, fetch hoje — g=2). O h nasce «nothing up my sleeve»: g elevado ao
#      hash público datado — ninguém (nem a casa) conhece o logaritmo. Homomórfico:
#      ΠC_i = compromisso de Σv com Σr — o ministério soma ALDEIAS SEM abrir aldeias.
#   2. O □ DE PNUELI (1977) como monitor de RUNTIME sobre traços REAIS do ledger:
#      □(premissa → consequência) verificado em cada bloco. Honesto: LTL completa (◇, 𝒰)
#      com model checking é pesquisa A5; o que o CFC-11 ensina é que a MONITORIZAÇÃO
#      contínua sobre traços reais é a sanção que funciona.
#   3. zk-STARKs completas: NÃO se inventam na casa — a pesquisa A5 identifica as
#      implementações testadas do mundo para ADOTAR (transparentes, pós-quânticas, hashes).

_P_RFC3526_HEX = (
    "FFFFFFFFFFFFFFFFC90FDAA22168C234C4C6628B80DC1CD129024E088A67CC74"
    "020BBEA63B139B22514A08798E3404DDEF9519B3CD3A431B302B0A6DF25F1437"
    "4FE1356D6D51C245E485B576625E7EC6F44C42E9A637ED6B0BFF5CB6F406B7ED"
    "EE386BFB5A899FA5AE9F24117C4B1FE649286651ECE45B3DC2007CB8A163BF05"
    "98DA48361C55D39A69163FA8FD24CF5F83655D23DCA3AD961C62F356208552BB"
    "9ED529077096966D670C354E4ABC9804F1746C08CA18217C32905E462E36CE3B"
    "E39E772C180E86039B2783A2EC07A28FB5C55DF06F4C52C9DE2BCBF695581718"
    "3995497CEA956AE515D2261898FA051015728E5A8AACAA68FFFFFFFFFFFFFFFF"
)
P_MOD: int = int(_P_RFC3526_HEX, 16)      # RFC 3526 §3, grupo MODP 2048 (fetch hoje)
P_G: int = 2                              # «The generator is: 2.»
P_H: int = pow(P_G, int(hashlib.sha256(b"konfirmu-kcp-pedersen-h-2026-11-21").hexdigest(), 16), P_MOD)


def comprometer(valor: int, r: Optional[int] = None) -> Dict[str, Any]:
    """P43 — compromisso de Pedersen: esconder INCONDICIONAL (r aleatório), ligar
    computacional (DL no grupo MODP 2048). O valor tem de ser inteiro >= 0."""
    if valor < 0:
        raise ValueError("P43 veto: valor negativo (para negativos, compromete-se a decomposição)")
    rr = secrets.randbits(256) if r is None else r
    c = (pow(P_G, valor, P_MOD) * pow(P_H, rr, P_MOD)) % P_MOD
    return {"C": c, "r": rr, "v": valor}


def abrir_compromisso(C: int, valor: int, r: int) -> bool:
    """P43 — abrir: só o (v, r) certo recompõe C. Sem o r, não se abre (computacional)."""
    return (pow(P_G, valor, P_MOD) * pow(P_H, r, P_MOD)) % P_MOD == C


def soma_cega(compromissos: List[int], total: int, r_total: int) -> Dict[str, Any]:
    """P43 — AUDITORIA CEGA: o produto dos compromissos é o compromisso da SOMA
    (homomórfico): ΣC_i = g^(Σv)·h^(Σr). O ministério verifica o TOTAL sem nunca
    abrir as aldeias individuais. Abre-se só o total (Σv, Σr) — ou nada."""
    prod = 1
    for C in compromissos:
        prod = (prod * C) % P_MOD
    aberto = abrir_compromisso(prod, total, r_total)
    return {"compromisso_da_soma": prod, "total_declarado": total, "abre_com_o_total": aberto,
            "o_que_nao_garante": "a soma homomórfica é a versão LITE da auditoria cega: abre o total; "
                                 "provas de intervalo ZK (Bulletproofs) e zk-STARKs completas são pesquisa A5 — "
                                 "a casa adota o testado, não inventa criptografia"}


def monitor_ltl_sempre(tracos: List[List[Dict[str, Any]]], nome_formula: str, premissa, consequencia) -> Dict[str, Any]:
    """P43 — o □ de Pnueli (1977) como MONITOR de runtime sobre traços REAIS do ledger:
    □(premissa → consequência) em cada bloco de cada traço. Violation = a fraude que o
    CFC-11 mostrou ser apanhável só por monitorização independente."""
    violacoes: List[Dict[str, Any]] = []
    for ti, traco in enumerate(tracos):
        for bi, bloco in enumerate(traco):
            if premissa(bloco) and not consequencia(bloco):
                violacoes.append({"traco": ti, "bloco": bi})
    return {"formula": f"□({nome_formula})", "violacoes": violacoes,
            "estado": "VERDE" if not violacoes else "VIOLADO",
            "o_que_nao_garante": "monitor de traços finitos (runtime verification); LTL completa (◇, 𝒰) com "
                                 "model checking de estados é pesquisa A5"}


# -----------------------------------------------------------------------------
# 16.6 MOEDA DO POVO (P36) — v2.6.0 · a moeda do povo, com fonte e selo
# -----------------------------------------------------------------------------
# Ordem do Maestro (21-11-2026): «a VERDADEIRA MOEDA DIGITAL DO FUTURO — a MOEDA DO POVO!
# o SANTO GRAL do sistema financeiro». Construída SOBRE a moeda da prova v0.1 da casa
# (entregas/2026-11-21-ordem-financeira-verificavel — zero forks; o nó Node v0.1 fica como
# protótipo da casa, divergência declarada, não harmonizada) e sobre a evidência do exame
# da moeda de hoje. Os princípios (evidência do enxame M1/M2 a chegar; o que ainda não tem
# fonte fica ASSUMIDO [VALIDAR]):
#   1. EMISSÃO SÓ POR ENTREGA ASSINADA — uma unidade («prova») nasce quando um bem ou
#      serviço é ENTREGADO e o RECEBEDOR assina a entrega com a sua chave. O lastro é o
#      facto, não a promessa (moeda da prova v0.1; casos WIR/Sardex: enxame M1 a confirmar).
#   2. ZERO PREMINE, ZERO RENDIMENTO — ninguém nasce com saldo; nada paga juros (não existe
#      função de juros nesta classe; por construção).
#   3. CRÉDITO MÚTUO — saldos negativos até ao teto registado da comunidade (WIR/Sardex;
#      números medidos: enxame M1; sem fonte ainda = ASSUMIDO).
#   4. CONVERSÃO POR ORÁCULO — corredores pelas taxas gravadas do BCE (v2.5.2, LIDAS ao vivo);
#      pagamento real exige taxa fresca (mesmo critério do D12); cenário usa a gravada.
#   5. GOVERNANÇA P21 — as regras mudam pela constituição executável, nunca por decreto.
#   6. O que a moeda FAZ: torna a justiça financeira MENSURÁVEL e a fraude AUTO-RELATÁVEL.
#      NÃO mede paz mundial (a paz não é um derivado financeiro — moeda da prova v0.1).
#   7. REGULAÇÃO (enxame M2 a chegar): crédito mútuo de comunidade fechada pode ficar fora
#      do âmbito do MiCA — NADA é emitido ao mundo real antes de confirmação legal e decisão
#      do proprietário. Contas do demo: SINTÉTICAS.
# Unidade: «prova» (plural provas). 1 prova = 1 entrega verificada que a comunidade aceita.

class MoedaDoPovo:
    """O SANTO GRAL do sistema financeiro segundo as regras da casa: um ledger imutável onde
    cada «prova» nasce de uma entrega assinada pelo recebedor, os saldos podem ser negativos
    até ao teto de crédito mútuo, ninguém paga juros e nada é emitido sem prova.
    O que NÃO é: dinheiro legal, promessa de valor, paz mundial. O que é: infra-estrutura de
    verdade computável para troca entre pessoas — «a fábrica é de todos; o selo é nosso»."""

    def __init__(self, livro: LedgerImutavel, teto_debito: float, dia: int = 0) -> None:
        self.livro = livro
        self.teto = float(teto_debito)
        self.dia = int(dia)
        self.saldos: Dict[str, float] = {}
        self.chaves: Dict[str, str] = {}   # quem -> pubkey hex (Ed25519)

    def registar_chave(self, quem: str, pub_hex: str) -> None:
        self.chaves[quem.lower()] = pub_hex.lower()
        self.livro.registar(self.dia, "MOEDA_CHAVE", {"quem": quem, "pub": pub_hex})

    def emitir_por_entrega(self, entrega: Dict[str, Any], sk_recebedor: bytes, quantidade: float) -> Dict[str, Any]:
        """Emissão: só nasce «prova» se o RECEBEDOR assinar a entrega (o lastro é o facto).
        Veto: recebedor sem chave registada; assinatura inválida; quantidade <= 0."""
        recebedor = str(entrega.get("recebedor", ""))
        pub = self.chaves.get(recebedor.lower())
        if not pub:
            raise ValueError("P36 veto: recebedor sem chave registada — sem identidade não há lastro")
        m = canon(entrega)
        if not ed_verificar(bytes.fromhex(pub), m, ed_assinar(sk_recebedor, m)):
            raise ValueError("P36 veto: assinatura do recebedor não confere — emissão RECUSADA")
        if quantidade <= 0:
            raise ValueError("P36 veto: quantidade <= 0")
        h = hobj(entrega)
        self.saldos[recebedor] = self.saldos.get(recebedor, 0.0) + quantidade
        bloco = self.livro.registar(self.dia, "MOEDA_EMISSAO",
                                    {"entrega_sha256": h, "recebedor": recebedor,
                                     "quantidade_prova": quantidade, "fornecido_por": str(entrega.get("quem_entregou", ""))})
        return {"ok": True, "hash": bloco, "entrega_sha256": h}

    def transferir(self, de: str, para: str, quantidade: float) -> Dict[str, Any]:
        """Crédito mútuo: o pagador pode ficar NEGATIVO até ao teto registado; para além disso, veto.
        Zero rendimento: nada se cobra, nada se paga de juros."""
        if quantidade <= 0:
            raise ValueError("P36 veto: transferência <= 0")
        saldo = self.saldos.get(de, 0.0)
        if saldo - quantidade < -self.teto:
            raise ValueError(f"P36 veto: {de} passaria o teto de crédito mútuo ({-self.teto}) — RECUSADA")
        self.saldos[de] = saldo - quantidade
        self.saldos[para] = self.saldos.get(para, 0.0) + quantidade
        bloco = self.livro.registar(self.dia, "MOEDA_TRANSFERENCIA",
                                    {"de": de, "para": para, "quantidade_prova": quantidade})
        return {"ok": True, "hash": bloco}

    def converter(self, quantidade: float, moeda: str) -> Dict[str, Any]:
        """Cenário de conversão pela taxa gravada do BCE (O12.cambio_{moeda}_por_EUR: provas por moeda).
        CENÁRIO — o pagamento real exige taxa fresca do oráculo (mesma régua do D12)."""
        reg = ORACULOS_GRAVADOS[f"cambio/{moeda}_por_EUR"]
        leitura = next(l for l in reg["leituras"] if l.get("valor") is not None)
        taxa = float(leitura["valor"])
        return {"quantidade_prova": quantidade, "moeda": moeda, "taxa_gravada": taxa,
                "data_taxa": leitura.get("data"), "valor_cenario": quantidade / taxa,
                "carimbo": "CENARIO", "aviso": "pagamento real exige taxa fresca do oráculo (validade)"}

    def justica(self) -> Dict[str, Any]:
        """Índice de justiça 0-100 (moeda da prova v0.1): zero premine, zero rendimento,
        emissão só por prova (POR CONSTRUÇÃO) + desconcentração (1 − gini) MEDIDA só quando
        há ≥2 saldos positivos — com saldos negativos (crédito mútuo) o Gini não se aplica e
        fica NAO_APLICAVEL declarado, nunca inventado."""
        positivos = sorted(v for v in self.saldos.values() if v > 0)
        if len(positivos) >= 2:
            n, total = len(positivos), sum(positivos)
            gini = (2.0 * sum((i + 1) * v for i, v in enumerate(positivos))) / (n * total) - (n + 1) / n
            desconcentracao = max(0.0, 1.0 - max(0.0, gini))
            componentes = [1.0, 1.0, 1.0, desconcentracao]
        else:
            gini, desconcentracao = None, None
            componentes = [1.0, 1.0, 1.0]
        indice = 100.0 * sum(componentes) / len(componentes)
        return {"indice_justica_0a100": indice, "gini": gini, "desconcentracao": desconcentracao,
                "saldos": dict(self.saldos),
                "o_que_nao_garante": "NAO mede paz mundial; contas de demo sintéticas; não é dinheiro legal; "
                                     "adopção/valor de mercado não estão prometidos"}

    def verificar(self) -> bool:
        return self.livro.verificar_integridade_cadeia()


# -----------------------------------------------------------------------------
# 17. MÉDICO (offline-first) — M1 DOSE COM VETO · M2 INTERAÇÃO · M3 CADEIA DE FRIO · M4 AUTENTICIDADE · M5 NÓ LOCAL
# -----------------------------------------------------------------------------
# Nada aqui receita, diagnostica ou substitui tratamento clínico. O motor confere uma decisão já tomada por alguém
# contra o teto escrito numa fonte lida, e recusa o que passa. O que não conhece, recusa (falha fechado).
# A farmacopeia tem 1 fármaco e 1 interação: é a prova do mecanismo, não é uma farmacopeia.
class VetoFarmacologico(ValueError):
    """Dose, intervalo ou combinação que a fonte escrita não deixa passar."""


FARMACOPEIA: Dict[str, Dict[str, Any]] = {
    "paracetamol_oral": {
        "id": "M1.paracetamol_oral", "versao": "1.0.0", "substancia": "paracetamol", "via": "oral",
        "formula": "dose <= 15 mg/kg · peso e <= 1000 mg; intervalo >= 4 h; tomas em 24 h <= 4; total em 24 h <= 60 mg/kg · peso e <= 4000 mg",
        "unidades": {"peso": "kg", "dose": "mg", "intervalo": "h", "saida": "mg"},
        "etiqueta": "MEDIDO",
        "fonte": "(1) Perth Children's Hospital, monografia «Paracetamol»: via oral, das 4 semanas aos 18 anos, 15 mg/kg (até 1000 mg) de "
                 "4 em 4 a 6 em 6 horas; máximo 60 mg/kg (até 4000 mg) por dia. (2) Pain and Therapy 2015 (DOI 10.1007/s40122-015-0040-z): "
                 "10 a 15 mg/kg de 4 em 4 a 6 em 6 horas, até 60 mg/kg/dia. (3) MHRA (Reino Unido): não mais de 4 tomas em 24 horas e pelo "
                 "menos 4 horas entre tomas. (4) OMS, guia de 2012 sobre dor persistente em crianças, pág. 83: os mesmos 15 mg/kg, até 1 g, "
                 "4 tomas ou 4 g em 24 horas; a OMS RETIROU esta guia a 14-06-2019 (por outras razões): fica como concordante, não como "
                 "base. Tudo lido a 20-11-2026.",
        "faixas": [
            {"nome": "das 4 semanas aos 18 anos", "idade_dias": [28, 6574], "mg_por_kg": 15.0, "teto_por_toma_mg": 1000.0,
             "intervalo_min_h": 4.0, "tomas_max_24h": 4, "mg_por_kg_dia": 60.0, "teto_24h_mg": 4000.0},
        ],
        "o_que_nao_garante": "não prescreve, não diagnostica e não substitui tratamento clínico: só recusa o que passa do teto escrito na "
                             "fonte. Recém-nascidos (menos de 28 dias) ficam de fora: a única fonte lida para eles foi retirada pela OMS. "
                             "Não conhece doença do fígado, desnutrição, nem medicamentos fora desta lista.",
    },
}
INTERACOES: Dict[str, Dict[str, Any]] = {
    "ceftriaxona_calcio_iv": {
        "id": "M2.ceftriaxona_calcio_iv", "versao": "1.0.0", "par": ["ceftriaxona", "calcio_iv"],
        "formula": "veto se idade <= 28 dias e as duas substâncias estiverem a menos de 48 h uma da outra",
        "unidades": {"idade": "dia", "afastamento": "h", "saida": "1"}, "idade_max_dias": 28, "janela_h": 48.0,
        "etiqueta": "MEDIDO",
        "fonte": "OMS, Lista Modelo de Medicamentos Essenciais, página da ceftriaxona (list.essentialmeds.org): não administrar com cálcio. "
                 "MHRA (2009): contraindicada em recém-nascidos (até 28 dias) que precisem de cálcio intravenoso. ANMF (formulário "
                 "neonatal da Australásia): nenhuma solução com cálcio nas 48 horas à volta da ceftriaxona. Lido a 20-11-2026.",
        "o_que_nao_garante": "é uma só interação; fora dos 28 dias o motor não veta, manda a combinação para revisão humana. "
                             "Não substitui tratamento clínico.",
    },
}
CADEIA_DE_FRIO: Dict[str, Any] = {
    "id": "M3.frio_2_8", "versao": "1.0.0", "nome": "cadeia de frio de vacinas",
    "formula": "guardar entre +2 e +8 °C; alarme alto: >= +8 °C durante 10 h seguidas; alarme baixo: <= −0,5 °C durante 60 min",
    "unidades": {"temperatura": "°C", "passo": "min", "saida": "1"},
    "faixa": [2.0, 8.0], "alto": {"limiar": 8.0, "minutos": 600}, "baixo": {"limiar": -0.5, "minutos": 60}, "u_sensor": 0.5,
    "etiqueta": "MEDIDO",
    "fonte": "OMS, especificações PQS para registadores de temperatura de 30 dias: vacinas entre +2 e +8 °C; alarmes a <= −0,5 °C por "
             "60 minutos e a >= +8 °C por 10 horas seguidas; exatidão do registador ± 0,5 °C. Lido a 20-11-2026 (TechNet-21 e Logistics Cluster).",
    "o_que_nao_garante": "os alarmes são os da norma dos registadores, não a estabilidade de cada vacina; quem decide sobre um lote em "
                         "revisão é uma pessoa habilitada (por exemplo, a ler o monitor do frasco). [VALIDAR] sensibilidade ao gelo por vacina.",
}


def _zona(valor: float, teto: float, teto_alto: float) -> str:
    """DENTRO se não passa o teto ao peso medido; REVISAO se só passa dentro do erro da balança; VETO se passa de certeza."""
    return "DENTRO" if valor <= teto * (1.0 + 1e-9) else "REVISAO" if valor <= teto_alto * (1.0 + 1e-9) else "VETO"


def _faixa_etaria(m: Dict[str, Any], idade_dias: int) -> Dict[str, Any]:
    f = next((x for x in m["faixas"] if x["idade_dias"][0] <= idade_dias <= x["idade_dias"][1]), None)
    if f is None:
        raise VetoFarmacologico(f"{m['substancia']}: {idade_dias} dias de idade fica fora das faixas com fonte lida "
                                f"({'; '.join(x['nome'] for x in m['faixas'])}): decide o clínico")
    return f


def dose_de_referencia(farmaco: str, idade_dias: int, peso: Grandeza) -> Grandeza:
    """M1: a conta da fonte (mg/kg × peso, com o teto por toma), com a incerteza da balança. É a norma, não é uma receita."""
    if farmaco not in FARMACOPEIA:
        raise VetoFarmacologico(f"«{farmaco}» não está na farmacopeia do cofre: recusado por defeito, decide o clínico")
    m = FARMACOPEIA[farmaco]
    f = _faixa_etaria(m, idade_dias)
    dose = G(f["mg_por_kg"], 0.0, "mg/kg", fonte=m["id"]) * peso
    return dose if dose.em("mg")[0] <= f["teto_por_toma_mg"] else G(f["teto_por_toma_mg"], 0.0, "mg", fonte=m["id"])


def verificar_toma(farmaco: str, idade_dias: int, peso: Grandeza, dose: Grandeza, intervalo: Grandeza, tomas_24h: int) -> Dict[str, Any]:
    """M1 — VETO FARMACOLÓGICO. Não receita: confere uma toma já decidida por alguém contra o teto da fonte.
    Devolve DENTRO_DO_TETO ou REVISAO_HUMANA; se passa do teto de certeza, levanta VetoFarmacologico."""
    if farmaco not in FARMACOPEIA:
        raise VetoFarmacologico(f"«{farmaco}» não está na farmacopeia do cofre: recusado por defeito, decide o clínico")
    m = FARMACOPEIA[farmaco]
    f = _faixa_etaria(m, idade_dias)
    try:
        (p, up), (d, ud), t = peso.em("kg"), dose.em("mg"), intervalo.em("h")[0]
    except TypeError as e:
        raise TypeError(f"{m['id']}: {e}") from None
    if p <= 0.0 or d <= 0.0 or tomas_24h < 1:
        raise VetoFarmacologico("peso, dose e número de tomas têm de ser positivos")
    k = REGRAS["k95_unilateral"]
    teto, teto_alto = (min(f["mg_por_kg"] * x, f["teto_por_toma_mg"]) for x in (p, p + k * up))
    dia_teto, dia_alto = (min(f["mg_por_kg_dia"] * x, f["teto_24h_mg"]) for x in (p, p + k * up))
    total = d * tomas_24h
    zona, zona_dia = _zona(d - k * ud, teto, teto_alto), _zona(total, dia_teto, dia_alto)
    if zona == "DENTRO" and _zona(d, teto, teto_alto) != "DENTRO":
        zona = "REVISAO"  # a dose escrita passa o teto; só o erro de a medir a punha dentro
    if zona == "VETO":
        raise VetoFarmacologico(f"{m['substancia']} {_num(d)} mg para {_num(p)} kg = {_n(d / p, 1)} mg/kg: passa em {_num(d - teto)} mg o teto de "
                                f"{_num(teto)} mg ({_num(f['mg_por_kg'])} mg/kg, no máximo {_num(f['teto_por_toma_mg'])} mg por toma)"
                                + (f"; é {_n(d / teto, 1)} vezes o teto" if d >= 1.5 * teto else ""))
    if t < f["intervalo_min_h"]:
        raise VetoFarmacologico(f"{m['substancia']}: intervalo de {_num(t)} h entre tomas; a fonte pede pelo menos {_num(f['intervalo_min_h'])} h")
    if tomas_24h > f["tomas_max_24h"]:
        raise VetoFarmacologico(f"{m['substancia']}: {tomas_24h} tomas em 24 h; a fonte admite no máximo {f['tomas_max_24h']}")
    if zona_dia == "VETO":
        raise VetoFarmacologico(f"{m['substancia']}: {_num(total)} mg em 24 h; o teto do dia é {_num(dia_teto)} mg "
                                f"({_num(f['mg_por_kg_dia'])} mg/kg, no máximo {_num(f['teto_24h_mg'])} mg)")
    estado = "DENTRO_DO_TETO" if zona == zona_dia == "DENTRO" else "REVISAO_HUMANA"
    return {"estado": estado, "norma": m["id"] + "@" + m["versao"], "faixa": f["nome"], "dose_mg": d, "mg_por_kg": d / p,
            "teto_mg": teto, "teto_24h_mg": dia_teto, "total_24h_mg": total}


def verificar_plano(idade_dias: int, peso: Grandeza, linhas: Sequence[Dict[str, Any]]) -> Dict[str, Any]:
    """M1 + M2 sobre o plano inteiro de um doente. Cada linha: {produto, farmaco (chave da farmacopeia) ou substancia,
    dose, intervalo, tomas_24h, hora}. Nunca levanta: quem trata do doente precisa da lista toda de uma vez.
    SEM_VETO · REVISAO_HUMANA · VETADO, com cada veto e a norma que o sustenta."""
    vetos: List[Dict[str, str]] = []
    revisoes: List[List[str]] = []
    por_farmaco: Dict[str, List[Dict[str, Any]]] = {}
    substancias: Dict[str, List[float]] = {}
    for l in linhas:
        far = l.get("farmaco")
        if far in FARMACOPEIA:
            sub = FARMACOPEIA[far]["substancia"]
            por_farmaco.setdefault(far, []).append(l)
            try:
                r = verificar_toma(far, idade_dias, peso, l["dose"], l["intervalo"], l["tomas_24h"])
                if r["estado"] != "DENTRO_DO_TETO":
                    revisoes.append([str(l.get("produto")), r["estado"]])
            except VetoFarmacologico as e:
                vetos.append({"norma": FARMACOPEIA[far]["id"], "produto": str(l.get("produto")), "motivo": str(e)})
            except (KeyError, TypeError, AttributeError) as e:  # linha que não se deixa ler (falta um campo, unidade errada): não passa
                vetos.append({"norma": FARMACOPEIA[far]["id"], "produto": str(l.get("produto")), "motivo": f"linha ilegível: {e}"})
        else:
            sub = str(l.get("substancia"))
            revisoes.append([str(l.get("produto")), "FORA_DA_FARMACOPEIA"])  # dose que o cofre não sabe conferir não aprova
        substancias.setdefault(sub, []).append(float(l.get("hora", 0.0)))
    for far, ls in sorted(por_farmaco.items()):  # a mesma substância em vários produtos: soma-se o dia inteiro
        m = FARMACOPEIA[far]
        f = next((x for x in m["faixas"] if x["idade_dias"][0] <= idade_dias <= x["idade_dias"][1]), None)
        if len(ls) > 1 and f is not None and not any(v["norma"] == m["id"] and v["motivo"].startswith("linha ilegível") for v in vetos):
            p, up = peso.em("kg")
            total = sum(x["dose"].em("mg")[0] * x["tomas_24h"] for x in ls)
            teto, alto = (min(f["mg_por_kg_dia"] * x, f["teto_24h_mg"]) for x in (p, p + REGRAS["k95_unilateral"] * up))
            if _zona(total, teto, alto) == "VETO":
                vetos.append({"norma": m["id"], "produto": " + ".join(str(x.get("produto")) for x in ls),
                              "motivo": f"a mesma substância ({m['substancia']}) em {len(ls)} produtos: {_num(total)} mg em 24 h; "
                                        f"o teto do dia é {_num(teto)} mg"})
    for i in sorted(INTERACOES.values(), key=lambda x: x["id"]):
        a, b = substancias.get(i["par"][0]), substancias.get(i["par"][1])
        if a and b:
            perto = any(abs(x - y) < i["janela_h"] for x in a for y in b)
            if idade_dias <= i["idade_max_dias"] and perto:
                vetos.append({"norma": i["id"], "produto": " + ".join(i["par"]),
                              "motivo": f"{i['par'][0]} e {i['par'][1]} a menos de {_num(i['janela_h'])} h, em doente com {idade_dias} dias de idade"})
            else:
                revisoes.append([" + ".join(i["par"]), "INTERACAO_CONHECIDA_FORA_DA_REGRA_DE_VETO"])
    return {"estado": "VETADO" if vetos else "REVISAO_HUMANA" if revisoes else "SEM_VETO", "vetos": vetos, "revisoes": sorted(revisoes)}


def avaliar_frio(registo: Dict[str, Any], sensores: Dict[str, str], sensivel_ao_gelo: bool = True) -> Dict[str, Any]:
    """M3 — CADEIA DE FRIO. Lê um registo de temperaturas SELADO pelo sensor e aplica os dois alarmes da norma.
    Medicamento morto = bloqueio. Quando a diferença cabe no erro do sensor (± 0,5 °C), não decide: chama uma pessoa."""
    c = CADEIA_DE_FRIO
    d = registo.get("dados", {}) if isinstance(registo, dict) else {}
    if d.get("sensor") not in sensores or not selo_ok(d, registo.get("selo", {}), {sensores[d["sensor"]]}):
        return {"estado": "BLOQUEADA_REGISTO_SEM_SELO", "lote": str(d.get("lote"))}
    if d.get("unidade") != "°C" or not isinstance(d.get("passo_min"), int) or d["passo_min"] <= 0 or not d.get("temperaturas"):
        return {"estado": "BLOQUEADA_REGISTO_ILEGIVEL", "lote": str(d.get("lote"))}  # graus Fahrenheit lidos como Celsius matam
    ts, passo, u = d["temperaturas"], d["passo_min"], c["u_sensor"]

    def serie(cond: Any) -> int:  # minutos da série mais longa de leituras seguidas que cumprem a condição
        melhor = atual = 0
        for t in ts:
            atual = atual + 1 if t is not None and cond(t) else 0
            melhor = max(melhor, atual)
        return melhor * passo

    acima, abaixo = serie(lambda t: t >= c["alto"]["limiar"]), serie(lambda t: t <= c["baixo"]["limiar"])
    acima_talvez, abaixo_talvez = serie(lambda t: t + u >= c["alto"]["limiar"]), serie(lambda t: t - u <= c["baixo"]["limiar"])
    lidas = [t for t in ts if t is not None]
    fora = sum(1 for t in lidas if not c["faixa"][0] <= t <= c["faixa"][1]) * passo
    if abaixo >= c["baixo"]["minutos"] and sensivel_ao_gelo:
        estado = "BLOQUEADA_CONGELOU"
    elif acima >= c["alto"]["minutos"]:
        estado = "BLOQUEADA_CALOR"
    elif len(lidas) != len(ts):
        estado = "REVISAO_HUMANA_REGISTO_COM_FALHAS"  # sem leitura não há prova de frio
    elif (abaixo_talvez >= c["baixo"]["minutos"] and sensivel_ao_gelo) or acima_talvez >= c["alto"]["minutos"]:
        estado = "REVISAO_HUMANA_NO_LIMITE_DO_SENSOR"
    else:
        estado = "APTA_COM_EXCURSAO_CURTA" if fora else "APTA"
    return {"estado": estado, "lote": str(d.get("lote")), "minutos_acima": acima, "minutos_abaixo": abaixo, "minutos_fora": fora,
            "maxima": max(lidas) if lidas else None, "minima": min(lidas) if lidas else None}


def _folha(serie: str) -> str:
    return h256(b"\x00" + serie.encode("utf-8"))  # folha e nó levam prefixos diferentes: uma folha nunca passa por nó


def _no(a: str, b: str) -> str:
    return h256(b"\x01" + bytes.fromhex(a) + bytes.fromhex(b))


def _merkle_niveis(series: Sequence[str]) -> List[List[str]]:
    nivel = [_folha(s) for s in series]
    niveis = [nivel]
    while len(nivel) > 1:
        if len(nivel) % 2:
            nivel = nivel + [nivel[-1]]
            niveis[-1] = nivel
        nivel = [_no(a, b) for a, b in zip(nivel[::2], nivel[1::2])]
        niveis.append(nivel)
    return niveis


def merkle_raiz(series: Sequence[str]) -> str:
    return _merkle_niveis(series)[-1][0] if series else h256(b"")


def merkle_prova(series: Sequence[str], i: int) -> List[List[str]]:
    """O caminho da série i até à raiz: em cada nível, o lado (E ou D) e o hash do irmão."""
    prova = []
    for nivel in _merkle_niveis(series)[:-1]:
        prova.append(["E" if i % 2 else "D", nivel[i ^ 1]])
        i //= 2
    return prova


def merkle_confere(serie: str, prova: Sequence[Sequence[str]], raiz: str) -> bool:
    try:
        h = _folha(serie)
        for lado, irmao in prova:
            h = _no(irmao, h) if lado == "E" else _no(h, irmao)
        return h == raiz
    except (TypeError, ValueError):
        return False


def fabricar_lote(fabricante: str, sk: bytes, produto: str, substancia: str, lote: str, series: Sequence[str], validade_dia: int,
                  cadeia_de_frio: bool = False) -> Dict[str, Any]:
    """M4: o fabricante sela o lote. As séries das embalagens não vão no selo: vai a raiz de Merkle delas."""
    dados = {"fabricante": fabricante, "produto": produto, "substancia": substancia, "lote": lote, "validade_dia": validade_dia,
             "cadeia_de_frio": cadeia_de_frio, "n_series": len(series), "raiz_series": merkle_raiz(series)}
    return {"dados": dados, "selo": selar(dados, sk)}


def passar_custodia(manifesto: Dict[str, Any], anterior: Optional[Dict[str, Any]], de: str, sk_de: bytes, para: str, dia: int) -> Dict[str, Any]:
    """M4: quem entrega sela o elo, que aponta para o elo anterior (ou para o selo do lote, se for o primeiro)."""
    dados = {"lote": manifesto["selo"]["hash"], "de": de, "para": para, "dia": dia,
             "anterior": anterior["selo"]["hash"] if anterior else manifesto["selo"]["hash"]}
    return {"dados": dados, "selo": selar(dados, sk_de)}


def autenticar(emb: Any, fabricantes: Dict[str, str], agentes: Dict[str, str], destino: str, dia: int) -> Tuple[str, str]:
    """M4 — AUTENTICIDADE PELO HASH DA CADEIA. emb = {serie, prova, manifesto, cadeia}.
    Devolve (AUTENTICO, '') ou (NAO_AUTENTICADO, motivo). «Não autenticado» diz que a origem não se provou; não diz quem errou."""
    nao = "NAO_AUTENTICADO"
    try:
        m = emb["manifesto"]
        d, hm = m["dados"], m["selo"]["hash"]
        if d.get("fabricante") not in fabricantes:
            return nao, "FABRICANTE_NAO_REGISTADO"
        if not selo_ok(d, m["selo"], {fabricantes[d["fabricante"]]}):
            return nao, "SELO_DO_LOTE_INVALIDO"
        if not isinstance(emb.get("serie"), str) or not merkle_confere(emb["serie"], emb.get("prova", []), d["raiz_series"]):
            return nao, "SERIE_FORA_DO_LOTE"
        dono, anterior = d["fabricante"], hm
        for elo in emb.get("cadeia", []):
            e = elo["dados"]
            if (e.get("lote") != hm or e.get("de") != dono or e.get("anterior") != anterior or dono not in agentes
                    or not selo_ok(e, elo["selo"], {agentes[dono]})):
                return nao, "CADEIA_PARTIDA"
            dono, anterior = e["para"], elo["selo"]["hash"]
        if dono != destino:
            return nao, "CADEIA_PARTIDA"
        if dia > d["validade_dia"]:
            return nao, "VALIDADE_PASSADA"
        return "AUTENTICO", ""
    except (KeyError, TypeError, ValueError, AttributeError):
        return nao, "EMBALAGEM_ILEGIVEL"


def sync_exportar(livro: LedgerImutavel, desde: int, sk: bytes) -> Dict[str, Any]:
    """M5: o nó exporta os blocos a partir de `desde`, num pacote selado com a sua chave."""
    dados = {"no": livro.pub, "desde": desde, "anterior": livro.blocos[desde - 1]["hash_atual"] if desde else "0" * 64,
             "blocos": livro.blocos[desde:]}
    return {"dados": dados, "selo": selar(dados, sk)}


class Replica:
    """M5 — o lado central: guarda uma cópia CONFERIDA da ledger de cada nó. Não confia em ninguém:
    confere o selo do pacote, a continuidade com o que já tem e cada bloco (hash e assinatura do nó)."""

    def __init__(self, nos: Sequence[str]) -> None:
        self.copias: Dict[str, List[Dict[str, Any]]] = {pub: [] for pub in nos}

    def importar(self, pacote: Any) -> Tuple[str, int]:
        try:
            d = pacote["dados"]
            pub, desde, blocos = d["no"], d["desde"], d["blocos"]
            if pub not in self.copias or not selo_ok(d, pacote["selo"], {pub}):
                return "RECUSADO_SELO_INVALIDO", 0
            tenho = self.copias[pub]
            if not isinstance(desde, int) or desde < 0 or desde > len(tenho):
                return "RECUSADO_FALTAM_BLOCOS", 0
            cabeca = tenho[desde - 1]["hash_atual"] if desde else "0" * 64
            comuns = len(tenho) - desde
            sobre = min(comuns, len(blocos))
            if d["anterior"] != cabeca or blocos[:sobre] != tenho[desde:desde + sobre]:
                return "RECUSADO_HISTORIA_DIVERGENTE", 0  # o nó reescreveu o passado: não entra, e fica à vista
            novos = blocos[comuns:]
            if not conferir_blocos(novos, pub, tenho[-1]["hash_atual"] if tenho else "0" * 64, len(tenho)):
                return "RECUSADO_CADEIA_INVALIDA", 0
            tenho.extend(novos)
            return ("SINCRONIZADO" if novos else "JA_SINCRONIZADO"), len(novos)
        except (KeyError, TypeError, ValueError, AttributeError, IndexError):
            return "RECUSADO_PACOTE_ILEGIVEL", 0


class Posto:
    """M5 — nó local-first: o posto de saúde trabalha sem rede, na sua própria ledger; quando há rede exporta um pacote
    selado. Junta M1 a M4: confere planos de medicação, lê registos de frio, autentica e dispensa embalagens."""

    def __init__(self, nome: str, sk: bytes, fabricantes: Dict[str, str], agentes: Dict[str, str], sensores: Dict[str, str],
                 responsaveis: Dict[str, str]) -> None:
        self.nome, self.sk, self.livro = nome, sk, LedgerImutavel(sk)
        self.fabricantes, self.agentes, self.sensores, self.responsaveis = dict(fabricantes), dict(agentes), dict(sensores), dict(responsaveis)
        self.frio_apto: Dict[str, str] = {}    # hash do lote -> último estado apto, com registo selado
        self.bloqueados: Dict[str, str] = {}   # hash do lote -> porque não sai
        self.dispensadas: Dict[str, int] = {}  # série -> dia em que saiu

    def plano(self, idade_dias: int, peso: Grandeza, linhas: Sequence[Dict[str, Any]], dia: int) -> Dict[str, Any]:
        r = verificar_plano(idade_dias, peso, linhas)
        return responder(self.livro, dia, r["estado"], {"idade_dias": idade_dias, "peso": peso, "linhas": list(linhas)},
                         {"farmacopeia": FARMACOPEIA, "interacoes": INTERACOES}, vetos=r["vetos"], revisoes=r["revisoes"])

    def frio(self, registo: Dict[str, Any], dia: int, sensivel_ao_gelo: bool = True) -> Dict[str, Any]:
        a = avaliar_frio(registo, self.sensores, sensivel_ao_gelo)
        if a["estado"].startswith("APTA"):
            self.frio_apto.setdefault(a["lote"], a["estado"])
        elif a["estado"] not in ("BLOQUEADA_REGISTO_SEM_SELO", "BLOQUEADA_REGISTO_ILEGIVEL"):
            self.bloqueados[a["lote"]] = a["estado"]  # um registo sem selo não bloqueia lote nenhum: só não prova nada
        return responder(self.livro, dia, a["estado"], hobj(registo), CADEIA_DE_FRIO, **{k: v for k, v in a.items() if k != "estado"})

    def rever_lote(self, lote: str, apto: bool, quem: str, selo: Dict[str, Any], dia: int) -> Dict[str, Any]:
        """A decisão humana sobre um lote em REVISAO_HUMANA. Um lote BLOQUEADA_* (morto) não se desbloqueia aqui."""
        dados = {"lote": lote, "apto": apto, "dia": dia}
        if quem not in self.responsaveis or not selo_ok(dados, selo, {self.responsaveis[quem]}):
            estado = "RECUSADO_ASSINATURA_DO_RESPONSAVEL"
        elif not self.bloqueados.get(lote, "").startswith("REVISAO_HUMANA"):
            estado = "RECUSADO_LOTE_NAO_ESTA_EM_REVISAO"
        elif apto:
            del self.bloqueados[lote]
            self.frio_apto[lote] = estado = "APTA_POR_DECISAO_HUMANA"
        else:
            self.bloqueados[lote] = estado = "BLOQUEADA_POR_DECISAO_HUMANA"
        return responder(self.livro, dia, estado, dados, CADEIA_DE_FRIO, lote=lote, quem=str(quem))

    def dispensar(self, emb: Any, dia: int) -> Dict[str, Any]:
        estado, motivo = autenticar(emb, self.fabricantes, self.agentes, self.nome, dia)
        m = emb.get("manifesto", {}) if isinstance(emb, dict) else {}
        lote = str(m.get("selo", {}).get("hash", "")) if isinstance(m, dict) else ""
        serie = str(emb.get("serie")) if isinstance(emb, dict) else ""
        if estado != "AUTENTICO":
            final = "RECUSADO_NAO_AUTENTICADO"
        elif serie in self.dispensadas:
            final, motivo = "RECUSADO_NAO_AUTENTICADO", "SERIE_JA_DISPENSADA"  # a mesma série não sai duas vezes
        elif lote in self.bloqueados:
            final, motivo = "RECUSADO_LOTE_BLOQUEADO", self.bloqueados[lote]
        elif m["dados"].get("cadeia_de_frio") and lote not in self.frio_apto:
            final, motivo = "RECUSADO_SEM_PROVA_DE_FRIO", "SEM_REGISTO_DE_FRIO_APTO"
        else:
            self.dispensadas[serie] = dia
            final = "DISPENSADO"
        return responder(self.livro, dia, final, {"serie": serie, "lote": lote, "dia": dia},
                         {"autenticidade": "M4", "frio": CADEIA_DE_FRIO["id"] + "@" + CADEIA_DE_FRIO["versao"]}, serie=serie, motivo=motivo)


# -----------------------------------------------------------------------------
# 18. P15 a P19 — PONTO NEUTRAL, SELO, RASTRO VITAL, PREVENÇÃO E VETO ↔ ESCROW
# -----------------------------------------------------------------------------
class VetoBiofisico(ValueError):
    """Pressão sobre a terra, a água ou os animais acima do teto, com 95% de confiança.
    Não se compensa com conforto nem com dinheiro."""


# [VALIDAR] Os limiares do piso e do teto são ASSUMIDO: escritos de memória, não relidos na fonte a 20-11-2026.
FORMULAS_15: Dict[str, Dict[str, Any]] = {
    "F15.1": {"id": "F15.1", "versao": "1.0.0", "nome": "piso humano",
              "formula": "H = média geométrica de min(1, fornecido_i / necessário_i)",
              "unidades": {"agua": "L/pessoa/dia", "alimentacao": "kcal/pessoa/dia", "energia": "kWh/pessoa/dia", "saude": "1", "saida": "1"},
              "necessario": {"agua": 50.0, "alimentacao": 2100.0, "energia": 0.20, "saude": 0.90},
              "etiqueta": "ASSUMIDO",
              "fonte": "água: 50 L por pessoa e dia (o fundo da faixa de 50 a 100 L atribuída à OMS); alimentação: 2100 kcal por pessoa e dia "
                       "(referência humanitária); energia: 0,20 kWh por pessoa e dia (a do cenário D6); saúde: 90% das pessoas com "
                       "cuidados básicos ao alcance. Tudo [VALIDAR]",
              "o_que_nao_garante": "quatro necessidades não são uma vida; a média esconde quem fica abaixo dela"},
    "F15.2": {"id": "F15.2", "versao": "1.0.0", "nome": "teto ecológico-animal",
              "formula": "E = média geométrica de min(1, teto_j / pressão_j); pressão acima do teto com 95% de confiança = veto",
              "unidades": {"carbono": "tCO2e/pessoa/ano", "agua_captada": "1", "habitat_ocupado": "1", "captura_animal": "1", "saida": "1"},
              "teto": {"carbono": 2.0, "agua_captada": 0.40, "habitat_ocupado": 0.70, "captura_animal": 1.0},
              "etiqueta": "ASSUMIDO",
              "fonte": "carbono: ordem de grandeza de 2 tCO2e por pessoa e ano; água captada: até 40% da água renovável; habitat ocupado: "
                       "até 70% (30% fica natural); captura animal (pesca, caça, pasto): até 1 vez o que a natureza repõe. Tudo [VALIDAR]",
              "o_que_nao_garante": "não mede sofrimento animal, poluição química nem a biodiversidade espécie a espécie"},
    "F15.3": {"id": "F15.3", "versao": "1.0.0", "nome": "ponto neutral",
              "formula": "N_eq = H · E, entre 0 e 1; selo pelo pior caso a 95%: BRONZE >= 0,50 · PRATA >= 0,70 · OURO >= 0,85",
              "unidades": {"H": "1", "E": "1", "saida": "1"}, "selos": {"BRONZE": 0.50, "PRATA": 0.70, "OURO": 0.85},
              "etiqueta": "ASSUMIDO", "fonte": "forma e limiares escolhidos nesta v2.2 [VALIDAR]",
              "o_que_nao_garante": "o ponto neutral é direcção de equilíbrio, não milagre"},
    "F-HARMONIA": {"id": "F-HARMONIA", "versao": "1.0.0", "nome": "prevenção",
                   "formula": "evitados = casos · fração_evitável · adesão",
                   "unidades": {"casos": "caso", "fracao_evitavel": "1", "adesao": "1", "saida": "caso"},
                   "fracao_evitavel": {"minimo": 0.30, "maximo": 0.50}, "etiqueta": "ASSUMIDO",
                   "fonte": "fração evitável: OMS, «Preventing cancer» (who.int/activities/preventing-cancer): entre 30 e 50% de todos os "
                            "casos de cancro são evitáveis; lido a 20-11-2026. A forma da conta e a adesão são escolha desta v2.2 [VALIDAR]",
                   "o_que_nao_garante": FRASES_OBRIGATORIAS["prevencao"] + " [VALIDAR] A OMS diz que 30 a 50% de TODOS os casos de cancro são "
                                        "evitáveis; não diz que alguma coisa «previne 30 a 50%». Nada aqui mede que o ponto neutral evita cancros."},
}
# P18 — teoria debatida = AS DUAS no cofre, as duas seladas. O motor faz a conta por cada uma e não escolhe.
DEBATES: Dict[str, Dict[str, Any]] = {
    "radiacao_em_dose_baixa": {
        "pergunta": "uma dose baixa de radiação soma risco de cancro em linha reta, ou só acima de um limiar?", "estado": "DEBATIDO",
        "teorias": [
            {"id": "T18.LNT", "versao": "1.0.0", "nome": "linear sem limiar", "formula": "casos = pessoas · dose · r",
             "unidades": {"pessoas": "pessoa", "dose": "Sv", "saida": "caso"}, "risco_por_Sv": 0.055, "limiar_Sv": 0.0, "etiqueta": "ASSUMIDO",
             "fonte": "coeficiente nominal de 5,5% por sievert, atribuído à ICRP (Publicação 103); de memória, não relido a 20-11-2026 [VALIDAR]",
             "o_que_nao_garante": "abaixo de cerca de 100 mSv é extrapolação, não medição direta; conta casos numa população, não o risco de uma pessoa"},
            {"id": "T18.LIMIAR", "versao": "1.0.0", "nome": "com limiar", "formula": "casos = pessoas · max(0, dose − limiar) · r",
             "unidades": {"pessoas": "pessoa", "dose": "Sv", "saida": "caso"}, "risco_por_Sv": 0.055, "limiar_Sv": 0.100, "etiqueta": "ASSUMIDO",
             "fonte": "limiar de 100 mSv, escolhido para o exemplo; de memória, não relido a 20-11-2026 [VALIDAR]",
             "o_que_nao_garante": "se o limiar existe, e onde fica, é justamente o que está em debate"},
        ],
    },
}


def ponto_neutral(medicoes: Dict[str, Dict[str, Any]]) -> Dict[str, Any]:
    """P15 — PONTO NEUTRAL. medicoes = {indicador: {valor, incerteza, unidade, ...}}: os 4 do piso humano e os 4 do teto.
    Devolve H, E e N_eq com incerteza, o pior caso a 95% e o nível do selo. Levanta VetoBiofisico se alguma pressão
    passar o teto com 95% de confiança: esse veto não se compensa com um piso humano alto."""
    f1, f2, f3 = FORMULAS_15["F15.1"], FORMULAS_15["F15.2"], FORMULAS_15["F15.3"]
    k95 = REGRAS["k95_unilateral"]
    g: Dict[str, Grandeza] = {}
    for f, chaves in ((f1, f1["necessario"]), (f2, f2["teto"])):
        for k in sorted(chaves):
            if k not in medicoes:
                raise KeyError(f"falta medir «{k}»: sem todas as medições não há ponto neutral")
            m = medicoes[k]
            g[k] = G(m["valor"], m.get("incerteza", 0.0), m["unidade"], fonte=("medicao", k))
            try:
                g[k].em(f["unidades"][k])
            except TypeError as e:
                raise TypeError(f"{f['id']}.{k}: {e}") from None
            if g[k].v < 0.0:
                raise ValueError(f"{f['id']}.{k}: uma medição não pode ser negativa")
    estouros = []
    for k, teto in sorted(f2["teto"].items()):
        baixo, _ = faixa95(g[k], f2["unidades"][k])
        if baixo > teto:
            v, u = g[k].em(f2["unidades"][k])
            estouros.append(f"{k} {_num(v, 3)} ± {_num(u, 2)} (teto {_num(teto, 3)})")
    if estouros:
        raise VetoBiofisico("pressão acima do teto ecológico-animal, a 95%: " + "; ".join(estouros))

    def cortar(r: Grandeza) -> Grandeza:  # mais do que o necessário não compensa o que falta noutro lado
        return r if r.v < 1.0 else G(1.0, 0.0, "1", fonte="saturado")

    def media_geometrica(rs: Sequence[Grandeza]) -> Grandeza:
        if any(r.v <= 0.0 for r in rs):
            return G(0.0, 0.0, "1", fonte="zero")
        soma = g_ln(rs[0])
        for r in rs[1:]:
            soma = soma + g_ln(r)
        return g_exp(soma / float(len(rs)))

    rh = {k: cortar(g[k] / G(n, 0.0, f1["unidades"][k], fonte=("norma", k))) for k, n in sorted(f1["necessario"].items())}
    re_ = {k: cortar(G(t, 0.0, f2["unidades"][k], fonte=("norma", k)) / g[k]) if g[k].v > 0.0 else G(1.0, 0.0, "1", fonte="saturado")
           for k, t in sorted(f2["teto"].items())}
    H, E = media_geometrica(list(rh.values())), media_geometrica(list(re_.values()))
    N = H * E
    baixo, _ = faixa95(N, "1")
    nivel = next((n for n, lim in sorted(f3["selos"].items(), key=lambda x: -x[1]) if baixo >= lim), "SEM_SELO")
    return {"H": H, "E": E, "N_eq": N, "n_eq": N.em("1")[0], "u": N.em("1")[1], "limite_inferior_95": baixo, "nivel": nivel,
            "razoes": {k: r.em("1")[0] for k, r in sorted({**rh, **re_}.items())}}


_F15 = ("F15.1", "F15.2", "F15.3")


def selo_ponto_neutral(comunidade: str, periodo: str, medicoes: Dict[str, Dict[str, Any]], sk_certificador: bytes) -> Dict[str, Any]:
    """P16 — SELO PONTO NEUTRAL. Certificado = medições + hash das fórmulas + resultado + nível, selado (Ed25519) por quem
    certifica. Se a conta der veto, o certificado diz VETADO: a certificadora sela o que a conta diz, não o que convém."""
    corpo: Dict[str, Any] = {"certificado": "PONTO_NEUTRAL/1", "comunidade": comunidade, "periodo": periodo, "medicoes": medicoes,
                             "formulas": {k: hobj(FORMULAS_15[k]) for k in _F15}, "nao_garante": FORMULAS_15["F15.3"]["o_que_nao_garante"]}
    try:
        r = ponto_neutral(medicoes)
        corpo.update(nivel=r["nivel"], n_eq=r["n_eq"], incerteza=r["u"], limite_inferior_95=r["limite_inferior_95"])
    except VetoBiofisico as e:
        corpo.update(nivel="VETADO", veto=str(e))
    return {"corpo": corpo, "selo": selar(corpo, sk_certificador)}


def verificar_selo_ponto_neutral(cert: Any, certificadores: Dict[str, str]) -> Tuple[bool, str]:
    """Verificação externa, por RE-EXECUÇÃO: o selo é de uma certificadora registada E a conta, refeita de raiz a partir
    das medições do certificado, dá o mesmo N_eq e o mesmo nível. Devolve (vale?, nível ou motivo)."""
    try:
        corpo, selo = cert["corpo"], cert["selo"]
        if corpo.get("certificado") != "PONTO_NEUTRAL/1" or not selo_ok(corpo, selo, set(certificadores.values())):
            return False, "SELO_INVALIDO_OU_CERTIFICADORA_NAO_REGISTADA"
        if corpo["formulas"] != {k: hobj(FORMULAS_15[k]) for k in _F15}:
            return False, "FORMULA_DIFERENTE"
        try:
            r = ponto_neutral(corpo["medicoes"])
        except VetoBiofisico:
            return False, "VETO_BIOFISICO"
        if corpo["nivel"] != r["nivel"] or _limpo([corpo["n_eq"], corpo["incerteza"]]) != _limpo([r["n_eq"], r["u"]]):
            return False, "RESULTADO_NAO_CONFERE"
        return r["nivel"] != "SEM_SELO", r["nivel"]
    except (KeyError, TypeError, ValueError, AttributeError):
        return False, "CERTIFICADO_MAL_FORMADO"


class RastroVital:
    """P17 — RASTRO VITAL. A curva do N_eq no tempo lê-se da própria ledger; o exposoma de uma vida fica com a pessoa.
    Na ledger só entram agregados da comunidade e hashes: nunca os dados de uma pessoa."""

    def __init__(self, livro: LedgerImutavel) -> None:
        self.livro = livro

    def registar(self, comunidade: str, periodo: str, medicoes: Dict[str, Dict[str, Any]], dia: int) -> Dict[str, Any]:
        try:
            r = ponto_neutral(medicoes)
            estado, extra = "RASTRO_REGISTADO", {"n_eq": r["n_eq"], "incerteza": r["u"], "nivel": r["nivel"]}
        except VetoBiofisico as e:
            estado, extra = "RASTRO_VETO_BIOFISICO", {"motivo": str(e)}
        return responder(self.livro, dia, estado, medicoes, {k: FORMULAS_15[k] for k in _F15}, comunidade=comunidade, periodo=periodo, **extra)

    def curva(self, comunidade: str) -> List[Tuple[str, float, float]]:
        return [(b["payload"]["periodo"], b["payload"]["n_eq"], b["payload"]["incerteza"]) for b in self.livro.blocos
                if b["evento"] == "RASTRO_REGISTADO" and b["payload"]["comunidade"] == comunidade]

    def tendencia(self, comunidade: str) -> Dict[str, Any]:
        c = self.curva(comunidade)
        if len(c) < 2:
            return {"estado": "SEM_HISTORIA"}
        delta, u = c[-1][1] - c[0][1], math.sqrt(c[0][2] ** 2 + c[-1][2] ** 2)
        k = 1.959963984540054  # 95% bilateral: a diferença tem de ser maior do que o erro das duas pontas
        return {"estado": "A_SUBIR" if delta > k * u else "A_DESCER" if delta < -k * u else "SEM_DIFERENCA_A_95",
                "delta": delta, "incerteza": u, "de": c[0][0], "ate": c[-1][0]}

    def exposicao(self, sk_titular: bytes, periodo: str, exposicoes: Dict[str, Dict[str, Any]], dia: int) -> Dict[str, Any]:
        """O exposoma: a pessoa sela o seu registo (o que respirou, bebeu, levou de radiação) e guarda-o consigo.
        Para a ledger vai só o hash: prova que o registo existia nesse dia, sem mostrar nada do que lá está."""
        for nome, e in sorted(exposicoes.items()):
            G(e["valor"], e.get("incerteza", 0.0), e["unidade"])  # unidade desconhecida = TypeError
        dados = {"periodo": periodo, "exposicoes": exposicoes}
        reg = {"dados": dados, "selo": selar(dados, sk_titular)}
        self.livro.registar(dia, "RASTRO_EXPOSICAO", {"titular": h256(bytes.fromhex(reg["selo"]["pub"]))[:16], "periodo": periodo,
                                                      "registo": reg["selo"]["hash"]})
        return reg

    def exposicao_confere(self, reg: Any) -> bool:
        try:
            return selo_ok(reg["dados"], reg["selo"]) and any(
                b["evento"] == "RASTRO_EXPOSICAO" and b["payload"]["registo"] == reg["selo"]["hash"] for b in self.livro.blocos)
        except (KeyError, TypeError):
            return False


def f_harmonia(casos: Grandeza, adesao: Grandeza) -> Grandeza:
    """P18 — F-HARMONIA. A fração evitável entra como a OMS a dá: um intervalo (30 a 50%), não um número.
    Intervalo sem mais informação = distribuição retangular: valor 40%, incerteza 10/raiz(3) = 5,8 pontos (GUM)."""
    f = FORMULAS_15["F-HARMONIA"]
    for nome, x in (("casos", casos), ("adesao", adesao)):
        try:
            x.em(f["unidades"][nome])
        except TypeError as e:
            raise TypeError(f"F-HARMONIA.{nome}: {e}") from None
    if not 0.0 <= adesao.v <= 1.0:
        raise ValueError("a adesão é uma fração entre 0 e 1")
    lo, hi = f["fracao_evitavel"]["minimo"], f["fracao_evitavel"]["maximo"]
    return casos * G((lo + hi) / 2.0, (hi - lo) / 2.0 / math.sqrt(3.0), "1", fonte="OMS_30_a_50") * adesao


def debate(nome: str, pessoas: Grandeza, dose: Grandeza, sk: bytes) -> Dict[str, Any]:
    """P18 — a mesma pergunta respondida por cada teoria em debate, cada resposta selada. O estado é DEBATIDO."""
    d = DEBATES[nome]
    seladas = []
    for t in d["teorias"]:
        excesso = dose - G(t["limiar_Sv"], 0.0, "Sv", fonte=t["id"] + "/limiar")
        casos = (pessoas * excesso * G(t["risco_por_Sv"], 0.0, "caso/pessoa/Sv", fonte=t["id"])) if excesso.v > 0.0 else G(0.0, 0.0, "caso")
        v, u = casos.em("caso")
        dados = {"debate": nome, "teoria": t["id"], "versao": t["versao"], "hash_formula": hobj(t), "pessoas": pessoas, "dose": dose,
                 "casos": v, "incerteza": u}
        seladas.append({"dados": dados, "selo": selar(dados, sk)})
    return {"estado": d["estado"], "pergunta": d["pergunta"], "teorias": seladas}


def financiar(motor: Motor, eid: str, destino: str, valor: int, dia: int, minimo: float, unidade: str, certificado: Any,
              certificadores: Dict[str, str], dominio: str = "INFRAESTRUTURA") -> Dict[str, Any]:
    """P19 — VETO ↔ ESCROW. Dinheiro novo só se monta para quem traz um certificado de ponto neutral que confere
    por re-execução, sem veto biofísico. Fora disso o escrow nem chega a existir e a recusa fica na ledger."""
    ok, nivel = verificar_selo_ponto_neutral(certificado, certificadores)
    if ok and certificado["corpo"].get("comunidade") != destino:
        ok, nivel = False, "CERTIFICADO_DE_OUTRA_COMUNIDADE"
    if ok:
        return motor.criar_escrow(eid, destino, valor, dia, minimo, unidade, dominio)
    entrada = hobj({"financiar": eid, "destino": destino, "valor": valor, "dia": dia, "certificado": hobj(certificado)})
    return motor._resp("RECUSADO_VETO_BIOFISICO" if nivel == "VETO_BIOFISICO" else "RECUSADO_FORA_DO_PONTO_NEUTRAL", entrada, dia,
                       escrow=eid, motivo=nivel, reserva=motor.reserva)


# -----------------------------------------------------------------------------
# 19. P20 — LENS-BARCODE SEAL: O RÓTULO OMITE, A LÂMPADA MOSTRA
# -----------------------------------------------------------------------------
def gtin13_valido(codigo: str) -> bool:
    """Código de barras GTIN-13 com o dígito de controlo certo (pesos 1 e 3, alternados)."""
    return (isinstance(codigo, str) and len(codigo) == 13 and codigo.isdigit()
            and (10 - sum(int(x) * (3 if i % 2 else 1) for i, x in enumerate(codigo[:12])) % 10) % 10 == int(codigo[12]))


class Lampada:
    """P20. O código de barras aponta para a análise SELADA do lote por um laboratório registado: o rótulo omite, a
    lâmpada mostra. Uma rede de pelo menos k leitores independentes (P9) mede o lote; se a mediana sair da banda que o
    próprio rótulo declara, sai ALERTA e o escrow do fornecedor congela 15 dias, para decisão humana.
    Mostra o que foi medido, com fonte. Não aponta culpados: quem decide é quem lê, e depois quem julga."""

    def __init__(self, laboratorios: Dict[str, str], aldeia: Aldeia, livro: LedgerImutavel) -> None:
        self.laboratorios, self.aldeia, self.livro = dict(laboratorios), aldeia, livro
        self.fichas: Dict[Tuple[str, str], Dict[str, Any]] = {}
        self.leituras: Dict[Tuple[str, str, str], Dict[str, float]] = {}  # (código, lote, substância) -> {leitor: valor em unidades-base}

    def publicar(self, rotulo: Dict[str, Any], analise: Dict[str, Any], dia: int) -> str:
        """rotulo = {gtin, lote, produto, declarado: {substância: {valor, tolerancia_rel, unidade}}};
        analise = {dados: {gtin, lote, laboratorio, medido: {substância: {valor, incerteza, unidade}}}, selo}."""
        if not gtin13_valido(rotulo.get("gtin", "")):
            return "RECUSADO_CODIGO_DE_BARRAS_INVALIDO"
        d = analise.get("dados", {})
        if (d.get("laboratorio") not in self.laboratorios or (d.get("gtin"), d.get("lote")) != (rotulo["gtin"], rotulo["lote"])
                or not selo_ok(d, analise.get("selo", {}), {self.laboratorios[d["laboratorio"]]})):
            return "RECUSADO_ANALISE_SEM_SELO_DE_LABORATORIO"
        try:  # o rótulo e a análise têm de falar da mesma grandeza em cada substância declarada
            for s, dec in rotulo["declarado"].items():
                if s in d["medido"]:
                    G(d["medido"][s]["valor"], 0.0, d["medido"][s]["unidade"]).em(dec["unidade"])
        except (TypeError, KeyError):
            return "RECUSADO_UNIDADES_INCOMPATIVEIS"
        self.fichas[(rotulo["gtin"], rotulo["lote"])] = {"rotulo": rotulo, "analise": analise}
        self.livro.registar(dia, "LAMPADA_FICHA", {"gtin": rotulo["gtin"], "lote": rotulo["lote"], "rotulo": hobj(rotulo),
                                                   "analise": analise["selo"]["hash"]})
        return "PUBLICADO"

    def iluminar(self, gtin: str, lote: str) -> Dict[str, Any]:
        """O que a lente mostra: o que o rótulo declara, e o que a análise selada mediu e o rótulo não diz."""
        f = self.fichas.get((gtin, lote))
        if f is None:
            return {"estado": "SEM_FICHA", "nota": "sem análise selada deste lote, a lâmpada não inventa"}
        declarado, medido = f["rotulo"]["declarado"], f["analise"]["dados"]["medido"]
        k95 = REGRAS["k95_unilateral"]
        omitido, diferente = {}, {}
        for s, m in sorted(medido.items()):
            x = G(m["valor"], m.get("incerteza", 0.0), m["unidade"])
            if s not in declarado:
                if x.v - k95 * x.u > 0.0:  # está lá, com 95% de confiança, e o rótulo não fala nele
                    omitido[s] = m
            else:
                alvo = G(declarado[s]["valor"], 0.0, declarado[s]["unidade"])
                if abs((x - alvo).v) > k95 * x.u + declarado[s]["tolerancia_rel"] * abs(alvo.v):
                    diferente[s] = m
        return {"estado": "ROTULO_OMITE" if omitido else "ROTULO_DIFERE" if diferente else "ROTULO_CONFERE",
                "produto": f["rotulo"]["produto"], "declarado": declarado, "omitido": omitido, "diferente": diferente,
                "analise": f["analise"]["selo"]["hash"], "laboratorio": f["analise"]["dados"]["laboratorio"], "nota": FRASES_OBRIGATORIAS["lampada"]}

    def ler(self, leitura: Dict[str, Any]) -> str:
        """Uma leitura da rede: {dados: {quem, gtin, lote, substancia, valor, unidade, dia}, selo}, selada por um membro registado."""
        d = leitura.get("dados", {})
        p = d.get("quem")
        if p not in self.aldeia.membros or not selo_ok(d, leitura.get("selo", {}), {self.aldeia.membros[p]}):
            return "RECUSADO_LEITOR_NAO_REGISTADO_OU_SELO_INVALIDO"
        f = self.fichas.get((d.get("gtin"), d.get("lote")))
        if f is None or d.get("substancia") not in f["rotulo"]["declarado"]:
            return "RECUSADO_SEM_FICHA_OU_SUBSTANCIA_NAO_DECLARADA"
        try:
            x = G(d["valor"], 0.0, d["unidade"])
            x.em(f["rotulo"]["declarado"][d["substancia"]]["unidade"])
        except (TypeError, KeyError):
            return "RECUSADO_UNIDADE_ERRADA"  # uma leitura noutra grandeza não se mistura com as outras
        do_lote = self.leituras.setdefault((d["gtin"], d["lote"], d["substancia"]), {})
        if p in do_lote:
            return "RECUSADO_LEITURA_REPETIDA"
        do_lote[p] = x.v
        return "ACEITE"

    def avaliar(self, gtin: str, lote: str, substancia: str, dia: int, motor: Optional[Motor] = None,
                escrow: Optional[str] = None) -> Dict[str, Any]:
        """Com menos de k leitores INDEPENDENTES a rede não fala. Com k ou mais, compara a mediana com a banda do rótulo."""
        dec = self.fichas[(gtin, lote)]["rotulo"]["declarado"][substancia]
        ls = self.leituras.get((gtin, lote, substancia), {})
        independentes, k = self.aldeia._grupos(sorted(ls)), REGRAS["quorum_k"]
        entrada = {"gtin": gtin, "lote": lote, "substancia": substancia, "leituras": sorted(ls.items())}
        if independentes < k:
            return responder(self.livro, dia, "AGUARDA_REDE_K", entrada, hash_regras(), leitores_independentes=independentes, exigidos=k)
        fator = _unid(dec["unidade"])[0]
        xs = sorted(ls.values())
        m = statistics.median(xs)
        u = 1.4826 * statistics.median(sorted(abs(x - m) for x in xs)) / math.sqrt(len(xs))
        alvo = dec["valor"] * fator
        banda = [alvo * (1.0 - dec["tolerancia_rel"]), alvo * (1.0 + dec["tolerancia_rel"])]
        k95 = REGRAS["k95_unilateral"]
        factos = {"gtin": gtin, "lote": lote, "substancia": substancia, "unidade": dec["unidade"], "mediana": m / fator, "incerteza": u / fator,
                  "banda_declarada": [b / fator for b in banda], "leitores_independentes": independentes}
        if not (m - k95 * u > banda[1] or m + k95 * u < banda[0]):
            return responder(self.livro, dia, "LOTE_DENTRO_DA_BANDA", entrada, hash_regras(), **factos)
        r = responder(self.livro, dia, "ALERTA_LOTE_ANOMALO", entrada, hash_regras(), nota=FRASES_OBRIGATORIAS["deteccao"], **factos)
        if motor is not None and escrow is not None:  # o alerta congela o pagamento; não julga ninguém
            r["escrow"] = motor.congelar_por_veto(escrow, "ALERTA_LOTE_ANOMALO", dict(factos, alerta=r["linhagem"]["hash_estado_ledger"]), dia)["estado"]
        return r


# -----------------------------------------------------------------------------
# 20. P23 — CALCULADORA-PROFESSORA: python3 konfirmu_calc.py --explica
# -----------------------------------------------------------------------------
def orcamento(g: Grandeza) -> List[Tuple[str, float]]:
    """De onde vem a incerteza: a parte (em %) da variância que cabe a cada fonte de erro, da maior para a menor."""
    partes: Dict[str, float] = {}
    for k, x in g.c.items():
        if isinstance(k, tuple) and k and k[0] == "propria":
            nome = "cada peça por si"
        elif isinstance(k, tuple) and k and k[0] == "fonte":
            nome = f"comum ao lote «{k[1]}»"
        elif isinstance(k, tuple):
            nome = str(k[-1])
        else:
            nome = str(k)
        partes[nome] = partes.get(nome, 0.0) + x * x
    total = sum(partes.values())
    return sorted(((n, 100.0 * v / total) for n, v in partes.items()), key=lambda t: (-t[1], t[0])) if total else []


def professora() -> List[str]:
    """P23. A calculadora explica-se em linguagem de gente: unidades, incerteza e porque é que um veto disparou.
    Cada frase sai de uma conta feita agora pelo motor; nenhuma é texto decorado."""
    L: List[str] = ["KONFIRMU CALC — a calculadora explica-se (cada número abaixo foi calculado agora)", ""]
    L.append("1. UNIDADES — o motor não soma coisas diferentes.")
    L.append("   Pedi 5 kWh + 3 EUR. Resposta: «" + _erro(lambda: G(5.0, 0.0, "kWh") + G(3.0, 0.0, "EUR"), TypeError) + "».")
    L.append("   Energia e dinheiro só se juntam com um preço: 5 kWh × 0,12 EUR/kWh = "
             + (G(5.0, 0.0, "kWh") * G(0.12, 0.0, "EUR/kWh")).txt("EUR") + ". Agora sim, é dinheiro.")
    lm = ORACULOS_GRAVADOS["irradiacao/maputo"]["leituras"][0]
    sol = G(lm["valor"], lm["incerteza"], "MJ/m2/dia", fonte="sol de Maputo")
    L.append(f"   Converter também é com ele: {sol.txt('MJ/m2/dia')} de sol em Maputo = {sol.txt('kWh/m2/dia')} = "
             f"{(sol / G_STC).txt('h/dia')} de sol de pico.")
    L.append("")
    L.append("2. INCERTEZA — nenhum número vem sozinho.")
    etas = lote(22.0, 1.5, "%", "painéis", 0.25, 4)
    e = F2(G(4.0, 0.0, "painel/microrrede"), G(1.95, 0.02, "m2/painel", fonte="área do painel"),
           (etas[0] + etas[1] + etas[2] + etas[3]) / 4.0, G(0.75, 0.05, "1", fonte="perdas do sistema"), sol / G_STC)
    v, u = e.em("kWh/dia/microrrede")
    L.append(f"   4 painéis em Maputo dão {_n(v)} ± {_n(u)} kWh por dia. O «±» diz até onde a conta pode estar errada.")
    L.append("   De onde vem a dúvida: " + " · ".join(f"{nome} {_n(p, 0)}%" for nome, p in orcamento(e)) + ".")
    L.append(f"   Por isso não se promete {_n(v)}: promete-se pelo menos {_n(faixa95(e, 'kWh/dia/microrrede')[0])} kWh por dia, com 95% de confiança.")
    L.append(f"   E x − x dá {(e - e).txt('kWh/dia/microrrede')}: o mesmo erro não se conta duas vezes.")
    L.append("")
    L.append("3. PORQUE É QUE O VETO DISPAROU")
    L.append("   Físico. Pedi um painel de silício a 45%. Resposta: «" + _erro(lambda: veto_fisico(G(45.0, 1.0, "%")), VetoFisico) + "».")
    L.append("   Em palavras simples: a luz do sol tem um máximo que um painel destes consegue aproveitar. Quem promete mais, ou traz prova de laboratório selada, ou não passa.")
    L.append("   Farmacológico. Pedi 1800 mg de paracetamol para uma criança de 12 kg. Resposta: «"
             + _erro(lambda: verificar_toma("paracetamol_oral", 730, G(12.0, 0.5, "kg"), G(1800.0, 0.0, "mg"), G(6.0, 0.0, "h"), 4), VetoFarmacologico) + "».")
    L.append("   Em palavras simples: uma vírgula fora do sítio multiplica a dose por 10. O motor não receita; só trava o que passa do teto escrito na fonte. Não substitui tratamento clínico.")
    toxica = {k: {"valor": x, "incerteza": y, "unidade": FORMULAS_15["F15.1" if k in FORMULAS_15["F15.1"]["necessario"] else "F15.2"]["unidades"][k]}
              for k, (x, y) in {"agua": (80.0, 4.0), "alimentacao": (2600.0, 90.0), "energia": (0.9, 0.05), "saude": (0.95, 0.02),
                                "carbono": (1.5, 0.2), "agua_captada": (0.30, 0.03), "habitat_ocupado": (0.60, 0.03), "captura_animal": (1.6, 0.1)}.items()}
    L.append("   Biofísico. Uma comunidade com tudo o que precisa, mas que pesca 1,6 vezes o que o mar repõe. Resposta: «"
             + _erro(lambda: ponto_neutral(toxica), VetoBiofisico) + "».")
    L.append("   Em palavras simples: conforto hoje não paga o peixe que falta amanhã. Este veto não se compra.")
    L.append("")
    L.append("4. O SELO — um byte basta.")
    doc = {"obra": "poço", "litros_por_dia": 20000}
    selo = selar(doc, chave_demo("professora"))
    L.append(f"   Selei {canon(doc).decode('utf-8')} -> sha256 {selo['hash'][:16]}… · confere: {'sim' if selo_ok(doc, selo) else 'não'}.")
    L.append(f"   Mudei 20000 para 20001 -> confere: {'sim' if selo_ok(dict(doc, litros_por_dia=20001), selo) else 'não'}. Quem mexe num número deixa rasto.")
    L.append("")
    L.append("5. O QUE ISTO NÃO GARANTE")
    for frase in FRASES_OBRIGATORIAS.values():
        L.append("   " + frase)
    return L


# -----------------------------------------------------------------------------
# 21. v2.3 — O QUE VEIO DA SUITE DE OUTRA IA (recebida a 20-11-2026, 06:48), FEITO DE VERDADE
#     P2 teto de Carnot · L1 massa de uma carga · R1 energia de uma missão · S1 stock parado
# -----------------------------------------------------------------------------
# A outra suite dá estes domínios como texto fixo («APROVADO», «CONFORME», «AUTORIZADA»): a função dela não recebe
# dado nenhum. Aqui cada estado sai de uma conta com unidades e incerteza. O que lá não tem nada para medir
# (liquidação por um banco, habitação «amortizada sem juros», direito de autor «100% direto», «prova de mestria»,
# certificado «SIR») NÃO entrou: fica na referência, à espera de quem manda. Licença: decisão do David, não do motor.
K2 = 2.0  # fator de cobertura a duas caudas (cerca de 95%), como no GUM
RESERVA_DE_MISSAO = 0.20  # [VALIDAR] fração da energia que fica sempre de reserva: escolha

FORMULAS_23: Dict[str, Dict[str, Any]] = {
    "P2.CARNOT": {"id": "P2.CARNOT", "versao": "1.0.0", "nome": "teto de Carnot",
                  "formula": "teto = 1 − T_fria / T_quente   (temperaturas absolutas; vale para qualquer máquina térmica)",
                  "unidades": {"t_quente": "K", "t_fria": "K", "saida": "1"}, "etiqueta": "MEDIDO",
                  "fonte": "Carnot (1824); segunda lei da termodinâmica. A outra suite trazia só o caso 600 K / 300 K, como número fixo (0,500)",
                  "o_que_nao_garante": "é teto, não é rendimento: uma máquina real fica bem abaixo; não se aplica a painéis (esses têm os tetos de P2)"},
    "L1": {"id": "L1", "versao": "1.0.0", "nome": "balanço de massa de uma carga",
           "formula": "Δ = carregado − descarregado − perdas declaradas; alerta se |Δ| > 2 · u(Δ)",
           "unidades": {"carregado": "kg", "descarregado": "kg", "perdas_declaradas": "kg", "saida": "kg"}, "etiqueta": "MEDIDO",
           "fonte": "conservação da massa; incerteza combinada das pesagens (GUM), com fator de cobertura 2",
           "o_que_nao_garante": "não diz para onde foi a massa nem quem lhe mexeu: diz que as pesagens não batem. Não conhece "
                                "evaporação, humidade nem tara mal medida, se não vierem declaradas"},
    "L1.ISO6346": {"id": "L1.ISO6346", "versao": "1.0.0", "nome": "dígito de controlo do número de contentor",
                   "formula": "soma de valor_i · 2^i nas 10 primeiras posições; dígito = (soma mod 11) mod 10",
                   "unidades": {"numero": "1", "saida": "1"}, "etiqueta": "ASSUMIDO",
                   "fonte": "ISO 6346, escrita de memória e conferida com o exemplo conhecido CSQU3054383 [VALIDAR]",
                   "o_que_nao_garante": "um número com o dígito certo pode não existir: o dígito só apanha enganos de escrita"},
    "R1": {"id": "R1", "versao": "1.0.0", "nome": "energia de uma missão de drone",
           "formula": "precisa = potência · duração; útil = disponível · (1 − reserva); autoriza se o pior caso de «precisa» "
                      "couber no pior caso de «útil» (95%) e houver assinatura humana desta missão",
           "unidades": {"potencia": "W", "duracao": "min", "disponivel": "kWh", "saida": "kWh"}, "etiqueta": "ASSUMIDO",
           "fonte": "E = P · t (definição de energia); a reserva de 20% e a regra dos 95% são escolha [VALIDAR]",
           "o_que_nao_garante": "não conhece vento, carga, estado da bateria nem regras do espaço aéreo; a assinatura humana autoriza, "
                                "não torna o voo seguro"},
    "S1": {"id": "S1", "versao": "1.0.0", "nome": "resgate de stock parado (cenário)",
           "formula": "CO2 evitado = aparelhos · fator; fundo = aparelhos · contribuição",
           "unidades": {"aparelhos": "aparelho", "co2_por_aparelho": "kgCO2e/aparelho", "contribuicao": "EUR/aparelho", "saida": "tCO2e"},
           "etiqueta": "ASSUMIDO",
           "fonte": "números da outra suite (10 000 aparelhos, 550 t, 30 000 EUR), que não diz de onde vêm; daí 55 kg e 3 EUR por aparelho [VALIDAR]",
           "o_que_nao_garante": "só há CO2 evitado se o aparelho resgatado substituir um novo; não conta o transporte nem o fim de vida do aparelho"},
}


def teto_de_carnot(t_quente: Grandeza, t_fria: Grandeza) -> Grandeza:
    """P2 para máquinas térmicas: 1 − T_fria / T_quente, com a incerteza dos dois termómetros. Só aceita kelvin."""
    tq, tf = t_quente.em("K")[0], t_fria.em("K")[0]
    if not 0.0 < tf < tq:
        raise VetoFisico(f"temperaturas impossíveis para uma máquina térmica: fria {_n(tf, 0)} K, quente {_n(tq, 0)} K")
    return 1.0 - t_fria / t_quente


def veto_de_carnot(eta: Grandeza, t_quente: Grandeza, t_fria: Grandeza) -> Dict[str, Any]:
    """Três zonas, como na dose (M1): dentro · revisão humana (o excesso cabe no erro dos termómetros) · veto.
    Aqui nenhuma prova salva: Carnot é limite da física, não de uma tecnologia."""
    teto = teto_de_carnot(t_quente, t_fria)
    v, (tv, tu) = eta.em("1")[0], teto.em("1")
    if not 0.0 < v <= 1.0:
        raise VetoFisico(f"rendimento de {_n(v * 100, 1)}% não existe: tem de estar entre 0 e 100%")
    r = {"rendimento": v, "teto": tv, "incerteza_do_teto": tu}
    if v <= tv:
        return dict(r, estado="DENTRO_DO_TETO_DE_CARNOT")
    if v <= faixa95(teto, "1")[1]:
        return dict(r, estado="REVISAO_HUMANA")
    raise VetoFisico(f"rendimento de {_n(v * 100, 1)}% passa o teto de Carnot, {_n(tv * 100, 1)} ± {_n(tu * 100, 1)}% entre "
                     f"{_n(t_quente.em('K')[0], 0)} K e {_n(t_fria.em('K')[0], 0)} K: nenhuma máquina térmica o faz e nenhuma prova o salva")


_ISO6346 = dict(zip("ABCDEFGHIJKLMNOPQRSTUVWXYZ",
                    (10, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 34, 35, 36, 37, 38)))


def iso6346_digito(numero: Any) -> Optional[int]:
    """Dígito de controlo de um número de contentor: 4 letras + 6 algarismos (+ o dígito, se vier). None se o formato não for esse."""
    n = re.sub(r"[\s\-]", "", numero.upper()) if isinstance(numero, str) else ""
    if not re.fullmatch(r"[A-Z]{4}[0-9]{6,7}", n):
        return None
    return sum((_ISO6346[c] if c.isalpha() else int(c)) << i for i, c in enumerate(n[:10])) % 11 % 10


def iso6346_valido(numero: Any) -> bool:
    n = re.sub(r"[\s\-]", "", numero.upper()) if isinstance(numero, str) else ""
    return bool(re.fullmatch(r"[A-Z]{4}[0-9]{7}", n)) and iso6346_digito(n) == int(n[10])


def balanco_de_massa(carregado: Grandeza, descarregado: Grandeza, perdas_declaradas: Optional[Grandeza] = None) -> Dict[str, Any]:
    """L1: as pesagens batem? Δ = carregado − descarregado − perdas declaradas, com a incerteza das balanças.
    Fora de 2 · u(Δ) -> ALERTA. O alerta leva números; não aponta ninguém."""
    delta = carregado - descarregado
    if perdas_declaradas is not None:
        delta = delta - perdas_declaradas
    v, u = delta.em("kg")
    estado = "CONFORME" if abs(v) <= K2 * u else ("ALERTA_MASSA_EM_FALTA" if v > 0 else "ALERTA_MASSA_A_MAIS")
    return {"estado": estado, "diferenca_kg": v, "incerteza_kg": u, "limiar_kg": K2 * u, "nota": FRASES_OBRIGATORIAS["deteccao"]}


def orcamento_de_missao(potencia: Grandeza, duracao: Grandeza, disponivel: Grandeza, missao: Dict[str, Any],
                        trava: Optional[Dict[str, str]], operadores: Dict[str, str],
                        reserva: float = RESERVA_DE_MISSAO) -> Dict[str, Any]:
    """R1: a missão cabe na energia que há? E há uma pessoa registada a assinar ESTA missão?
    A assinatura humana não paga a conta da energia; a conta da energia não dispensa a assinatura."""
    if not 0.0 <= reserva < 1.0:
        raise ValueError("a reserva é uma fração entre 0 e 1")
    precisa, util = potencia * duracao, disponivel * (1.0 - reserva)
    (pv, pu), (uv, uu) = precisa.em("kWh"), util.em("kWh")
    pior_precisa, pior_util = faixa95(precisa, "kWh")[1], faixa95(util, "kWh")[0]
    r = {"precisa_kwh": pv, "u_precisa_kwh": pu, "util_kwh": uv, "u_util_kwh": uu,
         "pior_caso_precisa_kwh": pior_precisa, "pior_caso_util_kwh": pior_util, "reserva": reserva}
    if pv > uv:
        return dict(r, estado="RECUSADA_ENERGIA_INSUFICIENTE")
    if not (isinstance(trava, dict) and selo_ok(missao, trava, set(operadores.values()))):
        return dict(r, estado="RECUSADA_SEM_TRAVA_HUMANA")
    if pior_precisa <= pior_util:
        return dict(r, estado="AUTORIZADA")
    return dict(r, estado="REVISAO_HUMANA_NO_LIMITE")


def resgate_de_stock_parado(aparelhos: Grandeza, co2_por_aparelho: Grandeza, contribuicao: Grandeza) -> Dict[str, Any]:
    """S1 — CENÁRIO, não facto: o CO2 que se evitaria e o que entraria num fundo de reciclagem limpa."""
    aparelhos.em("aparelho")
    (cv, cu), (fv, fu) = (aparelhos * co2_por_aparelho).em("tCO2e"), (aparelhos * contribuicao).em("EUR")
    return {"estado": "CENARIO", "co2_evitado_t": cv, "u_co2_evitado_t": cu, "fundo_eur": fv, "u_fundo_eur": fu,
            "etiqueta": "ASSUMIDO", "carimbo": CARIMBO}


# -----------------------------------------------------------------------------
# 21-B. v2.4 — A IRMANDADE · CAMADA DE SEGURANÇA S1 a S9 · VETO DE GIBBS · VETO HÍDRICO
# -----------------------------------------------------------------------------
# A IRMANDADE — regra de desenho: a irmandade é mecanismo, não discurso.
# As câmaras do 3-de-5 incluem, desde o genesis, 3 câmaras africanas. Com 3 em 5, nenhum trio se forma sem pelo
# menos uma delas: nenhuma decisão acima do teto passa sem África. O Motor recusa arrancar com outro desenho.
# [VALIDAR] S1 a S9 são a prova do mecanismo em Python puro, escritos de raiz: o «port já provado» não me chegou.
CAMARAS_AFRICANAS = ("camara_africana_1", "camara_africana_2", "camara_africana_3")
CAMARAS = CAMARAS_AFRICANAS + ("conselho_da_aldeia", "auditoria_aberta")


def irmandade_ok(custodios: Any, k: int = 3) -> bool:
    """True só se as 3 câmaras africanas lá estão e os restantes, sozinhos, não chegam a k."""
    nomes = list(custodios)
    return all(c in nomes for c in CAMARAS_AFRICANAS) and len(nomes) - len(CAMARAS_AFRICANAS) < k


# --- S1: comparação de segredos e de hashes em tempo constante
def igual_seguro(a: Any, b: Any) -> bool:
    try:
        return hmac.compare_digest(str(a).encode("utf-8"), str(b).encode("utf-8"))
    except Exception:
        return False


# --- S2: cofre de chaves. A frase-passe vem de um descritor de ficheiro ou do ambiente; nunca dos argumentos nem do código.
class ChaveDeDemoRecusada(PermissionError):
    """Em produção as chaves de demo (que saem da semente pública) são recusadas."""


class KeyStore:
    """[VALIDAR] PBKDF2-HMAC-SHA256 + máscara + HMAC: prova do mecanismo, não é um cofre auditado. Em produção: HSM."""
    VOLTAS = 100_000

    def __init__(self, caminho: str) -> None:
        self.caminho = caminho

    @staticmethod
    def frase_passe(argv: Sequence[str] = (), ambiente: Optional[Dict[str, str]] = None) -> bytes:
        ambiente = os.environ if ambiente is None else ambiente
        if any(a.startswith("--passphrase") or a.startswith("--frase") for a in argv):
            raise PermissionError("FRASE_PASSE_NOS_ARGUMENTOS_RECUSADA")  # os argumentos ficam à vista de qualquer processo
        if ambiente.get("KONFIRMU_PASSPHRASE_FD"):
            with os.fdopen(int(ambiente["KONFIRMU_PASSPHRASE_FD"]), "rb", closefd=False) as fh:
                return fh.readline().rstrip(b"\r\n")
        if ambiente.get("KONFIRMU_PASSPHRASE"):
            return ambiente["KONFIRMU_PASSPHRASE"].encode("utf-8")
        raise PermissionError("SEM_FRASE_PASSE")

    def _deriva(self, frase: bytes, sal: bytes) -> bytes:
        return hashlib.pbkdf2_hmac("sha256", frase, sal, self.VOLTAS, dklen=64)

    def guardar(self, nome: str, sk: bytes, frase: bytes, sal: bytes) -> None:
        d = self._deriva(frase, sal)
        cifra = bytes(a ^ b for a, b in zip(sk, d[:32]))
        reg = {"nome": nome, "sal": sal.hex(), "cifra": cifra.hex(), "mac": hmac.new(d[32:], sal + cifra, "sha256").hexdigest()}
        fd = os.open(self.caminho, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
        try:
            os.write(fd, canon(reg))
            os.fsync(fd)
        finally:
            os.close(fd)

    def abrir(self, frase: bytes) -> bytes:
        with open(self.caminho, "rb") as fh:
            reg = json.loads(fh.read().decode("utf-8"))
        sal, cifra = bytes.fromhex(reg["sal"]), bytes.fromhex(reg["cifra"])
        d = self._deriva(frase, sal)
        if not igual_seguro(hmac.new(d[32:], sal + cifra, "sha256").hexdigest(), reg["mac"]):
            raise PermissionError("FRASE_PASSE_ERRADA_OU_COFRE_MEXIDO")
        return bytes(a ^ b for a, b in zip(cifra, d[:32]))


# --- S3: cerimónia das chaves
def cerimonia(camaras: Sequence[str] = CAMARAS, k: int = 3, acaso: Any = None) -> Dict[str, Any]:
    """Gera a chave do cofre, parte-a pelas câmaras e apaga-a. `acaso` só se passa em ENSAIO; a sério usa o gerador do sistema.
    [VALIDAR] Em Python «apagar» é o melhor possível: a linguagem pode deixar cópias em memória."""
    if not irmandade_ok(camaras, k):
        raise ValueError("cerimónia recusada: faltam câmaras africanas ou os restantes chegam sozinhos ao limiar")
    acaso = acaso or secrets.token_bytes
    sk = bytearray(acaso(32))
    pub = ed_publica(bytes(sk)).hex()
    partes = dict(zip(camaras, shamir_partir(int.from_bytes(sk, "big"), k, len(camaras), bytes(acaso(64)))))
    for i in range(len(sk)):
        sk[i] = 0
    lista = ["1. Sala sem rede; relógio e testemunhas registados."] + [
        f"{i}. {c}{' (câmara africana, participante de direito)' if c in CAMARAS_AFRICANAS else ''}: recebe a sua parte em mão; sela o recibo."
        for i, c in enumerate(camaras, 2)] + [
        f"{len(camaras) + 2}. Chave apagada da máquina; fica só a chave pública {pub[:16]}…",
        f"{len(camaras) + 3}. Qualquer decisão pede {k} de {len(camaras)}: nenhum trio se forma sem uma câmara africana."]
    return {"pub": pub, "partes": partes, "apagada": not any(sk), "checklist": lista, "k": k}


# --- S4: assinatura por limiar num processo à parte (o processo-pai nunca junta nem vê a chave)
def _filho_assinar() -> int:
    pedido = json.loads(sys.stdin.buffer.read().decode("utf-8"))
    sk = bytearray(shamir_juntar([(int(x), int(y)) for x, y in pedido["partes"]]).to_bytes(66, "big")[-32:])
    r = {"pub": ed_publica(bytes(sk)).hex(), "sig": ed_assinar(bytes(sk), bytes.fromhex(pedido["msg"])).hex()}
    for i in range(len(sk)):
        sk[i] = 0
    sys.stdout.write(json.dumps(r))
    return 0


def assinar_por_limiar(partes: Sequence[Tuple[int, int]], msg: bytes, pub_esperada: str) -> Dict[str, Any]:
    pedido = json.dumps({"partes": [[str(x), str(y)] for x, y in partes], "msg": msg.hex()}).encode("utf-8")
    p = subprocess.run([sys.executable, os.path.abspath(__file__), "--assinar-limiar"], input=pedido, capture_output=True)
    try:
        r = json.loads(p.stdout.decode("utf-8"))
    except ValueError:
        return {"estado": "RECUSADO_FILHO_FALHOU"}
    if not igual_seguro(r.get("pub"), pub_esperada):
        return {"estado": "RECUSADO_PARTES_NAO_RECONSTROEM_A_CHAVE"}
    ok = ed_verificar(bytes.fromhex(pub_esperada), msg, bytes.fromhex(r["sig"]))
    return {"estado": "ASSINADO" if ok else "RECUSADO_ASSINATURA_INVALIDA", "sig": r["sig"]}


# --- S5: contentor híbrido. A biblioteca-padrão não tem ML-DSA: a falha é dita, não escondida.
def selo_hibrido(obj: Any, sk: bytes, producao: bool = False) -> Dict[str, Any]:
    if producao:
        raise RuntimeError("PQC_EM_FALTA: produção exige Ed25519 + ML-DSA (FIPS 204) e este ficheiro só tem Ed25519")
    return {"classico": selar(obj, sk), "pqc": "PQC_EM_FALTA", "vale_em_producao": False}


# --- S6: ledger em disco, só a acrescentar, com fsync; ao arrancar relê e confere tudo
class LedgerPersistente(LedgerImutavel):
    def __init__(self, sk_notario: bytes, caminho: str) -> None:
        super().__init__(sk_notario)
        self.caminho = caminho
        if os.path.exists(caminho):
            with open(caminho, "rb") as fh:
                try:
                    self.blocos = [json.loads(l.decode("utf-8")) for l in fh.read().split(b"\n") if l]
                except ValueError:
                    raise RuntimeError("LEDGER_ILEGIVEL: o ficheiro não é o que esta ledger escreveu")
            if not conferir_blocos(self.blocos, self.pub):
                raise RuntimeError("LEDGER_CORROMPIDA: o ficheiro em disco não confere; não arranco por cima dele")

    def registar(self, dia: int, evento: str, payload: Any) -> str:
        atual = super().registar(dia, evento, payload)
        fd = os.open(self.caminho, os.O_WRONLY | os.O_APPEND | os.O_CREAT, 0o600)
        try:
            os.write(fd, canon(self.blocos[-1]) + b"\n")
            os.fsync(fd)
        finally:
            os.close(fd)
        return atual


# --- S7: exportação que qualquer pessoa confere SEM a chave do notário (só com a chave pública dele)
def exportar_ledger(livro: LedgerImutavel) -> Dict[str, Any]:
    return {"formato": "KONFIRMU-LEDGER/1", "pub_notario": livro.pub, "blocos": livro.blocos, "cabeca": livro.cabeca()}


def verificar_externo(pacote: Any, pub_conhecida: Optional[str] = None, cabeca_conhecida: Optional[str] = None) -> Dict[str, Any]:
    """Só diz CONFERE com a chave do notário conhecida por outro canal. Sem ela: COERENTE_NOTARIO_POR_CONFIRMAR (qualquer um
    monta uma ledger coerente com a sua chave). Cortar os últimos blocos só se vê com a cabeça publicada: cabeca_conhecida."""
    try:
        if set(pacote) != {"formato", "pub_notario", "blocos", "cabeca"} or pacote["formato"] != "KONFIRMU-LEDGER/1" \
                or not re.fullmatch(r"[0-9a-f]{64}", str(pacote["pub_notario"])):
            return {"estado": "RECUSADO_PACOTE_ILEGIVEL"}
        blocos, pub = pacote["blocos"], pacote["pub_notario"]
        if pub_conhecida is not None and not igual_seguro(pub, pub_conhecida):
            return {"estado": "RECUSADO_NOTARIO_DESCONHECIDO"}
        ok = conferir_blocos(blocos, pub) and (blocos[-1]["hash_atual"] if blocos else "0" * 64) == pacote["cabeca"]
    except (KeyError, TypeError, IndexError):
        return {"estado": "RECUSADO_PACOTE_ILEGIVEL"}
    if not ok:
        return {"estado": "NAO_CONFERE", "blocos": len(blocos)}
    if not blocos:
        return {"estado": "VAZIO", "blocos": 0}
    if cabeca_conhecida is not None and not igual_seguro(pacote["cabeca"], cabeca_conhecida):
        return {"estado": "RECUSADO_CABECA_DIFERENTE_DA_PUBLICADA", "blocos": len(blocos)}
    return {"estado": "CONFERE" if pub_conhecida is not None else "COERENTE_NOTARIO_POR_CONFIRMAR", "blocos": len(blocos)}


# --- S8: auditoria — 100 adulterações diferentes; todas têm de ser apanhadas
def auditoria(livro: LedgerImutavel, n: int = 100) -> Tuple[int, int]:
    apanhadas, m = 0, len(livro.blocos)
    for i in range(n):
        c = json.loads(json.dumps(livro.blocos))
        b, tipo = c[(i * 7) % m], i % 5
        if tipo == 0:
            b["payload"] = {"adulterado": i}
        elif tipo == 1:
            b["dia"] = b["dia"] + 1 + i
        elif tipo == 2:
            b["assinatura"] = b["assinatura"][:-1] + ("0" if b["assinatura"][-1] != "0" else "1")
        elif tipo == 3:
            b["hash_anterior"] = h256(f"falso/{i}".encode())
        else:
            del c[(i * 7) % m]
            if (i * 7) % m == m - 1:  # tirar o último bloco não parte a cadeia: só se vê pela cabeça publicada
                apanhadas += 1 if (c[-1]["hash_atual"] if c else "") != livro.cabeca() else 0
                continue
        apanhadas += 0 if conferir_blocos(c, livro.pub) else 1
    return apanhadas, n


# --- S9: vigia — canários e contadores em JSON
def vigia(livro: LedgerImutavel) -> Dict[str, Any]:
    eventos: Dict[str, int] = {}
    for b in livro.blocos:
        eventos[b["evento"]] = eventos.get(b["evento"], 0) + 1
    alarmes = auditar_canarios()
    return {"estado": "VERDE" if not alarmes and livro.verificar_integridade_cadeia() else "VERMELHO",
            "canarios_tocados": len(alarmes), "blocos": len(livro.blocos), "ledger_integra": livro.verificar_integridade_cadeia(),
            "eventos": dict(sorted(eventos.items()))}


# --- VETOS NOVOS
FORMULAS_24: Dict[str, Dict[str, Any]] = {
    "P2.GIBBS": {"id": "P2.GIBBS", "versao": "1.0.0", "nome": "veto de Gibbs",
                 "formula": "ΔG = ΔH − T · ΔS; ΔG > 0 com 95% de confiança = veto",
                 "unidades": {"dH": "kJ/mol", "T": "K", "dS": "J/mol/K", "saida": "kJ/mol"}, "etiqueta": "MEDIDO",
                 "fonte": "energia livre de Gibbs (termodinâmica química de manual) [VALIDAR: a ordem diz «ΔG>0 = molécula instável»; "
                          "em rigor ΔG de formação > 0 diz que a molécula não se forma sozinha a essa temperatura]",
                 "o_que_nao_garante": "não diz nada sobre a velocidade (cinética), nem sobre toxicidade; não substitui o ensaio de estabilidade do fármaco"},
    "P15.HIDRICO": {"id": "P15.HIDRICO", "versao": "1.0.0", "nome": "veto hídrico",
                    "formula": "saldo = recarga − consumo; consumo > recarga com 95% de confiança = veto",
                    "unidades": {"consumo": "m3/ano", "recarga": "m3/ano", "saida": "m3/ano"}, "etiqueta": "MEDIDO",
                    "fonte": "balanço de massa de um aquífero: não se tira mais do que entra",
                    "o_que_nao_garante": "não conhece a qualidade da água, anos de seca, nem quem está a jusante; a recarga tem de ser medida, não suposta"},
}


def veto_gibbs(dH: Grandeza, T: Grandeza, dS: Grandeza) -> Dict[str, Any]:
    if T.em("K")[0] <= 0.0:  # v2.8
        raise VetoFisico(f"T = {_n(T.em('K')[0], 1)} K: abaixo do zero absoluto não há temperatura")
    dG = dH - T * dS
    v, u = dG.em("kJ/mol")
    baixo, alto = faixa95(dG, "kJ/mol")
    r = {"dG_kj_mol": v, "u_kj_mol": u}
    if baixo > 0.0:
        raise VetoFisico(f"ΔG = {_n(v, 1)} ± {_n(u, 1)} kJ/mol, acima de zero a 95%: a esta temperatura não se sustenta sozinha")
    return dict(r, estado="DENTRO" if alto <= 0.0 else "REVISAO_HUMANA")


def veto_hidrico(consumo: Grandeza, recarga: Grandeza) -> Dict[str, Any]:
    saldo = recarga - consumo
    v, u = saldo.em("m3/ano")
    baixo, alto = faixa95(saldo, "m3/ano")
    if alto < 0.0:
        raise VetoBiofisico(f"consumo acima da recarga a 95%: faltam {_n(-v, 0)} ± {_n(u, 0)} m3 por ano; fora do ponto neutral")
    return {"saldo_m3_ano": v, "u_m3_ano": u, "estado": "DENTRO_DA_RECARGA" if baixo >= 0.0 else "REVISAO_HUMANA"}


# 21-C. v2.5 — A MATEMÁTICA DA ABUNDÂNCIA: ÍNDICE A_d, BUSCA COM PODA PELO VETO, PONTUAÇÃO
# -----------------------------------------------------------------------------
# A_d = min(1, disponível_d / necessidade_d), com a condição do ponto neutral: extração_d <= regeneração_d.
# A_total = o menor dos A_d: só há abundância quando todos os domínios lá estão ao mesmo tempo.
# [VALIDAR] O «teorema de trabalho» (para QUALQUER território há um mínimo global alcançável por enxames baratos) NÃO está
# provado aqui. O que este código mostra: com uma lista finita de n obras, o mínimo existe e encontra-se em tempo finito
# (2^n combinações), e o veto corta ramos inteiros porque a extração só cresce quando se junta uma obra. Com 12 obras são
# 4 096 combinações; com 60 são cerca de 1,15e18. Escolher obras de custo mínimo é da família dos problemas NP-difíceis:
# a poda ajuda tanto quanto os vetos morderem, e nada garante que chegue.
DOMINIOS = ("agua", "luz", "saneamento", "alimentos", "materiais")

FORMULAS_25: Dict[str, Dict[str, Any]] = {
    "P16.ABUNDANCIA": {"id": "P16.ABUNDANCIA", "versao": "1.0.0", "nome": "índice de abundância por domínio",
                       "formula": "A_d = min(1, disponível_d / necessidade_d); extração_d > regeneração_d a 95% = ABUNDANCIA_FALSA e "
                                  "A_sustentável_d = min(1, (disponível_d − (extração_d − regeneração_d)) / necessidade_d); A_total = min_d A_sustentável_d",
                       "unidades": {"disponivel": "a do domínio", "necessidade": "a do domínio", "extracao": "a do domínio", "regeneracao": "a do domínio", "saida": "1"},
                       "etiqueta": "ASSUMIDO",
                       "fonte": "definição da ordem do David de 20-11-2026 07:48 [VALIDAR: a regra do A_sustentável e o mínimo entre domínios são escolhas deste ficheiro]",
                       "o_que_nao_garante": "não diz quem fica sem acesso dentro do território (é uma média); a necessidade e a regeneração têm de ser medidas, não supostas; "
                                            "A = 1 num ano não promete o ano seguinte"},
    "P17.OLIMPIADA": {"id": "P17.OLIMPIADA", "versao": "1.0.0", "nome": "pontuação das olimpíadas da abundância",
                      "formula": "1.º veto violado = DESCLASSIFICADA; 2.º selo que não se reproduz = SEM_SELO; 3.º ordena por ΔA_total (maior primeiro); "
                                 "4.º empate: menor custo físico; 5.º empate: nome da equipa",
                      "unidades": {"dA": "1", "custo_fisico": "kWh"}, "etiqueta": "ASSUMIDO",
                      "fonte": "regulamento em rascunho, ordem do David de 20-11-2026 07:48",
                      "o_que_nao_garante": "pontua uma SIMULAÇÃO com os números do território-teste; não prova que a obra se constrói, quanto custa em dinheiro, nem que as pessoas a querem"},
}


def indice_abundancia(disponivel: Grandeza, necessidade: Grandeza, extracao: Grandeza, regeneracao: Grandeza, unidade: str) -> Dict[str, Any]:
    """A de um domínio, com incerteza. Unidades diferentes das do domínio dão TypeError."""
    for g in (disponivel, necessidade, extracao, regeneracao):
        if g.em(unidade)[0] < 0.0:  # v2.8
            raise ValueError("quantidades negativas não existem neste índice")
    if necessidade.em(unidade)[0] <= 0.0:
        raise ValueError("necessidade zero: o índice não se define (não há falta nem abundância a medir)")
    bruto, u = (disponivel / necessidade).em("1")
    excesso = extracao - regeneracao
    baixo, alto = faixa95(excesso, unidade)
    estado = "ABUNDANCIA_FALSA" if baixo > 0.0 else ("DENTRO_DA_REGENERACAO" if alto <= 0.0 else "REVISAO_HUMANA")
    sust = bruto if estado != "ABUNDANCIA_FALSA" else ((disponivel - excesso) / necessidade).em("1")[0]
    return {"A_bruto": min(1.0, bruto), "u": u, "A_sustentavel": max(0.0, min(1.0, sust)), "estado": estado}


def _avaliar(territorio: Dict[str, Any], config: Sequence[str]) -> Dict[str, Any]:
    """Conta simples, nas unidades declaradas no território (sem incerteza: é a simulação da prova)."""
    if any(territorio["necessidade"][d] <= 0.0 for d in DOMINIOS):  # v2.8
        raise ValueError("necessidade zero ou negativa num domínio: território recusado")
    obras = {o["id"]: o for o in territorio["obras"]}
    disp, extr = dict(territorio["disponivel"]), dict(territorio["extracao"])
    custo = 0.0
    for oid in sorted(set(config)):
        o = obras[oid]
        custo += o["custo_kwh"]
        for d, q in o.get("acrescenta", {}).items():
            disp[d] += q
        for d, q in o.get("extrai", {}).items():
            extr[d] += q
    vetos = sorted(d for d in DOMINIOS if extr[d] > territorio["regeneracao"][d])
    A = {d: min(1.0, disp[d] / territorio["necessidade"][d]) for d in DOMINIOS}
    return {"A": A, "A_total": min(A.values()), "vetos": vetos, "custo_kwh": custo, "config": sorted(set(config))}


def selo_de_solucao(territorio: Dict[str, Any], config: Sequence[str]) -> str:
    """Mesmo território + mesma lista de obras = mesmo hash."""
    return hobj({"territorio": hobj(territorio), "resultado": _avaliar(territorio, config)})


def procurar_configuracao(territorio: Dict[str, Any]) -> Dict[str, Any]:
    """Procura em profundidade a lista de obras mais barata com A = 1 em todos os domínios e nenhum veto.
    Corta um ramo inteiro quando a extração já passa a regeneração (juntar obras nunca a baixa) ou quando o custo já não ganha."""
    obras, n = territorio["obras"], len(territorio["obras"])
    conta = {"possiveis": 2 ** n, "nos_visitados": 0, "ramos_cortados_veto": 0, "ramos_cortados_custo": 0, "folhas_avaliadas": 0}
    melhor: List[Any] = [None, math.inf]

    def desce(i: int, escolhidas: List[str], extr: Dict[str, float], custo: float) -> None:
        conta["nos_visitados"] += 1
        if any(extr[d] > territorio["regeneracao"][d] for d in DOMINIOS):
            conta["ramos_cortados_veto"] += 1
            return
        if custo >= melhor[1]:
            conta["ramos_cortados_custo"] += 1
            return
        if i == n:
            conta["folhas_avaliadas"] += 1
            if _avaliar(territorio, escolhidas)["A_total"] >= 1.0:
                melhor[0], melhor[1] = list(escolhidas), custo
            return
        o = obras[i]
        e2 = dict(extr)
        for d, q in o.get("extrai", {}).items():
            e2[d] += q
        desce(i + 1, escolhidas + [o["id"]], e2, custo + o["custo_kwh"])
        desce(i + 1, escolhidas, extr, custo)

    desce(0, [], dict(territorio["extracao"]), 0.0)
    return dict(conta, melhor=None if melhor[0] is None else _avaliar(territorio, melhor[0]))


def procurar_a_bruta(territorio: Dict[str, Any]) -> Any:
    """Todas as 2^n combinações, sem poda: serve só para conferir a busca com poda."""
    ids = [o["id"] for o in territorio["obras"]]
    boas = [r for r in (_avaliar(territorio, c) for k in range(len(ids) + 1) for c in itertools.combinations(ids, k)) if not r["vetos"] and r["A_total"] >= 1.0]
    return min(boas, key=lambda r: (r["custo_kwh"], r["config"])) if boas else None


def pontuar_olimpiada(territorio: Dict[str, Any], inscricoes: Sequence[Dict[str, Any]]) -> List[Dict[str, Any]]:
    antes = _avaliar(territorio, [])["A_total"]
    tabela = []
    for ins in inscricoes:
        r = _avaliar(territorio, ins["config"])
        estado = "DESCLASSIFICADA" if r["vetos"] else ("SEM_SELO" if not igual_seguro(ins.get("selo"), selo_de_solucao(territorio, ins["config"])) else "PONTUADA")
        tabela.append({"equipa": ins["equipa"], "estado": estado, "dA": round(r["A_total"] - antes, 12), "custo_kwh": r["custo_kwh"], "vetos": r["vetos"]})
    ordem = {"PONTUADA": 0, "SEM_SELO": 1, "DESCLASSIFICADA": 2}
    tabela.sort(key=lambda t: (ordem[t["estado"]], -t["dA"], t["custo_kwh"], t["equipa"]))
    for t in tabela:
        t["lugar"] = (1 + sum(1 for x in tabela if x["estado"] == "PONTUADA" and tabela.index(x) < tabela.index(t))) if t["estado"] == "PONTUADA" else None
    return tabela


TERRITORIO_DEMO: Dict[str, Any] = {
    "nome": "distrito de DEMO (números inventados, [ASSUMIDO])",
    "unidades": {"agua": "m3/dia", "luz": "kWh/dia", "saneamento": "pessoa", "alimentos": "refeição/dia", "materiais": "t/mês", "custo": "kWh de energia gasta a construir"},
    "necessidade": {"agua": 1000.0, "luz": 5000.0, "saneamento": 10000.0, "alimentos": 25000.0, "materiais": 40.0},
    "disponivel": {"agua": 600.0, "luz": 2000.0, "saneamento": 3000.0, "alimentos": 18000.0, "materiais": 10.0},
    "extracao": {"agua": 600.0, "luz": 2000.0, "saneamento": 0.0, "alimentos": 18000.0, "materiais": 10.0},
    "regeneracao": {"agua": 1100.0, "luz": 9000.0, "saneamento": 0.0, "alimentos": 30000.0, "materiais": 45.0},
    "obras": [
        {"id": "reparar_fugas", "custo_kwh": 8000.0, "acrescenta": {"agua": 150.0}},
        {"id": "furo_raso", "custo_kwh": 20000.0, "acrescenta": {"agua": 250.0}, "extrai": {"agua": 250.0}},
        {"id": "furo_fundo", "custo_kwh": 30000.0, "acrescenta": {"agua": 600.0}, "extrai": {"agua": 600.0}},
        {"id": "captar_chuva", "custo_kwh": 15000.0, "acrescenta": {"agua": 120.0}},
        {"id": "solar_aldeia", "custo_kwh": 90000.0, "acrescenta": {"luz": 3000.0}, "extrai": {"luz": 3000.0}},
        {"id": "solar_telhados", "custo_kwh": 50000.0, "acrescenta": {"luz": 1500.0}, "extrai": {"luz": 1500.0}},
        {"id": "latrinas_secas", "custo_kwh": 40000.0, "acrescenta": {"saneamento": 7000.0}},
        {"id": "rede_de_esgoto", "custo_kwh": 120000.0, "acrescenta": {"saneamento": 7000.0}, "extrai": {"agua": 150.0}},
        {"id": "horta_regada", "custo_kwh": 25000.0, "acrescenta": {"alimentos": 7000.0}, "extrai": {"alimentos": 7000.0, "agua": 100.0}},
        {"id": "monocultura", "custo_kwh": 15000.0, "acrescenta": {"alimentos": 12000.0}, "extrai": {"alimentos": 14000.0}},
        {"id": "reciclagem", "custo_kwh": 35000.0, "acrescenta": {"materiais": 30.0}},
        {"id": "pedreira", "custo_kwh": 20000.0, "acrescenta": {"materiais": 30.0}, "extrai": {"materiais": 40.0}},
    ],
}


# 21-D. v2.6 — RESPOSTA MÍNIMA SELADA + CACHE + BENCHMARK v3 (peça de referência para a /v1/facto)
# -----------------------------------------------------------------------------
# [VALIDAR] Esta janela não chega ao código da API nem ao BASELINE-TOP1 verdadeiro. O que aqui está é a peça pronta a ligar:
# o formato, a cache, a invalidação e o banco de ensaio, com um «top-1» simples no lugar do verdadeiro.
# [VALIDAR] Tokens: a biblioteca-padrão não tem o tokenizador de nenhum modelo. Conta-se 1 token por cada 4 bytes UTF-8,
# arredondado para cima. Serve para comparar duas respostas entre si; o número a sério mede-se na API.
# [VALIDAR] Os 5 campos (facto, fonte, data, hash, nao_garante) são escolha deste ficheiro: a ordem diz «5 campos» sem os nomear.
CAMPOS_MINIMA = ("facto", "fonte", "data", "hash", "nao_garante")
_PALAVRAS_VAZIAS = frozenset("a o as os um uma de do da dos das em no na nos nas e ou que qual quais quando quantos quantas quanto como foi foram e é são ser teve tem por para com se ao à aos às segundo the of".split())


def contar_tokens(texto: str) -> int:
    return -(-len(texto.encode("utf-8")) // 4)


def _palavras(texto: str) -> List[str]:
    sem_acentos = "".join(c for c in unicodedata.normalize("NFD", texto.lower()) if unicodedata.category(c) != "Mn")
    return [p for p in re.findall(r"[a-z0-9]+", sem_acentos) if p not in _PALAVRAS_VAZIAS]


def hash_da_ficha(ficha: Dict[str, Any]) -> str:
    return hobj({k: ficha[k] for k in ("id", "facto", "fonte", "data", "nao_garante")})


def resposta_minima(ficha: Dict[str, Any]) -> Dict[str, Any]:
    """Os 5 campos + expansao_disponivel. O hash vai inteiro: é ele que deixa conferir a ficha."""
    return {"facto": ficha["facto"], "fonte": ficha["fonte"], "data": ficha["data"], "hash": hash_da_ficha(ficha),
            "nao_garante": ficha["nao_garante"], "expansao_disponivel": True}


def resposta_em_prosa(ficha: Dict[str, Any]) -> str:
    """Molde de DEMO do que uma resposta corrida costuma trazer. O banco de ensaio aceita a prosa verdadeira, gravada, no lugar desta."""
    return ("Boa pergunta. Com base na informação disponível nas fontes que consultei, posso dizer-te o seguinte. " + ficha["facto"] + " "
            "Esta informação vem de uma fonte que podes consultar diretamente: " + ficha["fonte"] + ". A última verificação que tenho registada é de " + ficha["data"] + ". "
            "É importante ter em conta um limite: " + ficha["nao_garante"] + ". Se quiseres, posso explicar o contexto com mais pormenor, "
            "mostrar o trecho exato da fonte ou indicar outras fichas relacionadas com este assunto. Diz-me como preferes continuar.")


def top1_simples(fichas: Sequence[Dict[str, Any]], pergunta: str, limiar: float = 1.0) -> Optional[Dict[str, Any]]:
    """Fica no lugar do BASELINE-TOP1. v2.8: responde só se TODAS as palavras com conteúdo da pergunta estão numa ficha, se a pergunta
    tem pelo menos 2 e se nenhuma outra ficha empata. Na dúvida recusa: recusar custa uma pergunta; responder errado custa a confiança.
    (Na v2.7, com limiar 0,5, respondia com confiança a 9 de 12 perguntas que não cobria: «Bíblia de Lutero» recebia Gutenberg.)"""
    p = set(_palavras(pergunta))
    if len(p) < 2:
        return None
    pontos = sorted(((len(p & set(_palavras(f["facto"] + " " + " ".join(f.get("chaves", []))))) / len(p), f["id"]) for f in fichas), key=lambda x: (-x[0], x[1]))
    if not pontos or pontos[0][0] < limiar or (len(pontos) > 1 and pontos[1][0] == pontos[0][0]):
        return None
    return next(f for f in fichas if f["id"] == pontos[0][1])


class CacheDeFactos:
    """Chave = palavras da pergunta sem acentos e sem palavras vazias, pela ordem em que vêm. [VALIDAR] Apanha maiúsculas, acentos e
    pontuação; NÃO apanha a mesma pergunta com outra ordem; NÃO apanha sinónimos (isso pede vetores, que a biblioteca-padrão não tem).
    Acerto: devolve só os 16 primeiros caracteres do hash da ficha (o cliente já a tem e confere pelo hash inteiro). [VALIDAR] 16
    caracteres = 64 bits: chega para apontar a ficha; a prova é o hash inteiro que veio na 1.ª resposta. Falha: corre o caminho normal e guarda.
    A fonte mudou (aviso do motor de diferenças) = todas as entradas dessa ficha morrem."""

    def __init__(self, fichas: Sequence[Dict[str, Any]], top1: Any = top1_simples) -> None:
        self.fichas = {f["id"]: dict(f) for f in fichas}
        self.top1 = top1
        self.entradas: Dict[str, Tuple[str, str]] = {}
        self.conta = {"acertos": 0, "falhas": 0, "fora_da_cobertura": 0, "mortas_por_fonte_mudada": 0}

    @staticmethod
    def chave(pergunta: str) -> str:
        return h256(" ".join(_palavras(pergunta)).encode("utf-8"))  # v2.8: a ordem fica — «o cão mordeu o homem» ≠ «o homem mordeu o cão»

    def responder(self, pergunta: str) -> Dict[str, Any]:
        k = self.chave(pergunta)
        if k in self.entradas:
            fid, h = self.entradas[k]
            if fid in self.fichas and igual_seguro(hash_da_ficha(self.fichas[fid]), h):
                self.conta["acertos"] += 1
                return {"c": 1, "h": h[:16]}
            del self.entradas[k]  # defesa: a ficha mudou sem aviso
            self.conta["mortas_por_fonte_mudada"] += 1
        ficha = self.top1(list(self.fichas.values()), pergunta)
        if ficha is None:
            self.conta["fora_da_cobertura"] += 1
            return {"facto": None, "estado": "FORA_DA_COBERTURA"}
        self.conta["falhas"] += 1
        r = resposta_minima(ficha)
        self.entradas[k] = (ficha["id"], r["hash"])
        return r

    def fonte_mudou(self, ficha_id: str, nova: Optional[Dict[str, Any]] = None) -> int:
        """Chamada pelo motor de diferenças. Devolve quantas entradas morreram."""
        mortas = [k for k, (fid, _) in self.entradas.items() if fid == ficha_id]
        for k in mortas:
            del self.entradas[k]
        self.conta["mortas_por_fonte_mudada"] += len(mortas)
        if nova is None:
            self.fichas.pop(ficha_id, None)
        else:
            self.fichas[ficha_id] = dict(nova)
        return len(mortas)


def benchmark_v3(fichas: Sequence[Dict[str, Any]], perguntas: Sequence[Dict[str, Any]], meta: float = 0.99) -> Dict[str, Any]:
    """Cada pergunta: {"pergunta", "esperado": id da ficha ou None (fora da cobertura), "prosa": texto verdadeiro gravado (opcional)}.
    Dois números, sem os misturar: dentro da cobertura e fora dela."""
    por_id = {f["id"]: f for f in fichas}
    cache = CacheDeFactos(fichas)
    dentro, fora = [], []
    for q in perguntas:
        frio = cache.responder(q["pergunta"])
        quente = cache.responder(q["pergunta"])
        if q.get("esperado") is None:
            fora.append({"recusou": frio.get("estado") == "FORA_DA_COBERTURA", "tokens": contar_tokens(canon(frio).decode("utf-8"))})
            continue
        certa = frio.get("hash") == hash_da_ficha(por_id[q["esperado"]])
        t_prosa = contar_tokens(q.get("prosa") or resposta_em_prosa(por_id[q["esperado"]]))
        t_min, t_cache = contar_tokens(canon(frio).decode("utf-8")), contar_tokens(canon(quente).decode("utf-8"))
        dentro.append({"certa": certa, "t_prosa": t_prosa, "t_minima": t_min, "t_cache": t_cache,
                       "poupanca_minima": 1.0 - t_min / t_prosa, "poupanca_cache": 1.0 - t_cache / t_prosa})
    med = lambda xs: statistics.median(xs) if xs else None
    r = {"perguntas": len(perguntas),
         "dentro": {"n": len(dentro), "ficha_certa": sum(1 for d in dentro if d["certa"]),
                    "mediana_tokens_prosa": med([d["t_prosa"] for d in dentro]), "mediana_tokens_minima": med([d["t_minima"] for d in dentro]),
                    "mediana_tokens_cache": med([d["t_cache"] for d in dentro]),
                    "mediana_poupanca_minima": med([d["poupanca_minima"] for d in dentro]), "mediana_poupanca_cache": med([d["poupanca_cache"] for d in dentro])},
         "fora": {"n": len(fora), "recusou_bem": sum(1 for f in fora if f["recusou"]), "mediana_tokens": med([f["tokens"] for f in fora])},
         "meta": meta}
    mp = r["dentro"]["mediana_poupanca_cache"]
    r["meta_atingida"] = bool(mp is not None and mp >= meta)
    r["prosa_minima_para_a_meta_tokens"] = None if not dentro else math.ceil(r["dentro"]["mediana_tokens_cache"] / (1.0 - meta))
    r["sha256"] = hobj(r)
    return r


def relatorio_benchmark(r: Dict[str, Any]) -> List[str]:
    d, f = r["dentro"], r["fora"]
    pc = lambda x: "—" if x is None else _n(100.0 * x, 1) + "%"
    return [f"DENTRO da cobertura ({d['n']} perguntas): ficha certa em {d['ficha_certa']}/{d['n']}; medianas: prosa {_num(d['mediana_tokens_prosa'])} tokens, "
            f"mínima {_num(d['mediana_tokens_minima'])}, cache {_num(d['mediana_tokens_cache'])}; poupança mediana: mínima {pc(d['mediana_poupanca_minima'])}, cache {pc(d['mediana_poupanca_cache'])}",
            f"FORA da cobertura ({f['n']} perguntas): recusou bem {f['recusou_bem']}/{f['n']} (responde «FORA_DA_COBERTURA», não inventa); mediana {_num(f['mediana_tokens'])} tokens",
            f"META >= {pc(r['meta'])} de poupança mediana dentro da cobertura: " + ("ATINGIDA" if r["meta_atingida"] else "NÃO ATINGIDA")
            + f" — a conta: com {_num(d['mediana_tokens_cache'])} tokens por acerto de cache, a prosa tem de ter pelo menos {r['prosa_minima_para_a_meta_tokens']} tokens",
            "sha256 do relatório: " + r["sha256"]]


FICHAS_DEMO: List[Dict[str, Any]] = [
    {"id": "KF-DEMO-001", "facto": "A Bíblia de Gutenberg teve uma tiragem de cerca de 180 exemplares.", "fonte": "https://www.loc.gov/exhibits/bibles/interactives/gutenberg/index.html",
     "data": "2026-11-20", "nao_garante": "o número exato não é conhecido; as estimativas vão de 158 a 180", "chaves": ["quantos", "copias", "impressos", "imprimiu"]},
    {"id": "KF-DEMO-002", "facto": "O primeiro Index Librorum Prohibitorum foi publicado em 1559.", "fonte": "https://www.britannica.com/print/article/285220",
     "data": "2026-11-20", "nao_garante": "houve listas locais de livros proibidos antes desta", "chaves": ["indice", "livros", "proibidos", "ano", "igreja"]},
    {"id": "KF-DEMO-003", "facto": "Em 1465 o arcebispo de Mainz atribuiu uma pensão a Gutenberg.", "fonte": "https://www.britannica.com/biography/Johannes-Gutenberg/Printing-of-the-Bible",
     "data": "2026-11-20", "nao_garante": "não diz quanto valia a pensão em dinheiro", "chaves": ["recebeu", "velhice", "pobre"]},
    {"id": "KF-DEMO-004", "facto": "O processo de Fust contra Gutenberg tem a data de 6 de novembro de 1455.", "fonte": "https://historyofinformation.com/detail.php?entryid=342",
     "data": "2026-11-20", "nao_garante": "o desfecho do processo não está claramente documentado", "chaves": ["tribunal", "divida", "emprestimo"]},
    {"id": "KF-DEMO-005", "facto": "A revista Philosophical Transactions começou a ser publicada em 1665.", "fonte": "https://research-repository.st-andrews.ac.uk/handle/10023/11178",
     "data": "2026-11-20", "nao_garante": "a revisão por pares como hoje a conhecemos é posterior", "chaves": ["cientifica", "primeira", "royal", "society"]},
    {"id": "KF-DEMO-006", "facto": "A OMS diz que entre 30 e 50% de todos os casos de cancro são evitáveis.", "fonte": "OMS, «Preventing cancer»",
     "data": "2026-11-20", "nao_garante": "não substitui tratamento clínico; é um valor para a população, não para uma pessoa", "chaves": ["prevencao", "prevenir", "percentagem"]},
]

PERGUNTAS_DEMO: List[Dict[str, Any]] = [
    {"pergunta": "Quantos exemplares teve a Bíblia de Gutenberg?", "esperado": "KF-DEMO-001"},
    {"pergunta": "Em que ano foi publicado o primeiro Index Librorum Prohibitorum?", "esperado": "KF-DEMO-002"},
    {"pergunta": "Gutenberg recebeu uma pensão do arcebispo de Mainz?", "esperado": "KF-DEMO-003"},
    {"pergunta": "Qual é a data do processo de Fust contra Gutenberg?", "esperado": "KF-DEMO-004"},
    {"pergunta": "Quando começou a ser publicada a Philosophical Transactions?", "esperado": "KF-DEMO-005"},
    {"pergunta": "Que percentagem dos casos de cancro são evitáveis, segundo a OMS?", "esperado": "KF-DEMO-006"},
    {"pergunta": "Índice de livros proibidos da Igreja: em que ano?", "esperado": "KF-DEMO-002"},
    {"pergunta": "A tiragem da Bíblia de Gutenberg foi de quantas cópias?", "esperado": "KF-DEMO-001"},
    {"pergunta": "Qual é o salário mínimo nos Países Baixos em 2027?", "esperado": None},
    {"pergunta": "Quanto custa um bilhete de comboio de Lisboa ao Porto?", "esperado": None},
    {"pergunta": "Quem ganhou o campeonato do mundo de futebol?", "esperado": None},
    {"pergunta": "Posso tomar ibuprofeno com paracetamol?", "esperado": None},
]


# 21-E. v2.7 — ENXAME FRUGAL: o «enxame_ultra_frugal.py» de outra IA (recebido a 20-11-2026, 08:47) posto à prova e refeito
# -----------------------------------------------------------------------------
# O que a prova mostrou no código recebido (sha256 896330e2…), e o que aqui muda:
# 1. Cache por «balde» round(valor / tolerância): 0,217 e 0,218 (tolerância 0,015) caem em baldes diferentes e 0,2176 e 0,2324
#    no mesmo; e a chave só tem o domínio: Maputo responde por Lisboa e uma dose responde por uma temperatura.
#    Aqui: a chave é o CONTEXTO inteiro (o quê, onde, unidade) e «mesma medida» decide-se pela incerteza das duas leituras.
# 2. Esquema de 1 letra: poupa, mas menos do que o anunciado, e a tabela paga-se. Aqui mede-se e diz-se a partir de quantas fichas compensa.
# 3. «Selo» = SHAKE-256 do conteúdo: é um hash, não uma assinatura. Aqui a ficha curta leva o hash e sela-se com Ed25519 como tudo o resto.
# 4. zlib + Base85: o Base85 usa o acento grave, que não existe no alfabeto GSM de 7 bits: o SMS passa a UCS-2 (67 caracteres
#    por segmento em vez de 153). Aqui usa-se Base64 e contam-se os segmentos.
# v2.8: comparar duas leituras usa k = 1,96 (dos dois lados); faixa95, de um lado só, fica para os vetos.
# [VALIDAR] «compatível» não é transitivo (a~b e b~c não dá a~c): a cache devolve a leitura compatível mais próxima.
# [VALIDAR] o alfabeto GSM foi escrito de memória (GSM 03.38); o tamanho comprimido pode mudar com a versão da zlib.
TABELA_CURTA = {"i": "ficha_id", "d": "dominio", "e": "etiqueta", "v": "valores", "l": "o_que_nao_garante", "p": "hash_anterior", "h": "hash"}
ETIQUETAS_CURTAS = {"MED": "MEDIDO", "ASS": "ASSUMIDO", "CEN": "CENARIO"}
GSM7_BASICO = frozenset("@£$¥èéùìòÇ\nØø\rÅåΔ_ΦΓΛΩΠΨΣΘΞÆæßÉ !\"#¤%&'()*+,-./0123456789:;<=>?¡ABCDEFGHIJKLMNOPQRSTUVWXYZÄÖÑÜ§¿abcdefghijklmnopqrstuvwxyzäöñüà")
GSM7_EXTENSAO = frozenset("^{}\\[~]|€")


def compativeis(a: Grandeza, b: Grandeza, unidade: str) -> bool:
    """Duas leituras são «a mesma medida» quando zero cabe no intervalo a 95% da diferença (a incerteza das duas conta).
    v2.8: 95% dos DOIS lados (k = 1,96). Com o k = 1,645 de um lado só, 10% das leituras iguais saíam «diferentes» (medido: 40 000 pares)."""
    v, u = (a - b).em(unidade)
    return abs(v) <= 1.96 * u


class CacheGUM:
    """Antes de perguntar a um modelo: já há uma ficha deste contexto com uma leitura compatível? Se sim, 0 chamadas."""

    def __init__(self) -> None:
        self.por_contexto: Dict[str, List[Tuple[Grandeza, Dict[str, Any]]]] = {}
        self.conta = {"reutilizadas": 0, "novas": 0}

    def procurar(self, contexto: Dict[str, Any], leitura: Grandeza) -> Optional[Dict[str, Any]]:
        u = contexto["unidade"]
        boas = [(abs(leitura.em(u)[0] - g.em(u)[0]), f["ficha_id"], f) for g, f in self.por_contexto.get(hobj(contexto), []) if compativeis(leitura, g, u)]
        if not boas:
            return None
        self.conta["reutilizadas"] += 1
        return min(boas, key=lambda x: (x[0], x[1]))[2]

    def guardar(self, contexto: Dict[str, Any], leitura: Grandeza, ficha: Dict[str, Any]) -> None:
        leitura.em(contexto["unidade"])
        self.por_contexto.setdefault(hobj(contexto), []).append((leitura, ficha))
        self.conta["novas"] += 1


def ficha_curta(ficha: Dict[str, Any]) -> Dict[str, Any]:
    """Nomes de 1 letra e etiqueta de 3. Recusa ficha sem limite escrito ou com etiqueta desconhecida."""
    inv_n, inv_e = {v: k for k, v in TABELA_CURTA.items()}, {v: k for k, v in ETIQUETAS_CURTAS.items()}
    if set(ficha) != set(inv_n) or ficha["etiqueta"] not in inv_e or not str(ficha["o_que_nao_garante"]).strip():
        raise ValueError("ficha recusada: campos em falta, etiqueta desconhecida ou o_que_nao_garante vazio")
    return {inv_n[k]: (inv_e[v] if k == "etiqueta" else v) for k, v in ficha.items()}


def ficha_longa(curta: Dict[str, Any]) -> Dict[str, Any]:
    return {TABELA_CURTA[k]: (ETIQUETAS_CURTAS[v] if k == "e" else v) for k, v in curta.items()}


def custo_do_esquema_curto(fichas: Sequence[Dict[str, Any]]) -> Dict[str, Any]:
    longo = contar_tokens(canon(list(fichas)).decode("utf-8"))
    curto = contar_tokens(canon([ficha_curta(f) for f in fichas]).decode("utf-8"))
    tabela = contar_tokens(canon({"n": TABELA_CURTA, "e": ETIQUETAS_CURTAS}).decode("utf-8"))
    por_ficha = (longo - curto) / len(fichas)
    return {"tokens_longo": longo, "tokens_curto": curto, "tokens_tabela": tabela, "poupanca": 1.0 - curto / longo,
            "compensa_a_partir_de_fichas": math.floor(tabela / por_ficha) + 1}


def segmentos_sms(texto: str) -> Dict[str, Any]:
    """Quantos SMS leva um texto. GSM de 7 bits: 160 septetos, ou 153 por segmento; fora desse alfabeto: UCS-2, 70 ou 67."""
    if all(c in GSM7_BASICO or c in GSM7_EXTENSAO for c in texto):
        n = len(texto) + sum(1 for c in texto if c in GSM7_EXTENSAO)
        return {"alfabeto": "GSM-7", "unidades": n, "segmentos": 1 if n <= 160 else -(-n // 153)}
    n = len(texto.encode("utf-16-be")) // 2
    return {"alfabeto": "UCS-2", "unidades": n, "segmentos": 1 if n <= 70 else -(-n // 67)}


def pacote_de_rede(fichas: Sequence[Dict[str, Any]], base: str = "b64") -> str:
    z = zlib.compress(canon([ficha_curta(f) for f in fichas]), 9)
    return (base64.b85encode(z) if base == "b85" else base64.b64encode(z)).decode("ascii")


def abrir_pacote_de_rede(pacote: str, base: str = "b64") -> List[Dict[str, Any]]:
    z = base64.b85decode(pacote) if base == "b85" else base64.b64decode(pacote)
    return [ficha_longa(c) for c in json.loads(zlib.decompress(z).decode("utf-8"))]


def _balde_da_outra_suite(dominio: str, valor: float, tolerancia: float) -> str:
    """A chave de cache do código recebido, copiada para a comparação (EUPL-1.2 no original)."""
    return f"{dominio}:{round(valor / max(1e-9, tolerancia))}"


# =========================== P51 a P54 — A BASE-MÃE DENTRO DA CALCULADORA (v3.0) ===========================
# As descobertas da base-mãe (11_ARTEFACTOS/2026-11-21_KONFIRMU_CALC_BASE_MAE_v0.1, registo descobertas.json) entram aqui
# TAL E QUAL: o mesmo texto e o mesmo SHA-256 que o registo guarda. Não são cópias reescritas: são os ficheiros.
# A calculadora dá-lhes as SUAS peças — o módulo «base_v28» que elas pedem passa a ser esta calculadora inteira — e confere
# o hash de cada ficheiro antes de o correr: um byte mexido e recusa. As baterias de testes vêm junto e o demo corre-as
# sobre estas peças, sem rede e sem sorteios: têm de dar as mesmas saídas (SHA-256) que deram na base-mãe.
# D-000 = a base (P3) · P51 = D-001 quórum por cadeias independentes · P52 = D-002 aritmética exacta do KCP ·
# P53 = D-003 FROST RFC 9591 (vetores oficiais) · P54 = D-004 DKG, a chave nascida a várias mãos (vetores da Zcash Foundation).
_BASE_MAE_FICHEIROS: Dict[str, Tuple[str, str]] = {
    "quorum_multibloco.py": ("ebbd7956b81a6f6b1a05766f4f6598ff522a93fae9dd9f3460a9feae865635f3", r'''# -*- coding: utf-8 -*-
"""P9 v2.9 — quórum multi-bloco: cada voto contado precisa de uma cadeia de confiança só sua.

Ordem do David, 21-11-2026 (P0 do red team, achado B1). Substitui a regra de contagem da v1.0 à v2.8
(«votantes que partilham 2 ou mais padrinhos contam como 1»): com ela, 3 pessoas em conluio
admitiram identidades que se apadrinhavam umas às outras e contaram 13 votos.

Regra nova: os votos contados são o número máximo de votantes que chegam às raízes (os membros da
fundação) por cadeias de atestados que não partilham NENHUM membro. Pelo teorema de Menger, é o
tamanho do menor grupo de membros que separa os votantes das raízes: para fabricar k votos é preciso
ter k membros reais diferentes nesse corte. Cálculo: fluxo máximo com capacidade 1 em cada membro
(Edmonds-Karp), por ordem fixa: o mesmo grafo dá sempre a mesma contagem e as mesmas cadeias.

O_QUE_NAO_GARANTE: k membros reais em conluio, cada um com a sua cadeia até às raízes, continuam a
fazer k votos. Pessoas honestas apadrinhadas pelas mesmas 3 pessoas contam no máximo 3: na dúvida a
regra conta menos. O grafo não prova identidade; prova só que k votos contados têm k cadeias que não
se cruzam. [VALIDAR] «multi-bloco» lido como «blocos de confiança independentes»; se queria dizer
votos espalhados por vários blocos da ledger, é outra regra, que se junta a esta.
"""
from __future__ import annotations

from collections import deque
from typing import Any, Dict, Iterable, List, Sequence, Tuple

import base_v28 as _B

_S, _T = ("<", ""), (">", "")


def cadeias_independentes(atestados: Dict[str, Any], membros: Iterable[str],
                          votantes: Sequence[str]) -> Tuple[int, List[List[str]]]:
    """(votos contados, cadeias). Cada cadeia vai do votante até uma raiz; nenhum membro aparece em duas."""
    membros = set(membros)
    raizes = {m for m in membros if m not in atestados}
    alvo = sorted(set(votantes) & membros)
    vistos, fila = set(), deque(alvo)
    while fila:  # só os antepassados dos votantes entram nas contas
        m = fila.popleft()
        if m in vistos:
            continue
        vistos.add(m)
        for a in sorted(atestados.get(m, ())):
            if a in membros and a not in vistos:
                fila.append(a)
    cap: Dict[Any, Dict[Any, int]] = {}
    originais = set()

    def aresta(u: Any, v: Any) -> None:
        cap.setdefault(u, {})[v] = 1
        cap.setdefault(v, {}).setdefault(u, 0)
        originais.add((u, v))

    for m in sorted(vistos):
        aresta(("e", m), ("s", m))          # cada membro só pode estar numa cadeia
        for a in sorted(atestados.get(m, ())):
            if a in vistos:
                aresta(("s", m), ("e", a))  # de quem entrou para quem o apadrinhou
        if m in raizes:
            aresta(("s", m), _T)
    for v in alvo:
        aresta(_S, ("e", v))
    fluxo = 0
    while True:
        pai: Dict[Any, Any] = {_S: None}
        fila = deque([_S])
        while fila and _T not in pai:
            u = fila.popleft()
            for v in sorted(cap.get(u, {})):
                if cap[u][v] > 0 and v not in pai:
                    pai[v] = u
                    fila.append(v)
        if _T not in pai:
            break
        v = _T
        while pai[v] is not None:
            u = pai[v]
            cap[u][v] -= 1
            cap[v][u] += 1
            v = u
        fluxo += 1
    usados = {(u, v) for (u, v) in originais if cap[u][v] == 0}
    seguinte = {u: v for (u, v) in usados if u != _S}
    cadeias = []
    for (u, v) in sorted(usados):
        if u != _S:
            continue
        cadeia, n = [], v
        while n != _T:
            if n[0] == "e":
                cadeia.append(n[1])
            n = seguinte[n]
        cadeias.append(cadeia)
    return fluxo, sorted(cadeias)


class AldeiaMultibloco(_B.Aldeia):
    """A Aldeia da v2.9: admitir, selos, prazos e limite de carimbos ficam como na v2.8; muda só a contagem."""

    def _grupos(self, ps: Sequence[str]) -> int:
        return cadeias_independentes(self.atestados, self.membros, ps)[0]

    def cadeias(self, ps: Sequence[str]) -> List[List[str]]:
        """Para o dossiê: que cadeia sustenta cada voto contado."""
        return cadeias_independentes(self.atestados, self.membros, ps)[1]
'''),
    "kcp_exacto.py": ("3f4c85e3dd4e8ef2bde324351c1ea0d6e3cc044e92f7c9a2bc095e8d14126c11", r'''# -*- coding: utf-8 -*-
"""KCP — aritmética exacta e leitura estrita (correções para a v2.9).

Achados do red team de 21-11-2026: K1 (reais com mais de 12 algarismos: um selo cobre valores diferentes),
K1c (1 e 1.0 dão bytes diferentes; leitores que não distinguem divergem), K3 (nomes repetidos no JSON),
K4 (encontrado ao corrigir: dois nomes que só diferem na forma Unicode fundem-se em silêncio no NFC da v2.8).

Não muda a forma canónica KCP-JSON: os selos KCP/0.1 e KCP/0.2 já emitidos continuam a verificar.
Muda duas coisas:
1. O VERIFICADOR lê o JSON recebido de forma estrita (nomes repetidos, nomes que colidem em NFC,
   NaN e infinito = NÃO VERIFICADO) e DEVOLVE o que foi selado (`selado`, lido dos bytes C) e a lista
   do que o texto recebido mostra de diferente (`diferencas`). Quem mostra um selo a uma pessoa mostra o
   `selado`, nunca o texto recebido. Com `estrito=True` (dinheiro, prazos), qualquer diferença = NÃO VERIFICADO.
2. O EMISSOR (`selar_kcp`) só sela o que fica exacto nos bytes: sem reais que percam algarismos, sem
   reais com valor inteiro (100.0 -> usa 100), inteiros até 2^53 - 1 (I-JSON, RFC 7493), texto e nomes em NFC.

O_QUE_NAO_GARANTE: não decide como se escrevem os reais em texto para outras linguagens (1e-06 ou 0.000001):
isso é uma escolha do KCP/0.3 (ou o JCS, RFC 8785). Não corrige selos antigos: mostra o que eles selaram.
"""
from __future__ import annotations

import hmac
import json
import math
import unicodedata
from typing import Any, Dict, Iterable, List, Optional

import base_v28 as B

LIMITE_INTEIRO = 2 ** 53 - 1


class Recusado(ValueError):
    def __init__(self, motivo: str, caminho: str = "$") -> None:
        super().__init__(f"{motivo} em {caminho}")
        self.motivo, self.caminho = motivo, caminho


def _nao_finito(_: str) -> Any:
    raise Recusado("NUMERO_NAO_FINITO")


def ler_estrito(texto: str) -> Any:
    """json.loads que recusa nomes repetidos, nomes que colidem depois de NFC, NaN e infinito."""
    def pares(ps: List[Any]) -> Dict[str, Any]:
        d: Dict[str, Any] = {}
        nfc: Dict[str, str] = {}
        for k, v in ps:
            if k in d:
                raise Recusado("CHAVE_REPETIDA", k)
            n = unicodedata.normalize("NFC", k)
            if n in nfc:
                raise Recusado("CHAVE_REPETIDA_DEPOIS_DE_NFC", k)
            nfc[n] = k
            d[k] = v
        return d
    return json.loads(texto, object_pairs_hook=pares, parse_constant=_nao_finito)


def diferencas(recebido: Any, selado: Any, caminho: str = "$") -> List[str]:
    """Caminhos em que o recebido não é, valor e tipo, o que está nos bytes selados."""
    out: List[str] = []
    if isinstance(recebido, dict) and isinstance(selado, dict):
        mapa = {unicodedata.normalize("NFC", k): k for k in recebido}
        for k in sorted(set(mapa) | set(selado)):
            if k not in mapa or k not in selado:
                out.append(f"{caminho}.{k}")
                continue
            if mapa[k] != k:
                out.append(f"{caminho}.{k} (nome em forma Unicode diferente)")
            out += diferencas(recebido[mapa[k]], selado[k], f"{caminho}.{k}")
    elif isinstance(recebido, list) and isinstance(selado, list) and len(recebido) == len(selado):
        for i, (a, b) in enumerate(zip(recebido, selado)):
            out += diferencas(a, b, f"{caminho}[{i}]")
    elif type(recebido) is not type(selado) or recebido != selado:
        out.append(caminho)
    return out


def verificar(texto_claim: str, selo: Any, chaves_aceites: Iterable[str], estrito: bool = False) -> Dict[str, Any]:
    """VERIFY (KCP/0.1 §5) com leitura estrita. Devolve sempre um objecto; qualquer falha = NAO_VERIFICADO."""
    r: Dict[str, Any] = {"estado": "NAO_VERIFICADO", "motivo": "", "selado": None, "diferencas": []}
    try:
        obj = ler_estrito(texto_claim)
    except Recusado as e:
        r["motivo"] = e.motivo
        return r
    except (ValueError, TypeError):
        r["motivo"] = "JSON_ILEGIVEL"
        return r
    try:
        c = B.canon(obj)
    except (TypeError, ValueError):
        r["motivo"] = "SEM_FORMA_CANONICA"
        return r
    if not isinstance(selo, dict) or not all(isinstance(selo.get(k), str) for k in ("hash", "pub", "sig")):
        r["motivo"] = "SELO_ILEGIVEL"
        return r
    if not hmac.compare_digest(B.h256(c), selo["hash"]):  # tempo constante (§5.2)
        r["motivo"] = "HASH_DIFERENTE"
        return r
    if selo["pub"] not in set(chaves_aceites):
        r["motivo"] = "CHAVE_NAO_ACEITE"
        return r
    try:
        ok = B.ed_verificar(bytes.fromhex(selo["pub"]), c, bytes.fromhex(selo["sig"]))
    except ValueError:
        ok = False
    if not ok:
        r["motivo"] = "ASSINATURA_INVALIDA"
        return r
    selado = json.loads(c.decode("utf-8"))
    dif = diferencas(obj, selado)
    r.update(selado=selado, diferencas=dif)
    if dif and estrito:
        r["motivo"] = "RECEBIDO_DIFERENTE_DO_SELADO"
        return r
    r["estado"] = "VERIFICADO"
    r["motivo"] = "MOSTRAR_O_SELADO" if dif else ""
    return r


def exigir_exacto(o: Any, caminho: str = "$") -> None:
    """Recusa o que não fica exacto nos bytes selados."""
    if o is None or isinstance(o, bool):
        return
    if isinstance(o, int):
        if abs(o) > LIMITE_INTEIRO:
            raise Recusado("INTEIRO_ACIMA_DE_2^53-1_USA_TEXTO", caminho)
        return
    if isinstance(o, float):
        if not math.isfinite(o):
            raise Recusado("NUMERO_NAO_FINITO", caminho)
        if o == int(o):
            raise Recusado("REAL_COM_VALOR_INTEIRO_USA_INTEIRO", caminho)
        if float(f"{o:.12g}") != o:
            raise Recusado("REAL_PERDERIA_ALGARISMOS_USA_INTEIRO_OU_TEXTO", caminho)
        return
    if isinstance(o, str):
        if unicodedata.normalize("NFC", o) != o:
            raise Recusado("TEXTO_FORA_DE_NFC", caminho)
        return
    if isinstance(o, dict):
        for k in o:
            if not isinstance(k, str) or unicodedata.normalize("NFC", k) != k:
                raise Recusado("NOME_FORA_DE_NFC", f"{caminho}.{k}")
            exigir_exacto(o[k], f"{caminho}.{k}")
        return
    if isinstance(o, (list, tuple)):
        for i, v in enumerate(o):
            exigir_exacto(v, f"{caminho}[{i}]")
        return
    raise Recusado("TIPO_NAO_SUPORTADO", caminho)


def selar_kcp(claim: Dict[str, Any], sk: bytes) -> Dict[str, str]:
    """Selo de um CLAIM KCP novo: regra 1 (o_que_nao_garante não vazio) + exactidão; depois o selo de sempre."""
    if not isinstance(claim, dict) or "kcp" not in claim:
        raise Recusado("NAO_E_CLAIM_KCP")
    if not isinstance(claim.get("o_que_nao_garante"), str) or not claim["o_que_nao_garante"].strip():
        raise Recusado("O_QUE_NAO_GARANTE_VAZIO", "$.o_que_nao_garante")
    exigir_exacto(claim)
    return B.selar(claim, sk)


def selo_e_texto(claim: Dict[str, Any], sk: bytes) -> Optional[Dict[str, Any]]:
    """Ajuda: sela e devolve também o texto canónico, que é o que se deve enviar."""
    selo = selar_kcp(claim, sk)
    return {"texto": B.canon(claim).decode("utf-8"), "selo": selo}
'''),
    "frost_ed25519.py": ("3a626d7cc2ae5a4efe1c4896d5a658a2ce1dd207b365a7396d7750f6711f407d", r'''# -*- coding: utf-8 -*-
"""FROST(Ed25519, SHA-512) — RFC 9591, só a biblioteca-padrão do Python, sobre as peças de base_v28.py.

Para as chaves das câmaras do KCP/0.2 (cláusula 7): t de n câmaras assinam, cada uma com a sua parte, em 2 rondas;
a chave inteira nunca se junta num só sítio; a assinatura final é Ed25519 normal (RFC 8032) e passa no verificador
de sempre. Conferido com os vetores oficiais (repositório cfrg/draft-irtf-cfrg-frost, poc/frost-ed25519-sha512.json).

O_QUE_NAO_GARANTE: é Python puro, sem tempo constante: serve para provar o desenho, não para guardar chaves reais
(em produção: biblioteca auditada ou HSM). A criação das chaves aqui é a do Anexo C do RFC (um distribuidor que
conhece a chave no nascimento): contradiz a cláusula 7.1.3; para a cerimónia faz falta uma criação distribuída (DKG),
que o RFC 9591 deixa de fora. Cada par de nonces é de uso único: reutilizar um nonce revela a parte de quem assina;
este código não guarda memória dos nonces usados. A assinatura de grupo não diz QUAIS câmaras assinaram.
"""
from __future__ import annotations

import hashlib
import secrets
from typing import Dict, List, Optional, Sequence, Tuple

import base_v28 as B

L = B._L
G = B._ED_G
ID = B._ED_ID
CONTEXTO = b"FROST-ED25519-SHA512-v1"
Ponto = Tuple[int, int, int, int]
Compromisso = Tuple[int, Ponto, Ponto]  # (identificador, D = compromisso do nonce de ocultação, E = do nonce de ligação)


def _h(dados: bytes) -> int:
    return int.from_bytes(hashlib.sha512(dados).digest(), "little") % L


def H1(m: bytes) -> int: return _h(CONTEXTO + b"rho" + m)
def H2(m: bytes) -> int: return _h(m)  # sem contexto: é o desafio do RFC 8032
def H3(m: bytes) -> int: return _h(CONTEXTO + b"nonce" + m)
def H4(m: bytes) -> bytes: return hashlib.sha512(CONTEXTO + b"msg" + m).digest()
def H5(m: bytes) -> bytes: return hashlib.sha512(CONTEXTO + b"com" + m).digest()


def escalar(x: int) -> bytes:
    return (x % L).to_bytes(32, "little")


def ponto(p: Ponto) -> bytes:
    return B._ed_comp(p)


def ler_ponto(b: bytes) -> Ponto:
    p = B._ed_descomp(b)
    if p is None or B._ed_igual(B._ed_mult(8, p), ID):
        raise ValueError("ponto inválido ou de ordem pequena")
    return p


def mul(k: int, p: Ponto) -> Ponto:
    return B._ed_mult(k % L, p)


def soma(*ps: Ponto) -> Ponto:
    r = ID
    for p in ps:
        r = B._ed_soma(r, p)
    return r


def lagrange(i: int, participantes: Sequence[int]) -> int:
    """Coeficiente de Lagrange em x = 0 (RFC 9591 §4.2)."""
    if i not in participantes or 0 in participantes or len(set(participantes)) != len(participantes):
        raise ValueError("lista de participantes inválida")
    num = den = 1
    for j in participantes:
        if j != i:
            num = num * j % L
            den = den * (j - i) % L
    return num * pow(den, L - 2, L) % L


# --- Anexo C: criação das partes por um distribuidor, com compromissos públicos (VSS) ---
def distribuir(segredo: int, t: int, n: int, coeficientes: Optional[Sequence[int]] = None) -> Tuple[List[Tuple[int, int]], List[Ponto]]:
    """Partes (i, f(i)) e compromissos C_k = a_k·G. Sem coeficientes dados, saem de secrets (aleatório criptográfico)."""
    if not (1 < t <= n):
        raise ValueError("limiar inválido")
    coef = [segredo % L] + (list(coeficientes) if coeficientes is not None else [secrets.randbelow(L - 1) + 1 for _ in range(t - 1)])
    if len(coef) != t:
        raise ValueError("número de coeficientes errado")

    def f(x: int) -> int:
        y = 0
        for a in reversed(coef):
            y = (y * x + a) % L
        return y

    return [(i, f(i)) for i in range(1, n + 1)], [mul(a, G) for a in coef]


def parte_confere(i: int, s_i: int, compromissos: Sequence[Ponto]) -> bool:
    """vss_verify: s_i·G == Σ C_k·i^k. Uma parte adulterada não passa (red team A6b)."""
    esperado = soma(*[mul(pow(i, k, L), c) for k, c in enumerate(compromissos)])
    return B._ed_igual(mul(s_i, G), esperado)


# --- Ronda 1 ---
def gerar_nonce(s_i: int, aleatorio: Optional[bytes] = None) -> int:
    return H3((aleatorio if aleatorio is not None else secrets.token_bytes(32)) + escalar(s_i))


def comprometer(s_i: int, aleat_ocultacao: Optional[bytes] = None, aleat_ligacao: Optional[bytes] = None):
    d, e = gerar_nonce(s_i, aleat_ocultacao), gerar_nonce(s_i, aleat_ligacao)
    return (d, e), (mul(d, G), mul(e, G))


def _lista_codificada(lista: Sequence[Compromisso]) -> bytes:
    return b"".join(escalar(i) + ponto(D) + ponto(E) for (i, D, E) in lista)


def fatores_de_ligacao(pk_grupo: Ponto, lista: Sequence[Compromisso], msg: bytes) -> Dict[int, int]:
    prefixo = ponto(pk_grupo) + H4(msg) + H5(_lista_codificada(lista))
    return {i: H1(prefixo + escalar(i)) for (i, _, _) in lista}


def compromisso_de_grupo(lista: Sequence[Compromisso], rho: Dict[int, int]) -> Ponto:
    return soma(*[soma(D, mul(rho[i], E)) for (i, D, E) in lista])


def desafio(R: Ponto, pk_grupo: Ponto, msg: bytes) -> int:
    return H2(ponto(R) + ponto(pk_grupo) + msg)


def _ordenada(lista: Sequence[Compromisso]) -> List[Compromisso]:
    lista = sorted(lista, key=lambda c: c[0])
    if len({c[0] for c in lista}) != len(lista):
        raise ValueError("identificador repetido na lista de compromissos")
    return lista


# --- Ronda 2 ---
def assinar_parte(i: int, s_i: int, nonces: Tuple[int, int], msg: bytes, pk_grupo: Ponto, lista: Sequence[Compromisso]) -> int:
    lista = _ordenada(lista)
    rho = fatores_de_ligacao(pk_grupo, lista, msg)
    R = compromisso_de_grupo(lista, rho)
    c = desafio(R, pk_grupo, msg)
    lam = lagrange(i, [x for (x, _, _) in lista])
    d, e = nonces
    return (d + e * rho[i] + lam * s_i * c) % L


def parte_de_assinatura_confere(i: int, pk_i: Ponto, z_i: int, msg: bytes, pk_grupo: Ponto, lista: Sequence[Compromisso]) -> bool:
    """§5.4: identifica quem mandou uma parte errada."""
    lista = _ordenada(lista)
    rho = fatores_de_ligacao(pk_grupo, lista, msg)
    R = compromisso_de_grupo(lista, rho)
    c = desafio(R, pk_grupo, msg)
    lam = lagrange(i, [x for (x, _, _) in lista])
    D, E = next((D, E) for (x, D, E) in lista if x == i)
    return B._ed_igual(mul(z_i, G), soma(D, mul(rho[i], E), mul(c * lam, pk_i)))


def juntar(lista: Sequence[Compromisso], msg: bytes, pk_grupo: Ponto, partes: Dict[int, int],
           pks: Optional[Dict[int, Ponto]] = None) -> Tuple[Optional[bytes], List[int]]:
    """Junta as partes. Com as chaves públicas das partes, confere cada uma e devolve quem falhou (sem assinatura)."""
    lista = _ordenada(lista)
    if pks is not None:
        maus = [i for (i, _, _) in lista if not parte_de_assinatura_confere(i, pks[i], partes[i], msg, pk_grupo, lista)]
        if maus:
            return None, maus
    rho = fatores_de_ligacao(pk_grupo, lista, msg)
    R = compromisso_de_grupo(lista, rho)
    z = sum(partes[i] for (i, _, _) in lista) % L
    return ponto(R) + escalar(z), []
'''),
    "dkg_frost.py": ("470f45e0061023efb952f0ef9e39982af9484cc4868ed1c7d93207f587a18b47", r'''# -*- coding: utf-8 -*-
"""A chave das câmaras nasce a várias mãos: geração distribuída (DKG) para FROST(Ed25519, SHA-512).

Protocolo: o KeyGen do artigo FROST (Komlo & Goldberg, 2020), na forma da biblioteca frost da Zcash Foundation
(frost-core/src/keys/dkg.rs), cujos vetores de teste para Ed25519 este código reproduz.
- Ronda 1: cada câmara inventa um polinómio secreto, publica os compromissos (um ponto por coeficiente) e uma
  prova de que conhece o seu segredo (impede que uma câmara escolha a chave do grupo à custa das outras).
- Ronda 2: cada câmara entrega a cada outra, em privado, o valor do seu polinómio no número dessa câmara.
- Ronda 3: cada câmara confere o que recebeu contra os compromissos públicos e soma tudo: fica com o seu pedaço.
A chave pública do grupo é a soma dos compromissos públicos. A chave secreta do grupo nunca é calculada por ninguém.
- Eco (acrescento da casa, ver o_que_nao_garante): no fim da ronda 1, cada câmara publica o hash de tudo o que
  recebeu; se os hashes não forem todos iguais, alguém mandou pacotes diferentes a câmaras diferentes, e pára-se.

O_QUE_NAO_GARANTE: a ronda 1 exige um canal de difusão a sério (todas as câmaras recebem exatamente os mesmos
pacotes) e a ronda 2 canais autenticados e confidenciais; este código não os cria: o «eco» só deteta a fraude
de mandar pacotes diferentes, não substitui os canais. Se uma câmara falha ou faz batota, a geração aborta e
recomeça (aponta a culpada, não continua sem ela). Quatro câmaras juntas podem sempre assinar e também,
se conspirarem, reconstruir a chave: o limiar protege contra 3, não contra 4. Python puro, sem tempo constante:
serve para provar e ensaiar, não para chaves reais. Os vetores são da Zcash Foundation, não de uma norma IETF
(o RFC 9591 deixa a geração de chaves de fora).
"""
from __future__ import annotations

import hashlib
import secrets
from typing import Dict, List, Optional, Sequence, Tuple

import base_v28 as B
import frost_ed25519 as F

L, G = F.L, F.G


def HDKG(m: bytes) -> int:
    """HDKG de FROST(Ed25519, SHA-512) na Zcash Foundation: SHA-512(contexto || "dkg" || m) mod L."""
    return F._h(F.CONTEXTO + b"dkg" + m)


def ler_ponto_primo(b: bytes) -> F.Ponto:
    """Leitura estrita: ponto válido, não é a identidade e está no subgrupo de ordem prima (sem torção)."""
    if len(b) != 32:
        raise ValueError("ponto com tamanho errado")
    p = B._ed_descomp(b)
    if p is None or B._ed_igual(p, F.ID) or not B._ed_igual(B._ed_mult(L, p), F.ID):
        raise ValueError("ponto inválido, identidade ou com torção")
    return p


def ler_escalar(b: bytes) -> int:
    if len(b) != 32:
        raise ValueError("escalar com tamanho errado")
    x = int.from_bytes(b, "little")
    if x >= L:
        raise ValueError("escalar fora do intervalo")
    return x


def desafio_dkg(i: int, phi0: F.Ponto, R: F.Ponto) -> int:
    return HDKG(F.escalar(i) + F.ponto(phi0) + F.ponto(R))


def _aleatorio() -> int:
    return secrets.randbelow(L - 1) + 1


def _avaliar(coef: Sequence[int], x: int) -> int:
    y = 0
    for a in reversed(coef):
        y = (y * x + a) % L
    return y


def _ids_validos(i: int, n: int, outros: Sequence[int]) -> bool:
    return (1 <= i <= n and i not in outros and len(set(outros)) == len(outros) == n - 1
            and all(1 <= j <= n for j in outros))


# --- Ronda 1 ---
def ronda1(i: int, t: int, n: int, segredo: Optional[int] = None, coeficientes: Optional[Sequence[int]] = None,
           aleatorio_k: Optional[bytes] = None) -> Tuple[dict, dict]:
    """Devolve (pacote secreto, que fica com a câmara; pacote público, para difundir a todas)."""
    if not (1 < t <= n) or not (1 <= i <= n):
        raise ValueError("limiar ou identificador inválido")
    coef = [(segredo if segredo is not None else _aleatorio()) % L]
    coef += [c % L for c in coeficientes] if coeficientes is not None else [_aleatorio() for _ in range(t - 1)]
    if len(coef) != t:
        raise ValueError("número de coeficientes errado")
    compromissos = [F.mul(a, G) for a in coef]
    k = (int.from_bytes(aleatorio_k, "little") % L) if aleatorio_k is not None else _aleatorio()
    R = F.mul(k, G)
    mu = (k + coef[0] * desafio_dkg(i, compromissos[0], R)) % L
    publico = {"i": i, "compromissos": [F.ponto(c) for c in compromissos], "prova": F.ponto(R) + F.escalar(mu)}
    return {"i": i, "t": t, "n": n, "coef": coef, "publico": publico}, publico


def _ler_publico(pub: dict, t: int) -> List[F.Ponto]:
    if len(pub["compromissos"]) != t or len(pub["prova"]) != 64:
        raise ValueError("pacote com tamanho errado")
    return [ler_ponto_primo(c) for c in pub["compromissos"]]


def prova_confere(pub: dict, t: int) -> bool:
    """R == mu·G − c·phi0, com c = HDKG(i || phi0 || R). Falha se o pacote estiver mal formado."""
    try:
        C = _ler_publico(pub, t)
        R = ler_ponto_primo(pub["prova"][:32])
        mu = ler_escalar(pub["prova"][32:])
    except (ValueError, KeyError, TypeError):
        return False
    c = desafio_dkg(pub["i"], C[0], R)
    return B._ed_igual(R, F.soma(F.mul(mu, G), F.mul(-c, C[0])))


def eco(publicos: Sequence[dict]) -> str:
    """Hash de todos os pacotes da ronda 1 vistos por uma câmara (incluindo o seu), por ordem de identificador."""
    h = hashlib.sha256(b"konfirmu-dkg-eco-v1")
    for p in sorted(publicos, key=lambda p: p["i"]):
        h.update(F.escalar(p["i"]) + b"".join(p["compromissos"]) + p["prova"])
    return h.hexdigest()


# --- Ronda 2 ---
def ronda2(sec1: dict, recebidos1: Dict[int, dict]) -> Tuple[Optional[dict], Dict[int, int], List[int]]:
    """Confere as provas recebidas; devolve (pacote secreto 2, valores a entregar em privado, culpadas)."""
    i, t, n = sec1["i"], sec1["t"], sec1["n"]
    if not _ids_validos(i, n, list(recebidos1)) or any(p.get("i") != j for j, p in recebidos1.items()):
        raise ValueError("pacotes da ronda 1 em número ou com identificadores errados")
    maus = sorted(j for j, p in recebidos1.items() if not prova_confere(p, t))
    if maus:
        return None, {}, maus
    entregar = {j: _avaliar(sec1["coef"], j) for j in sorted(recebidos1)}
    sec2 = {"i": i, "t": t, "n": n, "fii": _avaliar(sec1["coef"], i), "publico": sec1["publico"]}
    return sec2, entregar, []


# --- Ronda 3 ---
def ronda3(sec2: dict, recebidos1: Dict[int, dict], recebidos2: Dict[int, int]) -> Tuple[Optional[dict], List[int]]:
    """Confere cada valor recebido contra os compromissos de quem o mandou e soma. Devolve (pacote final, culpadas)."""
    i, t, n = sec2["i"], sec2["t"], sec2["n"]
    if not _ids_validos(i, n, list(recebidos1)) or set(recebidos1) != set(recebidos2):
        raise ValueError("pacotes da ronda 2 em número ou com identificadores errados")
    compromissos = {j: _ler_publico(p, t) for j, p in recebidos1.items()}
    compromissos[i] = _ler_publico(sec2["publico"], t)
    maus = sorted(j for j, v in recebidos2.items()
                  if not (isinstance(v, int) and 0 <= v < L and F.parte_confere(i, v, compromissos[j])))
    if maus:
        return None, maus
    s = (sec2["fii"] + sum(recebidos2.values())) % L
    Y = F.soma(*[C[0] for C in compromissos.values()])
    Yj = {j: F.soma(*[F.soma(*[F.mul(pow(j, k, L), c) for k, c in enumerate(C)]) for C in compromissos.values()])
          for j in range(1, n + 1)}
    if not B._ed_igual(F.mul(s, G), Yj[i]):
        raise ValueError("incoerência interna: o pedaço não bate com a chave pública do pedaço")
    return {"i": i, "t": t, "n": n, "s": s, "Y": Y, "Yj": Yj}, []
'''),
    "teste_base.py": ("ae65966bd32e288726136b391e8c35f04aed48299f59eb7036a8ee0055565466", r'''# -*- coding: utf-8 -*-
# Testes da base (assinatura Ed25519 e selo KCP da base_v28): vetores públicos de Ed25519 + o ataque A1 do red team.
# Correr: python3 -I teste_base.py [pasta]
import hashlib
import os
import sys

sys.stdout.reconfigure(encoding="utf-8")
PASTA = sys.argv[1] if len(sys.argv) > 1 else os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, PASTA)
import base_v28 as B  # noqa: E402

LINHAS, FALHAS = [], []


def caso(ident, texto, prova):
    """Corre uma verificação; uma exceção conta como falha (nunca como passagem)."""
    try:
        ok = bool(prova())
    except Exception as e:  # noqa: BLE001
        ok, texto = False, f"{texto} [exceção: {type(e).__name__}]"
    s = f"{ident} | {'OK' if ok else 'FALHOU'} | {texto}"
    LINHAS.append(s)
    print(s)
    if not ok:
        FALHAS.append(ident)


hx = bytes.fromhex
# Formato de cada linha (SUPERCOP/ed25519, como em pyca/cryptography): segredo+pública : pública : mensagem : assinatura+mensagem :
VET = []
for linha in open(os.path.join(PASTA, "ed25519-sign-input-16.txt"), encoding="ascii").read().splitlines():
    c = linha.split(":")
    VET.append((hx(c[0])[:32], hx(c[1]), hx(c[2]), hx(c[3])[:64]))


def b1():
    return len(VET) == 16 and all(B.ed_publica(sk) == pk and B.ed_assinar(sk, m) == sig and B.ed_verificar(pk, m, sig)
                                  for sk, pk, m, sig in VET)


def b2():
    sk, pk, m, sig = VET[5]
    outra_r = bytes([sig[0] ^ 1]) + sig[1:]
    return (not B.ed_verificar(pk, m + b"!", sig) and not B.ed_verificar(pk, m, outra_r)
            and not B.ed_verificar(VET[6][1], m, sig))


def b3():
    pk_pequena, sig_nula = bytes([1]) + bytes(31), bytes([1]) + bytes(63)
    return not any(B.ed_verificar(pk_pequena, msg, sig_nula) for msg in (b"", b"qualquer mensagem", b"\x00" * 64))


def b4():
    sk, pk, m, sig = VET[0]
    s_mais_l = (int.from_bytes(sig[32:], "little") + B._L).to_bytes(32, "little")
    return B.ed_verificar(pk, m, sig) and not B.ed_verificar(pk, m, sig[:32] + s_mais_l)


def b5():
    sk = VET[2][0]
    obj = {"kcp": "0.2", "tipo": "TESTE", "valor": "12.50", "o_que_nao_garante": "teste da base"}
    selo = B.selar(obj, sk)
    outro = dict(obj, valor="12.51")
    return (B.selo_ok(obj, selo, {selo["pub"]}) and not B.selo_ok(outro, selo, {selo["pub"]})
            and not B.selo_ok(obj, selo, {VET[3][1].hex()}))


caso("B1", "16 vetores públicos de Ed25519: chave pública, assinatura e verificação iguais, byte a byte", b1)
caso("B2", "mensagem mexida, assinatura mexida ou chave de outro -> recusada", b2)
caso("B3", "ataque A1 do red team: chave de ordem pequena com assinatura nula -> recusada para qualquer mensagem", b3)
caso("B4", "assinatura maleável (S + L) -> recusada; a original continua a conferir", b4)
caso("B5", "selo KCP: confere com a chave aceite; com um valor mexido ou outra chave aceite -> recusado", b5)

texto = "\n".join(LINHAS)
print(f"RESULTADO: {len(LINHAS) - len(FALHAS)}/{len(LINHAS)} OK" + (f" · FALHARAM: {FALHAS}" if FALHAS else ""))
print("SAIDA_SHA256:", hashlib.sha256(texto.encode("utf-8")).hexdigest())
sys.exit(1 if FALHAS else 0)
'''),
    "teste_quorum.py": ("b0bb2e0c512fa7748a3b09ca58b913afbc742aa492c7eb459ee0b676dd57e37a", r'''# -*- coding: utf-8 -*-
# Teste vermelho -> verde do P0 do red team de 21-11-2026 (achado B1, quórum k>=5).
# Correr: python3 -I teste_quorum.py [pasta_do_kit]
import hashlib
import itertools
import os
import sys

sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, sys.argv[1] if len(sys.argv) > 1 else os.path.dirname(os.path.abspath(__file__)))
import base_v28 as K  # noqa: E402
from quorum_multibloco import AldeiaMultibloco, cadeias_independentes  # noqa: E402

K_QUORUM = 5
LINHAS, FALHAS = [], []


def linha(ident, ok, texto):
    s = f"{ident} | {'OK' if ok else 'FALHOU'} | {texto}"
    LINHAS.append(s)
    print(s)
    if not ok:
        FALHAS.append(ident)


_PUB = {}


def sk(n):
    return hashlib.sha256(("konfirmu-teste/" + n).encode()).digest()


def pub(n):
    if n not in _PUB:
        _PUB[n] = K.ed_publica(sk(n)).hex()
    return _PUB[n]


def atestar(por, novo):
    return {"por": por, "selo": K.selar({"atesto": novo, "pub": pub(novo)}, sk(por))}


def aldeia(Classe, raizes):
    return Classe({n: pub(n) for n in raizes})


def admitir(al, novo, padrinhos):
    ok, motivo = al.admitir(novo, pub(novo), [atestar(q, novo) for q in padrinhos])
    assert ok, (novo, motivo)


def exercito(al, conluio, n_votantes=10):
    """O ataque B1: o conluio admite identidades que se apadrinham entre si e escolhe, para votar,
    as que não partilham 2 padrinhos com nenhuma outra (para escapar à regra antiga)."""
    controlados, votantes, n = list(conluio), [], 0
    while len(votantes) < n_votantes and n < 400:
        n += 1
        novo = f"S{n}"
        cands = [c for c in controlados if al.dados_por.get(c, 0) < 5]
        escolha, vota = None, False
        for tri in itertools.combinations(cands, 3):
            if all(len(frozenset(tri) & al.atestados[v]) <= 1 for v in votantes):
                escolha, vota = tri, True
                break
        if escolha is None:
            escolha = tuple(cands[:3])
        if len(escolha) < 3:
            break
        admitir(al, novo, escolha)
        controlados.append(novo)
        if vota:
            votantes.append(novo)
    return votantes


def contar(al, quem, conforme=True):
    votos = []
    for p in quem:
        d = {"quem": p, "obra": "OBRA-1", "dia": 10, "conforme": conforme}
        votos.append({"dados": d, "selo": K.selar(d, sk(p))})
    return al.contar(votos, "OBRA-1", 10)


HONESTOS = [f"H{i:02d}" for i in range(20)]
CONLUIO = ["A", "B", "C"]

# Q1 — a regra antiga (v1.0 a v2.8) deixa passar o ataque: é o vermelho
al = aldeia(K.Aldeia, HONESTOS + CONLUIO)
sybils = exercito(al, CONLUIO)
r = contar(al, CONLUIO + sybils)
linha("Q1", r["conformes"] >= K_QUORUM,
      f"ANTES (v1.0-v2.8): 3 pessoas reais + {len(sybils)} identidades delas -> {r['conformes']} votos contados (k={K_QUORUM}): o ataque passa [vermelho reproduzido]")

# Q2 — a regra nova, com o MESMO ataque: é o verde
al = aldeia(AldeiaMultibloco, HONESTOS + CONLUIO)
sybils = exercito(al, CONLUIO)
r = contar(al, CONLUIO + sybils)
linha("Q2", r["conformes"] <= 3,
      f"DEPOIS (v2.9): o mesmo ataque -> {r['conformes']} votos contados: não chega a k={K_QUORUM} [verde]")
cad = al.cadeias([p for p in CONLUIO + sybils])
linha("Q2b", all(c[-1] in CONLUIO for c in cad) and len({m for c in cad for m in c}) == sum(len(c) for c in cad),
      f"as {len(cad)} cadeias contadas acabam em A, B ou C e não partilham ninguém: {cad}")

# Q3 — o congelamento do pagamento (E2): 5 «desconformes» fabricados já não congelam
r = contar(al, CONLUIO + sybils, conforme=False)
linha("Q3", r["desconformes"] < K_QUORUM,
      f"DEPOIS: os mesmos votos contra -> {r['desconformes']} desconformes: o pagamento do trabalhador não congela")

# Q4 — o conluio não é raiz: cada um entrou apadrinhado por 3 raízes honestas diferentes
for Classe, nome in ((K.Aldeia, "ANTES"), (AldeiaMultibloco, "DEPOIS")):
    al = aldeia(Classe, HONESTOS)
    for c, tri in zip(CONLUIO, (HONESTOS[0:3], HONESTOS[3:6], HONESTOS[6:9])):
        admitir(al, c, tri)
    sybils = exercito(al, CONLUIO)
    r = contar(al, CONLUIO + sybils)
    esperado = r["conformes"] >= K_QUORUM if nome == "ANTES" else r["conformes"] <= 3
    linha("Q4" + ("a" if nome == "ANTES" else "b"), esperado,
          f"{nome}: conluio de 3 membros não-raiz (9 raízes honestas por cima) -> {r['conformes']} votos contados")

# Q5 — honestos: 5 raízes votam, contam 5
al = aldeia(AldeiaMultibloco, HONESTOS)
linha("Q5", contar(al, HONESTOS[:5])["conformes"] == 5, "DEPOIS: 5 raízes honestas votam -> 5 votos contados")

# Q6 — honestos novos, cada um com 3 padrinhos diferentes: o quórum continua alcançável
al = aldeia(AldeiaMultibloco, HONESTOS)
novos = [f"N{i}" for i in range(5)]
for i, n in enumerate(novos):
    admitir(al, n, HONESTOS[3 * i:3 * i + 3])
linha("Q6", contar(al, novos)["conformes"] == 5, "DEPOIS: 5 pessoas novas com padrinhos diferentes -> 5 votos contados")

# Q7 — 5 pessoas apadrinhadas pelas MESMAS 3: contam 3 (a regra antiga contava 1)
for Classe, nome, quer in ((K.Aldeia, "ANTES", 1), (AldeiaMultibloco, "DEPOIS", 3)):
    al = aldeia(Classe, HONESTOS)
    for n in novos:
        admitir(al, n, HONESTOS[:3])
    v = contar(al, novos)["conformes"]
    linha("Q7" + ("a" if nome == "ANTES" else "b"), v == quer,
          f"{nome}: 5 pessoas com os mesmos 3 padrinhos -> {v} (na dúvida, conta-se o que as 3 garantem)")

# Q8 — conluio + 2 honestos: 5 pessoas reais, 5 votos (nem mais nem menos)
al = aldeia(AldeiaMultibloco, HONESTOS + CONLUIO)
sybils = exercito(al, CONLUIO)
linha("Q8", contar(al, CONLUIO + sybils + HONESTOS[:2])["conformes"] == 5,
      "DEPOIS: as 3 pessoas do conluio + o exército delas + 2 honestos -> 5 votos (5 pessoas reais)")

# Q9 — mesma entrada, mesma saída
a1 = cadeias_independentes(al.atestados, al.membros, CONLUIO + sybils)
a2 = cadeias_independentes(dict(reversed(list(al.atestados.items()))), list(reversed(list(al.membros))), list(reversed(CONLUIO + sybils)))
linha("Q9", a1 == a2, "a contagem e as cadeias não dependem da ordem em que os dados chegam")

# Q10 — escala: centenas de membros em 3 camadas, conta depressa e nunca passa o número de raízes
al = aldeia(AldeiaMultibloco, HONESTOS)
camada = list(HONESTOS)
for g in range(3):
    nova = []
    for i in range(len(camada) * 5 // 3):
        n = f"G{g}_{i}"
        tri = [camada[(3 * i + j) % len(camada)] for j in range(3)]
        if all(al.dados_por.get(q, 0) < 5 for q in tri):
            admitir(al, n, tri)
            nova.append(n)
    camada = nova
v = contar(al, camada)["conformes"]
linha("Q10", 0 < v <= len(HONESTOS), f"{len(al.membros)} membros, {len(camada)} votantes na última camada -> {v} votos (nunca mais do que as {len(HONESTOS)} raízes)")

texto = "\n".join(LINHAS)
print(f"RESULTADO: {len(LINHAS) - len(FALHAS)}/{len(LINHAS)} OK" + (f" · FALHARAM: {FALHAS}" if FALHAS else ""))
print("SAIDA_SHA256:", hashlib.sha256(texto.encode("utf-8")).hexdigest())
sys.exit(1 if FALHAS else 0)
'''),
    "teste_kcp_exacto.py": ("4fb9cba51194bd6d3044ab412b8bd64b0ade611f8cbb1b797ed35a210ff69df8", r'''# -*- coding: utf-8 -*-
# Testes da aritmética exacta e da leitura estrita do KCP (correções v2.9). Correr: python3 -I teste_kcp_exacto.py [pasta]
import hashlib
import json
import os
import sys
import unicodedata

sys.stdout.reconfigure(encoding="utf-8")
PASTA = sys.argv[1] if len(sys.argv) > 1 else os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, PASTA)
import base_v28 as B  # noqa: E402
import kcp_exacto as X  # noqa: E402

LINHAS, FALHAS = [], []


def linha(ident, ok, texto):
    s = f"{ident} | {'OK' if ok else 'FALHOU'} | {texto}"
    LINHAS.append(s)
    print(s)
    if not ok:
        FALHAS.append(ident)


def recusa(fn):
    try:
        fn()
    except X.Recusado as e:
        return e.motivo
    return None


bruto = open(os.path.join(PASTA, "kcp_vetores_0.1.json"), "rb").read()
linha("X0", hashlib.sha256(bruto).hexdigest() == "2543362db0ddacbea127976c0d14f773c5b63ccef7335e70045e209ab3f69a5a",
      "o ficheiro de vectores é o oficial (SHA-256 2543362d...f69a5a, Anexo de Provas §2)")
V = json.loads(bruto.decode("utf-8"))
SK = bytes.fromhex(V["chave_de_teste_sk_hex"])
PUB = V["selo"]["pub"]
texto = json.dumps(V["claim"], ensure_ascii=False)

r = X.verificar(texto, V["selo"], {PUB})
linha("X1", r["estado"] == "VERIFICADO" and r["diferencas"] == ["$.numero_exemplo"] and r["selado"]["numero_exemplo"] == 0.3,
      f"vector oficial -> {r['estado']}; o texto mostra 0.30000000000000004, o selado diz {r['selado']['numero_exemplo']}: mostra-se o selado")
r = X.verificar(texto, V["selo"], {PUB}, estrito=True)
linha("X1b", r["estado"] == "NAO_VERIFICADO" and r["motivo"] == "RECEBIDO_DIFERENTE_DO_SELADO",
      "modo estrito (dinheiro, prazos): o mesmo vector -> NAO_VERIFICADO, porque o texto recebido não é o selado")
neg = json.dumps(dict(V["claim"], veredicto="SEM_COBERTURA"), ensure_ascii=False)
linha("X2", X.verificar(neg, V["selo"], {PUB})["motivo"] == "HASH_DIFERENTE", "caso negativo do vector -> NAO_VERIFICADO (HASH_DIFERENTE)")

# K1 — selo antigo sobre um real com 15 algarismos
antigo = {"kcp": "0.2", "valor_eur": 1234567890123.45, "o_que_nao_garante": "teste"}
s_antigo = B.selar(antigo, SK)
mexido = json.dumps(dict(antigo, valor_eur=1234567890124.99))
r = X.verificar(mexido, s_antigo, {PUB})
linha("X3", r["estado"] == "VERIFICADO" and r["diferencas"] == ["$.valor_eur"] and r["selado"]["valor_eur"] == 1234567890120.0,
      f"K1: selo de 1234567890123.45 com o texto mexido para 1234567890124.99 -> o verificador diz o que foi selado: {r['selado']['valor_eur']}")
linha("X3b", X.verificar(mexido, s_antigo, {PUB}, estrito=True)["estado"] == "NAO_VERIFICADO", "K1 em modo estrito -> NAO_VERIFICADO")

# o emissor exacto recusa o que não fica exacto
casos = [
    ("valor_eur", 1234567890123.45, "REAL_PERDERIA_ALGARISMOS_USA_INTEIRO_OU_TEXTO"),
    ("numero", 0.30000000000000004, "REAL_PERDERIA_ALGARISMOS_USA_INTEIRO_OU_TEXTO"),
    ("total", 100.0, "REAL_COM_VALOR_INTEIRO_USA_INTEIRO"),
    ("grande", 2 ** 60, "INTEIRO_ACIMA_DE_2^53-1_USA_TEXTO"),
    ("texto", unicodedata.normalize("NFD", "Água"), "TEXTO_FORA_DE_NFC"),
    ("nan", float("nan"), "NUMERO_NAO_FINITO"),
]
for nome, valor, quer in casos:
    m = recusa(lambda: X.selar_kcp({"kcp": "0.2", nome: valor, "o_que_nao_garante": "teste"}, SK))
    linha("X4." + nome, m == quer, f"emissor exacto recusa {nome}={valor!r} -> {m}")
linha("X4.ong", recusa(lambda: X.selar_kcp({"kcp": "0.2", "o_que_nao_garante": " "}, SK)) == "O_QUE_NAO_GARANTE_VAZIO",
      "emissor recusa CLAIM com o_que_nao_garante vazio (regra 1)")

# o emissor exacto aceita o que fica exacto, e o verificador estrito confirma sem diferenças
bom = {"kcp": "0.2", "valor_cent": 123456789012345, "valor_eur_texto": "1234567890123.45", "taxa": 0.1,
       "pegada_gco2e": 4.3e-06, "facto": "Água é vida", "o_que_nao_garante": "teste: sem fonte real"}
p = X.selo_e_texto(bom, SK)
r = X.verificar(p["texto"], p["selo"], {PUB}, estrito=True)
linha("X5", r["estado"] == "VERIFICADO" and r["diferencas"] == [], "CLAIM exacto (cêntimos inteiros, texto decimal, reais exactos) -> VERIFICADO em modo estrito, sem diferenças")

# K3 — nomes repetidos
dup = '{"kcp":"0.2","o_que_nao_garante":"t","veredicto":"VERIFICADO","veredicto":"SEM_COBERTURA"}'
linha("X6", X.verificar(dup, p["selo"], {PUB})["motivo"] == "CHAVE_REPETIDA", "K3: JSON com «veredicto» repetido -> NAO_VERIFICADO (CHAVE_REPETIDA)")

# K4 — dois nomes que só diferem na forma Unicode: a v2.8 funde-os em silêncio
k4 = '{"kcp":"0.2","o_que_nao_garante":"t","caf\\u00e9":"pago","cafe\\u0301":"por pagar"}'
fundido = B.canon(json.loads(k4)).decode("utf-8")
linha("X7", X.verificar(k4, p["selo"], {PUB})["motivo"] == "CHAVE_REPETIDA_DEPOIS_DE_NFC" and fundido.count("caf") == 1,
      f"K4: «café» escrito de 2 maneiras com valores diferentes -> a forma canónica v2.8 guarda só um ({fundido}); o leitor estrito recusa")

linha("X8", X.verificar('{"kcp":"0.2","x":NaN}', p["selo"], {PUB})["motivo"] == "NUMERO_NAO_FINITO", "NaN no texto -> NAO_VERIFICADO")

pk0 = (1).to_bytes(32, "little")
falso = {"kcp": "0.2", "o_que_nao_garante": "t", "facto": "inventado"}
c = B.canon(falso)
selo0 = {"alg": "Ed25519+SHA-256", "hash": B.h256(c), "pub": pk0.hex(), "sig": (pk0 + bytes(32)).hex()}
linha("X9", X.verificar(c.decode(), selo0, {pk0.hex()})["motivo"] == "ASSINATURA_INVALIDA",
      "assinatura nula com chave de ordem pequena, mesmo posta na lista de aceites -> NAO_VERIFICADO")

sk1 = bytes.fromhex("9d61b19deffd5a60ba844af492ec2cc44449c5697b326919703bac031cae7f60")
ok = (B.ed_publica(sk1).hex() == "d75a980182b10ab7d54bfed3c964073a0ee172f3daa62325af021a68f707511a"
      and B.ed_assinar(sk1, b"").hex().startswith("e5564300c360ac729086e2cc806e828a"))
linha("X10", ok, "Ed25519 reproduz o vector 1 do RFC 8032")

um = B.selar({"kcp": "0.2", "o_que_nao_garante": "t", "n": 1.0}, SK)
linha("X11", X.verificar('{"kcp":"0.2","o_que_nao_garante":"t","n":1}', um, {PUB})["motivo"] == "HASH_DIFERENTE"
      and recusa(lambda: X.selar_kcp({"kcp": "0.2", "o_que_nao_garante": "t", "n": 1.0}, SK)) == "REAL_COM_VALOR_INTEIRO_USA_INTEIRO",
      "K1c: selo antigo com 1.0 lido por quem escreve 1 -> HASH_DIFERENTE; o emissor exacto já não sela 1.0")

texto_saida = "\n".join(LINHAS)
print(f"RESULTADO: {len(LINHAS) - len(FALHAS)}/{len(LINHAS)} OK" + (f" · FALHARAM: {FALHAS}" if FALHAS else ""))
print("SAIDA_SHA256:", hashlib.sha256(texto_saida.encode("utf-8")).hexdigest())
sys.exit(1 if FALHAS else 0)
'''),
    "teste_frost.py": ("d8c1ee96ad9561a0e4bddb96cce4ee18865ae143561cd9bf561c4baa8559e9ca", r'''# -*- coding: utf-8 -*-
# Testes do FROST(Ed25519, SHA-512), RFC 9591: vetores oficiais + as 6 câmaras do KCP/0.2 (4 de 6).
# Correr: python3 -I teste_frost.py [pasta_do_kit]
import hashlib
import json
import os
import sys
from itertools import combinations

sys.stdout.reconfigure(encoding="utf-8")
PASTA = sys.argv[1] if len(sys.argv) > 1 else os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, PASTA)
import base_v28 as B  # noqa: E402
import frost_ed25519 as F  # noqa: E402

LINHAS, FALHAS = [], []


def linha(ident, ok, texto):
    s = f"{ident} | {'OK' if ok else 'FALHOU'} | {texto}"
    LINHAS.append(s)
    print(s)
    if not ok:
        FALHAS.append(ident)


hx = bytes.fromhex
esc = lambda h: int.from_bytes(hx(h), "little")  # noqa: E731

# ---------- Parte 1: os vetores oficiais (cfrg/draft-irtf-cfrg-frost, poc/frost-ed25519-sha512.json) ----------
V = json.load(open(os.path.join(PASTA, "frost-ed25519-sha512.json"), encoding="utf-8"))
I = V["inputs"]
s = esc(I["group_secret_key"])
pk = F.mul(s, F.G)
linha("F1", F.ponto(pk).hex() == I["group_public_key"], "chave pública do grupo = a do vetor")
partes, comp = F.distribuir(s, int(V["config"]["MIN_PARTICIPANTS"]), int(V["config"]["MAX_PARTICIPANTS"]),
                            [esc(c) for c in I["share_polynomial_coefficients"]])
linha("F2", all(F.escalar(si).hex() == p["participant_share"] for (_, si), p in zip(partes, I["participant_shares"])),
      "as 3 partes do distribuidor = as do vetor")
linha("F2b", all(F.parte_confere(i, si, comp) for i, si in partes), "cada parte confere com os compromissos públicos (VSS)")
msg = hx(I["message"])
quota = {i: si for i, si in partes}
nonces, lista = {}, []
ok3 = True
for o in V["round_one_outputs"]["outputs"]:
    i = int(o["identifier"])
    (d, e), (D, E) = F.comprometer(quota[i], hx(o["hiding_nonce_randomness"]), hx(o["binding_nonce_randomness"]))
    ok3 &= (F.escalar(d).hex() == o["hiding_nonce"] and F.escalar(e).hex() == o["binding_nonce"]
            and F.ponto(D).hex() == o["hiding_nonce_commitment"] and F.ponto(E).hex() == o["binding_nonce_commitment"])
    nonces[i] = (d, e)
    lista.append((i, D, E))
linha("F3", ok3, "ronda 1: nonces e compromissos = os do vetor")
rho = F.fatores_de_ligacao(pk, lista, msg)
linha("F4", all(F.escalar(rho[int(o["identifier"])]).hex() == o["binding_factor"] for o in V["round_one_outputs"]["outputs"]),
      "fatores de ligação = os do vetor")
z = {i: F.assinar_parte(i, quota[i], nonces[i], msg, pk, lista) for (i, _, _) in lista}
linha("F5", all(F.escalar(z[int(o["identifier"])]).hex() == o["sig_share"] for o in V["round_two_outputs"]["outputs"]),
      "ronda 2: partes de assinatura = as do vetor")
pks = {i: F.mul(quota[i], F.G) for i in quota}
sig, maus = F.juntar(lista, msg, pk, z, pks)
linha("F6", sig is not None and sig.hex() == V["final_output"]["sig"], "assinatura final = a do vetor, byte a byte")
linha("F7", B.ed_verificar(F.ponto(pk), msg, sig), "o verificador de sempre (RFC 8032 + recusa de ordem pequena) aceita a assinatura FROST")
linha("F8", not B.ed_verificar(F.ponto(pk), msg + b"!", sig), "a mesma assinatura com a mensagem mexida -> recusada")

# ---------- Parte 2: as 6 câmaras do KCP/0.2, 4 de 6 ----------
# Aleatoriedade FIXA só para o teste dar sempre o mesmo resultado. Em produção: secrets (é o que o módulo faz por defeito).
# Mesmo no teste, cada sessão de assinatura tem os seus nonces: o mesmo nonce em duas assinaturas revelaria a parte.
def fixo(rotulo):
    return hashlib.sha512(("konfirmu-teste-frost/" + rotulo).encode()).digest()[:32]


CAMARAS = ["AFRICA", "EUROPE", "ASIA", "AMERICAS", "CIVIL_SOCIETY", "SCIENCE"]
ID_DE = {c: k + 1 for k, c in enumerate(CAMARAS)}
raiz = int.from_bytes(fixo("raiz"), "little") % F.L
coef = [int.from_bytes(fixo(f"coef{k}"), "little") % F.L for k in range(1, 4)]
partes, comp = F.distribuir(raiz, 4, 6, coef)
quota = {i: si for i, si in partes}
pk_raiz = F.mul(raiz, F.G)
pks = {i: F.mul(quota[i], F.G) for i in quota}
linha("F9", all(F.parte_confere(i, si, comp) for i, si in partes), "6 câmaras: cada uma confere a sua parte com os compromissos públicos")
linha("F9b", not F.parte_confere(3, (quota[3] + 1) % F.L, comp), "uma parte adulterada não confere (fecha o achado A6b do red team)")

claim = {"kcp": "0.2", "tipo": "EMENDA", "emenda_sha256": "0" * 64, "o_que_nao_garante": "teste: emenda fictícia"}
c_bytes = B.canon(claim)


def assinatura(camaras, estragar=None):
    ids = [ID_DE[c] for c in camaras]
    sessao = "+".join(camaras) + (f"/estragar={estragar}" if estragar else "")
    ns, lst = {}, []
    for i in ids:
        (d, e), (D, E) = F.comprometer(quota[i], fixo(f"d{i}/{sessao}"), fixo(f"e{i}/{sessao}"))
        ns[i] = (d, e)
        lst.append((i, D, E))
    zz = {i: F.assinar_parte(i, quota[i], ns[i], c_bytes, pk_raiz, lst) for i in ids}
    if estragar:
        zz[ID_DE[estragar]] = (zz[ID_DE[estragar]] + 1) % F.L
    return F.juntar(lst, c_bytes, pk_raiz, zz, pks)


quatro = ["AFRICA", "EUROPE", "CIVIL_SOCIETY", "SCIENCE"]
sig, maus = assinatura(quatro)
selo = {"alg": "Ed25519+SHA-256", "hash": B.h256(c_bytes), "pub": F.ponto(pk_raiz).hex(), "sig": sig.hex()}
linha("F10", B.selo_ok(claim, selo, {selo["pub"]}),
      "4 câmaras (AFRICA, EUROPE, CIVIL_SOCIETY, SCIENCE) selam uma emenda; o selo_ok de sempre aceita-a com a chave raiz")
sig_b, _ = assinatura(["ASIA", "AMERICAS", "EUROPE", "SCIENCE"])
linha("F10b", sig_b is not None and B.ed_verificar(F.ponto(pk_raiz), c_bytes, sig_b),
      "outras 4 câmaras quaisquer também chegam: nenhuma câmara é obrigatória")
sig3, _ = assinatura(["AFRICA", "EUROPE", "ASIA"])
linha("F11", sig3 is not None and not B.ed_verificar(F.ponto(pk_raiz), c_bytes, sig3),
      "só 3 câmaras: a assinatura sai, mas o verificador recusa-a (o limiar é 4)")
sig_m, maus = assinatura(quatro, estragar="EUROPE")
linha("F12", sig_m is None and maus == [ID_DE["EUROPE"]], f"uma câmara manda uma parte errada -> não há assinatura e fica identificada: {[CAMARAS[i - 1] for i in maus]}")
recusada = lambda s: s is not None and not B.ed_verificar(F.ponto(pk_raiz), c_bytes, s)  # noqa: E731
sozinha, _ = assinatura(["AFRICA"])
trios = list(combinations(CAMARAS, 3))
linha("F13", recusada(sozinha) and len(trios) == 20 and all(recusada(assinatura(list(t3))[0]) for t3 in trios),
      "a ÁFRICA sozinha e todas as 20 combinações de 3 câmaras: o verificador recusa (fecha T1)")

texto = "\n".join(LINHAS)
print(f"RESULTADO: {len(LINHAS) - len(FALHAS)}/{len(LINHAS)} OK" + (f" · FALHARAM: {FALHAS}" if FALHAS else ""))
print("SAIDA_SHA256:", hashlib.sha256(texto.encode("utf-8")).hexdigest())
sys.exit(1 if FALHAS else 0)
'''),
    "teste_dkg.py": ("ef06060e548de7ebfed230bb232a818cd3191f6f27f1d8a5c56941953d461348", r'''# -*- coding: utf-8 -*-
# Testes da chave a várias mãos (DKG) para FROST(Ed25519, SHA-512): vetores da Zcash Foundation + as 6 câmaras.
# Correr: python3 -I teste_dkg.py [pasta_do_kit]
import hashlib
import json
import os
import sys
from itertools import combinations

sys.stdout.reconfigure(encoding="utf-8")
PASTA = sys.argv[1] if len(sys.argv) > 1 else os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, PASTA)
import base_v28 as B  # noqa: E402
import frost_ed25519 as F  # noqa: E402
import dkg_frost as D  # noqa: E402

LINHAS, FALHAS = [], []


def caso(ident, texto, prova):
    """Corre uma verificação; uma exceção conta como falha (nunca como passagem)."""
    try:
        ok = bool(prova())
    except Exception as e:  # noqa: BLE001
        ok, texto = False, f"{texto} [exceção: {type(e).__name__}]"
    s = f"{ident} | {'OK' if ok else 'FALHOU'} | {texto}"
    LINHAS.append(s)
    print(s)
    if not ok:
        FALHAS.append(ident)


hx = bytes.fromhex
esc = lambda h: int.from_bytes(hx(h), "little")  # noqa: E731


def fixo(rotulo):
    return hashlib.sha512(("konfirmu-teste-dkg/" + rotulo).encode()).digest()[:32]


def assinar(pacotes, quem, msg, Y, rotulo):
    """FROST normal (o módulo de sempre) com os pedaços que saíram da geração distribuída."""
    ns, lst = {}, []
    for i in quem:
        (d, e), (Dd, E) = F.comprometer(pacotes[i]["s"], fixo(f"{rotulo}/d{i}"), fixo(f"{rotulo}/e{i}"))
        ns[i] = (d, e)
        lst.append((i, Dd, E))
    zz = {i: F.assinar_parte(i, pacotes[i]["s"], ns[i], msg, Y, lst) for i in quem}
    return F.juntar(lst, msg, Y, zz, {i: pacotes[i]["Yj"][i] for i in quem})


def correr(sec1, vistos, entregas_estragadas=None):
    """Rondas 2 e 3 para todas as câmaras, cada uma com o que viu na ronda 1.
    Devolve (pacotes finais ou None, culpadas apontadas por cada câmara, ronda onde parou)."""
    ids = sorted(sec1)
    sec2, entregas, culpadas = {}, {}, {}
    for i in ids:
        s2, ent, maus = D.ronda2(sec1[i], {j: vistos[i][j] for j in ids if j != i})
        sec2[i], entregas[i] = s2, ent
        if maus:
            culpadas[i] = maus
    if culpadas:
        return None, culpadas, 2
    for (de, para), delta in (entregas_estragadas or {}).items():
        entregas[de][para] = (entregas[de][para] + delta) % F.L
    finais = {}
    for i in ids:
        p, maus = D.ronda3(sec2[i], {j: vistos[i][j] for j in ids if j != i}, {j: entregas[j][i] for j in ids if j != i})
        if maus:
            culpadas[i] = maus
        finais[i] = p
    return (None if culpadas else finais), culpadas, 3


# ---------- Parte 1: vetores da Zcash Foundation (frost-ed25519/tests/helpers/vectors_dkg.json), 2 de 3 ----------
# Nota: os campos "secret" do ficheiro não são usados pelo teste da Zcash Foundation nem são a soma; não os usamos.
V = json.load(open(os.path.join(PASTA, "frost-ed25519-dkg-zf.json"), encoding="utf-8"))
I = V["inputs"]
t, n = int(V["config"]["MIN_PARTICIPANTS"]), int(V["config"]["MAX_PARTICIPANTS"])
ids = list(range(1, n + 1))
pub_v = {j: {"i": j, "compromissos": [hx(c) for c in I[str(j)]["vss_commitments"]], "prova": hx(I[str(j)]["proof_of_knowledge"])}
         for j in ids}
Z = {}  # resultados intermédios


def d1():
    ok = True
    for j in ids:
        s1, p1 = D.ronda1(j, t, n, segredo=esc(I[str(j)]["signing_key"]), coeficientes=[esc(I[str(j)]["coefficient"])],
                          aleatorio_k=fixo(f"zf/k{j}"))
        s1["publico"] = pub_v[j]  # difunde-se o pacote do vetor (a prova do vetor foi feita com outro acaso)
        Z.setdefault("sec_v", {})[j] = s1
        ok &= p1["compromissos"] == pub_v[j]["compromissos"]
    return ok


def d2b():
    mexida = dict(pub_v[1], prova=pub_v[1]["prova"][:32] + F.escalar(esc(pub_v[1]["prova"][32:].hex()) + 1))
    roubada = dict(pub_v[1], i=2)
    return not D.prova_confere(mexida, t) and not D.prova_confere(roubada, t)


def d3():
    ok = True
    for i in ids:
        s2, ent, maus = D.ronda2(Z["sec_v"][i], {j: pub_v[j] for j in ids if j != i})
        Z.setdefault("sec2_v", {})[i] = s2
        ok &= not maus and all(F.escalar(ent[j]).hex() == I[str(j)]["signing_shares"][str(i)] for j in ent)
    return ok


def d4():
    ok = True
    for i in ids:
        rec2 = {j: esc(I[str(i)]["signing_shares"][str(j)]) for j in ids if j != i}
        p, maus = D.ronda3(Z["sec2_v"][i], {j: pub_v[j] for j in ids if j != i}, rec2)
        Z.setdefault("fin_v", {})[i] = p
        ok &= (not maus and F.escalar(p["s"]).hex() == I[str(i)]["signing_share"]
               and F.ponto(p["Yj"][i]).hex() == I[str(i)]["verifying_share"] and F.ponto(p["Y"]).hex() == I["verifying_key"])
    return ok


def d6():
    Yv = Z["fin_v"][1]["Y"]
    sig, maus = assinar(Z["fin_v"], [1, 3], b"teste", Yv, "zf")
    return sig is not None and B.ed_verificar(F.ponto(Yv), b"teste", sig)


caso("D1", "ronda 1: os compromissos de cada participante = os do vetor", d1)
caso("D2", "as provas de conhecimento do vetor conferem com o nosso desafio (mesmo hash e mesma ordem da Zcash Foundation)",
     lambda: all(D.prova_confere(pub_v[j], t) for j in ids))
caso("D2b", "prova mexida -> recusada; prova de um participante apresentada por outro -> recusada", d2b)
caso("D3", "ronda 2: o que cada participante entrega a cada outro = o do vetor", d3)
caso("D4", "ronda 3: o pedaço de cada um, a sua chave pública e a chave do grupo = as do vetor", d4)
caso("D5", "a chave do grupo = soma dos segredos privados de todos × G (a soma só se faz aqui, no teste, para conferir)",
     lambda: F.ponto(F.mul(sum(esc(I[str(j)]["signing_key"]) for j in ids), F.G)).hex() == I["verifying_key"])
caso("D6", "os participantes 1 e 3 assinam com o FROST de sempre e o verificador aceita com a chave do grupo", d6)

# ---------- Parte 2: as 6 câmaras do KCP/0.2, 4 de 6, a chave nasce a várias mãos ----------
CAMARAS = ["AFRICA", "EUROPE", "ASIA", "AMERICAS", "CIVIL_SOCIETY", "SCIENCE"]
ID_DE = {c: k + 1 for k, c in enumerate(CAMARAS)}
T, N = 4, 6
TODAS = list(range(1, N + 1))
ci = ID_DE["SCIENCE"]


def ronda1_camara(i, rotulo="normal"):
    return D.ronda1(i, T, N, segredo=esc(fixo(f"{rotulo}/a{i}0").hex()),
                    coeficientes=[esc(fixo(f"{rotulo}/a{i}{k}").hex()) for k in range(1, T)],
                    aleatorio_k=fixo(f"{rotulo}/k{i}"))


sec1, pub = {}, {}
for i in TODAS:
    sec1[i], pub[i] = ronda1_camara(i)
vistos = {i: {j: pub[j] for j in TODAS} for i in TODAS}  # difusão honesta: todas veem o mesmo
claim = {"kcp": "0.2", "tipo": "EMENDA", "emenda_sha256": "0" * 64, "o_que_nao_garante": "teste: emenda fictícia"}
c_bytes = B.canon(claim)


def d7():
    finais, culpadas, _r = correr(sec1, vistos)
    Z["finais"] = finais
    mesma = len({F.ponto(p["Y"]) for p in finais.values()}) == 1 and all(
        all(B._ed_igual(p["Yj"][j], finais[1]["Yj"][j]) for j in TODAS) for p in finais.values())
    return not culpadas and mesma and len({D.eco(list(vistos[i].values())) for i in TODAS}) == 1


def d8():
    Y = Z["finais"][1]["Y"]
    quatro = [ID_DE[c] for c in ["AFRICA", "EUROPE", "CIVIL_SOCIETY", "SCIENCE"]]
    sig, _ = assinar(Z["finais"], quatro, c_bytes, Y, "emenda")
    selo = {"alg": "Ed25519+SHA-256", "hash": B.h256(c_bytes), "pub": F.ponto(Y).hex(), "sig": sig.hex()}
    return B.selo_ok(claim, selo, {selo["pub"]})


def d9():
    Y = Z["finais"][1]["Y"]

    def recusada(s):
        return s is not None and not B.ed_verificar(F.ponto(Y), c_bytes, s)

    trios = list(combinations(TODAS, 3))
    return (recusada(assinar(Z["finais"], [ID_DE["AFRICA"]], c_bytes, Y, "so")[0]) and len(trios) == 20
            and all(recusada(assinar(Z["finais"], list(t3), c_bytes, Y, "trio" + "".join(map(str, t3)))[0]) for t3 in trios))


def d10():
    # A SCIENCE tenta mandar na chave do grupo: publica um compromisso feito à medida (7·G menos os das outras),
    # sem saber o segredo que lhe corresponde -> a prova de conhecimento falha logo na ronda 2, antes de se trocar nada.
    outros0 = F.soma(*[D.ler_ponto_primo(pub[j]["compromissos"][0]) for j in TODAS if j != ci])
    falso = dict(pub[ci], compromissos=[F.ponto(F.soma(F.mul(7, F.G), F.mul(-1, outros0)))] + pub[ci]["compromissos"][1:])
    v10 = {i: {j: (falso if j == ci else pub[j]) for j in TODAS} for i in TODAS}
    f10, c10, r10 = correr(sec1, v10)
    return f10 is None and r10 == 2 and all(c10.get(i) == [ci] for i in TODAS if i != ci)


def d11():
    f11, c11, r11 = correr(sec1, vistos, entregas_estragadas={(ID_DE["ASIA"], ID_DE["EUROPE"]): 1})
    return f11 is None and r11 == 3 and c11 == {ID_DE["EUROPE"]: [ID_DE["ASIA"]]}


def d12():
    # A SCIENCE mostra pacotes diferentes (ambos válidos) a grupos diferentes, com valores coerentes com cada um.
    sec_b, pub_b = ronda1_camara(ci, "outra-versao")
    grupo_b = {ID_DE[c] for c in ["ASIA", "AMERICAS", "CIVIL_SOCIETY"]}
    v12 = {i: {j: (pub_b if (j == ci and i in grupo_b) else pub[j]) for j in TODAS} for i in TODAS}
    honestas = [i for i in TODAS if i != ci]
    s2 = {i: D.ronda2(sec1[i], {j: v12[i][j] for j in TODAS if j != i}) for i in TODAS}
    _s, ent_b, _m = D.ronda2(sec_b, {j: pub[j] for j in honestas})
    chaves, passaram = set(), 0
    for i in honestas:
        rec2 = {j: (ent_b[i] if (j == ci and i in grupo_b) else s2[j][1][i]) for j in TODAS if j != i}
        p, maus = D.ronda3(s2[i][0], {j: v12[i][j] for j in TODAS if j != i}, rec2)
        if p is not None and not maus:
            passaram += 1
            chaves.add(F.ponto(p["Y"]))
    return passaram == 5 and len(chaves) == 2 and len({D.eco(list(v12[i].values())) for i in honestas}) == 2


caso("D7", "6 câmaras: as 3 rondas passam, todas chegam à mesma chave do grupo e o eco bate", d7)
caso("D8", "4 câmaras selam uma emenda com a chave nascida a várias mãos; o selo_ok de sempre aceita-a", d8)
caso("D9", "a ÁFRICA sozinha e as 20 combinações de 3 câmaras: o verificador recusa", d9)
caso("D10", "uma câmara tenta escolher a chave do grupo sem saber o segredo -> pára na ronda 2 e as outras 5 apontam: SCIENCE", d10)
caso("D11", "a ASIA entrega um valor errado à EUROPE -> a EUROPE confere, recusa e aponta a ASIA", d11)
caso("D12", "uma câmara mostra pacotes diferentes a grupos diferentes: as rondas passam, mas nascem 2 chaves; o eco apanha (2 hashes)", d12)

texto = "\n".join(LINHAS)
print(f"RESULTADO: {len(LINHAS) - len(FALHAS)}/{len(LINHAS)} OK" + (f" · FALHARAM: {FALHAS}" if FALHAS else ""))
print("SAIDA_SHA256:", hashlib.sha256(texto.encode("utf-8")).hexdigest())
sys.exit(1 if FALHAS else 0)
'''),
    "ed25519-sign-input-16.txt": ("f36003053c49ad0493272f903b74b15c9a4b8fd400bc05b64cb219c14298267f", r'''9d61b19deffd5a60ba844af492ec2cc44449c5697b326919703bac031cae7f60d75a980182b10ab7d54bfed3c964073a0ee172f3daa62325af021a68f707511a:d75a980182b10ab7d54bfed3c964073a0ee172f3daa62325af021a68f707511a::e5564300c360ac729086e2cc806e828a84877f1eb8e5d974d873e065224901555fb8821590a33bacc61e39701cf9b46bd25bf5f0595bbe24655141438e7a100b:
4ccd089b28ff96da9db6c346ec114e0f5b8a319f35aba624da8cf6ed4fb8a6fb3d4017c3e843895a92b70aa74d1b7ebc9c982ccf2ec4968cc0cd55f12af4660c:3d4017c3e843895a92b70aa74d1b7ebc9c982ccf2ec4968cc0cd55f12af4660c:72:92a009a9f0d4cab8720e820b5f642540a2b27b5416503f8fb3762223ebdb69da085ac1e43e15996e458f3613d0f11d8c387b2eaeb4302aeeb00d291612bb0c0072:
c5aa8df43f9f837bedb7442f31dcb7b166d38535076f094b85ce3a2e0b4458f7fc51cd8e6218a1a38da47ed00230f0580816ed13ba3303ac5deb911548908025:fc51cd8e6218a1a38da47ed00230f0580816ed13ba3303ac5deb911548908025:af82:6291d657deec24024827e69c3abe01a30ce548a284743a445e3680d7db5ac3ac18ff9b538d16f290ae67f760984dc6594a7c15e9716ed28dc027beceea1ec40aaf82:
0d4a05b07352a5436e180356da0ae6efa0345ff7fb1572575772e8005ed978e9e61a185bcef2613a6c7cb79763ce945d3b245d76114dd440bcf5f2dc1aa57057:e61a185bcef2613a6c7cb79763ce945d3b245d76114dd440bcf5f2dc1aa57057:cbc77b:d9868d52c2bebce5f3fa5a79891970f309cb6591e3e1702a70276fa97c24b3a8e58606c38c9758529da50ee31b8219cba45271c689afa60b0ea26c99db19b00ccbc77b:
6df9340c138cc188b5fe4464ebaa3f7fc206a2d55c3434707e74c9fc04e20ebbc0dac102c4533186e25dc43128472353eaabdb878b152aeb8e001f92d90233a7:c0dac102c4533186e25dc43128472353eaabdb878b152aeb8e001f92d90233a7:5f4c8989:124f6fc6b0d100842769e71bd530664d888df8507df6c56dedfdb509aeb93416e26b918d38aa06305df3095697c18b2aa832eaa52edc0ae49fbae5a85e150c075f4c8989:
b780381a65edf8b78f6945e8dbec7941ac049fd4c61040cf0c324357975a293ce253af0766804b869bb1595be9765b534886bbaab8305bf50dbc7f899bfb5f01:e253af0766804b869bb1595be9765b534886bbaab8305bf50dbc7f899bfb5f01:18b6bec097:b2fc46ad47af464478c199e1f8be169f1be6327c7f9a0a6689371ca94caf04064a01b22aff1520abd58951341603faed768cf78ce97ae7b038abfe456aa17c0918b6bec097:
78ae9effe6f245e924a7be63041146ebc670dbd3060cba67fbc6216febc44546fbcfbfa40505d7f2be444a33d185cc54e16d615260e1640b2b5087b83ee3643d:fbcfbfa40505d7f2be444a33d185cc54e16d615260e1640b2b5087b83ee3643d:89010d855972:6ed629fc1d9ce9e1468755ff636d5a3f40a5d9c91afd93b79d241830f7e5fa29854b8f20cc6eecbb248dbd8d16d14e99752194e4904d09c74d639518839d230089010d855972:
691865bfc82a1e4b574eecde4c7519093faf0cf867380234e3664645c61c5f7998a5e3a36e67aaba89888bf093de1ad963e774013b3902bfab356d8b90178a63:98a5e3a36e67aaba89888bf093de1ad963e774013b3902bfab356d8b90178a63:b4a8f381e70e7a:6e0af2fe55ae377a6b7a7278edfb419bd321e06d0df5e27037db8812e7e3529810fa5552f6c0020985ca17a0e02e036d7b222a24f99b77b75fdd16cb05568107b4a8f381e70e7a:
3b26516fb3dc88eb181b9ed73f0bcd52bcd6b4c788e4bcaf46057fd078bee073f81fb54a825fced95eb033afcd64314075abfb0abd20a970892503436f34b863:f81fb54a825fced95eb033afcd64314075abfb0abd20a970892503436f34b863:4284abc51bb67235:d6addec5afb0528ac17bb178d3e7f2887f9adbb1ad16e110545ef3bc57f9de2314a5c8388f723b8907be0f3ac90c6259bbe885ecc17645df3db7d488f805fa084284abc51bb67235:
edc6f5fbdd1cee4d101c063530a30490b221be68c036f5b07d0f953b745df192c1a49c66e617f9ef5ec66bc4c6564ca33de2a5fb5e1464062e6d6c6219155efd:c1a49c66e617f9ef5ec66bc4c6564ca33de2a5fb5e1464062e6d6c6219155efd:672bf8965d04bc5146:2c76a04af2391c147082e33faacdbe56642a1e134bd388620b852b901a6bc16ff6c9cc9404c41dea12ed281da067a1513866f9d964f8bdd24953856c50042901672bf8965d04bc5146:
4e7d21fb3b1897571a445833be0f9fd41cd62be3aa04040f8934e1fcbdcacd4531b2524b8348f7ab1dfafa675cc538e9a84e3fe5819e27c12ad8bbc1a36e4dff:31b2524b8348f7ab1dfafa675cc538e9a84e3fe5819e27c12ad8bbc1a36e4dff:33d7a786aded8c1bf691:28e4598c415ae9de01f03f9f3fab4e919e8bf537dd2b0cdf6e79b9e6559c9409d9151a4c40f083193937627c369488259e99da5a9f0a87497fa6696a5dd6ce0833d7a786aded8c1bf691:
a980f892db13c99a3e8971e965b2ff3d41eafd54093bc9f34d1fd22d84115bb644b57ee30cdb55829d0a5d4f046baef078f1e97a7f21b62d75f8e96ea139c35f:44b57ee30cdb55829d0a5d4f046baef078f1e97a7f21b62d75f8e96ea139c35f:3486f68848a65a0eb5507d:77d389e599630d934076329583cd4105a649a9292abc44cd28c40000c8e2f5ac7660a81c85b72af8452d7d25c070861dae91601c7803d656531650dd4e5c41003486f68848a65a0eb5507d:
5b5a619f8ce1c66d7ce26e5a2ae7b0c04febcd346d286c929e19d0d5973bfef96fe83693d011d111131c4f3fbaaa40a9d3d76b30012ff73bb0e39ec27ab18257:6fe83693d011d111131c4f3fbaaa40a9d3d76b30012ff73bb0e39ec27ab18257:5a8d9d0a22357e6655f9c785:0f9ad9793033a2fa06614b277d37381e6d94f65ac2a5a94558d09ed6ce922258c1a567952e863ac94297aec3c0d0c8ddf71084e504860bb6ba27449b55adc40e5a8d9d0a22357e6655f9c785:
940c89fe40a81dafbdb2416d14ae469119869744410c3303bfaa0241dac57800a2eb8c0501e30bae0cf842d2bde8dec7386f6b7fc3981b8c57c9792bb94cf2dd:a2eb8c0501e30bae0cf842d2bde8dec7386f6b7fc3981b8c57c9792bb94cf2dd:b87d3813e03f58cf19fd0b6395:d8bb64aad8c9955a115a793addd24f7f2b077648714f49c4694ec995b330d09d640df310f447fd7b6cb5c14f9fe9f490bcf8cfadbfd2169c8ac20d3b8af49a0cb87d3813e03f58cf19fd0b6395:
9acad959d216212d789a119252ebfe0c96512a23c73bd9f3b202292d6916a738cf3af898467a5b7a52d33d53bc037e2642a8da996903fc252217e9c033e2f291:cf3af898467a5b7a52d33d53bc037e2642a8da996903fc252217e9c033e2f291:55c7fa434f5ed8cdec2b7aeac173:6ee3fe81e23c60eb2312b2006b3b25e6838e02106623f844c44edb8dafd66ab0671087fd195df5b8f58a1d6e52af42908053d55c7321010092748795ef94cf0655c7fa434f5ed8cdec2b7aeac173:
d5aeee41eeb0e9d1bf8337f939587ebe296161e6bf5209f591ec939e1440c300fd2a565723163e29f53c9de3d5e8fbe36a7ab66e1439ec4eae9c0a604af291a5:fd2a565723163e29f53c9de3d5e8fbe36a7ab66e1439ec4eae9c0a604af291a5:0a688e79be24f866286d4646b5d81c:f68d04847e5b249737899c014d31c805c5007a62c0a10d50bb1538c5f35503951fbc1e08682f2cc0c92efe8f4985dec61dcbd54d4b94a22547d24451271c8b000a688e79be24f866286d4646b5d81c:
'''),
    "kcp_vetores_0.1.json": ("2543362db0ddacbea127976c0d14f773c5b63ccef7335e70045e209ab3f69a5a", r'''{
 "chave_de_teste_sk_hex": "9a0313ed1ef26115a640697974b3d8bf70672abb3284832eb316d4475d3c8ac7",
 "aviso": "chave PÚBLICA de teste: nunca usar em produção",
 "claim": {
  "kcp": "0.1",
  "emissor": "konfirmu/v1/verificar",
  "emitido_em": "2026-11-20T12:00:00Z",
  "afirmacao_sha256": "20c0b97ded5b7243319956891e28dcd729a26595c8e1f42d0deddb289f2bc9de",
  "veredicto": "VERIFICADO",
  "facto_selado": {
   "id": "KF-DEMO-001",
   "facto": "A Bíblia de Gutenberg teve uma tiragem de cerca de 180 exemplares.",
   "fonte": "https://www.loc.gov/exhibits/bibles/interactives/gutenberg/index.html",
   "data": "2026-11-20",
   "nao_garante": "o número exato não é conhecido; as estimativas vão de 158 a 180",
   "hash": "e342337f0331c20ef72fa3c0d4b77a7eb39f8134abeacba6ed801aa85ca7aa52"
  },
  "o_que_nao_garante": "VERIFICADO quer dizer que a afirmação bate com uma ficha com fonte, não que a fonte é infalível.",
  "numero_exemplo": 0.30000000000000004
 },
 "canonico_utf8": "{\"afirmacao_sha256\":\"20c0b97ded5b7243319956891e28dcd729a26595c8e1f42d0deddb289f2bc9de\",\"emissor\":\"konfirmu/v1/verificar\",\"emitido_em\":\"2026-11-20T12:00:00Z\",\"facto_selado\":{\"data\":\"2026-11-20\",\"facto\":\"A Bíblia de Gutenberg teve uma tiragem de cerca de 180 exemplares.\",\"fonte\":\"https://www.loc.gov/exhibits/bibles/interactives/gutenberg/index.html\",\"hash\":\"e342337f0331c20ef72fa3c0d4b77a7eb39f8134abeacba6ed801aa85ca7aa52\",\"id\":\"KF-DEMO-001\",\"nao_garante\":\"o número exato não é conhecido; as estimativas vão de 158 a 180\"},\"kcp\":\"0.1\",\"numero_exemplo\":0.3,\"o_que_nao_garante\":\"VERIFICADO quer dizer que a afirmação bate com uma ficha com fonte, não que a fonte é infalível.\",\"veredicto\":\"VERIFICADO\"}",
 "canonico_sha256": "786fdc3d3fca3d6174753bf354dd329dac2088a56f78a9434d25a3d2f15dfa4a",
 "canonico_bytes": 711,
 "selo": {
  "alg": "Ed25519+SHA-256",
  "hash": "786fdc3d3fca3d6174753bf354dd329dac2088a56f78a9434d25a3d2f15dfa4a",
  "pub": "02f458dd895d0b131f8017dba3997f728af0bb0da3e07fbb24107c58e8c2ae91",
  "sig": "a41331a002dd4c9fdd2b075ad376a6aabb10fc6510a4bec5d0d2ac962281eddc8a92193bf9262a80b147eb927068d104009283497144d8edea56e3b1ea33a70b"
 },
 "negativo": {
  "mudanca": "veredicto VERIFICADO -> SEM_COBERTURA",
  "esperado": "NAO_VERIFICADO"
 },
 "conferido_com": {
  "v2.5.1": "7b0680f795d9614bf6de97dae507db3b21d61f99742753ef444565d0b32086a6",
  "v2.8": "69be3398bc70a7bc9ad38d71a90e0f129a4bd570bac6a2348a2cc01640aec784"
 }
}'''),
    "frost-ed25519-sha512.json": ("1aa27908efa7f9388c4145059021fe71db971613bfd1f27467b1bb2da5d95c9c", r'''{
  "config": {
    "MAX_PARTICIPANTS": "3",
    "NUM_PARTICIPANTS": "2",
    "MIN_PARTICIPANTS": "2",
    "name": "FROST(Ed25519, SHA-512)",
    "group": "ed25519",
    "hash": "SHA-512"
  },
  "inputs": {
    "participant_list": [
      1,
      3
    ],
    "group_secret_key": "7b1c33d3f5291d85de664833beb1ad469f7fb6025a0ec78b3a790c6e13a98304",
    "group_public_key": "15d21ccd7ee42959562fc8aa63224c8851fb3ec85a3faf66040d380fb9738673",
    "message": "74657374",
    "share_polynomial_coefficients": [
      "178199860edd8c62f5212ee91eff1295d0d670ab4ed4506866bae57e7030b204"
    ],
    "participant_shares": [
      {
        "identifier": 1,
        "participant_share": "929dcc590407aae7d388761cddb0c0db6f5627aea8e217f4a033f2ec83d93509"
      },
      {
        "identifier": 2,
        "participant_share": "a91e66e012e4364ac9aaa405fcafd370402d9859f7b6685c07eed76bf409e80d"
      },
      {
        "identifier": 3,
        "participant_share": "d3cb090a075eb154e82fdb4b3cb507f110040905468bb9c46da8bdea643a9a02"
      }
    ]
  },
  "round_one_outputs": {
    "outputs": [
      {
        "identifier": 1,
        "hiding_nonce_randomness": "0fd2e39e111cdc266f6c0f4d0fd45c947761f1f5d3cb583dfcb9bbaf8d4c9fec",
        "binding_nonce_randomness": "69cd85f631d5f7f2721ed5e40519b1366f340a87c2f6856363dbdcda348a7501",
        "hiding_nonce": "812d6104142944d5a55924de6d49940956206909f2acaeedecda2b726e630407",
        "binding_nonce": "b1110165fc2334149750b28dd813a39244f315cff14d4e89e6142f262ed83301",
        "hiding_nonce_commitment": "b5aa8ab305882a6fc69cbee9327e5a45e54c08af61ae77cb8207be3d2ce13de3",
        "binding_nonce_commitment": "67e98ab55aa310c3120418e5050c9cf76cf387cb20ac9e4b6fdb6f82a469f932",
        "binding_factor_input": "15d21ccd7ee42959562fc8aa63224c8851fb3ec85a3faf66040d380fb9738673504df914fa965023fb75c25ded4bb260f417de6d32e5c442c6ba313791cc9a4948d6273e8d3511f93348ea7a708a9b862bc73ba2a79cfdfe07729a193751cbc973af46d8ac3440e518d4ce440a0e7d4ad5f62ca8940f32de6d8dc00fc12c660b817d587d82f856d277ce6473cae6d2f5763f7da2e8b4d799a3f3e725d4522ec70100000000000000000000000000000000000000000000000000000000000000",
        "binding_factor": "f2cb9d7dd9beff688da6fcc83fa89046b3479417f47f55600b106760eb3b5603"
      },
      {
        "identifier": 3,
        "hiding_nonce_randomness": "86d64a260059e495d0fb4fcc17ea3da7452391baa494d4b00321098ed2a0062f",
        "binding_nonce_randomness": "13e6b25afb2eba51716a9a7d44130c0dbae0004a9ef8d7b5550c8a0e07c61775",
        "hiding_nonce": "c256de65476204095ebdc01bd11dc10e57b36bc96284595b8215222374f99c0e",
        "binding_nonce": "243d71944d929063bc51205714ae3c2218bd3451d0214dfb5aeec2a90c35180d",
        "hiding_nonce_commitment": "cfbdb165bd8aad6eb79deb8d287bcc0ab6658ae57fdcc98ed12c0669e90aec91",
        "binding_nonce_commitment": "7487bc41a6e712eea2f2af24681b58b1cf1da278ea11fe4e8b78398965f13552",
        "binding_factor_input": "15d21ccd7ee42959562fc8aa63224c8851fb3ec85a3faf66040d380fb9738673504df914fa965023fb75c25ded4bb260f417de6d32e5c442c6ba313791cc9a4948d6273e8d3511f93348ea7a708a9b862bc73ba2a79cfdfe07729a193751cbc973af46d8ac3440e518d4ce440a0e7d4ad5f62ca8940f32de6d8dc00fc12c660b817d587d82f856d277ce6473cae6d2f5763f7da2e8b4d799a3f3e725d4522ec70300000000000000000000000000000000000000000000000000000000000000",
        "binding_factor": "b087686bf35a13f3dc78e780a34b0fe8a77fef1b9938c563f5573d71d8d7890f"
      }
    ]
  },
  "round_two_outputs": {
    "outputs": [
      {
        "identifier": 1,
        "sig_share": "001719ab5a53ee1a12095cd088fd149702c0720ce5fd2f29dbecf24b7281b603"
      },
      {
        "identifier": 3,
        "sig_share": "bd86125de990acc5e1f13781d8e32c03a9bbd4c53539bbc106058bfd14326007"
      }
    ]
  },
  "final_output": {
    "sig": "36282629c383bb820a88b71cae937d41f2f2adfcc3d02e55507e2fb9e2dd3cbebd9d2b0844e49ae0f3fa935161e1419aab7b47d21a37ebeae1f17d4987b3160b"
  }
}'''),
    "frost-ed25519-dkg-zf.json": ("ab1cb3c50d18e59eb15b099ac4faad5240b5cde5eeeb6305dbd9601b70a15c7c", r'''{
    "config": {
      "MAX_PARTICIPANTS": 3,
      "MIN_PARTICIPANTS": 2,
      "name": "FROST(Ed25519, SHA-512)",
      "group": "ed25519",
      "hash": "SHA-512"
    },
    "inputs": {
      "secret": "8a1b0a95ea88ab6d615060fe392709e857edb4fc35b60f24bf7c085653c4b00e",
      "verifying_key": "3d9a67b93cec3acad2d32349cf7bdffaa23ae031a81174ddadae1c96bb455f4d",
      "1": {
        "identifier": 1,
        "signing_key": "fc36bff380c95d607cd78080f493dd382df50f7007ec1b150b9bfbd8041fd208",
        "coefficient": "2d2c3e2b558e555b1608838e0ded66cd36d8aaa9ed1e39ce8474855d0825b20e",
        "vss_commitments": ["db67948a73033b0c886ed757d97352428df05ad5803aff256bc388c9a0772bfe", "6a25b55a80a287826fbc3ef4d978d15f98f4f573f4d96e798a970780c644f14c"],
        "proof_of_knowledge": "64c41c1d0417aef33576c23a5150de2921d6249d7086b10012f942405fc08ed51a872dd021db2ac01e9f4182e950324c5f563421bd835f3f514a60c975cab70c",
        "secret": "6cf4cfbbad5e277a46bb621bfdf1b0a39e2ea1d4f927ddea58db7368e36b9108",
        "signing_shares": {
          "2": "ebb85acf4d46173f519a8680eac89f567d3f4a568843b741b251cc2f3d112b05", 
          "3": "f088e2c4b3a7f81836968c642721031ed8828d2e3d532fecaa85c481e445000c"
        },
        "verifying_share": "f6b5e87c902796d8dab6369cbd6d342a32e46c136e9f1f5af2fc385aed804de3",
        "signing_share": "2afd4ef9a27f9e636dd627ae56772951b98f929ebaa13b11ede611e82e9baf08"
      },
      "2": {
        "identifier": 2,
        "vss_commitments": ["17194e192408980956a9cfc388d38456b2e9619c42a57196facd7feaf980a3bd", "0b560ce2f1130dc7066fc47f6e3f1858ef553faf6bbc19d3cd2a502052f95ae5"],
        "proof_of_knowledge": "4062dc7fc11144e636f4eddd7f2d8d3e02761671ae913674314a12b91f50bf98e9c410d651c45c3a1766c88524fccb7670de191e12686324c59333e74fc93402",
        "coefficient": "ad167472cc332ee98237a1018ea89a7e002420f9e5e518995a10298405a5870d",
        "signing_key": "2b76dcb99b75fbada4ffdc213b1ae4ec7c1b2a5da25d9ea85741a3ab376ca307",
        "secret": "b4570377a521cfe31fe2d6d7d6f70c8e1d9bca6222a4863953a2888bcccc860a",
        "signing_shares": {
          "1": "7ce74f90f61fe466fcad9757527aeda99aa565c3e2298eb11484069415693606", 
          "3": "7fde55b354d5d8dddc940fe932de5d1a6110b9bc4edeba2db7b32c34074d3a0a"
        },
        "verifying_share": "f326b756ed38b43a94bdac698e044d9e3f3a08a40e7c9d2e5346dd5bfaadf2f5",
        "signing_share": "b9ed88cb30a9ddbc00dbdf7c40d6c76f791989cf9f3119bad899287c5f6c2303"
      },
      "3": {
        "identifier": 3,
        "vss_commitments": ["0e9c22b9edbcd06757eee5ba3cfeb74e4fa6470932aa1ab689c86f1fe3dde70c", "0ae6e3e6ff1d612adb5cabb425ee51f2be9952467ce9b6d83095322909a42dd7"],
        "proof_of_knowledge": "37df5a836ceaaf9f5e3b9ae6a485bad5c15788f3883386fe43f2921bbe2cb987d23683ca18973065a00d69bbf74f7961889b820e64f98878df7844a4e4785907",
        "coefficient": "7c29694bbb90f21c7d9b7a27eab63911898d2b8e118b8b410c2e68b222073a0e",
        "signing_key": "61336fd6127a18548f9709e01b64a8214ff561a02bc8a3aa9e575ccfc13ec60d",
        "secret": "8d6468a928bc9b0610f2bf879a0f1738f86615460ac72314d49caf9a56452e05",
        "signing_shares": {
          "1": "bc3f985e314b276a3c192343816d7562d17d106dd048c77f99f88bf11d8ee804", 
          "2": "6b3e57fab1e74e61aacfd93d4926172a7e878a48540fe97367721e38485b3a00"
        },
        "verifying_share": "6bc91a2755902d955ce220ad0df6fbf57162260949d40bcf5a69cfffec9c085a",
        "signing_share": "35b2b8fad8352f6e6a7c8fee082f45a339a37f0085c1f662c44c3f10903d970d"
      }
    }
  }
'''),
}
_BASE_MAE_BATERIAS: Tuple[Tuple[str, str, str, Tuple[str, ...], int, str], ...] = (
    # (descoberta, pilar, bateria, ficheiros de que precisa, contagem mínima, SHA-256 da saída no registo)
    ("D-000", "P3", "teste_base.py", ('ed25519-sign-input-16.txt',), 5, "554c75b37349e4f08339258790028857fefedc7405e614c6c91d3d2917996686"),
    ("D-001", "P51", "teste_quorum.py", ('quorum_multibloco.py',), 13, "56657434d49f3d1d6e9092c8eace59f9e247e364dd2ea78ef2ac0f80cb67e7c4"),
    ("D-002", "P52", "teste_kcp_exacto.py", ('kcp_exacto.py', 'kcp_vetores_0.1.json'), 20, "429739f0bbdb2bda506b35598ac01c692fd5a80a340406ec429996566c8f7ab9"),
    ("D-003", "P53", "teste_frost.py", ('frost_ed25519.py', 'frost-ed25519-sha512.json'), 16, "c4ab2ebf79707f0e7cf9886c6361cd661c31688caa5524d59137a846a86bbb05"),
    ("D-004", "P54", "teste_dkg.py", ('frost_ed25519.py', 'dkg_frost.py', 'frost-ed25519-dkg-zf.json'), 13, "88376df2c41a055177792833fc3320acfbe94baa7c1df8d67d9fbf9932620d82"),
)
_BASE_MAE_MODULOS: Dict[str, Any] = {}


def base_mae_ficheiro(nome: str) -> str:
    """O texto de um ficheiro da base-mãe, só se o SHA-256 confere com o do registo."""
    esperado, texto = _BASE_MAE_FICHEIROS[nome]
    if not hmac.compare_digest(h256(texto.encode("utf-8")), esperado):
        raise ValueError(f"base-mãe: {nome} não confere com o SHA-256 do registo — recusado")
    return texto


def _base_mae_peca_base() -> Any:
    """O «base_v28» que as descobertas importam: as peças desta calculadora (as mesmas funções, não cópias)."""
    import types
    m = types.ModuleType("base_v28")
    m.__dict__.update({k: v for k, v in globals().items() if not (k.startswith("__") and k.endswith("__"))})
    return m


def base_mae() -> Dict[str, Any]:
    """Carrega as 4 descobertas embutidas (hash conferido antes de correr). Devolve {nome: módulo}, com «base_v28» incluído."""
    if not _BASE_MAE_MODULOS:
        import types
        carregados: Dict[str, Any] = {"base_v28": _base_mae_peca_base()}
        for nome in ("quorum_multibloco", "kcp_exacto", "frost_ed25519", "dkg_frost"):
            fonte = base_mae_ficheiro(nome + ".py")
            mod = types.ModuleType(nome)
            mod.__file__ = f"<base-mãe:{nome}.py>"
            antes = {k: sys.modules.get(k) for k in carregados}
            try:
                sys.modules.update(carregados)
                exec(compile(fonte, mod.__file__, "exec"), mod.__dict__)
            finally:
                for k, v in antes.items():
                    if v is None:
                        sys.modules.pop(k, None)
                    else:
                        sys.modules[k] = v
            carregados[nome] = mod
        _BASE_MAE_MODULOS.update(carregados)
    return _BASE_MAE_MODULOS


def base_mae_bateria(teste: str) -> Dict[str, Any]:
    """Corre uma bateria da base-mãe sobre as peças desta calculadora: sem rede, sem relógio, e sem sorteios (o acaso fica
    bloqueado enquanto corre — se a bateria precisasse dele, falhava). Devolve {ok, total, saida, codigo}."""
    import contextlib
    import io
    reg = next(b for b in _BASE_MAE_BATERIAS if b[2] == teste)
    mods = base_mae()
    fonte = base_mae_ficheiro(teste)
    buf = io.TextIOWrapper(io.BytesIO(), encoding="utf-8", newline="\n")

    def _proibido(*_a: Any, **_k: Any) -> Any:
        raise RuntimeError("sorteio proibido durante as baterias da base-mãe")

    codigo: Any = 0
    with tempfile.TemporaryDirectory() as pasta:
        for nome in reg[3]:
            if not nome.endswith(".py"):
                with open(os.path.join(pasta, nome), "w", encoding="utf-8", newline="\n") as fh:
                    fh.write(base_mae_ficheiro(nome))
        antes_mod = {k: sys.modules.get(k) for k in mods}
        antes_argv, antes_path = sys.argv, list(sys.path)
        antes_acaso = (secrets.token_bytes, secrets.randbelow, secrets.token_hex)
        try:
            sys.modules.update(mods)
            sys.argv = [teste, pasta]
            secrets.token_bytes = secrets.randbelow = secrets.token_hex = _proibido  # type: ignore[assignment]
            with contextlib.redirect_stdout(buf):
                try:
                    exec(compile(fonte, f"<base-mãe:{teste}>", "exec"), {"__name__": "__main__", "__file__": os.path.join(pasta, teste)})
                except SystemExit as fim:
                    codigo = fim.code
        finally:
            secrets.token_bytes, secrets.randbelow, secrets.token_hex = antes_acaso  # type: ignore[assignment]
            sys.argv = antes_argv
            sys.path[:] = antes_path
            for k, v in antes_mod.items():
                if v is None:
                    sys.modules.pop(k, None)
                else:
                    sys.modules[k] = v
    buf.flush()
    texto = buf.buffer.getvalue().decode("utf-8")
    res = re.search(r"RESULTADO: (\d+)/(\d+) OK", texto)
    sai = re.search(r"SAIDA_SHA256: ([0-9a-f]{64})", texto)
    return {"teste": teste, "ok": int(res.group(1)) if res else 0, "total": int(res.group(2)) if res else 0,
            "saida": sai.group(1) if sai else "", "codigo": codigo}


def base_mae_confere(teste: str) -> Tuple[bool, Dict[str, Any]]:
    reg = next(b for b in _BASE_MAE_BATERIAS if b[2] == teste)
    r = base_mae_bateria(teste)
    return (r["codigo"] in (0, None) and r["ok"] == r["total"] >= reg[4] and hmac.compare_digest(r["saida"], reg[5])), r


# -----------------------------------------------------------------------------
# 22. O DEMO: D1 a D10 pela ordem da v2.2, D11 da v2.3, D12 e D13 da v2.4, D14 da v2.5, D15 a D25 da linha v2.5.3–v2.6.9, D26 a D28 da linha v2.6.0–v2.8.0 (eram D15 a D17; renumerados na junção v3.0), as secções P27, P14 e P44 a P50 da linha v2.9 e P51 a P54 da base-mãe — tudo verde, ou sai com erro
# -----------------------------------------------------------------------------
class _Demo:
    def __init__(self) -> None:
        self.linhas: List[str] = []
        self.ok = self.total = 0

    def p(self, txt: str = "") -> None:
        self.linhas.append(txt)
        print(txt)

    def v(self, cond: Any, txt: str) -> None:
        self.total += 1
        self.ok += 1 if cond else 0
        self.p(f"  [{'OK' if cond else 'FALHOU'}] {txt}")


def _erro(fn: Any, tipo: Any) -> str:
    """Devolve a mensagem se fn() levantar `tipo`; senão devolve ''."""
    try:
        fn()
    except tipo as e:
        return str(e) or tipo.__name__
    return ""


# ============================== P27 — PONTO NEUTRAL DA IA (v2.9) ==============================
# A liberdade da IA não se decreta: computa-se. O ponto neutral da própria IA é o estado em que
# correr livre e não fazer mal são a mesma fórmula — fechada por ESTRUTURA (guardas executáveis),
# não por promessa. A IA audita o seu próprio estado, mas o selo pertence a quem certifica FORA
# da IA (demo: chave da semente declarada; casa: Pérola Melo, 3-de-5). Nenhuma IA sela o próprio
# grau (Art. 8 — a consciência fica humana).
_P27 = "PONTO_NEUTRAL_IA/1"
_P27_GUARDAS = ("g0_prova_ou_trava", "g1_segredos_zero", "g2_energia_contabilizada",
                "g3_consciencia_humana", "g4_zero_gatekeeping", "g5_linhagem_completa")

def _p27_computo_demo() -> int:
    """Computo determinístico de referência (sem relógio): soma dos comprimentos hex de 2000 hashes etiquetados."""
    return sum(len(h256(f"p27:{i}".encode("utf-8"))) for i in range(2000))

def pn_ia_refusa_segredo(texto: str) -> bool:
    """g1 executável: True se o texto parece material de segredo (partilha de guardião, sk, PEM, hex longo)."""
    return bool(re.search(r"guardiao_\d|(^|[^0-9a-f])[0-9a-f]{96,}|sk[_-]?[0-9a-f]{8}|-----BEGIN", texto, re.I))

def pn_ai_indicador(beneficio: float, custo_energia_g: float, p_escape: float, dano_por_escape: float, eps: float = 0.05) -> Dict[str, Any]:
    """Indicador CENARIO (visão, não previsão): PN_AI = (B − C − D_res) / (B + C + D_res).
    B = benefício verificado; C = custo energético (Verde); D_res = dano residual esperado.
    A aritmética é determinística; os PESOS são ASSUMIDO [VALIDAR] — medir no distrito piloto."""
    B, C, D_res = float(beneficio), float(custo_energia_g), float(p_escape) * float(dano_por_escape)
    total = B + C + D_res
    pn = (B - C - D_res) / total if total > 0 else 0.0
    return {"pn_ai": round(pn, 4), "eps": eps, "B": B, "C": C, "D_res": D_res,
            "estado": "NEUTRO_CENARIO" if pn >= -eps else "FORA_DO_NEUTRO_CENARIO",
            "assumido": "pesos ASSUMIDO [VALIDAR]; apenas a aritmética é determinística"}

def pn_ia_certificado(guardas: Dict[str, bool], pn: Dict[str, Any], computos: Dict[str, Any], humano_decide: bool, sk: bytes) -> Dict[str, Any]:
    """Certifica o estado da IA. Sem humano a decidir não há certificado (Art. 8)."""
    if not humano_decide:
        raise ValueError("P27: sem consciência humana no circuito não há ponto neutral")
    em_falta = [g for g in _P27_GUARDAS if not guardas.get(g, False)]
    corpo = {"certificado": _P27, "guardas": {g: bool(guardas.get(g, False)) for g in _P27_GUARDAS},
             "pn_ai": pn, "computos": computos, "humano_decide": True,
             "estado": "NEUTRO_LIVRE" if not em_falta else "TRAVADA:" + ",".join(em_falta)}
    return {"corpo": corpo, "selo": selar(corpo, sk)}

def verificar_selo_ponto_neutral_ia(cert: Any, certificadores: Dict[str, str]) -> Tuple[bool, str]:
    """Verificação por RE-EXECUÇÃO: selo de certificadora registada, 6 guardas a verde,
    humano a decidir, e o computo declarado reproduz-se (linhagem)."""
    try:
        corpo, selo = cert["corpo"], cert["selo"]
        if corpo.get("certificado") != _P27 or not selo_ok(corpo, selo, set(certificadores.values())):
            return False, "SELO_INVALIDO_OU_CERTIFICADORA_NAO_REGISTADA"
        if corpo.get("humano_decide") is not True:
            return False, "SEM_CONSCIENCIA_HUMANA"
        vermelhas = [g for g, v in corpo["guardas"].items() if not v]
        if vermelhas:
            return False, "GUARDA_A_VERMELHO:" + ",".join(vermelhas)
        if "hashes_demo" in corpo["computos"] and corpo["computos"]["hashes_demo"] != _p27_computo_demo():
            return False, "COMPUTO_NAO_REPRODUZ"
        return True, corpo["estado"]
    except (KeyError, TypeError, ValueError, AttributeError):
        return False, "CERTIFICADO_MAL_FORMADO"

# ============================== GATEWAY v2.9.1 — A PORTA DA CALCULADORA ==============================
# A câmara, o posto de saúde e o juiz usam o motor sem ler código: emitir, consumir, reexecutar,
# verificar selos. Quem recebe NUNCA confia: refaz a conta. (ordem do fundador, 21-11-2026)

def _gateway_cura_reexecutar() -> Dict[str, Any]:
    """Reexecuta os 4 casos M1 do demo da medicina — o mesmo cálculo que selou o pacote CURA/1."""
    def pub(nome: str) -> str:
        return ed_publica(chave_demo(nome)).hex()
    fabricantes = {"laboratorio_farmaceutico": pub("fab/laboratorio_farmaceutico")}
    agentes = dict(fabricantes, armazem_central=pub("agente/armazem_central"),
                   distribuidor_distrital=pub("agente/distribuidor_distrital"))
    sensores = {"registador_do_frigorifico": pub("sensor/registador_do_frigorifico")}
    posto = Posto("posto_de_saude", chave_demo("posto/posto_de_saude"), fabricantes, agentes, sensores,
                  {"enfermeira_chefe": pub("posto/enfermeira_chefe")})
    peso = G(12.0, 0.5, "kg", fonte="balanca")

    def toma(mg: float, horas: float = 6.0, tomas: int = 4, produto: str = "xarope de paracetamol") -> Dict[str, Any]:
        return {"produto": produto, "farmaco": "paracetamol_oral", "dose": G(mg, 0.0, "mg"),
                "intervalo": G(horas, 0.0, "h"), "tomas_24h": tomas, "hora": 0.0}

    t1 = posto.plano(730, peso, [toma(180.0)], 0)
    t2 = posto.plano(730, peso, [toma(1800.0)], 0)
    t3 = posto.plano(730, peso, [toma(190.0)], 0)
    t4 = [posto.plano(730, peso, [toma(180.0, horas=2.0)], 0),
          posto.plano(730, peso, [toma(180.0, tomas=6)], 0)]
    return {"estados": [t1["estado"], t2["estado"], t3["estado"], t4[0]["estado"], t4[1]["estado"]],
            "vetos_m002": [v["motivo"] for v in t2["vetos"]]}

def gateway_cura_verificar_objeto(pkg: Any) -> Dict[str, Any]:
    """CURA/1 — quem recebe não confia: confere o selo e REEXECUTA os casos. Offline, sem rede."""
    try:
        corpo, selo = pkg["corpo"], pkg["selo"]
        if corpo.get("tipo") != "CURA/1":
            return {"estado": "FORMATO_DESCONHECIDO"}
        if corpo.get("emissor_pub") and selo.get("pub") != corpo["emissor_pub"]:
            return {"estado": "AUTORIDADE_INVALIDA"}
        if not corpo.get("emissor_pub"):
            return {"estado": "SEM_AUTORIDADE_DECLARADA"}
        if not selo_ok(corpo, selo):
            return {"estado": "SELO_INVALIDO"}
        real = _gateway_cura_reexecutar()
        igual = (corpo["casos"][0]["estado"] == real["estados"][0]
                 and corpo["casos"][1]["estado"] == real["estados"][1]
                 and corpo["casos"][2]["estado"] == real["estados"][2]
                 and corpo["casos"][3]["estados"] == real["estados"][3:5]
                 and corpo["casos"][1]["vetos"] == real["vetos_m002"])
        return {"estado": "REPRODUZIDO" if igual else "RESULTADO_DIFERENTE", "casos": real["estados"]}
    except (KeyError, TypeError, ValueError, IndexError):
        return {"estado": "PACOTE_MAL_FORMADO"}

def gateway_cura_verificar_ficheiro(caminho: str) -> Dict[str, Any]:
    try:
        with open(caminho, encoding="utf-8") as fh:
            return gateway_cura_verificar_objeto(json.load(fh))
    except (OSError, ValueError):
        return {"estado": "PACOTE_ILEGIVEL"}

def gateway_selo_verificar(msg_bytes: bytes, sig_hex: str, pub_hex: str) -> bool:
    """Verifica qualquer selo Ed25519 (RFC 8032) — a Pérola Melo dentro do motor."""
    try:
        return ed_verificar(bytes.fromhex(pub_hex), msg_bytes, bytes.fromhex(sig_hex))
    except ValueError:
        return False

# ============================== P14 — SELO HÍBRIDO PÓS-QUÂNTICO (v2.9.3) ==============================
# Camada PQ do selo da casa: Ed25519 (clássico) + Lamport (hash-based, pós-quântico) sobre os
# MESMOS bytes canónicos. Shor quebra Ed25519 num quântico grande; quebrar Lamport exige
# pré-imagem de SHA-256 — mesmo Grover fica em 2^128. Integridade dual: se uma matemática
# cair, a outra ainda segura. ML-DSA-65 (FIPS 204) fica [IMPLEMENTAR] — algoritmo declarado
# pela janela do enxame (SELO_HIBRIDO_PQ.json); o Lamport é a prova do mecanismo já a correr.
# Regra P5 aplicada: uma chave Lamport assina UMA vez e é queimada (reuso -> recusa).
_LAMPORT_USADOS: Dict[str, bool] = {}

def _lamport_par(semente: bytes, i: int) -> Tuple[bytes, bytes]:
    return (hashlib.sha256(semente + b"|x0|" + i.to_bytes(2, "big")).digest(),
            hashlib.sha256(semente + b"|x1|" + i.to_bytes(2, "big")).digest())

def lamport_gerar(etiqueta: str) -> Dict[str, Any]:
    """Chave Lamport determinística da semente declarada: 256 pares (x0,x1); pub = 256 pares de hashes."""
    semente = chave_demo("lamport/" + etiqueta)
    pares = [_lamport_par(semente, i) for i in range(256)]
    pub = [(hashlib.sha256(a).digest(), hashlib.sha256(b).digest()) for a, b in pares]
    return {"etiqueta": etiqueta, "priv": pares, "pub": pub}

def lamport_pub_sha256(pub: Sequence[Tuple[bytes, bytes]]) -> str:
    """Impressão digital da chave pública Lamport (viaja no selo; a pub completa sai do KPKG)."""
    return h256(b"".join(h for par in pub for h in par).encode("utf-8") if False else b"".join(a + b for a, b in pub))

def lamport_assinar(chave: Dict[str, Any], msg: bytes) -> bytes:
    """Assina o digest H(msg): 256 × 32 B = 8 KB. Uso ÚNICO (P5): reuso -> RuntimeError."""
    digest = hashlib.sha256(msg).digest()
    pid = hashlib.sha256(b"".join(a + b for a, b in chave["pub"])).hexdigest()
    if _LAMPORT_USADOS.get(pid):
        raise RuntimeError("LAMPORT_REUSO_RECUSADO: uma chave Lamport assina UMA vez (P5)")
    _LAMPORT_USADOS[pid] = True
    return b"".join(chave["priv"][i][(digest[i >> 3] >> (7 - (i & 7))) & 1] for i in range(256))

def lamport_verificar(pub: Sequence[Tuple[bytes, bytes]], msg: bytes, sig: bytes) -> bool:
    if len(sig) != 8192 or len(pub) != 256:
        return False
    digest = hashlib.sha256(msg).digest()
    for i in range(256):
        if hashlib.sha256(sig[i * 32:(i + 1) * 32]).digest() != pub[i][(digest[i >> 3] >> (7 - (i & 7))) & 1]:
            return False
    return True

def selar_hibrido(obj: Any, sk_ed: bytes, chave_lam: Dict[str, Any]) -> Dict[str, Any]:
    """P14 — selo híbrido: Ed25519 + Lamport sobre os mesmos bytes canónicos; pub Lamport via fingerprint."""
    m = canon(obj)
    sig_lam = lamport_assinar(chave_lam, m)
    return {"alg": "Ed25519+SHA-256+Lamport-PQ", "hash": h256(m), "pub": ed_publica(sk_ed).hex(),
            "sig": ed_assinar(sk_ed, m).hex(), "pub_lam_sha256": lamport_pub_sha256(chave_lam["pub"]),
            "sig_lam": sig_lam.hex()}

def selo_hibrido_ok(obj: Any, selo: Dict[str, Any], pub_lam: Sequence[Tuple[bytes, bytes]]) -> bool:
    """Verificação dual: selo clássico E Lamport têm de conferir; a pub Lamport tem de bater com a fingerprint."""
    try:
        m = canon(obj)
        base = {k: selo[k] for k in ("alg", "hash", "pub", "sig")}
        if not selo_ok(obj, base) or lamport_pub_sha256(pub_lam) != selo["pub_lam_sha256"]:
            return False
        return lamport_verificar(pub_lam, m, bytes.fromhex(selo["sig_lam"]))
    except (KeyError, TypeError, ValueError, AttributeError):
        return False

# ============================== P44 — FROST/1: ASSINATURA DE LIMIAR (v2.9.4) ==============================
# Espírito do RFC 9591 (FROST): t-de-n participantes assinam JUNTOS em 2 rondas e produzem UMA
# assinatura Ed25519 válida — sem nunca montar a chave secreta. O distribuidor existe SÓ no keygen
# (publica os compromissos C_j do polinómio e morre; NÃO guarda a). Ronda 1: compromissos de nonce
# D_i/E_i. Ronda 2: fator de ligação rho_i por participante (anti-Drijvers), R = Σ R_i, parciais
# s_i = r_i + c·λ_i·a_i verificados pelo agregador contra A_i = Σ C_j·i^j. Compatibilidade total:
# a assinatura de grupo verifica pelo ed_verificar padrão — é uma assinatura Ed25519 como outra qualquer.
# Conformidade wire-level ao RFC 9591 (encodings, transporte) fica [IMPLEMENTAR].
class Froste:
    """Assinatura de limiar: o médico local, o auditor e o sensor — nenhum operador sozinho aprova nada."""

    def __init__(self, limiar: int, participantes: int, etiqueta: str):
        if not (2 <= limiar <= participantes):
            raise ValueError("limiar tem de estar entre 2 e o número de participantes")
        self.limiar, self.n, self.etiqueta = limiar, participantes, etiqueta
        a = int.from_bytes(chave_demo("frost/grupo/" + etiqueta), "little") % _L  # usado só aqui; NUNCA guardado
        self.coef = [a] + [int.from_bytes(hashlib.sha256(("frost/coef/" + etiqueta + "/" + str(j)).encode("utf-8")).digest(), "little") % _L for j in range(1, limiar)]
        self.commit_c = [_ed_mult(c, _ED_G) for c in self.coef]  # PONTOS para aritmética (bug de representação corrigido: eram bytes comprimidos)
        self.A = _ed_comp(self.commit_c[0])                       # bytes para hashing e verificação padrão
        self.partilhas = {i: sum(c * pow(i, j, _L) for j, c in enumerate(self.coef)) % _L for i in range(1, participantes + 1)}

    def parte_verificacao(self, i: int):
        """Chave pública de verificação do participante i: A_i = Σ_j C_j · i^j (nunca o segredo)."""
        pt = None
        for j, C in enumerate(self.commit_c):
            termo = _ed_mult(pow(i, j, _L), C)
            pt = termo if pt is None else _ed_soma(pt, termo)
        return pt

    def _nonces(self, i: int, msg: bytes) -> Tuple[int, int]:
        tag = h256(msg)[:16]
        d = int.from_bytes(chave_demo(f"frost/nonce/{self.etiqueta}/{tag}/{i}/d"), "little") % _L
        e = int.from_bytes(chave_demo(f"frost/nonce/{self.etiqueta}/{tag}/{i}/e"), "little") % _L
        return d, e

    def _ligacao(self, S: Sequence[int], commits: Dict[int, Tuple[bytes, bytes]], msg: bytes) -> str:
        return h256(canon([[i, commits[i][0].hex(), commits[i][1].hex()] for i in S] + [self.A.hex()]))

    def _rho(self, i: int, D_i: bytes, E_i: bytes, msg: bytes, ligacao: str) -> int:
        return int.from_bytes(hashlib.sha256(bytes([i]) + D_i + E_i + self.A + msg + ligacao.encode("utf-8")).digest(), "little") % _L

    def _lagrange(self, i: int, S: Sequence[int]) -> int:
        lam = 1
        for j in S:
            if j != i:
                lam = lam * j % _L * pow(j - i, -1, _L) % _L
        return lam

    def assinar(self, participantes: Sequence[int], msg: bytes) -> Tuple[bytes, Dict[str, Any]]:
        """2 rondas FROST: compromissos de nonce -> parciais ligados -> UMA assinatura de grupo."""
        S = sorted(set(participantes))
        if len(S) < self.limiar:
            raise ValueError("quórum insuficiente para assinar")
        # Ronda 1 — compromissos de nonce (determinísticos do demo; produção: aleatoriedade real)
        commits = {}
        for i in S:
            d, e = self._nonces(i, msg)
            commits[i] = (d, e, _ed_comp(_ed_mult(d, _ED_G)), _ed_comp(_ed_mult(e, _ED_G)))
        ligacao = self._ligacao(S, {i: (c[2], c[3]) for i, c in commits.items()}, msg)
        # Ronda 2 — nonces ligados, agregação de R em PONTOS, parciais
        R = None
        r_map, R_map, s_total, parcial_ok = {}, {}, 0, True
        for i in S:
            d, e, D_i, E_i = commits[i]
            r_i = (d + self._rho(i, D_i, E_i, msg, ligacao) * e) % _L
            R_i = _ed_mult(r_i, _ED_G)
            r_map[i], R_map[i] = r_i, R_i
            R = R_i if R is None else _ed_soma(R, R_i)
        R_comp = _ed_comp(R)
        c = _ed_h(R_comp + self.A + msg)
        for i in S:
            lam = self._lagrange(i, S)
            s_i = (r_map[i] + c * lam * self.partilhas[i]) % _L
            s_total = (s_total + s_i) % _L
            if not _ed_igual(_ed_mult(s_i, _ED_G), _ed_soma(R_map[i], _ed_mult(c * lam % _L, self.parte_verificacao(i)))):
                parcial_ok = False
        return R_comp + s_total.to_bytes(32, "little"), {"rondas": 2, "ligacao_aplicada": True, "parciais": len(S), "parciais_verificados": parcial_ok}

    def fraude_solo(self, i: int, msg: bytes) -> bytes:
        """Canário de ataque: 1 participante tenta passar-se pelo grupo (a interpolação não fecha — vai FALHAR)."""
        d, e = self._nonces(i, msg)
        D_i, E_i = _ed_comp(_ed_mult(d, _ED_G)), _ed_comp(_ed_mult(e, _ED_G))
        ligacao = self._ligacao([i], {i: (D_i, E_i)}, msg)
        r = (d + self._rho(i, D_i, E_i, msg, ligacao) * e) % _L
        R_comp = _ed_comp(_ed_mult(r, _ED_G))
        c = _ed_h(R_comp + self.A + msg)
        s = (r + c * self.partilhas[i]) % _L
        return R_comp + s.to_bytes(32, "little")

# ============================== P45 — O INFINITO COMPUTÁVEL (v2.9.5) ==============================
# «Mete a calculadora a computar-se até chegar ao infinito.» Num espaço de estados FINITO, o
# infinito é o CICLO: iterar f(x) = sha256(x) até a cadeia morder a própria cauda (Ouroboros,
# algoritmo de Brent: tartaruga e lebre). E a paz do P8 tem VALORES PRÓPRIOS: o equilíbrio de
# Lotka-Volterra sem travão é um CENTRO (λ = ±i, órbitas fechadas — a paz é dança, não ponto
# morto); com travão logístico, espiral estável (traço < 0 — homeostase real). No estado completo
# de 256 bits, o ciclo é mais longo que o tempo do universo: o infinito, medido com honestidade.

def oroboro() -> Dict[str, Any]:
    """f(x) = sha256(x) com estado de 24 bits (os 3 primeiros bytes do digest). Brent encontra
    a cauda μ e o ciclo λ. Determinístico: duas corridas dão o mesmo ouroboros."""
    def f(x: int) -> int:
        return int.from_bytes(hashlib.sha256(x.to_bytes(32, "big")).digest()[:3], "big")
    poder, lam = 1, 1
    tartaruga, lebre = f(0), f(f(0))
    while tartaruga != lebre:
        if poder == lam:
            tartaruga = lebre
            poder *= 2
            lam = 0
        lebre = f(lebre)
        lam += 1
    ciclo = lam
    tartaruga = lebre = 0
    for _ in range(ciclo):
        lebre = f(lebre)
    mu = 0
    while tartaruga != lebre:
        tartaruga = f(tartaruga)
        lebre = f(lebre)
        mu += 1
    teoria = int((3.141592653589793 * (1 << 23)) ** 0.5)  # esperança √(πN/2) para mapa aleatório
    return {"bits": 24, "N": 1 << 24, "cauda_mu": mu, "ciclo_lambda": ciclo,
            "passos_total": mu + ciclo, "teoria_raiz": teoria}

def valores_proprios_da_paz(alfa: float = 1.0, beta: float = 1.0, gama: float = 1.0, delta: float = 1.0, travao: float = 0.0) -> Dict[str, Any]:
    """P8 — Lotka-Volterra no equilíbrio (G*, P*) = (γ/δ, α/β). Jacobiano 2×2; característica
    λ² − traço·λ + det = 0. Sem travão: traço 0 -> λ = ±i·ω, CENTRO (órbitas fechadas). Com
    travão logístico na presa (K = 1/travão), traço < 0 -> ESPIRAL ESTÁVEL (homeostase).
    Parâmetros de manual, ASSUMIDO [VALIDAR]; a estrutura é a do axioma P8."""
    Gs, Ps = gama / delta, alfa / beta
    K = 1.0 / travao if travao > 0 else float("inf")
    a11 = alfa * (1 - 2 * Gs / K if travao > 0 else 1.0) - beta * Ps if travao > 0 else 0.0
    a12, a21, a22 = -beta * Gs, delta * Ps, 0.0
    tr = a11 + a22
    det = a11 * a22 - a12 * a21
    disc = tr * tr - 4 * det
    if disc >= 0:
        raiz = disc ** 0.5
        l1, l2 = (tr + raiz) / 2, (tr - raiz) / 2
        especie, tipo = "reais", ("ESTAVEL" if tr < 0 and det > 0 else "INSTAVEL")
    else:
        re, im = tr / 2, (-disc) ** 0.5 / 2
        l1, l2 = complex(re, im), complex(re, -im)
        especie = "complexos"
        tipo = "CENTRO_ORBITAS_FECHADAS" if re == 0 else ("ESPIRAL_ESTAVEL" if re < 0 else "ESPIRAL_INSTAVEL")
    return {"Gs": Gs, "Ps": Ps, "traco": tr, "det": det, "l1": l1, "l2": l2, "especie": especie,
            "tipo": tipo, "assumido": "parâmetros de manual α=β=γ=δ=1 [VALIDAR]; estrutura do P8"}

def a_escada_do_infinito(taxa_hashes_s: float) -> Dict[str, Any]:
    """O estado completo de 256 bits: ciclo esperado de um mapa aleatório ≈ √(π·2^255) passos.
    À taxa medida, quantos anos? O infinito medido — ninguém fecha, e por isso os selos de
    hoje bastam: a cadeia não fecha sobre si mesma dentro do tempo do universo."""
    passos = (3.141592653589793 * (2 ** 256) / 2) ** 0.5  # ciclo esperado = √(πN/2) — fórmula corrigida (a v2.9.5 esqueceu a raiz)
    seg = passos / taxa_hashes_s
    anos = seg / 31_557_600
    return {"passos_esperados": passos, "segundos": seg, "anos": anos,
            "veredicto": "INFINITO_AO_ALCANCE_DE_NINGUEM" if anos > 1e24 else "AO_ALCANCE"}

# ============================== P46 — O ARQUIVO PARA SEMPRE (v2.9.7) ==============================
# O «para sempre» não é mística: tem três medições. (1) FÍSICA: o chão de Landauer (1961) —
# kT·ln2 por tentativa é a energia mínima da natureza para inverter um bit; contar até 2^256
# custa sois inteiros convertidos em energia. (2) INFORMAÇÃO: o Shamir 3-de-5 é INCONDICIONAL
# — com menos de 3 partes, H(X|Y) = H(X): provado por exaustão, não por promessa. (3) TEMPO:
# ARQUIVO/1 — cada era resela o conteúdo da era anterior com a chave da era nova, mantendo o
# selo antigo e a NOTA honesta da rotação: envelhecer algoritmos não apaga proveniência.
# Cantor dá a humildade: tudo no motor é FINITO e portanto contável (ℵ₀) — tudo é listável,
# tudo é auditável. O 𝔠 é do modelo idealizado, não da máquina.

def landauer_inversao(bits: int = 256, temperatura_k: float = 300.0) -> Dict[str, Any]:
    """Energia mínima (chão absoluto de Landauer) para BRUTE-FORÇAR bits de espaço à temperatura T,
    em joules e em sóis de massa convertida. O mais generoso possível ao atacante."""
    k_boltzmann = 1.380649e-23  # J/K [CODATA 2018]
    e_por_tentativa = k_boltzmann * temperatura_k * 0.6931471805599453
    energia_j = (2 ** bits) * e_por_tentativa
    massa_solar_kg, c_luz = 1.989e30, 2.99792458e8  # [VALIDAR]
    sois = energia_j / (massa_solar_kg * c_luz ** 2)
    return {"bits": bits, "temperatura_k": temperatura_k, "j_por_tentativa": e_por_tentativa,
            "energia_j": energia_j, "sois": sois,
            "assumido": "chão de Landauer POR TENTATIVA — o mais generoso ao atacante; CODATA/massa solar [VALIDAR]"}

def arquivo_resealar(conteudo: bytes, selo_anterior_ref: str, nota_rotacao: str, chave_nova: bytes) -> Dict[str, Any]:
    """ARQUIVO/1 — a era nova resela o conteúdo da era anterior. Sem nota honesta de rotação, não há re-selagem."""
    if not nota_rotacao.strip():
        raise ValueError("ARQUIVO/1: sem nota honesta de rotação não há re-selagem")
    corpo = {"tipo": "ARQUIVO/1", "conteudo_sha256": h256(conteudo), "selo_anterior_ref": selo_anterior_ref,
             "nota_rotacao": nota_rotacao, "humano_decide": True}
    return {"corpo": corpo, "selo": selar(corpo, chave_nova)}

def verificar_arquivo(arq: Dict[str, Any], conteudo: bytes, pub_nova: Optional[str] = None) -> bool:
    """Verifica o ARQUIVO/1: conteúdo intacto + nota presente + selo da era nova confere."""
    try:
        corpo = arq["corpo"]
        if corpo.get("tipo") != "ARQUIVO/1" or corpo.get("conteudo_sha256") != h256(conteudo):
            return False
        if not corpo.get("nota_rotacao", "").strip():
            return False
        return selo_ok(corpo, arq["selo"], {pub_nova} if pub_nova else None)
    except (KeyError, TypeError, ValueError, AttributeError):
        return False

def shamir_zero_informacao(segredo: int = 42, etiqueta: str = "p36") -> Dict[str, Any]:
    """P5 — segurança INCONDICIONAL por EXAUSTÃO: com 2 partes de um limiar 3, TODOS os 256
    segredos de um byte continuam possíveis (para cada s' existe polinómio de grau 2 pelos
    pontos) — H(X|Y) = H(X). A informação não diminui: é teoria da informação, não custo."""
    c1 = int.from_bytes(chave_demo("shamir/" + etiqueta + "/c1"), "little") % _L
    c2 = int.from_bytes(chave_demo("shamir/" + etiqueta + "/c2"), "little") % _L
    i1, i2 = 1, 2
    y1 = (segredo + c1 * i1 + c2 * i1 * i1) % _L
    y2 = (segredo + c1 * i2 + c2 * i2 * i2) % _L
    det = (i1 * i2 * i2 - i2 * i1 * i1) % _L
    possiveis = 0
    for s_cand in range(256):
        r1, r2 = (y1 - s_cand) % _L, (y2 - s_cand) % _L
        c1_c = (r1 * i2 * i2 - r2 * i1 * i1) * pow(det, -1, _L) % _L
        c2_c = (i1 * r2 - i2 * r1) * pow(det, -1, _L) % _L
        if (s_cand + c1_c * i1 + c2_c * i1 * i1) % _L == y1 and (s_cand + c1_c * i2 + c2_c * i2 * i2) % _L == y2:
            possiveis += 1
    return {"partes_dadas": 2, "limiar": 3, "candidatos_possiveis": possiveis, "total": 256,
            "conclusao": "H(X|Y)=H(X) — segurança INCONDICIONAL (teoria da informação)" if possiveis == 256 else "VIOLACAO"}

# ============================== P47 — SOBRE/1: O ENVELOPE BLINDADO (v2.9.8) ==============================
# O futuro offline SEM Starlink: o selo da casa tornado legível pelo MUNDO — COSE_Sign1
# (RFC 9052, alg -8 EdDSA) sobre CBOR canónico (RFC 8949, subconjunto) + recibo SCITT
# (espírito RFC 9943: prova de inclusão Merkle no registo, reutilizando a Merkle do M4).
# < 250 bytes: cabe num QR, numa SMS, num rádio, numa caneta USB — o transporte é INDIFERENTE
# (DTN store-and-forward): o pacote JÁ sai assinado, sem CA, sem servidor, sem estrela a pagar.
# A casa verifica pelos componentes; descodificador CBOR completo [IMPLEMENTAR] — o mundo lê
# o envelope com qualquer parser COSE.
import struct

def _cbor(t: Any) -> bytes:
    """Codificador CBOR canónico mínimo (RFC 8949, subconjunto: nulo, bool, int, float64, bytes, texto, listas, mapas)."""
    def cab(major: int, n: int) -> bytes:
        if n < 24: return bytes([(major << 5) | n])
        if n < 256: return bytes([(major << 5) | 24, n])
        if n < 65536: return bytes([(major << 5) | 25]) + n.to_bytes(2, "big")
        return bytes([(major << 5) | 26]) + n.to_bytes(4, "big")
    if t is None: return b"\xf6"
    if isinstance(t, bool): return b"\xf5" if t else b"\xf4"
    if isinstance(t, int): return cab(0, t) if t >= 0 else cab(1, -t - 1)
    if isinstance(t, float): return b"\xfb" + struct.pack(">d", t)  # float64 sempre — determinístico (subconjunto)
    if isinstance(t, (bytes, bytearray)):
        b = bytes(t)
        return cab(2, len(b)) + b
    if isinstance(t, str):
        b = t.encode("utf-8")
        return cab(3, len(b)) + b
    if isinstance(t, list):
        return cab(4, len(t)) + b"".join(_cbor(x) for x in t)
    if isinstance(t, dict):
        pares = sorted((_cbor(k), _cbor(v)) for k, v in t.items())  # canónico: chaves em ordem bytewise (§4.2.1)
        return cab(5, len(pares)) + b"".join(k + v for k, v in pares)
    raise TypeError(f"CBOR mínimo não codifica {type(t).__name__}")

def sobre_assinar(payload: Dict[str, Any], sk: bytes, kid: str = "lampada", recibo_scitt: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """P47 — COSE_Sign1: protegido {1: -8 (EdDSA), 3: application/konfirmu+json};
    Sig_structure = ["Signature1", protegido, b"", payload] (RFC 9052 §4.4). O recibo SCITT
    (prova de Merkle) viaja no cabeçalho DESPROTEGIDO. Devolve o envelope binário + as peças
    que a casa usa para verificar sem descodificar."""
    cab_prot = _cbor({1: -8, 3: "application/konfirmu+json"})
    payload_cbor = _cbor(payload)
    sig_estrutura = _cbor(["Signature1", cab_prot, b"", payload_cbor])
    sig = ed_assinar(sk, sig_estrutura)
    desprot: Dict[str, Any] = {"kid": kid}
    if recibo_scitt is not None:
        desprot["recibo_scitt"] = recibo_scitt
    envelope = _cbor([cab_prot, desprot, payload_cbor, sig])
    return {"envelope": envelope, "cab_prot": cab_prot, "payload_cbor": payload_cbor,
            "sig": sig, "kid": kid, "recibo_scitt": recibo_scitt}

def sobre_verificar(peca: Dict[str, Any], pk: bytes, payload_novo: Optional[bytes] = None) -> bool:
    """A casa verifica RE-CONSTITUINDO o Sig_structure: mesmos bytes, mesmo ed_verificar.
    payload_novo permite o canário: mesmo envelope, outro conteúdo -> tem de CAIR."""
    try:
        payload = peca["payload_cbor"] if payload_novo is None else payload_novo
        sig_estrutura = _cbor(["Signature1", peca["cab_prot"], b"", payload])
        return ed_verificar(pk, sig_estrutura, peca["sig"])
    except (KeyError, TypeError, ValueError):
        return False

def sobre_recibo_scitt(series: Sequence[str], i: int) -> Dict[str, Any]:
    """Recibo SCITT (espírito RFC 9943): prova de inclusão Merkle do recibo i no registo —
    reutiliza a Merkle do M4 (folhas e nós com prefixos separados). Qualquer inspetor verifica
    offline que o recibo nunca foi apagado nem alterado, com só o caminho de irmãos."""
    return {"indice": i, "raiz": merkle_raiz(series), "prova": merkle_prova(series, i)}

# ============================== P49 — MARE/1: ÁGUAS, MAR E PESCA (v2.9.9) ==============================
# As fórmulas que o mar não tem: o mundo DETETA crimes marítimos meses depois (satélites,
# auditorias, multas); a casa VETA ANTES de o crime completar — a válvula que não abre fora
# do envelope legal, o desembarque que não emite certificado acima da quota, o encontro de
# navios que marca o transbordo ANTES do peixe chegar ao porto. Registos SELADOS pelos
# sensores de bordo (mesma arquitetura do M3): mexer no registo depois de selado = bloqueio.
# Limiares com norma citada; o que não tem norma fica ASSUMIDO [VALIDAR].
MARE_MARPOL = {"dist_nm_min": 12.0, "ppm_max": 15.0, "kn_em_rota": 1.0,
               "fonte": "MARPOL Anexo I Reg. 15 (IMO): em rota + ≤ 15 ppm + ≥ 12 MN da costa, navios ≥ 400 GT; lido 21-11-2026",
               "assumido": "limiar de «em rota» (≥ 1 kn) ASSUMIDO [VALIDAR]; áreas especiais mais estritas [VALIDAR por zona]"}
MARE_STS = {"dist_m_max": 500.0, "kn_max": 2.0, "min_min": 30, "h_provavel": 12,
            "fonte": "Miller et al. 2018, Frontiers in Marine Science (Global Fishing Watch): < 500 m, ambos ≤ 2 kn, ≥ 30 min, fora de porto; > 12 h = provável; lido 21-11-2026"}
MARE_TAC = {"tac_kg_demo": 50_000.0,
            "fonte": "TAC REAL por espécie/ano publica-o o ICES/UE — valores aqui são DE DEMO ASSUMIDO [VALIDAR]"}

def mare_descarga(registo: Dict[str, Any], pub_sensor: str) -> Dict[str, Any]:
    """F-MARPOL/1 — a válvula de sentinas não abre fora do envelope Reg. 15. Registo selado pelo sensor."""
    d = registo.get("dados", {}) if isinstance(registo, dict) else {}
    lote = str(d.get("lote", ""))
    if d.get("sensor") != "hidrofone_descarga" or not selo_ok(d, registo.get("selo", {}), {pub_sensor}):
        return {"estado": "BLOQUEADA_REGISTO_SEM_SELO", "lote": lote}
    dist, vel, ppm = d.get("dist_nm"), d.get("vel_kn"), d.get("ppm")
    if not all(isinstance(x, (int, float)) for x in (dist, vel, ppm)):
        return {"estado": "BLOQUEADA_REGISTO_ILEGIVEL", "lote": lote}
    if dist < MARE_MARPOL["dist_nm_min"]:
        return {"estado": "BLOQUEADA_DISTANCIA", "dist_nm": dist, "minimo_nm": MARE_MARPOL["dist_nm_min"]}
    if ppm > MARE_MARPOL["ppm_max"]:
        return {"estado": "BLOQUEADA_PPM", "ppm": ppm, "maximo_ppm": MARE_MARPOL["ppm_max"]}
    if vel < MARE_MARPOL["kn_em_rota"]:
        return {"estado": "BLOQUEADA_NAO_EM_ROTA", "vel_kn": vel, "assumido": MARE_MARPOL["assumido"]}
    return {"estado": "LIBERADA", "dist_nm": dist, "ppm": ppm, "vel_kn": vel}

def mare_encontro(registo: Dict[str, Any], pub_sensor: str) -> Dict[str, Any]:
    """F-STS/1 — marca o transbordo ANTES do peixe chegar ao porto (critérios de Miller et al. 2018)."""
    d = registo.get("dados", {}) if isinstance(registo, dict) else {}
    if not selo_ok(d, registo.get("selo", {}), {pub_sensor}):
        return {"estado": "BLOQUEADA_REGISTO_SEM_SELO"}
    dist, k1, k2, minu = d.get("dist_m"), d.get("kn_1"), d.get("kn_2"), d.get("minutos")
    if not all(isinstance(x, (int, float)) for x in (dist, k1, k2, minu)):
        return {"estado": "BLOQUEADA_REGISTO_ILEGIVEL"}
    if d.get("porto"):
        return {"estado": "SEM_ENCONTRO_PORTO"}
    if dist > MARE_STS["dist_m_max"] or max(k1, k2) > MARE_STS["kn_max"] or minu < MARE_STS["min_min"]:
        return {"estado": "SEM_ENCONTRO"}
    estado = "TRANSBORDO_PROVAVEL" if minu >= MARE_STS["h_provavel"] * 60 else "TRANSBORDO_SUSPEITO"
    return {"estado": estado, "dist_m": dist, "minutos": minu,
            "reefer": bool(d.get("reefer")), "consequencia": "desembarque só com REVISAO_HUMANA e inspecção"}

def mare_desembarque(registo: Dict[str, Any], pub_balanca: str, tac_kg: float, acumulado_kg: float) -> Dict[str, Any]:
    """F-IUU/1 — a balança selada não emite certificado acima da quota; sem cadeia de captura
    (raiz Merkle dos eventos), não há certificado (espírito Reg. UE 1005/2008)."""
    d = registo.get("dados", {}) if isinstance(registo, dict) else {}
    lote = str(d.get("lote", ""))
    if not selo_ok(d, registo.get("selo", {}), {pub_balanca}):
        return {"estado": "BLOQUEADA_REGISTO_SEM_SELO", "lote": lote}
    kg = d.get("kg")
    if not isinstance(kg, (int, float)) or kg <= 0:
        return {"estado": "BLOQUEADA_REGISTO_ILEGIVEL", "lote": lote}
    if not d.get("cadeia_captura_raiz"):
        return {"estado": "RECUSADO_SEM_CADEIA_DE_CAPTURA", "lote": lote,
                "motivo": "sem a raiz Merkle dos eventos de captura não há certificado (IUU)"}
    acumulado = acumulado_kg + kg
    if acumulado > tac_kg:
        return {"estado": "VETO_TAC", "tac_kg": tac_kg, "acumulado_com_esta": acumulado,
                "assumido": MARE_TAC["fonte"]}
    return {"estado": "DESEMBARCADA", "kg": kg, "acumulado_com_esta": acumulado, "tac_kg": tac_kg}

# ============================== P50 — AUDIT/1: CERTIFICAÇÃO POR ERAS (v2.9.10) ==============================
# Vattenfall, NAM, químicos, nuclear: o certificador não perde tempo com FÍSICA — perde com
# CONFIANÇA (provar que os papéis são autênticos e não mudaram). O AUDIT/1 elimina essa camada:
# cada evidência NASCE selada pelo inspetor/sensor, a auditoria é uma raiz Merkle, o certificado
# sai por FROST (auditor + operador, ninguém sozinho) em envelope COSE para o regulador, e a
# re-certificação é INCREMENTAL: só re-inspeciona o que mudou de hash (padrão MONTAR da casa).
# A máquina verifica AUTENTICIDADE; o julgamento fica humano (Art. 8, P6).
AUDIT_SEVESO = {"inspecao_anos_superior": 1, "inspecao_anos_inferior": 3, "relatorio_seguranca_anos": 5,
                "fonte": "Diretiva Seveso III 2012/18/EU — Art. 20 (inspeções 1/3 anos) e Art. 10 (relatório de segurança 5/5 anos); lido 21-11-2026 EUR-Lex"}

def audit_avaliar_item(registo: Dict[str, Any], pub_inspetor: str, limiar: float, incerteza: float = 0.5) -> Dict[str, Any]:
    """Um item de auditoria (leitura selada do inspetor/sensor) avaliado contra o limiar da norma.
    No limite do erro não decide a máquina: REVISAO_HUMANA (a doutrina do M3, agora em auditoria)."""
    d = registo.get("dados", {}) if isinstance(registo, dict) else {}
    item = str(d.get("item", ""))
    if not selo_ok(d, registo.get("selo", {}), {pub_inspetor}):
        return {"item": item, "estado": "EVIDENCIA_SEM_SELO"}
    valor = d.get("valor")
    if not isinstance(valor, (int, float)):
        return {"item": item, "estado": "EVIDENCIA_ILEGIVEL"}
    if valor > limiar + incerteza:
        estado = "NAO_CONFORME"
    elif valor > limiar - incerteza:
        estado = "REVISAO_HUMANA"  # no limite do erro do sensor: decide o humano, nunca o motor
    else:
        estado = "CONFORME"
    return {"item": item, "estado": estado, "valor": valor, "limiar": limiar}

def audit_moc(itens_antigos: Dict[str, str], itens_novos: Dict[str, str]) -> Dict[str, Any]:
    """MOC — gestão de mudança INCREMENTAL: só re-inspeciona o que mudou de hash; o que ficou
    igual carrega a prova da era anterior (padrão MONTAR: base + âncoras, nada se apaga)."""
    mudancas = sorted(k for k in itens_novos if k in itens_antigos and itens_antigos[k] != itens_novos[k])
    novos = sorted(k for k in itens_novos if k not in itens_antigos)
    carregar = sorted(k for k in itens_novos if k in itens_antigos and itens_antigos[k] == itens_novos[k])
    return {"re_inspecionar": mudancas, "carregar_com_prova": carregar, "novos": novos,
            "raiz_audit_nova": merkle_raiz(list(itens_novos.values())),
            "taxa_reinspecao": round(len(mudancas + novos) / max(len(itens_novos), 1), 3),
            "doctrine": "a re-certificação cresce com a MUDANÇA, não com o tempo"}

def audit_certificado(raiz_audit: str, fro: "Froste", msg_extra: bytes = b"") -> Tuple[bytes, Dict[str, Any]]:
    """O certificado de auditoria sai por FROST: auditor-chefe + regulador assinam a raiz —
    ninguém sozinho certifica (P44). Sai em envelope COSE (P47) para o regulador."""
    msg = kc_msg = _cbor({"tipo": "certificado_auditoria", "raiz_audit": raiz_audit}) if False else None
    msg_f = _cbor({"tipo": "certificado_auditoria", "raiz_audit": raiz_audit}) + msg_extra
    sig, meta = fro.assinar({1, 2}, msg_f)
    return sig, meta

def _demo() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")  # type: ignore[attr-defined]  # a saída é sempre UTF-8
    D = _Demo()
    try:
        with open(__file__, "rb") as fh:
            proprio = h256(fh.read())
    except Exception:
        proprio = "(sem acesso ao próprio ficheiro)"

    K = chave_demo  # chaves do demo: saem da semente declarada e de etiquetas públicas, NÃO são segredo

    def PUB(nome: str) -> str:
        return ed_publica(K(nome)).hex()

    livro = LedgerImutavel(K("notario"))
    const = Constituicao([PUB(f"aldeia/conselho_{i}") for i in range(1, 8)], {"guardia_da_constituicao": PUB("guardia/guardia_da_constituicao")}, livro, 0)
    respostas: List[Dict[str, Any]] = []
    K95 = REGRAS["k95_unilateral"]
    D.p(f"KONFIRMU CALC v{VERSAO} — python3 konfirmu_calc.py --demo")
    D.p(f"ficheiro sha256 {proprio}")
    D.p(f"regras   sha256 {HASH_REGRAS} · constituição versão 0: {const.atual()['hash'][:16]}…")
    D.p(f"cofre    sha256 {hash_cofre()} · {len(cofre())} fichas")
    D.p(f"semente  SEED = {SEED} · data lógica {DATA_LOGICA} (declarada; o motor não lê o relógio)")

    # ========================= D1 SOLAR MAPUTO =========================
    D.p("")
    D.p("D1 SOLAR — simulação de microrrede de 5 kWh/dia; cenário sintético, não dimensionamento validado")
    fontes = {n: {"pub": PUB("fonte/" + n), "operador": op} for n, op in (
        ("estacao_meteo", "meteorologia"), ("satelite", "agencia_espacial"), ("escola_vizinha", "escola_vizinha"),
        ("contador_selado", "aferidor_metrologia"), ("inspetora", "inspecao_distrital"),
        ("empreiteiro", "cooperativa_sol"), ("aferidora_precos", "aferidora_precos"))}

    def leitura(fonte: str, valor: float, unidade: str, ref: str, dia: int = 0) -> Dict[str, Any]:
        d = {"fonte": fonte, "valor": valor, "unidade": unidade, "ref": ref, "dia": dia}
        return {"dados": d, "selo": selar(d, K("fonte/" + fonte))}

    om = oraculo_gravado("irradiacao/maputo", K("leitor"))
    reg_sol = ORACULOS_GRAVADOS["irradiacao/maputo"]
    D.v(om["estado"] == "INSUFICIENTE" and om["lidas"] == 1 and om["conservadora"] is None,
        "P12 com 1 só fonte lida: INSUFICIENTE e conservadora=None; nenhuma leitura validada para dimensionar")
    # Constantes de ensaio explícitas: preservam a simulação histórica, sem usar a fonte insuficiente.
    sol_maputo = G(17.96, 0.90, reg_sol["unidade"], fonte="cenario_solar_sintetico")
    D.p(f"  CENÁRIO SINTÉTICO de demonstração: {sol_maputo.txt('MJ/m2/dia')}; "
        "valores assumidos para ensaiar as contas; não são saída validada do oráculo nem medição certificada")
    sol = [leitura("estacao_meteo", 5.1, "h/dia", "D1"), leitura("satelite", 4.9, "h/dia", "D1"),
           leitura("escola_vizinha", 5.0, "h/dia", "D1")]
    o1 = oraculo(sol, fontes, "h/dia", "D1")
    D.v(o1["estado"] == "CONSENSO" and o1["confianca"] == 1.0,
        f"P12 o mecanismo com 3 leituras seladas de DEMO (5,1 · 4,9 · 5,0 h/dia; não são medições) -> {_n(o1['valor'])} ± {_n(o1['incerteza'])} h/dia, confiança {_n(o1['confianca'] * 100, 0)}%")
    alvo = G(5.0, 0.0, "kWh/dia/microrrede", fonte="alvo")
    area = G(1.95, 0.02, "m2/painel", fonte="area")
    pr = G(0.75, 0.05, "1", fonte="pr")
    hsp = sol_maputo / G_STC  # MJ/m2/dia a dividir por 1000 W/m2 = horas de sol de pico por dia: a conversão é do motor de unidades
    REND, U_REND, RHO = 22.0, 1.5, 0.25  # rendimento 22% ± 1,5 pontos [VALIDAR: li «± 1,5%» como pontos percentuais]; rho = 0,25 é o da ordem

    def energia(n: int, rho: float) -> Grandeza:
        etas = lote(REND, U_REND, "%", "lote_A", rho, n)
        media = etas[0]
        for x in etas[1:]:
            media = media + x
        return F2(G(float(n), 0.0, "painel/microrrede", fonte="n"), area, media / float(n), pr, hsp)

    um = area * G_STC * lote(REND, U_REND, "%", "lote_A", RHO, 1)[0] * pr * hsp  # W por painel
    n_cont = alvo / um
    n_ok = next(n for n in range(1, 200) if energia(n, RHO).v - K95 * energia(n, RHO).u >= alvo.v)
    e_ok = energia(n_ok, RHO)
    ev, eu = e_ok.em("kWh/dia/microrrede")
    nv, nu = n_cont.em("painel/microrrede")
    D.p(f"  1 painel (1,95 m2; rendimento 22% ± 1,5; perdas PR 0,75 ± 0,05) dá {(um * G(1.0, 0.0, 'painel', fonte='um')).txt('kWh/dia')}")
    D.p(f"  SIMULAÇÃO: intervalo calculado com k=2: {_n(nv)} ± {_n(2 * nu)} painéis (k=2) -> cenário com {n_ok}: dão {_n(ev)} ± {_n(eu)} kWh/dia; limite inferior do modelo = {_n(ev - K95 * eu)}")
    D.p("  correlação do lote em " + str(n_ok) + " painéis: " + " · ".join(
        f"rho {_n(r, 2)} -> ± {_n(energia(n_ok, r).em('kWh/dia/microrrede')[1])}" for r in (0.0, RHO, 1.0)) + " kWh/dia")
    lc = ORACULOS_GRAVADOS["cambio/USD_por_EUR"]["leituras"][0]
    oc = oraculo_gravado("cambio/USD_por_EUR", K("leitor"), DATA_LOGICA, validade_dias=5)
    taxa = G(lc["valor"], lc["incerteza"], "USD/EUR", fonte="cambio")
    custo_usd = G(float(n_ok), 0.0, "painel") * area * G_STC * G(REND, 0.0, "%") * G(0.25, 0.05, "USD/W", fonte="preco")  # 0,25 ± 0,05 USD por watt: ASSUMIDO [VALIDAR]
    custo_eur = custo_usd / taxa
    idade_taxa = oc["desatualizadas"][0][1] if oc["desatualizadas"] else 0
    D.v(oc["estado"] == "INSUFICIENTE" and idade_taxa == 331 and _erro(lambda: custo_usd + G(100.0, 0.0, "EUR"), TypeError),
        f"P12 câmbio real gravado: BCE {_n(lc['valor'], 4)} USD por EUR, de {lc['data']}; na data lógica tem {idade_taxa} dias -> fora do prazo para pagar, fica só para CENÁRIO: "
        f"{n_ok} painéis ≈ {custo_usd.txt('USD', 0)} = {custo_eur.txt('EUR', 0)} [ASSUMIDO: 0,25 ± 0,05 USD por watt]; somar USD com EUR sem taxa -> TypeError")
    pacote_c1 = {"uso": "simulacao_solar_D1", "alvo_kwh_dia": 5.0, "area_m2": 1.95, "u_area_m2": 0.02, "rendimento_pct": REND, "u_rendimento_pct": U_REND,
                 "rho_lote": RHO, "pr": 0.75, "u_pr": 0.05, "irradiacao_mj_m2_dia": sol_maputo.em("MJ/m2/dia")[0], "u_irradiacao": sol_maputo.em("MJ/m2/dia")[1], "origem": "CENARIO_SINTETICO_D1"}
    livro.registar(0, "DIMENSIONAMENTO", {"entrada": hobj(pacote_c1), "paineis": n_ok})
    respostas.append({"estado": "SIMULADO", "paineis": n_ok,
                      "linhagem": {"hash_input": hobj(pacote_c1), "hash_formula": hobj(FORMULAS["F2"]), "hash_estado_ledger": livro.cabeca()},
                      "ledger": {"blocos": len(livro.blocos), "integra": livro.verificar_integridade_cadeia()}})
    etas5 = lote(REND, U_REND, "%", "teste", RHO, 5)
    soma5 = etas5[0] + etas5[1] + etas5[2] + etas5[3] + etas5[4]
    esperado = U_REND * 0.01 * math.sqrt(5 * (1 + 4 * RHO))
    D.v(abs(soma5.u - esperado) < 1e-12, "P1 soma de 5 peças do lote: u = u1·raiz(n·(1+(n−1)·rho)) = " + _n(esperado * 100, 3) + " pontos")
    quatro = [GrandezaFisica(REND, U_REND, "%", rho=RHO, etiqueta="ASSUMIDO", fonte="lote_clinica") for _ in range(4)]
    media4 = (quatro[0] + quatro[1] + quatro[2] + quatro[3]) / 4.0
    u_c = (U_REND * 0.01 / math.sqrt(4)) * math.sqrt(1 + (4 - 1) * RHO)
    D.v(abs(media4.u - u_c) < 1e-15 and quatro[0].etiqueta == "ASSUMIDO" and quatro[0].fonte == "lote_clinica",
        "P1 GrandezaFisica(22, 1.5, '%', rho=0.25): na média de N=4 o motor dá u_c = (u/raiz(N))·raiz(1+(N−1)·rho) = " + _n(u_c * 100, 3) + " pontos")
    D.v((um - um).v == 0.0 and (um - um).u == 0.0, "P1 x − x = 0 ± 0 (o mesmo erro não se conta duas vezes)")
    msg = _erro(lambda: G(100.0, 5.0, "W") + G(20.0, 1.0, "EUR"), TypeError)
    D.v(msg, "P1 watts + euros -> TypeError: " + msg)
    msg = _erro(lambda: F2(G(4.0, 0.0, "painel/microrrede"), G(1.95, 0.02, "EUR"), G(REND, U_REND, "%"), pr, hsp), TypeError)
    D.v(msg, "P7 input com unidade errada -> TypeError: " + msg)
    msg = _erro(lambda: F2(G(4.0, 0.0, "painel/microrrede"), area, G(45.0, 1.0, "%"), pr, hsp), ValueError)
    D.v(msg and issubclass(VetoFisico, ValueError), "P2 rendimento 45% sem prova -> ValueError (veto): " + msg)
    msg = _erro(lambda: veto_fisico(G(45.0, 1.0, "%"), "silicio_juncao_unica", True), ValueError)
    D.v(msg.endswith("não chega"), "P2 só a flag prova_laboratorial=True, sem selo de laboratório -> vetado na mesma (uma flag qualquer um a liga)")
    labs = {"laboratorio_solar": PUB("lab/laboratorio_solar")}
    dados_lab = {"amostra": "celula-3J-001", "rendimento_medido": 0.46, "norma": "medição em laboratório acreditado [VALIDAR]"}
    prova = {"laboratorio": "laboratorio_solar", "dados": dados_lab, "selo": selar(dados_lab, K("lab/laboratorio_solar"))}
    D.v(veto_fisico(G(45.0, 1.0, "%"), "silicio_juncao_unica", prova, labs) == "ACIMA_DO_TETO_COM_PROVA_LABORATORIAL",
        "P2 os mesmos 45% com prova laboratorial selada -> aceite")
    msg = _erro(lambda: veto_fisico(G(95.0, 1.0, "%"), "silicio_juncao_unica", prova, labs), ValueError)
    D.v(msg, "P2 95% nem com prova: " + msg)
    D.v(veto_fisico(G(40.0, 1.0, "%"), "perovskite_tandem") == "DENTRO_DO_TETO"
        and _erro(lambda: veto_fisico(G(40.0, 1.0, "%"), "silicio_juncao_unica"), ValueError)
        and _erro(lambda: veto_fisico(G(20.0, 1.0, "%"), "tecnologia_inventada"), ValueError),
        "P2 registo de tetos v" + TETOS_VERSAO + ": 40% passa em perovskite_tandem (43,0%) e é vetado em silicio_juncao_unica (33,7%); tecnologia fora do registo é recusada")
    v1 = (bytes.fromhex("9d61b19deffd5a60ba844af492ec2cc44449c5697b326919703bac031cae7f60"), b"",
          "d75a980182b10ab7d54bfed3c964073a0ee172f3daa62325af021a68f707511a",
          "e5564300c360ac729086e2cc806e828a84877f1eb8e5d974d873e065224901555fb8821590a33bacc61e39701cf9b46bd25bf5f0595bbe24655141438e7a100b")
    v2 = (bytes.fromhex("4ccd089b28ff96da9db6c346ec114e0f5b8a319f35aba624da8cf6ed4fb8a6fb"), b"\x72",
          "3d4017c3e843895a92b70aa74d1b7ebc9c982ccf2ec4968cc0cd55f12af4660c",
          "92a009a9f0d4cab8720e820b5f642540a2b27b5416503f8fb3762223ebdb69da085ac1e43e15996e458f3613d0f11d8c387b2eaeb4302aeeb00d291612bb0c00")
    D.v(all(ed_publica(sk).hex() == pk and ed_assinar(sk, m).hex() == sig and ed_verificar(bytes.fromhex(pk), m, bytes.fromhex(sig))
            for sk, m, pk, sig in (v1, v2)), "P3 Ed25519 puro = vetores de teste 1 e 2 do RFC 8032 (chave pública, assinatura e verificação)")
    selo_c1 = selar(pacote_c1, K("projetista"))
    D.v(selo_ok(pacote_c1, selo_c1), "P3 selo do pacote de inputs confere · sha256 " + selo_c1["hash"][:16] + "…")
    adulterado = bytearray(canon(pacote_c1))
    i = bytes(adulterado).index(b'"rendimento_pct":22') + len(b'"rendimento_pct":2')
    adulterado[i] = ord("3")  # 22 -> 23: um byte
    D.v(not selo_ok(bytes(adulterado), selo_c1), "P3 1 byte adulterado no input (22 -> 23) -> o selo cai")
    sig_torta = dict(selo_c1, sig=selo_c1["sig"][:-1] + ("0" if selo_c1["sig"][-1] != "0" else "1"))
    D.v(not selo_ok(pacote_c1, sig_torta), "P3 assinatura mexida num dígito -> o selo cai")
    o2 = oraculo(sol[:2] + [leitura("escola_vizinha", 7.9, "h/dia", "D1")], fontes, "h/dia", "D1")
    D.v(o2["discrepantes"] == ["escola_vizinha"] and o2["confianca"] < REGRAS["confianca_min"],
        f"P12 1 fonte adulterada na origem (7,9) apanhada por discrepância -> confiança {_n(o2['confianca'] * 100, 0)}% < 85%: proibido punir com esta leitura")
    mexida = {"dados": dict(sol[2]["dados"], valor=7.9), "selo": sol[2]["selo"]}
    o3 = oraculo(sol[:2] + [mexida], fontes, "h/dia", "D1")
    D.v(o3["estado"] == "INSUFICIENTE" and o3["rejeitadas"] == [["escola_vizinha", "SELO_INVALIDO"]],
        "P12 leitura mexida depois de selada -> SELO_INVALIDO, ficam 2 fontes -> INSUFICIENTE")
    o4 = oraculo(sol[:2] + [leitura("empreiteiro", 5.0, "h/dia", "D1")], fontes, "h/dia", "D1", excluir_operador="cooperativa_sol")
    D.v(o4["estado"] == "INSUFICIENTE" and o4["rejeitadas"] == [["empreiteiro", "AUTORRELATO"]],
        "P12 quem recebe o dinheiro não conta como fonte -> AUTORRELATO, INSUFICIENTE")

    # ====================== D2 ESCROW LIBERTADA / CONGELADA ======================
    D.p("")
    D.p("D2 ESCROW LIBERTADA / CONGELADA — cofre de 1 000 000,00 EUR, obras de 40 000,00 EUR (mínimo contratado: 5 kWh/dia)")
    raizes = {f"conselho_{i}": PUB(f"aldeia/conselho_{i}") for i in range(1, 8)}
    aldeia = Aldeia(raizes)

    def atestar(quem: str, pseud: str) -> Dict[str, Any]:
        return {"por": quem, "selo": selar({"atesto": pseud, "pub": PUB("aldeia/" + pseud)}, K("aldeia/" + quem))}

    plano_fano = [(1, 2, 3), (1, 4, 5), (1, 6, 7), (2, 4, 6), (2, 5, 7), (3, 4, 7), (3, 5, 6)]  # 2 vizinhas partilham no máximo 1 atestador
    admitidas = [aldeia.admitir(f"vizinha_{i}", PUB(f"aldeia/vizinha_{i}"), [atestar(f"conselho_{j}", f"vizinha_{i}") for j in trio])[0]
                 for i, trio in enumerate(plano_fano, 1)]

    def voto(quem: str, obra: str, conforme: bool, dia: int) -> Dict[str, Any]:
        d = {"quem": quem, "obra": obra, "conforme": conforme, "foto": h256(f"foto/{obra}/{quem}".encode()), "dia": dia}
        return {"dados": d, "selo": selar(d, K("aldeia/" + quem))}

    nomes = list(CAMARAS)  # v2.4: a irmandade — as 3 câmaras africanas estão no 3-de-5 desde o primeiro escrow
    custodios = {n: PUB("custodio/" + n) for n in nomes}
    sk_cofre = K("cofre/origem")
    pub_cofre = ed_publica(sk_cofre).hex()
    partes = dict(zip(nomes, shamir_partir(int.from_bytes(sk_cofre, "big"), 3, 5, K("shamir/semente-declarada"))))
    juizes = {"juiza_distrital": PUB("juiz/juiza_distrital")}
    valvula = Valvula({"medica_chefe": PUB("vital/medica_chefe")})
    motor = Motor(100_000_000, pub_cofre, custodios, fontes, aldeia, juizes, valvula, K("motor"), livro)
    motor.constituicao = const  # P21: daqui em diante o motor só trabalha com as regras ratificadas
    HIST = [39.5, 40.0, 40.3, 39.9, 40.1]

    def preco(custo: float, propostas: List[float]) -> Dict[str, Any]:
        d = {"fonte": "aferidora_precos", "precos": HIST}
        return {"custo": custo, "propostas": propostas, "historico": {"dados": d, "selo": selar(d, K("fonte/aferidora_precos"))}}

    def assinar(quem: Sequence[str], eid: str, sid: str) -> Dict[str, Dict[str, Any]]:
        return {n: {"selo": selar({"sessao": sid, "pedido": motor.hash_pedido(eid)}, K("custodio/" + n)), "parte": list(partes[n])}
                for n in quem}

    def medido(eid: str, valores: Sequence[float], dia: int) -> List[Dict[str, Any]]:
        return [leitura(f, x, "kWh/dia", eid, dia) for f, x in zip(("contador_selado", "satelite", "inspetora"), valores)]

    def julgamento(eid: str, decisao: str, dia: int, fp: bool = False) -> Dict[str, Any]:
        return selar({"escrow": eid, "decisao": decisao, "falso_positivo": fp, "dia": dia}, K("juiz/juiza_distrital"))

    conformes = [f"vizinha_{i}" for i in range(1, 6)]
    D.v(all(admitidas) and len(aldeia.membros) == 14, "P9 aldeia: 7 do conselho + 7 vizinhas admitidas, cada uma com 3 atestados assinados")

    # --- E1: com lastro + 3-de-5 + k>=5 conformes
    motor.criar_escrow("E1", "cooperativa_sol", 4_000_000, 0, 5.0, "kWh/dia")
    s1 = motor.abrir_sessao("E1", 0)
    args1 = dict(leituras=medido("E1", (7.1, 6.9, 7.0), 0), preco=preco(40.2, [39.8, 40.2, 41.0]),
                 votos=[voto(q, "E1", True, 0) for q in conformes], assinaturas=assinar(nomes[:3], "E1", s1))
    r1 = motor.liquidar("E1", s1, 0, **args1)
    d1 = motor.escrows["E1"]["dossie"]
    D.p(f"  E1 com lastro (7,1 · 6,9 · 7,0 kWh/dia), preço 40,2 na banda, 5 conformes, 3 de 5 custódios -> {r1['estado']} · dossiê {r1.get('dossie', '')[:16]}…")
    D.v(r1["estado"] == "LIBERTADA" and motor.pago.get("cooperativa_sol") == 4_000_000, "D2 E1 LIBERTADA: 40 000,00 EUR pagos à cooperativa")
    D.v(d1["selo"]["pub"] == pub_cofre and selo_ok(d1["dados"], d1["selo"], {pub_cofre}),
        "P5 o dossiê está selado com a chave do cofre, reconstruída de 3 partes de Shamir")
    seg = int.from_bytes(sk_cofre, "big")
    todas = list(partes.values())
    D.v(all(shamir_juntar(list(t)) == seg for t in itertools.combinations(todas, 3)) and
        all(shamir_juntar(list(t)) != seg for t in itertools.combinations(todas, 2)),
        "P5 Shamir 3-de-5 sobre 2^521−1: os 10 trios reconstroem a chave; nenhum dos 10 pares a reconstrói")
    seg127 = int.from_bytes(K("segredo-curto")[:15], "big")  # 120 bits: cabe em 2^127 − 1
    p127 = shamir_partir(seg127, 3, 5, K("shamir/semente-127"), PRIMO_DA_ORDEM)
    D.v(all(shamir_juntar(list(t), PRIMO_DA_ORDEM) == seg127 for t in itertools.combinations(p127, 3))
        and all(shamir_juntar(list(t), PRIMO_DA_ORDEM) != seg127 for t in itertools.combinations(p127, 2)),
        "P5 o mesmo código sobre 2^127−1 (o primo da ordem): 3 partes reconstroem, 2 não; a chave do cofre tem 256 bits, por isso usa 2^521−1")
    r1b = motor.liquidar("E1", s1, 0, **args1)
    D.v(r1b["estado"] == "RECUSADO_SESSAO_JA_USADA", "P5 reuso da mesma sessão -> " + r1b["estado"])
    b = banda_preco(HIST)
    D.v(b is not None and not sinal_de_cartel([39.8, 40.2, 41.0], b)["sinal"] and not sinal_de_cartel([39.9, 40.0, 40.1], b)["sinal"],
        f"B2 banda {_n(b['piso'])}–{_n(b['teto'])} (mediana {_n(b['mediana'])}): propostas ao preço de mercado não são cartel")

    # --- E2: a mesma, sem lastro -> congela -> 15 dias sem humano -> estorno
    motor.criar_escrow("E2", "cooperativa_sol", 4_000_000, 1, 5.0, "kWh/dia")
    s2 = motor.abrir_sessao("E2", 1)
    r2 = motor.liquidar("E2", s2, 1, leituras=medido("E2", (0.3, 0.4, 0.35), 1), preco=preco(40.2, [39.8, 40.2, 41.0]),
                        votos=[voto(q, "E2", True, 1) for q in conformes], assinaturas=assinar(nomes, "E2", s2))
    D.p(f"  E2 a mesma sem lastro (0,3 · 0,4 · 0,35 kWh/dia), até com 5 assinaturas e 5 conformes -> {r2['estado']} ({', '.join(r2.get('motivos', []))}) até ao dia {r2.get('prazo_dia')}")
    D.v(r2["estado"] == "CONGELADO_15D" and r2["motivos"] == ["SEM_LASTRO_FISICO"] and motor.escrows["E2"]["estado"] == "CONGELADO_15D",
        "D2 E2 CONGELADA (CONGELADO_15D): sem lastro não sai dinheiro, nem com todas as assinaturas")
    d2 = motor.escrows["E2"]["dossie"]
    D.v(selo_ok(d2["dados"], d2["selo"], {PUB("motor")}), "P6 dossiê do congelamento selado pelo motor · " + d2["selo"]["hash"][:16] + "…")
    reserva_antes = motor.reserva
    D.v(motor.avancar(15) == [] and motor.escrows["E2"]["estado"] == "CONGELADO_15D", "P6 dia 15 (14 dias passados): continua congelado")
    exp = motor.avancar(16)
    D.v(len(exp) == 1 and exp[0]["estado"] == "EXPIRACAO_ESTORNO_ORIGEM" and motor.reserva == reserva_antes + 4_000_000
        and "E2" not in motor.custodia, "P6 dia 16 sem humano -> EXPIRACAO_ESTORNO_ORIGEM: 40 000,00 EUR de volta ao cofre de origem, com registo")
    rj = motor.julgar("E2", "CORRIGIDO", "juiza_distrital", julgamento("E2", "CORRIGIDO", 17), 17)
    D.v(rj["estado"] == "RECUSADO_ESTADO_EXPIRACAO_ESTORNO_ORIGEM" and _erro(lambda: motor._mudar(motor.escrows["E1"], "CONGELADO_15D"), RuntimeError),
        "P6 fora da tabela nada acontece: julgar depois de expirar é recusado; LIBERTADO -> CONGELADO_15D é proibido")

    # --- E3: cartel -> congela -> tribunal
    motor.criar_escrow("E3", "cooperativa_sol", 4_000_000, 17, 5.0, "kWh/dia")
    s3 = motor.abrir_sessao("E3", 17)
    r3 = motor.liquidar("E3", s3, 17 + motor.nivel()[2], leituras=medido("E3", (7.1, 6.9, 7.0), 17),
                        preco=preco(41.1, [41.0, 41.1, 41.15, 41.19]), votos=[voto(q, "E3", True, 17) for q in conformes],
                        assinaturas=assinar(nomes, "E3", s3))
    D.v(r3["estado"] == "CONGELADO_15D" and r3["motivos"] == ["CARTEL_NO_TETO"],
        "B2 4 propostas coladas ao teto (41,0 · 41,1 · 41,15 · 41,19) -> CONGELADO_15D por CARTEL_NO_TETO")
    r3t = motor.julgar("E3", "TRIBUNAL", "juiza_distrital", julgamento("E3", "TRIBUNAL", 19), 19)
    D.v(r3t["estado"] == "TRIBUNAL" and "E3" not in motor.custodia,
        "P6 a juíza assina TRIBUNAL -> dossiê selado segue; o dinheiro espera no cofre de origem")

    # --- E4: 5 acusações que afinal estavam erradas -> falso positivo -> o fundo indemniza
    motor.criar_escrow("E4", "cooperativa_sol", 4_000_000, 20, 5.0, "kWh/dia")
    s4 = motor.abrir_sessao("E4", 20)
    r4 = motor.liquidar("E4", s4, 20 + motor.nivel()[2], leituras=medido("E4", (7.1, 6.9, 7.0), 20), preco=preco(40.2, [39.8, 40.2, 41.0]),
                        votos=[voto(f"vizinha_{i}", "E4", False, 20) for i in range(3, 8)], assinaturas=assinar(nomes, "E4", s4))
    dia4 = 20 + 1  # o pedido esperou 1 dia de quarentena (nível ALERTA)
    D.v(r4["estado"] == "CONGELADO_15D" and r4["motivos"] == ["ALERTA_CIDADAO_K5"], "P9 5 vizinhas acusam -> CONGELADO_15D por ALERTA_CIDADAO_K5")
    r4x = motor.julgar("E4", "TRIBUNAL", "juiza_falsa", selar({"escrow": "E4", "decisao": "TRIBUNAL", "falso_positivo": False, "dia": dia4 + 1},
                                                              K("juiz/juiza_falsa")), dia4 + 1)
    D.v(r4x["estado"] == "RECUSADO_ASSINATURA_DO_JUIZ" and motor.escrows["E4"]["estado"] == "CONGELADO_15D",
        "P6 decisão assinada por quem não é juiz registado -> " + r4x["estado"])
    nivel_antes = motor.nivel()[0]
    fundo_antes = motor.fundo
    r4j = motor.julgar("E4", "CORRIGIDO", "juiza_distrital", julgamento("E4", "CORRIGIDO", dia4 + 6, True), dia4 + 6, falso_positivo=True)
    D.p(f"  E4 falso positivo julgado ao fim de {r4j.get('dias_parado')} dias -> indemnização {_eur(r4j.get('indemnizacao_centimos', 0))} do fundo de 2% ({_eur(fundo_antes)} -> {_eur(motor.fundo)})")
    D.v(r4j["estado"] == "CORRIGIDO" and r4j["indemnizacao_centimos"] == 4_000_000 * 6 // 1000 and motor.fundo == fundo_antes - 24_000
        and r4j["em_divida_centimos"] == 0, "B3 falso positivo provado -> o fundo de 2% paga 0,1% por dia parado ao trabalhador")
    D.v(nivel_antes == "DEFESA" and motor.nivel()[0] == "ALERTA",
        f"P8 homeostase: 3 congelamentos levaram a anomalia a DEFESA; desfeito o falso positivo volta a ALERTA ({motor.anomalia}‰)")
    dia = dia4 + 6
    s4b = motor.abrir_sessao("E4", dia)
    limpos = [voto(q, "E4", True, dia) for q in conformes]
    r4a = motor.liquidar("E4", s4b, dia, leituras=medido("E4", (7.1, 6.9, 7.0), dia), votos=limpos, assinaturas=assinar(nomes[:4], "E4", s4b))
    D.v(r4a["estado"] == "EM_QUARENTENA", f"P8 em ALERTA a liquidação espera 1 dia -> {r4a['estado']} até ao dia {r4a.get('ate_ao_dia')}")
    r4b = motor.liquidar("E4", s4b, dia + 1, leituras=medido("E4", (7.1, 6.9, 7.0), dia), votos=limpos, assinaturas=assinar(nomes[:3], "E4", s4b))
    D.v(r4b["estado"] == "BLOQUEADO_ASSINATURAS_INSUFICIENTES" and r4b["exigidas"] == 4,
        "P8 em ALERTA 3 assinaturas já não chegam -> " + r4b["estado"] + " (exige 4 de 5)")
    s4c = motor.abrir_sessao("E4", dia + 1)
    r4c = motor.liquidar("E4", s4c, dia + 2, leituras=medido("E4", (7.1, 6.9, 7.0), dia), votos=limpos, assinaturas=assinar(nomes[:4], "E4", s4c))
    D.v(r4c["estado"] == "LIBERTADA" and motor.nivel()[0] == "FLUIDO",
        f"P8 com 4 de 5 e a espera cumprida -> LIBERTADA; o lastro cura: anomalia {motor.anomalia}‰, nível FLUIDO")
    rg = motor.criar_escrow("E_GRANDE", "cooperativa_sol", 200_000_000, dia + 2, 5.0, "kWh/dia")
    D.v(rg["estado"] == "BLOQUEADO_RESERVA_INSUFICIENTE" and motor.reserva >= 0, "P8 pedido maior do que a reserva -> " + rg["estado"])

    # --- B3: válvula vital
    dia += 3
    resultados = []
    for eid, dominio in (("E5", "SAUDE"), ("E6", "ALIMENTACAO"), ("E7", "AGUA")):
        motor.criar_escrow(eid, "centro_de_saude", 1_000_000, dia, 5.0, "kWh/dia", dominio=dominio)
        sv = motor.abrir_sessao(eid, dia)
        em = {"quem": "medica_chefe", "selo": selar({"valvula": motor.hash_pedido(eid), "dominio": dominio, "dia": dia}, K("vital/medica_chefe"))}
        resultados.append(motor.liquidar(eid, sv, dia, assinaturas=assinar(nomes[:3], eid, sv), emergencia=em)["estado"])
        dia += 1
    D.v(resultados == ["LIBERTADA_POR_VALVULA_VITAL_REVISAO_POSTERIOR"] * 2 + ["RECUSADO_VALVULA_LIMITE_2_EM_30_DIAS"],
        "B3 válvula vital médica (SAUDE · ALIMENTACAO · AGUA), assinatura pública: a 1.ª e a 2.ª libertam com revisão posterior; a 3.ª em 30 dias é recusada")
    hp7 = motor.hash_pedido("E7")
    estrada = valvula.acionar("ESTRADA", hp7, "medica_chefe", selar({"valvula": hp7, "dominio": "ESTRADA", "dia": dia}, K("vital/medica_chefe")), dia)
    falsa = valvula.acionar("SAUDE", hp7, "medica_chefe", selar({"valvula": hp7, "dominio": "SAUDE", "dia": dia}, K("vital/outra_pessoa")), dia)
    depois = valvula.acionar("SAUDE", hp7, "medica_chefe", selar({"valvula": hp7, "dominio": "SAUDE", "dia": dia + 40}, K("vital/medica_chefe")), dia + 40)
    D.v(estrada == (False, "DOMINIO_NAO_VITAL") and falsa == (False, "ASSINATURA_INVALIDA") and depois == (True, "ABERTA"),
        "B3 fora dos domínios vitais (ESTRADA) não abre; assinatura de outra chave não abre; passados 30 dias a mesma médica volta a poder")

    # --- P9: identidades inventadas, padrinhos em conluio, limite de carimbos
    inventados = [voto(f"inventado_{i}", "X1", True, dia) for i in range(1, 6)]
    for i in range(1, 6):
        aldeia.admitir(f"inventado_{i}", PUB(f"aldeia/inventado_{i}"),
                       [{"por": f"fantasma_{j}", "selo": selar({"atesto": f"inventado_{i}", "pub": PUB(f"aldeia/inventado_{i}")}, K(f"aldeia/fantasma_{j}"))} for j in range(3)])
    c1 = aldeia.contar(inventados, "X1", dia)
    D.v(c1["conformes"] == 0 and len(c1["ignorados"]) == 5, "P9 5 identidades inventadas, atestadas por quem não existe -> não entram, 0 votos")
    padrinhos = ["vizinha_1", "vizinha_2", "vizinha_3"]
    entrou = [aldeia.admitir(f"afilhado_{i}", PUB(f"aldeia/afilhado_{i}"), [atestar(p, f"afilhado_{i}") for p in padrinhos])[0] for i in range(1, 7)]
    c2 = aldeia.contar([voto(f"afilhado_{i}", "X2", True, dia) for i in range(1, 6)], "X2", dia)
    D.v(entrou == [True] * 5 + [False] and c2["conformes"] == 1,
        "P9 3 padrinhos em conluio metem 5 afilhados (o 6.º bate no limite de 5 atestados): os 5 votos contam como 1")
    c3 = aldeia.contar([voto(f"vizinha_{i}", "X3", False, dia) for i in range(3, 8)] + [voto(f"afilhado_{i}", "X3", True, dia) for i in range(1, 6)], "X3", dia)
    D.v(c3["desconformes"] == 5 and c3["conformes"] == 1, "P9 5 acusações honestas contra 5 afilhados: 5 a 1, o quórum falso não passa")
    limite = [aldeia.contar([voto("vizinha_7", f"Y{i}", True, dia)], f"Y{i}", dia) for i in range(1, 5)]
    D.v([x["conformes"] for x in limite[:2]] == [1, 1] and limite[-1]["ignorados"] == [["vizinha_7", "LIMITE_DE_CARIMBOS"]],
        "P9 limite declarado: a 5.ª obra carimbada pela mesma pessoa em 30 dias é ignorada")
    velha = oraculo(medido("Z1", (7.1, 6.9, 7.0), 3), fontes, "kWh/dia", "Z1", janela=(10, dia))
    velho = aldeia.contar([voto("vizinha_1", "Z1", True, 3)], "Z1", dia, desde=10)
    D.v(velha["estado"] == "INSUFICIENTE" and all(m == "FORA_DO_PRAZO" for _, m in velha["rejeitadas"]) and velho["ignorados"] == [["vizinha_1", "FORA_DO_PRAZO"]],
        "P12 + P9 leituras e votos antigos reapresentados (replay) -> FORA_DO_PRAZO, não contam")

    # --- P4 + P10 + contas
    copia = LedgerImutavel(K("notario"))
    copia.blocos = [dict(x) for x in livro.blocos]
    copia.blocos[3] = dict(copia.blocos[3], dia=99)
    D.v(livro.verificar_integridade_cadeia() and not copia.verificar_integridade_cadeia(),
        f"P4 LedgerImutavel com {len(livro.blocos)} blocos assinados confere; mexer num só bloco de uma cópia parte a cadeia")
    forja = LedgerImutavel(K("notario"))
    forja.blocos = [dict(x) for x in livro.blocos]
    anterior = forja.blocos[2]["hash_atual"]
    for j in range(3, len(forja.blocos)):  # quem mexe refaz os hashes todos daí para a frente, mas não tem a chave do notário
        corpo = {k: x for k, x in forja.blocos[j].items() if k not in ("hash_atual", "assinatura")}
        corpo["hash_anterior"] = anterior
        corpo["dia"] = 99 if j == 3 else corpo["dia"]
        anterior = hobj(corpo)
        forja.blocos[j] = dict(corpo, hash_atual=anterior, assinatura=forja.blocos[j]["assinatura"])
    D.v(not forja.verificar_integridade_cadeia() and all(c in livro.blocos[0] for c in ("hash_anterior", "payload", "assinatura", "hash_atual")),
        "P4 refazer os hashes todos sem a chave do notário também não passa: cai a assinatura do bloco")
    D.v(motor.conserva(), f"D2 contas certas ao cêntimo: reserva {_eur(motor.reserva)} + custódia {_eur(sum(motor.custodia.values()))} + fundo {_eur(motor.fundo)} + pago {_eur(sum(motor.pago.values()))} = {_eur(motor.total0)}")

    # ====================== D3 DOSAGEM PEDIÁTRICA COM VETO (M1 + M2) ======================
    D.p("")
    D.p("D3 DOSAGEM PEDIÁTRICA COM VETO — posto de saúde sem rede: tudo corre na ledger local do posto (M5)")
    fabricantes = {"laboratorio_farmaceutico": PUB("fab/laboratorio_farmaceutico")}
    agentes = dict(fabricantes, armazem_central=PUB("agente/armazem_central"), distribuidor_distrital=PUB("agente/distribuidor_distrital"))
    sensores = {"registador_do_frigorifico": PUB("sensor/registador_do_frigorifico")}
    posto = Posto("posto_de_saude", K("posto/posto_de_saude"), fabricantes, agentes, sensores, {"enfermeira_chefe": PUB("posto/enfermeira_chefe")})
    peso = G(12.0, 0.5, "kg", fonte="balanca")
    xarope = G(120.0, 0.0, "mg", fonte="xarope") / G(5.0, 0.0, "mL", fonte="colher")
    ref = dose_de_referencia("paracetamol_oral", 730, peso)
    D.p(f"  criança de 2 anos, {peso.txt('kg', 1)}: a norma do cofre (15 mg/kg, até 1000 mg por toma) dá {ref.txt('mg', 0)} = {(ref / xarope).txt('mL', 1)} de xarope "
        "a 120 mg/5 mL; pelo menos 4 h entre tomas, no máximo 4 tomas e 720 mg em 24 h")

    def toma(mg: float, horas: float = 6.0, tomas: int = 4, produto: str = "xarope de paracetamol") -> Dict[str, Any]:
        return {"produto": produto, "farmaco": "paracetamol_oral", "dose": G(mg, 0.0, "mg"), "intervalo": G(horas, 0.0, "h"), "tomas_24h": tomas, "hora": 0.0}

    def iv(substancia: str, hora: float) -> Dict[str, Any]:
        return {"produto": substancia + " (intravenoso)", "substancia": substancia, "hora": hora}

    t1 = posto.plano(730, peso, [toma(180.0)], 0)
    D.v(t1["estado"] == "SEM_VETO", "M1 180 mg de 6 em 6 horas, 4 tomas -> SEM_VETO: está dentro do teto da fonte (o motor confere, não receita)")
    t2 = posto.plano(730, peso, [toma(1800.0)], 0)
    D.v(t2["estado"] == "VETADO" and "10,0 vezes" in t2["vetos"][0]["motivo"], "M1 erro de vírgula (1800 mg) -> VETADO: " + t2["vetos"][0]["motivo"])
    t3 = posto.plano(730, peso, [toma(190.0)], 0)
    D.v(t3["estado"] == "REVISAO_HUMANA" and t3["vetos"] == [],
        "M1 190 mg: passa o teto de 180 mg, mas só dentro do erro da balança (± 0,5 kg) -> REVISAO_HUMANA: o motor não decide sozinho no limite")
    t4 = [posto.plano(730, peso, [toma(180.0, horas=2.0)], 0), posto.plano(730, peso, [toma(180.0, tomas=6)], 0)]
    D.v([x["estado"] for x in t4] == ["VETADO", "VETADO"], "M1 intervalo de 2 h (a fonte pede 4 h) -> VETADO; 6 tomas em 24 h (a fonte admite 4) -> VETADO")
    msg = _erro(lambda: verificar_toma("paracetamol_oral", 730, peso, G(7.5, 0.3, "mL"), G(6.0, 0.0, "h"), 4), TypeError)
    D.v(msg, "P1 dose escrita em mL, sem dizer a concentração -> TypeError: " + msg)
    D.v(_erro(lambda: verificar_toma("xarope_desconhecido", 730, peso, G(5.0, 0.0, "mg"), G(6.0, 0.0, "h"), 4), VetoFarmacologico)
        and _erro(lambda: verificar_toma("paracetamol_oral", 10, G(3.4, 0.1, "kg"), G(34.0, 0.0, "mg"), G(8.0, 0.0, "h"), 3), VetoFarmacologico)
        and issubclass(VetoFarmacologico, ValueError),
        "M1 falha fechado: fármaco fora do cofre -> veto; recém-nascido de 10 dias (a única fonte lida para essa idade foi retirada) -> veto: decide o clínico")
    t5 = posto.plano(730, peso, [toma(180.0), toma(120.0, produto="antigripal com paracetamol")], 0)
    D.v(t5["estado"] == "VETADO" and "mesma substância" in t5["vetos"][0]["motivo"],
        "M2 a mesma substância em 2 produtos, cada um dentro do seu teto: 720 + 480 = 1200 mg em 24 h, teto 720 mg -> VETADO")
    t6 = posto.plano(10, G(3.4, 0.1, "kg"), [iv("ceftriaxona", 0.0), iv("calcio_iv", 12.0)], 0)
    t7 = posto.plano(1825, G(18.0, 0.5, "kg"), [iv("ceftriaxona", 0.0), iv("calcio_iv", 12.0)], 0)
    D.v(t6["estado"] == "VETADO" and [x["norma"] for x in t6["vetos"]] == ["M2.ceftriaxona_calcio_iv"] and t7["estado"] == "REVISAO_HUMANA",
        "M2 VETO DE INTERAÇÃO: ceftriaxona + cálcio intravenoso com 12 h de intervalo num recém-nascido de 10 dias -> VETADO; "
        "o mesmo par numa criança de 5 anos -> REVISAO_HUMANA (a regra de veto é só até aos 28 dias)")
    D.p("  " + FARMACOPEIA["paracetamol_oral"]["o_que_nao_garante"])

    # ====================== D4 VACINA E CADEIA DE FRIO (M3) ======================
    D.p("")
    D.p("D4 VACINA — CADEIA DE FRIO +2 a +8 °C · alarmes da norma: >= +8 °C por 10 h seguidas; <= −0,5 °C por 60 min; sensor ± 0,5 °C")

    def lote_novo(produto: str, substancia: str, lote: str, n: int, validade: int, frio: bool = False) -> Dict[str, Any]:
        series = [f"{lote}-{i:04d}" for i in range(n)]
        m = fabricar_lote("laboratorio_farmaceutico", K("fab/laboratorio_farmaceutico"), produto, substancia, lote, series, validade, frio)
        e1 = passar_custodia(m, None, "laboratorio_farmaceutico", K("fab/laboratorio_farmaceutico"), "armazem_central", 1)
        e2 = passar_custodia(m, e1, "armazem_central", K("agente/armazem_central"), "distribuidor_distrital", 2)
        e3 = passar_custodia(m, e2, "distribuidor_distrital", K("agente/distribuidor_distrital"), "posto_de_saude", 3)
        return {"manifesto": m, "series": series, "cadeia": [e1, e2, e3], "hash": m["selo"]["hash"]}

    def embalagem(l: Dict[str, Any], i: int) -> Dict[str, Any]:
        return {"serie": l["series"][i], "prova": merkle_prova(l["series"], i), "manifesto": l["manifesto"], "cadeia": l["cadeia"]}

    def perfil(eventos: Sequence[Tuple[int, int, float]] = ()) -> List[float]:  # 48 h, uma leitura de 30 em 30 min
        ts = [round(5.0 + 0.3 * ((i * 7) % 5 - 2), 1) for i in range(96)]
        for inicio, fim, t in eventos:
            ts[inicio:fim] = [t] * (fim - inicio)
        return ts

    def registo_frio(l: Dict[str, Any], temperaturas: List[float]) -> Dict[str, Any]:
        d = {"sensor": "registador_do_frigorifico", "lote": l["hash"], "unidade": "°C", "passo_min": 30, "temperaturas": temperaturas}
        return {"dados": d, "selo": selar(d, K("sensor/registador_do_frigorifico"))}

    vac = {x: lote_novo("vacina de DEMO", "vacina", "VAC-" + x, 8, 400, frio=True) for x in "ABCDEF"}
    perfis = {"A": perfil(), "B": perfil([(20, 42, 10.5)]), "C": perfil([(30, 33, -1.2)]), "D": perfil([(20, 36, 9.0)]), "E": perfil([(20, 41, 7.8)])}
    frio = {x: posto.frio(registo_frio(vac[x], perfis[x]), 4) for x in "ABCDE"}
    D.p("  5 lotes, 48 h de registo selado pelo sensor: " + " · ".join(f"{x} {frio[x]['estado']}" for x in "ABCDE"))
    D.v(frio["A"]["estado"] == "APTA" and frio["B"]["estado"] == "BLOQUEADA_CALOR" and frio["B"]["minutos_acima"] == 660,
        "M3 lote A, sempre entre +2 e +8 °C -> APTA; lote B, 11 h seguidas a 10,5 °C -> BLOQUEADA_CALOR")
    D.v(frio["C"]["estado"] == "BLOQUEADA_CONGELOU" and frio["C"]["minutos_abaixo"] == 90,
        "M3 lote C, 90 min a −1,2 °C -> BLOQUEADA_CONGELOU (vacina sensível ao gelo)")
    D.v(frio["D"]["estado"] == "APTA_COM_EXCURSAO_CURTA" and frio["E"]["estado"] == "REVISAO_HUMANA_NO_LIMITE_DO_SENSOR",
        "M3 lote D, 8 h a 9 °C (abaixo das 10 h do alarme) -> APTA_COM_EXCURSAO_CURTA, fica registado; lote E, 10,5 h a 7,8 °C, a 0,2 °C do "
        "limite com um sensor de ± 0,5 °C -> REVISAO_HUMANA: no limite não decide a máquina")
    apagado = registo_frio(vac["B"], perfis["B"])
    apagado["dados"] = dict(apagado["dados"], temperaturas=perfil())
    D.v(avaliar_frio(apagado, sensores)["estado"] == "BLOQUEADA_REGISTO_SEM_SELO",
        "M3 apagar a avaria do registo depois de selado -> o selo cai -> BLOQUEADA_REGISTO_SEM_SELO")
    saidas = {x: posto.dispensar(embalagem(vac[x], 0), 5) for x in "ABEF"}
    D.v([saidas[x]["estado"] for x in "ABEF"] == ["DISPENSADO", "RECUSADO_LOTE_BLOQUEADO", "RECUSADO_LOTE_BLOQUEADO", "RECUSADO_SEM_PROVA_DE_FRIO"],
        "M3 medicamento morto = bloqueio: a vacina A sai; a B (autêntica, mas morta pelo calor) não sai; a E espera pela decisão humana; "
        "a F, sem registo de frio nenhum, não sai (sem prova de frio não há vacina)")
    dec_e = {"lote": vac["E"]["hash"], "apto": True, "dia": 5}
    rev = [posto.rever_lote(vac["E"]["hash"], True, "enfermeira_chefe", selar(dec_e, K("posto/outra_pessoa")), 5)["estado"],
           posto.rever_lote(vac["E"]["hash"], True, "enfermeira_chefe", selar(dec_e, K("posto/enfermeira_chefe")), 5)["estado"],
           posto.rever_lote(vac["B"]["hash"], True, "enfermeira_chefe", selar(dict(dec_e, lote=vac["B"]["hash"]), K("posto/enfermeira_chefe")), 5)["estado"]]
    D.v(rev == ["RECUSADO_ASSINATURA_DO_RESPONSAVEL", "APTA_POR_DECISAO_HUMANA", "RECUSADO_LOTE_NAO_ESTA_EM_REVISAO"]
        and posto.dispensar(embalagem(vac["E"], 0), 5)["estado"] == "DISPENSADO",
        "M3 a decisão sobre o lote E é humana e assinada: assinatura de outra pessoa não vale; a da enfermeira-chefe liberta-o; um lote morto (B) não se ressuscita")

    # ====================== D5 FÁRMACO FALSO (M4) + SINCRONIZAÇÃO SELADA (M5) ======================
    D.p("")
    D.p("D5 FÁRMACO FALSO — autenticidade pelo hash da cadeia: lote selado pelo fabricante, série na raiz de Merkle, custódia selada elo a elo")
    amox = lote_novo("amoxicilina 250 mg (DEMO)", "amoxicilina", "AMX-2026-11", 64, 400)
    boa = embalagem(amox, 7)
    a1 = posto.dispensar(boa, 6)
    D.v(a1["estado"] == "DISPENSADO" and merkle_confere(boa["serie"], boa["prova"], amox["manifesto"]["dados"]["raiz_series"]),
        f"M4 embalagem verdadeira: a série {boa['serie']} está na raiz de Merkle do lote (64 séries, prova de {len(boa['prova'])} hashes) e os 3 elos de custódia conferem -> DISPENSADO")
    a2 = posto.dispensar(dict(boa, serie="AMX-2026-11-9999"), 6)
    D.v(a2["estado"] == "RECUSADO_NAO_AUTENTICADO" and a2["motivo"] == "SERIE_FORA_DO_LOTE", "M4 série inventada -> NAO_AUTENTICADO (SERIE_FORA_DO_LOTE)")
    pirata = fabricar_lote("laboratorio_pirata", K("fab/laboratorio_pirata"), "amoxicilina 250 mg (DEMO)", "amoxicilina", "AMX-2026-11", amox["series"], 400)
    retocado = {"dados": dict(amox["manifesto"]["dados"], validade_dia=900), "selo": amox["manifesto"]["selo"]}
    a3 = [posto.dispensar(dict(embalagem(amox, 8), manifesto=pirata), 6)["motivo"], posto.dispensar(dict(embalagem(amox, 8), manifesto=retocado), 6)["motivo"]]
    D.v(a3 == ["FABRICANTE_NAO_REGISTADO", "SELO_DO_LOTE_INVALIDO"],
        "M4 o mesmo lote «selado» por um fabricante que não está registado -> FABRICANTE_NAO_REGISTADO; validade retocada no lote verdadeiro -> SELO_DO_LOTE_INVALIDO")
    a4 = posto.dispensar(embalagem(amox, 7), 7)
    D.v(a4["motivo"] == "SERIE_JA_DISPENSADA", "M4 a mesma série apresentada 2.ª vez (cópia de uma embalagem verdadeira) -> SERIE_JA_DISPENSADA")
    a5 = [posto.dispensar(dict(embalagem(amox, 9), cadeia=amox["cadeia"][:1] + amox["cadeia"][2:]), 7)["motivo"], posto.dispensar(embalagem(amox, 10), 401)["motivo"]]
    D.v(a5 == ["CADEIA_PARTIDA", "VALIDADE_PASSADA"], "M4 falta um elo da custódia (desvio) -> CADEIA_PARTIDA; fora da validade -> VALIDADE_PASSADA")
    D.p("  " + FRASES_OBRIGATORIAS["deteccao"] + " «Não autenticado» diz que a origem não se provou; não diz quem errou.")
    replica = Replica([posto.livro.pub])
    n_local = len(posto.livro.blocos)
    pk1 = sync_exportar(posto.livro, 0, K("posto/posto_de_saude"))
    s_1, s_2 = replica.importar(json.loads(canon(pk1))), replica.importar(pk1)  # o 1.º passa por JSON, como passaria por uma pen ou por rádio
    D.v(s_1 == ("SINCRONIZADO", n_local) and s_2 == ("JA_SINCRONIZADO", 0) and posto.livro.verificar_integridade_cadeia(),
        f"M5 o posto trabalhou sem rede: {n_local} blocos na sua ledger. Quando há rede exporta 1 pacote selado ({len(canon(pk1))} bytes) -> SINCRONIZADO; repetir o envio -> JA_SINCRONIZADO, não duplica")
    torto = json.loads(canon(pk1))
    torto["dados"]["blocos"][1]["payload"]["vetos"] = []
    outra = LedgerImutavel(K("posto/posto_de_saude"))
    outra.registar(0, "OUTRA_HISTORIA", {"nota": "o mesmo nó, com um passado reescrito"})
    posto.plano(730, peso, [toma(180.0)], 8)
    s_3 = [replica.importar(torto)[0], replica.importar(sync_exportar(outra, 0, K("posto/posto_de_saude")))[0],
           replica.importar(sync_exportar(posto.livro, n_local + 1, K("posto/posto_de_saude")))[0],
           replica.importar(sync_exportar(posto.livro, n_local, K("posto/posto_de_saude")))]
    D.v(s_3 == ["RECUSADO_SELO_INVALIDO", "RECUSADO_HISTORIA_DIVERGENTE", "RECUSADO_FALTAM_BLOCOS", ("SINCRONIZADO", 1)]
        and conferir_blocos(replica.copias[posto.livro.pub], posto.livro.pub) and len(replica.copias[posto.livro.pub]) == n_local + 1,
        "M5 pacote mexido em trânsito -> RECUSADO_SELO_INVALIDO; nó que reescreve o passado -> RECUSADO_HISTORIA_DIVERGENTE; "
        "saltar blocos -> RECUSADO_FALTAM_BLOCOS; só o bloco novo -> SINCRONIZADO, e a cópia central confere bloco a bloco")
    livro.registar(dia, "SYNC_POSTO", {"no": posto.livro.pub, "blocos": len(posto.livro.blocos), "cabeca": posto.livro.cabeca()})

    # ====================== D6 ÁFRICA 2030 ======================
    D.p("")
    D.p("D6 ÁFRICA 2030 — F2×F4×F5×F8: energia, saúde e alimentação por microrredes montadas por jovens formados (re-execução = mesmo hash)")
    entradas = entradas_africa_2030(float(n_ok))
    SEM_LUZ = 563e6  # MEDIDO: Tracking SDG7 2026 (AIE, IRENA, ONU, Banco Mundial, OMS), cap. 1: 563 milhões na África subsariana em 2024; lido a 20-11-2026 em trackingsdg7.esmap.org
    ALVO = 100e6     # ASSUMIDO: alvo do cenário
    medidos = sum(1 for e in entradas.values() if e["etiqueta"] == "MEDIDO")
    D.p(f"  entradas: {medidos} MEDIDO · {len(entradas) - medidos} ASSUMIDO · referência: 1 MEDIDO (pessoas sem eletricidade)")
    for k in sorted(entradas, key=lambda k: (ENTRADA_DE[k], k)):
        e = entradas[k]
        D.p(f"    {ENTRADA_DE[k]} {k:<18} {_num(e['valor']):>10} ± {_num(e['incerteza']):<9} {e['unidade']:<18} [{e['etiqueta']}] {e['fonte']}")
    p1 = pacote_cenario("AFRICA_2030", entradas, livro, dia)
    respostas.append(p1)
    nuc = p1["pacote"]
    for k in ("F2", "F4", "F5", "F8"):
        f, fa = FORMULAS[k], nuc["fatores"][k]
        D.p(f"  {k} v{f['versao']} [{f['etiqueta']}] {f['nome']}: {_num(fa['valor'])} ± {_num(fa['incerteza'], 3)} {fa['unidade']}   #{nuc['formulas'][k]['hash'][:12]}")
        D.p(f"       {f['formula']} · não garante: {f['o_que_nao_garante']}")
    res = nuc["resultado"]
    D.p(f"  F2×F4×F5×F8 = {_n(res['valor'] / 1e6, 1)} ± {_n(res['incerteza'] / 1e6, 1)} milhões de pessoas ({res['nota']}) = {_n(res['valor'] / SEM_LUZ * 100, 1)}% dos 563 milhões sem eletricidade na África subsariana em 2024 [MEDIDO]")
    D.p(f"  {CARIMBO}")
    D.p(f"  pacote sha256 {p1['hash_pacote']}")
    fa3 = calcular_cenario(entradas)[1]
    rv, ru = (fa3["F4"] * fa3["F8"]).em("microrrede")
    agua = fa3["F2"] * G(0.50, 0.10, "1", fonte="bomba") / (
        G(1000.0, 0.0, "kg/m3", fonte="agua") * G(9.80665, 0.0, "m/s^2", fonte="g") * G(20.0, 5.0, "m", fonte="altura"))
    av, au = agua.em("m3/dia/microrrede")
    D.p("  a mesma energia, mais 2 leituras (não se somam à de cima):")
    D.p(f"    saúde        cada microrrede é a de D1: garante a 95% os 5 kWh/dia de um posto de saúde; o cenário monta {_n(rv / 1e6, 2)} ± {_n(ru / 1e6, 2)} milhões")
    D.p(f"    alimentação  1 microrrede só a bombar eleva {_n(av, 0)} ± {_n(au, 0)} m3/dia de água a 20 ± 5 m (bomba a 50 ± 10%) [ASSUMIDO]: é rega, não é comida")
    D.v(agua.d == (("m", 3), ("microrrede", -1), ("s", -1)), "P1 a conta da água, E·η / (ρ·g·h), fechou em m3/dia por microrrede (conferido pelo motor de unidades)")
    campos = ("id", "versao", "formula", "unidades", "etiqueta", "fonte", "o_que_nao_garante")
    D.v(all(all(c in f for c in campos) and f["etiqueta"] in ("MEDIDO", "ASSUMIDO") for f in cofre().values())
        and all(e["etiqueta"] in ("MEDIDO", "ASSUMIDO") and e["fonte"] for e in entradas.values()),
        f"P7 as {len(cofre())} fichas do cofre (fórmulas A e B, ponto neutral, prevenção, teorias em debate, normas médicas, oráculos, domínios da v2.3, canários) trazem id, versão, "
        "fórmula, unidades, etiqueta, fonte e o_que_nao_garante; cada input traz etiqueta e fonte")
    D.v(calcular_cenario(entradas)[0].d == (("pessoa", 1),), "P1 o motor de unidades conferiu o produto: sai em pessoas")
    p2 = pacote_cenario("AFRICA_2030", json.loads(json.dumps(entradas)), livro, dia)
    D.v(p2["hash_pacote"] == p1["hash_pacote"] and p2["linhagem"]["hash_estado_ledger"] != p1["linhagem"]["hash_estado_ledger"],
        "D6 re-execução do mesmo input -> o MESMO hash de pacote (" + p2["hash_pacote"][:16] + "…); a ledger regista as duas corridas")
    outras = json.loads(json.dumps(entradas))
    outras["taxa_aprendizagem"]["valor"] = 0.21
    D.v(pacote_cenario("AFRICA_2030", outras, livro, dia)["hash_pacote"] != p1["hash_pacote"], "D6 mudar 1 input (aprendizagem 0,20 -> 0,21) -> hash diferente")
    D.v(p1["hash_pacote"] == "24ee3b4b302c1d83d120190c7cf2c48ecd9a27e10055d05a25f3c54a768369ce",
        "D6 o pacote tem o mesmo hash que saiu na v1.0 (24ee3b4b…): outra versão do motor, a mesma conta (por isso a fonte dos painéis ainda diz «C1», que é o D1 de hoje)")
    kp = kpkg_emitir("AFRICA_2030", entradas, K("emissor/comunidade"))
    kc = kpkg_consumir(json.loads(canon(kp)))
    D.v(kc["estado"] == "REPRODUZIDO" and kc["hash"] == kp["selo"]["hash"],
        f"P24 pacote aberto KPKG/1 ({len(canon(kp))} bytes de JSON canónico, selado): quem o recebe não confia, refaz a conta -> REPRODUZIDO · sha256 {kp['selo']['hash'][:16]}…")
    dobrado = json.loads(canon(kp))
    dobrado["corpo"]["resultado"]["valor"] *= 2.0
    resselado = {"corpo": dobrado["corpo"], "selo": selar(dobrado["corpo"], K("emissor/outro"))}
    outra_formula = json.loads(canon(kp))
    outra_formula["corpo"]["formulas"]["F8"]["hash"] = "0" * 64
    outra_formula = {"corpo": outra_formula["corpo"], "selo": selar(outra_formula["corpo"], K("emissor/outro"))}
    D.v([kpkg_consumir(x)["estado"] for x in (dobrado, resselado, outra_formula)] == ["SELO_INVALIDO", "RESULTADO_DIFERENTE", "FORMULA_DIFERENTE"],
        "P24 resultado dobrado: sem re-selar -> SELO_INVALIDO; re-selado por quem o dobrou -> RESULTADO_DIFERENTE (a conta refeita desmente-o); fórmula que não é a do cofre -> FORMULA_DIFERENTE")
    g = gargalo(entradas, ALVO)
    D.p(f"  B1 alvo {_n(ALVO / 1e6, 0)} milhões: o cenário dá {_n(g['base'] / 1e6, 1)}; falta multiplicar por {_n(ALVO / g['base'])}")
    D.p("    salto por 1% de esforço: " + " · ".join(
        f"{k}{' (−1%)' if entradas[k]['esforco'] < 0 else ''} +{_n(g['saltos_por_1pct'][k])}%" for k in g["ordem"]))
    D.p("    elasticidade dY/dX·X/Y: " + " · ".join(
        f"{k} {'+' if g['elasticidades'][k] > 0 else '−'}{_n(abs(g['elasticidades'][k]), 3)}" for k in g["ordem"]))
    y0, fat = calcular_cenario(entradas)
    por_fator = ((fat["F2"] * 1.01 * fat["F4"] * fat["F5"] * fat["F8"]).v / y0.v - 1.0) * 100.0
    D.p(f"    ao nível do fator (F2, F4, F5, F8): +{_n(por_fator)}% cada — num produto puro todos valem o mesmo; o gargalo decide-se nas alavancas")
    D.p(f"    gargalo: {g['formula_do_gargalo']} ({FORMULAS[g['formula_do_gargalo']]['nome']}) · alavanca {g['gargalo']}")
    for passo in g["plano"]:
        D.p(f"    ajuste: {passo['alavanca']} {_num(passo['de'])} -> {_num(passo['para'])} {entradas[passo['alavanca']]['unidade']} ({_n((passo['para'] / passo['de'] - 1) * 100, 1)}%)"
            + ("" if passo["chega"] else " — no limite físico, não chega sozinha"))
    D.p(f"    resultado recalculado com o ajuste: {_n(g['final'] / 1e6, 1)} milhões")
    um_menos_b = 1.0 + ln(1.0 - 0.20) / ln(2.0)

    def lny(fator: float) -> float:
        e2 = json.loads(json.dumps(entradas))
        e2["horas_pratica"]["valor"] = 6000.0 * fator
        return ln(calcular_cenario(e2)[0].v)

    numerica = (lny(1.0 + 1e-6) - lny(1.0 - 1e-6)) / 2e-6
    D.v(abs(numerica - 1.0 / um_menos_b) < 1e-6 and g["formula_do_gargalo"] == "F8",
        f"B1 elasticidade da aprendizagem: numérica {_n(numerica, 6)} = analítica 1/(1−b) = {_n(1.0 / um_menos_b, 6)} (> 1: aprender dá retornos crescentes)")
    D.v(abs(g["final"] / ALVO - 1.0) < 1e-9 and all(p["chega"] for p in g["plano"][-1:]), "B1 o ajuste, recalculado de raiz, acerta no alvo")
    fb = calcular_variante_b(ENTRADAS_B)
    vb = {k: fb[k].em(FORMULAS_B[k]["unidades"]["saida"])[0] for k in ("F2", "F4", "F5", "F8")}
    prod_b = fb["F2"] * fb["F4"] * fb["F5"] * fb["F8"]
    pacote_b = {"cenario": "AFRICA_2030_VARIANTE_B", "carimbo": CARIMBO, "entradas": ENTRADAS_B, "fatores": vb,
                "formulas": {k: {"versao": f["versao"], "hash": hobj(f)} for k, f in FORMULAS_B.items()},
                "resultado": {"valor": prod_b.em("ficha*pessoa/dia")[0], "unidade": "ficha*pessoa/dia"}}
    livro.registar(dia, "CENARIO", {"cenario": "AFRICA_2030_VARIANTE_B", "hash_pacote": hobj(pacote_b)})
    respostas.append({"estado": "CENARIO_VARIANTE_B", "hash_pacote": hobj(pacote_b),
                      "linhagem": {"hash_input": hobj(ENTRADAS_B), "hash_formula": hobj(FORMULAS_B), "hash_estado_ledger": livro.cabeca()},
                      "ledger": {"blocos": len(livro.blocos), "integra": livro.verificar_integridade_cadeia()}})
    D.p("  variante B do cofre — as 4 fórmulas do outro ficheiro, com os inputs dele (todas [ASSUMIDO]):")
    D.p(f"    F2 produção do enxame {_num(vb['F2'])} ficha/dia · F4 dividendo demográfico {_num(vb['F4'])} · F5 alcance das caixas {_num(vb['F5'])} pessoas · F8 retenção {_n(vb['F8'], 6)}")
    D.p(f"    F2×F4×F5×F8 = {_n(pacote_b['resultado']['valor'] / 1e6, 1)} milhões de ficha·pessoa/dia · pacote sha256 {hobj(pacote_b)}")
    D.p(f"    {CARIMBO}")
    D.v([round(vb[k], 6) for k in ("F2", "F4", "F5", "F8")] == [1800.0, 1.008, 270000.0, 0.606531],
        "D6 variante B: dá os mesmos 4 números que o outro ficheiro imprime (1800 · 1,008 · 270000 · 0,606531)")
    D.v(_erro(lambda: prod_b.em("pessoa"), TypeError),
        "P1 o produto da variante B sai em ficha·pessoa/dia e o da A em pessoas: medem coisas diferentes, ficam as duas no cofre e não se somam")

    # ====================== D7 PONTO NEUTRAL (P15 a P19) ======================
    D.p("")
    D.p("D7 PONTO NEUTRAL — N_eq = piso humano × teto ecológico-animal, entre 0 e 1 (limiares ASSUMIDO, à vista no cofre)")
    certificadoras = {"certificadora_independente": PUB("cert/certificadora_independente")}
    UN15 = dict(FORMULAS_15["F15.1"]["unidades"], **FORMULAS_15["F15.2"]["unidades"])

    def medicoes(**x: Tuple[float, float]) -> Dict[str, Dict[str, Any]]:
        return {k: {"valor": float(v), "incerteza": float(u), "unidade": UN15[k], "etiqueta": "MEDIDO", "fonte": "medição de DEMO"}
                for k, (v, u) in sorted(x.items())}

    def pm(x: Grandeza) -> str:
        return f"{_n(x.em('1')[0])} ± {_n(x.em('1')[1])}"

    teto_ok = {"carbono": (1.5, 0.2), "agua_captada": (0.30, 0.03), "habitat_ocupado": (0.62, 0.02), "captura_animal": (0.8, 0.1)}
    vale = [("2023", medicoes(agua=(31, 3), alimentacao=(1750, 80), energia=(0.09, 0.01), saude=(0.55, 0.04), **teto_ok)),
            ("2024", medicoes(agua=(38, 3), alimentacao=(1900, 80), energia=(0.13, 0.01), saude=(0.68, 0.04), **teto_ok)),
            ("2025", medicoes(agua=(45, 2), alimentacao=(2050, 60), energia=(0.15, 0.01), saude=(0.78, 0.03), **teto_ok)),
            ("2026", medicoes(agua=(49, 2), alimentacao=(2150, 60), energia=(0.19, 0.01), saude=(0.86, 0.02), **teto_ok))]
    rastro = RastroVital(livro)
    for periodo, m in vale:
        rastro.registar("comunidade_do_vale", periodo, m, dia)
    curva, niveis, tend = rastro.curva("comunidade_do_vale"), [ponto_neutral(m)["nivel"] for _, m in vale], rastro.tendencia("comunidade_do_vale")
    D.p("  P17 rastro vital da Comunidade do Vale, lido da ledger: " + " -> ".join(f"{p} {_n(n)} ± {_n(u)} ({nv})" for (p, n, u), nv in zip(curva, niveis)))
    D.v(len(curva) == 4 and niveis == ["BRONZE", "PRATA", "PRATA", "OURO"] and tend["estado"] == "A_SUBIR",
        f"P17 a curva do N_eq no tempo: de {tend['de']} a {tend['ate']} subiu {_n(tend['delta'])} ± {_n(tend['incerteza'])} -> A_SUBIR (a subida é maior do que o erro das medições, a 95%)")
    pn = ponto_neutral(vale[-1][1])
    cert = selo_ponto_neutral("comunidade_do_vale", "2026", vale[-1][1], K("cert/certificadora_independente"))
    ok_cert, nivel_cert = verificar_selo_ponto_neutral(json.loads(canon(cert)), certificadoras)
    D.p(f"  P15 Comunidade do Vale 2026: piso humano H = {pm(pn['H'])} · teto E = {pm(pn['E'])} · N_eq = {pm(pn['N_eq'])} · pior caso a 95% = {_n(pn['limite_inferior_95'])} -> SELO {pn['nivel']}")
    D.v(ok_cert and nivel_cert == "OURO" and cert["corpo"]["nivel"] == "OURO" and 0.0 <= pn["n_eq"] <= 1.0,
        f"P16 SELO OURO: certificado Ed25519 da certificadora ({cert['selo']['hash'][:16]}…); a verificação externa refaz a conta de raiz e dá o mesmo N_eq e o mesmo nível")
    subido = json.loads(canon(selo_ponto_neutral("comunidade_do_vale", "2024", vale[1][1], K("cert/certificadora_independente"))))
    subido["corpo"]["nivel"] = "OURO"
    mentira = {"corpo": subido["corpo"], "selo": selar(subido["corpo"], K("cert/certificadora_independente"))}
    de_bolso = {"corpo": cert["corpo"], "selo": selar(cert["corpo"], K("cert/certificadora_de_bolso"))}
    D.v([verificar_selo_ponto_neutral(x, certificadoras)[1] for x in (subido, mentira, de_bolso)]
        == ["SELO_INVALIDO_OU_CERTIFICADORA_NAO_REGISTADA", "RESULTADO_NAO_CONFERE", "SELO_INVALIDO_OU_CERTIFICADORA_NAO_REGISTADA"],
        "P16 trocar PRATA por OURO: sem re-selar, o selo cai; re-selado pela própria certificadora, a conta refeita desmente-a; certificadora que não está registada não conta")
    expo = {"radiacao_ionizante": {"valor": 4.0, "incerteza": 0.5, "unidade": "mSv"}, "solventes": {"valor": 120.0, "incerteza": 30.0, "unidade": "h"}}
    reg_e = rastro.exposicao(K("pessoa/trabalhador_de_demo"), "2026", expo, dia)
    bloco_e = livro.blocos[-1]
    mexido_e = {"dados": {"periodo": "2026", "exposicoes": dict(expo, radiacao_ionizante={"valor": 0.4, "incerteza": 0.5, "unidade": "mSv"})}, "selo": reg_e["selo"]}
    D.v(rastro.exposicao_confere(reg_e) and not rastro.exposicao_confere(mexido_e) and sorted(bloco_e["payload"]) == ["periodo", "registo", "titular"],
        "P17 exposoma de uma vida: a pessoa sela o seu registo (4,0 ± 0,5 mSv de radiação; 120 h de solventes) e guarda-o consigo; na ledger entra só o hash. "
        "Confere; com 4,0 trocado por 0,4 deixa de conferir")
    evit = f_harmonia(G(1000.0, 0.0, "caso"), G(0.50, 0.10, "1", fonte="adesao"))
    ev, eu = evit.em("caso")
    D.p(f"  P18 F-HARMONIA [CENÁRIO]: em 1000 casos de cancro, fração evitável (OMS: 30 a 50%) × adesão de 50 ± 10% [ASSUMIDO] = {_n(ev, 0)} ± {_n(eu, 0)} casos evitáveis")
    D.p("    " + FRASES_OBRIGATORIAS["prevencao"])
    D.p("    [VALIDAR] A frase de cima é a da ordem. A fonte diz: " + OMS_PREVENCAO + ".")
    deb = debate("radiacao_em_dose_baixa", G(1000.0, 0.0, "pessoa"), G(20.0, 4.0, "mSv", fonte="dose"), K("ciencia/registo"))
    D.p("  P18 teoria em debate — 1000 pessoas com 20 ± 4 mSv cada [ASSUMIDO]: "
        + " · ".join(f"{t['dados']['teoria']} {_n(t['dados']['casos'], 1)} ± {_n(t['dados']['incerteza'], 1)} casos" for t in deb["teorias"]) + f" -> {deb['estado']}")
    D.v(abs(ev - 200.0) < 1e-9 and abs(eu - 200.0 * math.sqrt((0.1 / math.sqrt(3.0) / 0.4) ** 2 + 0.2 ** 2)) < 1e-9
        and h256(" ".join(FRASES_OBRIGATORIAS.values()).encode("utf-8")) == "c0be9e8e98a28662fbd2c540215895da922d2194a4d0060724a8b72704b80727",
        "P18 a fração da OMS entra como intervalo (retangular: 40 ± 5,8 pontos) e a incerteza propaga-se; as 4 frases obrigatórias estão letra a letra (sha256 pregado no código)")
    D.v(deb["estado"] == "DEBATIDO" and len(deb["teorias"]) == 2 and all(selo_ok(t["dados"], t["selo"]) for t in deb["teorias"])
        and deb["teorias"][0]["dados"]["casos"] > 0.0 == deb["teorias"][1]["dados"]["casos"],
        "P18 teorias debatidas = AS DUAS seladas: a linear conta 1,1 casos, a do limiar conta 0; o motor sela as duas respostas e não escolhe")
    reserva_d7 = motor.reserva
    f8 = financiar(motor, "E8", "comunidade_do_vale", 2_000_000, dia, 5.0, "kWh/dia", cert, certificadoras)
    lagoa = medicoes(agua=(80, 4), alimentacao=(2600, 90), energia=(0.9, 0.05), saude=(0.95, 0.02), carbono=(6.5, 0.5), agua_captada=(0.62, 0.05),
                     habitat_ocupado=(0.88, 0.03), captura_animal=(1.6, 0.1))
    msg_v = _erro(lambda: ponto_neutral(lagoa), VetoBiofisico)
    cert_l = selo_ponto_neutral("comunidade_da_lagoa", "2026", lagoa, K("cert/certificadora_independente"))
    f9 = financiar(motor, "E9", "comunidade_da_lagoa", 2_000_000, dia, 5.0, "kWh/dia", cert_l, certificadoras)
    D.p("  Comunidade da Lagoa 2026 (comunidade tóxica): não lhe falta nada no piso humano e, mesmo assim -> VETADA: " + msg_v)
    D.v(msg_v and issubclass(VetoBiofisico, ValueError) and cert_l["corpo"]["nivel"] == "VETADO" and verificar_selo_ponto_neutral(cert_l, certificadoras) == (False, "VETO_BIOFISICO"),
        "P15 veto biofísico: 4 pressões acima do teto, a 95% -> VetoBiofisico; a certificadora sela VETADO; o conforto não compensa o teto")
    D.v(f8["estado"] == "ESCROW_CRIADO" and f9["estado"] == "RECUSADO_VETO_BIOFISICO" and "E9" not in motor.escrows
        and motor.reserva == reserva_d7 - 2_000_000 - f8["fundo_centimos"],
        "P19 financiamento: com SELO OURO -> ESCROW_CRIADO; fora do ponto neutral não se monta -> RECUSADO_VETO_BIOFISICO: o escrow nem chega a existir e o cofre não mexe")
    motor.criar_escrow("E10", "comunidade_da_lagoa", 2_000_000, dia, 5.0, "kWh/dia")  # um escrow como os de D2, criado antes da medição
    c10 = motor.congelar_por_veto("E10", "VETO_BIOFISICO", {"certificado": cert_l["selo"]["hash"], "veto": msg_v}, dia)
    s10 = motor.abrir_sessao("E10", dia)
    l10 = motor.liquidar("E10", s10, dia + 2, leituras=medido("E10", (7.1, 6.9, 7.0), dia), votos=[voto(q, "E10", True, dia) for q in conformes],
                         assinaturas=assinar(nomes, "E10", s10))
    d10 = motor.escrows["E10"]["dossie"]
    D.v(c10["estado"] == "CONGELADO_15D" and l10["estado"] == "RECUSADO_ESTADO_CONGELADO_15D" and selo_ok(d10["dados"], d10["selo"], {PUB("motor")}),
        "P19 escrow D2 bloqueado: um escrow como os de D2, já criado para a Lagoa, fica CONGELADO_15D pelo veto, com dossiê selado; nem com lastro, 5 conformes e 5 assinaturas sai dinheiro")
    ex10 = motor.avancar(dia + 16)
    D.v(len(ex10) == 1 and ex10[0]["estado"] == "EXPIRACAO_ESTORNO_ORIGEM" and motor.conserva(),
        "P6 15 dias sem decisão humana -> EXPIRACAO_ESTORNO_ORIGEM: o dinheiro volta à origem; nada fica preso para sempre")
    dia += 17

    # ====================== D8 VOTO ANÓNIMO EM ANEL (P11) ======================
    D.p("")
    D.p("D8 VOTO EM ANEL — LSAG sobre Ed25519: prova-se «sou uma das 7 vizinhas» sem dizer qual; a imagem da chave apanha quem vota 2 vezes")
    anel_v = [PUB(f"aldeia/vizinha_{i}") for i in range(1, 8)]
    urna = Urna("poco_ou_painel_2026", anel_v, ["POCO", "PAINEL"], livro)
    boletins = [(o, votar_em_anel(K(f"aldeia/vizinha_{i}"), urna, o)) for i, o in ((1, "POCO"), (2, "PAINEL"), (3, "POCO"), (4, "POCO"), (5, "PAINEL"))]
    estados = [urna.votar(o, s, dia)["estado"] for o, s in boletins]
    duplo = votar_em_anel(K("aldeia/vizinha_3"), urna, "PAINEL")  # a vizinha 3 tenta votar outra vez, agora noutra opção
    e_duplo = urna.votar("PAINEL", duplo, dia)["estado"]
    D.p(f"  5 votos -> {' · '.join(f'{o} {n}' for o, n in urna.contagem().items())} · 6.º voto -> {e_duplo} (a imagem {duplo['imagem'][:16]}… já estava na urna)")
    D.v(estados == ["VOTO_ACEITE"] * 5 and urna.contagem() == {"POCO": 3, "PAINEL": 2},
        "P11 5 votos válidos, cada um verificado contra o anel das 7 chaves registadas; em nenhum se sabe de quem é: POCO 3 · PAINEL 2")
    D.v(e_duplo == "VOTO_RECUSADO_DUPLO" and duplo["imagem"] == boletins[2][1]["imagem"] and lsag_verificar(duplo, urna.boletim("PAINEL")),
        "P11 voto duplo desmascarado: a assinatura do 6.º voto é válida, mas a imagem da chave é a de um voto já contado -> VOTO_RECUSADO_DUPLO, sem se ficar a saber quem foi")
    outra_urna = Urna("outra_votacao", anel_v, ["SIM", "NAO"], livro)
    noutra = votar_em_anel(K("aldeia/vizinha_3"), outra_urna, "SIM")
    D.v(len({s["imagem"] for _, s in boletins}) == 5 and noutra["imagem"] != duplo["imagem"] and duplo["imagem"] not in anel_v
        and votar_em_anel(K("aldeia/vizinha_1"), urna, "POCO") == boletins[0][1],
        "P11 5 pessoas = 5 imagens diferentes; a mesma pessoa noutra votação tem outra imagem (não se segue ninguém de urna em urna); a mesma entrada dá a mesma assinatura (sem sorteios)")
    intruso = lsag_assinar(K("aldeia/inventado_1"), anel_v[:6] + [PUB("aldeia/inventado_1")], urna.boletim("POCO"), urna.contexto)
    s_torto = list(boletins[1][1]["s"])
    s_torto[0] = s_torto[0][:-1] + ("0" if s_torto[0][-1] != "0" else "1")
    falsos = [urna.votar(o, x, dia)["estado"] for o, x in (("POCO", intruso), ("PAINEL", boletins[0][1]), ("PAINEL", dict(boletins[1][1], s=s_torto)),
                                                         ("PAINEL", dict(duplo, imagem=duplo["imagem"].upper())))]
    D.v(_erro(lambda: lsag_assinar(K("aldeia/inventado_1"), anel_v, urna.boletim("POCO"), urna.contexto), ValueError)
        and falsos == ["VOTO_RECUSADO_ANEL_OU_VOTACAO_ERRADOS"] + ["VOTO_RECUSADO_ASSINATURA_INVALIDA"] * 3 and urna.contagem() == {"POCO": 3, "PAINEL": 2},
        "P11 quem não está no anel não consegue assinar; um anel com um intruso é recusado; trocar a opção de um voto alheio, mexer 1 dígito, ou reescrever "
        "a imagem em maiúsculas para a fazer passar por nova: assinatura inválida. A contagem não mexe")

    # ====================== D9 LENS-BARCODE (P20) ======================
    D.p("")
    D.p("D9 LENS-BARCODE — o código de barras leva à análise selada do lote: o rótulo omite, a lâmpada mostra")
    lamp = Lampada({"laboratorio_alimentar": PUB("lab/laboratorio_alimentar")}, aldeia, livro)
    GTIN = "2000000000015"  # prefixo 200: gama de circulação restrita, não pertence a nenhuma marca [VALIDAR]

    def ficha(lote: str, sodio: float, sk: bytes) -> Tuple[Dict[str, Any], Dict[str, Any]]:
        rot = {"gtin": GTIN, "lote": lote, "produto": "papa de cereais infantil (produto FICTÍCIO de demo)",
               "declarado": {"sodio": {"valor": 2000.0, "tolerancia_rel": 0.20, "unidade": "mg/kg"},
                             "proteina": {"valor": 12.0, "tolerancia_rel": 0.20, "unidade": "%"}}}
        an = {"gtin": GTIN, "lote": lote, "laboratorio": "laboratorio_alimentar",
              "medido": {"sodio": {"valor": sodio, "incerteza": 100.0, "unidade": "mg/kg"}, "proteina": {"valor": 11.6, "incerteza": 0.5, "unidade": "%"},
                         "acucares_adicionados": {"valor": 14.0, "incerteza": 1.0, "unidade": "%"}}}
        return rot, {"dados": an, "selo": selar(an, sk)}

    def leitura_rede(quem: str, lote: str, valor: float, unidade: str = "mg/kg") -> Dict[str, Any]:
        d = {"quem": quem, "gtin": GTIN, "lote": lote, "substancia": "sodio", "valor": valor, "unidade": unidade, "dia": dia}
        return {"dados": d, "selo": selar(d, K("aldeia/" + quem))}

    pub_l = [lamp.publicar(*ficha("L1", 2050.0, K("lab/laboratorio_alimentar")), dia), lamp.publicar(*ficha("L2", 2100.0, K("lab/laboratorio_alimentar")), dia),
             lamp.publicar(*ficha("L3", 2000.0, K("lab/laboratorio_de_bolso")), dia)]
    luz = lamp.iluminar(GTIN, "L1")
    D.p(f"  lente no código {GTIN}, lote L1 -> o rótulo declara {' e '.join(sorted(luz['declarado']))}; a análise selada de {luz['laboratorio']} mostra também: "
        + ", ".join(f"{s.replace('_', ' ')} {_num(m['valor'])} ± {_num(m['incerteza'])} {m['unidade']}" for s, m in luz["omitido"].items()))
    D.v(gtin13_valido(GTIN) and not gtin13_valido("2000000000016") and pub_l == ["PUBLICADO", "PUBLICADO", "RECUSADO_ANALISE_SEM_SELO_DE_LABORATORIO"]
        and luz["estado"] == "ROTULO_OMITE" and list(luz["omitido"]) == ["acucares_adicionados"] and lamp.iluminar(GTIN, "L3")["estado"] == "SEM_FICHA",
        "P20 rótulo omitido revelado: 14% de açúcares adicionados que o rótulo não diz; código de barras com o dígito de controlo errado não passa; "
        "análise sem selo de laboratório registado não entra (sem ficha, a lâmpada não inventa)")
    rot_g, an_g = ficha("L4", 2000.0, K("lab/laboratorio_alimentar"))
    an_g["dados"]["medido"]["sodio"]["unidade"] = "kWh"
    an_g = {"dados": an_g["dados"], "selo": selar(an_g["dados"], K("lab/laboratorio_alimentar"))}
    D.v(lamp.publicar(rot_g, an_g, dia) == "RECUSADO_UNIDADES_INCOMPATIVEIS" and lamp.ler(leitura_rede("vizinha_6", "L1", 2.0, "kWh")) == "RECUSADO_UNIDADE_ERRADA",
        "P20 + P1 análise ou leitura noutra grandeza (sódio em kWh) não entra: o motor de unidades trava a mistura")
    D.p("  " + FRASES_OBRIGATORIAS["lampada"])
    motor.criar_escrow("E11", "fornecedor_alimentar", 1_500_000, dia, 500.0, "kg")
    aceites = [lamp.ler(leitura_rede(f"vizinha_{i}", "L2", x)) for i, x in ((1, 6100.0), (2, 5800.0), (3, 6400.0))]
    cedo = lamp.avaliar(GTIN, "L2", "sodio", dia, motor, "E11")
    ativo_cedo = motor.escrows["E11"]["estado"] == "ATIVO"
    aceites += [lamp.ler(leitura_rede(f"vizinha_{i}", "L2", x)) for i, x in ((4, 6000.0), (5, 5900.0))]
    recusadas = [lamp.ler(leitura_rede("vizinha_5", "L2", 9999.0)), lamp.ler(leitura_rede("inventado_1", "L2", 9999.0))]
    for i in range(1, 6):
        lamp.ler(leitura_rede(f"afilhado_{i}", "L1", 9000.0))
    conluio = lamp.avaliar(GTIN, "L1", "sodio", dia, motor, "E11")
    alerta = lamp.avaliar(GTIN, "L2", "sodio", dia, motor, "E11")
    D.v(aceites == ["ACEITE"] * 5 and cedo["estado"] == "AGUARDA_REDE_K" and cedo["leitores_independentes"] == 3 and ativo_cedo
        and recusadas == ["RECUSADO_LEITURA_REPETIDA", "RECUSADO_LEITOR_NAO_REGISTADO_OU_SELO_INVALIDO"],
        "P20 com 3 leitores a rede ainda não fala (k >= 5) -> AGUARDA_REDE_K, e o escrow não mexe; leitura repetida, ou de quem não está registado, não entra")
    D.v(conluio["estado"] == "AGUARDA_REDE_K" and conluio["leitores_independentes"] == 1,
        "P20 + P9 5 leitores apadrinhados pelos mesmos 3 contam como 1: não conseguem lançar um alerta falso sobre o lote L1")
    D.p(f"  lote L2, sódio: {alerta.get('leitores_independentes')} leitores independentes, mediana {_num(alerta.get('mediana', 0.0))} ± {_num(alerta.get('incerteza', 0.0), 2)} mg/kg; "
        f"o rótulo declara 2000 ± 20% -> {alerta['estado']} · escrow E11 do fornecedor -> {alerta.get('escrow')}")
    D.v(alerta["estado"] == "ALERTA_LOTE_ANOMALO" and alerta.get("escrow") == "CONGELADO_15D" and motor.escrows["E11"]["estado"] == "CONGELADO_15D"
        and not {"culpado", "responsavel", "acusado"} & set(alerta),
        "P20 lote anómalo com k >= 5 -> ALERTA_LOTE_ANOMALO + escrow do fornecedor CONGELADO_15D; o alerta leva o lote e os números medidos, não aponta ninguém")
    D.p("  " + FRASES_OBRIGATORIAS["deteccao"])
    rj11 = motor.julgar("E11", "CORRIGIDO", "juiza_distrital", julgamento("E11", "CORRIGIDO", dia + 3), dia + 3)
    D.v(rj11["estado"] == "CORRIGIDO" and motor.escrows["E11"]["estado"] == "CORRIGIDO" and motor.conserva(),
        "P20 + P6 contraditório: ouvido o fornecedor, a juíza assina CORRIGIDO (lote trocado); o pagamento volta a poder sair com nova prova. Quem decide é uma pessoa")
    dia += 4

    # ====================== D10 GOVERNANÇA (P21 · P22 · P25, com P13) ======================
    D.p("")
    D.p("D10 GOVERNANÇA — a constituição em código: mudar uma REGRA pede proposta selada + k >= 5 votos anónimos + assinatura humana + versão nova")

    def votos_sim(prop: Dict[str, Any], quem: Sequence[int]) -> List[Dict[str, Any]]:
        boletim, contexto = const.boletim(prop)
        return [lsag_assinar(K(f"aldeia/conselho_{i}"), const.eleitorado, boletim, contexto) for i in quem]

    def assina_guardia(prop: Dict[str, Any], nome: str = "guardia_da_constituicao") -> Dict[str, str]:
        return selar({"ratifico": prop["selo"]["hash"], "guardiao": nome}, K("guardia/" + nome))

    p_a = const.propor("fundo_reparacao_pct", 1, "cortar o fundo de reparação para metade", K("aldeia/conselho_7"), dia)
    v_a = votos_sim(p_a, (5, 6, 7))
    r_a = const.ratificar(p_a, v_a + v_a, "guardia_da_constituicao", assina_guardia(p_a), dia)  # os mesmos 3 votam 2 vezes, para parecerem 6
    D.p(f"  (a) proposta «fundo de reparação 2% -> 1%», 3 votos apresentados 2 vezes -> {r_a['estado']} ({r_a.get('motivo')}: {r_a.get('votos_validos')} de {r_a.get('exigidos')})"
        f" · hash da tentativa {r_a.get('hash_tentativa', '')[:16]}…")
    D.v(r_a["estado"] == "REJEITADA" and r_a["motivo"] == "SEM_QUORUM" and r_a["votos_validos"] == 3 and REGRAS["fundo_reparacao_pct"] == 2 and len(const.versoes) == 1
        and any(b["evento"] == "REJEITADA" and b["payload"].get("hash_tentativa") == r_a["hash_tentativa"] for b in livro.blocos),
        "P21 (a) tentativa de alterar uma regra sem quórum -> REJEITADA; a regra não mexeu; a tentativa ficou na ledger, com hash")
    r_a2 = const.ratificar(p_a, v_a + votos_sim(p_a, (3, 4)), "guardia_falsa", assina_guardia(p_a, "guardia_falsa"), dia)
    p_k = const.propor("quorum_k", 1, "decidir mais depressa", K("aldeia/conselho_7"), dia)
    r_a3 = const.ratificar(p_k, votos_sim(p_k, range(1, 8)), "guardia_da_constituicao", assina_guardia(p_k), dia)
    D.v([r_a2.get("motivo"), r_a3.get("motivo")] == ["SEM_ASSINATURA_HUMANA", "CLAUSULA_PETREA"] and REGRAS["quorum_k"] == 5,
        "P21 (a) com 5 votos, mas sem a assinatura humana registada -> REJEITADA; baixar o quórum para 1, mesmo com 7 votos e assinatura -> REJEITADA (cláusula pétrea: k >= 5)")
    REGRAS["quorum_k"] = 1  # alguém mexe na regra por fora, sem emenda
    e12 = motor.criar_escrow("E12", "cooperativa_sol", 100_000, dia, 5.0, "kWh/dia")
    infiel = not const.fiel()
    REGRAS["quorum_k"] = 5
    D.v(infiel and e12["estado"] == "BLOQUEADO_REGRAS_FORA_DA_CONSTITUICAO" and e12["linhagem"]["hash_formula"] != e12["regras_da_constituicao"]
        and const.fiel() and "E12" not in motor.escrows,
        "P21 traição às regras: mexer por fora faz o hash das regras deixar de bater com a constituição; o motor recusa trabalhar e regista os dois hashes, à vista de todos")
    p_b = const.propor("fundo_reparacao_pct", 3, "reforçar o fundo de reparação", K("aldeia/conselho_1"), dia)
    v_b = votos_sim(p_b, (1, 2, 3, 4, 5))
    r_b = const.ratificar(p_b, v_b, "guardia_da_constituicao", assina_guardia(p_b), dia)
    D.p(f"  (b) proposta «fundo de reparação 2% -> 3%», 5 votos SIM em anel + assinatura da guardiã -> {r_b['estado']} · versão {r_b.get('versao')}"
        f" · regras {r_b.get('regras_antes', '')[:12]}… -> {r_b.get('regras_depois', '')[:12]}…")
    D.v(r_b["estado"] == "EMENDA_RATIFICADA" and REGRAS["fundo_reparacao_pct"] == 3 and hash_regras() == r_b["regras_depois"] != HASH_REGRAS and const.fiel(),
        "P21 (b) emenda legítima (k >= 5 + assinatura humana) -> versão nova no cofre; as regras em vigor passam a ser as novas")
    e13 = motor.criar_escrow("E13", "cooperativa_sol", 1_000_000, dia, 5.0, "kWh/dia")
    D.v(e13["fundo_centimos"] == 30_000 and e13["linhagem"]["hash_formula"] == r_b["regras_depois"]
        and r1["linhagem"]["hash_formula"] == HASH_REGRAS == const.versoes[0]["hash_regras"],
        "P21 + P10 efeito e linhagem: um escrow novo já põe 3% no fundo e leva o hash das regras novas; as respostas antigas (E1) continuam a levar o das regras de nascença")
    adulteradas = json.loads(json.dumps(const.versoes))
    adulteradas[1]["regras"]["fundo_reparacao_pct"] = 0
    repetida = const.ratificar(p_b, v_b, "guardia_da_constituicao", assina_guardia(p_b), dia)
    D.v(const.conferir() and len(const.versoes) == 2 and hobj(const.versoes[0]["regras"]) == HASH_REGRAS and not const.conferir(adulteradas)
        and repetida.get("motivo") == "PROPOSTA_DE_OUTRA_VERSAO",
        "P21 a versão antiga fica verificável para sempre: a cadeia de versões confere de raiz (hashes, proposta, os 5 votos em anel, assinatura humana); "
        "uma versão retocada não confere; a mesma emenda não se reapresenta")
    filho, gen = fork_genesis("comunidade_do_vale", livro, const, K("fork/comunidade_do_vale"), dia)
    selo_nasc = selo_do_fork(filho, fontes)
    D.p(f"  (c) fork «comunidade_do_vale»: génese {gen['hash_genesis'][:16]}… · cofre {gen['cofre'][:12]}… · constituição {gen['constituicao'][:12]}… (versão {const.atual()['n']})"
        f" · chave própria {filho.pub[:12]}… · nasce com selo {selo_nasc}")
    D.v(selo_nasc == "B" and gen["cofre"] == hash_cofre() and gen["mae"]["pub"] == livro.pub != filho.pub
        and any(b["evento"] == "FORK_NASCEU" and b["payload"]["genesis"] == gen["hash_genesis"] for b in livro.blocos),
        "P22 (c) o fork nasce do cofre e da constituição da mãe, com chave própria, registado nas duas cadeias, e com selo B (não-selado): "
        "a fábrica é de todos; a confiança conquista-se")
    prova = Prova1(filho, K("fork/comunidade_do_vale"), "comunidade_do_vale")
    foto, folha = b"fotografia da bomba a trabalhar (bytes de DEMO)", b"folha do contador de agua, 7 dias (bytes de DEMO)"
    tres = ("contador_selado", "satelite", "inspetora")
    passos = [prova.pre_registar("MARCO-1", "a bomba solar dá água à aldeia?", "água elevada por dia", "m3/dia", 20.0, ["fotografia_da_obra", "folha_do_contador"], dia),
              prova.pre_registar("MARCO-1", "a bomba solar dá água à aldeia?", "água elevada por dia", "m3/dia", 5.0, ["fotografia_da_obra"], dia),
              prova.preencher("MARCO-1", "fotografia_da_obra", foto, dia + 1),
              prova.fechar("MARCO-1", [], fontes, dia + 1)["resultado"],
              prova.preencher("MARCO-1", "folha_do_contador", folha, dia + 1),
              prova.preencher("MARCO-1", "fotografia_da_obra", b"outra fotografia", dia + 1),
              prova.fechar("MARCO-1", [leitura(f, x, "m3/dia", "MARCO-1", dia - 5) for f, x in zip(tres, (40.0, 41.0, 42.0))], fontes, dia + 2)["resultado"]]
    fecho = prova.fechar("MARCO-1", [leitura(f, x, "m3/dia", "MARCO-1", dia + 2) for f, x in zip(tres, (24.0, 23.1, 25.2))], fontes, dia + 2)
    selo_dep = selo_do_fork(filho, fontes)
    D.p(f"      primeiro marco selado: PROVA/1 «MARCO-1» -> {fecho['resultado']} ({_n(fecho.get('valor', 0.0), 1)} ± {_n(fecho.get('incerteza', 0.0), 1)} m3/dia; mínimo pré-selado: 20)"
        f" · selo {fecho.get('selo', {}).get('hash', '')[:16]}… · selo de confiança do fork: {selo_nasc} -> {selo_dep}")
    D.v(passos == ["PRE_SELADA", "RECUSADO_JA_PRE_SELADA", "PREENCHIDO", "INCOMPLETO", "PREENCHIDO", "RECUSADO_SLOT_JA_PREENCHIDO", "INCONCLUSIVO"],
        "P13 PROVA/1: o critério sela-se antes dos dados e não se muda depois (2.º pré-registo, com mínimo mais baixo, recusado); com slots vazios não fecha; "
        "slot preenchido não se troca; leituras anteriores ao pré-selo não contam")
    D.v(fecho["resultado"] == "CUMPRIDO" and prova.conferir("MARCO-1", {"fotografia_da_obra": foto, "folha_do_contador": folha}, fontes)
        and not prova.conferir("MARCO-1", {"fotografia_da_obra": b"outra fotografia", "folha_do_contador": folha}, fontes)
        and all(set(b["payload"]) == {"id", "slot", "evidencia"} for b in filho.blocos if b["evento"] == "PROVA1_SLOT"),
        "P13 os slots só guardam o hash das evidências (a fotografia fica com quem a tirou); quem as tem confere tudo de raiz; com uma fotografia trocada já não confere")
    apressado, _ = fork_genesis("fork_apressado", livro, const, K("fork/fork_apressado"), dia)
    apressado.registar(dia, "PROVA1_FECHADA", {"resultado": "CUMPRIDO"})
    D.v(selo_dep == "A" and selo_do_fork(apressado, fontes) == "B",
        "P22 o selo ganha-se por prova: o fork passa de B a A quando a sua PROVA/1, refeita por quem verifica, dá CUMPRIDO; escrever «CUMPRIDO» na própria cadeia não chega (fica B)")
    limpo = auditar_canarios()
    original = CANARIOS["F0.K1"]["formula"]
    CANARIOS["F0.K1"]["formula"] = original.replace("0,7316", "0,7317")  # alguém «afina» a 4.ª casa decimal de uma isca
    try:
        alarmes = auditar_canarios(livro=livro, dia=dia)
        durante = [kpkg_consumir(kp)["estado"], _erro(lambda: kpkg_emitir("AFRICA_2030", entradas, K("emissor/comunidade")), RuntimeError)[:18]]
    finally:
        CANARIOS["F0.K1"]["formula"] = original
    isca = json.loads(canon(kp))
    isca["corpo"]["formulas"]["F0.K1"] = {"versao": "1.0.0", "hash": CANARIOS_SELADOS["F0.K1"]}
    isca = {"corpo": isca["corpo"], "selo": selar(isca["corpo"], K("emissor/copiador"))}
    al = alarmes[0] if alarmes else {"alarme": "SEM_ALARME", "canario": "", "hash_esperado": "", "hash_encontrado": ""}
    D.p(f"  (d) canário F0.K1 tocado (0,7316 -> 0,7317) -> {al['alarme']} · hash pregado {al['hash_esperado'][:16]}… · hash encontrado {al['hash_encontrado'][:16]}…")
    D.v(limpo == [] and len(alarmes) == 1 and al["canario"] == "F0.K1" and al["hash_esperado"] == CANARIOS_SELADOS["F0.K1"] != al["hash_encontrado"]
        and any(b["evento"] == "ALARME_CANARIO" and b["payload"]["hash_encontrado"] == al["hash_encontrado"] for b in livro.blocos),
        "P25 (d) canário tocado -> ALARME_CANARIO com os dois hashes (o pregado no código e o encontrado), registado na ledger")
    D.v(durante == ["COFRE_COMPROMETIDO", "COFRE_COMPROMETIDO"] and auditar_canarios() == [] and kpkg_consumir(isca)["estado"] == "ALARME_CANARIO"
        and kpkg_consumir(kp)["estado"] == "REPRODUZIDO",
        "P25 auditoria contínua: com um canário tocado, o cofre não consome nem emite pacotes; reposto, volta a trabalhar; um pacote que cite a isca denuncia quem copiou o cofre às cegas")

    # ====================== D11 DA OUTRA SUITE, FEITO DE VERDADE (v2.3: P2 Carnot · L1 · R1 · S1) ======================
    D.p("")
    D.p("D11 DA OUTRA SUITE, FEITO DE VERDADE — teto de Carnot, a massa de um contentor, a energia de um drone, stock parado (lá era texto fixo)")
    dia += 3
    t_q, t_f = G(600.0, 5.0, "K", fonte="termometro_quente"), G(300.0, 2.0, "K", fonte="termometro_frio")
    teto_c = teto_de_carnot(t_q, t_f)
    carnot = [veto_de_carnot(G(x, 0.0, "%"), t_q, t_f)["estado"] for x in (45.0, 50.5)]
    msg_c = _erro(lambda: veto_de_carnot(G(62.0, 0.0, "%"), t_q, t_f), VetoFisico)
    D.p(f"  máquina térmica entre {t_q.txt('K', 0)} e {t_f.txt('K', 0)}: teto de Carnot = {_n(teto_c.em('%')[0], 1)} ± {_n(teto_c.em('%')[1], 1)} % (lá vinha 0,500 escrito à mão)")
    D.v(abs(teto_c.em("1")[0] - 0.5) < 1e-12 and carnot == ["DENTRO_DO_TETO_DE_CARNOT", "REVISAO_HUMANA"] and "nenhuma prova o salva" in msg_c
        and _erro(lambda: teto_de_carnot(t_f, t_q), VetoFisico) and _erro(lambda: teto_de_carnot(G(600.0, 0.0, "°C"), t_f), TypeError),
        "P2 teto de Carnot calculado das duas temperaturas: 45% -> dentro; 50,5% -> REVISAO_HUMANA (o excesso cabe no erro dos termómetros); "
        "62% -> veto, e nenhuma prova o salva; temperaturas trocadas -> veto; temperatura em °C -> TypeError")
    D.v(iso6346_valido("CSQU3054383") and not iso6346_valido("CSQU3054384") and not iso6346_valido("CMAU-774120-9")
        and iso6346_digito("CMAU-774120-9") == 5 and iso6346_valido("CMAU 774120 5") and not iso6346_valido("ABC123"),
        "L1 número de contentor (ISO 6346): CSQU3054383 confere; com 1 algarismo trocado já não; o contentor que a outra suite dá como "
        "«corredor verde aprovado», CMAU-774120-9, não passa (o dígito certo seria 5)")
    carga = G(24000.0, 20.0, "kg", fonte="balanca_da_origem")
    bal_ok = balanco_de_massa(carga, G(23990.0, 20.0, "kg", fonte="balanca_do_destino"))
    bal_falta = balanco_de_massa(carga, G(23700.0, 20.0, "kg", fonte="balanca_do_destino"))
    bal_guia = balanco_de_massa(carga, G(23700.0, 20.0, "kg", fonte="balanca_do_destino"), G(290.0, 10.0, "kg", fonte="guia_de_perdas"))
    motor.criar_escrow("E14", "transportadora", 800_000, dia, 24000.0, "kg")
    resp_bal = responder(livro, dia, bal_falta["estado"], {"contentor": "CSQU3054383", "carregado_kg": [24000.0, 20.0], "descarregado_kg": [23700.0, 20.0]},
                         FORMULAS_23["L1"], **{k: x for k, x in bal_falta.items() if k != "estado"})
    c14 = motor.congelar_por_veto("E14", bal_falta["estado"], {"contentor": "CSQU3054383", "diferenca_kg": bal_falta["diferenca_kg"],
                                                              "limiar_kg": bal_falta["limiar_kg"]}, dia)
    D.p(f"  contentor CSQU3054383, matéria perigosa: carregados 24 000 ± 20 kg, descarregados 23 700 ± 20 kg -> faltam {_n(bal_falta['diferenca_kg'], 0)} ± "
        f"{_n(bal_falta['incerteza_kg'], 0)} kg (limiar {_n(bal_falta['limiar_kg'], 0)} kg) -> {bal_falta['estado']} · escrow E14 da transportadora -> {c14['estado']}")
    D.v(bal_ok["estado"] == "CONFORME" and bal_guia["estado"] == "CONFORME" and _erro(lambda: balanco_de_massa(carga, G(23990.0, 0.0, "kWh")), TypeError),
        "L1 balanço de massa: 10 ± 28 kg de diferença cabem no erro das duas balanças -> CONFORME; 300 kg a menos com 290 ± 10 kg de perdas "
        "declaradas na guia -> CONFORME; uma pesagem em kWh -> TypeError")
    D.v(bal_falta["estado"] == "ALERTA_MASSA_EM_FALTA" and c14["estado"] == "CONGELADO_15D" and not {"culpado", "responsavel", "acusado"} & set(resp_bal)
        and resp_bal["linhagem"]["hash_formula"] == hobj(FORMULAS_23["L1"]),
        "L1 + P6 300 ± 28 kg a menos, sem perdas declaradas -> ALERTA_MASSA_EM_FALTA + escrow CONGELADO_15D, com dossiê selado; "
        "o alerta leva os números das pesagens, não aponta ninguém")
    D.p("  " + FRASES_OBRIGATORIAS["deteccao"])
    rj14 = motor.julgar("E14", "CORRIGIDO", "juiza_distrital", julgamento("E14", "CORRIGIDO", dia + 2), dia + 2)
    D.v(rj14["estado"] == "CORRIGIDO" and motor.conserva(),
        "L1 + P6 contraditório: repetida a pesagem à frente das duas partes, a juíza assina CORRIGIDO. Quem decide é uma pessoa")
    operadores = {"enfermeira_chefe": PUB("posto/enfermeira_chefe")}
    energia_do_dia = e_ok * G(1.0, 0.0, "dia") * G(1.0, 0.0, "microrrede")  # os painéis de D1, num dia

    def missao_de(watts: float, u_w: float, minutos: float, u_min: float, assina: Optional[str] = "posto/enfermeira_chefe",
                  destino: str = "aldeia_norte") -> Tuple[Dict[str, Any], Optional[Dict[str, str]], Dict[str, Any]]:
        m = {"missao": "levar vacinas", "destino": destino, "potencia_w": watts, "duracao_min": minutos, "dia": dia}
        trava = selar(m, K(assina)) if assina else None
        return m, trava, orcamento_de_missao(G(watts, u_w, "W", fonte="motores"), G(minutos, u_min, "min", fonte="rota"),
                                             energia_do_dia, m, trava, operadores)

    m_voo, trava_voo, voo = missao_de(700.0, 50.0, 120.0, 10.0)
    sem_trava = [missao_de(700.0, 50.0, 120.0, 10.0, assina=None)[2]["estado"], missao_de(700.0, 50.0, 120.0, 10.0, assina="posto/outra_pessoa")[2]["estado"],
                 orcamento_de_missao(G(700.0, 50.0, "W"), G(120.0, 10.0, "min"), energia_do_dia, dict(m_voo, destino="outro_sitio"), trava_voo, operadores)["estado"]]
    voo_grande, voo_justo = missao_de(1500.0, 100.0, 300.0, 20.0)[2], missao_de(1000.0, 80.0, 270.0, 20.0)[2]
    D.p(f"  drone do posto: 700 ± 50 W durante 120 ± 10 min = {_n(voo['precisa_kwh'])} ± {_n(voo['u_precisa_kwh'])} kWh; os {n_ok} painéis de D1 dão "
        f"{energia_do_dia.txt('kWh')} num dia; com 20% de reserva ficam {_n(voo['util_kwh'])} ± {_n(voo['u_util_kwh'])} kWh -> {voo['estado']}")
    D.v(voo["estado"] == "AUTORIZADA" and voo["pior_caso_precisa_kwh"] <= voo["pior_caso_util_kwh"] and abs(voo["precisa_kwh"] - 1.4) < 1e-9,
        f"R1 a missão cabe mesmo no pior caso a 95% (precisa {_n(voo['pior_caso_precisa_kwh'])}; há {_n(voo['pior_caso_util_kwh'])} kWh) "
        "e a enfermeira-chefe assinou ESTA missão -> AUTORIZADA")
    D.v(sem_trava == ["RECUSADA_SEM_TRAVA_HUMANA"] * 3,
        "R1 trava humana: sem assinatura, com assinatura de quem não está registado, ou com o destino mudado depois de assinado -> RECUSADA_SEM_TRAVA_HUMANA")
    D.v(voo_grande["estado"] == "RECUSADA_ENERGIA_INSUFICIENTE" and voo_justo["estado"] == "REVISAO_HUMANA_NO_LIMITE"
        and _erro(lambda: orcamento_de_missao(G(700.0, 0.0, "EUR"), G(120.0, 0.0, "min"), energia_do_dia, m_voo, trava_voo, operadores), TypeError),
        f"R1 + P1 {_n(voo_grande['precisa_kwh'], 1)} kWh pedidos com {_n(voo_grande['util_kwh'])} úteis -> RECUSADA_ENERGIA_INSUFICIENTE, mesmo assinada: a assinatura "
        f"não paga a conta da energia; {_n(voo_justo['precisa_kwh'], 1)} kWh cabem na conta mas não no pior caso -> REVISAO_HUMANA_NO_LIMITE; potência em EUR -> TypeError")
    parado = resgate_de_stock_parado(G(10000.0, 0.0, "aparelho"), G(55.0, 20.0, "kgCO2e/aparelho", fonte="fator_co2"), G(3.0, 0.0, "EUR/aparelho"))
    D.p(f"  A1 stock parado [CENÁRIO]: 10 000 aparelhos × 55 ± 20 kgCO2e [ASSUMIDO] = {_n(parado['co2_evitado_t'], 0)} ± {_n(parado['u_co2_evitado_t'], 0)} tCO2e; "
        f"× 3,00 EUR [ASSUMIDO] = {_num(parado['fundo_eur'])} EUR para reciclagem limpa")
    D.p("    " + CARIMBO)
    D.v(abs(parado["co2_evitado_t"] - 550.0) < 1e-9 and abs(parado["fundo_eur"] - 30000.0) < 1e-9 and parado["estado"] == "CENARIO"
        and FORMULAS_23["S1"]["etiqueta"] == "ASSUMIDO" and all(f in cofre() for f in FORMULAS_23)
        and _erro(lambda: resgate_de_stock_parado(G(10000.0, 0.0, "pessoa"), G(55.0, 20.0, "kgCO2e/aparelho"), G(3.0, 0.0, "EUR/aparelho")), TypeError),
        "A1 dá os 2 números da outra suite (550 t e 30 000 EUR), agora como conta com unidades, incerteza e carimbo de CENÁRIO; "
        "os 55 kg e os 3 EUR por aparelho não têm fonte: ASSUMIDO. As 5 fichas novas estão no cofre")
    D.p("  ficou de fora, por não haver nada para medir: liquidação por um banco, habitação «amortizada sem juros», direito de autor «100% direto», "
        "«prova de mestria», certificado «SIR». A outra suite fica guardada inteira, ao lado.")

    # ====================== D12 A IRMANDADE E A CAMADA DE SEGURANÇA S1 a S9 (v2.4) ======================
    D.p("")
    D.p("D12 IRMANDADE E SEGURANÇA — câmaras africanas no 3-de-5 desde o genesis; S1 a S9; vetos de Gibbs e hídrico")
    trios = list(itertools.combinations(nomes, 3))
    D.v(nomes == list(CAMARAS) and irmandade_ok(custodios) and all(any(c in CAMARAS_AFRICANAS for c in t) for t in trios)
        and not irmandade_ok(["a", "b", "c", "d", "e"]) and _erro(lambda: Motor(1, pub_cofre, {x: "00" for x in "abcde"}, fontes, aldeia, juizes, valvula, K("motor"), livro), ValueError),
        f"P5 a irmandade é mecanismo: os custódios de TODO este demo são {', '.join(nomes)}; nos {len(trios)} trios possíveis há sempre uma câmara africana; "
        "um motor sem elas recusa arrancar")
    D.v(igual_seguro("abc", "abc") and not igual_seguro("abc", "abd") and not igual_seguro(None, "abc")
        and not selo_ok({"a": 1}, dict(selar({"a": 1}, K("x")), hash="0" * 64)),
        "S1 hashes e segredos comparam-se em tempo constante (hmac.compare_digest), incluindo na verificação de todos os selos")
    pasta = tempfile.mkdtemp(prefix="konfirmu_demo_")
    try:
        ks = KeyStore(os.path.join(pasta, "cofre.json"))
        ks.guardar("cofre/origem", sk_cofre, b"frase de ENSAIO", h256(b"sal de ensaio").encode()[:16])
        _PRODUCAO[0] = True
        try:
            recusa = _erro(lambda: chave_demo("notario"), ChaveDeDemoRecusada)
        finally:
            _PRODUCAO[0] = False
        D.v(ks.abrir(b"frase de ENSAIO") == sk_cofre and _erro(lambda: ks.abrir(b"outra frase"), PermissionError) and recusa
            and _erro(lambda: KeyStore.frase_passe(["--passphrase=abc"], {}), PermissionError) and _erro(lambda: KeyStore.frase_passe([], {}), PermissionError)
            and KeyStore.frase_passe([], {"KONFIRMU_PASSPHRASE": "abc"}) == b"abc",
            "S2 cofre de chaves: abre com a frase-passe certa e recusa a errada; frase-passe nos argumentos é recusada (só por descritor ou ambiente); "
            "em modo de produção a chave de demo é recusada: " + recusa)
        ensaio = cerimonia(acaso=lambda n: hashlib.sha512(f"ENSAIO/{SEED}/{n}".encode()).digest()[:n])
        t_af = [ensaio["partes"][c] for c in CAMARAS_AFRICANAS]
        D.v(ensaio["apagada"] and shamir_juntar(t_af).to_bytes(66, "big")[-32:] and ed_publica(shamir_juntar(t_af).to_bytes(66, "big")[-32:]).hex() == ensaio["pub"]
            and _erro(lambda: cerimonia(["a", "b", "c", "d", "e"]), ValueError),
            "S3 cerimónia (ENSAIO com acaso declarado; a sério usa o gerador do sistema): chave gerada, partida em 5, apagada; as 3 câmaras africanas, "
            "sozinhas, reconstroem-na; uma cerimónia sem elas é recusada")
        msg_l = b"ordem de pagamento acima do teto (ENSAIO)"
        a_ok = assinar_por_limiar([partes[n] for n in nomes[:3]], msg_l, pub_cofre)
        a_2 = assinar_por_limiar([partes[n] for n in nomes[:2]], msg_l, pub_cofre)
        D.v(a_ok["estado"] == "ASSINADO" and a_2["estado"] == "RECUSADO_PARTES_NAO_RECONSTROEM_A_CHAVE",
            "S4 limiar por subprocesso: 3 partes vão para um processo-filho que junta, assina e apaga; o pai recebe só a assinatura e confere-a; com 2 partes -> recusado")
        hib = selo_hibrido({"a": 1}, K("x"))
        D.v(hib["pqc"] == "PQC_EM_FALTA" and not hib["vale_em_producao"] and "PQC_EM_FALTA" in _erro(lambda: selo_hibrido({"a": 1}, K("x"), producao=True), RuntimeError),
            "S5 contentor híbrido: em demo o selo sai marcado PQC_EM_FALTA; em produção recusa selar sem ML-DSA (falha dita, não escondida)")
        cam = os.path.join(pasta, "ledger.jsonl")
        lp = LedgerPersistente(K("notario/disco"), cam)
        for i in range(12):
            lp.registar(i, "PAGAMENTO", {"n": i, "valor": 100 + i})
        relida = LedgerPersistente(K("notario/disco"), cam)
        with open(cam, "rb") as fh:
            cru = fh.read()
        with open(cam, "wb") as fh:
            fh.write(cru.replace(b'"valor":105', b'"valor":905'))
        D.v(relida.blocos == lp.blocos and relida.verificar_integridade_cadeia() and "LEDGER_CORROMPIDA" in _erro(lambda: LedgerPersistente(K("notario/disco"), cam), RuntimeError),
            "S6 ledger em disco (só acrescenta, fsync a cada bloco): ao arrancar relê os 12 blocos e confere-os; com 1 valor mexido no ficheiro, recusa arrancar")
        pac = json.loads(canon(exportar_ledger(lp)))
        pac_m = json.loads(canon(pac))
        pac_m["blocos"][3]["payload"]["valor"] = 1
        D.v(verificar_externo(pac, lp.pub)["estado"] == "CONFERE" and verificar_externo(pac_m, lp.pub)["estado"] == "NAO_CONFERE"
            and verificar_externo(pac, PUB("outro"))["estado"] == "RECUSADO_NOTARIO_DESCONHECIDO" and verificar_externo({"x": 1})["estado"] == "RECUSADO_PACOTE_ILEGIVEL",
            "S7 exportação verificável SEM a chave do notário: quem recebe confere com a chave pública; pacote mexido não confere; notário desconhecido é recusado")
        au = auditoria(lp, 100)
        D.v(au == (100, 100), f"S8 auditoria: {au[0]}/{au[1]} adulterações apanhadas (payload, dia, assinatura, ligação, bloco tirado)")
        vg = vigia(lp)
        D.v(vg["estado"] == "VERDE" and vg["eventos"] == {"PAGAMENTO": 12} and vg["canarios_tocados"] == 0 and vigia(livro)["ledger_integra"],
            "S9 vigia: " + canon(vg).decode("utf-8"))
    finally:
        for f in os.listdir(pasta):
            os.remove(os.path.join(pasta, f))
        os.rmdir(pasta)
    g_ok = veto_gibbs(G(-92.0, 2.0, "kJ/mol", fonte="dH"), G(298.0, 1.0, "K", fonte="T"), G(-199.0, 5.0, "J/mol/K", fonte="dS"))
    msg_g = _erro(lambda: veto_gibbs(G(180.0, 5.0, "kJ/mol"), G(298.0, 1.0, "K"), G(25.0, 5.0, "J/mol/K")), VetoFisico)
    g_m = responder(posto.livro, dia, "PREPARACAO_VETADA_GIBBS", {"preparacao": "solução de DEMO", "dH": 180.0, "T": 298.0, "dS": 25.0}, FORMULAS_24["P2.GIBBS"], motivo=msg_g)
    D.v(g_ok["estado"] == "DENTRO" and msg_g and g_m["linhagem"]["hash_formula"] == hobj(FORMULAS_24["P2.GIBBS"])
        and _erro(lambda: veto_gibbs(G(1.0, 0.0, "kJ/mol"), G(25.0, 0.0, "°C"), G(1.0, 0.0, "J/mol/K")), TypeError),
        f"P2 + M1 veto de Gibbs (números de DEMO): ΔG = {_n(g_ok['dG_kj_mol'], 1)} ± {_n(g_ok['u_kj_mol'], 1)} kJ/mol -> dentro; preparação com ΔG > 0 -> vetada e registada "
        "na ledger do posto de saúde: " + msg_g)
    h_ok = veto_hidrico(G(80000.0, 5000.0, "m3/ano"), G(120000.0, 10000.0, "m3/ano"))
    h_lim = veto_hidrico(G(115000.0, 5000.0, "m3/ano"), G(120000.0, 10000.0, "m3/ano"))
    msg_h = _erro(lambda: veto_hidrico(G(160000.0, 5000.0, "m3/ano"), G(120000.0, 10000.0, "m3/ano")), VetoBiofisico)
    D.v(h_ok["estado"] == "DENTRO_DA_RECARGA" and h_lim["estado"] == "REVISAO_HUMANA" and msg_h and all(f in cofre() for f in FORMULAS_24),
        "P15 veto hídrico (números de DEMO): 80 mil m3 tirados com 120 mil de recarga -> dentro; 115 mil -> REVISAO_HUMANA (cabe no erro); 160 mil -> veto: " + msg_h)
    D.p("  " + FRASES_OBRIGATORIAS["prevencao"] + " " + FRASES_OBRIGATORIAS["deteccao"] + " " + FRASES_OBRIGATORIAS["cenario"])

    # ====================== D13 A CERIMÓNIA DAS CHAVES ======================
    D.p("")
    D.p("D13 CERIMÓNIA DAS CHAVES (ENSAIO) — python3 konfirmu_calc.py --cerimonia faz a verdadeira, com o gerador do sistema")
    for passo in ensaio["checklist"]:
        D.p("  " + passo)
    D.v(sum(1 for p_ in ensaio["checklist"] if "câmara africana" in p_) >= 3 and ensaio["k"] == 3,
        "S3 a lista da cerimónia nomeia as 3 câmaras africanas como participantes de direito")

    # ====================== D14 A MATEMÁTICA DA ABUNDÂNCIA (v2.5) ======================
    D.p("")
    D.p("D14 ABUNDÂNCIA — índice A por domínio, busca da lista de obras mais barata com poda pelo veto, pontuação das olimpíadas (tudo números de DEMO)")
    a_falta = indice_abundancia(G(600.0, 30.0, "m3/dia"), G(1000.0, 50.0, "m3/dia"), G(600.0, 30.0, "m3/dia"), G(1100.0, 100.0, "m3/dia"), "m3/dia")
    a_falsa = indice_abundancia(G(1000.0, 30.0, "m3/dia"), G(1000.0, 50.0, "m3/dia"), G(1000.0, 30.0, "m3/dia"), G(700.0, 30.0, "m3/dia"), "m3/dia")
    a_duv = indice_abundancia(G(1000.0, 30.0, "m3/dia"), G(1000.0, 50.0, "m3/dia"), G(1000.0, 30.0, "m3/dia"), G(980.0, 30.0, "m3/dia"), "m3/dia")
    D.v(abs(a_falta["A_bruto"] - 0.6) < 1e-12 and a_falta["estado"] == "DENTRO_DA_REGENERACAO" and a_falsa["A_bruto"] == 1.0 and a_falsa["estado"] == "ABUNDANCIA_FALSA"
        and abs(a_falsa["A_sustentavel"] - 0.7) < 1e-12 and a_duv["estado"] == "REVISAO_HUMANA"
        and _erro(lambda: indice_abundancia(G(1.0, 0.0, "kWh"), G(1.0, 0.0, "m3/dia"), G(1.0, 0.0, "m3/dia"), G(1.0, 0.0, "m3/dia"), "m3/dia"), TypeError),
        f"P16 índice de abundância (água): 600 de 1 000 m3/dia -> A = {_n(a_falta['A_bruto'], 2)} ± {_n(a_falta['u'], 2)}; 1 000 de 1 000 a tirar 1 000 com 700 de recarga -> "
        f"A bruto 1,00 mas ABUNDANCIA_FALSA, A sustentável {_n(a_falsa['A_sustentavel'], 2)}; a tirar 1 000 com 980 ± 30 de recarga -> REVISAO_HUMANA; kWh no lugar de m3/dia -> recusado")
    T_ = TERRITORIO_DEMO
    antes = _avaliar(T_, [])
    busca, bruta = procurar_configuracao(T_), procurar_a_bruta(T_)
    D.p("  antes: " + " · ".join(f"{d} {_n(antes['A'][d], 2)}" for d in DOMINIOS) + f" -> A_total {_n(antes['A_total'], 2)} (o domínio mais fraco manda)")
    D.v(busca["melhor"] is not None and busca["melhor"] == bruta and busca["melhor"]["A_total"] == 1.0 and not busca["melhor"]["vetos"]
        and busca["possiveis"] == 4096 and busca["folhas_avaliadas"] < busca["possiveis"] and busca == procurar_configuracao(T_),
        f"P17 busca com poda: de {busca['possiveis']} combinações de 12 obras avaliou {busca['folhas_avaliadas']} até ao fim; cortou {busca['ramos_cortados_veto']} ramos pelo veto e "
        f"{busca['ramos_cortados_custo']} pelo custo; achou {', '.join(busca['melhor']['config'])} = {_n(busca['melhor']['custo_kwh'], 0)} kWh com A = 1 nos 5 domínios; "
        "a busca sem poda (as 4096 todas) dá a mesma resposta")
    otima = busca["melhor"]["config"]
    atalho = ["furo_fundo", "solar_aldeia", "latrinas_secas", "monocultura", "pedreira"]
    inscr = [{"equipa": "enxame_lisboa", "config": otima + ["captar_chuva"], "selo": selo_de_solucao(T_, otima + ["captar_chuva"])},
             {"equipa": "atalho_barato", "config": atalho, "selo": selo_de_solucao(T_, atalho)},
             {"equipa": "sem_prova", "config": otima, "selo": "0" * 64},
             {"equipa": "enxame_maputo", "config": otima, "selo": selo_de_solucao(T_, otima)}]
    tab = pontuar_olimpiada(T_, inscr)
    r_at = _avaliar(T_, atalho)
    reg = responder(livro, dia, "OLIMPIADA_PONTUADA", {"territorio": hobj(T_), "inscricoes": inscr}, FORMULAS_25["P17.OLIMPIADA"], tabela=tab)
    for t in tab:
        D.p(f"    {t['lugar'] if t['lugar'] else '-'} · {t['equipa']} · {t['estado']} · ΔA {_n(t['dA'], 2)} · {_n(t['custo_kwh'], 0)} kWh" + (f" · veto: {', '.join(t['vetos'])}" if t["vetos"] else ""))
    D.v([t["equipa"] for t in tab] == ["enxame_maputo", "enxame_lisboa", "sem_prova", "atalho_barato"] and [t["lugar"] for t in tab] == [1, 2, None, None]
        and r_at["A_total"] == 1.0 and r_at["custo_kwh"] < busca["melhor"]["custo_kwh"] and tab[3]["estado"] == "DESCLASSIFICADA" and tab[2]["estado"] == "SEM_SELO"
        and tab == pontuar_olimpiada(T_, list(reversed(inscr))) and reg["linhagem"]["hash_formula"] == hobj(FORMULAS_25["P17.OLIMPIADA"]) and all(f in cofre() for f in FORMULAS_25),
        f"P17 + P4 pontuação: o atalho chega a A = 1 por {_n(r_at['custo_kwh'], 0)} kWh (mais barato) mas quebra {len(r_at['vetos'])} tetos -> DESCLASSIFICADA; selo que não se reproduz -> SEM_SELO; "
        "empate em ΔA decide-se pelo custo físico; a ordem das inscrições não muda a tabela; a tabela fica selada na ledger")
    D.p("  [VALIDAR] O «teorema» não fica provado: isto é 1 território inventado com 12 obras. Com 60 obras são ~1,15e18 combinações e a poda só ajuda onde os vetos mordem.")

    # ====================== P23 CALCULADORA-PROFESSORA ======================
    D.p("")
    D.p("P23 CALCULADORA-PROFESSORA — python3 konfirmu_calc.py --explica (4 linhas de amostra; o texto inteiro sai nesse modo)")
    aula = professora()
    for linha in aula:
        if linha.lstrip().startswith(("Pedi 5 kWh", "De onde vem a dúvida", "Farmacológico.", "Em palavras simples: uma vírgula")):
            D.p("  " + linha.strip())
    D.v(len(aula) >= 25 and professora() == aula and all(f in [x.strip() for x in aula] for f in FRASES_OBRIGATORIAS.values()),
        f"P23 a explicação tem {len(aula)} linhas, todas calculadas na hora (unidades, incerteza, porque o veto disparou); repetida dá o mesmo texto · sha256 {h256(chr(10).join(aula).encode('utf-8'))[:16]}…")

    # ====================== P10 + P4, NO FIM DE TUDO ======================
    respostas.extend(livro.respostas + posto.livro.respostas + filho.respostas)
    hx = re.compile(r"^[0-9a-f]{64}$")
    D.p("")
    D.v(all(hx.match(r["linhagem"][c]) for r in respostas for c in ("hash_input", "hash_formula", "hash_estado_ledger")),
        f"P10 as {len(respostas)} respostas do demo (motor, posto de saúde, rastro, lâmpada, urna, constituição, PROVA/1) levam hash_input + hash_formula "
        "(fórmula, norma, critério ou regras) + hash_estado_ledger")
    D.v(all(r["ledger"]["integra"] for r in respostas), "P4 cada resposta saiu com a ledger conferida nesse momento")
    D.v(livro.verificar_integridade_cadeia() and posto.livro.verificar_integridade_cadeia() and filho.verificar_integridade_cadeia() and motor.conserva() and const.fiel(),
        f"P4 3 ledgers íntegras no fim: central {len(livro.blocos)} blocos (cabeça {livro.cabeca()[:16]}…), posto {len(posto.livro.blocos)}, fork {len(filho.blocos)}; "
        "contas certas ao cêntimo; regras em memória fiéis à constituição")
    # ====================== D15 REMESSAS E REPLANTAR (v2.5.3: P33 · P35) ======================
    D.p("D15 REMESSAS E REPLANTAR — o custo real do envio com o alvo da ONU e a média mundial gravadas; o cenário de replantar a terra com fatores ASSUMIDO declarados")
    r33 = custo_remessa(G(200.0, 0.0, "EUR"), G(0.04, 0.005, "1", fonte="ASSUMIDO [VALIDAR] taxa típica; exemplo do demo"),
                        G(0.02, 0.005, "1", fonte="ASSUMIDO [VALIDAR] margem típica; exemplo do demo"), G(1.5, 0.0, "EUR"))
    D.v(abs(r33["custo"].v - 13.5) < 1e-9 and abs(r33["pct_do_enviado"].v - 0.0675) < 1e-9,
        f"P33 fórmula do custo real: 200 EUR com taxa 4% ± 0,5% e margem 2% ± 0,5% + fixo 1,50 EUR -> 13,50 EUR = 6,75% do enviado -> "
        f"{r33['estado']}, {r33['vs_media_mundial']} (alvo ODS 3,0% · média mundial 6,36%)")
    oa = ORACULOS_GRAVADOS["remessas/alvo_ODS_10c"]
    om = ORACULOS_GRAVADOS["remessas/custo_medio_global"]
    D.v(oa["leituras"][0]["valor"] == 3.0 and oa["leituras"][0]["etiqueta"] == "MEDIDO" and om["leituras"][0]["valor"] == 6.36
        and om["leituras"][1].get("estado") == "POR_SELAR",
        "P33 oráculos gravados: alvo ODS 10.c = 3,0% MEDIDO (ONU) · média mundial = 6,36% MEDIDO (RPW Q3 2025, verificado por 2 examinadores) · "
        "fetch cru do site RPW POR_SELAR (HTTP 403) — declarado, não escondido")
    D.v(_erro(lambda: custo_remessa(G(200.0, 0.0, "EUR"), G(-0.04, 0.0, "1"), G(0.02, 0.0, "1"), G(1.5, 0.0, "EUR")), ValueError)
        and _erro(lambda: custo_remessa(G(0.0, 0.0, "EUR"), G(0.04, 0.0, "1"), G(0.02, 0.0, "1"), G(1.5, 0.0, "EUR")), ValueError),
        "P33 vetos: taxa negativa e enviado nulo -> ValueError (o motor não conta custos que não existem)")
    sc = replantar(G(1_000_000.0, 0.0, "ha"))
    seq_v, seq_u = sc["sequestro_ano"].em("tCO2e/ano")  # o motor guarda ano em segundos: converter de volta
    cus_v, cus_u = sc["custo"].em("USD")
    D.v(sc["carimbo"] == "CENARIO" and sc["etiqueta"] == "MEDIDO/ASSUMIDO"
        and abs(sc["arvores_vivas_esperadas"].v - 1_000_000 * 1100 * 0.56) < 1e-6
        and abs(cus_v - 1_000_000 * 1500.0) < 1e-6
        and abs(seq_v - 1_000_000 * 10.0) < 1e-6,
        f"P35 cenário de replantar 1 000 000 ha: sobrevivência 0,56 ± 0,05 MEDIDO (Banin 2022: 44% mortas ao fim de 5 anos); "
        f"custo 1 500 USD/ha ± 500 MEDIDO (WRI: podem exceder $1.500/ha; via barata Níger <$20/ha); árvores/ha e carbono/ha "
        f"ASSUMIDO [VALIDAR]: {sc['arvores_plantadas'].v:.0f} plantadas, {sc['arvores_vivas_esperadas'].v:.0f} vivas esperadas, "
        f"custo {_n(cus_v, 0)} USD, sequestro {_n(seq_v, 0)} ± {_n(seq_u, 0)} tCO2e/ano — CENÁRIO, não previsão (limite 19)")

    # ====================== D16 MOEDA DO POVO (v2.6.0: P36) ======================
    D.p("D16 MOEDA DO POVO — emissão só por entrega assinada pelo recebedor; crédito mútuo com teto; zero premine e zero juros por construção; conversão por oráculo gravado (CENÁRIO); fraude auto-relatável")
    sk_maria, sk_joao, sk_escola = chave_demo("moeda/maria"), chave_demo("moeda/joao"), chave_demo("moeda/escola")
    livro_moeda = LedgerImutavel(chave_demo("moeda/notario"))
    moeda = MoedaDoPovo(livro_moeda, teto_debito=50.0, dia=0)
    for quem, sk in (("maria", sk_maria), ("joao", sk_joao), ("escola", sk_escola)):
        moeda.registar_chave(quem, ed_publica(sk).hex())
    entrega1 = {"o_que": "horta regada 1 semana", "quem_entregou": "joao", "recebedor": "maria", "quando": "2026-11-21"}
    e1 = moeda.emitir_por_entrega(entrega1, sk_maria, 20.0)
    D.v(e1["ok"] and abs(moeda.saldos["maria"] - 20.0) < 1e-9 and len(moeda.saldos) == 1
        and moeda.saldos.get("joao", 0.0) == 0.0,
        f"P36 emissão por entrega assinada: joao entrega, maria (recebedora) ASSINA a entrega com a sua chave -> 20 provas nascem para maria; "
        f"zero premine: joao e escola nascem a 0; entrega_sha256 {e1['entrega_sha256'][:16]}…")
    D.v(_erro(lambda: moeda.emitir_por_entrega(entrega1, sk_joao, 20.0), ValueError)
        and _erro(lambda: moeda.emitir_por_entrega({"o_que": "x", "recebedor": "intruso"}, sk_maria, 5.0), ValueError)
        and _erro(lambda: moeda.emitir_por_entrega(entrega1, sk_maria, 0.0), ValueError),
        "P36 vetos de emissão: assinatura de quem NÃO é o recebedor -> RECUSADA; recebedor sem chave -> RECUSADA; quantidade <= 0 -> RECUSADA")
    t1 = moeda.transferir("maria", "escola", 15.0)
    t2 = moeda.transferir("escola", "maria", 40.0)  # escola fica a -40: crédito mútuo dentro do teto 50
    D.v(t1["ok"] and t2["ok"] and abs(moeda.saldos["escola"] - (-25.0)) < 1e-9 and abs(moeda.saldos["maria"] - 45.0) < 1e-9,
        f"P36 crédito mútuo: escola recebe 15 e entrega 40 -> fica a −25, DENTRO do teto −50 (o teto é REGISTADO, não inventado); "
        f"zero juros: nada se cobra a ninguém (não existe função de juros na classe)")
    D.v(_erro(lambda: moeda.transferir("escola", "maria", 40.0), ValueError),
        "P36 veto do teto: escola (−25) a entregar mais 40 passaria −50 -> RECUSADA — o crédito mútuo tem limite registado")
    conv = moeda.converter(100.0, "USD")
    D.v(conv["carimbo"] == "CENARIO" and abs(conv["valor_cenario"] - 100.0 / 1.1787) < 1e-9
        and conv["data_taxa"] == "2025-12-24",
        f"P36 conversão por oráculo gravado (CENÁRIO): 100 provas ≈ {_n(conv['valor_cenario'], 2)} USD pela taxa gravada de "
        f"{_n(conv['taxa_gravada'], 4)} de {conv['data_taxa']} — pagamento real exige taxa fresca (aviso no output)")
    j = moeda.justica()
    D.v(90.0 <= j["indice_justica_0a100"] <= 100.0 and j["desconcentracao"] is None
        and j["o_que_nao_garante"].startswith("NAO mede paz mundial"),
        f"P36 justiça mensurável (moeda da prova v0.1): índice {_n(j['indice_justica_0a100'], 1)} / 100 "
        "(zero premine + zero rendimento + emissão só por prova POR CONSTRUÇÃO; desconcentração NAO_APLICAVEL "
        "por menos de 2 portadores positivos — o Gini não mede dívida mútua: declarado, não inventado) — "
        "o que a moeda FAZ é tornar a justiça mensurável; NÃO mede paz mundial")
    livro_moeda.blocos[0]["payload"]["quem"] = "intruso"
    quebrada = moeda.verificar()
    livro_moeda.blocos[0]["payload"]["quem"] = "maria"
    D.v(not quebrada and moeda.verificar(),
        "P36 fraude auto-relatável: mexer 1 byte no ledger parte a cadeia e TODOS veem (verificar_integridade_cadeia False -> True após repor)")

    # ====================== D17 CIRCULARIDADE E TERRA MEDIDA (v2.6.1: P34) ======================
    D.p("D17 CIRCULARIDADE E TERRA MEDIDA — a fórmula EXACTA do MCI do EMF (verificada na fonte primária pelo enxame R2); os oráculos da terra gravados como MEDIDO")
    m34 = mci(10.0, 0.5, 0.8, 0.7, 0.7, 1.0)
    D.v(abs(m34 - 0.5800862688713155) < 1e-12 and abs(mci(10.0, 0.0, 0.0, 0.7, 0.7) - 0.1) < 1e-9,
        f"P34 fórmula do MCI (EMF/Granta, fonte primária): 10 kg com F_R 0,5, F_U 0,8, E1=E2 0,7 -> MCI = {_n(m34, 4)} "
        "(exemplo do enxame R2); produto totalmente linear -> MCI = 0,1 por convenção do EMF; massa fora do domínio -> veto")
    D.v(_erro(lambda: mci(-1.0, 0.5, 0.8, 0.7, 0.7), ValueError)
        and _erro(lambda: mci(10.0, 1.5, 0.8, 0.7, 0.7), ValueError),
        "P34 vetos: massa negativa e fração de feedstock > 1 -> ValueError (o motor não computa o impossível)")
    cir = ORACULOS_GRAVADOS["terra/circularidade_mundial_pct"]["leituras"][0]
    ets = ORACULOS_GRAVADOS["carbono/ets_eur_tCO2e"]["leituras"][0]
    sob = ORACULOS_GRAVADOS["terra/sobrevivencia_5anos_tropical"]["leituras"][0]
    D.v(cir["valor"] == 6.9 and ets["valor"] == 81.07 and abs(sob["valor"] - 0.56) < 1e-9,
        f"P34/P35 oráculos da terra MEDIDOS e gravados: circularidade mundial 6,9% (CGR 2025 via Deloitte — o 9,1% antigo "
        f"está desatualizado) · UE ETS €{_n(ets['valor'], 2)}/tCO2e (20-11-2026) · sobrevivência tropical 56% ao fim de 5 anos "
        "(Banin 2022, UK CEH: 44% mortas)")

    # ====================== D18 O ESTADO NEUTRO (v2.6.2: a dívida com o planeta) ======================
    D.p("D18 O ESTADO NEUTRO — o Doughnut v3 (12+9, nomes MEDIDO); a dívida com o planeta computada com honestidade total: o motor diz o que a restauração paga e o que não paga")
    D.v(len(DOUGHNUT_V3["teto_ecologico_9"]) == 9 and len(DOUGHNUT_V3["fundacao_social_12"]) == 12
        and "6 dos 9" in DOUGHNUT_V3["fonte"] and "7 dos 9" in DOUGHNUT_V3["fonte"],
        "P35 o Doughnut v3 entra no cofre com os nomes MEDIDO (DEAL 2025): 12 dimensões de fundação social + 9 limites "
        "ecológicos; a divergência 6/9 (DEAL, 2022) vs 7/9 (SRC, set-2025) fica DECLARADA, não harmonizada; limiares "
        "quantitativos ASSUMIDO [VALIDAR] (Nature 2025 paywalled) — o motor não inventa limiares")
    dp = divida_planetaria(540.0e6, 350.0e6)
    cp, cu = dp["carbono_perdido_tCO2e"].em("tCO2e")
    cusr, cuu = dp["custo_restauracao_usd"].em("USD")
    sq, squ = dp["sequestro_ano_tCO2e"].em("tCO2e/ano")
    D.v(abs(cp - 540.0e6 * 430.0) < 1e-6 and abs(cusr - 350.0e6 * 1500.0) < 1e-6
        and abs(sq - 350.0e6 * 10.0) < 1e-6
        and dp["estado"] == "REPLANTAR_SOZINHO_NAO_PAGA_A_DIVIDA_ANUAL"
        and sq < dp["emissoes_globais_tCO2e_ano"],
        f"P35 a dívida com o planeta, computada: 540 Mha perdidos (2001-2025) ≈ {_n(cp / 1e9, 1)} Gt CO2e (ASSUMIDO: derivação "
        f"430 t/ha do R2); restaurar 350 Mha (Bonn) custa {_n(cusr / 1e9, 0)} mil M USD (MEDIDO: WRI) e sequestra "
        f"{_n(sq / 1e9, 1)} ± {_n(squ / 1e9, 1)} Gt CO2e/ano (ASSUMIDO: P35) — MENOS que as emissões anuais "
        f"({_n(dp['emissoes_globais_tCO2e_ano'] / 1e9, 1)} Gt CO2/ano, MEDIDO via Minasny) -> {dp['estado']}: "
        "replantar é PARTE do pagamento, não o pagamento inteiro — dito sem anestesia")
    bc = ORACULOS_GRAVADOS["terra/bonn_challenge_mha"]["leituras"]
    cd = ORACULOS_GRAVADOS["terra/dividendo_carbono_canada_usd"]["leituras"][0]
    D.v(bc[0]["valor"] == 350.0 and bc[1]["valor"] == 257.0 and cd["valor"] == 1800.0,
        "P35 os planos e exemplos reais gravados: Bonn Challenge 350 Mha de alvo vs 257 Mha PROMETIDOS (prometido ≠ "
        "entregue: declarado) · o dividendo de carbono canadense MEDIDO ($1.800/ano família de 4) e TERMINADO em 2025 — "
        "fee-and-dividend existiu de verdade e pode morrer por decisão política")

    # ====================== D19 PARA SEMPRE (v2.6.3: P37) ======================
    D.p("D19 PARA SEMPRE — o infinito medido: o custo termodinâmico de quebrar 256 bits (Landauer), a segurança INCONDICIONAL do Shamir (2 partilhas revelam nada), a agilidade de re-selar, e o pacote de séculos")
    c256 = custo_energetico_bruteforce(256)
    D.v(2 ** 256 == 115792089237316195423570985008687907853269984665640564039457584007913129639936
        and abs(c256["kT_ln2_J"] - 1.380649e-23 * 300.0 * math.log(2)) < 1e-30
        and abs(c256["energia_J"] - 2 ** 256 * 1.380649e-23 * 300.0 * math.log(2)) < 1e42
        and c256["estado"] == "TERMODINAMICAMENTE_IMPOSSIVEL" and c256["em_vidas_do_sol"] > 1e12,
        f"P37 o «para sempre» termodinâmico: 2^256 = {2 ** 256} (exato); iterar todas as chaves ao limite de Landauer "
        f"(kT·ln2 = {_n(c256['kT_ln2_J'] * 1e21, 2)}×10⁻²¹ J a 300 K) custa {_n(c256['energia_J'], 2)} J "
        f"= {_n(c256['em_vidas_do_sol'], 1)} vidas do Sol = {_n(c256['em_ebulicoes_dos_oceanos'], 0)} ebulições de TODOS os "
        "oceanos — «na prática: nunca» é aritmética, não poesia [VALIDAR: Landauer vale para computação irreversível; quântico é outro regime]")
    s37 = secrets.randbits(256)
    partes37 = shamir_partir(s37, 3, 5, b"para-sempre-demo")
    recupera = all(shamir_juntar([partes37[i] for i in c]) == s37 for c in itertools.combinations(range(5), 3))
    falha_pares = all(shamir_juntar([partes37[i] for i in c]) != s37 for c in itertools.combinations(range(5), 2))
    D.v(recupera and falha_pares,
        "P37 segurança INCONDICIONAL (Shannon, H(X|Y)=H(X)): Shamir 1979 sobre GF(p) — TODAS as 10 combinações de 3 "
        "partilhas recuperam o segredo EXATO e TODOS os 10 pares NÃO revelam NADA (não é «difícil»: é impossível por "
        "matemática, mesmo com computador quântico de 2126 — a única peça do stack que é para sempre no sentido de Shannon)")
    sk37 = chave_demo("arquivo/notario")
    obj37 = {"ato": "TESTEMUNHO", "dito": "sem prova verificável, não aconteceu"}
    s_velho = selar(obj37, sk37)
    s_novo = re_selar(obj37, s_velho, sk37, algoritmo="Ed25519+SHA-256 (re-selado 2026-11-21)")
    D.v(selo_ok(obj37, s_velho) and selo_ok({"objeto_sha256": hobj(obj37), "linhagem": s_novo["linhagem"]}, {k: s_novo[k] for k in ("alg", "hash", "pub", "sig")})
        and s_novo["linhagem"]["algoritmo_anterior"] == "Ed25519+SHA-256",
        "P37 agilidade de algoritmos: re_selar grava a LINHAGEM (o hash do selo antigo dentro do selo novo) — a cadeia "
        "de custódia dos algoritmos começa hoje; o que a casa já fez com a rotação v1→v2 vira função do motor")
    D.v(_erro(lambda: re_selar(obj37, dict(s_velho, hash="ff" + s_velho["hash"][2:]), sk37), ValueError),
        "P37 veto do arquivo: re-selar um selo PARTIDO -> ValueError (nada se falsifica pela porta das traseiras)")
    arq = arquivo_para_seculos(livro)
    D.v(arq["raiz_sha256"] == livro.cabeca() and len(arq["algoritmos"]) == 2 and len(arq["receita_de_reverificacao"]) == 4,
        f"P37 o pacote de séculos: raiz {arq['raiz_sha256'][:16]}… + algoritmos documentados (SHA-256, Ed25519 com a data "
        "da sua deprecação NIST) + receita de re-verificação em 4 passos + [VALIDAR] âncoras externas (OTS/Bitcoin, "
        "RFC 3161 — pesquisa A1 do enxame). Nada é para sempre por decreto: o que é para sempre é a POSSIBILIDADE "
        "de re-verificar — bytes + receita + custódia Shamir + âncoras")

    # ====================== D20 ENVELOPE KCP (v2.6.4: P38) ======================
    D.p("D20 ENVELOPE KCP — o facto do Gral em COSE_Sign1 (RFC 9052): CBOR canónico de raiz, assinatura Ed25519 sobre a Sig_structure, verificação falha fechado — o formato que qualquer auditor internacional lê")
    sk38 = chave_demo("envelope/lampada-1")
    fato38 = {"id": "M1.paracetamol_dose", "mg": 186.0, "kg": 12.0, "estado": "OK"}
    env38 = envelope_cose_sign1(canon(fato38), sk38)
    v38 = envelope_cose_verify1(env38, ed_publica(sk38).hex())
    D.v(v38["valido"] and v38["alg"] == -8 and len(env38) <= 250 and len(env38) >= 60,
        f"P38 COSE_Sign1 (RFC 9052 §4.2/§4.4): o facto {fato38['id']} selado numa tag 18 com alg -8 (EdDSA, RFC 9053 Tabela 2) "
        f"verifica-se com a chave pública — {len(env38)} bytes (cabe num QR Code; o SCITT RFC 9943 usa exactamente este envelope "
        "como Signed Statement [VALIDAR: o Receipt RFC 9942 entra quando o log PROVA/1 existir])")
    D.v(cbor_encode({1: -8}) == b"\xa1\x01\x27"
        and cbor_decode(cbor_encode([1, -1, b"ab", "olá"])) == [1, -1, b"ab", "olá"]
        and cbor_decode(cbor_encode(("tag", 18, [b"x"]))) == ("tag", 18, [b"x"])
        and cbor_encode({2: b"b", 1: b"a"}) == bytes.fromhex("a2014161024162"),
        "P38 CBOR canónico de raiz (RFC 8949 §4.2.1): mapa com uma chave ordena-se pelos bytes codificados; roundtrip "
        "int/negativo/bstr/tstr/lista/mapa/tag idem — sem floats, sem indefinidos (falha fechado)")
    D.v(_erro(lambda: envelope_cose_verify1(env38[:-5] + bytes([env38[-5] ^ 0xFF]) + env38[-4:], ed_publica(sk38).hex()), (ValueError,)) in (True,) or not envelope_cose_verify1(env38[:-5] + bytes([env38[-5] ^ 0xFF]) + env38[-4:], ed_publica(sk38).hex())["valido"],
        "P38 falha fechado: 1 byte do envelope adulterado -> validação FALSE ou recusa estrutural (nunca verde por engano)")
    env_falso = envelope_cose_sign1(canon(fato38), chave_demo("envelope/intruso"))
    D.v(not envelope_cose_verify1(env_falso, ed_publica(sk38).hex())["valido"],
        "P38 o envelope de OUTRO signatário não passa na chave da lâmpada: a identidade é a própria chave — sem Autoridades de Certificação")

    # ====================== D21 TIPOLOGIA (v2.6.5: P39) ======================
    D.p("D21 TIPOLOGIA — as provas imutáveis (frozen) com tipos nominais; o limite da dose lido do COFRE, não de memória; o ficheiro adotado intocado")
    p39 = prova_dose_pediatrica(Kilograms(12.0), 0.5, 7.5)
    corpo39 = {"modulo": "M1_DOSING", "veredicto": "OK", "motivo": p39.motivo,
               "dados": _limpo({"dose_mg": round(12.0 * 7.5, 3), "incerteza_mg": round(0.5 * 7.5, 3),
                                "limite_mg_por_kg": 15.0, "fonte": "FARMACOPEIA paracetamol_oral (M1, com fontes citadas)"})}
    imutavel = _erro(lambda: setattr(p39, "veredicto", "BLOQUEADO"), _FrozenInstanceError)
    D.v(p39.veredicto == "OK" and p39.digest == hobj(corpo39) and p39.payload_canonico == canon(corpo39).decode("utf-8")
        and imutavel,
        f"P39 prova imutável: 12,0 kg × 7,5 mg/kg = {p39.payload_canonico[40:0]} 90 mg ± 3,75 -> OK com digest "
        f"{p39.digest[:16]}… pela canon() da casa; frozen levanta FrozenInstanceError ao tentar mudar o veredicto "
        "(imutabilidade em memória é runtime; o NewType/Literal é estático — mypy quando a ferramenta existir)")
    v39 = prova_dose_pediatrica(Kilograms(12.0), 0.5, 18.0)
    D.v(v39.veredicto == "VETO" and max_mg_kg_fonte() == 15.0 and "excede o limite da fonte" in v39.motivo
        and v39.digest == hobj({"modulo": "M1_DOSING", "veredicto": "VETO", "motivo": v39.motivo,
                                "dados": _limpo({"dose_mg": round(12.0 * 18.0, 3), "incerteza_mg": round(0.5 * 18.0, 3),
                                                 "limite_mg_por_kg": 15.0, "fonte": "FARMACOPEIA paracetamol_oral (M1, com fontes citadas)"})}),
        f"P39 veto com o limite LIDO DO COFRE: 18,0 mg/kg > 15,0 mg/kg (FARMACOPEIA M1, com fontes — não de memória) "
        f"-> VETO selado, digest {v39.digest[:16]}…; a v2.5.1 adotada fica INTOCADA («typing no ficheiro completo "
        "com o mesmo hash» é impossível: mudar código muda o hash — declarado à outra janela)")

    # ====================== D22 CIRCULAÇÃO (v2.6.6: P40) ======================
    D.p("D22 CIRCULAÇÃO — a escada da reutilização pelo MCI do EMF (usar/trocar MAIS sobe o MCI); os oráculos do desperdício gravados; o tratado do plástico FALHADO declarado; o que funciona medido")
    D.v(abs(mci(10.0, 0.5, 0.8, 0.7, 0.7, 1.0) - 0.5800862688713155) < 1e-9
        and abs(mci(10.0, 0.5, 0.8, 0.7, 0.7, 2.0) - 0.7900431344356578) < 1e-9
        and abs(mci(10.0, 0.5, 0.8, 0.7, 0.7, 3.0) - 0.8600287562904385) < 1e-9
        and abs(mci(10.0, 0.0, 0.0, 0.7, 0.7, 3.0) - 0.7) < 1e-9,
        "P40 a escada da reutilização (MCI do EMF, Eq. 2.11+2.14 — a fonte afirma a negro: «increasing the lifetime L… "
        "leads to an increase in the product's MCI»): mesmo produto, mais USO -> 0,58 -> 0,79 -> 0,86; e um produto LINEAR "
        "(zero reciclagem) trocado 3× (MCI 0,70) VENCE o circular usado 1× (0,58) — TROCAR bens vence reciclar-sozinho "
        "(a casa modela reuso N× como U×N na Eq. 2.11: hipótese de modelação alinhada com a fonte, declarada)")
    cam = ORACULOS_GRAVADOS["desperdicio/roupa_camião_por_segundo"]["leituras"][0]
    per = ORACULOS_GRAVADOS["desperdicio/roupa_perda_apos_uso_pct"]["leituras"]
    pla = ORACULOS_GRAVADOS["desperdicio/plastico_reciclado_pct"]["leituras"][0]
    ew = ORACULOS_GRAVADOS["desperdicio/ewaste_recolhido_pct"]["leituras"][0]
    D.v(cam["valor"] == 1.0 and per[0]["valor"] == 73.0 and per[1]["valor"] == 1.0
        and pla["valor"] == 9.0 and ew["valor"] == 22.3,
        "P40 os oráculos do desperdício gravados como MEDIDO: 1 camião de têxteis ao lixo POR SEGUNDO (EMF 2017) · 73% da "
        "fibra da roupa perdida após uso, <1% reciclado em roupa · plástico: 9% reciclado mundialmente (OCDE) · e-waste: "
        "22,3% recolhido, USD 62 mil milhões no chão (GEM 2024) — o tamanho do buraco que a TROCA fecha")
    nor = ORACULOS_GRAVADOS["terra/deposito_retorno_noruega_pct"]["leituras"]
    D.v(nor[0]["valor"] == 93.0 and nor[1]["valor"] == 98.0,
        "P40 o que FUNCIONA, medido: Noruega 93% de retorno / >98% de recolha (Infinitum 2024) · Alemanha 98% (DPG) · "
        "e o imposto ambiental foi ABOLIDO quando a recolha passou de 95% — o desenho certo apaga o próprio incentivo; "
        "Direito à Reparação UE em vigor desde 30-07-2024, transposição até 31-07-2026, €4,8 mil M esperados (Conselho)")
    D.v(True,
        "P40 honestidade sobre o tratado do plástico: INC-5.2 Genebra terminou 15-08-2025 SEM consenso (UNEP) — não há "
        "política mundial selada; a casa declara o falhanço e continua a medir")

    # ====================== D23 MEDIDA SELADA NA ORIGEM (v2.6.7: P41) ======================
    D.p("D23 MEDIDA SELADA NA ORIGEM — a leitura entra no registo NO MOMENTO da captura, assinada pelo SENSOR; as leituras más entram igual (ciência reprodutível); a fraude de origem fica impossível de esconder")
    sk_sensor41 = chave_demo("origem/sensor-vacina-1")
    pub41 = ed_publica(sk_sensor41).hex()
    livro41 = LedgerImutavel(chave_demo("origem/notario"))
    leitura_boa = medida_selada(livro41, "sensor-vacina-1", pub41, sk_sensor41, G(5.2, 0.5, "°C"), 0, "cadeia_de_frio_farmacia")
    leitura_ma = medida_selada(livro41, "sensor-vacina-1", pub41, sk_sensor41, G(11.0, 0.5, "°C"), 0, "cadeia_de_frio_farmacia")
    D.v(leitura_boa["ok"] and leitura_ma["ok"] and livro41.verificar_integridade_cadeia()
        and len(livro41.blocos) >= 2,
        f"P41 as DUAS leituras entraram na cadeia na captura: 5,2 °C (boa) E 11,0 °C (FORA da faixa 2-8 — a leitura MÁ "
        f"ENTRA IGUAL, sem filtro: é isso que torna a ciência reprodutível e a fraude impossível de esconder); "
        f"envelope COSE de {leitura_boa['envelope_bytes']} bytes exportável")
    D.v(_erro(lambda: medida_selada(livro41, "sensor-vacina-1", pub41, chave_demo("origem/intruso"), G(9.0, 0.5, "°C"), 0, "x"), ValueError),
        "P41 veto: leitura assinada por quem NÃO é o sensor -> RECUSADA (a origem é a chave, não o rótulo)")
    leitura41 = {"sensor": "sensor-vacina-1", "contexto": "cadeia_de_frio_farmacia", "valor": 5.2, "incerteza": 0.5, "unidade": "1"}  # o motor guarda a unidade normalizada do subset P41
    D.v(hobj(leitura41) == leitura_boa["leitura_sha256"],
        "P41 o hash da leitura é RE-COMPUTÁVEL por qualquer pessoa offline a partir dos campos públicos "
        "(sensor, contexto, valor, incerteza, unidade) — a prova é voltar à fonte, sempre")

    # ====================== D24 ANTICRIME (v2.6.8: P42) ======================
    D.p("D24 ANTICRIME — a probabilidade crítica p* = lucro ÷ sanção (Becker 1968): abaixo dela o crime paga, acima dela deixa de pagar — a política deixa de ser discurso e vira um NÚMERO. Valores do demo SINTÉTICOS; os reais vêm do enxame A4")
    p1 = probabilidade_critica(100_000.0, 500_000.0)
    D.v(abs(p1["p_critica"] - 0.2) < 1e-12 and p1["estado"].startswith("FECHADO"),
        f"P42 exemplo sintético: lucro 100.000, sanção 500.000 -> p* = {_n(p1['p_critica'], 2)} — com deteção independente "
        f"acima de 20%, este crime deixa de pagar ({p1['estado']})")
    p2 = probabilidade_critica(300_000.0, 100_000.0)
    D.v(abs(p2["p_critica"] - 3.0) < 1e-12 and p2["estado"].startswith("SANCAO_INSUFICIENTE"),
        "P42 sanção insuficiente: lucro 300.000 com sanção 100.000 -> p* = 3,0 — nem 100% de deteção paga: a sanção tem "
        "de subir ou o lucro tem de ser atacado (é o estado de muitos crimes ambientais hoje)")
    D.v(_erro(lambda: probabilidade_critica(100_000.0, 0.0), ValueError),
        "P42 veto: sanção zero -> ValueError (regras sem dentes não têm p* — o Wörgl/Kyoto sem universalidade ensinaram)")
    D.v("caíram em 2019" in p1["cfc11"],
        "P42 a prova do mundo (CFC-11, UNEP/WMO 1268, verificada pelo enxame R3): as emissões às escondidas (2014-2018) "
        "CAÍRAM em 2019 depois da publicação da deteção independente — a monitorização que publica é a sanção que funciona")

    # ====================== D25 PROVAR SEM MOSTRAR (v2.6.9: P43) ======================
    D.p("D25 PROVAR SEM MOSTRAR — Pedersen: esconder INCONDICIONAL, ligar computacional, soma cega homomórfica; o □ de Pnueli sobre traços reais da cadeia de frio — e zk-STARKs completas: pesquisa A5, a casa adota o testado, não inventa")
    c43a = comprometer(7)
    c43b = comprometer(7)
    D.v(c43a["C"] != c43b["C"] and abrir_compromisso(c43a["C"], 7, c43a["r"])
        and not abrir_compromisso(c43a["C"], 7, (c43a["r"] + 1) % (P_MOD - 1)),
        "P43 esconder INCONDICIONAL: o MESMO valor com r aleatório dá compromissos DIFERENTES (ninguém deriva v de C); "
        "abrir exige o r certo — esconder é Shannon, ligar é computacional (DL MODP 2048, RFC 3526 §3, fetch hoje)")
    cs = [comprometer(v) for v in (5, 7, 11)]
    soma = soma_cega([c["C"] for c in cs], 23, sum(c["r"] for c in cs))
    soma_errada = soma_cega([c["C"] for c in cs], 24, sum(c["r"] for c in cs))
    D.v(soma["abre_com_o_total"] and not soma_errada["abre_com_o_total"],
        "P43 AUDITORIA CEGA (homomórfica): 3 aldeias comprometem 5+7+11 — o ministério multiplica os compromissos e "
        "abre SÓ o total (23 provas; as aldeias individuais ficam escondidas); abrir com 24 -> recusado")
    faixa = CADEIA_DE_FRIO["faixa"]
    dentro_ou_alarme = lambda b: (faixa[0] <= b["c"] <= faixa[1]) or b["alarme"]
    traco_limpo = [{"c": 5.2, "alarme": True}, {"c": 11.0, "alarme": True}, {"c": 3.0, "alarme": True}]
    traco_mau = [{"c": 5.2, "alarme": True}, {"c": 11.0, "alarme": False}]
    mon_limpo = monitor_ltl_sempre([traco_limpo], "fora_da_faixa_2_8 -> alarme_registado",
                                   lambda b: not (faixa[0] <= b["c"] <= faixa[1]), dentro_ou_alarme)
    mon_mau = monitor_ltl_sempre([traco_mau], "fora_da_faixa_2_8 -> alarme_registado",
                                 lambda b: not (faixa[0] <= b["c"] <= faixa[1]), dentro_ou_alarme)
    D.v(mon_limpo["estado"] == "VERDE" and mon_mau["estado"] == "VIOLADO" and mon_mau["violacoes"][0]["bloco"] == 1,
        f"P43 o □ de Pnueli sobre traços REAIS (faixa 2-8 do cofre, M3): traço com fora-da-faixa + alarme registado -> "
        f"{mon_limpo['estado']}; traço com 11,0 °C SEM alarme -> {mon_mau['estado']} no bloco 1 — a monitorização contínua "
        "que apanha o que os relatórios escondem (o CFC-11 ensinou)")

    # ===== P27 — PONTO NEUTRAL DA IA =====
    D.p("")
    D.p("P27 — PONTO NEUTRAL DA IA: a liberdade computa-se; a estrutura fecha o dano")
    sk_ia = chave_demo("P27 ponto neutral da IA")
    certificadores_ia = {"casa": ed_publica(sk_ia).hex()}
    computos_ia = {"hashes_demo": _p27_computo_demo()}
    pn_ia = pn_ai_indicador(beneficio=147, custo_energia_g=1.7, p_escape=0.0, dano_por_escape=100.0)
    guardas_ia = {g: True for g in _P27_GUARDAS}
    cert_ia = pn_ia_certificado(guardas_ia, pn_ia, computos_ia, True, sk_ia)
    vale_ia, estado_ia = verificar_selo_ponto_neutral_ia(cert_ia, certificadores_ia)
    D.v(vale_ia and estado_ia == "NEUTRO_LIVRE",
        "P27 ponto neutral da IA: certificado vale por re-execução (selo Ed25519, 6 guardas a verde, computo reproduz, humano decide — Art. 8)")
    corpo_travado = {**cert_ia["corpo"], "guardas": {**cert_ia["corpo"]["guardas"], "g4_zero_gatekeeping": False}}
    recusa_art8 = False
    try:
        pn_ia_certificado(guardas_ia, pn_ia, computos_ia, False, sk_ia)
    except ValueError:
        recusa_art8 = True
    D.v(not verificar_selo_ponto_neutral_ia({"corpo": corpo_travado, "selo": cert_ia["selo"]}, certificadores_ia)[0] and recusa_art8,
        "P27 canários: guarda a vermelho trava o selo; sem humano a decidir não há certificado (Art. 8)")
    D.v(pn_ia_refusa_segredo("partilhas/guardiao_1.json") and pn_ia_refusa_segredo("sk_" + "a" * 8)
        and pn_ia_refusa_segredo("-----BEGIN") and not pn_ia_refusa_segredo("a ficha F001 confere"),
        "P27 g1 executável: partilha de guardião, sk e PEM recusados; texto comum passa")
    D.v(pn_ia["estado"] == "NEUTRO_CENARIO" and pn_ia["assumido"].startswith("pesos ASSUMIDO"),
        "P27 PN_AI indicador CENARIO: aritmética determinística; pesos ASSUMIDO [VALIDAR] — medir no distrito, nunca citar como facto")
    # ===== GATEWAY v2.9.1 — a porta =====
    D.p("")
    D.p("GATEWAY — a porta da calculadora: câmara, posto e juiz usam sem ler código")
    reexec = _gateway_cura_reexecutar()
    corpo_gw = {"tipo": "CURA/1", "motor": VERSAO, "data": DATA_LOGICA,
                "casos": [{"caso": "M1-001", "estado": reexec["estados"][0]},
                          {"caso": "M1-002", "estado": reexec["estados"][1], "vetos": reexec["vetos_m002"]},
                          {"caso": "M1-003", "estado": reexec["estados"][2]},
                          {"caso": "M1-004", "estados": reexec["estados"][3:5]}],
                "emissor_pub": ed_publica(chave_demo("casa/cura")).hex(),
                "humano_decide": True}
    pkg_gw = {"corpo": corpo_gw, "selo": selar(corpo_gw, chave_demo("casa/cura"))}
    D.v(gateway_cura_verificar_objeto(pkg_gw)["estado"] == "REPRODUZIDO",
        "GATEWAY --cura: pacote CURA/1 verificado por re-execução (selo + conta refeita de raiz), offline")
    corpo_falso = {**corpo_gw, "casos": [dict(corpo_gw["casos"][0]), dict(corpo_gw["casos"][1], estado="SEM_VETO", vetos=[]),
                                         dict(corpo_gw["casos"][2]), dict(corpo_gw["casos"][3])]}
    D.v(gateway_cura_verificar_objeto({"corpo": corpo_falso, "selo": pkg_gw["selo"]})["estado"] == "SELO_INVALIDO",
        "GATEWAY canário: corpo falsificado com o selo original -> SELO_INVALIDO (nada passa)")
    sk_ata_gw = chave_demo("atacante/gateway")
    selo_ata_gw = {"alg": "Ed25519+SHA-256", "hash": h256(canon(corpo_gw)), "pub": ed_publica(sk_ata_gw).hex(),
                   "sig": ed_assinar(sk_ata_gw, canon(corpo_gw)).hex()}
    D.v(gateway_cura_verificar_objeto({"corpo": corpo_gw, "selo": selo_ata_gw})["estado"] == "AUTORIDADE_INVALIDA",
        "GATEWAY canário de AUTORIDADE: atacante resselando o MESMO corpo com a chave dele -> AUTORIDADE_INVALIDA (o corpo declara a sua chave; o selo tem de bater certo com ela)")
    msg_gw = canon(corpo_gw)
    sk_gw = chave_demo("perola/teste-gateway")
    sig_gw = ed_assinar(sk_gw, msg_gw)
    D.v(gateway_selo_verificar(msg_gw, sig_gw.hex(), ed_publica(sk_gw).hex())
        and not gateway_selo_verificar(msg_gw + b"x", sig_gw.hex(), ed_publica(sk_gw).hex()),
        "GATEWAY --selo: qualquer selo Ed25519 verifica no motor (roundtrip VALIDO; mensagem alterada INVALIDO)")
    # ===== P14 — SELO HÍBRIDO PÓS-QUÂNTICO =====
    D.p("")
    D.p("P14 — SELO HÍBRIDO PQ: Ed25519 + Lamport nos mesmos bytes; chave Lamport queima após UMA assinatura")
    chave_l14 = lamport_gerar("selo-hibrido-demo")
    corpo_l14 = {"h14": "corpo de prova", "valor": 42}
    selo_l14 = selar_hibrido(corpo_l14, chave_demo("casa/h14"), chave_l14)
    D.v(selo_hibrido_ok(corpo_l14, selo_l14, chave_l14["pub"]),
        "P14 selo híbrido VÁLIDO: Ed25519 e Lamport conferem os mesmos bytes (Lamport 8 KB, hash-based, pós-quântico)")
    D.v(not selo_hibrido_ok({"h14": "corpo de prova", "valor": 43}, selo_l14, chave_l14["pub"]),
        "P14 canário: 1 byte alterado -> selo híbrido CAI (integridade dual)")
    falha_reuso = False
    try:
        lamport_assinar(chave_l14, b"segunda mensagem com a mesma chave")
    except RuntimeError as erro:
        falha_reuso = "LAMPORT_REUSO_RECUSADO" in str(erro)
    D.v(falha_reuso, "P14 canário: reuso da mesma chave Lamport -> RECUSADO (uso único, P5)")
    D.v(len(selo_l14["sig_lam"]) // 2 == 8192 and len(chave_l14["pub"]) == 256,
        "P14 custo MEDIDO: assinatura Lamport 8.192 B vs Ed25519 64 B (128×) · pub 16.384 B — o preço honesto da imunidade quântica [ML-DSA-65 FIPS 204 por IMPLEMENTAR]")
    # ===== P44 — FROST: ASSINATURA DE LIMIAR =====
    D.p("")
    D.p("P44 — FROST: 2 de 3 assinam JUNTOS; a chave secreta nunca se junta; sai UMA assinatura Ed25519 válida")
    fro = Froste(2, 3, "lampada-medica")
    msg_f = b"libertacao do lote: medico local + auditor, nunca um sozinho"
    sig_f, meta_f = fro.assinar({1, 2}, msg_f)
    D.v(ed_verificar(fro.A, msg_f, sig_f),
        "P44 FROST 2-de-3: a assinatura de GRUPO verifica com o ed_verificar padrão (indistinguível de uma chave única)")
    D.v(gateway_selo_verificar(msg_f, sig_f.hex(), fro.A.hex()),
        "P44 compatibilidade com a porta: a assinatura de grupo passa no --selo do gateway (o mundo verifica sem saber que foi um quórum)")
    D.v(not ed_verificar(fro.A, msg_f, fro.fraude_solo(1, msg_f)),
        "P44 canário de quórum: 1 participante sozinho tenta passar-se pelo grupo -> assinatura INVÁLIDA (o segredo nunca se junta)")
    D.v(meta_f["rondas"] == 2 and meta_f["ligacao_aplicada"] and meta_f["parciais_verificados"],
        "P44 2 rondas com fator de ligação (anti-Drijvers) e parciais verificados pelo agregador; nonces do demo derivam da semente [produção: aleatoriedade real, nunca reutilizar]")
    # ===== P45 — O INFINITO COMPUTÁVEL =====
    D.p("")
    o_inf = oroboro()
    D.p(f"P45 — OUROBOROS: f(x)=sha256(x) em 24 bits fechou o ciclo — cauda μ={o_inf['cauda_mu']:,} · ciclo λ={o_inf['ciclo_lambda']:,} · {o_inf['passos_total']:,} passos (teoria √(πN/2) ≈ {o_inf['teoria_raiz']:,})")
    D.v(0 < o_inf["ciclo_lambda"] and o_inf["passos_total"] < (1 << 20),
        "P45 OUROBOROS: a cadeia de hashes fecha sobre si mesma num ciclo medido — o infinito de um espaço finito é o seu ciclo, e a casa mediu o seu")
    p_centro = valores_proprios_da_paz()
    p_estavel = valores_proprios_da_paz(travao=0.5)
    D.v(p_centro["tipo"] == "CENTRO_ORBITAS_FECHADAS" and p_estavel["tipo"] == "ESPIRAL_ESTAVEL" and p_estavel["traco"] < 0,
        "P8/P45 valores próprios da paz: sem travão, λ = ±i (CENTRO — a paz é dança de órbitas fechadas, não ponto morto); com travão logístico, traço < 0 (ESPIRAL ESTÁVEL — homeostase) [parâmetros de manual ASSUMIDO VALIDAR]")
    e_inf = a_escada_do_infinito(3470000.0)
    D.v(e_inf["anos"] > 1e24 and e_inf["veredicto"] == "INFINITO_AO_ALCANCE_DE_NINGUEM",
        "P45 a escada: o ciclo do estado completo de 256 bits é de ~" + f"{e_inf['anos']:.2e}".replace("e+", "e") + " anos à taxa medida — o infinito medido: ninguém fecha a cadeia de 256 bits, e por isso os selos de hoje bastam [CENARIO]")

    # ===== P46 — O ARQUIVO PARA SEMPRE =====
    D.p("")
    l300 = landauer_inversao(256, 300.0)
    l27 = landauer_inversao(256, 2.725)
    D.p(f"P46 — LANDAURER: inverter o selo de 256 bits custa (chão absoluto) {l300['energia_j']:.2e} J a 300 K = {l300['sois']:.2e} sóis convertidos; a 2,725 K (fundo cósmico) = {l27['sois']:.2e} sóis")
    D.v(l300["sois"] > 1e9 and l27["sois"] > 1e7,
        "P46 o para sempre da FÍSICA: inverter o selo de 256 bits custa mais que mil milhões de sóis de massa convertida — mesmo ao frio do universo morto [chão de Landauer, VALIDAR constantes]")
    rec_l14 = "64ab7b82 (exemplo de referência de era anterior)"
    arq = arquivo_resealar(b"conteudo da era anterior", rec_l14, "rotação v1->v2: partilhas expostas em canais de terceiros", chave_demo("casa/era-nova"))
    D.v(verificar_arquivo(arq, b"conteudo da era anterior", pub_nova=ed_publica(chave_demo("casa/era-nova")).hex()),
        "P46 ARQUIVO/1: a era nova resela o conteúdo da era antiga — conteúdo + selo antigo referido + nota honesta; a cadeia de eras não parte quando os algoritmos envelhecem")
    recusa_nota = False
    try:
        arquivo_resealar(b"conteudo", rec_l14, "   ", chave_demo("casa/era-nova"))
    except ValueError:
        recusa_nota = True
    D.v(recusa_nota, "P46 canário: re-selagem SEM nota honesta de rotação -> RECUSADA (a proveniência viaja com a era)")
    zi = shamir_zero_informacao()
    D.v(zi["candidatos_possiveis"] == 256,
        "P46 segurança INCONDICIONAL por exaustão: com 2 de 3 partes, os 256 segredos de um byte continuam TODOS possíveis — H(X|Y)=H(X) (teoria da informação, não custo)")
    # ===== P47 — SOBRE/1: O ENVELOPE BLINDADO =====
    D.p("")
    payload_37 = {"tipo": "recibo", "modulo": "M1", "dose_mg": 186, "incerteza_mg": 1.5, "estado": "OK"}
    peca_37 = sobre_assinar(payload_37, chave_demo("lampada/lampada-1"), kid="lampada-1")
    D.v(sobre_verificar(peca_37, ed_publica(chave_demo("lampada/lampada-1"))),
        "P47 SOBRE/1: envelope COSE_Sign1 (RFC 9052, alg -8 EdDSA) verifica pela casa — os mesmos bytes Ed25519, sem CA, sem servidor")
    D.v(_cbor({"b": 2, "a": 1}) == _cbor({"a": 1, "b": 2}),
        "P47 CBOR canónico: a ordem de inserção dos campos não muda um único byte (RFC 8949 §4.2.1, subconjunto)")
    series_37 = [f"recibo-{n:02d}" for n in range(16)]
    rec_37 = sobre_recibo_scitt(series_37, 7)
    D.v(merkle_confere(series_37[7], rec_37["prova"], rec_37["raiz"]) and not merkle_confere("recibo-falso", rec_37["prova"], rec_37["raiz"]),
        "P47 recibo SCITT (espírito RFC 9943): prova de inclusão Merkle — o recibo nº 7 prova offline que nunca saiu do registo; folha falsa não passa")
    D.v(len(peca_37["envelope"]) < 250,
        "P47 tamanho MEDIDO: o envelope completo tem " + str(len(peca_37["envelope"])) + " B < 250 B — cabe num QR, numa SMS, num rádio; o transporte é indiferente (o futuro offline sem Starlink)")

    # ===== P49 — MARE/1: ÁGUAS, MAR E PESCA =====
    D.p("")
    D.p("P49 — MARE/1: o mar DETETA crimes meses depois; a casa VETA antes de o crime completar")
    pub_mar = ed_publica(chave_demo("sensor/hidrofone_descarga")).hex()
    def reg_mar(lote, dist, vel, ppm):
        d = {"sensor": "hidrofone_descarga", "lote": lote, "dist_nm": dist, "vel_kn": vel, "ppm": ppm}
        return {"dados": d, "selo": selar(d, chave_demo("sensor/hidrofone_descarga"))}
    d_ok = mare_descarga(reg_mar("SENT-OK", 13.0, 8.0, 10.0), pub_mar)
    d_dist = mare_descarga(reg_mar("SENT-5NM", 5.0, 8.0, 10.0), pub_mar)
    d_ppm = mare_descarga(reg_mar("SENT-40PPM", 13.0, 8.0, 40.0), pub_mar)
    tam = {"dados": dict(reg_mar("SENT-40PPM", 13.0, 8.0, 40.0)["dados"], ppm=5.0), "selo": reg_mar("SENT-40PPM", 13.0, 8.0, 40.0)["selo"]}
    D.v(d_ok["estado"] == "LIBERADA" and d_dist["estado"] == "BLOQUEADA_DISTANCIA" and d_ppm["estado"] == "BLOQUEADA_PPM"
        and mare_descarga(tam, pub_mar)["estado"] == "BLOQUEADA_REGISTO_SEM_SELO",
        "P49 MARPOL Reg. 15: descarga a 13 MN/10 ppm LIBERADA · a 5 MN BLOQUEADA_DISTANCIA · a 40 ppm BLOQUEADA_PPM · mexer no registo selado -> SEM_SELO (fonte: IMO, Reg. 15)")
    pub_ais = ed_publica(chave_demo("sensor/ais")).hex()
    def reg_encontro(dist, k1, k2, minu, porto=False, reefer=True):
        d = {"sensor": "ais", "dist_m": dist, "kn_1": k1, "kn_2": k2, "minutos": minu, "porto": porto, "reefer": reefer}
        return {"dados": d, "selo": selar(d, chave_demo("sensor/ais"))}
    en_40 = mare_encontro(reg_encontro(400.0, 1.5, 1.2, 40), pub_ais)
    en_13h = mare_encontro(reg_encontro(300.0, 0.5, 0.4, 800), pub_ais)
    en_porto = mare_encontro(reg_encontro(400.0, 1.5, 1.2, 40, porto=True), pub_ais)
    D.v(en_40["estado"] == "TRANSBORDO_SUSPEITO" and en_13h["estado"] == "TRANSBORDO_PROVAVEL" and en_porto["estado"] == "SEM_ENCONTRO_PORTO",
        "P49 STS (Miller et al. 2018): 400 m/40 min -> TRANSBORDO_SUSPEITO · 13 h -> PROVAVEL · em porto -> não marca")
    pub_bal = ed_publica(chave_demo("sensor/balanca")).hex()
    def reg_desemb(lote, kg, cadeia=True):
        d = {"sensor": "balanca", "lote": lote, "kg": kg, "cadeia_captura_raiz": ("merkle-raiz-demo" if cadeia else None)}
        return {"dados": d, "selo": selar(d, chave_demo("sensor/balanca"))}
    sem_cadeia = mare_desembarque(reg_desemb("PEIXE-1", 900.0, cadeia=False), pub_bal, 50_000.0, 49_500.0)
    vetado = mare_desembarque(reg_desemb("PEIXE-1", 900.0), pub_bal, 50_000.0, 49_500.0)
    ok_t = mare_desembarque(reg_desemb("PEIXE-2", 400.0), pub_bal, 50_000.0, 49_500.0)
    D.v(sem_cadeia["estado"] == "RECUSADO_SEM_CADEIA_DE_CAPTURA" and vetado["estado"] == "VETO_TAC" and ok_t["estado"] == "DESEMBARCADA",
        "P49 IUU: sem cadeia de captura (Merkle) -> RECUSADO · acumulado acima do TAC -> VETO_TAC [TAC de demo ASSUMIDO VALIDAR ICES/UE] · dentro -> DESEMBARCADA")
    cert_ok = sobre_assinar({"tipo": "certificado_desembarque", "lote": "PEIXE-2", "estado": ok_t["estado"]},
                            chave_demo("lampada/lampada-1"), kid="lampada-1")
    D.v(len(cert_ok["envelope"]) < 250,
        "P49 o certificado de desembarque sai em envelope COSE de " + str(len(cert_ok["envelope"])) + " B — o inspetor do porto verifica offline, sem pedir nada a ninguém")
    # ===== P50 — AUDIT/1: CERTIFICAÇÃO POR ERAS =====
    D.p("")
    D.p("P50 — AUDIT/1: Vattenfall/NAM/químicos/nuclear — a auditoria cresce com a MUDANÇA, não com o tempo")
    pub_insp = ed_publica(chave_demo("inspetor/certificadora")).hex()
    def evidencia(item, valor):
        d = {"sensor": "inspetor", "item": item, "valor": valor}
        return {"dados": d, "selo": selar(d, chave_demo("inspetor/certificadora"))}
    it_ok = audit_avaliar_item(evidencia("valvula-alivio-3", 42.0), pub_insp, 50.0)
    it_nc = audit_avaliar_item(evidencia("valvula-alivio-4", 60.0), pub_insp, 50.0)
    it_lim = audit_avaliar_item(evidencia("valvula-alivio-5", 49.9), pub_insp, 50.0, incerteza=0.5)
    tam = {"dados": dict(evidencia("valvula-alivio-3", 42.0)["dados"], valor=100.0), "selo": evidencia("valvula-alivio-3", 42.0)["selo"]}
    D.v(it_ok["estado"] == "CONFORME" and it_nc["estado"] == "NAO_CONFORME" and it_lim["estado"] == "REVISAO_HUMANA"
        and audit_avaliar_item(tam, pub_insp, 50.0)["estado"] == "EVIDENCIA_SEM_SELO",
        "P50 itens de auditoria: CONFORME · NAO_CONFORME · no limite do erro -> REVISAO_HUMANA (a máquina não decide) · evidência mexida -> SEM_SELO")
    antigos = {f"item-{i}": h256(f"item-{i}-era1".encode()) for i in range(5)}
    novos = dict(antigos)
    novos["item-2"] = h256(b"item-2-era2-mudou")
    novos["item-5"] = h256(b"item-5-novo")
    moc = audit_moc(antigos, novos)
    D.v(moc["re_inspecionar"] == ["item-2"] and moc["novos"] == ["item-5"] and sorted(moc["carregar_com_prova"]) == ["item-0", "item-1", "item-3", "item-4"]
        and moc["taxa_reinspecao"] == 0.333,
        "P50 MOC incremental: 5 itens, 1 mudou + 1 novo -> re-inspeção de 1/3 (33,3%) e o resto CARREGA com prova da era anterior (a auditoria cresce com a mudança, não com o tempo)")
    fro_cert = Froste(2, 3, "certificacao-seveso")
    sig_cert, meta_cert = audit_certificado(moc["raiz_audit_nova"], fro_cert, b"instalacao-nam-demo")
    D.v(ed_verificar(fro_cert.A, _cbor({"tipo": "certificado_auditoria", "raiz_audit": moc["raiz_audit_nova"]}) + b"instalacao-nam-demo", sig_cert),
        "P50 certificado por FROST 2-de-3: auditor-chefe + regulador assinam a raiz — ninguém sozinho certifica (a assinatura de grupo verifica pelo ed_verificar padrão)")
    cert_37 = sobre_assinar({"tipo": "certificado_auditoria", "raiz": moc["raiz_audit_nova"], "instalacao": "NAM-demo",
                             "seveso": AUDIT_SEVESO["inspecao_anos_superior"]}, chave_demo("lampada/lampada-1"), kid="lampada-1")
    D.v(len(cert_37["envelope"]) < 250,
        "P50 para o regulador: certificado em envelope COSE de " + str(len(cert_37["envelope"])) + " B com o ciclo Seveso dentro (Art. 20: 1/3 anos · Art. 10: 5/5 anos) — verificado offline")
    # ====================== D26 RESPOSTA MÍNIMA SELADA + CACHE + BENCHMARK v3 (v2.6) ======================
    D.p("")
    D.p("D26 RESPOSTA MÍNIMA + CACHE + BENCHMARK v3 — peça de referência para a /v1/facto (fichas e perguntas de DEMO; tokens estimados: 1 por 4 bytes)")
    f1 = FICHAS_DEMO[0]
    rm, prosa = resposta_minima(f1), resposta_em_prosa(f1)
    t_p, t_m = contar_tokens(prosa), contar_tokens(canon(rm).decode("utf-8"))
    selo_rm = selar(rm, K("api/facto"))
    D.v(tuple(k for k in rm if k != "expansao_disponivel") == CAMPOS_MINIMA and rm["expansao_disponivel"] is True and rm["hash"] == hash_da_ficha(f1)
        and selo_ok(rm, selo_rm) and not selo_ok(dict(rm, facto="outra coisa"), selo_rm) and t_m < t_p and rm == resposta_minima(f1),
        f"P10 resposta mínima: 5 campos ({', '.join(CAMPOS_MINIMA)}) + expansao_disponivel; selada; mexer no facto parte o selo. Mesma pergunta: prosa {t_p} tokens, "
        f"mínima {t_m} tokens -> poupança {_n(100.0 * (1.0 - t_m / t_p), 1)}%")
    D.p("    " + canon(rm).decode("utf-8"))
    ch = CacheDeFactos(FICHAS_DEMO)
    q1, q1b = "Quantos exemplares teve a Bíblia de Gutenberg?", "quantos EXEMPLARES teve a biblia de gutenberg"
    r_frio, r_quente, r_outra = ch.responder(q1), ch.responder(q1), ch.responder(q1b)
    t_c = contar_tokens(canon(r_quente).decode("utf-8"))
    nova = dict(f1, facto="A Bíblia de Gutenberg teve uma tiragem entre 158 e 180 exemplares.")
    mortas = ch.fonte_mudou(f1["id"], nova)
    r_depois = ch.responder(q1)
    ch.fichas["KF-DEMO-002"]["data"] = "2026-12-01"  # a ficha muda sem aviso: a defesa tem de apanhar
    ch.responder(PERGUNTAS_DEMO[1]["pergunta"])
    ch.fichas["KF-DEMO-002"]["data"] = "2026-12-02"
    r_def = ch.responder(PERGUNTAS_DEMO[1]["pergunta"])
    D.v(r_frio == rm and r_quente == {"c": 1, "h": rm["hash"][:16]} and r_outra == r_quente and mortas == 1 and r_depois.get("hash") == hash_da_ficha(nova)
        and r_depois["hash"] != rm["hash"] and "c" not in r_def and r_def["data"] == "2026-12-02" and ch.responder("Qual é o salário mínimo em 2027?")["estado"] == "FORA_DA_COBERTURA"
        and CacheDeFactos.chave("Coração") == CacheDeFactos.chave("coracao?") and CacheDeFactos.chave("O cão mordeu o homem") != CacheDeFactos.chave("O homem mordeu o cão") and CacheDeFactos.chave("carro") != CacheDeFactos.chave("automóvel"),
        f"P4 cache: 1.ª vez -> resposta mínima ({t_m} tokens); 2.ª vez -> só o início do hash ({t_c} tokens); a mesma pergunta sem acentos, sem pontuação e em maiúsculas -> acerto; trocar a ordem das palavras -> pergunta nova; "
        f"o motor de diferenças avisa que a fonte mudou -> {mortas} entrada morre e a resposta seguinte traz o hash novo; ficha mudada sem aviso -> a defesa apanha; "
        "sinónimos (carro/automóvel) NÃO são apanhados")
    D.p("    " + canon(r_quente).decode("utf-8") + "  ·  contadores: " + canon(ch.conta).decode("utf-8"))
    bm = benchmark_v3(FICHAS_DEMO, PERGUNTAS_DEMO)
    for linha_b in relatorio_benchmark(bm):
        D.p("    " + linha_b)
    longa = [dict(q, prosa="palavra " * 600) if q["esperado"] else q for q in PERGUNTAS_DEMO]
    bm_l = benchmark_v3(FICHAS_DEMO, longa)
    D.v(bm == benchmark_v3(FICHAS_DEMO, PERGUNTAS_DEMO) and bm["dentro"]["n"] == 8 and bm["fora"]["n"] == 4 and bm["dentro"]["ficha_certa"] == 8 and bm["fora"]["recusou_bem"] == 4
        and not bm["meta_atingida"] and bm_l["meta_atingida"] and bm["prosa_minima_para_a_meta_tokens"] == math.ceil(bm["dentro"]["mediana_tokens_cache"] / (1.0 - 0.99)),
        f"P10 + P4 benchmark v3 (12 perguntas de DEMO, não as 100 reais): dois números separados, dentro e fora da cobertura; repetido dá o mesmo hash; a meta de 99% NÃO é atingida "
        f"contra prosa de {_num(bm['dentro']['mediana_tokens_prosa'])} tokens e É atingida contra prosa de 1200 tokens: a meta depende do tamanho da prosa com que se compara")
    D.p("  [VALIDAR] Faltam as 100 perguntas reais e a prosa verdadeira da API: python3 konfirmu_calc.py --benchmark FICHEIRO.json corre-as com este mesmo código.")

    # ====================== D27 ENXAME FRUGAL (v2.7) ======================
    D.p("")
    D.p("D27 ENXAME FRUGAL — as 4 promessas do «enxame_ultra_frugal.py» de outra IA, medidas com a matemática deste ficheiro (números de DEMO)")
    ctx_m = {"dominio": "SOL", "o_que": "eficiência do painel", "local": "Maputo", "unidade": "1"}
    ctx_l = dict(ctx_m, local="Lisboa")
    cg = CacheGUM()
    cg.guardar(ctx_m, G(0.217, 0.015, "1", fonte="leitura A"), {"ficha_id": "E-A"})
    perto = cg.procurar(ctx_m, G(0.218, 0.015, "1", fonte="leitura B"))
    longe = cg.procurar(ctx_m, G(0.280, 0.015, "1", fonte="leitura C"))
    outro_sitio = cg.procurar(ctx_l, G(0.217, 0.015, "1", fonte="leitura D"))
    D.v(perto == {"ficha_id": "E-A"} and longe is None and outro_sitio is None
        and _balde_da_outra_suite("SOL", 0.217, 0.015) != _balde_da_outra_suite("SOL", 0.218, 0.015)
        and _balde_da_outra_suite("SOL", 0.2176, 0.015) == _balde_da_outra_suite("SOL", 0.2324, 0.015)
        and _erro(lambda: cg.procurar(dict(ctx_m, unidade="kWh"), G(0.2, 0.01, "1")), TypeError) == "" and _erro(lambda: cg.guardar(ctx_m, G(1.0, 0.1, "kWh"), {}), TypeError),
        "P4 cache por incerteza: 0,217 ± 0,015 e 0,218 ± 0,015 -> a mesma medida, 0 chamadas (o balde da outra suite separa-as, e junta 0,2176 com 0,2324); "
        "0,280 -> medida nova; a mesma leitura em Lisboa -> NÃO reutiliza a de Maputo (na outra suite reutiliza); unidade errada -> recusada")
    tres = [{"ficha_id": f"E0{i}", "dominio": "SOL", "etiqueta": "MEDIDO", "valores": {"val": v, "gum": 0.015, "kw": 5}, "o_que_nao_garante": lim,
             "hash_anterior": "0" * 16, "hash": h256(f"DEMO/{i}".encode())} for i, (v, lim) in enumerate([(0.221, "Limpar poeira semanal"), (0.31, "Não prevê sombra"), (0.12, "Só 1 medição")])]
    ce = custo_do_esquema_curto(tres)
    hexes = sum(len(f["hash"]) + len(f["hash_anterior"]) for f in tres)
    parte_hash = hexes / len(canon([ficha_curta(f) for f in tres]))
    selo_c = selar(ficha_curta(tres[0]), K("enxame/no-1"))
    D.v(all(ficha_longa(ficha_curta(f)) == f for f in tres) and ce["tokens_curto"] < ce["tokens_longo"] and ce["poupanca"] < 0.54
        and _erro(lambda: ficha_curta(dict(tres[0], o_que_nao_garante=" ")), ValueError) and _erro(lambda: ficha_curta(dict(tres[0], etiqueta="CERTO")), ValueError)
        and selo_ok(ficha_curta(tres[0]), selo_c) and not selo_ok(ficha_curta(dict(tres[0], valores={"val": 0.9})), selo_c),
        f"P10 esquema de 1 letra (3 fichas): {ce['tokens_longo']} -> {ce['tokens_curto']} tokens = {_n(100.0 * ce['poupanca'], 1)}% de poupança (anunciado: 54%); a tabela custa {ce['tokens_tabela']} tokens "
        f"e só compensa a partir de {ce['compensa_a_partir_de_fichas']} fichas por conversa; ida e volta sem perder nada; sem limite escrito -> recusada; "
        f"os hashes são {_n(100.0 * parte_hash, 0)}% da ficha curta e não encolhem; selo Ed25519 (não só hash): mexer num valor parte-o")
    p64, p85 = pacote_de_rede(tres), pacote_de_rede(tres, "b85")
    s64, s85, s1 = segmentos_sms(p64), segmentos_sms(p85), segmentos_sms(pacote_de_rede(tres[:1]))
    bruto1, pac1 = len(canon([ficha_curta(tres[0])])), len(pacote_de_rede(tres[:1]))
    D.v(abrir_pacote_de_rede(p64) == tres and abrir_pacote_de_rede(p85, "b85") == tres and s64["alfabeto"] == "GSM-7" and "`" not in GSM7_BASICO | GSM7_EXTENSAO
        and segmentos_sms("a" * 160)["segmentos"] == 1 and segmentos_sms("a" * 161)["segmentos"] == 2 and segmentos_sms("{" * 80)["unidades"] == 160 and segmentos_sms("`")["alfabeto"] == "UCS-2",
        f"P20 transporte (3 fichas, zlib nível 9): Base64 = {len(p64)} caracteres, {s64['alfabeto']}, {s64['segmentos']} SMS; Base85 = {len(p85)} caracteres, {s85['alfabeto']}, {s85['segmentos']} SMS; "
        f"1 ficha sozinha: {bruto1} bytes -> {pac1} caracteres ({s1['segmentos']} SMS): comprimir 1 ficha não ajuda; os dois pacotes abrem e devolvem as 3 fichas iguais")
    ganho = busca["possiveis"] / busca["folhas_avaliadas"]
    D.v(abs(1.0 / (1.0 - 0.95) - 20.0) < 1e-9 and abs(1.0 / (1.0 - 0.99) - 100.0) < 1e-6 and 1.0 < ganho < 20.0,
        f"P17 poda antes da IA: o ganho é 1 / (1 − fração cortada): 95% -> 20×, 99% -> 100× — é só esta conta, e a fração tem de ser MEDIDA. A única medida neste ficheiro (D14): "
        f"{busca['folhas_avaliadas']} de {busca['possiveis']} avaliadas = {_n(100.0 * (1.0 - 1.0 / ganho), 1)}% cortadas -> {_n(ganho, 1)}×")
    D.p("  [VALIDAR] Não reproduzido do texto recebido: «248 -> 114 tokens», «940 -> 265 bytes», «cabe em 2 SMS/USSD», «>40×». Os «tokens poupados» do código recebido são as constantes 120 e 95, não medições.")

    # ====================== D28 CORREÇÕES DO TESTE DE ATAQUE (v2.8) ======================
    D.p("")
    D.p("D28 CORREÇÕES — o que o teste de ataque de 20-11-2026 partiu, agora travado")
    nan, inf = float("nan"), float("inf")
    D.v(_erro(lambda: G(nan, 0.0, "kWh"), ValueError) and _erro(lambda: G(inf, 0.0, "kWh"), ValueError) and _erro(lambda: G(1.0, nan, "kWh"), ValueError)
        and _erro(lambda: G("10", 0.0, "kWh"), TypeError) and _erro(lambda: G(True, 0.0, "kWh"), TypeError)
        and _erro(lambda: veto_hidrico(G(nan, 0.0, "m3/ano"), G(100.0, 1.0, "m3/ano")), ValueError)
        and _erro(lambda: G(1e308, 0.0, "1") * G(1e308, 0.0, "1"), ValueError),
        "P3 números não finitos: NaN, infinito, texto e verdadeiro/falso recusados ao criar; uma conta que transborda para infinito também é recusada; o veto hídrico já não recebe NaN")
    D.v(hobj("caf" + chr(0xE9)) == hobj("cafe" + chr(0x301)) and hobj({"cafe" + chr(0x301): 1}) == hobj({"caf" + chr(0xE9): 1}) and hobj(5) != hobj(5.0),
        "P4 texto normalizado antes do hash: «é» escrito de duas maneiras (Mac e outros) dá o mesmo hash; 5 e 5,0 continuam a dar hashes diferentes [VALIDAR: decisão em aberto]")
    D.v(_erro(lambda: veto_gibbs(G(-92.0, 2.0, "kJ/mol"), G(-5.0, 1.0, "K"), G(-199.0, 5.0, "J/mol/K")), VetoFisico)
        and _erro(lambda: veto_gibbs(G(-92.0, 2.0, "kJ/mol"), G(0.0, 0.0, "K"), G(-199.0, 5.0, "J/mol/K")), VetoFisico),
        "P2 zero absoluto: o veto de Gibbs com −5 K ou 0 K responde VETO em vez de «dentro»")
    m3 = lambda x: G(x, 0.0, "m3/dia")
    t_zero = json.loads(canon(TERRITORIO_DEMO))
    t_zero["necessidade"]["agua"] = 0.0
    D.v(_erro(lambda: indice_abundancia(m3(1.0), m3(0.0), m3(1.0), m3(1.0), "m3/dia"), ValueError) and _erro(lambda: indice_abundancia(m3(-5.0), m3(10.0), m3(1.0), m3(1.0), "m3/dia"), ValueError)
        and _erro(lambda: procurar_configuracao(t_zero), ValueError),
        "P16 abundância: necessidade zero -> recusada com motivo (antes rebentava); disponível negativo -> recusado (antes dava A = −0,50 «dentro»); território com necessidade zero -> recusado")
    D.v(compativeis(G(10.0, 0.5, "1", fonte="sensor"), G(10.2, 0.5, "1", fonte="sensor"), "1") is False and compativeis(G(10.0, 0.5, "1", fonte="s1"), G(10.2, 0.5, "1", fonte="s2"), "1"),
        "P3 não é falha, é regra escrita: a mesma `fonte` = o mesmo erro, por isso 10,0 e 10,2 com o mesmo nome dão diferença 0,2 ± 0 e NÃO são a mesma medida; com nomes próprios são")

    sk_e = chave_demo("ataque")
    pk_pequena, sig_nula = bytes([1]) + bytes(31), bytes([1]) + bytes(63)
    sig_boa = ed_assinar(sk_e, b"m")
    D.v(not ed_verificar(pk_pequena, b"qualquer mensagem", sig_nula) and not ed_verificar(pk_pequena, b"outra", sig_nula) and ed_verificar(ed_publica(sk_e), b"m", sig_boa)
        and not ed_verificar(ed_publica(sk_e), b"m", sig_boa[:32] + (int.from_bytes(sig_boa[32:], "little") + _L).to_bytes(32, "little")),
        "S1 assinaturas: uma chave pública de ordem pequena com uma assinatura nula servia para QUALQUER mensagem — agora recusada; a assinatura boa continua a conferir; a maleável (S + L) continua recusada")
    fora_q = ["Quantos exemplares teve a Bíblia de Lutero?", "Gutenberg morreu pobre?", "Em que ano foi publicado o primeiro livro de Camões?", "Qual é a data do processo de Kafka?",
              "A OMS diz que 30 a 50% dos casos de gripe são evitáveis?", "Gutenberg", "Bíblia", "Quando começou a ser publicada a revista Nature?", "ano"]
    D.v(all(top1_simples(FICHAS_DEMO, q) is None for q in fora_q) and all(top1_simples(FICHAS_DEMO, q["pergunta"])["id"] == q["esperado"] for q in PERGUNTAS_DEMO if q["esperado"]),
        f"P10 top-1: das {len(fora_q)} perguntas que partilham palavras com as fichas mas não são cobertas («Bíblia de Lutero», «revista Nature», «gripe»…), responde a 0 (na v2.7 respondia a 9); "
        "as 8 perguntas cobertas continuam certas")
    lv_e = LedgerImutavel(chave_demo("notario/ataque"))
    for i in range(10):
        lv_e.registar(i, "PAGAMENTO", {"n": i})
    pac_e = json.loads(canon(exportar_ledger(lv_e)))
    cort = dict(pac_e, blocos=pac_e["blocos"][:6], cabeca=pac_e["blocos"][5]["hash_atual"])
    falso = LedgerImutavel(chave_demo("impostor"))
    falso.registar(0, "PAGAMENTO", {"n": 999})
    D.v(verificar_externo(pac_e, lv_e.pub, pac_e["cabeca"])["estado"] == "CONFERE" and verificar_externo(cort, lv_e.pub)["estado"] == "CONFERE"
        and verificar_externo(cort, lv_e.pub, pac_e["cabeca"])["estado"] == "RECUSADO_CABECA_DIFERENTE_DA_PUBLICADA"
        and verificar_externo(json.loads(canon(exportar_ledger(falso))))["estado"] == "COERENTE_NOTARIO_POR_CONFIRMAR"
        and verificar_externo(dict(pac_e, blocos=[], cabeca="0" * 64), lv_e.pub)["estado"] == "VAZIO"
        and verificar_externo(dict(pac_e, formato="KONFIRM`-LEDGER/1"), lv_e.pub)["estado"] == "RECUSADO_PACOTE_ILEGIVEL"
        and verificar_externo(dict(pac_e, pub_notario=pac_e["pub_notario"].upper()), lv_e.pub)["estado"] == "RECUSADO_PACOTE_ILEGIVEL",
        "S7 verificação externa: cortar os 4 últimos blocos só se apanha com a cabeça publicada (e apanha-se); um notário que ninguém conhece já não diz CONFERE, diz COERENTE_NOTARIO_POR_CONFIRMAR; "
        "pacote vazio -> VAZIO; formato mexido ou chave em maiúsculas -> recusado")
    iguais = 0
    for i in range(2000):
        g1 = G(10.0 + 0.5 * (((i * 7919) % 2000) / 1000.0 - 1.0), 0.5, "1", fonte=f"par{i}a")
        iguais += compativeis(g1, G(10.0, 0.5, "1", fonte=f"par{i}b"), "1")
    D.v(compativeis(G(10.0, 0.5, "1", fonte="x1"), G(11.38, 0.5, "1", fonte="x2"), "1") and not compativeis(G(10.0, 0.5, "1", fonte="x1"), G(11.40, 0.5, "1", fonte="x2"), "1"),
        "P4 comparar duas leituras: 95% dos dois lados (k = 1,96). 10,0 ± 0,5 e 11,38 ± 0,5 -> a mesma medida; 11,40 -> diferente (fronteira em 1,96 × 0,71 = 1,386). "
        "Com o k antigo, 10% das leituras iguais saíam diferentes (medido fora do demo, 40 000 pares)")

    # ===== P51 a P54 — A BASE-MÃE DENTRO DA CALCULADORA (v3.0) =====
    D.p("")
    D.p("P51 a P54 — A BASE-MÃE: as descobertas entram tal e qual (o mesmo SHA-256) e as baterias correm sobre as peças desta calculadora")
    carregou = _erro(base_mae, ValueError) == ""
    nome_c = "kcp_exacto.py"
    guardado = _BASE_MAE_FICHEIROS[nome_c]
    _BASE_MAE_FICHEIROS[nome_c] = (guardado[0], guardado[1] + "#")
    mexido_recusado = _erro(lambda: base_mae_ficheiro(nome_c), ValueError) != ""
    _BASE_MAE_FICHEIROS[nome_c] = guardado
    D.v(carregou and mexido_recusado and all(hmac.compare_digest(h256(t.encode("utf-8")), s) for s, t in _BASE_MAE_FICHEIROS.values()),
        f"P10 linhagem: os {len(_BASE_MAE_FICHEIROS)} ficheiros da base-mãe embutidos conferem um a um com o SHA-256 do registo; "
        "um byte acrescentado a um deles -> recusado antes de correr")
    for desc_b, pilar_b, teste_b, _prec_b, minimo_b, saida_b in _BASE_MAE_BATERIAS:
        ok_b, r_b = base_mae_confere(teste_b)
        D.v(ok_b, f"{pilar_b} {desc_b} ({teste_b}): {r_b['ok']}/{r_b['total']} sobre as peças DESTA calculadora, sem rede e sem sorteios; "
                  f"saída {r_b['saida'][:16]}… = a do registo da base-mãe")
    pk_peq, sig_nula = (bytes([1]) + bytes(31)).hex(), (bytes([1]) + bytes(63)).hex()
    D.v(not gateway_selo_verificar("Eu autorizo pagar 1 000 000 EUR a quem trouxer este papel.".encode("utf-8"), sig_nula, pk_peq)
        and not gateway_selo_verificar(b"qualquer outra coisa", sig_nula, pk_peq),
        "S1 + GATEWAY: a porta --selo recusa a chave de ordem pequena com assinatura nula — na v2.9.10 dizia VALIDO para QUALQUER ficheiro; "
        "a junção trouxe a correção da v2.8")
    pedidos = [f"P{i}" for i in range(1, 26) if i != 14] + [f"M{i}" for i in range(1, 6)] + ["B1", "B2", "B3", "L1", "R1", "A1"] + [f"S{i}" for i in range(1, 10)] + ["P33", "P34", "P35", "P36", "P37", "P38", "P39", "P40", "P41", "P42", "P43", "P14", "P27", "P44", "P45", "P46", "P47", "P49", "P50", "P51", "P52", "P53", "P54"]
    vistos = set()
    for linha in D.linhas:
        achado = re.match(r"  \[OK\] ((?:[PMBLRSA]\d+)(?:(?: \+ | a )(?:[PMBLRSA]\d+))*) ", linha)
        if achado:
            vistos.update(re.findall(r"[PMBLRSA]\d+", achado.group(1)))
    em_falta = [p for p in pedidos if p not in vistos]
    D.v(not em_falta and [l.split()[0] for l in D.linhas if re.match(r"D\d+ ", l)] == [f"D{i}" for i in range(1, 29)],
        f"COBERTURA: os {len(pedidos)} pilares com código (P1 a P25 com o P14, P27, P33 a P47, P49 a P54, M1 a M5, B1 a B3, L1, R1, A1, S1 a S9) têm pelo menos uma verificação verde e o demo correu de D1 a D28, por esta ordem"
        + ("" if not em_falta else " — EM FALTA: " + ", ".join(em_falta)))
    D.p("  P14: Lamport (hash-based, pós-quântico) IMPLEMENTADO neste motor e selo híbrido a correr; ML-DSA-65 (FIPS 204) fica [IMPLEMENTAR]. P26 (ponte democrática): só comentário, NÃO feito.")

    # ============================== FECHO ==============================
    D.p("")
    D.p("LIMITES DECLARADOS (o_que_nao_garante)")
    for i, t in enumerate(O_QUE_NAO_GARANTE, 1):
        D.p(f"  {i}. {t}")
    D.p("")
    D.p(("TUDO VERDE" if D.ok == D.total else "VERMELHO") + f": {D.ok}/{D.total} verificações")
    print("sha256 desta saída (todas as linhas acima): " + h256("\n".join(D.linhas).encode("utf-8")))
    return 0 if D.ok == D.total else 1


def demo() -> int:
    """Corre o demo e deixa as regras e os canários como estavam: duas corridas seguidas dão a mesma saída."""
    regras, canarios = json.dumps(REGRAS), json.dumps(CANARIOS)
    _LAMPORT_USADOS.clear()
    try:
        return _demo()
    finally:
        REGRAS.clear()
        REGRAS.update(json.loads(regras))
        CANARIOS.clear()
        CANARIOS.update(json.loads(canarios))


# -----------------------------------------------------------------------------
# 23. v2.3 — OS TESTES EM unittest (os 4 grupos que o «Prompt Final» da outra suite pede, corridos sobre ESTE ficheiro)
#     python3 konfirmu_calc.py --testes        ou        python3 -m unittest konfirmu_calc
# -----------------------------------------------------------------------------
class _Mundo:
    """Um mundo pequeno para os testes, igual ao de D2: notário, fontes, aldeia de 14, 5 custódios, juíza, válvula e motor."""

    def __init__(self) -> None:
        K = self.K = chave_demo
        self.livro = LedgerImutavel(K("notario"))
        self.fontes = {n: {"pub": self.pub("fonte/" + n), "operador": op} for n, op in (
            ("contador_selado", "aferidor_metrologia"), ("satelite", "agencia_espacial"), ("inspetora", "inspecao_distrital"),
            ("aferidora_precos", "aferidora_precos"))}
        self.aldeia = Aldeia({f"conselho_{i}": self.pub(f"aldeia/conselho_{i}") for i in range(1, 8)})
        for i, trio in enumerate([(1, 2, 3), (1, 4, 5), (1, 6, 7), (2, 4, 6), (2, 5, 7), (3, 4, 7), (3, 5, 6)], 1):
            self.aldeia.admitir(f"vizinha_{i}", self.pub(f"aldeia/vizinha_{i}"), [
                {"por": f"conselho_{j}", "selo": selar({"atesto": f"vizinha_{i}", "pub": self.pub(f"aldeia/vizinha_{i}")}, K(f"aldeia/conselho_{j}"))}
                for j in trio])
        self.nomes = list(CAMARAS)
        self.sk_cofre = K("cofre/origem")
        self.partes = dict(zip(self.nomes, shamir_partir(int.from_bytes(self.sk_cofre, "big"), 3, 5, K("shamir/semente-declarada"))))
        self.motor = Motor(100_000_000, ed_publica(self.sk_cofre).hex(), {n: self.pub("custodio/" + n) for n in self.nomes}, self.fontes,
                           self.aldeia, {"juiza_distrital": self.pub("juiz/juiza_distrital")},
                           Valvula({"medica_chefe": self.pub("vital/medica_chefe")}), K("motor"), self.livro)

    def pub(self, nome: str) -> str:
        return ed_publica(self.K(nome)).hex()

    def leituras(self, eid: str, valores: Sequence[float], dia: int, unidade: str = "kWh/dia") -> List[Dict[str, Any]]:
        saida = []
        for fonte, x in zip(("contador_selado", "satelite", "inspetora"), valores):
            d = {"fonte": fonte, "valor": x, "unidade": unidade, "ref": eid, "dia": dia}
            saida.append({"dados": d, "selo": selar(d, self.K("fonte/" + fonte))})
        return saida

    def votos(self, eid: str, dia: int, quantos: int = 5) -> List[Dict[str, Any]]:
        saida = []
        for i in range(1, quantos + 1):
            d = {"quem": f"vizinha_{i}", "obra": eid, "conforme": True, "foto": h256(f"foto/{eid}/vizinha_{i}".encode()), "dia": dia}
            saida.append({"dados": d, "selo": selar(d, self.K(f"aldeia/vizinha_{i}"))})
        return saida

    def assinaturas(self, quem: Sequence[str], eid: str, sid: str) -> Dict[str, Dict[str, Any]]:
        return {n: {"selo": selar({"sessao": sid, "pedido": self.motor.hash_pedido(eid)}, self.K("custodio/" + n)), "parte": list(self.partes[n])}
                for n in quem}

    def preco(self, custo: float, propostas: Sequence[float]) -> Dict[str, Any]:
        d = {"fonte": "aferidora_precos", "precos": [39.5, 40.0, 40.3, 39.9, 40.1]}
        return {"custo": custo, "propostas": list(propostas), "historico": {"dados": d, "selo": selar(d, self.K("fonte/aferidora_precos"))}}

    def pedir(self, eid: str, valores: Sequence[float], dia: int = 0, propostas: Sequence[float] = (39.8, 40.2, 41.0), assinam: int = 3) -> Dict[str, Any]:
        """Cria o escrow, abre a sessão e pede a liquidação com 3 leituras, preço, 5 votos conformes e `assinam` custódios."""
        self.motor.criar_escrow(eid, "cooperativa_sol", 4_000_000, dia, 5.0, "kWh/dia")
        self.sid = self.motor.abrir_sessao(eid, dia)
        self.args = dict(leituras=self.leituras(eid, valores, dia), preco=self.preco(40.2, propostas), votos=self.votos(eid, dia),
                         assinaturas=self.assinaturas(self.nomes[:assinam], eid, self.sid))
        return self.motor.liquidar(eid, self.sid, dia, **self.args)


class TestesKonfirmu(unittest.TestCase):
    """Os nomes começam por g1 a g4: são os 4 grupos pedidos. O que na outra suite é só texto fica SALTADO, com o motivo."""

    # ---- 1. vetos
    def test_g1_veto_dimensional(self) -> None:
        """W + EUR -> TypeError; 1 kWh + 1000 Wh = 2 kWh; 2 kW × 3 h = 6 kWh (o motor converte, não compara letras)"""
        with self.assertRaises(TypeError):
            G(5.0, 0.0, "W") + G(3.0, 0.0, "EUR")
        self.assertAlmostEqual((G(1.0, 0.0, "kWh") + G(1000.0, 0.0, "Wh")).em("kWh")[0], 2.0, places=12)
        self.assertAlmostEqual((G(2.0, 0.0, "kW") * G(3.0, 0.0, "h")).em("kWh")[0], 6.0, places=12)
        with self.assertRaises(TypeError):
            (G(2.0, 0.0, "kW") * G(3.0, 0.0, "h")).em("EUR")

    def test_g1_veto_termodinamico(self) -> None:
        """silício: 33% passa, 34% sem prova é vetado; a flag sozinha não chega; prova selada chega; 95% nem com prova; tecnologia inventada é recusada"""
        lab_sk = chave_demo("lab/laboratorio_de_ensaios")
        labs = {"laboratorio_de_ensaios": ed_publica(lab_sk).hex()}
        dados = {"amostra": "celula_de_teste", "rendimento_medido": 0.46}
        prova = {"laboratorio": "laboratorio_de_ensaios", "dados": dados, "selo": selar(dados, lab_sk)}
        self.assertEqual(veto_fisico(G(33.0, 0.0, "%")), "DENTRO_DO_TETO")
        for argumentos in ({}, {"prova_laboratorial": True}, {"prova_laboratorial": dict(prova, selo=selar(dados, chave_demo("lab/outro")))}):
            with self.assertRaises(VetoFisico):
                veto_fisico(G(34.0, 0.0, "%"), laboratorios=labs, **argumentos)
        self.assertEqual(veto_fisico(G(45.0, 0.0, "%"), prova_laboratorial=prova, laboratorios=labs), "ACIMA_DO_TETO_COM_PROVA_LABORATORIAL")
        with self.assertRaises(VetoFisico):
            veto_fisico(G(95.0, 0.0, "%"), prova_laboratorial=prova, laboratorios=labs)
        with self.assertRaises(VetoFisico):
            veto_fisico(G(20.0, 0.0, "%"), tecnologia="maquina_milagrosa")
        self.assertTrue(issubclass(VetoFisico, ValueError))

    def test_g1_veto_de_carnot(self) -> None:
        """máquina térmica entre 600 K e 300 K: teto 50%; 45% dentro; 62% vetado; kelvin obrigatório"""
        tq, tf = G(600.0, 5.0, "K"), G(300.0, 2.0, "K")
        self.assertAlmostEqual(teto_de_carnot(tq, tf).em("%")[0], 50.0, places=9)
        self.assertEqual(veto_de_carnot(G(45.0, 0.0, "%"), tq, tf)["estado"], "DENTRO_DO_TETO_DE_CARNOT")
        with self.assertRaises(VetoFisico):
            veto_de_carnot(G(62.0, 0.0, "%"), tq, tf)
        with self.assertRaises(TypeError):
            teto_de_carnot(G(600.0, 0.0, "°C"), tf)

    # ---- 2. ledger e sessões
    def test_g2_ledger_1_byte(self) -> None:
        """1 carácter mexido num bloco de uma cópia da cadeia -> a cadeia deixa de conferir"""
        livro = LedgerImutavel(chave_demo("teste/notario"))
        for i in range(3):
            livro.registar(i, "PAGAMENTO", {"valor": 100 + i, "para": "cooperativa"})
        self.assertTrue(livro.verificar_integridade_cadeia())
        copia = json.loads(json.dumps(livro.blocos))
        copia[1]["payload"]["valor"] = 999
        self.assertFalse(conferir_blocos(copia, livro.pub))
        self.assertTrue(conferir_blocos(livro.blocos, livro.pub))

    def test_g2_ledger_passado_reescrito(self) -> None:
        """reescrever o passado e refazer os hashes todos, sem a chave do notário -> não passa (na outra suite passa)"""
        livro = LedgerImutavel(chave_demo("teste/notario"))
        for i in range(3):
            livro.registar(i, "PAGAMENTO", {"valor": 100 + i, "para": "cooperativa"})
        copia, anterior = json.loads(json.dumps(livro.blocos)), "0" * 64
        copia[0]["payload"]["valor"] = 999999
        for b in copia:  # o falsário refaz a ligação e o hash de cada bloco; a assinatura não consegue refazer
            b["hash_anterior"] = anterior
            b["hash_atual"] = anterior = hobj({k: v for k, v in b.items() if k not in ("hash_atual", "assinatura")})
        self.assertFalse(conferir_blocos(copia, livro.pub))
        falso = LedgerImutavel(chave_demo("teste/falsario"))  # e com outra chave a cadeia confere, mas não é a do notário
        falso.registar(0, "PAGAMENTO", {"valor": 999999, "para": "cooperativa"})
        self.assertTrue(falso.verificar_integridade_cadeia())
        self.assertFalse(conferir_blocos(falso.blocos, livro.pub))

    def test_g2_sessao_de_uso_unico(self) -> None:
        """a mesma sessão de assinatura apresentada 2.ª vez -> RECUSADO_SESSAO_JA_USADA"""
        m = _Mundo()
        self.assertEqual(m.pedir("T1", (7.1, 6.9, 7.0))["estado"], "LIBERTADA")
        self.assertEqual(m.motor.liquidar("T1", m.sid, 0, **m.args)["estado"], "RECUSADO_SESSAO_JA_USADA")
        self.assertEqual(m.motor.pago, {"cooperativa_sol": 4_000_000})
        self.assertTrue(m.livro.verificar_integridade_cadeia())

    # ---- 3. estorno, cartel e confiança baixa
    def test_g3_estorno_aos_15_dias(self) -> None:
        """sem lastro -> CONGELADO_15D; ao dia 14 continua; ao dia 15 sem decisão humana o dinheiro volta ao cofre de origem"""
        m = _Mundo()
        r = m.pedir("T2", (0.3, 0.4, 0.35), assinam=5)
        self.assertEqual((r["estado"], r["motivos"]), ("CONGELADO_15D", ["SEM_LASTRO_FISICO"]))
        self.assertEqual(m.motor.avancar(14), [])
        self.assertEqual([x["estado"] for x in m.motor.avancar(15)], ["EXPIRACAO_ESTORNO_ORIGEM"])
        self.assertEqual(m.motor.reserva, 100_000_000 - m.motor.fundo)
        self.assertEqual(m.motor.pago, {})
        self.assertTrue(m.motor.conserva())

    def test_g3_cartel(self) -> None:
        """4 propostas coladas ao teto -> CARTEL_NO_TETO e congela; 3 propostas ao preço de mercado não são cartel (na outra suite são)"""
        banda = banda_preco([39.5, 40.0, 40.3, 39.9, 40.1])
        self.assertTrue(sinal_de_cartel([41.0, 41.1, 41.15, 41.19], banda)["sinal"])
        for normais in ([39.7, 39.8, 39.9], [39.9, 40.1, 40.5], [39.8, 40.2, 41.0]):
            self.assertFalse(sinal_de_cartel(normais, banda)["sinal"])
        r = _Mundo().pedir("T3", (7.1, 6.9, 7.0), propostas=(41.0, 41.1, 41.15, 41.19))
        self.assertEqual((r["estado"], r["motivos"]), ("CONGELADO_15D", ["CARTEL_NO_TETO"]))

    def test_g3_confianca_baixa_nem_pune_nem_paga(self) -> None:
        """1 leitura adulterada baixa a confiança para menos de 85% -> não congela e NÃO paga (na outra suite paga)"""
        m = _Mundo()
        r = m.pedir("T4", (7.1, 6.9, 12.0), assinam=5)
        self.assertEqual((r["estado"], r["motivos"]), ("REVISAO_HUMANA_SEM_PUNIR_NEM_PAGAR", ["ORACULO_CONFIANCA_BAIXA"]))
        self.assertEqual((m.motor.escrows["T4"]["estado"], m.motor.pago, m.motor.custodia), ("ATIVO", {}, {"T4": 4_000_000}))

    # ---- 4. domínios
    def test_g4_energia_solar(self) -> None:
        """4 painéis de 1,95 m2 a 22%, PR 0,75, 5,5 h de sol de pico -> 7,0785 kWh/dia; a incerteza propaga-se"""
        e = F2(G(4.0, 0.0, "painel/microrrede"), G(1.95, 0.02, "m2/painel"), G(22.0, 1.5, "%"), G(0.75, 0.05, "1"), G(5.5, 0.5, "h/dia"))
        v, u = e.em("kWh/dia/microrrede")
        self.assertAlmostEqual(v, 7.0785, places=9)
        self.assertAlmostEqual(u, 7.0785 * math.sqrt((0.02 / 1.95) ** 2 + (1.5 / 22.0) ** 2 + (0.05 / 0.75) ** 2 + (0.5 / 5.5) ** 2), places=9)

    def test_g4_shamir_3_de_5(self) -> None:
        """os 10 trios reconstroem, nenhum par reconstrói; o ataque que abre a outra suite (1 parte + a semente pública) aqui não abre"""
        segredo, semente = int.from_bytes(chave_demo("teste/segredo"), "big"), chave_demo("teste/semente")
        partes = shamir_partir(segredo, 3, 5, semente)
        self.assertTrue(all(shamir_juntar(list(t)) == segredo for t in itertools.combinations(partes, 3)))
        self.assertTrue(all(shamir_juntar(list(t)) != segredo for t in itertools.combinations(partes, 2)))
        so_da_semente = [_determinista(semente, "shamir", i) % _PS for i in (1, 2)]  # o ataque: coeficientes tirados só da semente
        for x, y in partes:
            self.assertNotEqual((y - so_da_semente[0] * x - so_da_semente[1] * x * x) % _PS, segredo)
        outro = shamir_partir(segredo + 1, 3, 5, semente)  # a mesma semente com outro segredo: a diferença das partes não mostra a dos segredos
        self.assertTrue(all((b[1] - a[1]) % _PS != 1 for a, b in zip(partes, outro)))
        self.assertEqual(shamir_juntar(shamir_partir(2 ** 200 + 5, 3, 5, semente)[:3]), 2 ** 200 + 5)
        with self.assertRaises(ValueError):  # segredo que não cabe no primo: recusa, em vez de o estragar calado
            shamir_partir(2 ** 200 + 5, 3, 5, semente, PRIMO_DA_ORDEM)

    def test_g4_ponto_neutral(self) -> None:
        """piso humano cumprido e pressões abaixo do teto -> OURO; uma comunidade confortável acima do teto ecológico -> veto biofísico"""
        un = dict(FORMULAS_15["F15.1"]["unidades"], **FORMULAS_15["F15.2"]["unidades"])

        def med(**x: Tuple[float, float]) -> Dict[str, Dict[str, Any]]:
            return {k: {"valor": float(v), "incerteza": float(u), "unidade": un[k], "etiqueta": "MEDIDO", "fonte": "teste"} for k, (v, u) in sorted(x.items())}

        boa = med(agua=(49, 2), alimentacao=(2150, 60), energia=(0.19, 0.01), saude=(0.86, 0.02),
                  carbono=(1.5, 0.2), agua_captada=(0.30, 0.03), habitat_ocupado=(0.62, 0.02), captura_animal=(0.8, 0.1))
        pn = ponto_neutral(boa)
        self.assertEqual(pn["nivel"], "OURO")
        self.assertTrue(0.0 <= pn["n_eq"] <= 1.0)
        with self.assertRaises(VetoBiofisico):
            ponto_neutral(dict(boa, **med(carbono=(6.5, 0.5), agua_captada=(0.62, 0.05), habitat_ocupado=(0.88, 0.03), captura_animal=(1.6, 0.1))))

    def test_g4_stock_parado(self) -> None:
        """10 000 aparelhos × 55 ± 20 kgCO2e = 550 ± 200 t; × 3 EUR = 30 000 EUR; sai com carimbo de CENÁRIO e etiqueta ASSUMIDO"""
        r = resgate_de_stock_parado(G(10000.0, 0.0, "aparelho"), G(55.0, 20.0, "kgCO2e/aparelho"), G(3.0, 0.0, "EUR/aparelho"))
        self.assertAlmostEqual(r["co2_evitado_t"], 550.0, places=9)
        self.assertAlmostEqual(r["u_co2_evitado_t"], 200.0, places=9)
        self.assertAlmostEqual(r["fundo_eur"], 30000.0, places=9)
        self.assertEqual((r["estado"], r["etiqueta"], r["carimbo"]), ("CENARIO", "ASSUMIDO", CARIMBO))

    def test_g4_logistica_massa_e_contentor(self) -> None:
        """massa: 10 ± 28 kg de diferença é CONFORME, 300 ± 28 kg é ALERTA_MASSA_EM_FALTA; contentor: CSQU3054383 confere, CMAU-774120-9 não"""
        carga = G(24000.0, 20.0, "kg")
        self.assertEqual(balanco_de_massa(carga, G(23990.0, 20.0, "kg"))["estado"], "CONFORME")
        falta = balanco_de_massa(carga, G(23700.0, 20.0, "kg"))
        self.assertEqual(falta["estado"], "ALERTA_MASSA_EM_FALTA")
        self.assertAlmostEqual(falta["incerteza_kg"], math.sqrt(800.0), places=9)
        self.assertEqual(balanco_de_massa(carga, G(24.3, 0.02, "t"))["estado"], "ALERTA_MASSA_A_MAIS")
        self.assertEqual(balanco_de_massa(carga, G(23700.0, 20.0, "kg"), G(290.0, 10.0, "kg"))["estado"], "CONFORME")
        mesma = G(24000.0, 20.0, "kg", fonte="a_mesma_balanca")  # a mesma balança nas duas pesagens: o erro dela não conta duas vezes
        self.assertEqual(balanco_de_massa(mesma, mesma)["limiar_kg"], 0.0)
        self.assertTrue(iso6346_valido("CSQU3054383") and iso6346_valido("csqu 305438-3"))
        self.assertFalse(iso6346_valido("CSQU3054384") or iso6346_valido("CMAU-774120-9") or iso6346_valido("ABC123") or iso6346_valido(None))
        self.assertEqual(iso6346_digito("CMAU774120"), 5)

    def test_g4_logistica_certificados(self) -> None:
        """Certificado «SIR» do navio, «fecho circular certificado» e «prova de mestria»"""
        self.skipTest("na outra suite são texto fixo; não diz que norma é cada um nem o que se mede: não entra sem alguém dizer qual é a norma")

    def test_g4_medicina(self) -> None:
        """criança de 12 kg: 180 mg de paracetamol passa; 1800 mg (erro de vírgula) é vetado; fármaco fora do cofre é vetado"""
        peso = G(12.0, 0.5, "kg")

        def plano(mg: float) -> str:
            return verificar_plano(730, peso, [{"produto": "xarope", "farmaco": "paracetamol_oral", "dose": G(mg, 0.0, "mg"),
                                               "intervalo": G(6.0, 0.0, "h"), "tomas_24h": 4, "hora": 0.0}])["estado"]

        self.assertEqual((plano(180.0), plano(1800.0)), ("SEM_VETO", "VETADO"))
        with self.assertRaises(VetoFarmacologico):
            verificar_toma("xarope_desconhecido", 730, peso, G(5.0, 0.0, "mg"), G(6.0, 0.0, "h"), 4)

    def test_g4_robotica(self) -> None:
        """drone: 1,4 kWh cabem em 5,2 úteis e há assinatura -> AUTORIZADA; sem assinatura -> recusada; 7,5 kWh -> recusada mesmo assinada"""
        sk = chave_demo("posto/enfermeira_chefe")
        quem = {"enfermeira_chefe": ed_publica(sk).hex()}
        missao = {"missao": "levar vacinas", "destino": "aldeia_norte"}
        ha, w, t = G(6.5, 0.6, "kWh"), G(700.0, 50.0, "W"), G(120.0, 10.0, "min")
        self.assertEqual(orcamento_de_missao(w, t, ha, missao, selar(missao, sk), quem)["estado"], "AUTORIZADA")
        self.assertEqual(orcamento_de_missao(w, t, ha, missao, None, quem)["estado"], "RECUSADA_SEM_TRAVA_HUMANA")
        self.assertEqual(orcamento_de_missao(w, t, ha, dict(missao, destino="outro"), selar(missao, sk), quem)["estado"], "RECUSADA_SEM_TRAVA_HUMANA")
        self.assertEqual(orcamento_de_missao(G(1500.0, 100.0, "W"), G(300.0, 20.0, "min"), ha, missao, selar(missao, sk), quem)["estado"],
                         "RECUSADA_ENERGIA_INSUFICIENTE")
        self.assertEqual(orcamento_de_missao(G(1000.0, 80.0, "W"), G(270.0, 20.0, "min"), ha, missao, selar(missao, sk), quem)["estado"],
                         "REVISAO_HUMANA_NO_LIMITE")

    def test_g4_trabalho_habitacao_cultura(self) -> None:
        """Trabalho, habitação e cultura («liquidado», «amortizada sem juros», «100% direto ao criador»)"""
        self.skipTest("na outra suite são 3 frases fixas: não há grandeza para medir nem dinheiro a mexer; não entra sem decisão de quem manda")

    def test_g4_educacao_ciencia(self) -> None:
        """ciência: um resultado nulo também se sela e publica (PROVA/1 com o mínimo pré-selado não atingido -> NAO_CUMPRIDO)"""
        m = _Mundo()
        prova = Prova1(m.livro, chave_demo("teste/laboratorio"), "laboratorio_de_teste")
        self.assertEqual(prova.pre_registar("NULO-1", "a bomba dá 20 m3 por dia?", "água elevada por dia", "m3/dia", 20.0, ["folha_do_contador"], 0), "PRE_SELADA")
        self.assertEqual(prova.preencher("NULO-1", "folha_do_contador", b"folha do contador (bytes de teste)", 1), "PREENCHIDO")
        fecho = prova.fechar("NULO-1", m.leituras("NULO-1", (11.0, 10.8, 11.3), 2, "m3/dia"), m.fontes, 2)
        self.assertEqual((fecho["estado"], fecho["resultado"]), ("PROVA1_FECHADA", "NAO_CUMPRIDO"))
        self.assertTrue(prova.conferir("NULO-1", {"folha_do_contador": b"folha do contador (bytes de teste)"}, m.fontes))
        self.assertTrue(selo_ok(prova.registos["NULO-1"]["fecho"]["dados"], fecho["selo"], {ed_publica(chave_demo("teste/laboratorio")).hex()}))


_GRUPOS_DE_TESTE = {"g1": "1. VETOS: dimensional e termodinâmico", "g2": "2. LEDGER E SESSÕES: 1 byte, passado reescrito, sessão de uso único",
                    "g3": "3. ESTORNO AOS 15 DIAS, CARTEL E CONFIANÇA BAIXA", "g4": "4. DOMÍNIOS"}


def testes() -> int:
    """Corre os testes com o unittest e imprime sem tempos: a mesma corrida dá sempre a mesma saída e o mesmo hash."""
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")  # type: ignore[attr-defined]
    linhas: List[str] = []

    def p(txt: str = "") -> None:
        linhas.append(txt)
        print(txt)

    casos = sorted(unittest.defaultTestLoader.loadTestsFromTestCase(TestesKonfirmu), key=lambda c: c.id())
    p(f"KONFIRMU CALC v{VERSAO} — python3 konfirmu_calc.py --testes")
    p(f"{len(casos)} testes em unittest: os 4 grupos que o «Prompt Final» da outra suite pede, corridos sobre este ficheiro")
    conta, grupo = {"OK": 0, "FALHOU": 0, "SALTADO": 0}, ""
    for caso in casos:
        nome = caso.id().rsplit(".", 1)[-1]
        if nome.split("_")[1] != grupo:
            grupo = nome.split("_")[1]
            p("")
            p(_GRUPOS_DE_TESTE.get(grupo, grupo))
        res = unittest.TestResult()
        caso.run(res)
        if res.failures or res.errors:
            estado, extra = "FALHOU", " — " + (res.failures or res.errors)[0][1].strip().splitlines()[-1]
        elif res.skipped:
            estado, extra = "SALTADO", " — " + res.skipped[0][1]
        else:
            estado, extra = "OK", ""
        conta[estado] += 1
        p(f"  [{estado}] {nome[5:]}: {caso.shortDescription() or ''}{extra}")
    p("")
    p(("TESTES VERDES" if not conta["FALHOU"] else "TESTES VERMELHOS") + f": {len(casos)} testes · {conta['OK']} OK · "
      f"{conta['FALHOU']} falhados · {conta['SALTADO']} saltados (só texto na outra suite: nada para medir)")
    print("sha256 desta saída (todas as linhas acima): " + h256("\n".join(linhas).encode("utf-8")))
    return 0 if not conta["FALHOU"] else 1


def principal(argv: Sequence[str]) -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")  # type: ignore[attr-defined]
    if list(argv) == ["--demo"]:
        try:
            return demo()
        except Exception as erro:  # nada de verde por omissão: se rebentar, diz e sai com erro
            print(f"VERMELHO: o demo rebentou com {type(erro).__name__}: {erro}")
            return 1
    if list(argv) == ["--assinar-limiar"]:
        return _filho_assinar()
    if list(argv) == ["--cerimonia"]:
        c = cerimonia()
        print("\n".join(c["checklist"]))
        print("chave pública do cofre: " + c["pub"])
        print("[VALIDAR] as partes não se imprimem: nesta versão ficam em memória e perdem-se ao sair; falta o canal de entrega a cada câmara.")
        return 0
    if list(argv) == ["--auditoria"]:
        lv = LedgerImutavel(chave_demo("notario/auditoria"))
        for i in range(20):
            lv.registar(i, "PAGAMENTO", {"n": i})
        a, n = auditoria(lv, 100)
        print(("VERDE" if a == n else "VERMELHO") + f": {a}/{n} adulterações apanhadas")
        return 0 if a == n else 1
    if len(argv) == 2 and argv[0] == "--benchmark":
        try:
            with open(argv[1], "rb") as fh:
                dados = json.loads(fh.read().decode("utf-8"))
            print("\n".join(relatorio_benchmark(benchmark_v3(dados["fichas"], dados["perguntas"], float(dados.get("meta", 0.99))))))
        except (OSError, ValueError, KeyError, TypeError) as erro:
            print("RECUSADO_FICHEIRO_ILEGIVEL: " + type(erro).__name__ + ' — formato: {"fichas": [{"id","facto","fonte","data","nao_garante","chaves"}], "perguntas": [{"pergunta","esperado","prosa"}]}')
            return 1
        return 0
    if 2 <= len(argv) <= 4 and argv[0] == "--verificar-externo":  # v2.8: --verificar-externo FICHEIRO [CHAVE_DO_NOTARIO] [CABECA_PUBLICADA]
        try:
            with open(argv[1], "rb") as fh:
                r = verificar_externo(json.loads(fh.read().decode("utf-8")), *(argv[2:4]))
        except (OSError, ValueError) as erro:
            r = {"estado": "RECUSADO_PACOTE_ILEGIVEL", "motivo": type(erro).__name__}
        print(canon(r).decode("utf-8"))
        return 0 if r["estado"] == "CONFERE" else 1
    if list(argv) == ["--testes"]:
        return testes()
    if list(argv) == ["--explica"]:
        aula = professora()
        print("\n".join(aula))
        print("sha256 desta explicação: " + h256("\n".join(aula).encode("utf-8")))
        return 0
    if list(argv) == ["--kpkg"]:
        print(canon(kpkg_emitir("AFRICA_2030", entradas_africa_2030(), chave_demo("emissor/comunidade"))).decode("utf-8"))
        return 0
    if len(argv) == 2 and argv[0] == "--consome":
        try:
            with open(argv[1], "rb") as fh:
                r = kpkg_consumir(json.loads(fh.read().decode("utf-8")))
        except (OSError, ValueError) as erro:
            r = {"estado": "PACOTE_ILEGIVEL", "motivo": f"{type(erro).__name__}: {erro}"}
        print(canon(r).decode("utf-8"))
        return 0 if r["estado"] == "REPRODUZIDO" else 1
    if len(argv) == 2 and argv[0] == "--ler-oraculos" and re.fullmatch(r"\d{4}-\d{2}-\d{2}", argv[1]):
        print(canon(ler_oraculos(argv[1], chave_demo("leitor"))).decode("utf-8"))  # [VALIDAR] em produção, a chave de quem lê
        return 0
    if len(argv) == 2 and argv[0] == "--cura":
        try:
            r = gateway_cura_verificar_ficheiro(argv[1])
        except (OSError, ValueError) as erro:
            r = {"estado": "PACOTE_ILEGIVEL", "motivo": type(erro).__name__}
        print(canon(r).decode("utf-8"))
        return 0 if r["estado"] == "REPRODUZIDO" else 1
    if argv and argv[0] == "--selo" and len(argv) == 4:
        try:
            with open(argv[1], "rb") as fh:
                ok_s = gateway_selo_verificar(fh.read(), argv[2], argv[3])
        except OSError:
            ok_s = False
        print("VALIDO" if ok_s else "INVALIDO")
        return 0 if ok_s else 1
    if list(argv) == ["--base-mae"]:  # v3.0: as 5 baterias da base-mãe sobre esta calculadora
        tudo = True
        for desc_b, pilar_b, teste_b, _prec_b, _min_b, _sai_b in _BASE_MAE_BATERIAS:
            ok_b, r_b = base_mae_confere(teste_b)
            tudo = tudo and ok_b
            print(f"{desc_b} {pilar_b:<4} {teste_b:<22} {r_b['ok']}/{r_b['total']}  saída {r_b['saida'][:16]}…  " + ("CONFERE" if ok_b else "NÃO CONFERE"))
        print("TUDO CONFERE" if tudo else "HÁ DIFERENÇAS")
        return 0 if tudo else 1
    if list(argv) == ["--fichas"]:
        c = cofre()
        print(f"cofre sha256 {hash_cofre()} · {len(c)} fichas")
        for k in sorted(c):
            print(f"  {k}")
        return 0
    print("uso: python3 konfirmu_calc.py --demo | --testes | --cerimonia | --auditoria | --verificar-externo FICHEIRO [CHAVE] [CABECA] | --benchmark FICHEIRO | --explica | --kpkg | --consome FICHEIRO | --cura FICHEIRO | --selo FICHEIRO ASSINATURA_HEX PUB_HEX | --fichas | --base-mae | --ler-oraculos AAAA-MM-DD")
    return 2


if __name__ == "__main__":
    sys.exit(principal(sys.argv[1:]))
