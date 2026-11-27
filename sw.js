// sw.js v3 — a app única: precache de TODAS as salas reais (regra 13: só ficheiros existentes)
// v3 (27-11-2026, KON-572): muda o nome da cache para as 4 páginas de selo corrigidas chegarem a quem já as tinha guardadas.
const CACHE_NAME = "konfirmu-app-unica-v3";
const ASSETS = ["./", "./app_unica.html", "./girafinhas_criancas_facil.html", "./sala_natal_girafinhas.html", "./estudio_video_criancas.html", "./executor_criancas.html", "./radio_selo.html", "./carta_selada.html", "./manifest.json", "./assets/qrcode.js", "./assets/nacl-fast.min.js", "./konfirmu_chat_offline_v0.1.html", "./verificador_offline.html", "./patient_vault_offline.html", "./ficha_campo.html", "./urna_voto_offline.html", "./testemunha_offline.html", "./chronolex_ata.html", "./chronolex_photo_seal.html", "./chronolex_verify.html", "./regua_do_planeta.html", "./neverland_family_quest.html", "./kcp_art_music_studio.html", "./webrtc_local.html"];
self.addEventListener("install", (event) => {
  event.waitUntil(caches.open(CACHE_NAME).then((cache) => cache.addAll(ASSETS)));
  self.skipWaiting();
});
self.addEventListener("activate", (event) => {
  event.waitUntil(caches.keys().then((keys) => Promise.all(keys.filter((k) => k !== CACHE_NAME).map((k) => caches.delete(k)))));
});
self.addEventListener("fetch", (event) => {
  event.respondWith(caches.match(event.request).then((r) => r || fetch(event.request)));
});
