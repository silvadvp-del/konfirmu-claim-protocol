# Correções de referência: o selo estrito e o livro-razão que não perde registos

Janela ZCode (GLM) `ZCODE-CHAVE-V3-20261121` · unidade 51 · 27-11-2026.

**Estado: BLOCKED.** Sem número KON (esta janela não tem rota para o Linear e não inventa números).
O motor v3.0.0 não está na `main` deste repositório: vive no PR #1410 e no repositório público.
Falta a revisão do dono da frente do núcleo. **Nada aqui altera o motor.**

## O que resolve

Três defeitos do motor público `konfirmu_calc.py` v3.0.0, cada um reproduzido em `provar_defeitos.py`:

1. **O selo aceita bits trocados no seu texto.** Medido: 183, de 2 528. A entrada `alg` (nome e valor)
   nunca é lida por quem verifica (110); `pub` e `sig` aceitam maiúsculas (73). Em nenhum se muda o
   objecto selado, nem a chave, nem a assinatura.
2. **Uma escrita curta no disco devolve «gravado» sem ter gravado.** `os.write` pode devolver menos
   bytes sem erro; o motor não confere o valor devolvido.
3. **Um disco cheio ou uma escrita cortada deixam o livro encravado para sempre.** Com o disco cheio,
   o bloco fica em memória sem estar no disco; a escrita seguinte faz um buraco; ao reler,
   `LEDGER_CORROMPIDA`. Com a última linha rasgada, `LEDGER_ILEGIVEL`.

## O que é cada ficheiro

| Ficheiro | sha256 | O que é |
|---|---|---|
| `correcoes_ledger.py` | `a60539a44145953ca457bcfc4c2d3b1d481db84137a45a1db37e414d036e6dbf` | as correcções, por cima do motor |
| `provar_defeitos.py` | `052806583b3786f09dd5f4a416992947763093febbbe775729a83dde4d2d9293` | reproduz os defeitos no motor tal como está |
| `provar_correcoes.py` | `641e417ab28bb9c3f9c801e105c88172dea5807f898025d6a0256d515db7d29e` | a bateria das correcções (24 verificações) |
| `sabotar_correcoes.py` | `3e516aef861b75884ab4488a8d2b60b2d95f46560326dc1c53876927f1123e0c` | parte 9 defesas, uma a uma, em cópias (só macOS: usa `sandbox-exec`) |
| `provas/` | — | as saídas, tal como saíram |

## Como repetir

O motor não está neste repositório. Vai buscá-lo onde ele está:

```sh
git clone https://github.com/silvadvp-del/konfirmu-claim-protocol.git
cd konfirmu-claim-protocol && git checkout 51df0a7ef55ab6fce4c6c44a338015c4286ab68d && cd ..
python3 -I -B tools/correcoes_ledger/provar_defeitos.py  konfirmu-claim-protocol/konfirmu_calc.py /tmp
python3 -I -B tools/correcoes_ledger/provar_correcoes.py konfirmu-claim-protocol/konfirmu_calc.py tools/correcoes_ledger /tmp
```

Os dois roteiros recusam-se a correr se o hash do motor não for
`529098c652ee8234960d69383e308f60db6a5df8ea6bdae578b538eb806e80cf`.

## Resultado medido (27-11-2026, macOS, Python 3.13, caixa de areia sem rede)

| O que | Resultado |
|---|---|
| Defeitos no motor | 16 de 16 conforme o esperado; duas corridas iguais |
| Correcções | 24 de 24; duas corridas byte a byte iguais. Hash da saída: `7a8da36b2be0a840e291582b2a4a6e1ecc1626b1a7109f846f14d4997427c432` |
| Encaixa no motor | cinco registos: blocos, hashes e bytes do ficheiro iguais aos de `LedgerPersistente` |
| Selo estrito | 2 528 bits trocados: 0 aceites |
| Sabotagem | 9 defesas partidas, 9 apanhadas (S01_sem_reler_o_disco, S02_sem_desfazer_a_memoria, S03_sem_cortar_o_ficheiro, S04_cauda_sem_conferir_a_cadeia, S05_isola_sem_cortar, S06_sem_guardar_os_bytes_rasgados, S07_carrega_sem_conferir, S08_selo_sem_o_alg, S09_selo_sem_minusculas); controlo neutro: VIVO |

## O que não é

- **Não é um remendo ao motor.** `LedgerSegura` e `selo_estrito` são uma referência. Para o motor
  ficar corrigido, `LedgerPersistente` e `selo_ok` têm de mudar no próprio motor — no PR #1410, ou no
  repositório público. É decisão de quem guarda o núcleo.
- **Não resolve o recuo do relógio.** Não está no motor público, que não lê o relógio.
- **Não há reserva de espaço em disco.** Com o disco cheio, o registo dá erro em vez de se perder.
- **Altera o comportamento ao arrancar:** uma cauda rasgada passa a ser isolada (num ficheiro ao lado,
  com o hash) em vez de travar. Quem achar que deve continuar a travar, que o diga na revisão.
