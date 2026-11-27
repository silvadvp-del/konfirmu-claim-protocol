// Nucleo unico (KON-596): o motor Python v2 e o motor das paginas (KSHA/2) dao as mesmas respostas.
// Corre com: node tests/nucleo_unico.mjs   (so Node e Python 3; sem rede, sem dependencias)
// 1. As 4 paginas de selo levam o mesmo motor, byte a byte, igual a fonte unica ksha_fluxo.js.
// 2. KSHA/2 = SHA-256 do Node: vetores NIST e 300 tamanhos ao acaso; a «regra antiga» (selos v1) bate.
// 3. Um recibo do motor Python v2 confere com KSHA/2 e com a tweetnacl das paginas.
// 4. Um recibo assinado com a tweetnacl das paginas confere no motor Python v2.
import { readFileSync, writeFileSync, mkdtempSync, rmSync } from "node:fs";
import { createHash, getRandomValues } from "node:crypto";
import { execFileSync } from "node:child_process";
import { createRequire } from "node:module";
import { tmpdir } from "node:os";
import { join, dirname } from "node:path";
import { fileURLToPath } from "node:url";
import vm from "node:vm";

const RAIZ = join(dirname(fileURLToPath(import.meta.url)), "..");
const MOTOR_PY = join(RAIZ, "ferramentas", "konfirmu_nova_geracao_2030.py");
const PAGINAS = ["chronolex_verify.html", "chronolex_photo_seal.html", "estudio_video_criancas.html", "verificador_offline.html", "enxame_naves.html"];
const INI = "/* >>> KSHA: inicio", FIM = "/* <<< KSHA: fim */";
let ok = 0, falhas = 0;
function prova(texto, cond, extra) {
  if (cond) ok++; else falhas++;
  console.log((cond ? "PASSA " : "FALHA ") + texto + (extra ? " — " + extra : ""));
}
const sha = (b) => createHash("sha256").update(b).digest("hex");
const bloco = (t) => { const a = t.indexOf(INI), b = t.indexOf(FIM); return a >= 0 && b > a ? t.slice(a, b + FIM.length) : null; };

// 1. uma so fonte
const fonte = bloco(readFileSync(join(RAIZ, "ksha_fluxo.js"), "utf8"));
prova("ksha_fluxo.js tem o bloco do motor", !!fonte, fonte ? fonte.length + " caracteres" : "");
for (const p of PAGINAS) prova(p + " leva o motor igual a ksha_fluxo.js", bloco(readFileSync(join(RAIZ, p), "utf8")) === fonte);

// carregar KSHA/2 tal como esta na fonte
const ctx = { crypto: globalThis.crypto, Uint8Array, Int32Array, Promise, Error, String, Math };
vm.createContext(ctx);
vm.runInContext(fonte + "\nthis.KSHA = KSHA;", ctx);
const K = ctx.KSHA;

// 2. KSHA/2 = SHA-256 do Node
prova("vetor NIST «abc»", K.deTexto("abc") === "ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad");
prova("vetor NIST vazio", K.deTexto("") === "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855");
prova("vetor NIST 1 000 000 × «a»", K.deTexto("a".repeat(1000000)) === "cdc76e5c9914fb9281a1c7e284d73e67f1809a48a497200e046d39ccc7112cd0");
let iguais = 0, antigosIguais = 0; const N = 300;
for (let i = 0; i < N; i++) {
  const n = i < 70 ? i : Math.floor(Math.random() * 200000);
  const u = new Uint8Array(n); for (let j = 0; j < n; j += 65536) getRandomValues(u.subarray(j, Math.min(n, j + 65536)));
  if (K.deBytes(u) === sha(u)) iguais++;
  if (K.deBytes(K.regraAntiga(u)) === sha(Buffer.from(Buffer.from(u).toString("latin1"), "utf8"))) antigosIguais++;
}
prova("KSHA/2 = SHA-256 do Node em " + N + " ficheiros ao acaso (0 a 200 KB)", iguais === N, iguais + " de " + N);
prova("regra antiga (selos v1) = SHA-256 dos bytes convertidos para UTF-8", antigosIguais === N, antigosIguais + " de " + N);

// tweetnacl das paginas
globalThis.self = globalThis;
const nacl = createRequire(import.meta.url)(join(RAIZ, "assets", "nacl-fast.min.js"));
const hexB = (h) => Uint8Array.from(h.match(/../g).map((x) => parseInt(x, 16)));
const bHex = (u) => Array.from(u, (x) => x.toString(16).padStart(2, "0")).join("");
const DOMINIO = new TextEncoder().encode("KONFIRMU-2030|v2|");
const junta = (a, b) => { const o = new Uint8Array(a.length + b.length); o.set(a); o.set(b, a.length); return o; };
// JSON canonico igual ao do motor Python: chaves por ordem, sem espacos, UTF-8
const canonico = (o) => Array.isArray(o) ? "[" + o.map(canonico).join(",") + "]"
  : o && typeof o === "object" ? "{" + Object.keys(o).sort().map((k) => JSON.stringify(k) + ":" + canonico(o[k])).join(",") + "}"
  : JSON.stringify(o);

const tmp = mkdtempSync(join(tmpdir(), "nucleo-unico-"));
try {
  const ficheiro = join(tmp, "carta_ação.bin");
  const dados = new Uint8Array(150000); for (let j = 0; j < dados.length; j += 65536) getRandomValues(dados.subarray(j, Math.min(dados.length, j + 65536)));
  writeFileSync(ficheiro, dados);
  const py = (...a) => JSON.parse(execFileSync("python3", ["-I", MOTOR_PY, "--cofre", join(tmp, "cofre"), ...a], { encoding: "utf8" }));

  // 3. recibo do motor Python v2, conferido pelo lado das paginas
  const r = py("selar", ficheiro).recibo;
  prova("motor Python v2 sela um ficheiro de 150 KB", !!r && r.recibo === "konfirmu-2030/2");
  prova("o SHA-256 do recibo Python = KSHA/2 = Node", r.bloco.sha256 === K.deBytes(dados) && r.bloco.sha256 === sha(dados));
  prova("hash_bloco do recibo = KSHA/2 do bloco canonico", r.hash_bloco === K.deTexto(canonico(r.bloco)));
  const msg = junta(DOMINIO, hexB(r.hash_bloco));
  prova("a assinatura Python confere com a tweetnacl das paginas", nacl.sign.detached.verify(msg, hexB(r.assinatura), hexB(r.bloco.pk)));
  const mexida = Uint8Array.from(msg); mexida[mexida.length - 1] ^= 1;
  prova("com 1 bit trocado, a tweetnacl recusa", !nacl.sign.detached.verify(mexida, hexB(r.assinatura), hexB(r.bloco.pk)));

  // 4. recibo assinado com a tweetnacl das paginas, conferido pelo motor Python v2
  const kp = nacl.sign.keyPair.fromSeed(getRandomValues(new Uint8Array(32)));
  const h512 = createHash("sha512").update(dados).digest("hex");
  const b = { v: "konfirmu-2030/2", seq: 1, ts: 1795000000, nome: "carta_ação.bin", bytes: dados.length,
              sha256: K.deBytes(dados), sha512: h512, anterior: "0".repeat(64), pk: bHex(kp.publicKey) };
  const hb = K.deTexto(canonico(b));
  const recibo = { recibo: "konfirmu-2030/2", bloco: b, hash_bloco: hb, assinatura: bHex(nacl.sign.detached(junta(DOMINIO, hexB(hb)), kp.secretKey)) };
  writeFileSync(join(tmp, "recibo_js.json"), JSON.stringify(recibo));
  const v = py("verificar", ficheiro, "--recibo", join(tmp, "recibo_js.json"));
  prova("recibo feito com a tweetnacl confere no motor Python v2", v.veredicto === "VERIFICADO", v.veredicto);
  const outro = join(tmp, "outro.bin"); const d2 = Uint8Array.from(dados); d2[777] ^= 1; writeFileSync(outro, d2);
  const v2 = py("verificar", outro, "--recibo", join(tmp, "recibo_js.json"));
  prova("o mesmo recibo com o ficheiro mudado em 1 bit dá ALTERADO", v2.veredicto === "ALTERADO", v2.veredicto);
} finally { rmSync(tmp, { recursive: true, force: true }); }

// 5. o Enxame usa os mesmos portões do chat (112 e crianças), cópia exata
{
  const chat = readFileSync(join(RAIZ, "konfirmu_chat_offline_v0.1.html"), "utf8");
  const a = chat.indexOf("/* ---------- portão de emergência"), j = chat.indexOf("function portaoCrianca", a), b = chat.indexOf("return null}", j) + "return null}".length;
  const enx = readFileSync(join(RAIZ, "enxame_naves.html"), "utf8");
  const PI = "/* >>> PORTOES: copia exata de konfirmu_chat_offline_v0.1.html (nao editar aqui) */\n", PF = "\n/* <<< PORTOES: fim */";
  const x = enx.indexOf(PI), y = enx.indexOf(PF, x);
  prova("enxame_naves.html leva os portões 112 e crianças iguais ao chat", a >= 0 && j > a && x >= 0 && y > x && enx.slice(x + PI.length, y) === chat.slice(a, b));
}

console.log("\n" + ok + " de " + (ok + falhas) + " passam");
process.exit(falhas ? 1 : 0);
