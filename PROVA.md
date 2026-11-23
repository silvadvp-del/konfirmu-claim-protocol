# PROVA.md — execução real (janela lead, 2026-11-23, Europe/Berlin)

> Regra 13: cada afirmação tem comando executado + saída colada. Motor: v3.0.0 canónico
> sha256 `529098c6…` (conferido ANTES de executar; base v2.5.1 `7b0680f7…`).

## 1. Bateria completa

```sh
$ python3 konfirmu_calc.py --demo
...
TUDO VERDE: 247/247 verificações
sha256 desta saída (todas as linhas acima): 7ef2d64e5957a9808cdf266fd87474dadefed041d0629cf568dbcaa25557af2e
$ echo EXIT=$?
EXIT=0
```

- Ficheiro executado: `konfirmu_calc.py` — sha256 `529098c652ee8234960d69383e308f60db6a5df8ea6bdae578b538eb806e80cf` (confere).
- Saída integral da corrida: `/tmp/demo_v300_23nov.txt` — sha256 `ee2aeb9f91b36027605da2cc6cc339becf30c8c82d03fd94977d3ac6d1fa8091`.

## 2. Linhagem (zero forks)

- Base: v2.5.1 canónica `7b0680f795d9614bf6de97dae507db3b21d61f99742753ef444565d0b32086a6`.
- Variante "Dia Zero" com Bloco Génese anexado (v3.0.0-genesis `ed9f746b…`) existe como candidata
  isolada em entregas/2026-11-22-kcp-dia-zero — NÃO é este motor.

## 3. Âncoras Bitcoin (verificadas nesta janela com ots v0.8.0)

- `GENESIS_STAMP_v4.json` (sha256 `3cfe8000…`) → `BitcoinBlockHeaderAttestation(976735)`, merkle root `2fe8d000…`
- `MANIFESTO_HASHES_2026-11-20.txt` (sha256 `01721dfa…`) → `BitcoinBlockHeaderAttestation(976760)`, merkle root `43bf5084…`
- 4 transacções de calendário nos blocos 976735/976737/976760/976761, conferidas contra a API
  pública mempool.space (txid + OP_RETURN integrais em entregas/2026-11-22-auditoria-4-carimbos/).

## 4. O que NÃO garante

- Não é dispositivo médico; «selado» ≠ «verdadeiro»; depósitos i-DEPOT provam data, não patente;
- auto-avaliação ECSS é de primeira parte; publicação do repositório e DOI = actos do fundador.
