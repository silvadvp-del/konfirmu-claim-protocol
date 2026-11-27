(() => {
  const scene=document.querySelector('.kh-scene');
  if (!scene) return;
  const frame=scene.querySelector('.holo-frame'), motion=scene.querySelector('.kh-motion');
  const tilt=scene.querySelector('.kh-tilt'), note=scene.querySelector('.kh-note');
  const words=scene.dataset;
  let current;
  const api=KonfirmuHoloWindow.init(frame,{onState(state){
    current=state;
    motion.textContent=state.active?words.stop:words.start;
    motion.disabled=state.locked;
    motion.setAttribute('aria-pressed',state.active);
    tilt.disabled=!state.active;
    tilt.setAttribute('aria-pressed',state.sensor);
    tilt.textContent=state.sensor?words.end:words.gyro;
    note.textContent=words[state.status] || (state.locked?words.locked:!state.active?words.static:state.sensor?words.on:'');
  }});
  scene.querySelector('.kh-options').hidden=false;
  tilt.hidden=!window.DeviceOrientationEvent || !window.isSecureContext;
  motion.onclick=()=>api.setMotion(!current.active);
  tilt.onclick=()=>api.setSensor(!current.sensor);
  window.addEventListener('pagehide',event=>{if(!event.persisted)api.destroy();});
})();
