# Konfirmu Claim Protocol

> Infraestrutura **humanitária**: a IA propõe, o humano confirma. O cliente é a família sem
> internet; o excedente é para as girafinhas. Zero premine, zero juros, emissão só contra prova
> física. Manifesto: MANIFESTO-MISSAO.md · Inovação: INOVACAO-SOBRE-A-BITCOIN.md.

Toda a afirmacao factual carrega a sua prova — ou a sua honestidade.

## O que NAO garante (lido primeiro, como manda a casa)

- NAO elimina alucinacoes: elimina afirmacoes sem prova. O que nao se verifica, nao passa.
- NAO garante matematicamente que nenhum operador ultrapassa limites: torna a violacao visivel, lenta e cara — e a conformidade a opcao mais barata.
- NAO promete que a fonte tenha razao: garante integridade e proveniencia.
- SEM_COBERTURA honesto e comportamento conforme — nao e falha.

## O que e

O Konfirmu Claim Protocol 0.1 define o minimo para uma afirmacao factual ser recebida como usavel:
CLAIM → PROOF → VERIFY. Sem terceira via: VERIFICADO ou SEM_COBERTURA.
A prova re-executa-se na maquina de quem recebe, em menos de 1 s, offline.

Autor da disciplina: David Peres da Silva · 2026-11-20 · Konfirmu, Amesterdao
Licenca: EUPL-1.2 · Prioridade declarada: 2026-11-20 (ancora Bitcoin, blocos 976.735/976.737)

## A familia de perfis (v0.1)

- KCP-PAZ — tratados e cessar-fogos com escrow por prova (entregas/2026-11-21-protocolo-da-paz)
- KCP-ACT — a verdade nos actos fisicos, robos e veiculos (entregas/2026-11-21-kcp-act)
- KCP-QR — o contentor fisico: prova offline no QR (este repositorio)
- KCP-GATEWAY — a alfandega automatica, verify-first (este repositorio)
- KCP-CARE — a verdade no cuidado: ISO 13482/15066, RGPD art. 9 (este repositorio)
- KCP-NUCLEAR — o perfil da inspecao: trust, but verify em codigo (este repositorio)

Indice da familia: FAMILIA-KCP.json (5 perfis, hash e dono).

## Desambiguacao e trabalho anterior (importante, 23-11-2026)

- A sigla «KCP» e usada publicamente por um padrao aberto ANTERIOR: o **Knowledge Context
  Protocol** (github.com/Cantara/knowledge-context-protocol; especificacao publica desde
  03-2026). Citado aqui como trabalho anterior.
- Por decisao do fundador, este protocolo usa SEMPRE por extenso **«Konfirmu Claim Protocol»**;
  a sigla sozinha nao e registada (i-DEPOT) nem usada em publico. Nada e apagado; a decisao e
  reversivel.
- O «KCP Agent» da Genesis Digital Solutions (Key Contractual Principles) e um produto de
  terceiros, sem relacao com a Konfirmu.

## O motor

\`konfirmu_calc.py\` v3.0.0 (sha256 \`529098c6…\`, licenca EUPL-1.2) executa a verificacao:

\`\`\`sh
python3 konfirmu_calc.py --demo        # TUDO VERDE 247/247 (prova em PROVA.md)
python3 konfirmu_calc.py --auditoria   # auditoria do ledger imutavel
\`\`\`

## Stack tecnologico

As 5 camadas do protocolo, com estado real por peca (PROVADO/PARCIAL/ROADMAP/PENDENTE):
ver STACK-TECNOLOGICO.md.

## Prova temporal — RFC 3161 (verificacao 100% offline)

O motor esta carimbado pela FreeTSA: **2026-11-23T05:13:01Z**. A prova completa vive em
\`anchors/\` (pedido \`.tsq\`, resposta assinada \`.tsr\`, certificados \`tsa.crt\` + \`cacert.pem\`);
o motor fica na raiz (unica copia, selada em SHA256SUMS.txt). Qualquer auditor confirma offline:

\`\`\`sh
openssl ts -verify -in anchors/konfirmu_calc.tsr -data konfirmu_calc.py \\
  -CAfile anchors/cacert.pem -untrusted anchors/tsa.crt
# esperado: Verification: OK
\`\`\`

## Verificador offline (PWA)

\`verificador_offline.html\` — calcula SHA-256 NO APARELHO (sem rede, sem servidor), compara
com os hash selados acima e mostra as provas de data (Bitcoin + RFC 3161 + BOIP). Com
\`sw.js\` + \`manifest.json\`, instala-se no ecra principal do telemovel e funciona offline.
Prova: 3/3 vectores NIST + sha256 do motor real CONFERE (verificado 23-11).

## Nao acredites — verifica

Cada ficheiro tem o seu hash em SHA256SUMS.txt. Re-computa:

shasum -a 256 -c SHA256SUMS.txt
