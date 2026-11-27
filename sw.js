// sw.js v6 — a app única: precache de TODAS as salas reais (regra 13: só ficheiros existentes)
// v4 (27-11-2026): a cache passa a levar também a página atual do chat de bolso (era a única das 21 que ficava de fora). Nome novo para chegar a quem já tinha a v3.
// v6: nome novo, para o botão e as páginas novas chegarem a quem já tinha a v5.
// v6.1 (27-11-2026): leva também assets/imersao.css e assets/imersao.js (6 páginas ficavam sem eles sem rede) e o endereço da pasta ("./") passa a opcional: num alojamento que responde 404 à pasta, ficavam 0 peças guardadas.
const CACHE_NAME = "konfirmu-app-unica-v6:" + self.registration.scope;
const ASSETS = ["./app_unica.html", "./girafinhas_criancas_facil.html", "./sala_natal_girafinhas.html", "./estudio_video_criancas.html", "./executor_criancas.html", "./radio_selo.html", "./carta_selada.html", "./manifest.json", "./assets/qrcode.js", "./assets/nacl-fast.min.js", "./assets/nacl-util.min.js", "./assets/imersao.css", "./assets/imersao.js", "./konfirmu_chat_offline_v0.1.html", "./konfirmu_chat_offline.html", "./verificador_offline.html", "./patient_vault_offline.html", "./ficha_campo.html", "./urna_voto_offline.html", "./testemunha_offline.html", "./chronolex_ata.html", "./chronolex_photo_seal.html", "./chronolex_verify.html", "./regua_do_planeta.html", "./neverland_family_quest.html", "./kcp_art_music_studio.html", "./webrtc_local.html"];
self.addEventListener("install", (event) => {
  event.waitUntil(caches.open(CACHE_NAME).then((cache) => cache.addAll(ASSETS).then(() => cache.add("./").catch(() => null))));
  self.skipWaiting();
});
self.addEventListener("activate", (event) => {
  event.waitUntil(caches.keys().then((keys) => Promise.all(keys.filter(k => /^konfirmu-app-unica-v[1-4]$/.test(k) || k === "konfirmu-app-unica-v5:" + self.registration.scope).map((k) => caches.delete(k)))));
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
