# Konfirmu Claim Protocol — Whitepaper v1.0

> Primeira parte (autoria da casa) · 2026-11-23 · Europe/Berlin · licença EUPL-1.2.
> Regra de ouro: cada afirmação leva à sua prova ou é declarada como [VALIDAR]. Este documento
> não é aconselhamento jurídico nem financeiro.

## 1. Sumário executivo

A Konfirmu é uma infraestrutura europeia onde a **inteligência artificial propõe e o humano
confirma**. Cada artefacto carrega um selo de proveniência (quem, quando) e um selo de frescura
(validade das fontes), e declara o que NÃO garante. A tese ambiental da casa: **«aprender online
uma vez, servir offline para sempre»** — o registo verifica-se no aparelho, sem rede; a internet
é usada uma única vez, na origem, para ancorar a génese num notário público.

Pergunta fundadora: **como pode uma família conferir um registo quando não tem acesso à
internet?** — por exemplo, o registo de vacinação de uma criança numa aldeia de Moçambique.

## 2. O problema

A fricção burocrática pesa sobre os mais pobres: registos sem prova, fontes sem data, decisões
sem rasto. A resposta não é mais burocracia nem mais confiança cega — é **prova re-executável**:
qualquer pessoa, em qualquer aparelho, confere o registo sem confiar em quem o emitiu.

## 3. O protocolo — CLAIM → PROOF → VERIFY

O Konfirmu Claim Protocol define o mínimo para uma afirmação factual ser recebida como usável:

1. **CLAIM** — a afirmação, com fonte citada e data.
2. **PROOF** — o selo: hash, assinatura Ed25519, cadeia de eventos, leituras com incerteza.
3. **VERIFY** — re-execução na máquina de quem recebe, em menos de 1 s, offline.

Sem terceira via: **VERIFICADO ou SEM_COBERTURA**. Nenhuma acção executa sem
CONFIRMAR / MODIFICAR / NÃO — o humano é o último elo, sempre.

## 4. O motor determinístico

`konfirmu_calc.py` v3.0.0 — um ficheiro, só biblioteca-padrão Python, sem rede, sem dependências.

- sha256 do ficheiro: `529098c652ee8234960d69383e308f60db6a5df8ea6bdae578b538eb806e80cf`
- Bateria completa re-executada (23-11): **TUDO VERDE 247/247** · saída selada `7ef2d64e…` (PROVA.md)
- Metrologia GUM: propagação de incerteza de 1.ª ordem com as limitações declaradas — a casa
  mediu e publicou a descoberta honesta: 1/(1,0±0,3) prometia 95 % e cobre **89,14 %**; o valor
  exacto (95 % → [0,6288 ; 2,4143], média inexistente) está resolvido pelo oráculo-pai.
- Vetos com fonte citada: dose pediátrica (teto 15 mg/kg, farmacopeia) · cadeia de frio 2–8 °C
  (OMS) — dose 10× → VERMELHO VETO, nunca silêncio.
- Auditoria do ledger imutável: 30/30 adulterações apanhadas (SAIDA-REAL.txt).

## 5. A cadeia da garantia (prova em cada passo)

FONTE → PACK → MOTOR → CONSENSO → PROPOSTA → CONFIRMAÇÃO HUMANA → RECIBO → LEDGER ÍNTEGRO →
FRESCURA VERIFICADA. Cada passo produz hash; um passo saltado = selo PROVISÓRIO, nunca pleno.

## 6. Prova de data (notários públicos, sem confiar em nós)

| Notário | O que atesta | Data |
|---|---|---|
| Bitcoin (OpenTimestamps) | `GENESIS_STAMP_v4.json` sha256 `3cfe8000…` → cabeçalho do bloco **976735** | 2026-11-20 14:17:33 UTC |
| Bitcoin (OpenTimestamps) | `MANIFESTO_HASHES_2026-11-20.txt` sha256 `01721dfa…` → bloco **976760** | 2026-11-20 17:32:00 UTC |
| RFC 3161 (FreeTSA) | `konfirmu_calc.py` — carimbo `rfc3161.tsr`, `openssl ts -verify` → OK | 2026-11-23T05:13:01Z |
| BOIP i-DEPOT | depósito **n.º 162925** | 2026-09-06 |
| BOIP i-DEPOT | depósito **n.º 164391** | 2026-10-21 |

Os 4 txid de calendário (blocos 976735/976737/976760/976761) foram conferidos contra a API
pública mempool.space, com raízes de Merkle byte a byte (entregas/2026-11-22-auditoria-4-carimbos/).

## 7. Arquitectura (5 camadas)

Ver STACK-TECNOLOGICO.md — cada peça com estado real: PROVADO (Ed25519, MCP, GUM, veto físico,
recibos offline, HTML5 offline, RFC 3161, QUIC no VPS) · PARCIAL (FROST, CBOR/COSE, JSON canónico)
· ROADMAP (Bluetooth/LoRa, Wasm) — nada é prometido sem prova.

## 8. Moeda — a posição da casa (não emitir; verificar)

O mundo tem moedas a mais; falta-lhes o selo. A Konfirmu **não emite criptomoeda**: é o
**verificador** — proof-of-reserves que o cliente confere sozinho (PoR v0.1), escrow condicionado
a prova física, e a «moeda do povo» experimental: emissão **só contra entrega assinada**, zero
premine, zero juros, teto de débito (prova em entregas/2026-11-22-pai-da-bitcoin, digest
`f437f1b8…`). MiCA: citado como enquadramento, não como parecer — [VALIDAR] com jurista; para o
rumo actual (sem emissão ao público) não há obrigação de whitepaper MiCA.

## 9. Desambiguação e trabalho anterior

A sigla «KCP» é usada publicamente pelo **Knowledge Context Protocol** (Cantara,
github.com/Cantara/knowledge-context-protocol, especificação pública desde 03-2026) — **citado
aqui como trabalho anterior**. Este protocolo usa por extenso **«Konfirmu Claim Protocol»** e não
regista nem usa a sigla sozinha em público (decisão do fundador, 23-11).

## 10. O que NÃO garante

- «Selado» ≠ «verdadeiro»; não diagnostica nem substitui profissionais de saúde.
- Depósitos i-DEPOT provam data de depósito — não patente nem aprovação regulatória.
- A auto-avaliação ECSS-Q-ST-80C é de primeira parte — não é certificação ESA/ECSS.
- Dados de demonstração são SINTÉTICOS e marcados; nenhum dado real de terceiros circula sem ordem.
- Publicação do DOI (Zenodo) é acto externo pendente do fundador.

## 11. Como verificar

```sh
shasum -a 256 -c SHA256SUMS.txt                 # integridade deste repositório
python3 konfirmu_calc.py --demo                 # 247/247
openssl ts -verify -in anchors/konfirmu_calc.tsr -data konfirmu_calc.py \
  -CAfile anchors/cacert.pem -untrusted anchors/tsa.crt   # Verification: OK
```

Contacto oficial: **admin@dpsindustrial.nl** · Fundador: David Peres da Silva.
