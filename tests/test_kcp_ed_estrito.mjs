// Ensaio da verificação Ed25519 estrita (KCP/0.1) das páginas: node tests/test_kcp_ed_estrito.mjs
import { createRequire } from "module";
const require = createRequire(import.meta.url);
globalThis.self = globalThis;
const nacl = require("../assets/nacl-fast.min.js");
globalThis.nacl = nacl;
const K = require("../assets/kcp_ed_estrito.js");
const hex = (u) => Array.from(u, (b) => b.toString(16).padStart(2, "0")).join("");
const msg = (t) => new TextEncoder().encode(t);
let bons = 0, maus = 0;
function prova(nome, cond) { if (cond) { bons++; console.log("OK   " + nome); } else { maus++; console.log("MAL  " + nome); } }
const par = nacl.sign.keyPair.fromSeed(new Uint8Array(32).fill(7));
const m = msg("KONFIRMU-CLX|v1|abc");
const sig = nacl.sign.detached(m, par.secretKey);
prova("assinatura boa confere", K.verificar(m, hex(sig), hex(par.publicKey)));
prova("assinatura boa noutra mensagem não confere", !K.verificar(msg("outra"), hex(sig), hex(par.publicKey)));
const neutro = "01" + "00".repeat(31);
prova("a tweetnacl sozinha aceitaria a assinatura universal (prova de que o perigo existe)", nacl.sign.detached.verify(msg("qualquer"), Uint8Array.from((neutro + "00".repeat(32)).match(/../g).map((x) => parseInt(x, 16))), Uint8Array.from(neutro.match(/../g).map((x) => parseInt(x, 16)))));
for (const p of K.PEQUENOS) {
  prova("assinatura universal recusada com a chave " + p.slice(0, 8) + "…", !K.verificar(msg("qualquer coisa"), p + "00".repeat(32), p));
}
prova("hexadecimal em maiúsculas recusado", !K.verificar(m, hex(sig).toUpperCase(), hex(par.publicKey)));
prova("hexadecimal com lixo recusado", !K.verificar(m, hex(sig).slice(0, 126) + "zz", hex(par.publicKey)));
prova("tamanho errado recusado", !K.verificar(m, hex(sig).slice(0, 126), hex(par.publicKey)));
// S + L (maleável)
const L = 2n ** 252n + 27742317777372353535851937790883648493n;
let s = 0n; for (let i = 31; i >= 0; i--) s = (s << 8n) | BigInt(sig[32 + i]);
const s2 = s + L; const mal = new Uint8Array(sig); let t = s2; for (let i = 0; i < 32; i++) { mal[32 + i] = Number(t & 255n); t >>= 8n; }
prova("assinatura maleável (S + L) recusada", !K.verificar(m, hex(mal), hex(par.publicKey)));
// codificação não canónica da chave (y >= p)
prova("chave não canónica recusada", !K.verificar(m, hex(sig), "ed" + "ff".repeat(30) + "7f"));
console.log("\nresultado: " + bons + " de " + (bons + maus));
process.exit(maus ? 1 : 0);
