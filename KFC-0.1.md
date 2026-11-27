# KFC-0.1 — Konfirmu Frugal Compute (roteador frugal)

Protocolo aberto (EUPL-1.2), 27-11-2026. Implementação de referência: `konfirmu_frugal_router.py` (só biblioteca padrão do Python). Ensaio: `python3 -I konfirmu_frugal_router.py --auto-teste`.

## Para que serve

Cada pergunta vai pelo caminho mais barato que serve, e a pessoa sabe sempre qual foi. Primeiro o que está escrito e tem fonte; depois, só se a pessoa disser sim, a IA no próprio aparelho; só no fim, e com regras apertadas, um modelo de fora.

## As camadas, por ordem fixa

| Camada | Onde corre | Rede | Custo | Quando entra |
|---|---|---|---|---|
| 0 | no aparelho: regras escritas e fichas | 0 bytes | 0 € | há resposta escrita com **fonte** e **data** |
| 1 | no aparelho: modelo de IA local | 0 bytes depois de guardado | 0 € | a pessoa **consentiu**, o modelo **já está guardado** e há **165 MB** de memória livre |
| 2 | fora: modelo da UE | sim | o estimado | **consentimento para este pedido**, **rede**, **não é pedido de criança**, **teto diário definido** e o gasto fica **abaixo de 80 %** do teto |
| recusa | — | 0 | 0 € | nenhuma das anteriores serve: diz que não sabe e onde confirmar |

A Camada 0 é a que está ligada por defeito: memória abaixo de 64 MB e zero chamadas para fora. A Camada 1 nunca se descarrega sem um «sim» explícito (na app, o chat pergunta antes e diz o tamanho).

## Regras que não se partem

1. **Determinismo:** o mesmo pedido dá sempre a mesma decisão (o ensaio confere duas vezes cada caso).
2. **Nada sem teto:** sem teto diário definido, a Camada 2 não entra. Para a 80 % (Adenda II de 27-11-2026).
3. **Crianças:** um pedido marcado `menor` nunca sai do aparelho. A Camada 1 pode servir, com o consentimento do adulto.
4. **Só decide:** o roteador não chama modelos, não abre a rede e não lê chaves. Quem o usa faz a chamada que a decisão permitir.
5. **Recibo:** cada decisão leva o SHA-256 do pedido e da decisão, em JSON canónico (chaves ordenadas, sem espaços, UTF-8), para poder ser selada e conferida.
6. **Entradas más são recusadas** com erro claro (números negativos, textos no lugar de números, pedido que não é objeto).

## Pedido (JSON)

```json
{
  "camada0": {"texto": "…", "fonte": "wetten.overheid.nl", "data": "2026-11-02"},
  "consentimento": {"camada1": false, "camada2": false},
  "aparelho": {"modelo_local": false, "ram_livre_mb": 900, "rede": false},
  "orcamento": {"teto_diario_eur": 1.0, "gasto_hoje_eur": 0.10, "custo_estimado_eur": 0.002},
  "menor": false
}
```

## Decisão (JSON)

```json
{"kfc": "KFC-0.1", "rota": "camada0", "custo_eur": 0.0, "rede": false, "conferida": true,
 "motivos": ["…"], "recibo": {"pedido_sha256": "…", "decisao_sha256": "…"}}
```

## O que NÃO garante

O KFC escolhe o caminho; não garante que a resposta de um modelo (Camada 1 ou 2) esteja certa. Essas respostas saem marcadas como não conferidas. Os valores de custo são os que quem chama estimar.
