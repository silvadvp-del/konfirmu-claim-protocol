// Konfirmu · Modo Família 3D (tigelas em WebGL, tranca de adulto, filme manifesto). Sem rede: tudo neste ficheiro.
import * as THREE from "three";
import { EffectComposer } from "three/addons/postprocessing/EffectComposer.js";
import { RenderPass } from "three/addons/postprocessing/RenderPass.js";
import { UnrealBloomPass } from "three/addons/postprocessing/UnrealBloomPass.js";
import { OutputPass } from "three/addons/postprocessing/OutputPass.js";
import { ShaderPass } from "three/addons/postprocessing/ShaderPass.js";
import { RoomEnvironment } from "three/addons/environments/RoomEnvironment.js";

// Paleta única (ordem de 27-11, 12:49 e 13:14). Nenhuma outra cor entra no desenho.
const ABISSAL = 0x0B192C, SOLAR = 0xFF9E7D, TITANIO = 0xF4F7FA, NEVOEIRO = 0x9FB3C8, VIDRO = 0x0F223D;
const D = JSON.parse(document.getElementById("dados").textContent);
const Q = new URLSearchParams(location.search);
const QUADROS = Q.has("quadros");
const RETRATO = Q.has("retrato") ? Math.max(0, Math.min(7, parseInt(Q.get("retrato"), 10) - 1)) : -1;
const CHAVE = "konfirmu_familia_v1";
const $ = (id) => document.getElementById(id);
const clamp = (x, a, b) => Math.max(a, Math.min(b, x));
const suave = (a, b, x) => { const u = clamp((x - a) / (b - a), 0, 1); return u * u * (3 - 2 * u); };
function semente(a) {
  return function () { a |= 0; a = a + 0x6D2B79F5 | 0; let t = Math.imul(a ^ a >>> 15, 1 | a); t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t; return ((t ^ t >>> 14) >>> 0) / 4294967296; };
}
function salto(u) {
  const n = 7.5625, d = 2.75;
  if (u < 1 / d) return n * u * u;
  if (u < 2 / d) { u -= 1.5 / d; return n * u * u + 0.75; }
  if (u < 2.5 / d) { u -= 2.25 / d; return n * u * u + 0.9375; }
  u -= 2.625 / d; return n * u * u + 0.984375;
}

// ---------------------------------------------------------------- estado guardado (só neste aparelho)
let estado = ler();
function ler() { try { return JSON.parse(localStorage.getItem(CHAVE)) || {}; } catch (e) { return {}; } }
function guardar() { try { localStorage.setItem(CHAVE, JSON.stringify(estado)); } catch (e) { /* sem armazenamento */ } }

// ---------------------------------------------------------------- línguas: menu (62) + frases da tranca (27; as outras em inglês)
const LINGS = D.linguas;
const TX = D.textos;
let lingua = escolherLingua();
function escolherLingua() {
  const tem = (c) => LINGS.some((l) => l.c === c);
  if (estado.lang && tem(estado.lang)) return estado.lang;
  const pedidas = navigator.languages && navigator.languages.length ? navigator.languages : [navigator.language || "pt"];
  for (const p0 of pedidas) {
    const p = String(p0 || "");
    if (tem(p)) return p;
    const base = p.split("-")[0].toLowerCase();
    if (base === "zh") return /TW|HK|MO|Hant/i.test(p) ? "zh-Hant" : "zh-Hans";
    if (tem(base)) return base;
  }
  return "pt";
}
function t(k) {
  const i = TX.chaves.indexOf(k);
  const l = TX.linguas[lingua] || TX.linguas.en;
  const s = (l && l.s[i]) || TX.linguas.en.s[i] || TX.linguas.pt.s[i];
  return s == null ? k : s;
}
function m(k) { const d = D.menu[lingua] || D.menu.en; return d[k] || D.menu.pt[k] || k; }

// ---------------------------------------------------------------- motor 3D
const tela = $("palco");
let renderer = null;
try {
  renderer = new THREE.WebGLRenderer({ canvas: tela, antialias: true, powerPreference: "high-performance" });
  if (!renderer.getContext()) throw new Error("sem WebGL");
} catch (e) { renderer = null; }
const COM3D = !!renderer;
document.body.classList.toggle("sem3d", !COM3D);

const cena = new THREE.Scene();
const camara = new THREE.PerspectiveCamera(38, innerWidth / innerHeight, 0.1, 90);
const camP = new THREE.Vector3(0, 1.4, 7), camO = new THREE.Vector3(0, 0.45, 0);
const alvoCamP = new THREE.Vector3(0, 1.4, 4.8), alvoCamO = new THREE.Vector3(0, 0.45, -0.6);
const ponteiro = new THREE.Vector2(0, 0), ponteiroSuave = new THREE.Vector2(0, 0);
let composer = null, bloom = null, chao = null, brilhoFundo = null, sol = null, particulas = null;
const tigelas = [];
const faiscas = [];
const R = semente(2711);

function texturaRadial(paragens) {
  const c = document.createElement("canvas"); c.width = c.height = 128;
  const g = c.getContext("2d"), gr = g.createRadialGradient(64, 64, 0, 64, 64, 64);
  paragens.forEach((s) => gr.addColorStop(s[0], s[1]));
  g.fillStyle = gr; g.fillRect(0, 0, 128, 128);
  const tx = new THREE.CanvasTexture(c); tx.colorSpace = THREE.SRGBColorSpace; return tx;
}

// O perfil da tigela, rodado à volta do eixo (torno): pé, barriga, rebordo e o fundo de dentro.
const PERFIL = [[0, 0], [0.40, 0], [0.455, 0.025], [0.44, 0.075], [0.53, 0.125], [0.71, 0.245], [0.86, 0.40], [0.955, 0.57],
  [1.0, 0.705], [1.026, 0.772], [1.004, 0.816], [0.962, 0.802], [0.938, 0.742], [0.868, 0.585], [0.748, 0.432],
  [0.588, 0.312], [0.37, 0.238], [0, 0.216]];
const T = (function () {
  const pts = new THREE.SplineCurve(PERFIL.map((p) => new THREE.Vector2(p[0], p[1]))).getPoints(119);
  pts[0].x = 0; pts[pts.length - 1].x = 0;
  let topo = 0; pts.forEach((p, i) => { if (p.y > pts[topo].y) topo = i; });
  const geo = new THREE.LatheGeometry(pts, 112), n = pts.length, cor = new Float32Array(geo.attributes.position.count * 3);
  for (let v = 0; v < geo.attributes.position.count; v++) {
    const i = v % n, p = pts[i];
    let f = 1;
    if (i > topo) f = 0.28 + 0.72 * suave(0.2, 0.8, p.y);       // dentro: mais escuro no fundo (oclusão)
    else if (p.y < 0.12) f = 0.6 + 0.4 * suave(0.0, 0.12, p.y); // o pé
    cor[v * 3] = cor[v * 3 + 1] = cor[v * 3 + 2] = f;
  }
  geo.setAttribute("color", new THREE.BufferAttribute(cor, 3));
  return { geo, pts, topo };
})();
function raioFora(y) {
  const P = T.pts;
  for (let i = 4; i <= T.topo; i++) { const a = P[i - 1], b = P[i]; if ((a.y - y) * (b.y - y) <= 0 && a.y !== b.y) return a.x + (b.x - a.x) * (y - a.y) / (b.y - a.y); }
  return 0.9;
}
function naParede(o, x, y, sal) {
  const r = raioFora(y) + (sal || 0), a = x / r, e = 0.01;
  o.position.set(Math.sin(a) * r, y, Math.cos(a) * r);
  o.rotation.set(Math.atan((raioFora(y + e) - raioFora(y - e)) / (2 * e)), a, 0, "YXZ");
  return o;
}

const G = {}, M = {};
function prepararMateriais() {
  G.esfera = new THREE.SphereGeometry(1, 32, 20);
  G.arco = new THREE.TorusGeometry(0.088, 0.022, 10, 28, Math.PI);
  G.sorriso = new THREE.TorusGeometry(0.128, 0.025, 10, 32, Math.PI);
  G.meioBaixo = new THREE.CircleGeometry(1, 40, Math.PI, Math.PI);
  G.meioCima = new THREE.CircleGeometry(1, 40, 0, Math.PI);
  G.disco = new THREE.CircleGeometry(1, 40);
  G.capsula = new THREE.CapsuleGeometry(0.021, 0.12, 4, 10);
  G.anel = new THREE.TorusGeometry(0.64, 0.024, 12, 96);
  G.pessego = new THREE.SphereGeometry(0.128, 28, 18);
  G.plano = new THREE.PlaneGeometry(1, 1);
  G.faisca = new THREE.SphereGeometry(0.032, 10, 8);
  G.cupula = new THREE.SphereGeometry(1, 40, 18, 0, Math.PI * 2, 0, Math.PI / 2);
  G.orla = new THREE.SphereGeometry(1, 40, 2, 0, Math.PI * 2, Math.PI / 2 - 0.15, 0.15);
  const s = new THREE.Shape(), q = 0.22;
  s.moveTo(0, 1); s.quadraticCurveTo(q, q, 1, 0); s.quadraticCurveTo(q, -q, 0, -1); s.quadraticCurveTo(-q, -q, -1, 0); s.quadraticCurveTo(-q, q, 0, 1);
  G.brilho = new THREE.ShapeGeometry(s, 8);
  const z = new THREE.CurvePath();
  [[-1, 1], [1, 1], [-1, -1], [1, -1]].reduce((a, b) => { z.add(new THREE.LineCurve3(new THREE.Vector3(a[0], a[1], 0), new THREE.Vector3(b[0], b[1], 0))); return b; });
  G.z = new THREE.TubeGeometry(z, 48, 0.16, 6, false);
  M.esclera = new THREE.MeshPhysicalMaterial({ color: TITANIO, roughness: 0.2, clearcoat: 1, clearcoatRoughness: 0.06 });
  M.tinta = new THREE.MeshStandardMaterial({ color: ABISSAL, roughness: 0.32 });
  M.luz = new THREE.MeshBasicMaterial({ color: TITANIO });
  M.bochecha = new THREE.MeshStandardMaterial({ color: SOLAR, emissive: SOLAR, emissiveIntensity: 0.18, roughness: 0.6, transparent: true, opacity: 0.88 });
  M.lingua = new THREE.MeshStandardMaterial({ color: SOLAR, roughness: 0.5 });
  M.palpebra = new THREE.MeshPhysicalMaterial({ color: SOLAR, roughness: 0.36, clearcoat: 0.85 });
  M.pessego = new THREE.MeshPhysicalMaterial({ color: SOLAR, roughness: 0.5, sheen: 1, sheenRoughness: 0.35, sheenColor: new THREE.Color(SOLAR), clearcoat: 0.25 });
  M.solar = new THREE.MeshStandardMaterial({ color: SOLAR, emissive: SOLAR, emissiveIntensity: 0.9 });
  M.titanio = new THREE.MeshStandardMaterial({ color: TITANIO, emissive: TITANIO, emissiveIntensity: 0.6 });
  M.bolha = new THREE.MeshPhysicalMaterial({ color: TITANIO, roughness: 0.1, transparent: true, opacity: 0.55, clearcoat: 1 });
  M.vidro = new THREE.MeshPhysicalMaterial({ color: VIDRO, roughness: 0.18, transparent: true, opacity: 0.86, clearcoat: 1 });
  M.docVidro = new THREE.MeshPhysicalMaterial({ color: VIDRO, roughness: 0.46, clearcoat: 0.3, clearcoatRoughness: 0.45, emissive: VIDRO, emissiveIntensity: 0.4 });
  M.selo = new THREE.MeshStandardMaterial({ color: SOLAR, emissive: SOLAR, emissiveIntensity: 0.38, roughness: 0.42 });
  M.linha = new THREE.MeshStandardMaterial({ color: NEVOEIRO, emissive: NEVOEIRO, emissiveIntensity: 0.22, roughness: 0.6 });
  M.sombra = new THREE.MeshBasicMaterial({ map: texturaRadial([[0, "rgba(11,25,44,0.92)"], [0.5, "rgba(11,25,44,0.42)"], [1, "rgba(11,25,44,0)"]]), transparent: true, depthWrite: false });
}
function malha(g, mat, pai) { const o = new THREE.Mesh(g, mat); if (pai) pai.add(o); return o; }

// ---------------------------------------------------------------- as 8 personagens
const LUGARES = [[0, 0.34, 0.02], [-0.27, 0.35, 0.1], [0.27, 0.35, 0.1], [-0.15, 0.37, -0.22], [0.17, 0.37, -0.2], [-0.43, 0.41, -0.04], [0.43, 0.41, -0.04], [0, 0.5, 0.04]];
function olho(b, x, y, esc, dx, dy) {
  const g = naParede(new THREE.Group(), x, y, -0.016);
  const es = malha(G.esfera, M.esclera, g); es.scale.set(0.12 * esc, 0.137 * esc, 0.075);
  const pup = new THREE.Group(); g.add(pup);
  const ir = malha(G.esfera, M.tinta, pup); ir.scale.set(0.068 * esc, 0.078 * esc, 0.03); ir.position.z = 0.062;
  const l1 = malha(G.esfera, M.luz, pup); l1.scale.setScalar(0.022 * esc); l1.position.set(0.028, 0.044, 0.088);
  const l2 = malha(G.esfera, M.luz, pup); l2.scale.setScalar(0.011 * esc); l2.position.set(-0.024, -0.03, 0.085);
  b.rosto.add(g);
  const o = { g, pup, base: [dx || 0, dy || 0] };
  b.olhos.push(o); return o;
}
function fechado(b, x, y) { b.rosto.add(naParede(malha(G.arco, M.tinta), x, y - 0.03, 0.02)); }
function sobr(b, x, y, inc) { const o = naParede(malha(G.capsula, M.tinta), x, y, 0.012); o.rotation.z = Math.PI / 2 + inc; b.rosto.add(o); }
function bochechas(b) { for (const s of [-1, 1]) { const o = naParede(malha(G.esfera, M.bochecha), s * 0.4, 0.37, -0.008); o.scale.set(0.078, 0.044, 0.02); b.rosto.add(o); } }
function boca(b, tipo) {
  const y = 0.335;
  if (tipo === "sorriso" || tipo === "lado") {
    const o = naParede(malha(G.sorriso, M.tinta), tipo === "lado" ? 0.05 : 0, y + 0.045, 0.016);
    o.rotation.z = Math.PI + (tipo === "lado" ? 0.32 : 0); if (tipo === "lado") o.scale.set(0.82, 0.82, 1); b.rosto.add(o);
  } else if (tipo === "aberta") {
    const o = naParede(malha(G.meioBaixo, M.tinta), 0, y + 0.06, 0.019); o.scale.set(0.16, 0.15, 1); b.rosto.add(o);
    const l = naParede(malha(G.meioBaixo, M.lingua), 0, y - 0.02, 0.022); l.scale.set(0.08, 0.055, 1); b.rosto.add(l);
  } else if (tipo === "o" || tipo === "o_grande") {
    const k = tipo === "o" ? 1 : 1.55, o = naParede(malha(G.disco, M.tinta), 0.01, y - 0.01, 0.019); o.scale.set(0.055 * k, 0.068 * k, 1); b.rosto.add(o);
  } else {
    const o = naParede(malha(G.capsula, M.tinta), tipo === "torta" ? 0.03 : 0, y, 0.014);
    o.rotation.z = Math.PI / 2 + (tipo === "torta" ? 0.2 : 0); o.scale.set(0.9, 0.5, 0.9); b.rosto.add(o);
  }
}
function extra(b, tipo) {
  const rnd = semente(500 + b.k);
  if (tipo === "estrelas" || tipo === "brilho") {
    const n = tipo === "estrelas" ? 3 : 1;
    for (let i = 0; i < n; i++) {
      const o = malha(G.brilho, i === 2 ? M.solar : M.titanio, b.corpo), f = rnd() * 6.28, r0 = tipo === "estrelas" ? 1.12 : 0.58;
      o.anima = (tt) => { const a = f + tt * 0.7; o.position.set(Math.sin(a) * r0, (tipo === "estrelas" ? 1.0 : 0.62) + 0.08 * Math.sin(tt * 2 + f), Math.cos(a) * 0.45 + 0.35); o.rotation.z = tt * 1.5 + f; o.scale.setScalar((tipo === "estrelas" ? 0.08 : 0.06) * (0.8 + 0.3 * Math.sin(tt * 3 + f))); };
      b.extras.push(o);
    }
  } else if (tipo === "zz") {
    for (let i = 0; i < 2; i++) {
      const o = malha(G.z, M.solar, b.corpo), f = i * 1.4;
      o.anima = (tt) => { const u = ((tt * 0.35 + f / 2.8) % 1); o.position.set(0.55 + u * 0.35, 0.95 + u * 0.75, 0.2); o.scale.setScalar(0.06 * (1 - u * 0.4)); o.visible = u < 0.92; };
      b.extras.push(o);
    }
  } else if (tipo === "bolhas") {
    [0.045, 0.07, 0.1].forEach((r0, i) => {
      const o = malha(G.esfera, M.bolha, b.corpo);
      o.anima = (tt) => { o.position.set(-0.62 - i * 0.2, 0.9 + i * 0.28 + 0.03 * Math.sin(tt * 1.6 + i), 0.35); o.scale.setScalar(r0); };
      b.extras.push(o);
    });
  }
}
function montarRosto(b) {
  const e = b.expr, L = -0.25, Rr = 0.25, Y = 0.5;
  if (e === "feliz") { olho(b, L, Y, 1); olho(b, Rr, Y, 1); sobr(b, L, 0.65, 0.08); sobr(b, Rr, 0.65, -0.08); boca(b, "sorriso"); bochechas(b); }
  if (e === "curiosa") { olho(b, L, Y, 1, 0.022, 0.016); olho(b, Rr, Y, 1, 0.022, 0.016); sobr(b, L, 0.69, 0.18); sobr(b, Rr, 0.65, -0.05); boca(b, "o"); bochechas(b); }
  if (e === "risonha") { fechado(b, L, Y); fechado(b, Rr, Y); sobr(b, L, 0.66, 0.1); sobr(b, Rr, 0.66, -0.1); boca(b, "aberta"); bochechas(b); b.semPiscar = true; }
  if (e === "surpresa") { olho(b, L, Y + 0.01, 1.18); olho(b, Rr, Y + 0.01, 1.18); sobr(b, L, 0.72, 0.05); sobr(b, Rr, 0.72, -0.05); boca(b, "o_grande"); }
  if (e === "marota") { olho(b, L, Y, 1, 0.01, 0); fechado(b, Rr, Y); sobr(b, L, 0.66, 0.12); sobr(b, Rr, 0.63, 0.12); boca(b, "lado"); bochechas(b); extra(b, "brilho"); b.semPiscar = true; }
  if (e === "sonolenta") {
    // pálpebra 3D: uma cúpula da cor da tigela por cima do olho, com a orla escura a seguir a curva (nada de discos planos)
    for (const x of [L, Rr]) { const o = olho(b, x, Y, 1, 0, -0.045); const p = malha(G.cupula, M.palpebra, o.g); p.scale.set(0.13, 0.148, 0.125); p.rotation.x = 0.3; const l = malha(G.orla, M.tinta, o.g); l.scale.set(0.134, 0.152, 0.129); l.rotation.x = 0.3; }
    sobr(b, L, 0.62, -0.06); sobr(b, Rr, 0.62, 0.06); boca(b, "pequena"); bochechas(b); extra(b, "zz"); b.semPiscar = true;
  }
  if (e === "pensativa") { olho(b, L, Y, 1, -0.024, 0.024); olho(b, Rr, Y, 1, -0.024, 0.024); sobr(b, L, 0.68, -0.1); sobr(b, Rr, 0.66, 0.16); boca(b, "torta"); extra(b, "bolhas"); }
  if (e === "orgulhosa") { fechado(b, L, Y); fechado(b, Rr, Y); sobr(b, L, 0.67, 0.12); sobr(b, Rr, 0.67, -0.12); boca(b, "sorriso"); bochechas(b); extra(b, "estrelas"); b.semPiscar = true; }
}
function criarTigela(a, k) {
  const raiz = new THREE.Group(), corpo = new THREE.Group(); raiz.add(corpo);
  const mat = new THREE.MeshPhysicalMaterial({ color: SOLAR, vertexColors: true, roughness: 0.36, clearcoat: 0.85, clearcoatRoughness: 0.14, sheen: 0.35, sheenRoughness: 0.6, sheenColor: new THREE.Color(SOLAR), emissive: SOLAR, emissiveIntensity: 0 });
  malha(T.geo, mat, corpo);
  const rosto = new THREE.Group(); corpo.add(rosto);
  const b = { k, n: k + 1, a, expr: a.expr, raiz, corpo, mat, rosto, olhos: [], extras: [], pessegos: [], rnd: semente(900 + k),
    p: new THREE.Vector3(0, 0, -6), alvoP: new THREE.Vector3(), rotY: 0, alvoRotY: 0, esc: 0.001, alvoEsc: 1, brilho: 0, alvoBrilho: 0,
    fase: k * 0.83, proxPiscar: 1.5 + k * 0.37, toque: -9, giro: -9, festa: false };
  montarRosto(b);
  b.sombra = malha(G.plano, M.sombra, raiz); b.sombra.rotation.x = -Math.PI / 2; b.sombra.scale.set(2.6, 2.6, 1); b.sombra.position.y = 0.004;
  b.anel = malha(G.anel, M.solar, raiz); b.anel.rotation.x = Math.PI / 2; b.anel.position.y = -0.02; b.anel.visible = false;
  for (let i = 0; i < 8; i++) { const p = malha(G.pessego, M.pessego, corpo); p.visible = false; b.pessegos.push({ m: p, t0: -9 }); }
  cena.add(raiz);
  return b;
}

// ---------------------------------------------------------------- cenário, luz e pós-produção
// Grelha de cor final (como um LUT de cinema): a luz pêssego sobre o azul nunca passa por violeta, rosa, amarelo nem verde.
// As cores da paleta ficam iguais; só as misturas proibidas são dobradas para o azul ou para o quente, com a saturação a apagar-se na dobra.
const TRAVA_PALETA = {
  name: "TravaPaleta",
  uniforms: { tDiffuse: { value: null }, vinheta: { value: 0.26 } },
  vertexShader: "varying vec2 vUv; void main() { vUv = uv; gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0); }",
  fragmentShader: `
uniform sampler2D tDiffuse; uniform float vinheta; varying vec2 vUv;
vec3 paraHSL(vec3 c) {
  float mx = max(max(c.r, c.g), c.b), mn = min(min(c.r, c.g), c.b), l = (mx + mn) * 0.5, d = mx - mn, h = 0.0, s = 0.0;
  if (d > 0.00001) {
    s = l > 0.5 ? d / (2.0 - mx - mn) : d / (mx + mn);
    if (mx == c.r) h = (c.g - c.b) / d + (c.g < c.b ? 6.0 : 0.0); else if (mx == c.g) h = (c.b - c.r) / d + 2.0; else h = (c.r - c.g) / d + 4.0;
    h *= 60.0;
  }
  return vec3(h, s, l);
}
float canal(float p, float q, float t) { t = fract(t); if (t < 1.0 / 6.0) return p + (q - p) * 6.0 * t; if (t < 0.5) return q; if (t < 2.0 / 3.0) return p + (q - p) * (2.0 / 3.0 - t) * 6.0; return p; }
vec3 deHSL(vec3 x) {
  float h = x.x / 360.0, s = x.y, l = x.z; if (s < 0.00001) return vec3(l);
  float q = l < 0.5 ? l * (1.0 + s) : l + s - l * s, p = 2.0 * l - q;
  return vec3(canal(p, q, h + 1.0 / 3.0), canal(p, q, h), canal(p, q, h - 1.0 / 3.0));
}
vec3 dobrar(vec3 x, float a, float b, float baixo, float cima) {
  if (x.x <= a || x.x >= b) return x;
  float m = (x.x - a) / (b - a), f = abs(m - 0.5) * 2.0;
  x.y *= f * f; x.x = m < 0.5 ? mix(a, baixo, m * 2.0) : mix(cima, b, (m - 0.5) * 2.0); return x;
}
void main() {
  vec4 t = texture2D(tDiffuse, vUv); vec3 x = paraHSL(clamp(t.rgb, 0.0, 1.0));
  x = dobrar(x, 236.0, 352.0, 226.0, 366.0);
  x = dobrar(x, 36.0, 190.0, 28.0, 198.0);
  x.x = mod(x.x, 360.0);
  vec3 r = deHSL(x);
  vec2 q = vUv - 0.5; r *= 1.0 - vinheta * smoothstep(0.42, 0.98, length(q) * 1.32);
  gl_FragColor = vec4(r, t.a);
}`
};
const FILME = {};
function iniciar3D() {
  renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, 1.75));
  renderer.setSize(innerWidth, innerHeight, false);
  renderer.toneMapping = THREE.ACESFilmicToneMapping; renderer.toneMappingExposure = 0.92;
  renderer.outputColorSpace = THREE.SRGBColorSpace;
  cena.background = new THREE.Color(ABISSAL);
  cena.fog = new THREE.FogExp2(ABISSAL, 0.05);
  const pmrem = new THREE.PMREMGenerator(renderer);
  cena.environment = pmrem.fromScene(new RoomEnvironment(), 0.04).texture; cena.environmentIntensity = 0.55;
  pmrem.dispose();
  prepararMateriais();
  const chave = new THREE.DirectionalLight(TITANIO, 1.5); chave.position.set(-3, 5, 4); cena.add(chave);
  const contra = new THREE.DirectionalLight(SOLAR, 2.4); contra.position.set(2.5, 2.8, -4); cena.add(contra);
  cena.add(new THREE.HemisphereLight(NEVOEIRO, ABISSAL, 0.4));
  const quente = new THREE.PointLight(SOLAR, 1.6, 9, 2); quente.position.set(0, 1.7, 2.2); cena.add(quente);
  chao = new THREE.Mesh(new THREE.CircleGeometry(26, 96), new THREE.MeshBasicMaterial({ map: texturaRadial([[0, "rgba(15,34,61,1)"], [0.35, "rgba(15,34,61,1)"], [1, "rgba(11,25,44,1)"]]) }));
  chao.rotation.x = -Math.PI / 2; cena.add(chao);
  const halo = new THREE.Mesh(G.plano, new THREE.MeshBasicMaterial({ map: texturaRadial([[0, "rgba(255,158,125,0.16)"], [0.4, "rgba(255,158,125,0.04)"], [1, "rgba(255,158,125,0)"]]), transparent: true, depthWrite: false }));
  halo.rotation.x = -Math.PI / 2; halo.scale.set(9, 9, 1); halo.position.set(0, 0.003, -0.4); chao.add(halo); halo.rotation.x = 0; halo.position.set(0, 0.4, 0.003);
  brilhoFundo = new THREE.Sprite(new THREE.SpriteMaterial({ map: texturaRadial([[0, "rgba(255,158,125,0.2)"], [0.35, "rgba(255,158,125,0.06)"], [1, "rgba(255,158,125,0)"]]), transparent: true, depthWrite: false, blending: THREE.AdditiveBlending, fog: false }));
  brilhoFundo.scale.set(9, 5, 1); brilhoFundo.position.set(0, 3.6, -14); brilhoFundo.material.opacity = 0.5; cena.add(brilhoFundo);
  sol = new THREE.Sprite(new THREE.SpriteMaterial({ map: texturaRadial([[0, "rgba(244,247,250,0.95)"], [0.2, "rgba(255,158,125,0.85)"], [0.55, "rgba(255,158,125,0.18)"], [1, "rgba(255,158,125,0)"]]), transparent: true, depthWrite: false, blending: THREE.AdditiveBlending, fog: false }));
  sol.scale.set(2.2, 2.2, 1); sol.position.set(0, 3.6, -14); sol.material.opacity = 0.8; cena.add(sol);
  const N = 260, pos = new Float32Array(N * 3), vel = new Float32Array(N), rp = semente(77);
  for (let i = 0; i < N; i++) { pos[i * 3] = (rp() - 0.5) * 16; pos[i * 3 + 1] = rp() * 7 - 0.5; pos[i * 3 + 2] = -1 - rp() * 11; vel[i] = 0.07 + rp() * 0.2; }
  const gp = new THREE.BufferGeometry(); gp.setAttribute("position", new THREE.BufferAttribute(pos, 3));
  particulas = new THREE.Points(gp, new THREE.PointsMaterial({ color: SOLAR, size: 0.07, map: texturaRadial([[0, "rgba(255,158,125,1)"], [0.4, "rgba(255,158,125,0.4)"], [1, "rgba(255,158,125,0)"]]), transparent: true, depthWrite: false, blending: THREE.AdditiveBlending, opacity: 0.9 }));
  particulas.userData.vel = vel; cena.add(particulas);
  D.atividades.forEach((a, k) => tigelas.push(criarTigela(a, k)));
  for (let i = 0; i < 48; i++) { const f = malha(G.faisca, M.solar); f.visible = false; cena.add(f); faiscas.push({ m: f, v: new THREE.Vector3(), vida: 0 }); }
  criarAdereços();
  composer = new EffectComposer(renderer);
  composer.addPass(new RenderPass(cena, camara));
  bloom = new UnrealBloomPass(new THREE.Vector2(innerWidth / 2, innerHeight / 2), 0.42, 0.45, 0.9);
  composer.addPass(bloom);
  composer.addPass(new OutputPass());
  composer.addPass(new ShaderPass(TRAVA_PALETA));
}
function retArredondado(w, h, r) {
  const s = new THREE.Shape(), x = -w / 2, y = -h / 2;
  s.moveTo(x + r, y); s.lineTo(x + w - r, y); s.quadraticCurveTo(x + w, y, x + w, y + r); s.lineTo(x + w, y + h - r); s.quadraticCurveTo(x + w, y + h, x + w - r, y + h);
  s.lineTo(x + r, y + h); s.quadraticCurveTo(x, y + h, x, y + h - r); s.lineTo(x, y + r); s.quadraticCurveTo(x, y, x + r, y); return s;
}
function criarAdereços() {
  const ext = (w, h, r, d) => new THREE.ExtrudeGeometry(retArredondado(w, h, r), { depth: d, bevelEnabled: true, bevelThickness: 0.02, bevelSize: 0.02, bevelSegments: 3, curveSegments: 10 });
  FILME.faisca = malha(new THREE.SphereGeometry(0.09, 20, 14), M.solar, cena);
  FILME.tel = new THREE.Group(); malha(ext(1.3, 2.3, 0.18, 0.06), M.vidro, FILME.tel); const aro = malha(ext(1.38, 2.38, 0.2, 0.02), M.solar, FILME.tel); aro.position.z = -0.03; aro.scale.set(1, 1, 0.5); cena.add(FILME.tel);
  FILME.cadeado = new THREE.Group(); malha(ext(0.46, 0.38, 0.07, 0.12), M.palpebra, FILME.cadeado); const arc = malha(new THREE.TorusGeometry(0.14, 0.038, 12, 32, Math.PI), M.titanio, FILME.cadeado); arc.position.y = 0.19; const fe = malha(G.disco, M.tinta, FILME.cadeado); fe.scale.setScalar(0.05); fe.position.set(0, -0.01, 0.15); cena.add(FILME.cadeado);
  // documento em vidro escuro com aro pêssego (como o telemóvel): nada de folha branca a rebentar de luz
  FILME.doc = new THREE.Group(); const fd = new THREE.Group(); fd.rotation.z = -0.05; FILME.doc.add(fd);
  malha(ext(1.45, 1.85, 0.12, 0.03), M.docVidro, fd); const aroD = malha(ext(1.53, 1.93, 0.15, 0.02), M.solar, fd); aroD.position.z = -0.03; aroD.scale.set(1, 1, 0.5);
  for (let i = 0; i < 6; i++) { const l = malha(new THREE.BoxGeometry(i === 5 ? 0.5 : 1.0, 0.045, 0.012), i === 5 ? M.solar : M.linha, fd); l.position.set(i === 5 ? -0.25 : 0, 0.62 - i * 0.22, 0.062); }
  cena.add(FILME.doc);
  FILME.carimbo = new THREE.Group(); const ci = malha(new THREE.CylinderGeometry(0.42, 0.42, 0.08, 48), M.selo, FILME.carimbo); ci.rotation.x = Math.PI / 2;
  const vis = new THREE.CurvePath(); vis.add(new THREE.LineCurve3(new THREE.Vector3(-0.2, 0.02, 0), new THREE.Vector3(-0.05, -0.13, 0))); vis.add(new THREE.LineCurve3(new THREE.Vector3(-0.05, -0.13, 0), new THREE.Vector3(0.22, 0.16, 0)));
  const ck = malha(new THREE.TubeGeometry(vis, 32, 0.045, 8, false), M.tinta, FILME.carimbo); ck.position.z = 0.05; cena.add(FILME.carimbo);
  const pl = new THREE.BoxGeometry(4.2, 0.13, 1.3); pl.translate(2.1, 0, 0); FILME.placa = malha(pl, M.solar, cena);
  Object.values(FILME).forEach((o) => { o.visible = false; });
}

// ---------------------------------------------------------------- disposições (Família, Criança, Filme, Retrato)
let modo = "familia", foco = 0, tSim = 0, filmeT0 = 0, cenaAtual = -1;
const cheias = D.atividades.map(() => 0);
function alvosFamilia() {
  const ret = camara.aspect < 0.8, Rr = 4.4;
  tigelas.forEach((b) => {
    let d = b.k - foco; if (d > 4) d -= 8; if (d < -3) d += 8;
    const a = d * 0.62;
    b.alvoP.set(Math.sin(a) * Rr, 0, Math.cos(a) * Rr - Rr); b.alvoRotY = a * 0.85; b.alvoEsc = d === 0 ? 1 : 0.8; b.alvoBrilho = d === 0 ? 0.1 : 0;
    b.anel.visible = false; b.sombra.visible = true;
  });
  const mv = Math.tan(THREE.MathUtils.degToRad(camara.fov / 2)), dist = Math.max(5.2, (ret ? 1.75 : 3.1) / (mv * camara.aspect));
  alvoCamP.set(0, 1.25 + dist * 0.12, dist); alvoCamO.set(0, ret ? 0.95 : 0.55, -0.4);
  if (chao) chao.visible = true;
}
function alvosCrianca() {
  const ret = camara.aspect < 1, cols = ret ? 2 : 4, rows = 8 / cols, sx = 2.15, sy = 1.6;
  tigelas.forEach((b) => {
    const c = b.k % cols, r = Math.floor(b.k / cols);
    b.alvoP.set((c - (cols - 1) / 2) * sx, ((rows - 1) / 2 - r) * sy, 0); b.alvoRotY = 0; b.alvoEsc = 0.86; b.alvoBrilho = cheias[b.k] >= b.n ? 0.4 : 0;
    b.anel.visible = true; b.sombra.visible = false;
  });
  const mv = Math.tan(THREE.MathUtils.degToRad(camara.fov / 2)), hh = rows * sy / 2 + 0.5, hw = cols * sx / 2 + 0.3;
  const dist = Math.max(hh / mv, hw / (mv * camara.aspect));
  alvoCamP.set(0, 0.42, dist); alvoCamO.set(0, 0.42, 0);
  if (chao) chao.visible = false;
}
function alvosRetrato() {
  tigelas.forEach((b) => { b.alvoEsc = b.k === RETRATO ? 1 : 0; b.alvoP.set(0, 0, 0); b.alvoRotY = 0; b.sombra.visible = true; b.anel.visible = false; });
  alvoCamP.set(0, 0.92, 3.35); alvoCamO.set(0, 0.48, 0);
}
function disposicao() { if (modo === "familia") alvosFamilia(); else if (modo === "crianca") alvosCrianca(); else if (modo === "retrato") alvosRetrato(); }

// O filme: 12 cenas de 10 s, desenhadas com as mesmas personagens (legendas do MANIFESTO-MISSAO.md).
function filmeEm(tt) {
  const i = Math.min(11, Math.floor(tt / 10)), u = tt - i * 10, c = D.cenas[i];
  if (i !== cenaAtual) { cenaAtual = i; tigelas.forEach((b) => { b.pessegos.forEach((p) => { p.m.visible = false; }); b.chuva = false; }); }
  Object.values(FILME).forEach((o) => { o.visible = false; });
  const so = (lista, f) => tigelas.forEach((b) => { if (lista.indexOf(b.k) < 0) { b.alvoEsc = 0; } else f(b, lista.indexOf(b.k)); });
  const fila = (esc, z, entrada) => tigelas.forEach((b) => { b.alvoP.set((b.k - 3.5) * 1.22, 0, z); b.alvoRotY = 0; b.alvoEsc = entrada && u < 0.3 + b.k * 0.32 ? 0 : esc; b.sombra.visible = true; b.anel.visible = false; });
  tigelas.forEach((b) => { b.alvoBrilho = 0; });
  if (chao) chao.visible = true;
  if (c.tipo === "uma") { so(c.tigelas, (b) => { b.alvoP.set(0, 0, 0); b.alvoEsc = suave(0.2, 1.1, u) * 1.05; b.alvoRotY = 0.22 * Math.sin(u * 0.5); b.sombra.visible = true; }); alvoCamP.set(0, 1.3 - 0.25 * suave(0, 10, u), 6.4 - 2.2 * suave(0, 10, u)); alvoCamO.set(0, 0.5, 0); }
  if (c.tipo === "duas") {
    so(c.tigelas, (b, j) => { b.alvoP.set(j ? 1.3 : -1.3, 0, 0); b.alvoRotY = j ? -0.35 : 0.35; b.alvoEsc = 1; b.sombra.visible = true; if (j && u > 3.6) b.alvoBrilho = 0.45 + 0.4 * Math.sin((u - 3.6) * 4); });
    const f = suave(1.2, 3.6, u); FILME.faisca.visible = u > 1.1 && u < 3.7; FILME.faisca.position.set(-0.75 + 1.5 * f, 0.95 + 0.55 * Math.sin(f * Math.PI), 0.25);
    alvoCamP.set(0, 1.25, 5.8); alvoCamO.set(0, 0.5, 0);
  }
  if (c.tipo === "fila" || c.tipo === "chuva" || c.tipo === "acender") {
    fila(0.64, 0, c.tipo === "fila");
    if (c.tipo === "chuva") tigelas.forEach((b) => { if (!b.chuva && u > 1.2 + b.k * 0.45) { b.chuva = true; b.pessegos[0].m.visible = true; b.pessegos[0].t0 = tSim; b.toque = tSim + 0.55; } });
    if (c.tipo === "acender") tigelas.forEach((b) => { b.alvoBrilho = u > 1 + b.k * 0.6 ? 0.95 : 0.04; });
    if (c.tipo === "chuva") { alvoCamP.set(0, 3.4, 8.2); alvoCamO.set(0, 0.15, 0); } else { alvoCamP.set(0, 1.55, 9.2 - 0.8 * suave(0, 10, u)); alvoCamO.set(0, 0.35, 0); }
  }
  if (c.tipo === "contador") { fila(0.5, -1.6, false); alvoCamP.set(0, 1.4, 8.4); alvoCamO.set(0, 0.8, 0); }
  if (c.tipo === "telemovel") {
    FILME.tel.visible = true; FILME.tel.position.set(-0.85, 1.2, 0); FILME.tel.rotation.y = 0.18;
    so(c.tigelas, (b, j) => { b.alvoP.set(-1.12 + (j % 2) * 0.55, 1.5 - Math.floor(j / 2) * 0.75, 0.18); b.alvoRotY = 0.18; b.alvoEsc = 0.32; b.sombra.visible = false; });
    FILME.cadeado.visible = u > 1.3; const e = suave(1.3, 2.3, u); FILME.cadeado.position.set(1.25, 1.05 + (1 - e) * 0.8, 0.3); FILME.cadeado.scale.setScalar(Math.max(0.001, e)); FILME.cadeado.rotation.y = -0.3 + 0.1 * Math.sin(u);
    alvoCamP.set(0.15, 1.35, 5.4); alvoCamO.set(0.15, 1.1, 0);
  }
  if (c.tipo === "selo") {
    so([], () => 0); FILME.doc.visible = true; FILME.doc.position.set(0, 1.2, 0); FILME.doc.rotation.set(-0.08, 0.12, 0);
    const e = suave(1.4, 1.9, u); FILME.carimbo.visible = u > 1.2; FILME.carimbo.position.set(0.38, 0.88 + (1 - e) * 1.3, 0.12 + (1 - e) * 0.9); FILME.carimbo.scale.setScalar(1 + (1 - e) * 0.7); FILME.carimbo.rotation.set(-0.08, 0.12, -0.14);
    alvoCamP.set(0, 1.3, 4.7); alvoCamO.set(0, 1.1, 0);
  }
  if (c.tipo === "camada") {
    so(c.tigelas, (b) => { b.alvoP.set(-1.7, 0.2, 0); b.alvoRotY = 0.3; b.alvoEsc = 1; b.sombra.visible = false; });
    FILME.placa.visible = true; FILME.placa.position.set(-2.6, 0.13, 0); FILME.placa.scale.set(Math.max(0.001, suave(1.4, 3.6, u)), 1, 1);
    alvoCamP.set(0, 1.5, 6.4); alvoCamO.set(0, 0.5, 0);
  }
  if (c.tipo === "marca") { so([], () => 0); alvoCamP.set(0, 1.4, 5.5); alvoCamO.set(0, 1.0, 0); }
  // por cima: legenda, contador, marca e régua
  const leg = $("legenda"), op = c.tipo === "marca" ? 0 : suave(0.5, 1.3, u) * (1 - suave(9.1, 9.8, u));
  leg.textContent = c.legenda; leg.style.opacity = op.toFixed(3);
  $("contador").hidden = c.tipo !== "contador"; $("contador").textContent = Math.round((c.ate || 0) * clamp((u - 0.8) / 5.2, 0, 1)) + " / " + (c.ate || 0);
  const mf = $("marca-filme"); mf.hidden = c.tipo !== "marca"; mf.style.opacity = suave(0.3, 1.6, u).toFixed(3);
  $("f-lema").textContent = c.lema || ""; $("f-nota").textContent = c.nota || "";
  $("f-cena").textContent = "Cena " + (i + 1) + "/12 · " + c.inicio + "–" + c.fim;
  $("f-prog").style.width = (clamp(tt / 120, 0, 1) * 100).toFixed(2) + "%";
  if (brilhoFundo) brilhoFundo.material.opacity = c.tipo === "marca" ? 0.9 : 0.5;
  if (tt >= 120 && !QUADROS) mudarModo("familia");
}

// ---------------------------------------------------------------- ciclo
function explodir(b) {
  const r = b.rnd, c = new THREE.Vector3(); b.raiz.getWorldPosition(c); c.y += 0.8 * b.esc;
  let n = 0;
  for (const f of faiscas) { if (f.vida > 0) continue; f.vida = 1; f.m.visible = true; f.m.position.copy(c); f.v.set((r() - 0.5) * 3.2, 1.4 + r() * 2.4, (r() - 0.5) * 2); if (++n >= 24) break; }
}
function passo(dt) {
  tSim += dt;
  if (modo === "filme") filmeEm(tSim - filmeT0);
  const k = 1 - Math.exp(-dt * 6.5);
  ponteiroSuave.lerp(ponteiro, 1 - Math.exp(-dt * 4));
  for (const b of tigelas) {
    b.p.lerp(b.alvoP, k); b.rotY += (b.alvoRotY - b.rotY) * k; b.esc += (b.alvoEsc - b.esc) * k; b.brilho += (b.alvoBrilho - b.brilho) * k;
    const flut = Math.sin(tSim * 1.4 + b.fase);
    b.raiz.position.copy(b.p); b.raiz.position.y += (modo === "crianca" ? 0.07 : 0.025) * flut;
    b.raiz.rotation.y = b.rotY + 0.05 * Math.sin(tSim * 0.9 + b.fase);
    b.raiz.scale.setScalar(Math.max(0.0001, b.esc)); b.raiz.visible = b.esc > 0.02;
    const ts = tSim - b.toque, sq = ts >= 0 && ts < 1.2 ? Math.exp(-ts * 5) * Math.cos(ts * 18) : 0;
    b.corpo.scale.set(1 + 0.1 * sq, 1 - 0.14 * sq, 1 + 0.1 * sq);
    const tg = tSim - b.giro; b.corpo.rotation.y = tg >= 0 && tg < 0.9 ? suave(0, 0.9, tg) * Math.PI * 2 : 0;
    b.mat.emissiveIntensity = 0.02 + b.brilho * 0.6;
    b.anel.material === M.solar && (b.anel.scale.setScalar(1 + 0.04 * flut));
    if (!b.semPiscar) {
      const tb = tSim - b.proxPiscar; let s = 1;
      if (tb >= 0 && tb < 0.16) s = 1 - Math.sin(tb / 0.16 * Math.PI) * 0.9; else if (tb >= 0.16) b.proxPiscar = tSim + 2.4 + b.rnd() * 3.2;
      b.olhos.forEach((o) => { o.g.scale.y = s; });
    }
    b.olhos.forEach((o) => { o.pup.position.x = o.base[0] + clamp(ponteiroSuave.x, -1, 1) * 0.022; o.pup.position.y = o.base[1] + clamp(ponteiroSuave.y, -1, 1) * 0.016; });
    b.pessegos.forEach((pp, i) => { if (!pp.m.visible) return; const u = clamp((tSim - pp.t0) / 0.7, 0, 1), L = LUGARES[i]; pp.m.position.set(L[0], L[1] + (1 - salto(u)) * 2.3, L[2]); pp.m.rotation.y = i * 1.3; });
    b.extras.forEach((o) => o.anima(tSim));
  }
  for (const f of faiscas) { if (f.vida <= 0) continue; f.vida -= dt * 0.85; f.v.y -= 3.2 * dt; f.m.position.addScaledVector(f.v, dt); f.m.scale.setScalar(Math.max(0.001, f.vida)); if (f.vida <= 0) f.m.visible = false; }
  if (particulas) { const a = particulas.geometry.attributes.position, v = particulas.userData.vel; for (let i = 0; i < v.length; i++) { let y = a.getY(i) + v[i] * dt; if (y > 6.6) y = -0.4; a.setY(i, y); a.setX(i, a.getX(i) + Math.sin(tSim * 0.5 + i) * 0.0015); } a.needsUpdate = true; }
  const kc = 1 - Math.exp(-dt * 3.2);
  camP.lerp(alvoCamP, kc); camO.lerp(alvoCamO, kc);
  camara.position.set(camP.x + ponteiroSuave.x * 0.28, camP.y + ponteiroSuave.y * 0.14, camP.z); camara.lookAt(camO);
}
function desenhar() { if (!COM3D) return; composer.render(); projetar(); }
const vA = new THREE.Vector3(), vB = new THREE.Vector3();
function projetar() {
  const W = innerWidth, H = innerHeight;
  cena.updateMatrixWorld();
  tigelas.forEach((b) => {
    const bt = botoes[b.k];
    if (!b.raiz.visible || modo === "filme" || modo === "retrato") { bt.style.visibility = "hidden"; return; }
    b.raiz.localToWorld(vA.set(0, 0.45, 0)).project(camara); b.raiz.localToWorld(vB.set(1.08, 0.45, 0)).project(camara);
    const cx = (vA.x + 1) / 2 * W, cy = (1 - vA.y) / 2 * H, r = Math.max(28, Math.abs(vB.x - vA.x) / 2 * W);
    bt.style.visibility = "visible"; bt.style.left = (cx - r).toFixed(1) + "px"; bt.style.top = (cy - r * 0.95).toFixed(1) + "px";
    bt.style.width = (2 * r).toFixed(1) + "px"; bt.style.height = (1.9 * r).toFixed(1) + "px";
  });
}
let tReal = null;
function ciclo(ms) {
  const s = ms / 1000, dt = tReal == null ? 1 / 60 : Math.min(0.05, s - tReal); tReal = s;
  passo(dt); desenhar(); requestAnimationFrame(ciclo);
}
// Tempo dado de fora, sempre em passos iguais (capturas e vídeo saem sempre iguais).
window.__quadro = function (alvo) { const h = 1 / 48; while (tSim + h / 2 < alvo) passo(h); desenhar(); return modo === "filme" ? cenaAtual : -1; };

// ---------------------------------------------------------------- interface
const ICONES = {
  livro: '<path d="M12 7c-2-1.4-4.6-2-7.4-2v12c2.8 0 5.4.6 7.4 2 2-1.4 4.6-2 7.4-2V5c-2.8 0-5.4.6-7.4 2zM12 7v12"/>',
  pergunta: '<path d="M9 9a3 3 0 1 1 4.2 2.8c-.8.4-1.2 1.1-1.2 1.9v.6"/><path d="M12 17.6v.4"/>',
  estrela: '<path d="m12 3 2.6 5.3 5.9.9-4.3 4.1 1 5.8L12 16.4 6.8 19.1l1-5.8-4.3-4.1 5.9-.9z"/>',
  filme: '<path d="M8.5 5.8v12.4L18.5 12z"/>',
  contas: '<path d="M12 5v14M5 12h14"/>',
  musica: '<path d="M9 17V6.5l10-2.2v10.5"/><circle cx="6.7" cy="17.2" r="2.3"/><circle cx="16.7" cy="15" r="2.3"/>',
  globo: '<circle cx="12" cy="12" r="8.2"/><path d="M3.8 12h16.4M12 3.8c2.6 2.6 2.6 13.8 0 16.4M12 3.8c-2.6 2.6-2.6 13.8 0 16.4"/>',
  bussola: '<circle cx="12" cy="12" r="8.2"/><path d="m15.5 8.5-2.2 4.8-4.8 2.2 2.2-4.8z"/>',
  tigela: '<path d="M3.5 11h17a8.5 7.5 0 0 1-17 0z"/><path d="M9.5 20.5h5"/><circle cx="12" cy="7" r="2.3"/>',
  portais: '<rect x="4" y="4" width="6.5" height="6.5" rx="1.6"/><rect x="13.5" y="4" width="6.5" height="6.5" rx="1.6"/><rect x="4" y="13.5" width="6.5" height="6.5" rx="1.6"/><rect x="13.5" y="13.5" width="6.5" height="6.5" rx="1.6"/>',
  seta: '<path d="m10 6 6 6-6 6"/>', voltar: '<path d="m14 6-6 6 6 6"/>', fechar: '<path d="M6 6l12 12M18 6 6 18"/>',
  toque: '<circle cx="12" cy="12" r="3.2"/><circle cx="12" cy="12" r="7.5"/>', impressao: '<path d="M8 11a4 4 0 0 1 8 0v2c0 2-.6 4-1.6 5.6M12 11v3c0 2.4-.9 4.6-2.4 6.2M5.2 9.6A7 7 0 0 1 18.8 10v2.6"/>'
};
const ico = (n) => '<svg viewBox="0 0 24 24" aria-hidden="true" focusable="false">' + (ICONES[n] || "") + "</svg>";
const botoes = [];
function construirUI() {
  document.querySelectorAll("[data-ico]").forEach((e) => { e.insertAdjacentHTML("afterbegin", ico(e.dataset.ico)); });
  const sel = $("sel-lingua");
  LINGS.forEach((l) => { const o = document.createElement("option"); o.value = l.c; o.textContent = l.nome; o.dir = l.dir; sel.appendChild(o); });
  sel.addEventListener("change", () => { lingua = sel.value; estado.lang = lingua; guardar(); aplicar(); });
  const zona = $("tigelas");
  D.atividades.forEach((a, k) => {
    const b = document.createElement("button"); b.type = "button"; b.className = "tig"; b.dataset.k = String(k);
    b.innerHTML = '<span class="tig-ico">' + ico(a.simbolo) + '</span><span class="pontos">' + "<i></i>".repeat(k + 1) + '</span><span class="bem"></span>';
    b.addEventListener("click", () => { if (modo === "crianca") tocar(k); else if (modo === "familia") focar(k); });
    zona.appendChild(b); botoes.push(b);
  });
  $("b-ant").addEventListener("click", () => focar((foco + 7) % 8));
  $("b-seg").addEventListener("click", () => focar((foco + 1) % 8));
  $("b-entrar").addEventListener("click", () => { if (temPin()) entrar(); else abrirPin("definir"); });
  $("b-sair").addEventListener("click", () => { if (temPin()) abrirPin("desbloquear"); else sair(); });
  $("b-filme").addEventListener("click", iniciarFilme);
  $("b-fechar").addEventListener("click", () => mudarModo("familia"));
  $("b-cancelar").addEventListener("click", fecharPin);
  $("b-denovo").addEventListener("click", recomecar);
  $("b-bio").addEventListener("click", registarBio);
  $("b-pin-bio").addEventListener("click", usarBio);
  $("entrada").href = D.entrada;
  teclado();
  window.addEventListener("pointermove", (e) => { ponteiro.set(e.clientX / innerWidth * 2 - 1, -(e.clientY / innerHeight * 2 - 1)); }, { passive: true });
}
function focar(k) { foco = k; disposicao(); aplicar(); const b = tigelas[k]; if (b) b.toque = tSim; }
function rotulo(k) { return t("tigela") + " " + (k + 1) + ": " + cheias[k] + " " + t("de") + " " + (k + 1); }
function atualizarBotao(k) {
  const bt = botoes[k], n = k + 1, c = cheias[k], cheia = c >= n;
  bt.querySelectorAll(".pontos i").forEach((e, i) => { e.className = i < c ? "cheio" : ""; });
  bt.classList.toggle("cheia", cheia); bt.dataset.cheia = cheia ? "1" : "0";
  bt.querySelector(".bem").textContent = cheia && modo === "crianca" ? t("muito_bem") : "";
  bt.setAttribute("aria-label", modo === "crianca" ? rotulo(k) : m("fam." + D.atividades[k].chave + ".t"));
}
function aplicar() {
  const info = LINGS.find((l) => l.c === lingua) || LINGS[0];
  document.documentElement.lang = info.c === "pt" ? "pt-PT" : info.c;
  document.documentElement.dir = info.dir;
  document.querySelectorAll("[data-t]").forEach((e) => { e.textContent = t(e.dataset.t); });
  document.querySelectorAll("[data-m]").forEach((e) => { e.textContent = m(e.dataset.m); });
  document.querySelectorAll(".marca-ia").forEach((e) => { e.hidden = !info.ia; }); // tradução por IA: a marca «por rever» fica até haver revisão humana
  $("sel-lingua").value = lingua;
  const a = D.atividades[foco];
  $("c-titulo").textContent = m("fam." + a.chave + ".t"); $("c-desc").textContent = m("fam." + a.chave + ".d");
  $("c-abrir").href = a.href; $("c-ico").innerHTML = ico(a.simbolo);
  $("c-abrir").setAttribute("aria-label", m("fam." + a.chave + ".t"));
  $("b-fechar").setAttribute("aria-label", t("fechar"));
  D.atividades.forEach((x, k) => atualizarBotao(k));
  if (!$("pin").hidden) tituloPin();
}
function mudarModo(novo) {
  if (modo === "crianca" && novo !== "crianca") document.body.classList.remove("modo-crianca");
  modo = novo; document.body.dataset.modo = novo;
  $("familia").hidden = novo !== "familia"; $("crianca").hidden = novo !== "crianca"; $("filme").hidden = novo !== "filme";
  $("topo").hidden = novo !== "familia";
  if (novo !== "filme") { Object.values(FILME).forEach((o) => { o.visible = false; }); cenaAtual = -1; tigelas.forEach((b) => b.pessegos.forEach((p, i) => { p.m.visible = novo === "crianca" && i < cheias[b.k]; })); }
  disposicao(); aplicar();
}
function iniciarFilme() { filmeT0 = tSim; cenaAtual = -1; mudarModo("filme"); }

// ---------------------------------------------------------------- jogo do Modo Criança
function tocar(k) {
  const b = tigelas[k];
  if (cheias[k] < k + 1) { const i = cheias[k]++; if (b) { b.pessegos[i].m.visible = true; b.pessegos[i].t0 = tSim; } }
  if (b) b.toque = tSim;
  if (cheias[k] >= k + 1 && b && !b.festa) { b.festa = true; b.giro = tSim + 0.55; b.alvoBrilho = 0.4; explodir(b); }
  atualizarBotao(k);
  if (cheias.every((c, i) => c >= i + 1)) $("final").hidden = false;
}
function recomecar() {
  cheias.fill(0); $("final").hidden = true;
  tigelas.forEach((b) => { b.festa = false; b.alvoBrilho = 0; b.pessegos.forEach((p) => { p.m.visible = false; }); });
  D.atividades.forEach((x, k) => atualizarBotao(k));
}

// ---------------------------------------------------------------- tranca de adulto (PIN e biometria)
const pin = { modo: null, buf: "", primeiro: null };
function emCrianca() { return document.body.classList.contains("modo-crianca"); }
function entrar() {
  document.body.classList.add("modo-crianca");
  estado.crianca = true; guardar(); casaGravar(CASA_MODO, "1");
  try { history.pushState({ konfirmu: "crianca" }, "", location.href); } catch (e) { /* sem histórico */ }
  try { const el = document.documentElement; if (el.requestFullscreen) { const r = el.requestFullscreen(); if (r && r.catch) r.catch(() => {}); } } catch (e) { /* recusado */ }
  recomecar(); mudarModo("crianca");
}
function sair() {
  document.body.classList.remove("modo-crianca");
  estado.crianca = false; guardar(); casaGravar(CASA_MODO, null);
  try { if (document.fullscreenElement && document.exitFullscreen) { const r = document.exitFullscreen(); if (r && r.catch) r.catch(() => {}); } } catch (e) { /* nada */ }
  mudarModo("familia"); mostrarBio();
}
window.addEventListener("popstate", () => { if (emCrianca()) { try { history.pushState({ konfirmu: "crianca" }, "", location.href); } catch (e) { /* nada */ } avisar(t("pede_adulto")); } });
document.addEventListener("contextmenu", (ev) => { if (emCrianca()) ev.preventDefault(); });
document.addEventListener("keydown", (ev) => {
  if (!$("pin").hidden) {
    if (/^[0-9]$/.test(ev.key)) { premir(ev.key); ev.preventDefault(); } else if (ev.key === "Backspace") { apagarDigito(); ev.preventDefault(); }
    else if (ev.key === "Enter") { confirmarPin(); ev.preventDefault(); } else if (ev.key === "Escape") { fecharPin(); ev.preventDefault(); }
    return;
  }
  if (modo === "familia" && (ev.key === "ArrowRight" || ev.key === "ArrowLeft")) focar((foco + (ev.key === "ArrowRight") * 2 + 7) % 8);
});
let tempoAviso = 0;
function avisar(txt) { const a = $("aviso"); a.textContent = txt; a.hidden = false; clearTimeout(tempoAviso); tempoAviso = setTimeout(() => { a.hidden = true; }, 2600); }
function hex(bytes) { return Array.prototype.map.call(bytes, (x) => (x < 16 ? "0" : "") + x.toString(16)).join(""); }
function aleatorio(n) { const b = new Uint8Array(n); crypto.getRandomValues(b); return b; }
function hashPin(sal, d) {
  const txt = sal + ":" + d;
  if (window.crypto && crypto.subtle && window.TextEncoder) return crypto.subtle.digest("SHA-256", new TextEncoder().encode(txt)).then((buf) => hex(new Uint8Array(buf)));
  return Promise.resolve(sha256js(txt));
}
// Tranca comum da casa (ordem do David, 28-11-2026, 04:25: «Girafinhas 3D com fechadura PIN comum da casa»).
// O PIN de adulto é um só em toda a app: fica em «konfirmu.tranca», no formato de assets/konfirmu-2040.js
// (PBKDF2-SHA-256, sal de 16 bytes, 150 000 voltas; o PIN nunca se guarda), com n = número de algarismos.
// O Modo Criança também é um só: «konfirmu.modoCrianca» = "1". Um PIN antigo só deste portal confere uma vez
// e passa logo para a tranca comum. Sem WebCrypto (endereço sem https), fica a tranca antiga deste portal.
const CASA_TRANCA = "konfirmu.tranca", CASA_MODO = "konfirmu.modoCrianca";
function casaLer(k) { try { return localStorage.getItem(k); } catch (e) { return null; } }
function casaGravar(k, v) { try { if (v === null) localStorage.removeItem(k); else localStorage.setItem(k, v); } catch (e) { /* sem armazenamento */ } }
function trancaCasa() { try { const c = JSON.parse(casaLer(CASA_TRANCA) || "null"); return c && c.v === 1 && c.sal && c.h ? c : null; } catch (e) { return null; } }
function temPin() { return !!(trancaCasa() || estado.pin); }
function casaEmCrianca() { return casaLer(CASA_MODO) === "1"; }
function b64(u) { return btoa(String.fromCharCode.apply(null, u)); }
function deb64(s) { const b = atob(s), u = new Uint8Array(b.length); for (let i = 0; i < b.length; i++) u[i] = b.charCodeAt(i); return u; }
function derivarCasa(d, sal, voltas) {
  if (!window.crypto || !crypto.subtle || !window.TextEncoder) return Promise.reject(new Error("sem-cripto"));
  return crypto.subtle.importKey("raw", new TextEncoder().encode(d), "PBKDF2", false, ["deriveBits"])
    .then((k) => crypto.subtle.deriveBits({ name: "PBKDF2", hash: "SHA-256", salt: sal, iterations: voltas }, k, 256))
    .then((b) => new Uint8Array(b));
}
function iguaisCasa(a, b) { if (a.length !== b.length) return false; let x = 0; for (let i = 0; i < a.length; i++) x |= a[i] ^ b[i]; return x === 0; }
function gravarTrancaCasa(d) {
  const sal = aleatorio(16), voltas = 150000, antiga = trancaCasa();
  return derivarCasa(d, sal, voltas).then((h) => {
    casaGravar(CASA_TRANCA, JSON.stringify({ v: 1, sal: b64(sal), voltas, h: b64(h), cred: antiga ? antiga.cred : null, n: d.length }));
  });
}
function conferirPin(d) {
  const c = trancaCasa();
  if (c) return derivarCasa(d, deb64(c.sal), c.voltas).then((h) => iguaisCasa(h, deb64(c.h)));
  if (estado.pin) return hashPin(estado.pin.sal, d).then((h) => {
    if (h !== estado.pin.hash) return false;
    return gravarTrancaCasa(d).then(() => { delete estado.pin; guardar(); return true; }, () => true);
  });
  return Promise.resolve(false);
}
function teclado() {
  const tk = $("teclado");
  ["1", "2", "3", "4", "5", "6", "7", "8", "9", "apagar", "0", "ok"].forEach((k) => {
    const b = document.createElement("button"); b.type = "button"; b.className = "tecla" + (k === "ok" ? " ok" : "");
    if (k === "apagar") { b.dataset.t = "apagar"; b.addEventListener("click", apagarDigito); }
    else if (k === "ok") { b.dataset.t = "ok"; b.addEventListener("click", confirmarPin); }
    else { b.textContent = k; b.dataset.d = k; b.addEventListener("click", () => premir(k)); }
    tk.appendChild(b);
  });
}
function pinos() { const p = $("pinos"); p.textContent = ""; for (let i = 0; i < Math.max(4, pin.buf.length); i++) { const e = document.createElement("i"); if (i < pin.buf.length) e.className = "cheio"; p.appendChild(e); } }
function tituloPin() { $("pin-titulo").textContent = t(pin.modo === "definir" ? "definir_pin" : pin.modo === "confirmar" ? "confirmar_pin" : "desbloquear"); }
function abrirPin(md) {
  pin.modo = md; pin.buf = ""; tituloPin(); pinos(); $("pin-erro").textContent = "";
  $("b-pin-bio").hidden = !(md === "desbloquear" && estado.cred && bioPossivel());
  $("pin").hidden = false; if (md === "desbloquear") mostrarBloqueio();
  const p1 = $("teclado").querySelector(".tecla"); if (p1) p1.focus();
}
function fecharPin() { $("pin").hidden = true; pin.modo = null; pin.buf = ""; clearTimeout(relogio); }
let relogio = 0;
function bloqueado() { return !!estado.bloqueio && Date.now() < estado.bloqueio; }
function mostrarBloqueio() {
  clearTimeout(relogio);
  if (!bloqueado()) { $("teclado").classList.remove("parado"); return; }
  $("pin-erro").textContent = t("pede_adulto") + " · " + Math.ceil((estado.bloqueio - Date.now()) / 1000) + " s";
  $("teclado").classList.add("parado"); relogio = setTimeout(mostrarBloqueio, 1000);
}
function premir(d) { if (bloqueado()) return; if (pin.buf.length < 6) { pin.buf += d; pinos(); } }
function apagarDigito() { pin.buf = pin.buf.slice(0, -1); pinos(); }
function erroPin(k) { $("pin-erro").textContent = t(k); }
function confirmarPin() {
  const d = pin.buf;
  if (pin.modo === "desbloquear" && bloqueado()) { mostrarBloqueio(); return; }
  if (d.length < 4) { erroPin("pin_curto"); return; }
  if (pin.modo === "definir") { pin.primeiro = d; abrirPin("confirmar"); return; }
  if (pin.modo === "confirmar") {
    if (d !== pin.primeiro) { pin.primeiro = null; abrirPin("definir"); erroPin("pin_diferente"); return; }
    gravarTrancaCasa(d).then(() => { delete estado.pin; guardar(); pin.primeiro = null; fecharPin(); entrar(); }, () => {
      const sal = hex(aleatorio(16));
      hashPin(sal, d).then((h) => { estado.pin = { sal, hash: h }; guardar(); pin.primeiro = null; fecharPin(); entrar(); });
    });
    return;
  }
  if (pin.modo === "desbloquear") {
    conferirPin(d).then((ok) => {
      if (ok) { estado.falhas = 0; guardar(); fecharPin(); sair(); return; }
      pin.buf = ""; pinos(); estado.falhas = (estado.falhas || 0) + 1;
      if (estado.falhas >= 5) { estado.falhas = 0; estado.bloqueio = Date.now() + 30000; }
      guardar(); if (bloqueado()) mostrarBloqueio(); else erroPin("pin_errado");
    }).catch(() => { pin.buf = ""; pinos(); erroPin("pin_errado"); });
  }
}
function bioPossivel() { return !!(window.PublicKeyCredential && window.isSecureContext && location.protocol === "https:"); }
function b64url(buf) { return btoa(String.fromCharCode.apply(null, new Uint8Array(buf))).replace(/\+/g, "-").replace(/\//g, "_").replace(/=+$/, ""); }
function deb64url(s) { s = s.replace(/-/g, "+").replace(/_/g, "/"); while (s.length % 4) s += "="; const b = atob(s), u = new Uint8Array(b.length); for (let i = 0; i < b.length; i++) u[i] = b.charCodeAt(i); return u; }
function mostrarBio() { $("b-bio").hidden = !(bioPossivel() && temPin() && !estado.cred); }
function registarBio() {
  navigator.credentials.create({ publicKey: { rp: { name: "Konfirmu" }, user: { id: aleatorio(16), name: "familia", displayName: "Família" }, challenge: aleatorio(32),
    pubKeyCredParams: [{ type: "public-key", alg: -7 }, { type: "public-key", alg: -257 }], authenticatorSelection: { authenticatorAttachment: "platform", userVerification: "required" }, timeout: 60000 } })
    .then((cr) => { estado.cred = b64url(cr.rawId); guardar(); mostrarBio(); }).catch(() => avisar(t("bio_falhou")));
}
function usarBio() {
  navigator.credentials.get({ publicKey: { challenge: aleatorio(32), allowCredentials: [{ type: "public-key", id: deb64url(estado.cred) }], userVerification: "required", timeout: 60000 } })
    .then(() => { fecharPin(); sair(); }).catch(() => erroPin("bio_falhou"));
}
// SHA-256 em JavaScript simples, para aparelhos sem crypto.subtle.
function sha256js(ascii) {
  const rr = (v, a) => (v >>> a) | (v << (32 - a)), maxW = Math.pow(2, 32), words = [], bitLen = ascii.length * 8;
  let h = [], k = [], cont = 0, res = "", i, j; const comp = {};
  for (let c = 2; cont < 64; c++) { if (!comp[c]) { for (i = 0; i < 313; i += c) comp[i] = c; h[cont] = (Math.pow(c, 0.5) * maxW) | 0; k[cont++] = (Math.pow(c, 1 / 3) * maxW) | 0; } }
  h = h.slice(0, 8); ascii += "\x80"; while (ascii.length % 64 - 56) ascii += "\x00";
  for (i = 0; i < ascii.length; i++) { j = ascii.charCodeAt(i); if (j >> 8) return null; words[i >> 2] |= j << ((3 - i) % 4) * 8; }
  words[words.length] = (bitLen / maxW) | 0; words[words.length] = bitLen;
  for (j = 0; j < words.length;) {
    const w = words.slice(j, j += 16), ant = h; h = h.slice(0, 8);
    for (i = 0; i < 64; i++) {
      const w15 = w[i - 15], w2 = w[i - 2], a = h[0], e = h[4];
      const t1 = h[7] + (rr(e, 6) ^ rr(e, 11) ^ rr(e, 25)) + ((e & h[5]) ^ ((~e) & h[6])) + k[i] + (w[i] = (i < 16) ? w[i] : (w[i - 16] + (rr(w15, 7) ^ rr(w15, 18) ^ (w15 >>> 3)) + w[i - 7] + (rr(w2, 17) ^ rr(w2, 19) ^ (w2 >>> 10))) | 0);
      const t2 = (rr(a, 2) ^ rr(a, 13) ^ rr(a, 22)) + ((a & h[1]) ^ (a & h[2]) ^ (h[1] & h[2]));
      h = [(t1 + t2) | 0].concat(h); h[4] = (h[4] + t1) | 0;
    }
    for (i = 0; i < 8; i++) h[i] = (h[i] + ant[i]) | 0;
  }
  for (i = 0; i < 8; i++) for (j = 3; j + 1; j--) { const by = (h[i] >> (j * 8)) & 255; res += (by < 16 ? "0" : "") + by.toString(16); }
  return res;
}

// ---------------------------------------------------------------- arranque
if (COM3D) iniciar3D();
construirUI();
function redimensionar() {
  camara.aspect = innerWidth / innerHeight; camara.updateProjectionMatrix();
  if (COM3D) { renderer.setSize(innerWidth, innerHeight, false); composer.setSize(innerWidth, innerHeight); }
  disposicao(); if (QUADROS) desenhar();
}
window.addEventListener("resize", redimensionar);
redimensionar();
if (RETRATO >= 0) { document.body.classList.add("retrato"); modo = "retrato"; $("topo").hidden = true; $("familia").hidden = true; disposicao(); }
else if (Q.has("filme")) iniciarFilme();
else mudarModo("familia");
aplicar(); mostrarBio();
if ((trancaCasa() ? casaEmCrianca() : estado.crianca) && temPin() && RETRATO < 0) entrar();
camP.copy(alvoCamP).add(new THREE.Vector3(0, 0.4, 2.2));
window.__k3d = { webgl: COM3D, estado: () => ({ modo, foco, cheias: cheias.slice(), cena: cenaAtual, lingua }), sha256js, versao: "2.0.0" };
if (QUADROS) window.__quadro(0); else requestAnimationFrame(ciclo);

// Modo avião: na app (dpsindustrial.nl/konfirmu/app/), a entrada regista o mesmo service worker do menu, para que tudo
// abra sem rede depois da primeira visita. Fora da app (ficheiro solto, sem sw.js ao lado) não faz nada.
if ("serviceWorker" in navigator && window.isSecureContext && !QUADROS && RETRATO < 0) {
  const registar = () => { navigator.serviceWorker.register("./sw.js").catch(() => {}); };
  if (document.readyState === "complete") registar(); else window.addEventListener("load", registar);
}
