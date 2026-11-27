/* kcp_ed_estrito.js — verificação Ed25519 estrita, regra KCP/0.1 (EUPL-1.2), 27-11-2026.
 * A tweetnacl aceita, sozinha, uma «assinatura universal»: chave pública e R de ordem pequena com S = 0
 * conferem para QUALQUER mensagem. O motor Python (konfirmu_calc.py, desde a v2.8) já recusa; as páginas
 * passam a recusar também, com as mesmas regras:
 *   1. hexadecimal estrito: só minúsculas 0-9a-f e o tamanho exato (chave 32 bytes, assinatura 64);
 *   2. chave e R em codificação canónica (y < p) e fora dos 8 pontos de ordem pequena (e das 2 variantes
 *      com o bit de sinal em x = 0);
 *   3. S < L (sem assinaturas maleáveis S + L);
 *   4. só depois, a verificação RFC 8032 da tweetnacl.
 * Precisa de nacl (assets/nacl-fast.min.js) carregado antes. */
var KCP_ED = (function () {
  "use strict";
  var PEQUENOS = [
    "0100000000000000000000000000000000000000000000000000000000000000", /* neutro, ordem 1 */
    "0100000000000000000000000000000000000000000000000000000000000080", /* neutro com bit de sinal */
    "ecffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff7f", /* ordem 2 */
    "ecffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff", /* ordem 2 com bit de sinal */
    "0000000000000000000000000000000000000000000000000000000000000000", /* ordem 4 */
    "0000000000000000000000000000000000000000000000000000000000000080", /* ordem 4 */
    "26e8958fc2b227b045c3f489f2ef98f0d5dfac05d3c63339b13802886d53fc05", /* ordem 8 */
    "26e8958fc2b227b045c3f489f2ef98f0d5dfac05d3c63339b13802886d53fc85", /* ordem 8 */
    "c7176a703d4dd84fba3c0b760d10670f2a2053fa2c39ccc64ec7fd7792ac037a", /* ordem 8 */
    "c7176a703d4dd84fba3c0b760d10670f2a2053fa2c39ccc64ec7fd7792ac03fa"  /* ordem 8 */
  ];
  /* L = 2^252 + 27742317777372353535851937790883648493, em little-endian */
  var L = [0xed, 0xd3, 0xf5, 0x5c, 0x1a, 0x63, 0x12, 0x58, 0xd6, 0x9c, 0xf7, 0xa2, 0xde, 0xf9, 0xde, 0x14,
           0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0x10];

  function hexEstrito(h, n) { return typeof h === "string" && h.length === 2 * n && /^[0-9a-f]+$/.test(h); }
  function deHex(h) { var u = new Uint8Array(h.length / 2); for (var i = 0; i < u.length; i++) u[i] = parseInt(h.substr(i * 2, 2), 16); return u; }
  function paraHex(u) { var s = ""; for (var i = 0; i < u.length; i++) s += (u[i] < 16 ? "0" : "") + u[i].toString(16); return s; }
  function canonico(u) { /* y (sem o bit de sinal) < p = 2^255 - 19 */
    for (var i = 31; i >= 0; i--) {
      var y = i === 31 ? (u[i] & 0x7f) : u[i], q = i === 31 ? 0x7f : (i === 0 ? 0xed : 0xff);
      if (y < q) return true;
      if (y > q) return false;
    }
    return false;
  }
  function menorQueL(s) {
    for (var i = 31; i >= 0; i--) { if (s[i] < L[i]) return true; if (s[i] > L[i]) return false; }
    return false;
  }
  /* devolve {ok, motivo} */
  function conferir(msg, sigHex, pkHex) {
    if (!hexEstrito(pkHex, 32)) return { ok: false, motivo: "chave fora do formato (64 hexadecimais minúsculos)" };
    if (!hexEstrito(sigHex, 64)) return { ok: false, motivo: "assinatura fora do formato (128 hexadecimais minúsculos)" };
    var pk = deHex(pkHex), sig = deHex(sigHex), R = sig.subarray(0, 32), S = sig.subarray(32);
    if (!canonico(pk) || !canonico(R)) return { ok: false, motivo: "ponto em codificação não canónica" };
    if (PEQUENOS.indexOf(pkHex) >= 0 || PEQUENOS.indexOf(paraHex(R)) >= 0) return { ok: false, motivo: "assinatura universal recusada (ponto de ordem pequena, KCP/0.1)" };
    if (!menorQueL(S)) return { ok: false, motivo: "assinatura maleável recusada (S fora do intervalo)" };
    try { return nacl.sign.detached.verify(msg, sig, pk) ? { ok: true, motivo: "" } : { ok: false, motivo: "a assinatura não confere" }; }
    catch (e) { return { ok: false, motivo: "erro na verificação" }; }
  }
  function verificar(msg, sigHex, pkHex) { return conferir(msg, sigHex, pkHex).ok; }
  return { verificar: verificar, conferir: conferir, PEQUENOS: PEQUENOS, REGRA: "KCP/0.1 ed25519 estrito" };
})();
if (typeof module !== "undefined") module.exports = KCP_ED;
