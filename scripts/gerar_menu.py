#!/usr/bin/env python3
"""Gera o menu de entrada da Konfirmu em 3 portais (pedido do David, 27-11, 04:59–05:00).

Escreve 3 ficheiros no repositório público:
  app_unica.html              menu da raiz (19 atividades + botão «Preparar modo avião»)
  edicao-21/app_unica.html    menu da edição integrada (21 atividades) — é o menu do pacote
  edicao-21/index.html        igual ao anterior

Regras da casa aplicadas: paleta «Pedra» (claro) e «Grafite» (escuro), «u» pêssego, sem verde,
sem mascote, sem emojis; o 112 não aparece no menu (regra de 31-10).
Ganchos que não se podem partir: a.card > .ico + b + .d (imersão 3D e teste do GitHub), um h1
(a imersão põe os botões a seguir), nenhum <summary> próprio, ids «aviao»/«aviaoEstado» e «id».

Protocolo de 27-11 (Definition of Done): o rodapé traz os 5 avisos legais, lidos da
avisos_legais.html (uma só fonte; sem ela, o gerador para), e há procura instantânea.
O menu da raiz liga também a página dos avisos em 24 línguas. O menu da edição 21 não a liga:
o empacotador junta tudo o que o menu liga e o teste do pacote só aceita atividades.

Uso: python3 -I scripts/gerar_menu.py [CAMINHO_DO_REPOSITORIO]   (por omissão, a pasta acima de scripts/)
Depois: refazer as 3 linhas destes ficheiros em SHA256SUMS.txt e correr os testes do pacote.
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

PORTAIS = [
    ("pro", "Profissional", "Profissional e indústria",
     "Confirmar ficheiros, registar o trabalho de campo e provar o que aconteceu.", [
         ("verificador_offline.html", "ficheiro", "Verificar ficheiro", "Confirma se um ficheiro ou um código é mesmo o original.", None),
         ("chronolex_photo_seal.html", "foto", "Foto com selo", "Tira uma fotografia e guarda-a com selo.", None),
         ("ficha_campo.html", "ficha", "Ficha de campo", "Regista água, energia e avarias, por ordem.", None),
         ("chronolex_ata.html", "ata", "Ata Chronolex", "Regista o que aconteceu, por ordem, com selo.", None),
         ("chronolex_verify.html", "verificar", "Verificar ata", "Confirma se uma ata ficou igual ao que foi selado.", None),
         ("testemunha_offline.html", "testemunha", "Testemunha", "Duas pessoas confirmam o mesmo momento.", None),
         ("radio_selo.html", "som", "Mensagem por som", "Envia mensagens por som que não se podem falsificar.", None),
         ("webrtc_local.html", "ligacao", "Ligação direta", "Liga dois aparelhos sem passar pela nuvem.", None),
     ]),
    ("cid", "Cidadão", "Cidadão e saúde",
     "Conversar, guardar a tua informação e tratar de cartas, no teu aparelho.", [
         ("konfirmu_chat_offline_v0.1.html", "chat", "Chat de bolso", "Responde com regras escritas. Quando não sabe, diz.", None),
         ("patient_vault_offline.html", "saude", "Cofre de saúde", "A tua história de saúde, guardada só neste aparelho.", EM_ENSAIO),
         ("carta_selada.html", "carta", "Carta com selo", "Escreve, põe o selo e imprime.", None),
         ("urna_voto_offline.html", "voto", "Votação sem rede", "Uma votação feita só nos aparelhos de quem vota.", EM_ENSAIO),
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

CSS = """
:root{color-scheme:dark;--pagina:#0B192C;--painel:rgb(15 34 61 / .72);--tinta:#F4F7FA;--tinta2:#9FB3C8;--tinta3:#9FB3C8;--linha:rgb(159 179 200 / .24);--azulejo:rgb(159 179 200 / .06);--u:#FF9E7D;
--letra:Inter,system-ui,-apple-system,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif}
*{box-sizing:border-box}
html{background:var(--pagina);-webkit-text-size-adjust:100%}
body{margin:0 auto;max-width:760px;padding:28px 20px 40px;font:16px/1.5 var(--letra);color:var(--tinta);background:var(--pagina)}
h1{margin:0;font-size:2rem;line-height:1.1;font-weight:650;letter-spacing:-.02em}
.acoes{display:flex;flex-wrap:wrap;align-items:center;gap:8px;margin:16px 0 0}
h1 .u{color:var(--u)}
.letra{flex:none;min-height:44px;padding:0 14px;border:1px solid var(--linha);border-radius:10px;background:var(--painel);color:var(--tinta);font:600 .9375rem/1 var(--letra);cursor:pointer}
.letra[aria-pressed="true"]{background:rgb(255 158 125 / .16);color:var(--tinta);border-color:var(--u)}
.intro{margin:12px 0 0;max-width:34em;color:var(--tinta2)}
.aviao{min-height:44px;padding:0 16px;border:1px solid var(--tinta);border-radius:10px;background:transparent;color:var(--tinta);font:600 .9375rem/1 var(--letra);cursor:pointer}
.aviao-estado{display:block;margin-top:8px;min-height:1.4em;font-size:.875rem;color:var(--tinta2)}
.portais{display:flex;gap:4px;margin:28px 0 0;padding:4px;border-radius:12px;background:var(--azulejo)}
.portais [role=tab]{flex:1 1 0;min-height:44px;padding:0 8px;border:0;border-radius:9px;background:transparent;color:var(--tinta2);font:600 .9375rem/1.2 var(--letra);cursor:pointer}
.portais [role=tab][aria-selected="true"]{background:var(--painel);color:var(--tinta);box-shadow:0 1px 2px rgb(11 25 44 / .4),inset 0 0 0 1px rgb(255 158 125 / .55)}
.portal{margin-top:24px}
.portal h2{margin:0;font-size:1.25rem;line-height:1.25;font-weight:650;letter-spacing:-.01em}
.portal .sub{margin:4px 0 14px;color:var(--tinta2);font-size:.9375rem}
.grid{display:block;border:1px solid var(--linha);border-radius:14px;background:var(--painel);overflow:hidden}
.card{display:grid;grid-template-columns:44px 1fr;grid-template-areas:"ico t" "ico d";column-gap:14px;align-items:center;min-height:68px;padding:12px 16px;color:var(--tinta);text-decoration:none;border-top:1px solid var(--linha)}
.card:first-child{border-top:0}
.card:hover{background:var(--azulejo)}
.card:active{background:var(--linha)}
.ico{grid-area:ico;display:flex;align-items:center;justify-content:center;width:44px;height:44px;border-radius:10px;background:var(--azulejo);color:var(--tinta)}
.ico svg{width:24px;height:24px;fill:none;stroke:currentColor;stroke-width:1.5;stroke-linecap:round;stroke-linejoin:round}
.card b{grid-area:t;align-self:end;font-size:1rem;line-height:1.3;font-weight:600}
.card .d{grid-area:d;align-self:start;font-size:.875rem;line-height:1.4;color:var(--tinta2)}
.card .estado{display:table;margin:6px 0 2px;padding:1px 7px;border:1px solid var(--linha);border-radius:6px;font-size:.75rem;line-height:1.4;color:var(--tinta3)}
.rodape{margin-top:32px;padding-top:16px;border-top:1px solid var(--linha);color:var(--tinta3);font-size:.8125rem}
.rodape p{margin:0 0 8px;max-width:46em}
.id{overflow-wrap:anywhere}
.rodape a{color:var(--tinta);text-decoration:underline;text-underline-offset:3px}
.id:empty{display:none}
:focus-visible{outline:2px solid var(--tinta);outline-offset:2px}
.card:focus-visible{outline-offset:-3px;border-radius:12px}
.portal[hidden],.card[hidden]{display:none}
.procura{margin:24px 0 0}
.procura label{display:block;margin:0 0 6px;font-size:.875rem;font-weight:600;color:var(--tinta2)}
.procura input{width:100%;min-height:44px;padding:0 14px;border:1px solid var(--linha);border-radius:10px;background:var(--painel);color:var(--tinta);font:400 1rem/1.2 var(--letra)}
.procura input::placeholder{color:var(--tinta3)}
.sem-resultados{margin:10px 0 0;min-height:1.4em;font-size:.875rem;color:var(--tinta2)}
.sem-resultados:empty{display:none}
.a-procurar .portais{display:none}
.avisos h2{margin:0 0 4px;font-size:.9375rem;line-height:1.3;font-weight:650;color:var(--tinta2)}
.avisos dl{margin:0 0 12px}
.avisos dt{margin:10px 0 0;font-weight:600;color:var(--tinta2)}
.avisos dd{margin:2px 0 0;max-width:46em}
@media (prefers-reduced-motion:no-preference){.js .portal{animation:surge .16s ease-out}@keyframes surge{from{opacity:0}to{opacity:1}}}
body.facil{font-size:19px}
body.facil .card b{font-size:1.1rem}
body.facil .card .d{font-size:1rem}
body.facil .portais [role=tab],body.facil .letra,body.facil .aviao{font-size:1.05rem}
/* imersão 3D: a mesma função, com a marca da casa (sem verde) */
body .acoes .im3d-tools{display:contents}
body .im3d-tools{margin:16px 0 0}
body .acoes .im3d-tools small{flex-basis:100%}
body .im3d-tools button{min-height:44px;padding:0 14px;border:1px solid var(--linha);border-radius:10px;background:var(--painel);color:var(--tinta);font:600 .9375rem/1 var(--letra)}
body .im3d-tools button[aria-pressed="true"]{background:var(--tinta);color:var(--pagina);border-color:var(--tinta)}
body .im3d-tools small{color:var(--tinta2)}
body .im3d-viewer{margin:12px 0 0;color:var(--tinta2);font-size:.9375rem}
:root.im3d-active{background:var(--pagina)}
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
  estado.textContent=total?(total===1?'1 atividade encontrada.':total+' atividades encontradas.'):'Nenhuma atividade tem «'+campo.value.trim()+'». Tenta outra palavra.';
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


def pagina(variante, avisos, pt, dados_json):
    edicao = variante == "edicao21"
    partes = ['<!DOCTYPE html>', '<html lang="pt">', '<head>', '<meta charset="UTF-8">',
              '<meta name="viewport" content="width=device-width, initial-scale=1.0">',
              '<meta name="theme-color" content="#0B192C">',
              '<title>Konfirmu</title>',
              # ícone dentro da página: o «u» pêssego; sem pedido ao servidor (sem favicon.ico 404)
              '<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns=\'http://www.w3.org/2000/svg\' viewBox=\'0 0 32 32\'%3E%3Crect width=\'32\' height=\'32\' rx=\'7\' fill=\'%231D1D21\'/%3E%3Ctext x=\'16\' y=\'22.5\' font-family=\'Inter,Arial,sans-serif\' font-size=\'21\' font-weight=\'700\' text-anchor=\'middle\' fill=\'%23D97D4A\'%3Eu%3C/text%3E%3C/svg%3E">',
              '<style>' + CSS.strip() + tigelas.CSS_FAMILIA.rstrip() + '</style>',
              '<link rel="stylesheet" href="./assets/imersao.css">',
              '<script defer src="./assets/imersao.js" data-viewer></script>']
    if edicao:
        partes.append('<link rel="manifest" href="./manifest.json">')
    partes += ['</head>', '<body>', tigelas.DEFS_PARTILHADAS,
               '<header>',
               '<h1>Konfirm<span class="u">u</span></h1>',
               '<p class="intro">Confirma e guarda com prova, no teu aparelho. Depois da primeira visita com internet, funciona também sem rede.</p>',
               '<div class="acoes"><button type="button" class="letra" onclick="facil()" aria-pressed="false">Letra maior</button>'
               + ('' if edicao else '<button id="aviao" class="aviao" type="button">Preparar modo avião</button>') + '</div>']
    if not edicao:
        partes.append('<span id="aviaoEstado" class="aviao-estado" role="status" aria-live="polite"></span>')
    partes.append('</header>')
    partes.append('<div class="procura" hidden><label for="procura">Procurar atividade</label>'
                  '<input id="procura" type="search" autocomplete="off" enterkeyhint="search" placeholder="Por exemplo: verificar, carta, família"></div>')
    partes.append('<p id="sem" class="sem-resultados" role="status" aria-live="polite"></p>')
    partes.append('<nav class="portais" role="tablist" aria-label="Portais">')
    for chave, rotulo, _, _, _ in PORTAIS:
        if chave == "fam":
            rotulo = '<bdi data-k="fam.rotulo">%s</bdi>' % html.escape(pt["fam.rotulo"])
        partes.append('<button type="button" role="tab" id="t-%s" aria-controls="p-%s" aria-selected="false">%s</button>' % (chave, chave, rotulo))
    partes.append('</nav>')
    total = 0
    for chave, _, titulo, sub, itens in PORTAIS:
        if chave == "fam":
            # o portal das tigelas: textos de locales/pt.json, desenho de scripts/tigelas.py
            hrefs = [i[0] for i in itens if edicao or i[0] not in SO_NA_EDICAO_21]
            secao, _ = tigelas.secao_familia(hrefs, pt, html.escape)
            partes.append(secao)
            total += len(hrefs)
            continue
        partes.append('<section class="portal" id="p-%s" role="tabpanel" aria-labelledby="t-%s">' % (chave, chave))
        partes.append('<h2>%s</h2><p class="sub">%s</p>' % (titulo, sub))
        partes.append('<div class="grid">')
        for href, icone, nome, descricao, estado in itens:
            if href in SO_NA_EDICAO_21 and not edicao:
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
    partes += ['<footer class="rodape">'] + bloco + [
               '<p class="id" id="id"></p>',
               '</footer>',
               '<script type="application/json" id="famDados">' + dados_json + '</script>',
               '<script src="./assets/nacl-fast.min.js"></script>',
               '<script>', JS_BASE, JS_PORTAIS.strip()]
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
    assert n_raiz == 19 and n_ed == 21, (n_raiz, n_ed)
    for caminho, conteudo in (("app_unica.html", raiz), ("edicao-21/app_unica.html", ed), ("edicao-21/index.html", ed)):
        with open(os.path.join(repo, caminho), "w", encoding="utf-8") as f:
            f.write(conteudo)
        print("%-26s %6d B" % (caminho, len(conteudo.encode("utf-8"))))
    print("atividades: raiz %d, edição 21 %d; avisos legais no rodapé: %d; línguas do portal da família: %d"
          % (n_raiz, n_ed, len(avisos), len(linguas)))


if __name__ == "__main__":
    main()
