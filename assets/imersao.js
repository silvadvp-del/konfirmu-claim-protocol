// Inclinação e luz seguem a orientação do ecrã. Fotografias e filmes mantêm os bytes originais.
(() => {
  'use strict';
  const viewerEnabled = document.currentScript.hasAttribute('data-viewer');
  const root = document.documentElement;
  const toolbar = document.createElement('div');
  toolbar.className = 'im3d-tools';
  toolbar.innerHTML = '<button type="button" id="im3d" aria-pressed="false">Imersão 3D</button><small hidden>Inclina o telemóvel ou move o dedo ou o rato. Toca de novo para sair.</small>';
  const heading = document.querySelector('h1, .top-bar');
  if (heading) heading.after(toolbar);
  else document.body.prepend(toolbar);
  const button = toolbar.querySelector('button');
  const hint = toolbar.querySelector('small');
  const reduced = matchMedia('(prefers-reduced-motion: reduce)');
  let active = false;
  let generation = 0;
  let frame = 0;
  let x = 0, y = 0, origin = null;
  let ownsFullscreen = false;
  // A inclinação vai direta para o «transform» de cada elemento à vista; a luz usa duas propriedades próprias
  // do elemento (não herdadas). Só se escreve quando o valor muda: passos de 0,5° na inclinação (menos de meio
  // píxel na borda de um cartão) e de 4 % na luz (uma sombra muito suave), com margem para o tremor da mão.
  // Assim, a cada quadro o navegador recalcula poucos elementos e a memória fica estável.
  const ALVOS = '.card,.game-card,.im3d-frame,.im3d-scene,.cert,.parchment,.hero';
  let alvos = [], recolha = 0, chaveInc = null, chaveLuz = null, inclinacao = '', luz = null;
  const visiveis = new Set();
  const vigia = 'IntersectionObserver' in window ? new IntersectionObserver(entradas => {
    for (const e of entradas) {
      if (e.isIntersecting) { visiveis.add(e.target); escrever(e.target, 3); }
      else visiveis.delete(e.target);
    }
  }, { rootMargin: '0px' }) : null;
  function escrever(el, quais) {
    if (!active) return;
    const s = el.style;
    if (quais & 1) s.transform = inclinacao;
    if (quais & 2) {
      if (luz) { s.setProperty('--lx', luz[0]); s.setProperty('--ly', luz[1]); }
      else { s.removeProperty('--lx'); s.removeProperty('--ly'); }
    }
  }
  function recolher() {
    const novos = Array.from(document.querySelectorAll(ALVOS));
    if (vigia) {
      const conjunto = new Set(novos);
      for (const el of alvos) if (!conjunto.has(el)) { vigia.unobserve(el); visiveis.delete(el); }
      for (const el of novos) vigia.observe(el);
    }
    alvos = novos;
    recolha = performance.now();
  }
  function limpar() {
    if (vigia) vigia.disconnect();
    visiveis.clear();
    for (const el of alvos) { el.style.transform = ''; el.style.removeProperty('--lx'); el.style.removeProperty('--ly'); }
    alvos = [];
    chaveInc = chaveLuz = null;
    rx = ry = 0; lx = 50; ly = 35;
  }
  // Segue o valor em passos fixos, com margem de um passo (histerese): sem saltos para trás e para a frente.
  const segue = (atual, alvo, p) => Math.abs(alvo - atual) >= p ? Math.round(alvo / p) * p + 0 : atual;
  let rx = 0, ry = 0, lx = 50, ly = 35;

  function paint() {
    frame = 0;
    if (!active) return;
    if (performance.now() - recolha > 1000) { recolher(); chaveInc = chaveLuz = null; }
    let quais = 0;
    if (reduced.matches) {
      if (chaveInc !== '') { chaveInc = inclinacao = ''; quais |= 1; }
      if (chaveLuz !== '') { chaveLuz = ''; luz = null; quais |= 2; }
    } else {
      rx = segue(rx, -y * 8, .5); ry = segue(ry, x * 12, .5);
      lx = segue(lx, 50 + x * 40, 4); ly = segue(ly, 35 + y * 34, 4);
      const inc = 'perspective(850px) rotateX(' + rx.toFixed(1) + 'deg) rotateY(' + ry.toFixed(1) + 'deg)';
      if (inc !== chaveInc) { chaveInc = inclinacao = inc; quais |= 1; }
      const l = [lx.toFixed(0) + '%', ly.toFixed(0) + '%'];
      const k = l.join(' ');
      if (k !== chaveLuz) { chaveLuz = k; luz = l; quais |= 2; }
    }
    if (quais) for (const el of (vigia ? visiveis : alvos)) escrever(el, quais);
  }
  function tilt(nx, ny) {
    x = Math.max(-1, Math.min(1, nx));
    y = Math.max(-1, Math.min(1, ny));
    if (!frame) frame = requestAnimationFrame(paint);
  }
  function pointer(event) {
    const p = event.touches ? event.touches[0] : event;
    if (p) tilt(p.clientX * 2 / innerWidth - 1, p.clientY * 2 / innerHeight - 1);
  }
  function orient(event) {
    if (!Number.isFinite(event.beta) || !Number.isFinite(event.gamma)) return;
    const angle = (screen.orientation?.angle ?? window.orientation ?? 0) * Math.PI / 180;
    if (!origin || angle !== origin.angle) origin = { beta: event.beta, gamma: event.gamma, angle };
    const dx = (event.gamma - origin.gamma) / 35, dy = (event.beta - origin.beta) / 35;
    tilt(dx * Math.cos(angle) + dy * Math.sin(angle), dy * Math.cos(angle) - dx * Math.sin(angle));
  }
  const pointerEvent = 'PointerEvent' in window ? 'pointermove' : 'mousemove';
  const fullscreen = () => document.fullscreenElement || document.webkitFullscreenElement;
  function toggle(on) {
    if (active === on) return;
    active = on;
    const current = ++generation;
    root.classList.toggle('im3d-active', on);
    button.setAttribute('aria-pressed', String(on));
    hint.hidden = !on;
    origin = null;
    if (on) {
      recolher();
      addEventListener(pointerEvent, pointer, { passive: true });
      if (pointerEvent === 'mousemove') addEventListener('touchmove', pointer, { passive: true });
      // Os dois pedidos dependem do gesto original no iOS.
      const sensor = window.DeviceOrientationEvent;
      try {
        if (sensor?.requestPermission) {
          Promise.resolve(sensor.requestPermission()).then(result => {
            if (result === 'granted' && current === generation) addEventListener('deviceorientation', orient);
          }).catch(() => {});
        } else if (sensor) addEventListener('deviceorientation', orient);
      } catch (_) { /* O ponteiro continua disponível. */ }
      if (!fullscreen()) {
        try {
          const request = root.requestFullscreen || root.webkitRequestFullscreen;
          if (request) { ownsFullscreen = true; Promise.resolve(request.call(root)).catch(() => { if (current === generation) ownsFullscreen = false; }); }
        } catch (_) { ownsFullscreen = false; }
      }
    } else {
      removeEventListener(pointerEvent, pointer);
      removeEventListener('touchmove', pointer);
      removeEventListener('deviceorientation', orient);
      if (frame) cancelAnimationFrame(frame);
      frame = 0; x = 0; y = 0;
      if (ownsFullscreen && fullscreen() === root) {
        const exit = document.exitFullscreen || document.webkitExitFullscreen;
        if (exit) Promise.resolve(exit.call(document)).catch(() => {});
      }
      ownsFullscreen = false;
      limpar();
    }
    paint();
  }
  button.addEventListener('click', () => toggle(!active));
  function syncFullscreen() { if (active && ownsFullscreen && !fullscreen()) toggle(false); }
  document.addEventListener('fullscreenchange', syncFullscreen);
  document.addEventListener('webkitfullscreenchange', syncFullscreen);
  addEventListener('keydown', e => { if (e.key === 'Escape') toggle(false); });
  addEventListener('pagehide', () => toggle(false));
  reduced.addEventListener?.('change', () => { if (active) paint(); });

  if (!viewerEnabled) return;
  const viewer = document.createElement('details');
  viewer.className = 'im3d-viewer';
  viewer.innerHTML = '<summary>Ver uma imagem ou um vídeo deste aparelho</summary><label>Escolher ficheiro <input type="file" accept="image/*,video/*"></label><div class="im3d-frame"></div><p role="status"></p>';
  toolbar.after(viewer);
  const input = viewer.querySelector('input'), stage = viewer.querySelector('.im3d-frame');
  const status = viewer.querySelector('[role="status"]');
  let url;
  function clearMedia() {
    const movie = stage.querySelector('video');
    if (movie) { movie.pause(); movie.removeAttribute('src'); movie.load(); }
    stage.replaceChildren();
    if (url) URL.revokeObjectURL(url);
    url = null;
  }
  input.addEventListener('change', () => {
    clearMedia();
    status.textContent = '';
    const file = input.files[0];
    if (!file) return;
    const type = file.type.split('/')[0];
    if (type !== 'image' && type !== 'video') { status.textContent = 'Escolhe uma imagem ou um vídeo.'; return; }
    const media = document.createElement(type === 'image' ? 'img' : 'video');
    if (type === 'image') media.alt = file.name;
    else { media.controls = true; media.playsInline = true; media.preload = 'metadata'; }
    media.addEventListener('error', () => {
      if (stage.firstChild === media) status.textContent = 'Este navegador não conseguiu abrir o ficheiro.';
    });
    url = URL.createObjectURL(file);
    stage.append(media);
    media.src = url;
  });
  addEventListener('pagehide', e => { if (!e.persisted) clearMedia(); });
})();
