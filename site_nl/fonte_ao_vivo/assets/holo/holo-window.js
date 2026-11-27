/* Local motion controller. Bind once per frame and destroy on unmount. */
window.KonfirmuHoloWindow = {
  init(frame, options = {}) {
    const stage = frame.querySelector('[data-holo-stage]');
    const sheen = frame.querySelector('[data-sheen]');
    const pref = matchMedia('(prefers-reduced-motion: reduce)');
    const lean = navigator.deviceMemory <= 1;
    const clamp = n => Math.max(-1, Math.min(1, n));
    const off = [];
    let x=0, y=0, u=0, v=0, raf=0, timer=0, origin=null;
    let motion=true, sensor=false, seen=true, dead=false, request=0;
    const active = () => motion && !pref.matches && !lean && !dead;
    function report(status) {
      frame.dataset.holoFlat=active()?'0':'1';
      options.onState?.({active:active(), locked:pref.matches || lean, sensor, status});
    }
    function draw() {
      stage.style.transform = 'rotateY('+(u*7)+'deg) rotateX('+(-v*7)+'deg)';
      if (sheen) sheen.style.background = 'radial-gradient(circle at '+(50+u*36)+'% '+(50+v*34)+'%, #ffefbf24, transparent 53%)';
    }
    function tick() {
      raf=0;
      if (!active() || !seen || document.hidden) return;
      u+=(x-u)*.19; v+=(y-v)*.19;
      if (Math.abs(x-u)+Math.abs(y-v)<.003) {u=x; v=y;}
      draw();
      if (u!==x || v!==y) raf=requestAnimationFrame(tick);
    }
    function aim(a,b) {
      x=clamp(a); y=clamp(b);
      if (!raf && active() && seen && !document.hidden) raf=requestAnimationFrame(tick);
    }
    function listen(el,type,fn,opts) {
      el.addEventListener(type,fn,opts); off.push(()=>el.removeEventListener(type,fn,opts));
    }
    function orient(e) {
      if (!sensor || !Number.isFinite(e.gamma) || !Number.isFinite(e.beta)) return;
      clearTimeout(timer);
      origin ||= [e.gamma,e.beta];
      const a=(e.gamma-origin[0])/24, b=(e.beta-origin[1])/24;
      const t=(window.screen.orientation?.angle ?? window.orientation ?? 0)*Math.PI/180;
      aim(a*Math.cos(t)+b*Math.sin(t), b*Math.cos(t)-a*Math.sin(t));
    }
    function stop() {
      sensor=false; origin=null; clearTimeout(timer); request++;
      window.removeEventListener('deviceorientation',orient);
    }
    function reset() {
      stop(); cancelAnimationFrame(raf); x=y=u=v=raf=0; draw(); report();
    }
    async function setSensor(value) {
      stop(); const id=request;
      if (!value || !active()) {aim(0,0); report(); return;}
      const api=window.DeviceOrientationEvent;
      if (!api || !window.isSecureContext) return report('unavailable');
      try {
        const access=await (api.requestPermission?.() ?? 'granted');
        if (id!==request || !active()) return;
        if (access!=='granted') return report('denied');
        sensor=true; window.addEventListener('deviceorientation',orient);
        timer=setTimeout(()=>{stop();report('unavailable');},2600); report();
      } catch {if(id===request) report('denied');}
    }
    listen(frame,'pointermove',e=>{
      if (sensor || !active()) return;
      const r=frame.getBoundingClientRect();
      aim(2*(e.clientX-r.left)/r.width-1,2*(e.clientY-r.top)/r.height-1);
    },{passive:true});
    listen(frame,'pointerleave',()=>{if(!sensor) aim(0,0);});
    listen(frame,'keydown',e=>{
      const d={ArrowLeft:[-.33,0],ArrowRight:[.33,0],ArrowUp:[0,-.33],ArrowDown:[0,.33],Home:[-x,-y]}[e.key];
      if(d && active()) {e.preventDefault();stop();report();aim(x+d[0],y+d[1]);}
    });
    listen(document,'visibilitychange',()=>aim(x,y));
    if(pref.addEventListener) listen(pref,'change',reset);
    else {pref.addListener(reset);off.push(()=>pref.removeListener(reset));}
    const io=window.IntersectionObserver && new IntersectionObserver(([e])=>{seen=e.isIntersecting;aim(x,y);});
    io?.observe(frame); report();
    return {setSensor,setMotion(on){motion=on;reset();},destroy(){dead=true;reset();io?.disconnect();off.forEach(f=>f());}};
  }
};
