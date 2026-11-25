"""Provas do konfirmu_chat_offline.html. Correr:  python3 tests/test_konfirmu_chat_offline.py
Precisa de: playwright (python) e Chrome. Sai com código 0 só se tudo passar."""
import asyncio, json, hashlib, os, sys, subprocess, time
from playwright.async_api import async_playwright
RAIZ=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CHROME=os.environ.get('CHROME','/usr/bin/google-chrome')
JS=r'''async()=>{const K=KONFIRMU;await K.pronto;K.definirLingua('pt');const o={};
 const c=[['nitrato 40 mg/L','OK'],['nitrato 48 ± 3 mg/L','NS'],['nitrato 55 ± 2 mg/L','VETO'],['nitrato 50 mg/L','OK'],['nitrato 50,000001 mg/L','VETO'],
  ['vacina a 5 °C','OK'],['vacina a 9,5 °C','VETO'],['vacina a 7,8 ± 0,5 °C','NS'],['vacina a 1,9 °C','VETO'],['vacina a 2 °C','OK'],['cadeia de frio 2 a 8 °C: medi 6 °C','OK']];
 o.portao=c.every(([q,e])=>{const g=K.portao(q);return g&&g.ver===e});
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
 return o}'''
async def main():
    falhas=[]
    def ver(nome,cond):
        print(('PASSA ' if cond else 'FALHA ')+nome)
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
            await pg.click('#cIA'); await pg.wait_for_timeout(200)
            ver('em ficheiro, a IA diz que precisa de https',"https" in await pg.evaluate("document.querySelector('#conversa').lastChild.textContent"))
            ver('em ficheiro, zero pedidos à rede',all(u.startswith('file:') or u.startswith('blob:') for u in pedidos))
            await pg.reload(); n=await pg.evaluate("(async()=>{await KONFIRMU.pronto;return KONFIRMU.pacote().n})()")
            p2=await pg.evaluate("KONFIRMU.pacote().ponta"); ver('conversa volta depois de fechar e abrir (3 registos, mesma ponta)',n==3 and p2==o['ponta'])
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
    print(f"\n{20-len(falhas)} de 20 passam"); sys.exit(1 if falhas else 0)
asyncio.run(main())
