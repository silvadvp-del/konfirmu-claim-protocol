// Konfirmu · chat de bolso · guarda a página para abrir sem rede (só na versão com link https)
const C='konfirmu-chat-v0.2',P='konfirmu_chat_offline.html';
self.addEventListener('install',e=>{e.waitUntil(caches.open(C).then(c=>c.add(P)));self.skipWaiting()});
self.addEventListener('activate',e=>e.waitUntil(self.clients.claim()));
self.addEventListener('fetch',e=>{const u=new URL(e.request.url);
 if(e.request.method!=='GET'||u.origin!==location.origin||!u.pathname.endsWith(P))return;
 e.respondWith(fetch(e.request).then(r=>{const k=r.clone();caches.open(C).then(c=>c.put(P,k));return r}).catch(()=>caches.match(P)))});
