// sw.js — Service Worker offline-first do verificador Konfirmu (corrigido: só ficheiros REAIS)
// Regra 13: nada de caminhos inventados. Ficheiros reais: verificador_offline.html + manifest.json.
const CACHE_NAME = "konfirmu-verificador-v1";
const ASSETS = ["./", "./verificador_offline.html", "./manifest.json"];

self.addEventListener("install", (event) => {
  event.waitUntil(caches.open(CACHE_NAME).then((cache) => cache.addAll(ASSETS)));
  self.skipWaiting();
});

self.addEventListener("activate", (event) => {
  event.waitUntil(
    caches.keys().then((keys) =>
      Promise.all(keys.filter((k) => k !== CACHE_NAME).map((k) => caches.delete(k)))
    )
  );
});

self.addEventListener("fetch", (event) => {
  event.respondWith(
    caches.match(event.request).then((cached) => cached || fetch(event.request))
  );
});

// O que NAO garante: offline dura enquanto o browser nao limpar o armazenamento.
// "Para sempre" e marketing; "verificavel offline" e facto.
