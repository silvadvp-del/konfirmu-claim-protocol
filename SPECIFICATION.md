# Konfirmu Claim Protocol — Wire & Receipt Specification (PROVA/1)
**Version:** `3.0.0`
**Date:** `2026-11-23`
**License:** `EUPL-1.2`
**Prior Art:** BOIP i-DEPOT certificates **no. 162925** (`06-09-2026`) & **no. 164391** (`21-10-2026`).
**Name disambiguation:** the acronym «KCP» is used publicly by the earlier *Knowledge Context
Protocol* (Cantara, spec public since 03-2026), cited as prior work; this protocol uses the full
name «Konfirmu Claim Protocol» in public and does not register the bare acronym.
**Not for treatment decisions:** this protocol and its cartridges were not made to diagnose or to
treat. The paediatric dose cartridge is a worked example of a calculation checked against declared
limits; it is not clinical advice. *(PT: não serve para decidir tratamentos.)*

> The key words **"MUST"**, **"MUST NOT"**, **"REQUIRED"**, **"SHALL"**, **"SHALL NOT"**,
> **"SHOULD"**, and **"OPTIONAL"** are to be interpreted as described in **RFC 2119** and **RFC 8174**.

---

## 1. Purpose & Determinism Invariant
The Konfirmu Claim Protocol defines a deterministic, offline-first verification envelope
(`PROVA/1`) for physical, clinical and scientific measurements.
**Core Invariant:** given identical canonical inputs and an identical cartridge specification,
any conformant implementation in any language **MUST** produce the exact same `SHA-256` digest
bit-for-bit. Reference implementation: `konfirmu_calc.py` v3.0.0
(sha256 `529098c652ee8234960d69383e308f60db6a5df8ea6bdae578b538eb806e80cf`),
validator `kcp_lint.py`, pipeline `kcp_pipeline.py`.

## 2. Canonical Serialization Rules
1. **Encoding:** all text **MUST** be UTF-8 without BOM.
2. **JSON Canonicalization:** envelopes **MUST** follow RFC 8785 (JCS): keys sorted by Unicode
   code point, no inter-token whitespace (`separators=(",", ":")`), numbers rounded to the
   precision declared by the cartridge **prior to hashing**.
3. **Hash:** all digests **MUST** use SHA-256 (FIPS 180-4), lowercase 64-char hex.

## 3. State Machine & Fail-Safe Verdicts
A conformant evaluation **MUST** terminate in exactly one of four mutually exclusive verdicts:

| Verdict | Meaning | Operational consequence |
| :--- | :--- | :--- |
| **OK** | `v ± u` lies inside `[min_allowed, max_allowed]` and invariants hold | permitted |
| **VETO** | `v + u > max_allowed` OR `v - u < min_allowed` (directional worst case) or a safety rule violated | **mandatory hard stop** |
| **SEM_COBERTURA** | uncertainty exceeds threshold, quorum unmet (`k < 5`, `N < 3`), or outside calibrated domain | epistemic abstention; **MUST NOT** guess |
| **RECUSADO** | structural tampering, invalid signature, clock rollback, post-hoc mutation | evidence rejected |

## 4. PROVA/1 Receipt Schema
Every receipt **MUST** contain, prior to computing `digest`:

```json
{
  "kcp_version": "3.0.0",
  "pillar": "WHO_PEDIATRIC_PARACETAMOL_V1",
  "verdict": "OK",
  "summary": "within limits",
  "data": { "value": 14.5161, "unc": 0.1238 }
}
```

- **digest:** SHA-256 of the canonical JSON of the object above.
- **Chain linking (prev_hash):** in sequential logs, entry `n` **MUST** include `prev_hash`
  equal to the `digest` of entry `n-1`; entry `0` **MUST** use `"0" * 64` or a sealed
  genesis hash (the public `/status` chain documents its own genesis marker).
- Note: the "Dia Zero" variant carries `kcp_version: 3.0.0-GENESIS` (candidate
  `ed9f746b…`); this spec is normative for `3.0.0` (`529098c6…`).

## 5. Cryptographic Agility & External Anchoring
1. **Signatures:** implementations **MUST** support Ed25519 (RFC 8032) — proven against the
   official TEST 1 vector in this repository. FROST (RFC 9591) is **PARTIAL/SHOULD**: the E.1
   ensemble is verified, but the house FROST/1 is not the wire RFC format (P44 vs P53 —
   declared in the engine, not hidden).
2. **Temporal anchoring:** receipts **MAY** be anchored externally via RFC 3161 (`.tsr`) and/or
   Bitcoin `OP_RETURN` Merkle proofs without altering the internal `digest`.

## 6. Conformance
A cartridge conforms when `kcp_lint.py` passes all its `test_vectors`; an implementation
conforms when its digests equal the reference for every published test vector (see `cartridges/`
and CI workflow `kcp_cartridge_ci.yml`). "Almost within limits" does not exist: the worst case
decides.


## 7. Reserva Pós-Quântica (PROVA/2-PQ) — sem tocar no núcleo congelado

A versão `3.0.0` NÃO muda. Para envelopes de longo prazo (30–50 anos), fica **reservado** o campo:

```json
{ "schema": "PROVA/2-PQ", "sig_suite": "ED25519+SLH-DSA-SHA2-128s", "digest": "…",
  "signatures": { "classical_ed25519": "…", "post_quantum_slh_dsa": "…" } }
```

- A reserva é um CAMPO NA SPEC — a implementação real de SLH-DSA (FIPS 205) é trabalho de versão
  futura (v4-PQ), com vectores oficiais do NIST, nunca cripto caseira.
- Existe um PROTÓTIPO DIDÁTICO em `kcp_pq_hybrid.py` (Lamport+Merkle, stdlib-only, marcado
  DIDÁTICO — não usar em produção) que demonstra o envelope híbrido de duas camadas.
- SHA-256 permanece adequado (Grover reduz 256→128 bits); SHA-384/SHA3-256 são a opção para os
  envelopes de muito longo prazo — decisão da versão v4-PQ.
