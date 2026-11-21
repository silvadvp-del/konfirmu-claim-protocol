# KCP-QR/0.1 - o CONTENTOR FISICO

Autor da disciplina: David Peres da Silva - 2026-11-21 - Konfirmu - Licenca EUPL-1.2 - Base KCP/0.1.

## 1. Principio

O QR e o contentor. Carrega a afirmacao e o seu hash, ate 4 KB, ou um URL curto mais hash.
Quem le, recomputa o hash no proprio telemovel, OFFLINE, sem rede, sem confiar em ninguem.
O hash e o lacre. O telemovel e a alfandega. Nenhum dos tres precisa de rede.

## 2. As tres mensagens

2.1 CLAIM - a afirmacao factual: medicamento autentico, rotulo, lei, documento de carga, certificado, voto.
2.2 PROOF - o hash da prova, a fonte e a data, dentro do payload QR. Implementacao de referencia em src/qr.mjs.
2.3 VERIFY - recomputacao local do hash no leitor, offline, em menos de 1 s.

## 3. Casos normativos

- Medicamentos e cadeia de frio, modulo M4.
- Rotulos de comida, P20 Lens-Barcode.
- Papel legal com QR, ChronoLex: o papel prova que nao foi mexido desde o selo.
- Documento de carga eBL, padrao DCSA.
- Certificados, diplomas, selo Ponto Neutral.
- Recibos de voto: o eleitor confirma que o voto contou.

## 4. Referencia

- ISO/IEC 18004 QR Code como codificacao fisica. VALIDAR: versao em vigor no catalogo ISO.

## 5. Regras duras

1. Payload ate 4 KB. Acima disso, o QR leva URL curto mais hash, nunca o conteudo em claro.
2. A verificacao corre no leitor, offline, nao no emissor.
3. Um byte adulterado significa hash partido e selo invalido.
4. Sem terceira via: VERIFICADO ou SEM_COBERTURA.

## 6. O que NAO garante

- O QR sozinho nao autentica o autor, so a integridade. Autoria pede assinatura Ed25519 do KCP/0.1.
- Nao e hardware anti-copia: a copia de um QR autentico continua valida ate o emissor o revogar.
