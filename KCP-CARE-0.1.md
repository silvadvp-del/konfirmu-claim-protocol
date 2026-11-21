# KCP-CARE/0.1 — a verdade no CUIDADO (perfil do protocolo para agentes de cuidado)

> **Autor da disciplina:** David Peres da Silva · 2026-11-21 · Konfirmu, Amesterdão · Licença EUPL-1.2 · Base: KCP/0.1.
> **Estado:** v0.1 PROPOSTA — [VALIDAR] fechados na fonte (ver FONTES.md); confirmação do jurista fica declarada, não inventada.

## 1. Princípio

Um agente de cuidado (robô físico, assistente de saúde, plataforma de telecuidado) só atua sobre uma
pessoa vulnerável **com prova verificável** — e **nunca sem confirmação humana identificada** nos actos
de cuidado. A mesma regra da casa: a IA propõe, o humano confirma, e a prova corre fora do agente.

## 2. As três mensagens (adaptadas do KCP/0.1)

2.1 **CARE-CLAIM** — o agente declara o que percebeu e o que pretende:
    { claim: { pessoa, contexto, acto_proposto }, autor: chave_publica_do_agente }.
2.2 **CARE-PROOF** — uma de duas, nunca uma terceira:
    { veredicto: VERIFICADO, evidencia: { sensores_selados, selo_do_acto, confirmacao_humana, fonte_do_facto_clinico: hash }, o_que_nao_garante }
    { veredicto: SEM_COBERTURA, nota: 'quem recebe decide', o_que_nao_garante }.
2.3 **CARE-VERIFY** — qualquer pessoa (família, cuidador, autoridade) re-executa a verificação em
    <1s, offline, na própria máquina, sem chave do agente nem do fabricante.

## 3. Confirmação remota (VALIDAR fechado)

- **QUEM:** operador/cuidador/familiar **identificado por chave pública** (Ed25519) — nunca o próprio agente.
- **EM QUANTO TEMPO:** **antes do acto**, fail-closed. Sem confirmação no prazo declarado (60 s por defeito),
  o acto é **recusado e registado**. **Sem timeout que autorize por omissão** — a ausência nunca vale como sim.
- **Emergência** (queda, paragem cardiorrespiratória): o agente pode **sinalizar e proteger** (nunca administrar);
  a autorização de qualquer acto terapêutico é **sempre humana e registada**.

## 4. Segurança de referência (VALIDAR fechado — edições em vigor)

- **ISO 13482:2014** — *Safety requirements for personal care robots* (mobile servant · physical assistant ·
  person carrier). Edição em vigor confirmada na listagem BSI (2024-11).
- **ISO/TS 15066:2016** — *Collaborative robots* (suplementa ISO 10218-1/2). Edição em vigor confirmada na
  listagem NSAI. (Nota: é Technical Specification, não standard pleno.)

## 5. Dados de saúde (VALIDAR fechado — RGPD art. 9)

- **RGPD art. 9.º, n.º 1:** os dados relativos à saúde são uma categoria especial — o processamento é
  proibido, salvo exceção do n.º 2 (consentimento explícito, cuidados de saúde, interesse público, etc.).
- **Regra da casa aplicada:** dados de saúde processam-se **no aparelho**; o que sai é **hash/selo**, nunca o
  dado em claro; **retenção zero por defeito**.
- **[JURISTA]:** a confirmação do enquadramento (consentimento explícito vs. cuidados de saúde) é gesto do
  jurista — fica **declarada como pendente**, não inventada como feita.

## 6. Regras duras do perfil

1. Acto de cuidado sem confirmação humana identificada **não acontece**.
2. Dado de saúde sai do aparelho **só como hash/selo**; zero retenção por defeito.
3. Envelope de segurança público (força, temperatura, proximidade) — fora dele, **veto mecânico**.
4. Auto-relato do erro: o agente de cuidado que errar **confessa com prova** (constituição da casa).
5. Sem terceira via: VERIFICADO ou SEM_COBERTURA; «provavelmente» é proibido.

## 7. O que NÃO garante

- Não substitui o juízo clínico nem o cuidador humano.
- É um perfil normativo + modelo de referência — **não é hardware certificado** (TPM/atestação real = roadmap).
- ISO 13482 / ISO/TS 15066 e RGPD são citados como **referência normativa**, não como certificação obtida.
- O [JURISTA] do art. 9 continua externo (gesto humano).

## 8. Caso fundador (1 linha)

O primeiro acto selado de um agente de cuidado: uma transferência de paciente que **só** se executou
depois de um cuidador identificado confirmar — e a confirmação ficou no hash, verificável pela família.

