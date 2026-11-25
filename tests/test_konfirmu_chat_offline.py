"""Provas do konfirmu_chat_offline.html. Correr:  python3 tests/test_konfirmu_chat_offline.py
Precisa de: playwright (python) e Chrome. Sai com código 0 só se tudo passar."""
import asyncio, json, hashlib, os, sys, subprocess, time
from playwright.async_api import async_playwright
RAIZ=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CHROME=os.environ.get('CHROME','/usr/bin/google-chrome')
import glob
VET=[]; FICH={}
for f in sorted(glob.glob(RAIZ+'/cartridges/*.json')):
    b=open(f,'rb').read(); d=json.loads(b)
    if 'pediatric' in f: continue
    FICH[os.path.basename(f)]=hashlib.sha256(b).hexdigest()
    for tv in d['test_vectors']: VET.append([d['cartridge_id'],tv['env'],tv['expected_verdict']])
JS=r'''async()=>{const VETORES=__VET__;const K=KONFIRMU;await K.pronto;K.definirLingua('pt');const o={};
 const casos=[['nitrato 40 mg/L','OK'],['nitrato 48 ± 3 mg/L','NS'],['nitrato 55 ± 2 mg/L','VETO'],['nitrato 50 mg/L','OK'],['nitrato 50,000001 mg/L','VETO'],
  ['vacina a 5 °C','OK'],['vacina a 9,5 °C','VETO'],['vacina a 7,8 ± 0,5 °C','NS'],['vacina a 1,9 °C','VETO'],['vacina a 2 °C','OK'],['cadeia de frio 2 a 8 °C: medi 6 °C','OK']];
 o.portao=casos.every(([q,e])=>{const g=K.portao(q);return g&&g.ver===e});
 o.dose_sem_veredicto=K.portao('qual a dose de paracetamol para 12 kg')===null;
 const big='ç€😀'.repeat(5000);o.sha=[await K.sha256('abc'),await K.sha256('abc',true),await K.sha256(big),await K.sha256(big,true)];
 for(const q of ['nitrato 48 ± 3 mg/L','vacina a 9,5 °C','olá, que horas são?'])await K.responder(q);
 const pk=JSON.parse(JSON.stringify(K.pacote()));o.cadeia_ok=(await K.conferirCadeia(pk)).ok;o.ponta=pk.ponta;
 pk.registos[1].a='mexido';o.mexido=(await K.conferirCadeia(pk)).em;o.lixo=(await K.conferirCadeia({a:1})).erro===true;
 o.selo=[(await K.selo('texto  \nfim\n','texto\nfim')).ver,(await K.selo('a','b')).ver,(await K.selo('a','')).ver];
 // som: ida e volta em contas, com ruído e com outro ritmo de amostragem
 const ruido=(s,amp,seed)=>{let x=seed;const r=new Float32Array(s.length+20000);for(let i=0;i<r.length;i++){x=(x*1664525+1013904223)>>>0;r[i]=(x/4294967296-.5)*2*amp}for(let i=0;i<s.length;i++)r[i+9137]+=s[i];return r};
 const msgs=['K1|3|NS|'+pk.ponta.slice(0,32),'nitrato 48 ± 3 mg/L — poço da escola','água: ainda não sei 😀'];o.som=[];
 for(const m of msgs)for(const sr of [44100,48000])for(const amp of [0,.3,.6]){const w=K.somOnda(K.somBits(m),sr);o.som.push(K.somLer(ruido(w,amp,sr+amp*10),sr)===m)}
 const w=K.somOnda(K.somBits(msgs[0]),44100),est=ruido(w,.1,7);for(let i=30000;i<34000;i++)est[i]=0;o.som_cortado=K.somLer(est,44100);
 o.som_so_ruido=K.somLer(ruido(new Float32Array(1),.6,3),44100);o.som_grande=K.somBits('x'.repeat(121));o.crc=K.crc16(new TextEncoder().encode('123456789')).toString(16);
 // folhas da casa
 o.folhas=K.FOLHAS.map(f=>[f.ficheiro,f.sha256]);
 o.vetores=VETORES.map(([id,env,esp])=>{const g=K.avaliar(K.FOLHAS.find(f=>f.cartridge_id===id),env);return [id,esp,g.ver]});
 let lancou=0;for(const fx of ['alert(1)','a.b','x=>x','nitrato_mgl;1','constructor','1e9','2**3','(1']){try{K.intervalo(fx,{nitrato_mgl:[1,0]})}catch(_){lancou++}}o.formula_ma=lancou;
 o.intervalos=[K.intervalo('a - b',{a:[10,1],b:[4,1]}),K.intervalo('a / b',{a:[8,0],b:[2,0]}),K.intervalo('-a / (b + c)',{a:[4,0],b:[1,0],c:[1,0]})];
 try{K.intervalo('a / b',{a:[1,0],b:[0,1]});o.div_zero=false}catch(_){o.div_zero=true}
 // prazo de validade e assinatura
 o.validade=[K.portao('nitrato 40 mg/L',new Date('2027-11-25T12:00:00Z')).ver,K.portao('nitrato 40 mg/L',new Date('2027-11-26T12:00:00Z')).ver,K.portao('nitrato 40 mg/L',new Date('2027-11-26T12:00:00Z')).velha];
 const pa=JSON.parse(JSON.stringify(await K.pacoteAssinado()));const ra=await K.conferirCadeia(pa);o.dedo=(await K.minhaChave()).dedo;o.assin_ok=ra.ok&&ra.dedo===o.dedo&&/^[0-9a-f]{16}$/.test(o.dedo);
 const pm=JSON.parse(JSON.stringify(pa));const sb=atob(pm.assinatura.sig).split('');sb[5]=String.fromCharCode(sb[5].charCodeAt(0)^1);pm.assinatura.sig=btoa(sb.join(''));const rm=await K.conferirCadeia(pm);o.assin_ma=rm.ok===false&&rm.assinMa===true;
 const pt2=JSON.parse(JSON.stringify(pa));pt2.registos.pop();pt2.n=2;pt2.ponta=pt2.registos[1].hash;const rt=await K.conferirCadeia(pt2);o.assin_cortada=rt.ok===false&&rt.assinMa===true;
 // foto leve
 const cv=document.createElement('canvas');cv.width=1200;cv.height=900;const g=cv.getContext('2d');const gr=g.createLinearGradient(0,0,1200,900);gr.addColorStop(0,'#234');gr.addColorStop(1,'#fb9');g.fillStyle=gr;g.fillRect(0,0,1200,900);
 let x=5;for(let i=0;i<400;i++){x=(x*1664525+1013904223)>>>0;g.fillStyle='hsl('+(x%360)+',60%,'+(30+x%40)+'%)';g.beginPath();g.arc(x%1200,(x>>>8)%900,10+(x>>>16)%60,0,7);g.fill()}
 g.fillStyle='#000';g.font='bold 120px sans-serif';g.fillText('MSKU 123456-7',80,480);
 const png=await new Promise(r=>cv.toBlob(r,'image/png'));const c=await K.fotoComprimir(png),k=await K.fotoPacotes(c.bytes,c.tipo);
 o.foto={png:png.size,bytes:k.bytes,tipo:c.tipo,larg:c.larg,alt:c.alt,n:k.n,reserva:k.reserva,maior:Math.max(...k.pacotes.map(p=>p.length))};
 const igual=(a,b)=>a.length===b.length&&a.every((v,i)=>v===b[i]);const P=k.pacotes;
 let r=await K.fotoJuntar(P);o.f_tudo=r.ver==='OK'&&igual(r.bytes,c.bytes)&&r.sha===k.sha;
 r=await K.fotoJuntar(P.slice().reverse());o.f_baralhado=r.ver==='OK'&&igual(r.bytes,c.bytes);
 const dados=P.filter(p=>p.split('|')[2]==='D');const um=new Set(dados.filter((_,i)=>i%4===1).map(p=>p));
 r=await K.fotoJuntar(P.filter(p=>!um.has(p)));o.f_perde1=[r.ver,r.recuperados,um.size,r.ver==='OK'&&igual(r.bytes,c.bytes)];
 r=await K.fotoJuntar(P.filter(p=>p!==dados[0]&&p!==dados[1]));o.f_perde2=[r.ver,r.faltam];
 const q=dados[2].split('|');const u=atob(q[4]).split('');u[10]=String.fromCharCode(u[10].charCodeAt(0)^1);q[4]=btoa(u.join(''));
 r=await K.fotoJuntar(P.map(p=>p===dados[2]?q.join('|'):p));o.f_mexido=r.ver;
 r=await K.fotoJuntar(P);o.f_assinada=r.ver==='OK'&&r.dedo===o.dedo;
 r=await K.fotoJuntar(P.filter(p=>p.split('|')[2]!=='S'));o.f_sem_assin=r.ver==='OK'&&r.dedo===null;
 const cv2=document.createElement('canvas');cv2.width=300;cv2.height=200;cv2.getContext('2d').fillRect(20,20,200,100);const outra=await K.fotoComprimir(await new Promise(r=>cv2.toBlob(r,'image/png')));
 const k2=await K.fotoPacotes(outra.bytes,outra.tipo),Sa=P.find(p=>p.split('|')[2]==='S').split('|');Sa[1]=k2.id;
 r=await K.fotoJuntar(k2.pacotes.filter(p=>p.split('|')[2]!=='S').concat([Sa.join('|')]));o.f_troca=r.ver==='VETO'&&r.assinMa===true;
 r=await K.fotoJuntar(P.slice(1));o.f_sem_cabecalho=r.ver;r=await K.fotoJuntar(['olá','KI1|x']);o.f_lixo=r.ver;
 return o}'''
async def main():
    falhas=[]; total=[0]
    def ver(nome,cond):
        total[0]+=1; print(('PASSA ' if cond else 'FALHA ')+nome)
        if not cond: falhas.append(nome)
    srv=subprocess.Popen([sys.executable,'-m','http.server','8765','--bind','127.0.0.1'],cwd=RAIZ,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL); time.sleep(1)
    try:
        async with async_playwright() as p:
            b=await p.chromium.launch(executable_path=CHROME,args=['--no-sandbox','--use-fake-ui-for-media-stream','--use-fake-device-for-media-stream'])
            ctx=await b.new_context(); pg=await ctx.new_page(); erros=[]; pedidos=[]
            pg.on('pageerror',lambda e:erros.append(str(e))); pg.on('request',lambda r:pedidos.append(r.url))
            await pg.goto('file://'+RAIZ+'/konfirmu_chat_offline.html'); o=await pg.evaluate(JS)
            ver('portão: 11 medidas com o veredicto certo',o['portao'])
            ver('dose: sem veredicto',o['dose_sem_veredicto'])
            big=('ç€😀'*5000).encode(); ref=[hashlib.sha256(b'abc').hexdigest()]*2+[hashlib.sha256(big).hexdigest()]*2
            ver('SHA-256 igual ao do Python (WebCrypto e JS puro)',o['sha']==ref)
            ver('cadeia inteira confere',o['cadeia_ok']); ver('registo mexido é apontado (n.º 2)',o['mexido']==2); ver('ficheiro estranho é recusado',o['lixo'])
            ver('selo: igual / diferente / não sei',o['selo']==['OK','VETO','NS'])
            ver('som: 18 idas e voltas (3 textos, 2 ritmos, 3 níveis de ruído)',len(o['som'])==18 and all(o['som']))
            ver('som cortado a meio não inventa mensagem',o['som_cortado'] is None); ver('só ruído não inventa mensagem',o['som_so_ruido'] is None)
            ver('texto com mais de 120 bytes é recusado',o['som_grande'] is None); ver('CRC-16 de «123456789» = 29b1',o['crc']=='29b1')
            ver('folhas: as %d da casa estão na página, com o sha256 do ficheiro de origem'%len(FICH),dict(o['folhas'])==FICH)
            ver('folhas: os %d vetores de teste da casa dão o mesmo lado (OK=OK; VETO=não confere ou ainda não sei)'%len(VET),all((e=='OK' and g=='OK') or (e=='VETO' and g in('VETO','NS')) for _,e,g in o['vetores']))
            print('   vetores:',[(i.split('_V1')[0][:18],e,g) for i,e,g in o['vetores']])
            ver('folhas: a de dose pediátrica não está na página','paracetamol' not in open(RAIZ+'/konfirmu_chat_offline.html',encoding='utf-8').read().lower())
            ver('conta: 8 fórmulas estranhas são recusadas (sem eval)',o['formula_ma']==8)
            ver('conta com margens: a-b, a/b, -a/(b+c) certos; divisão por zero recusada',o['intervalos']==[[4,8],[4,4],[-2,-2]] and o['div_zero'])
            ver('regra dentro do prazo responde; fora do prazo diz «ainda não sei»',o['validade']==['OK','NS',True])
            ver('conversa exportada sai assinada e a assinatura confere',o['assin_ok']); ver('assinatura com 1 bit mexido é recusada',o['assin_ma'])
            ver('conversa cortada no fim, com a assinatura antiga, é recusada',o['assin_cortada'])
            ver('foto: assinada pela chave do aparelho',o['f_assinada']); ver('foto: sem a linha de assinatura, diz que não sabe quem enviou',o['f_sem_assin'])
            ver('foto: imagem trocada com a assinatura de outra é recusada',o['f_troca'])
            f=o['foto']; print('   foto:',json.dumps(f))
            ver('foto: 1200×900 fica abaixo de 6 000 bytes e cada pacote abaixo de 240 letras',f['bytes']<6000 and f['maior']<240)
            ver('foto: todos os pacotes juntos dão a imagem exata',o['f_tudo']); ver('foto: pacotes fora de ordem dão a imagem exata',o['f_baralhado'])
            ver('foto: 1 pacote perdido em cada grupo de 4 é recuperado',o['f_perde1'][0]=='OK' and o['f_perde1'][1]==o['f_perde1'][2] and o['f_perde1'][3])
            ver('foto: 2 perdidos no mesmo grupo dá «ainda não sei, faltam 2»',o['f_perde2']==['NS',2])
            ver('foto: 1 bit mexido dá «não confere»',o['f_mexido']=='VETO'); ver('foto: sem cabeçalho ou com lixo não inventa imagem',o['f_sem_cabecalho']=='NS' and o['f_lixo']=='NS')
            await pg.click('#cIA'); await pg.wait_for_timeout(200)
            ver('em ficheiro, a IA diz que precisa de https',"https" in await pg.evaluate("document.querySelector('#conversa').lastChild.textContent"))
            ver('em ficheiro, zero pedidos à rede',all(u.startswith('file:') or u.startswith('blob:') for u in pedidos))
            await pg.reload(); n=await pg.evaluate("(async()=>{await KONFIRMU.pronto;return KONFIRMU.pacote().n})()")
            p2=await pg.evaluate("KONFIRMU.pacote().ponta"); ver('conversa volta depois de fechar e abrir (3 registos, mesma ponta)',n==3 and p2==o['ponta'])
            ver('a chave do aparelho é a mesma depois de fechar e abrir',await pg.evaluate("(async()=>(await KONFIRMU.minhaChave()).dedo)()")==o['dedo'])
            await pg.click('#cApg'); await pg.click('#cApg'); await pg.wait_for_timeout(200); await pg.reload()
            ver('apagar apaga mesmo',await pg.evaluate("(async()=>{await KONFIRMU.pronto;return KONFIRMU.pacote().n})()")==0)
            html=open(RAIZ+'/konfirmu_chat_offline.html',encoding='utf-8').read().lower()
            ver('sem verde no ficheiro',not any(x in html for x in ['green','verde','#10b981','#0f0','#00ff00']))
            ver('zero erros de página (ficheiro)',erros==[])
            # versão com link: página guardada abre sem rede
            pg2=await ctx.new_page(); await pg2.goto('http://localhost:8765/konfirmu_chat_offline.html')
            await pg2.evaluate("navigator.serviceWorker.ready.then(()=>1)"); await pg2.wait_for_timeout(800)
            srv.terminate(); srv.wait(); 
            try:
                await pg2.reload(); ok=await pg2.evaluate("(async()=>{await KONFIRMU.pronto;return KONFIRMU.portao('nitrato 40 mg/L').ver})()")=='OK'
            except Exception as e: ok=False
            ver('com link: depois da 1.ª visita, abre com o servidor desligado',ok)
            await pg2.set_viewport_size({'width':390,'height':780}); await pg2.screenshot(path='/tmp/chat2.png'); await b.close()
    finally:
        if srv.poll() is None: srv.terminate()
    print(f"\n{total[0]-len(falhas)} de {total[0]} passam"); sys.exit(1 if falhas else 0)
JS=JS.replace('__VET__',json.dumps(VET))
asyncio.run(main())
