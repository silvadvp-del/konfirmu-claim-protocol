// sw.js v8 — a app única: precache de TODAS as salas reais (regra 13: só ficheiros existentes)
// v4 (27-11-2026): a cache passa a levar também a página atual do chat de bolso (era a única das 21 que ficava de fora). Nome novo para chegar a quem já tinha a v3.
// v6: nome novo, para o botão e as páginas novas chegarem a quem já tinha a v5.
// v7 (27-11-2026): leva os 2 ficheiros da imersão, que vieram no pedido n.º 13 (sem eles, 6 páginas abriam incompletas sem rede).
//     O "./" passa a opcional (KON-608): há alojamentos que respondem 404 ao endereço da pasta, e o addAll falhado deixava 0 peças.
//     O botão conta só as peças obrigatórias. Nome novo, para chegar a quem já tinha a v6.
//     Leva também a página dos avisos legais (24 línguas), ligada a partir do início.
// v8 (27-11-2026): o início mudou (as 8 tigelas da Educação e família e as 62 línguas, diretiva das 12:29).
//     Nome novo, para o início novo chegar a quem já tinha a v7 (a cache serve primeiro o que tem guardado).
// v10 (27-11-2026): a Rádio com Prova lê a taxa real do aparelho e recusa tramas cortadas.
//     Nome novo, para a página nova chegar a quem já tinha a v9 (a cache serve primeiro o que tem guardado).
const CACHE_NAME = "konfirmu-app-unica-v10:" + self.registration.scope;
const OPCIONAIS = ["./"];
const ASSETS = ["./app_unica.html", "./girafinhas_criancas_facil.html", "./sala_natal_girafinhas.html", "./estudio_video_criancas.html", "./executor_criancas.html", "./radio_selo.html", "./carta_selada.html", "./manifest.json", "./assets/qrcode.js", "./assets/nacl-fast.min.js", "./assets/nacl-util.min.js", "./assets/imersao.css", "./assets/imersao.js", "./konfirmu_chat_offline_v0.1.html", "./konfirmu_chat_offline.html", "./verificador_offline.html", "./patient_vault_offline.html", "./ficha_campo.html", "./urna_voto_offline.html", "./testemunha_offline.html", "./chronolex_ata.html", "./chronolex_photo_seal.html", "./chronolex_verify.html", "./regua_do_planeta.html", "./neverland_family_quest.html", "./kcp_art_music_studio.html", "./webrtc_local.html", "./avisos_legais.html", "./terminal.html", "./assets/terminal_worker.js", "./assets/konfirmu-2040.js", "./assets/kcp_ed_estrito.js", "./economia_anti_casino.html"];
self.addEventListener("install", (event) => {
  event.waitUntil(caches.open(CACHE_NAME).then(async (cache) => {
    await cache.addAll(ASSETS);
    for (const a of OPCIONAIS) { try { await cache.add(a); } catch (e) { /* KON-608: a pasta pode dar 404; as páginas abrem pelo nome */ } }
  }));
  self.skipWaiting();
});
self.addEventListener("activate", (event) => {
  const meu = ":" + self.registration.scope;
  event.waitUntil(caches.keys().then((keys) => Promise.all(keys.filter((k) => k !== CACHE_NAME && (/^konfirmu-app-unica-v[1-4]$/.test(k) || (k.startsWith("konfirmu-app-unica-v") && k.endsWith(meu)))).map((k) => caches.delete(k)))));
});
self.addEventListener("fetch", (event) => {
  event.respondWith(caches.open(CACHE_NAME).then((cache) => cache.match(event.request)).then((r) => r || fetch(event.request)));
});
// v6 (27-11-2026, aprovado pelo David às 02:53): responde ao botão «Preparar modo avião» do início.
// Guarda o que faltar e diz quantas peças estão guardadas neste aparelho.
self.addEventListener("message", (event) => {
  if (!event.data || event.data.tipo !== "konfirmu-preparar" || !event.ports || !event.ports[0]) return;
  const porta = event.ports[0];
  event.waitUntil(caches.open(CACHE_NAME).then(async (cache) => {
    for (const a of ASSETS) if (!(await cache.match(a))) { try { await cache.add(a); } catch (e) {} }
    const faltam = [];
    for (const a of ASSETS) if (!(await cache.match(a))) faltam.push(a);
    porta.postMessage({ total: ASSETS.length, guardadas: ASSETS.length - faltam.length, faltam });
  }));
});
