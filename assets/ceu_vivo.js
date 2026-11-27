// assets/ceu_vivo.js — gerado por scripts/gerar_menu.py. Não editar à mão.
// O céu vivo do menu desenhado fora da linha principal da página (OffscreenCanvas): a página não repinta a cada quadro.
'use strict';
// O céu do menu: aurora e partículas quentes em WebGL (Canvas 2D só sem WebGL). Uma só fonte para os dois sítios onde corre:
// no trabalhador (assets/ceu_vivo.js, fora da linha principal da página) e, se não houver trabalhador, na própria página.
function criarCeu(A,P,novaTela,semGL,DPR){
 var dpr=Math.min(DPR||1,1)*.75,W=0,H=0,rolar=0,t0=performance.now();
 var incl={x:0,y:0},alvo={x:0,y:0},toque=null,ondas=[],ps=[];
 var gl=null,uT,uR,uL,uS;
 try{gl=A.getContext('webgl',{alpha:false,antialias:false,depth:false,stencil:false,powerPreference:'low-power'})}catch(_){}
 if(gl){
  var VS='attribute vec2 p;void main(){gl_Position=vec4(p,0.,1.);}';
  var FS=['precision mediump float;uniform float t;uniform vec2 r;uniform vec2 l;uniform float s;',
   'float h(vec2 p){return fract(sin(dot(p,vec2(127.1,311.7)))*43758.5453);}',
   'float n(vec2 p){vec2 i=floor(p),f=fract(p);f=f*f*(3.-2.*f);return mix(mix(h(i),h(i+vec2(1.,0.)),f.x),mix(h(i+vec2(0.,1.)),h(i+vec2(1.,1.)),f.x),f.y);}',
   'float fbm(vec2 p){float v=0.,a=.5;for(int k=0;k<5;k++){v+=a*n(p);p=p*2.03+vec2(1.7,9.2);a*=.5;}return v;}',
   'void main(){vec2 uv=gl_FragCoord.xy/r;vec2 q=uv;q.x*=r.x/r.y;q+=l*.08;float z=t*.03;',
   'float a=fbm(vec2(q.x*1.3+z,q.y*.8-z*.7));float b=fbm(vec2(q.x*2.1-z*.9,q.y*1.2+z*.5)+a*1.4);',
   'float c1=.66+.16*(a-.5)+.05*sin(q.x*2.3+z*4.);float b1=smoothstep(.22,0.,abs(uv.y-c1))*(.55+.6*b);',
   'float c2=.82+.12*(b-.5);float b2=smoothstep(.16,0.,abs(uv.y-c2))*(.4+.5*a);',
   'float g=clamp(b1+.7*b2+.18*fbm(q*2.6-z),0.,1.);',
   'float topo=mix(.5,1.,smoothstep(.5,.75,uv.y));float k=g*mix(topo,.5,s);',
   'vec3 fundo=vec3(.043,.098,.172);vec3 brasa=mix(vec3(.36,.22,.17),vec3(.35,.23,.16),b);',
   'vec3 cor=mix(fundo,brasa,k);float v=1.-.35*pow(length((uv-vec2(.5,.62))*vec2(1.,1.3)),1.6);',
   'gl_FragColor=vec4(cor*clamp(v,.6,1.),1.);}'].join('\n');
  var sh=function(tipo,src){var o=gl.createShader(tipo);gl.shaderSource(o,src);gl.compileShader(o);return gl.getShaderParameter(o,gl.COMPILE_STATUS)?o:null};
  var vs=sh(gl.VERTEX_SHADER,VS),fs=sh(gl.FRAGMENT_SHADER,FS),pr=gl.createProgram();
  if(vs&&fs){gl.attachShader(pr,vs);gl.attachShader(pr,fs);gl.linkProgram(pr)}
  if(!vs||!fs||!gl.getProgramParameter(pr,gl.LINK_STATUS)){gl=null}else{
   gl.useProgram(pr);gl.bindBuffer(gl.ARRAY_BUFFER,gl.createBuffer());
   gl.bufferData(gl.ARRAY_BUFFER,new Float32Array([-1,-1,1,-1,-1,1,1,1]),gl.STATIC_DRAW);
   var lp=gl.getAttribLocation(pr,'p');gl.enableVertexAttribArray(lp);gl.vertexAttribPointer(lp,2,gl.FLOAT,false,0,0);
   uT=gl.getUniformLocation(pr,'t');uR=gl.getUniformLocation(pr,'r');uL=gl.getUniformLocation(pr,'l');uS=gl.getUniformLocation(pr,'s');
  }
 }
 function perdeuGL(){if(gl!==false){gl=null;semGL()}}
 if(!gl)perdeuGL();
 if(A.addEventListener)A.addEventListener('webglcontextlost',function(e){e.preventDefault();perdeuGL()});
 // As faíscas desenham-se em WebGL: pontos com o mesmo degradê pêssego da imagem de antes. Em Canvas 2D, a 60 quadros
 // por segundo, a memória subia sem parar com a página parada (medido no computador: de 37 para 61 MB em 75 s).
 // Sem WebGL, ficam em Canvas 2D, com a faísca guardada como imagem fixa (ImageBitmap).
 var pg=null,pP=null,pA=null,pB=null,pQ=null,pD=null,pR,pAr,pAc,pAk,cx=null,fa=null;
 // ponto: x, y, tamanho e brilho (em píxeis da tela); o degradê vai de 1 no centro a .5 aos 30 % e a 0 na borda
 var FV='attribute vec4 a;uniform vec2 r;varying float al;void main(){gl_Position=vec4(a.x/r.x*2.-1.,1.-a.y/r.y*2.,0.,1.);gl_PointSize=a.z;al=a.w;}',
  FF='precision mediump float;varying float al;void main(){float d=length(gl_PointCoord-.5)*2.;float g=d<.3?1.-d/.3*.5:.5*(1.-d)/.7;float x=max(g,0.)*al;gl_FragColor=vec4(vec3(1.,.6196,.4902)*x,x);}',
 // onda do toque: um anel com a espessura e o brilho de antes (sem uniformes partilhados: as precisões não batem)
  OV='attribute vec2 a;uniform vec2 r;uniform vec3 c;varying vec2 e;varying float rz;void main(){e=a*(c.z+4.);rz=c.z;vec2 p=c.xy+e;gl_Position=vec4(p.x/r.x*2.-1.,1.-p.y/r.y*2.,0.,1.);}',
  OF='#ifdef GL_FRAGMENT_PRECISION_HIGH\nprecision highp float;\n#else\nprecision mediump float;\n#endif\nuniform vec2 k;varying vec2 e;varying float rz;void main(){float x=clamp(k.y*.5+.5-abs(length(e)-rz),0.,1.)*k.x;gl_FragColor=vec4(vec3(1.,.6196,.4902)*x,x);}';
 function prog(g,vsrc,fsrc){var v=g.createShader(g.VERTEX_SHADER),f=g.createShader(g.FRAGMENT_SHADER),o=g.createProgram();
  g.shaderSource(v,vsrc);g.compileShader(v);g.shaderSource(f,fsrc);g.compileShader(f);
  g.attachShader(o,v);g.attachShader(o,f);g.bindAttribLocation(o,0,'a');g.linkProgram(o);
  return g.getProgramParameter(o,g.LINK_STATUS)?o:null}
 // ensaio numa tela à parte: a tela das faíscas só aceita um tipo de desenho, por isso só passa a WebGL se os dois programas ligarem
 var ens=null;try{var te=novaTela(1,1);ens=te.getContext('webgl')}catch(_){}
 if(ens){var okE=!!(prog(ens,FV,FF)&&prog(ens,OV,OF));var pe=ens.getExtension('WEBGL_lose_context');if(pe)pe.loseContext();ens=null;
  if(okE){try{pg=P.getContext('webgl',{alpha:true,premultipliedAlpha:true,antialias:false,depth:false,stencil:false,powerPreference:'low-power'})}catch(_){}}}
 if(pg){pP=prog(pg,FV,FF);pA=prog(pg,OV,OF);
  if(!pP){pg=null}else{
   pD=new Float32Array(480);pB=pg.createBuffer();pg.bindBuffer(pg.ARRAY_BUFFER,pB);pg.bufferData(pg.ARRAY_BUFFER,pD.byteLength,pg.DYNAMIC_DRAW);
   pQ=pg.createBuffer();pg.bindBuffer(pg.ARRAY_BUFFER,pQ);pg.bufferData(pg.ARRAY_BUFFER,new Float32Array([-1,-1,1,-1,-1,1,1,1]),pg.STATIC_DRAW);
   pR=pg.getUniformLocation(pP,'r');if(pA){pAr=pg.getUniformLocation(pA,'r');pAc=pg.getUniformLocation(pA,'c');pAk=pg.getUniformLocation(pA,'k')}
   pg.enableVertexAttribArray(0);pg.enable(pg.BLEND);pg.blendFunc(pg.ONE,pg.ONE_MINUS_SRC_ALPHA);pg.clearColor(0,0,0,0);
   if(P.addEventListener)P.addEventListener('webglcontextlost',function(e){e.preventDefault();pg=null});
  }
 }
 if(!pg&&!cx){try{cx=P.getContext('2d')}catch(_){}}
 if(cx){fa=novaTela(64,64);
  (function(){var g=fa.getContext('2d'),gr=g.createRadialGradient(32,32,0,32,32,32);
   gr.addColorStop(0,'rgba(255,158,125,1)');gr.addColorStop(.3,'rgba(255,158,125,.5)');gr.addColorStop(1,'rgba(255,158,125,0)');
   g.fillStyle=gr;g.fillRect(0,0,64,64)})();
  if(fa.transferToImageBitmap)fa=fa.transferToImageBitmap();
 }
 function medir(w,h){
  var nW=Math.round(w*dpr),nH=Math.round(h*dpr);
  if(gl){A.width=Math.max(1,Math.round(w*.35));A.height=Math.max(1,Math.round(h*.35))}
  if(nW!==W||nH!==H){
   var sx=W?nW/W:1,sy=H?nH/H:1;W=P.width=nW;H=P.height=nH;
   var alvoN=Math.round(Math.min(120,Math.max(40,w*h/9000)));
   ps.forEach(function(p){p.x*=sx;p.y*=sy});
   while(ps.length<alvoN)ps.push({x:Math.random()*W,y:Math.random()*H,vx:0,vy:0,r:(1.6+Math.random()*2.8)*dpr,f:Math.random()*6.283,v:.12+Math.random()*.3});
   ps.length=alvoN;
  }
 }
 function aurora(agora){
  if(!gl)return;
  gl.viewport(0,0,A.width,A.height);gl.uniform1f(uT,(agora-t0)/1000);gl.uniform2f(uR,A.width,A.height);
  gl.uniform2f(uL,incl.x,-incl.y);gl.uniform1f(uS,rolar);gl.drawArrays(gl.TRIANGLE_STRIP,0,4);
 }
 function faiscas(dt,k){
  if(!pg&&!cx)return;
  if(cx)cx.clearRect(0,0,W,H);
  for(var i=0;i<ps.length;i++){var p=ps[i];
   p.f+=.012*k;var ax=0,ay=0;
   if(toque){var dx=p.x-toque.x,dy=p.y-toque.y,d2=dx*dx+dy*dy,R=(toque.forte?130:90)*dpr;
    if(d2<R*R){var d=Math.sqrt(d2)||1,fz=(1-d/R)*(toque.forte?1:.45)*dpr;ax+=dx/d*fz;ay+=dy/d*fz}}
   p.vx=p.vx*.94+(ax*.12+incl.x*.05*dpr)*k;p.vy=p.vy*.94+(ay*.12+incl.y*.05*dpr)*k;
   p.x+=(p.vx+Math.sin(p.f)*.18*dpr)*k;p.y+=(p.vy-p.v*dpr)*k;
   if(p.y<-12*dpr){p.y=H+12*dpr;p.x=Math.random()*W}else if(p.y>H+12*dpr)p.y=-12*dpr;
   if(p.x<-12*dpr)p.x=W+12*dpr;else if(p.x>W+12*dpr)p.x=-12*dpr;
   // teto do brilho: .12 na metade de cima (onde a aurora é mais forte), .2 em baixo
   var teto=p.y<H*.5?.12:.2,al=teto*(.55+.45*Math.sin(p.f*1.7)),s=p.r*6;
   if(pg){pD[i*4]=p.x;pD[i*4+1]=p.y;pD[i*4+2]=s;pD[i*4+3]=al}
   else{cx.globalAlpha=al;cx.drawImage(fa,p.x-s/2,p.y-s/2,s,s)}
  }
  if(pg){
   pg.viewport(0,0,W,H);pg.clear(pg.COLOR_BUFFER_BIT);
   pg.useProgram(pP);pg.uniform2f(pR,W,H);pg.bindBuffer(pg.ARRAY_BUFFER,pB);pg.bufferSubData(pg.ARRAY_BUFFER,0,pD);
   pg.vertexAttribPointer(0,4,pg.FLOAT,false,0,0);pg.drawArrays(pg.POINTS,0,ps.length);
   if(ondas.length&&pA){pg.useProgram(pA);pg.uniform2f(pAr,W,H);pg.bindBuffer(pg.ARRAY_BUFFER,pQ);pg.vertexAttribPointer(0,2,pg.FLOAT,false,0,0)}
  }else cx.globalAlpha=1;
  for(var j=ondas.length-1;j>=0;j--){var o=ondas[j];o.t+=dt;var u=o.t/900;
   if(u>=1){ondas.splice(j,1);continue}
   var rr=(1-Math.pow(1-u,3))*160*dpr;
   if(pg){if(pA){pg.uniform3f(pAc,o.x,o.y,rr);pg.uniform2f(pAk,.35*(1-u),1.5*dpr);pg.drawArrays(pg.TRIANGLE_STRIP,0,4)}}
   else{cx.beginPath();cx.arc(o.x,o.y,rr,0,6.2832);
    cx.strokeStyle='rgba(255,158,125,'+(.35*(1-u)).toFixed(3)+')';cx.lineWidth=1.5*dpr;cx.stroke()}
   for(var m=0;m<ps.length;m++){var q=ps[m],ex=q.x-o.x,ey=q.y-o.y,dd=Math.sqrt(ex*ex+ey*ey)||1;
    if(Math.abs(dd-rr)<14*dpr){q.vx+=ex/dd*.6*dpr;q.vy+=ey/dd*.6*dpr}}
  }
 }
 var luzAX=-1,luzAY=-1,luzX=50,luzY=24;
 // passos de 2 % com margem (histerese): o tremor da mão não reescreve a luz a cada quadro
 function segue(atual,alvo,passo){return Math.abs(alvo-atual)>=passo?Math.round(alvo/passo)*passo:atual}
 return {
  medir:medir,
  // um quadro: devolve a posição nova da luz dos portais quando muda (em %), senão null
  quadro:function(agora,dt){
   var k=dt/16.667;
   incl.x+=(alvo.x-incl.x)*Math.min(1,.06*k);incl.y+=(alvo.y-incl.y)*Math.min(1,.06*k);
   aurora(agora);faiscas(dt,k);
   luzX=segue(luzX,50+incl.x*35,2);luzY=segue(luzY,24+incl.y*28,2);
   if(luzX===luzAX&&luzY===luzAY)return null;luzAX=luzX;luzAY=luzY;return [luzX,luzY];
  },
  parado:function(){aurora(t0+9000);faiscas(0,0)},
  receber:function(m){
   if(m.tipo==='alvo'){alvo.x=m.x;alvo.y=m.y}
   else if(m.tipo==='toque'){toque=m.t?{x:m.t.x*dpr,y:m.t.y*dpr,forte:m.t.forte}:null}
   else if(m.tipo==='onda'){ondas.push({x:m.x*dpr,y:m.y*dpr,t:0})}
   else if(m.tipo==='rolar'){rolar=m.v}
   else if(m.tipo==='medida'){medir(m.larg,m.alt)}
  }
 };
}
var ceu=null,vivo=false,ult=0;
var pedir=self.requestAnimationFrame?function(f){self.requestAnimationFrame(f)}:function(f){setTimeout(function(){f(performance.now())},16)};
function quadro(agora){if(!vivo)return;var dt=Math.min(50,agora-ult);ult=agora;var l=ceu.quadro(agora,dt);if(l)postMessage({tipo:'luz',mx:l[0],my:l[1]});pedir(quadro)}
onmessage=function(e){var d=e.data;
 if(d.tipo==='inicio'){
  ceu=criarCeu(d.aurora,d.faiscas,function(w,h){return new OffscreenCanvas(w,h)},function(){postMessage({tipo:'semWebgl'})},d.dpr);
  ceu.medir(d.larg,d.alt);vivo=true;ult=performance.now();pedir(quadro);return;
 }
 if(!ceu)return;
 if(d.tipo==='pausa'){vivo=false}
 else if(d.tipo==='retoma'){if(!vivo){vivo=true;ult=performance.now();pedir(quadro)}}
 else ceu.receber(d);
};
