# KCP — Konfirmu Claim Protocol

Toda a afirmacao factual carrega a sua prova — ou a sua honestidade.

## O que NAO garante (lido primeiro, como manda a casa)

- NAO elimina alucinacoes: elimina afirmacoes sem prova. O que nao se verifica, nao passa.
- NAO garante matematicamente que nenhum operador ultrapassa limites: torna a violacao visivel, lenta e cara — e a conformidade a opcao mais barata.
- NAO promete que a fonte tenha razao: garante integridade e proveniencia.
- SEM_COBERTURA honesto e comportamento conforme — nao e falha.

## O que e

KCP/0.1 define o minimo para uma afirmacao factual ser recebida como usavel:
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

## Nao acredites — verifica

Cada ficheiro tem o seu hash em SHA256SUMS.txt. Re-computa:

shasum -a 256 -c SHA256SUMS.txt
