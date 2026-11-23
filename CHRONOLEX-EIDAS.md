# CHRONOLEX — Alinhamento eIDAS (autoavaliação, não conformidade)

> Regra de ouro: «alinhado com» ≠ «conforme». Isto é uma autoavaliação de primeira parte,
> para leitura de um jurista antes de qualquer uso probatório. Data: 2026-11-23.

| Elemento eIDAS | O que o Chronolex faz HOJE | Estado honesto |
|---|---|---|
| Assinaturas electrónicas (Art. 25) | assinaturas Ed25519 múltiplas sobre o selo mestre (chronolex_core.py — motor real, RFC 8032 provado) | assinatura ELECTRÓNICA (nível básico) — NÃO é assinatura qualificada |
| Efeito jurídico (Art. 25/2-3) | a assinatura não pode ser recusada só por ser electrónica; o valor probatório depende do contexto | [VALIDAR] jurista, caso a caso |
| Carimbos temporais (Art. 41) | RFC 3161 via FreeTSA (pública) + verificação local (openssl ts -verify) + âncoras Bitcoin/OTS | FreeTSA NÃO é QTSP qualificado — presunção legal exige prestador qualificado da lista de confiança UE |
| Integridade e cadeia de custódia | eventos encadeados prev_hash + selo mestre + anexos por hash | PROVADO (selftest: cadeia OK, tampers detetados) |
| Interoperabilidade | JSON canónico + QR + exportação | PROVADO |

## O nível seguinte (com dono)
1. QTSP qualificado (D-Trust/Bundesdruckerei ou equivalente NL) — contrato, decisão do fundador [VALIDAR custos].
2. O pacote legal NL (00_LEGAL_PACKAGE.md, outra janela) — preencher placeholders (entidade, morada, KvK 42005886, BTW-id) e publicar /colofon + /privacy.
3. Jurista lê isto antes do primeiro uso probatório real.
