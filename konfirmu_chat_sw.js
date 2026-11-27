// Konfirmu · chat de bolso · guarda a página para abrir sem rede (só na versão com link https)
const C='konfirmu-chat-v0.2',P='konfirmu_chat_offline.html';
self.addEventListener('install',e=>{e.waitUntil(caches.open(C).then(c=>c.add(P)));self.skipWaiting()});
self.addEventListener('activate',e=>e.waitUntil(self.clients.claim()));
self.addEventListener('fetch',e=>{const u=new URL(e.request.url);
 if(e.request.method!=='GET'||u.origin!==location.origin)return;
 // 27-11-2026: ao lado da app única, este guarda tapava a cache da app. O que não é o chat responde-se da cache, se lá estiver.
 if(!u.pathname.endsWith(P)){e.respondWith(caches.match(e.request).then(r=>r||fetch(e.request)));return}
 e.respondWith(fetch(e.request).then(r=>{const k=r.clone();caches.open(C).then(c=>c.put(P,k));return r}).catch(()=>caches.match(P)))});
