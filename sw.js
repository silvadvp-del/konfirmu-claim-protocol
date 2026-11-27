// sw.js v5 — a app única: precache de TODAS as salas reais (regra 13: só ficheiros existentes)
// v4 (27-11-2026): a cache passa a levar também a página atual do chat de bolso (era a única das 21 que ficava de fora). Nome novo para chegar a quem já tinha a v3.
const CACHE_NAME = "konfirmu-app-unica-v5:" + self.registration.scope;
const ASSETS = ["./", "./app_unica.html", "./girafinhas_criancas_facil.html", "./sala_natal_girafinhas.html", "./estudio_video_criancas.html", "./executor_criancas.html", "./radio_selo.html", "./carta_selada.html", "./manifest.json", "./assets/qrcode.js", "./assets/nacl-fast.min.js", "./assets/nacl-util.min.js", "./konfirmu_chat_offline_v0.1.html", "./konfirmu_chat_offline.html", "./verificador_offline.html", "./patient_vault_offline.html", "./ficha_campo.html", "./urna_voto_offline.html", "./testemunha_offline.html", "./chronolex_ata.html", "./chronolex_photo_seal.html", "./chronolex_verify.html", "./regua_do_planeta.html", "./neverland_family_quest.html", "./kcp_art_music_studio.html", "./webrtc_local.html"];
self.addEventListener("install", (event) => {
  event.waitUntil(caches.open(CACHE_NAME).then((cache) => cache.addAll(ASSETS)));
  self.skipWaiting();
});
self.addEventListener("activate", (event) => {
  event.waitUntil(caches.keys().then((keys) => Promise.all(keys.filter(k => /^konfirmu-app-unica-v[1-4]$/.test(k)).map((k) => caches.delete(k)))));
});
self.addEventListener("fetch", (event) => {
  event.respondWith(caches.open(CACHE_NAME).then((cache) => cache.match(event.request)).then((r) => r || fetch(event.request)));
});
