#!/usr/bin/env python3
"""Gera o menu de entrada da Konfirmu em 3 portais (pedido do David, 27-11, 04:59–05:00).

Escreve 3 ficheiros no repositório público:
  app_unica.html              menu da raiz (19 atividades, a página «Economia anti-casino» e o botão
                               «Preparar modo avião»)
  edicao-21/app_unica.html    menu da edição integrada (21 atividades) — é o menu do pacote
  edicao-21/index.html        igual ao anterior

Regras da casa aplicadas: paleta 2040 (Azul Abissal #0B192C, vidro rgba(15,34,61,.72), Pêssego Solar
#FF9E7D, Branco Titânio #F4F7FA, Cinza Nevoeiro #9FB3C8), sem verde nem violeta, sem emojis, ícones
SVG de linha 1,5 px; atmosfera viva (aurora WebGL + partículas) com teto de brilho para manter AAA;
o 112 não aparece no menu (regra de 31-10).
Ganchos que não se podem partir: a.card > .ico + b + .d (imersão 3D e teste do GitHub), um h1
(a imersão põe os botões a seguir), nenhum <summary> próprio, ids «aviao»/«aviaoEstado» e «id».

Protocolo de 27-11 (Definition of Done): o rodapé traz os 5 avisos legais, lidos da
avisos_legais.html (uma só fonte; sem ela, o gerador para), e há procura instantânea.
O menu da raiz liga também a página dos avisos em 24 línguas. O menu da edição 21 não a liga:
o empacotador junta tudo o que o menu liga e o teste do pacote só aceita atividades.

Uso: python3 -I scripts/gerar_menu.py [CAMINHO_DO_REPOSITORIO]   (por omissão, a pasta acima de scripts/)
Escreve também assets/ceu_vivo.js (o céu vivo, num trabalhador à parte, para a página não refazer estilos a cada quadro).
Depois: refazer as 4 linhas destes ficheiros em SHA256SUMS.txt e correr os testes do pacote.
"""
import html
import importlib.util
import json
import os
import re
import sys

# As tigelas do Portal Educação e família vivem em scripts/tigelas.py (diretiva do David, 27-11, 12:29).
# Carregado pelo caminho do ficheiro: funciona também com «python3 -I».
_spec = importlib.util.spec_from_file_location("tigelas", os.path.join(os.path.dirname(os.path.abspath(__file__)), "tigelas.py"))
tigelas = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(tigelas)

ICONES = {
    "terminal": '<rect x="3" y="4" width="18" height="16" rx="2"/><path d="m7 9 3 3-3 3M12.5 15H17"/>',
    "ficheiro": '<path d="M14 3H7a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2V8z"/><path d="M14 3v5h5"/><path d="m9 14 2 2 4-4"/>',
    "foto": '<path d="M4 8h3l2-3h6l2 3h3a1 1 0 0 1 1 1v9a1 1 0 0 1-1 1H4a1 1 0 0 1-1-1V9a1 1 0 0 1 1-1z"/><circle cx="12" cy="13" r="3.5"/>',
    "ficha": '<rect x="5" y="4" width="14" height="17" rx="2"/><path d="M9 4h6v3H9z"/><path d="M8.5 11h7M8.5 14.5h7M8.5 18h4"/>',
    "ata": '<path d="M7 4v16"/><circle cx="7" cy="7" r="1.6"/><circle cx="7" cy="12" r="1.6"/><circle cx="7" cy="17" r="1.6"/><path d="M11 7h8M11 12h8M11 17h6"/>',
    "verificar": '<circle cx="10.5" cy="10.5" r="6"/><path d="m15 15 5 5"/><path d="m8 10.5 1.8 1.8L13 9"/>',
    "testemunha": '<circle cx="8.5" cy="8" r="3"/><circle cx="16" cy="9" r="2.5"/><path d="M3 19c.6-3.3 2.9-5 5.5-5s4.9 1.7 5.5 5"/><path d="M14.5 14.2c.5-.1 1-.2 1.5-.2 2.2 0 4 1.4 4.5 4.5"/>',
    "ligacao": '<rect x="3" y="6" width="7" height="12" rx="1.5"/><rect x="14" y="6" width="7" height="12" rx="1.5"/><path d="M10 12h4"/>',
    "som": '<path d="M3 12h2l2-5 3 10 3-12 3 10 2-3h3"/>',
    "chat": '<path d="M5 5h14a1 1 0 0 1 1 1v9a1 1 0 0 1-1 1h-7l-4 4v-4H5a1 1 0 0 1-1-1V6a1 1 0 0 1 1-1z"/>',
    "saude": '<path d="M12 3 5 6v5c0 4.5 3 8.3 7 10 4-1.7 7-5.5 7-10V6z"/><path d="M12 9v6M9 12h6"/>',
    "carta": '<rect x="3" y="6" width="18" height="13" rx="1.5"/><path d="m3.5 7 8.5 6.5L20.5 7"/>',
    "voto": '<path d="M5 11h14v9H5z"/><path d="M9 11V5h6v6"/><path d="M8 15h8"/>',
    "toque": '<circle cx="12" cy="12" r="8"/><circle cx="12" cy="12" r="3"/>',
    "livro": '<path d="M5 4h11a3 3 0 0 1 3 3v13H8a3 3 0 0 1-3-3z"/><path d="M5 17a3 3 0 0 1 3-3h11"/>',
    "quiz": '<circle cx="12" cy="12" r="9"/><path d="M9.5 9.5a2.5 2.5 0 1 1 3.5 2.3c-.7.3-1 .9-1 1.7v.5"/><path d="M12 17h.01"/>',
    "estrela": '<path d="m12 3 2.6 5.6 6 .7-4.5 4.1 1.2 6L12 16.4l-5.3 3 1.2-6-4.5-4.1 6-.7z"/>',
    "video": '<rect x="3" y="7" width="13" height="10" rx="1.5"/><path d="m16 11 5-3v8l-5-3z"/>',
    "contas": '<rect x="5" y="3" width="14" height="18" rx="2"/><path d="M8 7h8"/><path d="M8.5 11.5h.01M12 11.5h.01M15.5 11.5h.01M8.5 14.75h.01M12 14.75h.01M15.5 14.75h.01M8.5 18h.01M12 18h.01M15.5 18h.01"/>',
    "arte": '<path d="M12 3a9 9 0 1 0 0 18c1.1 0 1.5-.8 1.5-1.6 0-.5-.2-.9-.5-1.3-.3-.4-.5-.8-.5-1.3 0-1 .8-1.8 1.8-1.8H17a4 4 0 0 0 4-4c0-4.4-4-8-9-8z"/><circle cx="7.5" cy="11" r="1"/><circle cx="10" cy="7.5" r="1"/><circle cx="14.5" cy="7.5" r="1"/>',
    "globo": '<circle cx="12" cy="12" r="9"/><path d="M3 12h18"/><path d="M12 3a14 14 0 0 1 0 18M12 3a14 14 0 0 0 0 18"/>',
    "bussola": '<circle cx="12" cy="12" r="9"/><path d="m15.5 8.5-2 5-5 2 2-5z"/>',
}

EM_ENSAIO = "Em ensaio, ainda não validado"

# Emblemas dos 3 portais (SVG de linha 1,5 px): âncora, escudo com coração, livro aberto.
EMBLEMAS = {
    "pro": '<circle cx="12" cy="5" r="2"/><path d="M12 7v14"/><path d="M8 10.5h8"/><path d="M5 13.5a7 7 0 0 0 14 0"/>',
    "cid": '<path d="M12 3 5 6v5c0 4.5 3 8.3 7 10 4-1.7 7-5.5 7-10V6z"/><path d="M9.3 11.2a1.9 1.9 0 0 1 2.7-.3 1.9 1.9 0 0 1 2.7.3c.8.9.5 2-.3 2.8L12 16.3 9.6 14c-.8-.8-1.1-1.9-.3-2.8z"/>',
    "fam": '<path d="M3 6.5C5.5 5 8.5 5 12 7c3.5-2 6.5-2 9-.5V19c-2.5-1.5-5.5-1.5-9 .5-3.5-2-6.5-2-9-.5z"/><path d="M12 7v12.5"/>',
}

PORTAIS = [
    ("pro", "Profissional", "Profissional e indústria",
     "Para quem trabalha no terreno: confirmar ficheiros, registar o que aconteceu e guardar a prova.", [
         ("verificador_offline.html", "ficheiro", "Verificar ficheiro", "Confirma se um ficheiro ou um código é mesmo o original.", None),
         ("chronolex_photo_seal.html", "foto", "Foto com selo", "Tira uma fotografia e guarda-a com selo.", None),
         ("ficha_campo.html", "ficha", "Ficha de campo", "Regista água, energia e avarias, por ordem.", None),
         ("chronolex_ata.html", "ata", "Ata Chronolex", "Regista o que aconteceu, por ordem, com selo.", None),
         ("chronolex_verify.html", "verificar", "Verificar ata", "Confirma se uma ata ficou igual ao que foi selado.", None),
         ("testemunha_offline.html", "testemunha", "Testemunha", "Duas pessoas confirmam o mesmo momento.", None),
         ("radio_selo.html", "som", "Mensagem por som", "Envia mensagens por som que não se podem falsificar.", None),
         ("webrtc_local.html", "ligacao", "Ligação direta", "Liga dois aparelhos sem passar pela nuvem.", None),
         ("terminal.html", "terminal", "Terminal sem rede", "Comandos para conferir: sha256, verify e bigint-test. Fica escondido no Modo Criança.", None),
     ]),
    ("cid", "Cidadão", "Cidadão e saúde",
     "Para o dia a dia: conversar, tratar de cartas e guardar a tua informação no teu aparelho.", [
         ("konfirmu_chat_offline.html", "chat", "Chat de bolso", "Responde com regras escritas. Quando não sabe, diz.", None),  # KON-608: o chat com o portão do 112
         ("patient_vault_offline.html", "saude", "Cofre de saúde", "A tua história de saúde, guardada só neste aparelho.", EM_ENSAIO),
         ("carta_selada.html", "carta", "Carta com selo", "Escreve, põe o selo e imprime.", None),
         ("urna_voto_offline.html", "voto", "Votação sem rede", "Uma votação feita só nos aparelhos de quem vota.", EM_ENSAIO),
         ("economia_anti_casino.html", "contas", "Economia anti-casino", "Porque aqui um crédito só nasce de um trabalho conferido. Passo a passo.", None),
     ]),
    ("fam", "Família", "Educação e família",
     "Aprender e brincar em família, com o mesmo cuidado pela privacidade.", [
         ("girafinhas_criancas_facil.html", "toque", "Primeiros passos", "Três toques, voz e cores, para quem nunca usou um telemóvel.", None),
         ("Tutor-Girafinha-offline.html", "livro", "Tutor", "Ensina passo a passo, mesmo sem rede.", None),
         ("kcp_family_quiz.html", "quiz", "Quiz em família", "Perguntas para jogar em família, ou só entre adultos.", None),
         ("sala_natal_girafinhas.html", "estrela", "Natal em família", "Jogos, moldes de papel e um certificado para guardar.", None),
         ("estudio_video_criancas.html", "video", "Estúdio de vídeo", "Filma sem internet e guarda o filme com selo.", None),
         ("executor_criancas.html", "contas", "Contas com selo", "Faz contas e guarda o resultado com selo.", None),
         ("kcp_art_music_studio.html", "arte", "Estúdio de arte", "Música e desenho, com o teu nome.", None),
         ("regua_do_planeta.html", "globo", "Régua do planeta", "Ainda vamos a tempo de salvar o planeta?", None),
         ("neverland_family_quest.html", "bussola", "Aventura em família", "Um jogo de aventura para jogar juntos.", None),
     ]),
]

SO_NA_EDICAO_21 = {"Tutor-Girafinha-offline.html", "kcp_family_quiz.html"}
# Página explicativa, não é atividade: só no menu da raiz (o pacote da edição 21 só aceita atividades).
SO_NA_RAIZ = {"economia_anti_casino.html", "terminal.html"}

CSS = """
:root{color-scheme:dark;--u-marca:#f7b397;--abissal:#0B192C;--vidro:rgba(15,34,61,.72);--vidro-solido:#0F223D;--pessego:#FF9E7D;--pessego-2:#FF9E7D;--titanio:#F4F7FA;--nevoeiro:#9FB3C8;--aresta:rgba(244,247,250,.12);--aresta-quente:rgba(255,158,125,.5);
--pagina:#0B192C;--painel:#0F223D;--tinta:#F4F7FA;--tinta2:#9FB3C8;--tinta3:#9FB3C8;--linha:rgba(244,247,250,.12);--azulejo:#0F223D;--u:#FF9E7D;
--letra:"SF Pro Text",-apple-system,BlinkMacSystemFont,"Segoe UI Variable Text","Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif;
--titulo:"SF Pro Display",-apple-system,BlinkMacSystemFont,"Segoe UI Variable Display","Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif;--mola:cubic-bezier(.2,.8,.2,1)}
*{box-sizing:border-box}
html{background:var(--abissal);-webkit-text-size-adjust:100%}
html.sem-webgl{background:radial-gradient(130% 75% at 50% 0%,rgba(255,158,125,.16) 0%,#0B192C 62%) fixed var(--abissal)}
body{margin:0 auto;max-width:780px;padding:34px 18px 48px;font:16px/1.55 var(--letra);color:var(--titanio);background:transparent;-webkit-font-smoothing:antialiased;-webkit-tap-highlight-color:transparent}
.ceu{position:fixed;inset:0;width:100%;height:100%;z-index:-1;display:block;pointer-events:none}
h1{margin:0;font:700 clamp(2.75rem,11vw,4.25rem)/1 var(--titulo);letter-spacing:-.035em;color:var(--titanio)}
h1 .u{color:var(--u-marca);text-shadow:0 0 16px rgba(255,158,125,.5),0 0 40px rgba(255,158,125,.22)}
.intro{margin:14px 0 0;max-width:30em;font-size:1.0625rem;line-height:1.55;color:var(--titanio)}
.acoes{display:flex;flex-wrap:wrap;align-items:center;gap:10px;margin:22px 0 0}
.letra,.aviao,body .im3d-tools button{flex:none;min-height:44px;padding:0 16px;border:1px solid var(--aresta);border-radius:12px;background:var(--vidro);color:var(--titanio);font:600 .9375rem/1 var(--letra);cursor:pointer;transition:border-color .3s,box-shadow .3s,transform .25s var(--mola)}
.letra:hover,.aviao:hover,body .im3d-tools button:hover{border-color:var(--aresta-quente);box-shadow:0 0 24px -8px rgba(255,158,125,.6)}
.letra:active,.aviao:active,body .im3d-tools button:active{transform:scale(.97)}
.letra[aria-pressed="true"],body .im3d-tools button[aria-pressed="true"]{background:var(--vidro);color:var(--titanio);border-color:var(--pessego);box-shadow:inset 0 0 0 1px rgba(255,158,125,.55)}
.aviao-estado{display:block;margin-top:10px;min-height:1.4em;font-size:.875rem;color:var(--titanio)}
.procura{margin:26px 0 0}
.procura label{display:block;margin:0 0 8px;font-size:.875rem;font-weight:600;color:var(--titanio)}
.procura input{width:100%;min-height:48px;padding:0 16px;border:1px solid var(--aresta);border-radius:14px;background:var(--vidro-solido);color:var(--titanio);font:400 1rem/1.2 var(--letra);transition:border-color .3s,box-shadow .3s}
.procura input::placeholder{color:var(--nevoeiro)}
.procura input:focus{outline:none;border-color:var(--pessego);box-shadow:0 0 0 3px rgba(255,158,125,.24)}
.sem-resultados{margin:10px 0 0;min-height:1.4em;font-size:.9375rem;color:var(--titanio)}
.sem-resultados:empty{display:none}
.portais{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:10px;margin:18px 0 0}
.portais [role=tab]{position:relative;overflow:hidden;isolation:isolate;display:flex;flex-direction:column;align-items:flex-start;justify-content:space-between;gap:14px;min-height:120px;padding:14px 12px 12px;border:1px solid var(--aresta);border-radius:20px;background:var(--vidro);-webkit-backdrop-filter:blur(16px) saturate(125%);backdrop-filter:blur(16px) saturate(125%);color:var(--titanio);text-align:left;font:650 1rem/1.15 var(--titulo);letter-spacing:-.01em;cursor:pointer;transition:transform .35s var(--mola),border-color .4s,box-shadow .5s}
.portais [role=tab]::before{content:"";position:absolute;left:calc(50% - 150px);top:calc(22% - 115px);width:300px;height:230px;z-index:-1;pointer-events:none;--dx:inherit;--dy:inherit;transform:translate(var(--dx),var(--dy));will-change:transform;background:radial-gradient(150px 115px at 50% 50%,rgba(255,158,125,.22),transparent 70%);opacity:0;transition:opacity .5s}
.portais [role=tab] .giro{position:absolute;inset:0;z-index:-1;border-radius:inherit;padding:1px;overflow:hidden;pointer-events:none;-webkit-mask:linear-gradient(#0B192C 0 0) content-box,linear-gradient(#0B192C 0 0);-webkit-mask-composite:xor;mask-composite:exclude;opacity:0;transition:opacity .5s}
.portais [role=tab] .giro::before{content:"";position:absolute;inset:-100%;background:conic-gradient(transparent 0 68%,rgba(255,158,125,.95) 82%,transparent 95%)}
.portais [role=tab]:hover::before,.portais [role=tab][aria-selected="true"]::before{opacity:1}
.portais [role=tab][aria-selected="true"]{border-color:rgba(255,158,125,.45);box-shadow:0 18px 46px -20px rgba(255,158,125,.6)}
.portais [role=tab][aria-selected="true"] .giro{opacity:1}
.portais [role=tab]:active{transform:scale(.97)}
.emblema{display:flex;width:38px;height:38px;align-items:center;justify-content:center;border:1px solid rgba(255,158,125,.32);border-radius:12px;transition:border-color .4s,box-shadow .5s}
.emblema svg{width:22px;height:22px;fill:none;stroke:var(--pessego);stroke-width:1.5;stroke-linecap:round;stroke-linejoin:round}
.portais [role=tab][aria-selected="true"] .emblema{border-color:rgba(255,158,125,.75);box-shadow:0 0 20px -4px rgba(255,158,125,.65)}
.portais .nome{display:block}
.portais .conta{display:block;margin-top:5px;font:400 .8125rem/1.2 var(--letra);letter-spacing:0;color:var(--titanio)}
.onda{position:absolute;z-index:-1;width:18px;height:18px;margin:-9px 0 0 -9px;border-radius:50%;background:radial-gradient(circle,rgba(255,158,125,.32),rgba(255,158,125,0) 70%);pointer-events:none;animation:onda .7s var(--mola) forwards}
@keyframes onda{from{transform:scale(1);opacity:1}to{transform:scale(24);opacity:0}}
.portal{position:relative;margin-top:16px;padding:20px 14px 12px;border:1px solid var(--aresta);border-radius:24px;background:var(--vidro);-webkit-backdrop-filter:blur(18px) saturate(120%);backdrop-filter:blur(18px) saturate(120%)}
.portal h2{margin:0 4px;font:650 1.375rem/1.2 var(--titulo);letter-spacing:-.015em;color:var(--titanio)}
.portal .sub{margin:6px 4px 14px;font-size:.9375rem;line-height:1.5;color:var(--nevoeiro)}
.portal[hidden],.card[hidden]{display:none}
.a-procurar .portais{display:none}
.grid{display:grid;gap:8px}
@media (min-width:640px){.grid{grid-template-columns:1fr 1fr}}
.card{position:relative;overflow:hidden;isolation:isolate;display:grid;grid-template-columns:44px 1fr;grid-template-areas:"ico t" "ico d";column-gap:14px;align-items:center;min-height:74px;padding:12px 14px;border:1px solid var(--aresta);border-radius:16px;color:var(--titanio);text-decoration:none;transition:border-color .35s,box-shadow .4s,transform .3s var(--mola)}
.card:hover,.card:focus-visible{border-color:rgba(255,158,125,.55);box-shadow:inset 0 0 0 1px rgba(255,158,125,.2),0 12px 32px -20px rgba(255,158,125,.7)}
.card:active{transform:scale(.985)}
.ico{grid-area:ico;display:flex;align-items:center;justify-content:center;width:44px;height:44px;border:1px solid rgba(255,158,125,.32);border-radius:13px;color:var(--pessego);transition:border-color .35s,box-shadow .45s}
.ico svg{width:22px;height:22px;fill:none;stroke:currentColor;stroke-width:1.5;stroke-linecap:round;stroke-linejoin:round}
.card:hover .ico,.card:focus-visible .ico{border-color:rgba(255,158,125,.75);box-shadow:0 0 18px -4px rgba(255,158,125,.6)}
.card b{grid-area:t;align-self:end;font:600 1rem/1.3 var(--letra)}
.card .d{grid-area:d;align-self:start;font-size:.875rem;line-height:1.45;color:var(--nevoeiro)}
.card .estado{display:table;margin:6px 0 2px;padding:2px 9px;border:1px solid rgba(255,158,125,.45);border-radius:999px;font-size:.75rem;line-height:1.4;color:var(--pessego-2)}
.rodape{margin-top:28px;padding:20px 18px;border:1px solid var(--aresta);border-radius:22px;background:var(--vidro);-webkit-backdrop-filter:blur(18px);backdrop-filter:blur(18px);color:var(--nevoeiro);font-size:.8125rem}
.rodape p{margin:0 0 8px;max-width:46em}
.avisos h2{margin:0 0 6px;font:650 1rem/1.3 var(--titulo);color:var(--titanio)}
.avisos dl{margin:0 0 12px}
.avisos dt{margin:12px 0 2px;font-weight:600;color:var(--titanio)}
.avisos dd{margin:0;max-width:46em;line-height:1.5}
.rodape a{color:var(--pessego);text-decoration:underline;text-underline-offset:3px}
.id{overflow-wrap:anywhere}
.id:empty{display:none}
:focus-visible{outline:2px solid var(--pessego);outline-offset:3px}
.card:focus-visible{outline-offset:-3px}
body.facil{font-size:19px}
body.facil .card b{font-size:1.125rem}
body.facil .card .d{font-size:1rem}
body.facil .portais [role=tab],body.facil .letra,body.facil .aviao{font-size:1.0625rem}
@media (max-width:380px){.portais{gap:8px}.portais [role=tab]{min-height:112px;padding:12px 10px 10px;font-size:.9375rem}}
@property --dx{syntax:'<length>';inherits:false;initial-value:0px}
@property --dy{syntax:'<length>';inherits:false;initial-value:0px}
@media (prefers-reduced-motion:no-preference){
.portais [role=tab][aria-selected="true"] .giro::before{animation:gira 7s linear infinite}
@keyframes gira{to{transform:rotate(360deg)}}
.portais [role=tab][aria-selected="true"] .emblema svg *{stroke-dasharray:64;animation:traca 1.1s var(--mola) both}
@keyframes traca{from{stroke-dashoffset:64}to{stroke-dashoffset:0}}
h1 .u{animation:respira 5.5s ease-in-out infinite}
@supports (content:"u"/""){
h1 .u{position:relative;z-index:0;animation:none;text-shadow:none}
h1 .u::before,h1 .u::after{content:"u"/"";position:absolute;left:0;top:0;z-index:-1;line-height:normal;color:transparent;pointer-events:none;animation:5.5s ease-in-out infinite}
h1 .u::before{text-shadow:0 0 14px rgba(255,158,125,.42),0 0 34px rgba(255,158,125,.18);animation-name:respira-sai}
h1 .u::after{text-shadow:0 0 22px rgba(255,158,125,.7),0 0 58px rgba(255,158,125,.32);opacity:0;animation-name:respira-entra}
@keyframes respira-sai{0%,100%{opacity:1}50%{opacity:0}}
@keyframes respira-entra{0%,100%{opacity:0}50%{opacity:1}}
}
.fam-acoes{display:flex;align-items:center;gap:8px}.fam-3d{display:inline-flex;align-items:center;justify-content:center;min-width:44px;min-height:44px;padding:0 14px;border:1px solid var(--aresta);border-radius:12px;background:var(--vidro);color:var(--titanio);font-weight:800;text-decoration:none}.fam-3d:focus-visible{outline:2px solid var(--pessego);outline-offset:2px}
.k-acoes{display:flex;flex-wrap:wrap;gap:8px;margin:0 0 14px}.k-acoes button{min-height:44px;padding:0 14px;border:1px solid var(--aresta);border-radius:12px;background:var(--vidro);color:var(--titanio);font:600 .875rem/1 var(--letra);cursor:pointer}.k-acoes button[aria-pressed="true"]{border-color:var(--pessego);color:var(--pessego)}
@keyframes respira{0%,100%{text-shadow:0 0 14px rgba(255,158,125,.42),0 0 34px rgba(255,158,125,.18)}50%{text-shadow:0 0 22px rgba(255,158,125,.7),0 0 58px rgba(255,158,125,.32)}}
.js .portal{animation:surge .45s var(--mola)}
@keyframes surge{from{opacity:0;transform:translateY(8px)}to{opacity:1;transform:none}}}
@media (prefers-reduced-motion:reduce){*,*::before,*::after{animation:none!important;transition:none!important}}
/* imersão 3D: a mesma função, com a paleta 2040 */
body .acoes .im3d-tools{display:contents}
body .im3d-tools{margin:16px 0 0}
body .acoes .im3d-tools small{flex-basis:100%}
body .im3d-tools small{color:var(--titanio)}
body .im3d-viewer{margin:12px 0 0;color:var(--titanio);font-size:.9375rem}
body .im3d-viewer summary{cursor:pointer;color:var(--titanio)}
body .im3d-viewer summary::marker{color:var(--pessego)}
:root.im3d-active{background:var(--abissal)}
"""

JS_PORTAIS = """
(function(){
 var tabs=[].slice.call(document.querySelectorAll('.portais [role=tab]'));
 if(!tabs.length)return;
 document.documentElement.classList.add('js');
 function abrir(t,foco){
  tabs.forEach(function(x){var on=x===t;x.setAttribute('aria-selected',on?'true':'false');x.tabIndex=on?0:-1;
   var p=document.getElementById(x.getAttribute('aria-controls'));if(p)p.hidden=!on});
  if(foco)t.focus();
  try{localStorage.setItem('konfirmu_portal',t.id)}catch(_){}
 }
 tabs.forEach(function(t,i){
  t.addEventListener('click',function(){abrir(t)});
  t.addEventListener('keydown',function(e){var n=null;
   if(e.key==='ArrowRight')n=tabs[(i+1)%tabs.length];else if(e.key==='ArrowLeft')n=tabs[(i-1+tabs.length)%tabs.length];
   else if(e.key==='Home')n=tabs[0];else if(e.key==='End')n=tabs[tabs.length-1];
   if(n){e.preventDefault();abrir(n,true)}});
 });
 var guardado=null;try{guardado=document.getElementById(localStorage.getItem('konfirmu_portal'))}catch(_){}
 abrir(guardado&&tabs.indexOf(guardado)>=0?guardado:tabs[0]);
})();
// Procura instantânea: mostra os cartões que batem, de todos os portais, agrupados pelo portal.
(function(){
 var campo=document.getElementById('procura');if(!campo)return;
 campo.parentNode.hidden=false;
 var secs=[].slice.call(document.querySelectorAll('.portal'));
 var tabs=[].slice.call(document.querySelectorAll('.portais [role=tab]'));
 var estado=document.getElementById('sem');
 function norm(t){return t.normalize('NFD').replace(/[\u0300-\u036f]/g,'').toLowerCase()}
 function aplicar(){
  var q=norm(campo.value.trim());
  document.body.classList.toggle('a-procurar',!!q);
  if(!q){
   [].forEach.call(document.querySelectorAll('a.card'),function(a){a.hidden=false});
   var sel=tabs.filter(function(t){return t.getAttribute('aria-selected')==='true'})[0]||tabs[0];
   secs.forEach(function(s){s.hidden=!sel||s.id!==sel.getAttribute('aria-controls')});
   estado.textContent='';return}
  var total=0;
  secs.forEach(function(s){var n=0;
   [].forEach.call(s.querySelectorAll('a.card'),function(a){var ok=norm(a.textContent).indexOf(q)>=0;a.hidden=!ok;if(ok)n++});
   s.hidden=!n;total+=n});
  estado.textContent=total?(total===1?'1 atividade encontrada.':total+' atividades encontradas.'):'Nenhuma atividade tem «'+campo.value.trim()+'». Experimenta outra palavra.';
 }
 campo.addEventListener('input',aplicar);
 campo.addEventListener('keydown',function(e){if(e.key==='Escape'&&campo.value){campo.value='';aplicar()}});
})();
// A imersão 3D põe os seus controlos a seguir ao título; aqui passam para a fila de ações.
document.addEventListener('DOMContentLoaded',function(){
 var acoes=document.querySelector('.acoes'),t=document.querySelector('.im3d-tools'),v=document.querySelector('.im3d-viewer');
 if(acoes&&t)acoes.appendChild(t);
 if(acoes&&v)acoes.after(v);
});
"""

JS_BASE = """function toHex(u8){var s='';for(var i=0;i<u8.length;i++)s+=('0'+u8[i].toString(16)).slice(-2);return s}
var pk;
try{pk=localStorage.getItem("konfirmu_id")}catch(_){}
if(!pk){var kp=nacl.sign.keyPair();pk=toHex(kp.publicKey);try{localStorage.setItem('konfirmu_id',pk)}catch(_){}}
function facil(){var on=document.body.classList.toggle('facil');var b=document.querySelector('.letra');if(b)b.setAttribute('aria-pressed',on?'true':'false')}
document.getElementById("id").textContent="A tua chave neste aparelho: " + pk.slice(0,16) + "…";"""

JS_AVIAO = """// 27-11-2026: o início passa a ligar a cache sem rede (antes só o verificador a ligava).
if(location.protocol!=="file:"&&"serviceWorker" in navigator){navigator.serviceWorker.register("./sw.js").catch(function(){});}
// 27-11-2026 (aprovado pelo David às 02:53): botão «Preparar modo avião». Guarda as peças da app neste aparelho e diz quantas estão guardadas.
function esperarGuarda(reg){return new Promise(function(ok,falha){var t0=Date.now();(function ver(){var w=reg.active;if(w&&/\\/sw\\.js$/.test(w.scriptURL)&&w.state==="activated")return ok(w);if(Date.now()-t0>60000)return falha(new Error("sem resposta"));setTimeout(ver,250)})()})}
function prepararAviao(){var el=document.getElementById("aviaoEstado");
 if(location.protocol==="file:"||!("serviceWorker" in navigator)){el.textContent="Este navegador não guarda a app para usar sem rede.";return}
 el.textContent="A guardar as peças neste aparelho…";
 navigator.serviceWorker.register("./sw.js").then(esperarGuarda).then(function(w){return new Promise(function(ok,falha){var c=new MessageChannel();c.port1.onmessage=function(e){ok(e.data)};w.postMessage({tipo:"konfirmu-preparar"},[c.port2]);setTimeout(function(){falha(new Error("sem resposta"))},120000)})})
 .then(function(r){el.textContent=r.guardadas===r.total?r.guardadas+" de "+r.total+" peças guardadas. Já podes ligar o modo avião.":r.guardadas+" de "+r.total+" peças guardadas. Faltam "+(r.total-r.guardadas)+". Liga a rede e carrega outra vez."})
 .catch(function(e){el.textContent="Não consegui confirmar ("+e.message+"). Liga a rede e carrega outra vez."})}
document.getElementById("aviao").onclick=prepararAviao;"""


NUCLEO_CEU = """// O céu do menu: aurora e partículas quentes em WebGL (Canvas 2D só sem WebGL). Uma só fonte para os dois sítios onde corre:
// no trabalhador (assets/ceu_vivo.js, fora da linha principal da página) e, se não houver trabalhador, na própria página.
function criarCeu(A,P,novaTela,semGL,DPR){
 var dpr=Math.min(DPR||1,1)*.75,W=0,H=0,rolar=0,t0=performance.now();
 var incl={x:0,y:0},alvo={x:0,y:0},toque=null,ondas=[],ps=[];
 var gl=null,uT,uR,uL,uS;
 try{gl=A.getContext('webgl',{alpha:false,antialias:false,depth:false,stencil:false,powerPreference:'low-power'})}catch(_){}
 if(gl){
  var VS='attribute vec2 p;void main(){gl_Position=vec4(p,0.,1.);}';
  var FS=['precision mediump float;uniform float t;uniform vec2 r;uniform vec2 l;uniform float s;',
   'float h(vec2 p){return fract(sin(dot(p,vec2(127.1,311.7)))*43758.5453);}',
   'float n(vec2 p){vec2 i=floor(p),f=fract(p);f=f*f*(3.-2.*f);return mix(mix(h(i),h(i+vec2(1.,0.)),f.x),mix(h(i+vec2(0.,1.)),h(i+vec2(1.,1.)),f.x),f.y);}',
   'float fbm(vec2 p){float v=0.,a=.5;for(int k=0;k<5;k++){v+=a*n(p);p=p*2.03+vec2(1.7,9.2);a*=.5;}return v;}',
   'void main(){vec2 uv=gl_FragCoord.xy/r;vec2 q=uv;q.x*=r.x/r.y;q+=l*.08;float z=t*.03;',
   'float a=fbm(vec2(q.x*1.3+z,q.y*.8-z*.7));float b=fbm(vec2(q.x*2.1-z*.9,q.y*1.2+z*.5)+a*1.4);',
   'float c1=.66+.16*(a-.5)+.05*sin(q.x*2.3+z*4.);float b1=smoothstep(.22,0.,abs(uv.y-c1))*(.55+.6*b);',
   'float c2=.82+.12*(b-.5);float b2=smoothstep(.16,0.,abs(uv.y-c2))*(.4+.5*a);',
   'float g=clamp(b1+.7*b2+.18*fbm(q*2.6-z),0.,1.);',
   'float topo=mix(.5,1.,smoothstep(.5,.75,uv.y));float k=g*mix(topo,.5,s);',
   'vec3 fundo=vec3(.043,.098,.172);vec3 brasa=mix(vec3(.36,.22,.17),vec3(.35,.23,.16),b);',
   'vec3 cor=mix(fundo,brasa,k);float v=1.-.35*pow(length((uv-vec2(.5,.62))*vec2(1.,1.3)),1.6);',
   'gl_FragColor=vec4(cor*clamp(v,.6,1.),1.);}'].join('\\n');
  var sh=function(tipo,src){var o=gl.createShader(tipo);gl.shaderSource(o,src);gl.compileShader(o);return gl.getShaderParameter(o,gl.COMPILE_STATUS)?o:null};
  var vs=sh(gl.VERTEX_SHADER,VS),fs=sh(gl.FRAGMENT_SHADER,FS),pr=gl.createProgram();
  if(vs&&fs){gl.attachShader(pr,vs);gl.attachShader(pr,fs);gl.linkProgram(pr)}
  if(!vs||!fs||!gl.getProgramParameter(pr,gl.LINK_STATUS)){gl=null}else{
   gl.useProgram(pr);gl.bindBuffer(gl.ARRAY_BUFFER,gl.createBuffer());
   gl.bufferData(gl.ARRAY_BUFFER,new Float32Array([-1,-1,1,-1,-1,1,1,1]),gl.STATIC_DRAW);
   var lp=gl.getAttribLocation(pr,'p');gl.enableVertexAttribArray(lp);gl.vertexAttribPointer(lp,2,gl.FLOAT,false,0,0);
   uT=gl.getUniformLocation(pr,'t');uR=gl.getUniformLocation(pr,'r');uL=gl.getUniformLocation(pr,'l');uS=gl.getUniformLocation(pr,'s');
  }
 }
 function perdeuGL(){if(gl!==false){gl=null;semGL()}}
 if(!gl)perdeuGL();
 if(A.addEventListener)A.addEventListener('webglcontextlost',function(e){e.preventDefault();perdeuGL()});
 // As faíscas desenham-se em WebGL: pontos com o mesmo degradê pêssego da imagem de antes. Em Canvas 2D, a 60 quadros
 // por segundo, a memória subia sem parar com a página parada (medido no computador: de 37 para 61 MB em 75 s).
 // Sem WebGL, ficam em Canvas 2D, com a faísca guardada como imagem fixa (ImageBitmap).
 var pg=null,pP=null,pA=null,pB=null,pQ=null,pD=null,pR,pAr,pAc,pAk,cx=null,fa=null;
 // ponto: x, y, tamanho e brilho (em píxeis da tela); o degradê vai de 1 no centro a .5 aos 30 % e a 0 na borda
 var FV='attribute vec4 a;uniform vec2 r;varying float al;void main(){gl_Position=vec4(a.x/r.x*2.-1.,1.-a.y/r.y*2.,0.,1.);gl_PointSize=a.z;al=a.w;}',
  FF='precision mediump float;varying float al;void main(){float d=length(gl_PointCoord-.5)*2.;float g=d<.3?1.-d/.3*.5:.5*(1.-d)/.7;float x=max(g,0.)*al;gl_FragColor=vec4(vec3(1.,.6196,.4902)*x,x);}',
 // onda do toque: um anel com a espessura e o brilho de antes (sem uniformes partilhados: as precisões não batem)
  OV='attribute vec2 a;uniform vec2 r;uniform vec3 c;varying vec2 e;varying float rz;void main(){e=a*(c.z+4.);rz=c.z;vec2 p=c.xy+e;gl_Position=vec4(p.x/r.x*2.-1.,1.-p.y/r.y*2.,0.,1.);}',
  OF='#ifdef GL_FRAGMENT_PRECISION_HIGH\\nprecision highp float;\\n#else\\nprecision mediump float;\\n#endif\\nuniform vec2 k;varying vec2 e;varying float rz;void main(){float x=clamp(k.y*.5+.5-abs(length(e)-rz),0.,1.)*k.x;gl_FragColor=vec4(vec3(1.,.6196,.4902)*x,x);}';
 function prog(g,vsrc,fsrc){var v=g.createShader(g.VERTEX_SHADER),f=g.createShader(g.FRAGMENT_SHADER),o=g.createProgram();
  g.shaderSource(v,vsrc);g.compileShader(v);g.shaderSource(f,fsrc);g.compileShader(f);
  g.attachShader(o,v);g.attachShader(o,f);g.bindAttribLocation(o,0,'a');g.linkProgram(o);
  return g.getProgramParameter(o,g.LINK_STATUS)?o:null}
 // ensaio numa tela à parte: a tela das faíscas só aceita um tipo de desenho, por isso só passa a WebGL se os dois programas ligarem
 var ens=null;try{var te=novaTela(1,1);ens=te.getContext('webgl')}catch(_){}
 if(ens){var okE=!!(prog(ens,FV,FF)&&prog(ens,OV,OF));var pe=ens.getExtension('WEBGL_lose_context');if(pe)pe.loseContext();ens=null;
  if(okE){try{pg=P.getContext('webgl',{alpha:true,premultipliedAlpha:true,antialias:false,depth:false,stencil:false,powerPreference:'low-power'})}catch(_){}}}
 if(pg){pP=prog(pg,FV,FF);pA=prog(pg,OV,OF);
  if(!pP){pg=null}else{
   pD=new Float32Array(480);pB=pg.createBuffer();pg.bindBuffer(pg.ARRAY_BUFFER,pB);pg.bufferData(pg.ARRAY_BUFFER,pD.byteLength,pg.DYNAMIC_DRAW);
   pQ=pg.createBuffer();pg.bindBuffer(pg.ARRAY_BUFFER,pQ);pg.bufferData(pg.ARRAY_BUFFER,new Float32Array([-1,-1,1,-1,-1,1,1,1]),pg.STATIC_DRAW);
   pR=pg.getUniformLocation(pP,'r');if(pA){pAr=pg.getUniformLocation(pA,'r');pAc=pg.getUniformLocation(pA,'c');pAk=pg.getUniformLocation(pA,'k')}
   pg.enableVertexAttribArray(0);pg.enable(pg.BLEND);pg.blendFunc(pg.ONE,pg.ONE_MINUS_SRC_ALPHA);pg.clearColor(0,0,0,0);
   if(P.addEventListener)P.addEventListener('webglcontextlost',function(e){e.preventDefault();pg=null});
  }
 }
 if(!pg&&!cx){try{cx=P.getContext('2d')}catch(_){}}
 if(cx){fa=novaTela(64,64);
  (function(){var g=fa.getContext('2d'),gr=g.createRadialGradient(32,32,0,32,32,32);
   gr.addColorStop(0,'rgba(255,158,125,1)');gr.addColorStop(.3,'rgba(255,158,125,.5)');gr.addColorStop(1,'rgba(255,158,125,0)');
   g.fillStyle=gr;g.fillRect(0,0,64,64)})();
  if(fa.transferToImageBitmap)fa=fa.transferToImageBitmap();
 }
 function medir(w,h){
  var nW=Math.round(w*dpr),nH=Math.round(h*dpr);
  if(gl){A.width=Math.max(1,Math.round(w*.35));A.height=Math.max(1,Math.round(h*.35))}
  if(nW!==W||nH!==H){
   var sx=W?nW/W:1,sy=H?nH/H:1;W=P.width=nW;H=P.height=nH;
   var alvoN=Math.round(Math.min(120,Math.max(40,w*h/9000)));
   ps.forEach(function(p){p.x*=sx;p.y*=sy});
   while(ps.length<alvoN)ps.push({x:Math.random()*W,y:Math.random()*H,vx:0,vy:0,r:(1.6+Math.random()*2.8)*dpr,f:Math.random()*6.283,v:.12+Math.random()*.3});
   ps.length=alvoN;
  }
 }
 function aurora(agora){
  if(!gl)return;
  gl.viewport(0,0,A.width,A.height);gl.uniform1f(uT,(agora-t0)/1000);gl.uniform2f(uR,A.width,A.height);
  gl.uniform2f(uL,incl.x,-incl.y);gl.uniform1f(uS,rolar);gl.drawArrays(gl.TRIANGLE_STRIP,0,4);
 }
 function faiscas(dt,k){
  if(!pg&&!cx)return;
  if(cx)cx.clearRect(0,0,W,H);
  for(var i=0;i<ps.length;i++){var p=ps[i];
   p.f+=.012*k;var ax=0,ay=0;
   if(toque){var dx=p.x-toque.x,dy=p.y-toque.y,d2=dx*dx+dy*dy,R=(toque.forte?130:90)*dpr;
    if(d2<R*R){var d=Math.sqrt(d2)||1,fz=(1-d/R)*(toque.forte?1:.45)*dpr;ax+=dx/d*fz;ay+=dy/d*fz}}
   p.vx=p.vx*.94+(ax*.12+incl.x*.05*dpr)*k;p.vy=p.vy*.94+(ay*.12+incl.y*.05*dpr)*k;
   p.x+=(p.vx+Math.sin(p.f)*.18*dpr)*k;p.y+=(p.vy-p.v*dpr)*k;
   if(p.y<-12*dpr){p.y=H+12*dpr;p.x=Math.random()*W}else if(p.y>H+12*dpr)p.y=-12*dpr;
   if(p.x<-12*dpr)p.x=W+12*dpr;else if(p.x>W+12*dpr)p.x=-12*dpr;
   // teto do brilho: .12 na metade de cima (onde a aurora é mais forte), .2 em baixo
   var teto=p.y<H*.5?.12:.2,al=teto*(.55+.45*Math.sin(p.f*1.7)),s=p.r*6;
   if(pg){pD[i*4]=p.x;pD[i*4+1]=p.y;pD[i*4+2]=s;pD[i*4+3]=al}
   else{cx.globalAlpha=al;cx.drawImage(fa,p.x-s/2,p.y-s/2,s,s)}
  }
  if(pg){
   pg.viewport(0,0,W,H);pg.clear(pg.COLOR_BUFFER_BIT);
   pg.useProgram(pP);pg.uniform2f(pR,W,H);pg.bindBuffer(pg.ARRAY_BUFFER,pB);pg.bufferSubData(pg.ARRAY_BUFFER,0,pD);
   pg.vertexAttribPointer(0,4,pg.FLOAT,false,0,0);pg.drawArrays(pg.POINTS,0,ps.length);
   if(ondas.length&&pA){pg.useProgram(pA);pg.uniform2f(pAr,W,H);pg.bindBuffer(pg.ARRAY_BUFFER,pQ);pg.vertexAttribPointer(0,2,pg.FLOAT,false,0,0)}
  }else cx.globalAlpha=1;
  for(var j=ondas.length-1;j>=0;j--){var o=ondas[j];o.t+=dt;var u=o.t/900;
   if(u>=1){ondas.splice(j,1);continue}
   var rr=(1-Math.pow(1-u,3))*160*dpr;
   if(pg){if(pA){pg.uniform3f(pAc,o.x,o.y,rr);pg.uniform2f(pAk,.35*(1-u),1.5*dpr);pg.drawArrays(pg.TRIANGLE_STRIP,0,4)}}
   else{cx.beginPath();cx.arc(o.x,o.y,rr,0,6.2832);
    cx.strokeStyle='rgba(255,158,125,'+(.35*(1-u)).toFixed(3)+')';cx.lineWidth=1.5*dpr;cx.stroke()}
   for(var m=0;m<ps.length;m++){var q=ps[m],ex=q.x-o.x,ey=q.y-o.y,dd=Math.sqrt(ex*ex+ey*ey)||1;
    if(Math.abs(dd-rr)<14*dpr){q.vx+=ex/dd*.6*dpr;q.vy+=ey/dd*.6*dpr}}
  }
 }
 var luzAX=-1,luzAY=-1,luzX=50,luzY=24;
 // passos de 2 % com margem (histerese): o tremor da mão não reescreve a luz a cada quadro
 function segue(atual,alvo,passo){return Math.abs(alvo-atual)>=passo?Math.round(alvo/passo)*passo:atual}
 return {
  medir:medir,
  // um quadro: devolve a posição nova da luz dos portais quando muda (em %), senão null
  quadro:function(agora,dt){
   var k=dt/16.667;
   incl.x+=(alvo.x-incl.x)*Math.min(1,.06*k);incl.y+=(alvo.y-incl.y)*Math.min(1,.06*k);
   aurora(agora);faiscas(dt,k);
   luzX=segue(luzX,50+incl.x*35,2);luzY=segue(luzY,24+incl.y*28,2);
   if(luzX===luzAX&&luzY===luzAY)return null;luzAX=luzX;luzAY=luzY;return [luzX,luzY];
  },
  parado:function(){aurora(t0+9000);faiscas(0,0)},
  receber:function(m){
   if(m.tipo==='alvo'){alvo.x=m.x;alvo.y=m.y}
   else if(m.tipo==='toque'){toque=m.t?{x:m.t.x*dpr,y:m.t.y*dpr,forte:m.t.forte}:null}
   else if(m.tipo==='onda'){ondas.push({x:m.x*dpr,y:m.y*dpr,t:0})}
   else if(m.tipo==='rolar'){rolar=m.v}
   else if(m.tipo==='medida'){medir(m.larg,m.alt)}
  }
 };
}
"""

JS_VIVO = NUCLEO_CEU + """// Atmosfera viva (ordem do David, 27-11-2026, 13:21): aurora e partículas quentes em WebGL (Canvas 2D só sem WebGL).
// Respira sozinha e segue o toque e a inclinação do telemóvel. Sem rede e sem bibliotecas.
// As cores ficam abaixo de um teto, para o texto manter o contraste AAA. Com «reduzir movimento», fica uma imagem parada.
// Memória (ordem do David, 27-11-2026, 17:42): o céu desenha num trabalhador à parte (assets/ceu_vivo.js). A página só
// recebe a posição da luz dos portais quando ela muda; assim não refaz estilos a cada quadro e a memória fica estável.
// Sem trabalhador (navegadores antigos, ou se o ficheiro falhar), o mesmo céu corre aqui, como antes.
(function(){
 var A=document.getElementById('aurora'),P=document.getElementById('faiscas');
 if(!A||!P||!P.getContext)return;
 var calmo=!!(window.matchMedia&&matchMedia('(prefers-reduced-motion: reduce)').matches);
 var DPR=window.devicePixelRatio||1,ratoTab=0,ultimaLuz=null,esperaLuz=0,mandar=function(){},retomar=function(){},pausar=function(){};
 var tabs=[].slice.call(document.querySelectorAll('.portais [role=tab]'));
 function aplicarLuz(mx,my){tabs.forEach(function(t){t.style.setProperty('--dx',((mx-50)/100*t.clientWidth).toFixed(1)+'px');t.style.setProperty('--dy',((my-22)/100*t.clientHeight).toFixed(1)+'px')})}
 function luz(mx,my){ultimaLuz=[mx,my];if(performance.now()-ratoTab>=1500)aplicarLuz(mx,my)}
 function semWebgl(){A.style.display='none';document.documentElement.classList.add('sem-webgl')}
 function aqui(){
  var ceu=criarCeu(A,P,function(w,h){if(typeof OffscreenCanvas==='function')return new OffscreenCanvas(w,h);var c=document.createElement('canvas');c.width=w;c.height=h;return c},semWebgl,DPR);
  ceu.medir(innerWidth,innerHeight);
  if(calmo){ceu.parado();mandar=function(m){ceu.receber(m);if(m.tipo==='medida')ceu.parado()};return}
  var vivo=true,ult=performance.now();
  function quadro(agora){if(!vivo)return;var dt=Math.min(50,agora-ult);ult=agora;var l=ceu.quadro(agora,dt);if(l)luz(l[0],l[1]);requestAnimationFrame(quadro)}
  requestAnimationFrame(quadro);
  mandar=function(m){ceu.receber(m)};
  pausar=function(){vivo=false};
  retomar=function(){if(!vivo){vivo=true;ult=performance.now();requestAnimationFrame(quadro)}};
 }
 function telaNova(c){var n=document.createElement('canvas');n.id=c.id;n.className=c.className;n.setAttribute('aria-hidden','true');c.parentNode.replaceChild(n,c);return n}
 var trab=null;
 if(!calmo&&window.Worker&&A.transferControlToOffscreen&&P.transferControlToOffscreen){
  try{
   trab=new Worker('./assets/ceu_vivo.js');
   var oa=A.transferControlToOffscreen(),op=P.transferControlToOffscreen();
   trab.postMessage({tipo:'inicio',aurora:oa,faiscas:op,dpr:DPR,larg:innerWidth,alt:innerHeight},[oa,op]);
   trab.onmessage=function(e){var d=e.data;if(d.tipo==='luz')luz(d.mx,d.my);else if(d.tipo==='semWebgl')semWebgl()};
   // se o ficheiro do trabalhador falhar, as telas já foram entregues: troca-as por telas novas e desenha aqui
   trab.onerror=function(){if(!trab)return;trab.terminate();trab=null;A=telaNova(A);P=telaNova(P);aqui()};
   mandar=function(m){if(trab)trab.postMessage(m)};
   pausar=function(){mandar({tipo:'pausa'})};
   retomar=function(){mandar({tipo:'retoma'})};
  }catch(_){trab=null}
 }
 if(!trab)aqui();
 addEventListener('resize',function(){mandar({tipo:'medida',larg:innerWidth,alt:innerHeight})});
 var rolarUlt=-1;
 addEventListener('scroll',function(){var v=Math.min(1,(window.scrollY||0)/160);if(v!==rolarUlt){rolarUlt=v;mandar({tipo:'rolar',v:v})}},{passive:true});
 var toque=null;
 addEventListener('pointerdown',function(e){toque={x:e.clientX,y:e.clientY,forte:true,id:e.pointerId};mandar({tipo:'toque',t:toque});if(!calmo)mandar({tipo:'onda',x:e.clientX,y:e.clientY})},{passive:true});
 addEventListener('pointermove',function(e){
  if(toque&&toque.id===e.pointerId){toque.x=e.clientX;toque.y=e.clientY;mandar({tipo:'toque',t:toque})}
  else if(e.pointerType==='mouse'){toque={x:e.clientX,y:e.clientY,forte:false,id:e.pointerId};mandar({tipo:'toque',t:toque});
   mandar({tipo:'alvo',x:(e.clientX/innerWidth-.5)*1.2,y:(e.clientY/innerHeight-.5)*1.2})}
  if(e.target&&e.target.closest&&e.target.closest('.portais [role=tab]')){ratoTab=performance.now();clearTimeout(esperaLuz);
   esperaLuz=setTimeout(function(){if(ultimaLuz)aplicarLuz(ultimaLuz[0],ultimaLuz[1])},1550)}
 },{passive:true});
 function largar(e){if(toque&&toque.id===e.pointerId&&e.pointerType!=='mouse'){toque=null;mandar({tipo:'toque',t:null})}}
 addEventListener('pointerup',largar,{passive:true});addEventListener('pointercancel',largar,{passive:true});
 document.addEventListener('mouseleave',function(){toque=null;mandar({tipo:'toque',t:null})});
 var alvoX=0,alvoY=0;
 function orientar(e){if(e.gamma==null)return;var x=Math.max(-1,Math.min(1,e.gamma/25)),y=Math.max(-1,Math.min(1,((e.beta||45)-45)/25));
  if(Math.abs(x-alvoX)<.004&&Math.abs(y-alvoY)<.004)return;alvoX=x;alvoY=y;mandar({tipo:'alvo',x:x,y:y})}
 var DOE=window.DeviceOrientationEvent;
 if(DOE&&typeof DOE.requestPermission==='function'){
  // iPhone: a inclinação só funciona depois de um toque; o pedido é do próprio Safari e os dados ficam no aparelho.
  document.addEventListener('click',function pedir(){document.removeEventListener('click',pedir);
   try{DOE.requestPermission().then(function(r){if(r==='granted')addEventListener('deviceorientation',orientar)}).catch(function(){})}catch(_){}});
 }else if(DOE){addEventListener('deviceorientation',orientar)}
 document.addEventListener('visibilitychange',function(){if(document.hidden)pausar();else if(!calmo)retomar()});
})();
// Portais e cartões: luz que segue o dedo, onda ao tocar e um toque curto de vibração onde o aparelho deixa.
(function(){
 var calmo=!!(window.matchMedia&&matchMedia('(prefers-reduced-motion: reduce)').matches);
 document.addEventListener('pointerdown',function(e){
  var el=e.target&&e.target.closest&&e.target.closest('.portais [role=tab], a.card');if(!el)return;
  if(el.classList.contains('tigela'))return; // as tigelas têm a sua própria luz e vibração (PR #19): uma só resposta ao toque
  if(!calmo){var r=el.getBoundingClientRect(),o=document.createElement('span');o.className='onda';
   o.style.left=(e.clientX-r.left)+'px';o.style.top=(e.clientY-r.top)+'px';el.appendChild(o);setTimeout(function(){o.remove()},750);
   try{if(navigator.vibrate)navigator.vibrate(8)}catch(_){}}
 },{passive:true});
 document.addEventListener('pointermove',function(e){
  var el=e.target&&e.target.closest&&e.target.closest('.portais [role=tab]');if(!el)return;
  var r=el.getBoundingClientRect();
  el.style.setProperty('--dx',(e.clientX-r.left-r.width*.5).toFixed(1)+'px');
  el.style.setProperty('--dy',(e.clientY-r.top-r.height*.22).toFixed(1)+'px');
 },{passive:true});
})();
"""


TRABALHADOR_CEU = """// assets/ceu_vivo.js — gerado por scripts/gerar_menu.py. Não editar à mão.
// O céu vivo do menu desenhado fora da linha principal da página (OffscreenCanvas): a página não repinta a cada quadro.
'use strict';
""" + NUCLEO_CEU + """var ceu=null,vivo=false,ult=0;
var pedir=self.requestAnimationFrame?function(f){self.requestAnimationFrame(f)}:function(f){setTimeout(function(){f(performance.now())},16)};
function quadro(agora){if(!vivo)return;var dt=Math.min(50,agora-ult);ult=agora;var l=ceu.quadro(agora,dt);if(l)postMessage({tipo:'luz',mx:l[0],my:l[1]});pedir(quadro)}
onmessage=function(e){var d=e.data;
 if(d.tipo==='inicio'){
  ceu=criarCeu(d.aurora,d.faiscas,function(w,h){return new OffscreenCanvas(w,h)},function(){postMessage({tipo:'semWebgl'})},d.dpr);
  ceu.medir(d.larg,d.alt);vivo=true;ult=performance.now();pedir(quadro);return;
 }
 if(!ceu)return;
 if(d.tipo==='pausa'){vivo=false}
 else if(d.tipo==='retoma'){if(!vivo){vivo=true;ult=performance.now();pedir(quadro)}}
 else ceu.receber(d);
};
"""


def avisos_pt(repo):
    """Os 5 avisos legais em português, tirados da avisos_legais.html (pedido #14). Sem ela, para."""
    caminho = os.path.join(repo, "avisos_legais.html")
    texto = open(caminho, encoding="utf-8").read()
    m = re.search(r'"pt"\s*:\s*\{.*?"a"\s*:\s*(\[\s*\[.*?\]\s*\])', texto, re.S)
    if not m:
        raise SystemExit("não encontrei os avisos em português na avisos_legais.html")
    itens = json.loads(m.group(1))
    if len(itens) != 5:
        raise SystemExit("esperava 5 avisos legais, encontrei %d" % len(itens))
    return itens


def cartao(href, icone, titulo, descricao, estado):
    extra = '<span class="estado">%s</span>' % estado if estado else ""
    return ('<a class="card" href="%s"><span class="ico" aria-hidden="true"><svg viewBox="0 0 24 24">%s</svg></span>'
            '<b>%s</b><span class="d">%s%s</span></a>' % (href, ICONES[icone], titulo, descricao, extra))


CSP_MENU = ("default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'; img-src 'self' data: blob:; media-src 'self' data: blob: mediastream:; "
            "connect-src 'self'; worker-src 'self'; manifest-src 'self'; font-src 'self' data:; object-src 'none'; base-uri 'none'; form-action 'none'")


def pagina(variante, avisos, pt, dados_json):
    edicao = variante == "edicao21"
    web = variante == "web"
    partes = ['<!DOCTYPE html>', '<html lang="pt">', '<head>', '<meta charset="UTF-8">',
              '<meta name="viewport" content="width=device-width, initial-scale=1.0">',
              '<meta name="theme-color" content="#0B192C">',
              '<meta name="color-scheme" content="dark">',
              '<meta name="konfirmu-portal" content="menu">',
              '<meta http-equiv="Content-Security-Policy" content="%s">' % CSP_MENU,
              '<title>Konfirmu</title>',
              # ícone dentro da página: o «u» pêssego; sem pedido ao servidor (sem favicon.ico 404)
              '<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns=\'http://www.w3.org/2000/svg\' viewBox=\'0 0 32 32\'%3E%3Crect width=\'32\' height=\'32\' rx=\'7\' fill=\'%230B192C\'/%3E%3Ctext x=\'16\' y=\'22.5\' font-family=\'Inter,Arial,sans-serif\' font-size=\'21\' font-weight=\'700\' text-anchor=\'middle\' fill=\'%23FF9E7D\'%3Eu%3C/text%3E%3C/svg%3E">',
              '<style>' + CSS.strip() + tigelas.CSS_FAMILIA.rstrip() + '</style>',
              '<link rel="stylesheet" href="./assets/imersao.css">',
              '<script defer src="./assets/imersao.js" data-viewer></script>']
    if edicao or web:
        partes.append('<link rel="manifest" href="./manifest.json">')
    partes += ['</head>', '<body>', tigelas.DEFS_PARTILHADAS,
               '<canvas id="aurora" class="ceu" aria-hidden="true"></canvas><canvas id="faiscas" class="ceu" aria-hidden="true"></canvas>',
               '<header>',
               '<h1>Konfirm<span class="u">u</span></h1>',
               '<p class="intro">Aquilo que importa, confirmado e guardado contigo. Corre no teu aparelho e, depois da primeira visita, funciona também sem rede.</p>',
               '<div class="acoes"><button type="button" class="letra" onclick="facil()" aria-pressed="false">Letra maior</button>'
               + ('' if edicao else '<button id="aviao" class="aviao" type="button">Preparar modo avião</button>') + '</div>']
    if not edicao:
        partes.append('<span id="aviaoEstado" class="aviao-estado" role="status" aria-live="polite"></span>')
    partes.append('</header>')
    partes.append('<div class="procura" hidden><label for="procura">Procurar atividade</label>'
                  '<input id="procura" type="search" autocomplete="off" enterkeyhint="search" placeholder="Por exemplo: verificar, carta, família"></div>')
    partes.append('<p id="sem" class="sem-resultados" role="status" aria-live="polite"></p>')
    partes.append('<nav class="portais" role="tablist" aria-label="Portais">')
    for chave, rotulo, _, _, itens in PORTAIS:
        n = sum(1 for it in itens if web or (edicao and it[0] not in SO_NA_RAIZ) or (not edicao and it[0] not in SO_NA_EDICAO_21))
        if chave == "fam":
            rotulo = '<bdi data-k="fam.rotulo">%s</bdi>' % html.escape(pt["fam.rotulo"])
        partes.append('<button type="button" role="tab" id="t-%s" aria-controls="p-%s" aria-selected="false"><span class="giro" aria-hidden="true"></span>'
                      '<span class="emblema" aria-hidden="true"><svg viewBox="0 0 24 24">%s</svg></span>'
                      '<span><span class="nome">%s</span><span class="conta">%d atividades</span></span></button>'
                      % (chave, chave, EMBLEMAS[chave], rotulo, n))
    partes.append('</nav>')
    total = 0
    for chave, _, titulo, sub, itens in PORTAIS:
        if chave == "fam":
            # o portal das tigelas: textos de locales/pt.json, desenho de scripts/tigelas.py
            hrefs = [i[0] for i in itens if edicao or web or i[0] not in SO_NA_EDICAO_21]
            secao, _ = tigelas.secao_familia(hrefs, pt, html.escape)
            if web:
                # Na app web a entrada é o Modo Família 3D (index.html); daqui volta-se a ele (ordem do David, 27-11, 17:42).
                botao = '<button type="button" class="fam-lingua"'
                assert secao.count(botao) == 1
                ini = secao.index(botao)
                fim = secao.index('</button>', ini) + len('</button>')
                secao = (secao[:ini] + '<div class="fam-acoes"><a class="fam-3d" href="./" aria-label="3D">3D</a>'
                         + secao[ini:fim] + '</div>' + secao[fim:])
            partes.append(secao)
            total += len(hrefs)
            continue
        partes.append('<section class="portal" id="p-%s" role="tabpanel" aria-labelledby="t-%s">' % (chave, chave))
        partes.append('<h2>%s</h2><p class="sub">%s</p>' % (titulo, sub))
        partes.append('<div class="grid">')
        for href, icone, nome, descricao, estado in itens:
            if href in SO_NA_EDICAO_21 and not (edicao or web):
                continue
            if href in SO_NA_RAIZ and edicao:
                continue
            partes.append(cartao(href, icone, nome, descricao, estado))
            total += 1
        partes += ['</div>', '</section>']
    bloco = ['<section class="avisos" aria-labelledby="avisos-t">', '<h2 id="avisos-t">Avisos legais</h2>', '<dl>']
    for titulo_aviso, texto_aviso in avisos:
        bloco.append('<dt>%s</dt><dd>%s</dd>' % (html.escape(titulo_aviso), html.escape(texto_aviso)))
    bloco.append('</dl>')
    if not edicao:
        bloco.append('<p class="legal"><a href="./avisos_legais.html">Os mesmos avisos em 24 línguas</a></p>')
    bloco.append('</section>')
    partes += ['<footer class="rodape">', '<div class="k-acoes" id="k-acoes" aria-label="Preferências deste aparelho"></div>'] + bloco + [
               '<p class="id" id="id"></p>',
               '</footer>',
               '<script type="application/json" id="famDados">' + dados_json + '</script>',
               '<script src="./assets/nacl-fast.min.js"></script>',
               '<script defer src="./assets/konfirmu-2040.js"></script>',
               '<script>', JS_BASE, JS_PORTAIS.strip(), JS_VIVO.strip()]
    if not edicao:
        partes.append(JS_AVIAO)
    partes.append('</script>')
    # script à parte: se outro bloco falhar, as tigelas e as línguas continuam a funcionar
    partes += ['<script>', tigelas.JS_FAMILIA.strip(), '</script>']
    if edicao:
        partes.append("<script>if(window.isSecureContext && location.protocol!=='file:' && 'serviceWorker' in navigator){navigator.serviceWorker.register('./sw.js').catch(console.error)}</script>")
    partes += ['</body>', '</html>', '']
    return "\n".join(partes), total


def main():
    repo = sys.argv[1] if len(sys.argv) > 1 else os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    avisos = avisos_pt(repo)
    linguas = tigelas.ler_linguas(repo)
    pt = linguas["pt"]
    # uma só fonte para os textos do portal da família: locales/pt.json tem de bater com PORTAIS
    for chave, rotulo, titulo, sub, itens in PORTAIS:
        if chave == "fam":
            assert (rotulo, titulo, sub) == (pt["fam.rotulo"], pt["fam.titulo"], pt["fam.sub"]), "PORTAIS e locales/pt.json divergem"
            for href, _, nome, descricao, _ in itens:
                k = tigelas.CHAVES[href]
                assert (nome, descricao) == (pt["fam.%s.t" % k], pt["fam.%s.d" % k]), href
    dados_json = tigelas.dados_linguas(linguas)
    raiz, n_raiz = pagina("raiz", avisos, pt, dados_json)
    ed, n_ed = pagina("edicao21", avisos, pt, dados_json)
    assert n_raiz == 21 and n_ed == 21, (n_raiz, n_ed)
    for caminho, conteudo in (("app_unica.html", raiz), ("edicao-21/app_unica.html", ed), ("edicao-21/index.html", ed),
                              ("assets/ceu_vivo.js", TRABALHADOR_CEU)):
        with open(os.path.join(repo, caminho), "w", encoding="utf-8") as f:
            f.write(conteudo)
        print("%-26s %6d B" % (caminho, len(conteudo.encode("utf-8"))))
    print("atividades: raiz %d, edição 21 %d; avisos legais no rodapé: %d; línguas do portal da família: %d"
          % (n_raiz, n_ed, len(avisos), len(linguas)))


if __name__ == "__main__":
    main()
