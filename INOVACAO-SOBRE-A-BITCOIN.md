# Porque a Konfirmu é mais inovadora que a Bitcoin

> Posição oficial da casa (ordem do fundador, 23-11: «não quero a Konfirmu associada à Bitcoin,
> mas sim algo inovador»). Regra de ouro: cada afirmação tem prova no chão.

## A frase

A Bitcoin provou que se pode **ordenar dinheiro sem confiar em ninguém**. A Konfirmu prova que se
pode **verificar o mundo físico sem confiar em ninguém** — e é aí que está a inovação. A Bitcoin é
um dos nossos relógios públicos; não é a nossa identidade.

## As 8 inovações (cada uma com prova executada)

| # | Inovação | Bitcoin | Konfirmu | Prova no chão |
|---|---|---|---|---|
| 1 | Lastro | electricidade queimada (PoW) | **facto físico**: entrega assinada, dose medida, frio conferido | emissão-girafinhas digest `84f52e71…` · pai-da-bitcoin `f437f1b8…` |
| 2 | Incerteza | não mede nada | **metrologia GUM em cada leitura** (± declarado; cobertura exacta publicada) | 1/(1,0±0,3) = 89,14 % descoberto e resolvido |
| 3 | Consenso | voto de mineiros | **humano confirma**: IA propõe, humano CONFIRMA/MODIFICAR/NÃO | motor — bypass = bug crítico |
| 4 | Frescura | inexistente | **selo de frescura**: validade e idade das fontes, sempre visível | regra 7 da casa |
| 5 | Anti-pirâmide | halving + escassez | **zero premine, zero juros, teto de débito** — a dívida é finita e visível | MoedaDoPovo: fantasma/teto RECUSADOS |
| 6 | Veto físico | inexistente | **Verde/Vermelho com fonte citada** (dose 10× → VETO; frio 11 °C → «medicamento morto») | provas_autoteste.txt |
| 7 | Âncoras | é a âncora dos outros | **múltiplas e substituíveis**: Bitcoin + RFC 3161 + BOIP + P3 híbrido PQC (roadmap) | blocos 976735–976761 · rfc3161.tsr · i-DEPOT 162925/164391 |
| 8 | Offline | precisa de rede para tudo | **verificação no aparelho, sem rede** — aprender online uma vez, servir offline para sempre | verificador_offline.html · fichas-criancas.html |

## O que NÃO reclamamos

Não reclamamos a segurança de rede da Bitcoin (17 anos de hashpower não se copiam) — e é por isso
que a usamos como relógio público, entre outros. Não reclamamos «melhor moeda» — a nossa moeda do
povo é crédito de PROVA com teto, não activo especulativo (MiCA [VALIDAR]).

## Como se verifica

`shasum -a 256 -c SHA256SUMS.txt` · `python3 konfirmu_calc.py --demo` (247/247) ·
`openssl ts -verify -in anchors/konfirmu_calc.tsr -data konfirmu_calc.py -CAfile anchors/cacert.pem -untrusted anchors/tsa.crt`
