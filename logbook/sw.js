const CACHE='logbook-shell-v2';
const ASSETS=['./','./index.html','./manifest.webmanifest','./icons/mark.svg','./feeds.json'];
self.addEventListener('install',e=>e.waitUntil(caches.open(CACHE).then(c=>c.addAll(ASSETS)).then(()=>self.skipWaiting())));
self.addEventListener('activate',e=>e.waitUntil(caches.keys().then(keys=>Promise.all(keys.filter(k=>k.startsWith('logbook-shell-')&&k!==CACHE).map(k=>caches.delete(k)))).then(()=>self.clients.claim())));
self.addEventListener('fetch',e=>{
 const q=e.request;
 if(q.method!=='GET'||new URL(q.url).origin!==self.location.origin)return;
 e.respondWith(fetch(q).then(r=>{if(r.ok){const c=r.clone();caches.open(CACHE).then(cache=>cache.put(q,c)).catch(()=>{})}return r}).catch(async()=>{
  const hit=await caches.match(q);if(hit)return hit;
  if(q.mode==='navigate')return caches.match('./index.html');
  return Response.error()
 }))
});
