# KCP-NUCLEAR/0.1 - o perfil da INSPECAO (verificacao nuclear sem confianca)

Autor da disciplina: David Peres da Silva - 2026-11-21 - Konfirmu, Amesterdao - Licenca EUPL-1.2 - Base KCP/0.1.

## 1. Principio

A historia ensina: o que travou a corrida nuclear nao foi a confianca - foi a INSPECAO.
Trust, but verify (Reagan, 1987). Os tratados sobreviveram porque inspectores viram os silos.
O KCP-NUCLEAR traduz essa disciplina para a informacao: cada declaracao (inventario, moratoria,
desmantelamento, ensaio) carrega prova verificavel por QUALQUER parte - inclusive pelo adversario.

## 2. As tres mensagens

2.1 NUC-CLAIM - a declaracao: declarante, objeto, quantidade, local, data.
2.2 NUC-PROOF - a prova: evidencia nascida selada na fonte + cadeia de custodia hash-a-hash + dupla selagem (humano confirma, maquina sela).
2.3 NUC-VERIFY - qualquer parte re-executa a verificacao na propria maquina, offline, sem chave do emissor.

## 3. Regras duras

1. SIMETRIA TOTAL: adversarios verificam-se entre si com o mesmo instrumento. Nenhuma parte recebe melhor verdade que outra.
2. PROVA NA FONTE: a evidencia nasce selada no sensor/local, nunca no relatorio.
3. CADEIA DE CUSTODIA: um byte adulterado quebra a cadeia e TODOS veem (src/inspecao.mjs).
4. SEM_COBERTURA e conforme: o que nao se consegue verificar, declara-se - e essa honestidade e arma.
5. ZERO CONFIANCA NO OPERADOR: o verificador corre na maquina de quem recebe.
6. o_que_nao_garante obrigatorio em cada resposta.

## 4. O que NAO e / NAO garante

- NAO e um tratado, NAO e politica, NAO substitui diplomatas nem inspectores.
- NAO garante desarmamento nem paz: garante que a nao-conformidade nao se esconde.
- NAO prova que a declaracao e verdadeira: prova quem declarou e que nada foi mexido depois (imprimatur).

## 5. A entrega as 3 grandes potencias

A entrega e a PUBLICACAO: protocolo aberto, EUPL-1.2, datado e com hash - prior art defensiva que
nenhuma potencia pode fechar em patente. Os protocolos nao se decretam - adotam-se (a licao do TCP/IP).
O contacto diplomatico direto e gesto do fundador pelos canais proprios, com convite - nao se envia
protocolo a chancelarias sem ele. O que entregamos ja e a prova: aberta, simetrica, inapropriavel.
