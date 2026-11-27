// assets/ceu_vivo.js — gerado por scripts/gerar_menu.py. Não editar à mão.
// O céu vivo do menu desenhado fora da linha principal da página (OffscreenCanvas): a página não repinta a cada quadro.
'use strict';
// O céu do menu: aurora em WebGL e partículas quentes em Canvas 2D. Uma só fonte para os dois sítios onde corre:
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
 var cx=P.getContext('2d'),fa=novaTela(64,64);
 (function(){var g=fa.getContext('2d'),gr=g.createRadialGradient(32,32,0,32,32,32);
  gr.addColorStop(0,'rgba(255,158,125,1)');gr.addColorStop(.3,'rgba(255,158,125,.5)');gr.addColorStop(1,'rgba(255,158,125,0)');
  g.fillStyle=gr;g.fillRect(0,0,64,64)})();
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
  cx.clearRect(0,0,W,H);
  for(var i=0;i<ps.length;i++){var p=ps[i];
   p.f+=.012*k;var ax=0,ay=0;
   if(toque){var dx=p.x-toque.x,dy=p.y-toque.y,d2=dx*dx+dy*dy,R=(toque.forte?130:90)*dpr;
    if(d2<R*R){var d=Math.sqrt(d2)||1,fz=(1-d/R)*(toque.forte?1:.45)*dpr;ax+=dx/d*fz;ay+=dy/d*fz}}
   p.vx=p.vx*.94+(ax*.12+incl.x*.05*dpr)*k;p.vy=p.vy*.94+(ay*.12+incl.y*.05*dpr)*k;
   p.x+=(p.vx+Math.sin(p.f)*.18*dpr)*k;p.y+=(p.vy-p.v*dpr)*k;
   if(p.y<-12*dpr){p.y=H+12*dpr;p.x=Math.random()*W}else if(p.y>H+12*dpr)p.y=-12*dpr;
   if(p.x<-12*dpr)p.x=W+12*dpr;else if(p.x>W+12*dpr)p.x=-12*dpr;
   // teto do brilho: .12 na metade de cima (onde a aurora é mais forte), .2 em baixo
   var teto=p.y<H*.5?.12:.2;cx.globalAlpha=teto*(.55+.45*Math.sin(p.f*1.7));
   var s=p.r*6;cx.drawImage(fa,p.x-s/2,p.y-s/2,s,s);
  }
  cx.globalAlpha=1;
  for(var j=ondas.length-1;j>=0;j--){var o=ondas[j];o.t+=dt;var u=o.t/900;
   if(u>=1){ondas.splice(j,1);continue}
   var rr=(1-Math.pow(1-u,3))*160*dpr;cx.beginPath();cx.arc(o.x,o.y,rr,0,6.2832);
   cx.strokeStyle='rgba(255,158,125,'+(.35*(1-u)).toFixed(3)+')';cx.lineWidth=1.5*dpr;cx.stroke();
   for(var m=0;m<ps.length;m++){var q=ps[m],ex=q.x-o.x,ey=q.y-o.y,dd=Math.sqrt(ex*ex+ey*ey)||1;
    if(Math.abs(dd-rr)<14*dpr){q.vx+=ex/dd*.6*dpr;q.vy+=ey/dd*.6*dpr}}
  }
 }
 var luzUlt='',luzX=50,luzY=24;
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
   if(luzX+','+luzY===luzUlt)return null;luzUlt=luzX+','+luzY;return [luzX,luzY];
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
