// sw.js v3 — a app única, um só service worker para a casa toda (27-11-2026).
// v3: junta assets/nacl-util.min.js (sem ele o selador de fotos e as atas rebentavam sem rede),
//     assets/konfirmu_sha256.js (KON-572) e o chat v0.2; páginas: rede primeiro, cache se não houver rede.
const CACHE_NAME = "konfirmu-app-unica-v3";
const ASSETS = ["./", "./app_unica.html", "./girafinhas_criancas_facil.html", "./sala_natal_girafinhas.html", "./estudio_video_criancas.html", "./executor_criancas.html", "./radio_selo.html", "./carta_selada.html", "./manifest.json", "./assets/qrcode.js", "./assets/nacl-fast.min.js", "./assets/nacl-util.min.js", "./assets/konfirmu_sha256.js", "./konfirmu_chat_offline.html", "./konfirmu_chat_offline_v0.1.html", "./verificador_offline.html", "./patient_vault_offline.html", "./ficha_campo.html", "./urna_voto_offline.html", "./testemunha_offline.html", "./chronolex_ata.html", "./chronolex_photo_seal.html", "./chronolex_verify.html", "./regua_do_planeta.html", "./neverland_family_quest.html", "./kcp_art_music_studio.html", "./webrtc_local.html"];
self.addEventListener("install", (event) => {
  event.waitUntil(caches.open(CACHE_NAME).then((cache) => cache.addAll(ASSETS)));
  self.skipWaiting();
});
self.addEventListener("activate", (event) => {
  event.waitUntil(caches.keys()
    .then((keys) => Promise.all(keys.filter((k) => k !== CACHE_NAME).map((k) => caches.delete(k))))
    .then(() => self.clients.claim()));
});
self.addEventListener("fetch", (event) => {
  const req = event.request;
  if (req.method !== "GET" || new URL(req.url).origin !== self.location.origin) return;
  if (req.mode === "navigate") { // página: rede primeiro (recebe correções), cache se não houver rede
    event.respondWith(fetch(req).then((r) => {
      if (r && r.ok) { const copia = r.clone(); caches.open(CACHE_NAME).then((c) => c.put(req, copia)); }
      return r;
    }).catch(() => caches.match(req, { ignoreSearch: true }).then((r) => r || caches.match("./app_unica.html"))));
    return;
  }
  event.respondWith(caches.match(req).then((r) => r || fetch(req)));
});
