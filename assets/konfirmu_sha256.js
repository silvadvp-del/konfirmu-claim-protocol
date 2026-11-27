/* Konfirmu SHA-256 v1.0.0 — EUPL-1.2 — sem dependências, sem rede.
 * Calcula o SHA-256 dos BYTES do ficheiro (o mesmo que sha256sum, shasum -a 256 ou certutil).
 * Lê o ficheiro aos bocados de 4 MB: não há limite de tamanho e a memória fica baixa.
 * Também calcula o "hash antigo v1" (KON-572): o cálculo que as páginas faziam até 27-11-2026,
 * em que cada byte acima de 127 contava como dois. Serve só para conferir selos feitos antes.
 * O hash antigo também identifica os bytes de forma única (a expansão é injetiva), mas não é o SHA-256 normal.
 */
(function (raiz) {
  'use strict';
  var K = new Int32Array([
    0x428a2f98, 0x71374491, 0xb5c0fbcf, 0xe9b5dba5, 0x3956c25b, 0x59f111f1, 0x923f82a4, 0xab1c5ed5,
    0xd807aa98, 0x12835b01, 0x243185be, 0x550c7dc3, 0x72be5d74, 0x80deb1fe, 0x9bdc06a7, 0xc19bf174,
    0xe49b69c1, 0xefbe4786, 0x0fc19dc6, 0x240ca1cc, 0x2de92c6f, 0x4a7484aa, 0x5cb0a9dc, 0x76f988da,
    0x983e5152, 0xa831c66d, 0xb00327c8, 0xbf597fc7, 0xc6e00bf3, 0xd5a79147, 0x06ca6351, 0x14292967,
    0x27b70a85, 0x2e1b2138, 0x4d2c6dfc, 0x53380d13, 0x650a7354, 0x766a0abb, 0x81c2c92e, 0x92722c85,
    0xa2bfe8a1, 0xa81a664b, 0xc24b8b70, 0xc76c51a3, 0xd192e819, 0xd6990624, 0xf40e3585, 0x106aa070,
    0x19a4c116, 0x1e376c08, 0x2748774c, 0x34b0bcb5, 0x391c0cb3, 0x4ed8aa4a, 0x5b9cca4f, 0x682e6ff3,
    0x748f82ee, 0x78a5636f, 0x84c87814, 0x8cc70208, 0x90befffa, 0xa4506ceb, 0xbef9a3f7, 0xc67178f2]);
  var BOCADO = 4 * 1024 * 1024;

  function Hasher() {
    this.h = new Int32Array([0x6a09e667, 0xbb67ae85, 0x3c6ef372, 0xa54ff53a, 0x510e527f, 0x9b05688c, 0x1f83d9ab, 0x5be0cd19]);
    this.w = new Int32Array(64);
    this.buf = new Uint8Array(64);
    this.n = 0;      // bytes à espera no buf
    this.total = 0;  // bytes já recebidos
    this.fim = false;
  }
  Hasher.prototype._blocos = function (d, p, fimP) { // comprime blocos de 64 bytes de d[p..fimP)
    var w = this.w, h = this.h, i, t1, t2, a, b, c, e, f, g, hh, dd, s0, s1;
    while (p + 64 <= fimP) {
      for (i = 0; i < 16; i++, p += 4) w[i] = (d[p] << 24) | (d[p + 1] << 16) | (d[p + 2] << 8) | d[p + 3];
      for (i = 16; i < 64; i++) {
        s0 = w[i - 15]; s1 = w[i - 2];
        w[i] = (((s1 >>> 17) | (s1 << 15)) ^ ((s1 >>> 19) | (s1 << 13)) ^ (s1 >>> 10)) + w[i - 7] +
               (((s0 >>> 7) | (s0 << 25)) ^ ((s0 >>> 18) | (s0 << 14)) ^ (s0 >>> 3)) + w[i - 16] | 0;
      }
      a = h[0]; b = h[1]; c = h[2]; dd = h[3]; e = h[4]; f = h[5]; g = h[6]; hh = h[7];
      for (i = 0; i < 64; i++) {
        t1 = hh + (((e >>> 6) | (e << 26)) ^ ((e >>> 11) | (e << 21)) ^ ((e >>> 25) | (e << 7))) +
             ((e & f) ^ (~e & g)) + K[i] + w[i] | 0;
        t2 = (((a >>> 2) | (a << 30)) ^ ((a >>> 13) | (a << 19)) ^ ((a >>> 22) | (a << 10))) +
             ((a & b) ^ (a & c) ^ (b & c)) | 0;
        hh = g; g = f; f = e; e = dd + t1 | 0; dd = c; c = b; b = a; a = t1 + t2 | 0;
      }
      h[0] = h[0] + a | 0; h[1] = h[1] + b | 0; h[2] = h[2] + c | 0; h[3] = h[3] + dd | 0;
      h[4] = h[4] + e | 0; h[5] = h[5] + f | 0; h[6] = h[6] + g | 0; h[7] = h[7] + hh | 0;
    }
    return p;
  };
  Hasher.prototype.update = function (d) {
    if (this.fim) throw new Error('KonfirmuSHA256: hash já fechado');
    if (!(d instanceof Uint8Array)) d = new Uint8Array(d);
    var p = 0, len = d.length;
    this.total += len;
    if (this.n > 0) {
      var falta = 64 - this.n, k = len < falta ? len : falta;
      this.buf.set(d.subarray(0, k), this.n); this.n += k; p = k;
      if (this.n < 64) return this;
      this._blocos(this.buf, 0, 64); this.n = 0;
    }
    p = this._blocos(d, p, len);
    if (p < len) { this.buf.set(d.subarray(p), 0); this.n = len - p; }
    return this;
  };
  Hasher.prototype.hex = function () {
    if (!this.fim) {
      var total = this.total, resto = new Uint8Array(this.n < 56 ? 64 : 128);
      resto.set(this.buf.subarray(0, this.n)); resto[this.n] = 0x80;
      var hi = Math.floor(total / 0x20000000), lo = (total % 0x20000000) * 8, L = resto.length;
      resto[L - 8] = hi >>> 24; resto[L - 7] = hi >>> 16; resto[L - 6] = hi >>> 8; resto[L - 5] = hi;
      resto[L - 4] = lo >>> 24; resto[L - 3] = lo >>> 16; resto[L - 2] = lo >>> 8; resto[L - 1] = lo;
      this._blocos(resto, 0, L); this.fim = true;
      var s = '';
      for (var i = 0; i < 8; i++) s += ('0000000' + (this.h[i] >>> 0).toString(16)).slice(-8);
      this._hex = s;
    }
    return this._hex;
  };

  // Hash antigo v1: o byte b >= 0x80 conta como os 2 bytes UTF-8 de U+00b.
  function expandirV1(d) {
    var o = new Uint8Array(d.length * 2), j = 0;
    for (var i = 0; i < d.length; i++) {
      var b = d[i];
      if (b < 0x80) o[j++] = b; else { o[j++] = 0xC0 | (b >> 6); o[j++] = 0x80 | (b & 0x3F); }
    }
    return o.subarray(0, j);
  }
  function utf8(str) {
    if (typeof TextEncoder !== 'undefined') return new TextEncoder().encode(str);
    var s = unescape(encodeURIComponent(str)), u = new Uint8Array(s.length);
    for (var i = 0; i < s.length; i++) u[i] = s.charCodeAt(i);
    return u;
  }
  function lerBocado(blob, ini, fim) {
    var pedaco = blob.slice(ini, fim);
    if (pedaco.arrayBuffer) return pedaco.arrayBuffer();
    return new Promise(function (ok, falha) {
      var rd = new FileReader();
      rd.onload = function () { ok(rd.result); };
      rd.onerror = function () { falha(rd.error); };
      rd.readAsArrayBuffer(pedaco);
    });
  }
  // Lê o ficheiro uma vez e devolve { sha256, legado_v1 (se pedido), bytes }.
  function ficheiro(blob, opcoes) {
    opcoes = opcoes || {};
    var hN = new Hasher(), hV1 = opcoes.legado ? new Hasher() : null, pos = 0, tam = blob.size;
    function passo() {
      if (pos >= tam) {
        var r = { sha256: hN.hex(), bytes: tam };
        if (hV1) r.legado_v1 = hV1.hex();
        return Promise.resolve(r);
      }
      var fim = Math.min(pos + BOCADO, tam);
      return lerBocado(blob, pos, fim).then(function (ab) {
        var u8 = new Uint8Array(ab);
        hN.update(u8); if (hV1) hV1.update(expandirV1(u8));
        pos = fim;
        if (opcoes.progresso) { try { opcoes.progresso(pos, tam); } catch (_) {} }
        return passo();
      });
    }
    return passo();
  }

  var API = {
    versao: '1.0.0',
    Hasher: Hasher,
    bytes: function (u8) { return new Hasher().update(u8).hex(); },
    text: function (str) { return new Hasher().update(utf8(String(str))).hex(); },
    legadoV1Bytes: function (u8) { return new Hasher().update(expandirV1(u8 instanceof Uint8Array ? u8 : new Uint8Array(u8))).hex(); },
    // Promise<string> com o SHA-256 dos bytes do ficheiro (Blob/File)
    ficheiro: function (blob, progresso) { return ficheiro(blob, { progresso: progresso }).then(function (r) { return r.sha256; }); },
    // Promise<{sha256, legado_v1, bytes}> numa só leitura
    ambos: function (blob, progresso) { return ficheiro(blob, { legado: true, progresso: progresso }); }
  };
  // Auto-teste à carga (vetores NIST FIPS 180-4): se falhar, as páginas avisam e não dão veredicto.
  API.ok = API.text('') === 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855' &&
           API.text('abc') === 'ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad' &&
           API.text('abcdbcdecdefdefgefghfghighijhijkijkljklmklmnlmnomnopnopq') === '248d6a61d20638b8e5c026930c3e6039a33ce45964ff2167f6ecedd419db06c1';
  raiz.KonfirmuSHA256 = API;
  if (typeof module !== 'undefined' && module.exports) module.exports = API;
})(typeof self !== 'undefined' ? self : this);
