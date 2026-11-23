# Stack Tecnológico — Konfirmu Claim Protocol (arquitectura em 5 camadas)

> Regra de ouro: cada entrada leva o seu estado REAL e a prova (ou a pendência declarada).
> Estados: **PROVADO** (executado e com saída colada) · **PARCIAL** (parte provada, parte não) ·
> **ROADMAP** (desenhado, não implementado) · **PENDENTE** (acto externo por fazer).
> Data: 2026-11-23 · fontes: motor v3.0.0 (sha256 `529098c6…`) + PROVA.md + auditorias da casa.

## 1. Camada Física e Transporte (como os bits viajam)

| Tecnologia | Estado | Prova / nota honesta |
|---|---|---|
| Ethernet · Wi-Fi · TCP/IP | PROVADO (infra) | usados por toda a infra; não são código deste repositório |
| QUIC (HTTP/3) | **PROVADO (infra)** | activado 23-11 no VPS: Caddy v2.11.9 escutava UDP 443; regra ufw 443/udp adicionada; handshake QUIC de máquina externa → OK, ALPN negociado `h3` (aioquic) |
| Bluetooth · LoRa | ROADMAP | desenhados para o produto offline; nenhuma implementação selada na casa (varrredura 23-11: zero evidência) |

## 2. Camada de Segurança e Identidade (como se protege o canal)

| Tecnologia | Estado | Prova / nota honesta |
|---|---|---|
| Ed25519 (RFC 8032) | **PROVADO** | Wycheproof 210/210 · RFC 8032 TEST 1 · 5/5 vectores ×2 rondas (oráculo-pai, 22-11) |
| FROST (RFC 9591) | **PARCIAL** | ensaio E.1 VERDE (sig 36282629…); o FROST/1 da casa ≠ RFC no fio — declarado no motor (P44 vs P53) |
| TLS 1.3 | PROVADO (infra) | usado nos servidores; não é código do motor |
| RFC 3161 (carimbo temporal) | **PROVADO** | executado 23-11: `openssl ts -query -data konfirmu_calc.py` → Free TSA (freetsa.org), granted 05:13:01 GMT; `openssl ts -verify -CAfile` → **Verification: OK**; recibo em `rfc3161.tsr` (sha256 `df182d72…`) |

## 3. Camada de Dados e Web (como se lê e corre o código)

| Tecnologia | Estado | Prova / nota honesta |
|---|---|---|
| JSON canónico (RFC 8785) | PARCIAL | selos com chaves ordenadas/compactos (determinísticos); conformidade RFC 8785 estrita não auditada |
| CBOR · COSE | PARCIAL | COSE_Sign1 no demo (primeira-aldeia, SAIDA-REAL.txt) · exame CBOR anexo A no oráculo-pai |
| HTML5 offline | **PROVADO** | fichas-criancas.html · neuro_cartoes_offline.html (zero rede, zero CDN, SHA-256 no ficheiro) |
| WebAssembly (Wasm) | ROADMAP | sem build selado na casa |
| IPFS | PARCIAL/ROADMAP | CIDv0/CIDv1 no selo-de-obra (pacote 2026-11-22); sem nó IPFS real |

## 4. Camada de IA e Ferramentas (como os agentes falam com o mundo)

| Tecnologia | Estado | Prova / nota honesta |
|---|---|---|
| MCP (Model Context Protocol) | **PROVADO** | mcp_konfirmu.py — JSON-RPC 2.0 sobre stdio, 5 ferramentas (m1_dose, m2_interacao, m3_cadeia_frio, consenso, selar_facto), importa o motor com verificação de hash, recibo Ed25519 por resposta |

## 5. Camada de Verdade Determinística e Prova Física (onde nasce o Konfirmu Claim Protocol)

| Peça | Estado | Prova / nota honesta |
|---|---|---|
| Metrologia (GUM) | **PROVADO** | GUM H.2 do BIPM conferido · 1/(1,0±0,3) resolvido EXACTO: 89,14 % (a casa corrigiu-se a si própria) |
| Regras declarativas | **PROVADO** | vetos com fonte citada: dose pediátrica P39 (15 mg/kg, farmacopeia) · cadeia de frio M3 (2–8 °C, OMS) |
| Veto físico (Verde/Vermelho) | **PROVADO** | demo: dose 10× → VERMELHO VETO · frio 11,0 °C → «medicamento morto» (provas_autoteste.txt) |
| Recibos offline auditáveis | **PROVADO** | cadeia encadeada por hash (raiz 9b1779e3…) · ledger imutável, auditoria 30/30 · verificação < 1 s, offline |

## O que NÃO garante

- «PROVADO» refere-se à execução da casa (23-11), nunca a certificação de terceiros.
- As peças ROADMAP/PENDENTE estão declaradas como tal — não são prometidas.
- A camada 5 prova o MECANISMO com dados sintéticos; não diagnostica nem substitui profissionais de saúde.
