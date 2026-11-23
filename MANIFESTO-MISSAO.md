# Manifesto da Missão — Konfirmu

> Ordem do fundador (23-11): «nós somos caridade, humanitários, por um futuro melhor para todos,
> não é o greedy do costume — temos de estar no topo, nunca igual ou em baixo.» Escrito com a
> regra de ouro: a ambição é pública, e cada afirmação de liderança vem com prova ou é declarada
> como objectivo.

## Quem somos

A Konfirmu é uma infraestrutura **humanitária** europeia: a IA propõe, o humano confirma. O nosso
cliente é a família sem internet, a criança sem registo, a aldeia sem prova. O excedente não é
para accionistas — é para as girafinhas: a pool comunitária devolve o selo gratuito a quem não o
pode pagar (estrutura stichting + BV, ANBI [VALIDAR]).

## Contra o greedy do costume

O costume é: premine para os fundadores, yield prometido, o pobre como liquidez de saída. A nossa
regra é o oposto, escrita ANTES de prometer: **zero premine · zero juros · teto de débito ·
emissão só contra prova física · humano confirma sempre.** Quem procura especulação não nos serve
de cliente; quem precisa de prova serve-nos de missão.

## No topo — como e onde

A nossa ambição é ser a **referência mundial de prova verificável**. E há terreno onde já
lideramos, com prova executada e pública:

- **Prova do mundo físico**: entrega assinada, dose medida, frio conferido — digest `84f52e71…`.
- **Verdade metrológica**: descobrimos e publicámos que 1/(1,0±0,3) cobre 89,14 % e não 95 % — e
  resolvemo-lo exacto. Ninguém mais publica as próprias limitações assim.
- **Anti-falsificação completa**: selos + frescura + âncoras (Bitcoin como relógio, RFC 3161, BOIP)
  + verificação offline no aparelho.
- **247/247 verificações verdes** re-executadas, whitepaper, spec formal, auto-auditoria pública.

Onde ainda NÃO estamos no topo — e dizemo-lo: segurança de rede (usamos a Bitcoin como relógio,
não competimos com ela), certificações externas (ECSS/ESA são de terceiros), adopção mundial
(é o trabalho dos próximos anos). Estar no topo **nunca igual ou em baixo** significa: nunca
copiar o que já existe — criar a camada que ninguém tem.

## Como se verifica

`shasum -a 256 -c SHA256SUMS.txt` · `python3 konfirmu_calc.py --demo` (247/247) ·
`openssl ts -verify -in anchors/konfirmu_calc.tsr -data konfirmu_calc.py -CAfile anchors/cacert.pem -untrusted anchors/tsa.crt`
