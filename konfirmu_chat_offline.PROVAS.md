# Chat de bolso offline v0.3 — o que está provado e o que não está

Data: 2026-11-25. Finalidade: ensino e investigação. Não serve para decisões sobre pessoas.

| Ficheiro | Bytes | SHA-256 |
|---|---|---|
| konfirmu_chat_offline.html | 32948 | 92df90cd4a3e306785aefaf47b1e0771b3e65aab4a0d72c1e77e9283b45ab3d0 |
| konfirmu_chat_sw.js | 630 | f22025f21635a977f4b2f946cb3b9ddf6b76da3a8335f2be38394d314b284a02 |

## Provado (26 de 26)

Repetir: `python3 tests/test_konfirmu_chat_offline.py` (Chrome sem ecrã; sai com 0 só se tudo passar).

1. Portão por regras: 11 medidas de nitrato (limite 50 mg/L, Diretiva (UE) 2020/2184) e de cadeia de frio (2 a 8 °C) com o veredicto certo, incluindo «ainda não sei» quando a margem cruza o limite.
2. Pergunta de dose: sem veredicto.
3. SHA-256 igual ao do Python, pelo WebCrypto e pelo código próprio.
4. Cadeia da conversa: inteira confere; um registo mexido é apontado; ficheiro estranho é recusado.
5. Selo de texto: igual, diferente, e «não sei» sem original.
6. Som: 18 idas e voltas em contas (3 textos, 44 100 e 48 000 amostras por segundo, sem ruído e com ruído forte). Som cortado e ruído puro não inventam mensagem. CRC-16 confere com o valor de referência.
7. Aberto como ficheiro: zero pedidos à rede; a IA diz que precisa de link https.
8. A conversa volta depois de fechar e abrir. Apagar apaga.
9. Com link: depois da primeira visita, a página abre com o servidor desligado.
10. Sem verde no ficheiro. Zero erros de página.
11. Foto leve: uma imagem de teste de 1200×900 (522 113 bytes) ficou em 4 340 bytes (WebP, 180×135), em 29 pacotes e 8 de reserva, cada um abaixo de 240 letras.
12. Pacotes todos juntos, ou fora de ordem, dão a imagem exata, byte a byte.
13. Um pacote perdido em cada grupo de 4 é recuperado. Dois perdidos no mesmo grupo dão «ainda não sei, faltam 2».
14. Um bit mexido dá «não confere». Sem cabeçalho, ou com lixo, não aparece imagem nenhuma.

## Não provado, e porquê

| O quê | Porquê |
|---|---|
| A IA local (Qwen2.5-0.5B) a descarregar e a responder | A máquina de teste não tem saída para cdn.jsdelivr.net nem huggingface.co. O código existe e nunca correu. |
| Som pelo ar, entre dois telemóveis | Não há telemóveis nem microfone real na máquina de teste. Só está provada a conta (onda gerada, ruído somado, onda lida). Eco, distância e altifalantes fracos não foram medidos. |
| iPhone | Não foi testado em nenhum iPhone. Um ficheiro .html aberto no WhatsApp do iPhone é só pré-visualizado; precisa de link https. |
| Foto por rádio LoRa, HF ou Wi-Fi HaLow | Não há rádio nenhum ligado. Os pacotes saem num ficheiro de texto; ninguém os pôs no ar. |
| Foto por som | Não é viável com este modem: 4 340 bytes a 28 bits por segundo são cerca de 25 minutos. |
| Se a foto reduzida ainda se lê | Não foi medido. 180 pontos de largura chegam para reconhecer uma coisa grande; não está provado que cheguem para ler letras pequenas, e não servem para diagnóstico. |
| Foto leve no iPhone | O Safari pode não gravar WebP; nesse caso a página usa JPEG. Não testado. |
| Android real, a partir do WhatsApp | Testado só em Chrome de computador. |

## Não feito

- Assinatura e cifra dos pacotes (a cadeia mostra alterações; não mostra quem escreveu).
- QR animado, Wi-Fi local, rádio LoRa.
- Modelo de IA mais pequeno para telemóveis com pouca memória.

## Limites que ficam

- O portão confere o número com a regra. Não confere se a medida foi bem feita.
- O que a IA local disser aparece marcado como «não conferido».
- O som confirma que a mensagem chegou inteira. Não confirma que é verdadeira.
- O selo da foto confere com o que o emissor declarou no cabeçalho. Sem assinatura, não prova quem enviou.
- A reserva recupera 1 pacote em cada 4. Não recupera perdas seguidas.
