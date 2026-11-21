# KCP-GATEWAY/0.1 - a ALFANDEGA AUTOMATICA (verify-first em todas as IAs)

Autor da disciplina: David Peres da Silva - 2026-11-21 - Konfirmu - Licenca EUPL-1.2 - Base KCP/0.1.

## 1. Principio

Cada pedido de IA passa PRIMEIRO pelo verificador. VERIFICADO devolve o facto selado sem acordar o modelo caro. SEM_COBERTURA escala para o LLM pago, so quando precisa. A Konfirmu torna-se a porta de entrada por matematica, nao por escolha.

## 2. As tres mensagens

2.1 CLAIM - o pedido que chega do agente ou da aplicacao.
2.2 PROOF - cache hit devolve o selo (fonte, data, hash); cache miss devolve SEM_COBERTURA honesto.
2.3 VERIFY - o selo re-verifica-se na maquina do receptor, offline, sem chave do emissor.

## 3. Integracao (a escada de adopcao)

1. Proxies unificados (LiteLLM, OpenRouter, Portkey) - o chokepoint: um plugin verifica tudo o que passa.
2. Frameworks (LangChain, LlamaIndex, Semantic Kernel, CrewAI, AutoGen).
3. Servidores de modelos (vLLM, TGI, Ollama).
4. Gateways de API (Kong, Cloudflare AI Gateway, Envoy).
5. Agentes nativos (MCP - ja registado) e no-code (n8n, Zapier, Make).

## 4. Referencia

- OpenAPI 3.1 para os endpoints /v1/verificar e /v1/facto.
- API viva: api.2-29-155-209.sslip.io (host real, VALIDAR dominio api.konfirmu.eu).

## 5. Regras duras

1. Verify-first: o cache resolve antes do LLM (a matematica do 99 por cento).
2. SEM_COBERTURA e comportamento conforme, nao falha.
3. Retencao zero: a afirmacao processa-se em memoria e morre; so o hash persiste.
4. Sem terceira via: VERIFICADO ou SEM_COBERTURA.

## 6. O que NAO garante

- O 99 por cento e META ate ser medido com selos antes/depois (benchmark v3).
- A integracao real nos proxies e trabalho de adopcao (plugin de referencia, ~50 linhas, a entregar).
- OpenAPI/endpoints citados como referencia; o dominio api.konfirmu.eu fica VALIDAR.
