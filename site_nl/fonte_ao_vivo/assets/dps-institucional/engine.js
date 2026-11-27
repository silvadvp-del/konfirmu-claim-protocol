(()=>{
'use strict';
const d=window.DPSInstitutional, page=d.page, locs=d.languages, sel=document.getElementById('dps-lang');
const supported=x=>x&&Object.hasOwn(locs,x)?x:Object.keys(locs).find(k=>k.toLowerCase()===(x||'').toLowerCase());
const shortLanguage=x=>supported(x)||supported((x||'').split('-')[0]);
const url=new URL(location.href), prefix=location.pathname.split('/')[1];
let stored='';try{stored=localStorage.getItem('dps-language')||''}catch{}
const lang=supported(url.searchParams.get('lang'))||(['pt','nl'].includes(prefix)?prefix:null)||supported(stored)||(navigator.languages||[navigator.language]).map(shortLanguage).find(Boolean)||'en';
const row=d.strings[lang], t=i=>row[i], native=locs[lang];
document.documentElement.lang=native.lang;document.documentElement.dir=native.dir;
const text=(node,str)=>{if(node&&node.nodeType===3&&typeof str==='string')node.data=node.data.replace(/^(\s*)[\s\S]*?(\s*)$/,(_,a,b)=>a+str+b)};
for(const e of document.querySelectorAll('[data-dt]'))text(e.firstChild,t(e.dataset.dt));
for(const e of document.querySelectorAll('[data-dtail]'))text(e.nextSibling,t(e.dataset.dtail));
for(const e of document.querySelectorAll('[data-da]'))for(const [key,idx] of Object.entries(JSON.parse(e.dataset.da)))e.setAttribute(key,t(idx));
if(d.qualifications){for(const e of document.querySelectorAll('[data-qual]'))e.textContent=d.qualifications[lang][Number(e.dataset.qual)];}
sel.value=lang;sel.setAttribute('aria-label',t(d.langKey));sel.style.maxWidth='100%';
const knownRoutes=new Set(['','services','about','contact','privacy','konfirmu']);
const toRoute=(path,code,base=location.origin)=>{const u=new URL(base),pref=code==='pt'||code==='pt-BR'?'/pt':code==='nl'?'/nl':'';u.pathname=pref+'/'+path;u.searchParams.set('lang',code);return u};
const priceLang=code=>d.priceCodes.includes(code)?code:(code==='fil'?'tl':code==='de-li-hueckelhoven'?'de':'');
for(const a of document.querySelectorAll('a[href]')){
 let u;try{u=new URL(a.getAttribute('href'),location.href)}catch{continue}
 if(u.origin!==location.origin)continue;
 const orig=a.getAttribute('href');
 if(orig.startsWith('#'))continue;
 if(/^\/(pt\/|nl\/)?(services|about|contact|privacy|konfirmu)?\/?$/.test(u.pathname)){
   const parts=u.pathname.split('/').filter(Boolean);if(['pt','nl'].includes(parts[0]))parts.shift();
   if(!knownRoutes.has(parts.join('/')))continue;
   const dest=toRoute(parts.join('/'),lang,u.href);dest.hash=u.hash;a.href=dest.href;
 }else if(u.pathname==='/konfirmu/filme/'){u.searchParams.set('lang',lang);a.href=u.href;
 }else if(u.pathname==='/konfirmu/livro/girafa/'){
   u.searchParams.set('lang',lang);a.href=u.href;
 }else if(/^\/konfirmu\/precos\/l\/[^/]+\/$/.test(u.pathname)){
   const id=priceLang(lang);u.pathname=id?'/konfirmu/precos/l/'+id+'/':'/konfirmu/precos/';a.href=u.href;
 }
}
for(const a of document.querySelectorAll('a[href^="mailto:"][href*="subject"]')){const u=new URL(a.href);const s=a.textContent.replace('↗','').trim();if(s){u.searchParams.set('subject',s);a.href=u.href}}
sel.addEventListener('change',()=>{const chosen=supported(sel.value);if(!chosen)return;try{localStorage.setItem('dps-language',chosen)}catch{}const dest=toRoute(page,chosen,location.href);location.assign(dest.href)});
const hint=document.getElementById('dps-dialect');if(hint){hint.hidden=lang!=='de-li-hueckelhoven';hint.textContent=t(d.dialectKey);}
window.dispatchEvent(new Event('dps:language'));
const org=document.querySelector('script[type="application/ld+json"]');if(org){try{const j=JSON.parse(org.textContent);if(j['@type']==='WebPage'){j.name=document.title;j.inLanguage=native.lang;j.description=document.querySelector('meta[name=description]')?.content||j.description;org.textContent=JSON.stringify(j)}}catch{}}
if(page==='konfirmu'){
 const box=document.getElementById('prisma');if(!box||!d.prism)return;
 const dict=d.prism[lang];window.DPSPage={t:key=>dict[key]||''};
 for(const e of box.querySelectorAll('[data-t]'))e.textContent=dict[e.dataset.t]||'';
 for(const e of document.querySelectorAll('[data-kt]'))e.textContent=dict[e.dataset.kt]||'';
 for(const e of box.querySelectorAll('[data-aria]'))e.setAttribute('aria-label',dict[e.dataset.aria]||'');
 for(const e of box.querySelectorAll('[data-label]'))e.setAttribute('aria-label',dict[e.dataset.label]||'');
 if(typeof window.DPSStartPrism==='function')window.DPSStartPrism();
}
})();
