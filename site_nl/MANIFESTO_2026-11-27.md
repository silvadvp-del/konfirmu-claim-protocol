# Konfirmu — o que é, o que existe hoje, como construir em cima

**Rascunho interno (nível 0).** Corrige o texto «infraestrutura aberta de confiança digital». Tudo o que está
escrito aqui foi verificado a 27-11-2026. **Não sai para fora sem o gate integral e a checklist de 12 pontos da casa**;
as frases públicas têm de nascer de carta real, do corpus ou de ronda de teste.

## 1. O que é a Konfirmu

A Konfirmu é a plataforma de conhecimento e organização pessoal do trabalhador migrante. Organiza a vida
administrativa e profissional, explica os documentos oficiais na língua da pessoa com prova verificável, protege
contra burla e abre a porta para o Estado. O conhecimento vem da biblioteca própria de fontes oficiais.

Tem quatro pilares:

1. **Organização da vida administrativa e profissional:** documentos, cartas, tarefas e prazos, recibos de vencimento,
   horas, despesas, faturação e preparação de informação para o contabilista.
2. **Compreensão e proteção:** um motor determinístico que junta facto e norma e nunca aconselha; verificação de
   recibos; deteção de fraude e burla; modo seguro de crise.
3. **Biblioteca do Conhecimento:** fontes oficiais capturadas com hash e fichas verificadas. A verdade é tratada como
   dados; os modelos de linguagem servem só a língua.
4. **Porta para o Estado e para o trabalho:** que portal usar, com link direto, prazo e login; currículo; apoios e direitos.

O público são os migrantes nos Países Baixos. A linha Pro serve quem trabalha por conta própria. O ciclo é
**Compreender · Confirmar · Agir**. O título da casa é «O país onde vives, na tua língua.»

## 2. Como se usa

- **Sem internet, no próprio aparelho.** As páginas são autocontidas. Medido a 27-11: a página inicial e a app pública
  não fazem nenhuma chamada remota.
- **Por código aberto.** Dois repositórios públicos com licença europeia EUPL-1.2:
  `github.com/silvadvp-del/konfirmu-claim-protocol` e `github.com/silvadvp-del/konfirmu-ancora`.
- **Por API e por MCP.** Um servidor MCP responde hoje com três ferramentas: procurar fichas oficiais, ler os limites
  da casa e construir uma ata de reunião. Uma API de leitura entrega fichas com fonte e hash (medida a 24-11).
- **Na web.** `dpsindustrial.nl/konfirmu/` e `dpsindustrial.nl/konfirmu/app/`, com menu em três portais (juntado a 27-11).

## 3. O que há por baixo

- **Regras de fronteira numérica.** Uma regra aprovada pelo proprietário (R35) fixa como se arredonda e o que acontece
  nos limites da vírgula flutuante. Existe uma bateria de 11 366 casos históricos. **Estado honesto:** o motor publicado
  ainda falha em 13 casos de fronteira; as correções estão em pacotes, por adotar.
- **Assinaturas e provas.** Assinaturas Ed25519, atas com cadeia de hash e recibos de sessão com hash. Dois carimbos
  de tempo RFC 3161 foram verificados de forma independente. O fornecedor desses carimbos não é um fornecedor
  qualificado de confiança.
- **Provas formais em Lean 4.** Vinte e dois teoremas e quatro contra-exemplos certificados pelo kernel. Dizem respeito
  a somas de inteiros, permutações, quadrados, conservação da divisão, um modelo de Merkle e partes de uma fórmula
  usada em farmacocinética. Não provam a criptografia.
- **Multilinguismo sem teto.** Desde 26-11 a casa não fixa um número de línguas. Cada edição declara o que traduziu,
  com que origem e se houve revisão por falantes. Uma prova técnica demonstra cinco línguas e duas escritas.

## 4. O que ainda não existe

Para ninguém prometer: assinaturas pós-quânticas (o código marca ML-DSA-65 como «implementar»); reconciliação por
IBLT; troca entre dois telemóveis por QR animado; bots de WhatsApp e Telegram provados no canal real; teste em várias
plataformas; memória medida no telemóvel.

## 5. Como cada um pode fazer a sua parte

- **Programadores:** ler, auditar e propor num repositório público. A entrada é por pedido de integração, com os
  testes automáticos a passar.
- **Tradutores e comunidades:** trazer a sua língua. Cada edição declara origem e revisão, e as lacunas ficam à vista.
- **Escolas, cooperativas e instituições:** pilotos privados, cada um com o «sim» registado do proprietário.

## O que a Konfirmu não garante

Não dá aconselhamento jurídico nem médico. Não toma decisões pelas pessoas: a máquina preenche e propõe, a pessoa
confere e confirma. Os endereços e os canais podem mudar; confira a data de cada página. Nada sai sem o teu consentimento.
