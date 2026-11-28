# Medições de memória — KON-623 (27-11-2026)

Medida: pico da memória privada (Private_Dirty de `/proc/PID/smaps_rollup`) do processo da página no Chrome 153, amostra a cada 100 ms (curvas longas: a cada 5 s). Perfis: telemóvel (Pixel 7, 412×915) e computador (1280×800). Linux sem GPU: o 3D é desenhado em software (SwiftShader). Limite: 64 000 000 bytes. Dados brutos: `02_DADOS_BRUTOS.json`. Programas: `03_METODO_PROGRAMAS.md`.

## A. Cenário padrão — o que deu os 72 MB no main

Carregar, 4 s parado, 8 toques, 3 setas, lista de línguas. Duas corridas por página. Valores em MB.

| página | telemóvel | computador | resultado |
|---|---|---|---|
| menu do `main`, árvore do repositório (17:46 e 17:51) | 67,0 · 68,0 | 72,4 · 72,0 | FALHA |
| menu do `main`, sítio construído (20:01) | 56,4 · 56,9 | 66,3 · 59,8 | FALHA (1 de 4) |
| **menu, candidata final** | **51,8 · 48,7** | **53,7 · 55,1** | **PASSA** |
| **entrada Família 3D, candidata final** | **54,4 · 56,4** | **54,3 · 54,0** | **PASSA** |

## B. Página parada 150 s

| página | perfil | commit d8dc1e1 (20:33) | candidata final |
|---|---|---|---|
| menu | computador | sobe sem parar: 36,7 → 61,1 MB em 75 s | estável perto de 31 MB; pico 38,4 |
| menu | telemóvel | 32,6 → 39,0 MB em 75 s | estável perto de 26,5 MB; pico 32,7 |
| entrada 3D | computador | — | pico 52,6 no arranque; depois 36 a 41 |
| entrada 3D | telemóvel | — | pico 53,9 no arranque; depois 37 a 42 |

A entrada 3D sobe devagar depois da primeira limpeza (cerca de 4 MB em 2 minutos). Não foi medida mais de 150 s: por confirmar numa sessão longa.

### Porque subia o menu parado (diagnóstico, computador)

| variante | resultado |
|---|---|
| céu todo na página, sem trabalhador, 150 s | sobe sem parar até 74,7 MB |
| no trabalhador só a aurora (WebGL), 75 s | plano, cerca de 31 MB |
| no trabalhador só as faíscas (Canvas 2D), 75 s | sobe até 59,9 MB |
| faíscas em 2D com a faísca como ImageBitmap, 150 s | sobe mais devagar, até 64,9 MB |
| **faíscas em WebGL (versão final), 150 s** | **plano, cerca de 31 MB** |

Causa: as faíscas desenhadas em Canvas 2D, 60 vezes por segundo. Correção: as faíscas e o anel do toque passam a WebGL, com o mesmo desenho. Sem WebGL, continuam em Canvas 2D.

### O desenho não mudou (verificado)

Comparação píxel a píxel no mesmo Chrome (`03_METODO_PROGRAMAS.md`, `faisca.html`):
- faísca: diferença máxima 1/255;
- anel do toque: diferença máxima 21/255 num traço de 1 píxel; brilho total 2,3 % acima.

No menu real, as faíscas mexem-se como antes: píxeis que mudam em 250 ms, telemóvel 3297 antes e 3307 agora; computador 3096 antes e 2487 agora (posições ao acaso). Zero erros na consola.

## C. Passeio contínuo de cerca de 1 minuto — FALHA

3 separadores, Imersão 3D ligada e 8 s a mexer, rolar, lista de línguas, 10 s parado. Valores de pico em MB.

| versão | telemóvel | computador |
|---|---|---|
| `main` (antes) | 146,6 | 139,3 |
| commit d8dc1e1 | 79,0 · 82,7 | 94,4 · 95,0 |
| candidata final | 76,4 · 76,2 | 93,8 · 87,9 |

Depois da limpeza do Chrome, a página volta a cerca de 50 MB. O pico vem de memória que já não está em uso e que o Chrome ainda não limpou. Continua acima de 64 MB: **por resolver**.

## D. A medida, sem esconder nada

- O meu medidor das 17:47 usava o PSS. Mudei para a memória privada porque o PSS conta a parte partilhada do próprio Chrome: uma página vazia já dá 63,1 MB de PSS e 12,9 MB de memória privada.
- O `SYSTEM_STATE.json` (revisão 4) chama ao limite `physicalPeakBytesExclusive` (memória física exclusiva). A passagem das 17:15 diz que o verificador da casa mede o PSS num Android físico, por ADB. **Não há Android físico nesta sessão: essa medida está por fazer.**
- Os 72,1 MB de hoje batem com a memória privada do menu no `main` (72,0 e 72,4 MB no computador). Inferido: a fonte dos 72,1 não está no OneDrive.
- PSS do processo da página na versão final: 97 a 137 MB. Processo da GPU (partilhado por todas as páginas): 31 a 40 MB no menu e cerca de 165 MB na entrada 3D, porque aqui o 3D é desenhado em software. Os números estão em `02_DADOS_BRUTOS.json`.
