/* terminal_worker.js — caixa de trabalho do Terminal sem rede da Konfirmu (EUPL-1.2).
 * Corre num Web Worker: não vê a página nem os dados dela. Leva uma cópia exata do motor KSHA/2
 * (entre as marcas KSHA, igual a ksha_fluxo.js) e, ao arrancar, desliga fetch, XMLHttpRequest, WebSocket,
 * EventSource e importScripts.
 * Comandos: help · sha256 · verify · bigint-test · selftest · clear · versao */
"use strict";
/* >>> KSHA: inicio (copia exata de ksha_fluxo.js) */
/* KSHA/2 - SHA-256 sobre BYTES, aos bocados (KON-572). Fonte unica: ksha_fluxo.js. Nao editar dentro das paginas. */
var KSHA = (function () {
  "use strict";
  var REGRA = "sha256-bytes/2";
  var BOCADO = 1048576;
  var LIMITE_CONFIRMA = 16 * BOCADO;
  var K = new Int32Array([
    0x428a2f98, 0x71374491, 0xb5c0fbcf, 0xe9b5dba5, 0x3956c25b, 0x59f111f1, 0x923f82a4, 0xab1c5ed5,
    0xd807aa98, 0x12835b01, 0x243185be, 0x550c7dc3, 0x72be5d74, 0x80deb1fe, 0x9bdc06a7, 0xc19bf174,
    0xe49b69c1, 0xefbe4786, 0x0fc19dc6, 0x240ca1cc, 0x2de92c6f, 0x4a7484aa, 0x5cb0a9dc, 0x76f988da,
    0x983e5152, 0xa831c66d, 0xb00327c8, 0xbf597fc7, 0xc6e00bf3, 0xd5a79147, 0x06ca6351, 0x14292967,
    0x27b70a85, 0x2e1b2138, 0x4d2c6dfc, 0x53380d13, 0x650a7354, 0x766a0abb, 0x81c2c92e, 0x92722c85,
    0xa2bfe8a1, 0xa81a664b, 0xc24b8b70, 0xc76c51a3, 0xd192e819, 0xd6990624, 0xf40e3585, 0x106aa070,
    0x19a4c116, 0x1e376c08, 0x2748774c, 0x34b0bcb5, 0x391c0cb3, 0x4ed8aa4a, 0x5b9cca4f, 0x682e6ff3,
    0x748f82ee, 0x78a5636f, 0x84c87814, 0x8cc70208, 0x90befffa, 0xa4506ceb, 0xbef9a3f7, 0xc67178f2
  ]);

  function Fluxo() {
    this.h = new Int32Array([0x6a09e667, 0xbb67ae85, 0x3c6ef372, 0xa54ff53a, 0x510e527f, 0x9b05688c, 0x1f83d9ab, 0x5be0cd19]);
    this.b = new Uint8Array(64);
    this.w = new Int32Array(64);
    this.n = 0;
    this.total = 0;
  }
  Fluxo.prototype.bloco = function (p, o) {
    var w = this.w, h = this.h, i, x, y, t1, t2;
    var a = h[0], b = h[1], c = h[2], d = h[3], e = h[4], f = h[5], g = h[6], q = h[7];
    for (i = 0; i < 16; i++) {
      w[i] = (p[o] << 24) | (p[o + 1] << 16) | (p[o + 2] << 8) | p[o + 3];
      o += 4;
    }
    for (i = 16; i < 64; i++) {
      x = w[i - 15];
      y = w[i - 2];
      x = ((x >>> 7) | (x << 25)) ^ ((x >>> 18) | (x << 14)) ^ (x >>> 3);
      y = ((y >>> 17) | (y << 15)) ^ ((y >>> 19) | (y << 13)) ^ (y >>> 10);
      w[i] = (w[i - 16] + x + w[i - 7] + y) | 0;
    }
    for (i = 0; i < 64; i++) {
      y = ((e >>> 6) | (e << 26)) ^ ((e >>> 11) | (e << 21)) ^ ((e >>> 25) | (e << 7));
      t1 = (q + y + ((e & f) ^ (~e & g)) + K[i] + w[i]) | 0;
      x = ((a >>> 2) | (a << 30)) ^ ((a >>> 13) | (a << 19)) ^ ((a >>> 22) | (a << 10));
      t2 = (x + ((a & b) ^ (a & c) ^ (b & c))) | 0;
      q = g;
      g = f;
      f = e;
      e = (d + t1) | 0;
      d = c;
      c = b;
      b = a;
      a = (t1 + t2) | 0;
    }
    h[0] = (h[0] + a) | 0;
    h[1] = (h[1] + b) | 0;
    h[2] = (h[2] + c) | 0;
    h[3] = (h[3] + d) | 0;
    h[4] = (h[4] + e) | 0;
    h[5] = (h[5] + f) | 0;
    h[6] = (h[6] + g) | 0;
    h[7] = (h[7] + q) | 0;
  };
  Fluxo.prototype.junta = function (u8) {
    var n = u8.length, i = 0, falta;
    this.total += n;
    if (this.n) {
      falta = 64 - this.n;
      if (n < falta) {
        this.b.set(u8, this.n);
        this.n += n;
        return this;
      }
      this.b.set(u8.subarray(0, falta), this.n);
      this.bloco(this.b, 0);
      this.n = 0;
      i = falta;
    }
    for (; i + 64 <= n; i += 64) this.bloco(u8, i);
    if (i < n) {
      this.b.set(u8.subarray(i), 0);
      this.n = n - i;
    }
    return this;
  };
  Fluxo.prototype.fim = function () {
    var b = this.b, n = this.n, t = this.total, i, s = "";
    var alto = Math.floor(t / 536870912), baixo = (t % 536870912) * 8;
    b[n++] = 128;
    if (n > 56) {
      while (n < 64) b[n++] = 0;
      this.bloco(b, 0);
      n = 0;
    }
    while (n < 56) b[n++] = 0;
    b[56] = (alto >>> 24) & 255;
    b[57] = (alto >>> 16) & 255;
    b[58] = (alto >>> 8) & 255;
    b[59] = alto & 255;
    b[60] = (baixo >>> 24) & 255;
    b[61] = (baixo >>> 16) & 255;
    b[62] = (baixo >>> 8) & 255;
    b[63] = baixo & 255;
    this.bloco(b, 0);
    for (i = 0; i < 8; i++) s += ("0000000" + (this.h[i] >>> 0).toString(16)).slice(-8);
    return s;
  };

  function hex(u8) {
    var s = "", i;
    for (i = 0; i < u8.length; i++) s += (u8[i] < 16 ? "0" : "") + u8[i].toString(16);
    return s;
  }
  /* Texto -> bytes UTF-8. Texto mal formado (surrogate solto) e recusado, nunca "arranjado". */
  function utf8(str) {
    var n = str.length, u = new Uint8Array(n * 3), j = 0, i, c, d;
    for (i = 0; i < n; i++) {
      c = str.charCodeAt(i);
      if (c < 128) {
        u[j++] = c;
      } else if (c < 2048) {
        u[j++] = 192 | (c >> 6);
        u[j++] = 128 | (c & 63);
      } else if (c >= 55296 && c <= 57343) {
        d = i + 1 < n ? str.charCodeAt(i + 1) : 0;
        if (c > 56319 || d < 56320 || d > 57343) throw new Error("texto mal formado");
        c = 65536 + ((c - 55296) << 10) + (d - 56320);
        i++;
        u[j++] = 240 | (c >> 18);
        u[j++] = 128 | ((c >> 12) & 63);
        u[j++] = 128 | ((c >> 6) & 63);
        u[j++] = 128 | (c & 63);
      } else {
        u[j++] = 224 | (c >> 12);
        u[j++] = 128 | ((c >> 6) & 63);
        u[j++] = 128 | (c & 63);
      }
    }
    return u.subarray(0, j);
  }
  /* Regra antiga (selos v1, das paginas anteriores ao KSHA/2): cada byte >= 128 era trocado por dois. So para conferir selos antigos. */
  function regraAntiga(u8) {
    var n = u8.length, o = new Uint8Array(n * 2), j = 0, i, b;
    for (i = 0; i < n; i++) {
      b = u8[i];
      if (b < 128) {
        o[j++] = b;
      } else {
        o[j++] = 192 | (b >> 6);
        o[j++] = 128 | (b & 63);
      }
    }
    return o.subarray(0, j);
  }

  var testado = false;
  function autoteste() {
    var z, i, f;
    if (testado) return;
    z = new Uint8Array(1000);
    for (i = 0; i < 1000; i++) z[i] = (i * 7 + 3) & 255;
    f = new Fluxo();
    f.junta(z.subarray(0, 1));
    f.junta(z.subarray(1, 130));
    f.junta(z.subarray(130));
    if (
      new Fluxo().junta(utf8("abc")).fim() !== "ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad" ||
      f.fim() !== "1e9bc38cbf860b9ec31918b065f9b52476c549a782e0e7990bed8ce3868d2371"
    ) {
      throw new Error("motor SHA-256 avariado neste aparelho");
    }
    testado = true;
  }
  function deBytes(u8) {
    autoteste();
    return new Fluxo().junta(u8).fim();
  }
  function deTexto(str) {
    return deBytes(utf8(String(str)));
  }

  function ler(blob, a, b) {
    var parte = blob.slice(a, b);
    if (typeof parte.arrayBuffer === "function") {
      return parte.arrayBuffer().then(function (x) {
        return new Uint8Array(x);
      });
    }
    return new Promise(function (ok, erro) {
      var r = new FileReader();
      r.onload = function () {
        ok(new Uint8Array(r.result));
      };
      r.onerror = function () {
        erro(r.error || new Error("leitura falhou"));
      };
      r.readAsArrayBuffer(parte);
    });
  }
  /* Segundo motor (o do navegador), quando existe e o ficheiro cabe em memoria. Se discordarem, recusa. */
  function confirma(blob, r) {
    var cs = typeof crypto !== "undefined" && crypto.subtle && crypto.subtle.digest ? crypto.subtle : null;
    if (!cs || r.bytes > LIMITE_CONFIRMA) return r;
    return ler(blob, 0, r.bytes)
      .then(function (u8) {
        return cs.digest("SHA-256", u8);
      })
      .then(
        function (d) {
          return hex(new Uint8Array(d));
        },
        function () {
          return null;
        }
      )
      .then(function (h2) {
        if (h2 === null) return r;
        if (h2 !== r.sha256) throw new Error("dois motores discordam: resultado recusado");
        r.confirmado = true;
        return r;
      });
  }
  /* Ficheiro (Blob/File) -> Promise de {sha256, bytes, regra, confirmado, antigo?}. Memoria constante. */
  function deBlob(blob, opc) {
    opc = opc || {};
    return new Promise(function (ok) {
      autoteste();
      ok();
    }).then(function () {
      var f = new Fluxo(), g = opc.antigo ? new Fluxo() : null, pos = 0, total = blob.size;
      function passo() {
        var ate;
        if (pos >= total) {
          var r = { sha256: f.fim(), bytes: total, regra: REGRA, confirmado: false };
          if (g) r.antigo = g.fim();
          return confirma(blob, r);
        }
        ate = Math.min(pos + BOCADO, total);
        return ler(blob, pos, ate).then(function (u8) {
          if (u8.length !== ate - pos) throw new Error("leitura incompleta do ficheiro");
          f.junta(u8);
          if (g) g.junta(regraAntiga(u8));
          pos = ate;
          if (opc.progresso) opc.progresso(pos, total);
          return passo();
        });
      }
      return passo();
    });
  }

  return { REGRA: REGRA, Fluxo: Fluxo, hex: hex, utf8: utf8, regraAntiga: regraAntiga, deBytes: deBytes, deTexto: deTexto, deBlob: deBlob };
})();
/* <<< KSHA: fim */
(function selar() {
  var fora = ["fetch", "XMLHttpRequest", "WebSocket", "EventSource", "importScripts", "WebTransport"];
  for (var i = 0; i < fora.length; i++) {
    try { Object.defineProperty(self, fora[i], { value: undefined, writable: false, configurable: false }); } catch (e) { try { self[fora[i]] = undefined; } catch (e2) {} }
  }
})();

var VERSAO = "terminal-konfirmu/1.0 (27-11-2026) · motor " + KSHA.REGRA;
var ultimo = null; // { sha256, origem }

function linha(texto, classe) { postMessage({ tipo: "linha", texto: String(texto), classe: classe || "" }); }
function hexValido(h) { return /^[0-9a-f]{64}$/.test(h); }

var AJUDA = [
  "Comandos (tudo neste aparelho, sem rede):",
  "  help                  esta lista",
  "  sha256 <texto>        SHA-256 dos bytes UTF-8 do texto",
  "  sha256 -f             escolher um ficheiro e calcular o SHA-256 (aos bocados de 1 MB)",
  "  verify <hash>         comparar com o último SHA-256 calculado",
  "  verify <hash> <texto> calcular o SHA-256 do texto e comparar",
  "  verify -f <hash>      escolher um ficheiro e comparar",
  "  bigint-test           contas exatas com BigInt, com respostas conhecidas",
  "  selftest              SHA-256 com respostas conhecidas (NIST FIPS 180-4)",
  "  clear                 limpar o ecrã",
  "  versao                versão do terminal e do motor"
];

/* ---------- SHA-256 ---------- */
function shaTexto(t) {
  var h = KSHA.deTexto(t);
  var bytes = KSHA.utf8(t).length;
  return { sha256: h, bytes: bytes };
}
function confirmarSubtle(t, h) {
  if (!self.crypto || !crypto.subtle) return Promise.resolve(null);
  return crypto.subtle.digest("SHA-256", KSHA.utf8(t)).then(function (b) {
    var u = new Uint8Array(b), s = "";
    for (var i = 0; i < u.length; i++) s += (u[i] < 16 ? "0" : "") + u[i].toString(16);
    return s === h;
  });
}

/* ---------- BigInt ---------- */
function lucasLehmer(p) {
  if (p === 2) return true;
  var m = (1n << BigInt(p)) - 1n, s = 4n;
  for (var i = 0; i < p - 2; i++) s = (s * s - 2n) % m;
  return s === 0n;
}
function potMod(b, e, m) { var r = 1n; b %= m; while (e > 0n) { if (e & 1n) r = r * b % m; b = b * b % m; e >>= 1n; } return r; }
function fatorial(n) { var r = 1n; for (var i = 2n; i <= n; i++) r *= i; return r; }
function fibonacci(n) { var a = 0n, b = 1n; for (var i = 0; i < n; i++) { var t = a + b; a = b; b = t; } return a; }

function bigintTest() {
  if (typeof BigInt !== "function") { linha("Este navegador não tem BigInt.", "nao"); return; }
  var casos = [
    ["2^127 − 1 é primo (Lucas–Lehmer)", function () { return lucasLehmer(127); }, true],
    ["2^61 − 1 é primo (Lucas–Lehmer)", function () { return lucasLehmer(61); }, true],
    ["2^11 − 1 = 2047 = 23 × 89 não é primo", function () { return lucasLehmer(11); }, false],
    ["2^67 − 1 não é primo (Cole, 1903)", function () { return lucasLehmer(67); }, false],
    ["2^67 − 1 = 193707721 × 761838257287", function () { return ((1n << 67n) - 1n) === 193707721n * 761838257287n; }, true],
    ["30! = 265252859812191058636308480000000", function () { return fatorial(30n).toString(); }, "265252859812191058636308480000000"],
    ["F(100) = 354224848179261915075", function () { return fibonacci(100).toString(); }, "354224848179261915075"],
    ["3^(10^18) mod (10^9+7) = 246336683", function () { return potMod(3n, 10n ** 18n, 1000000007n).toString(); }, "246336683"],
    ["2^256 mod (2^255 − 19) = 38", function () { return potMod(2n, 256n, (1n << 255n) - 19n).toString(); }, "38"],
    ["RSA de brincar: 65^17 mod 3233 = 2790 e volta a 65", function () { return potMod(65n, 17n, 3233n) === 2790n && potMod(2790n, 2753n, 3233n) === 65n; }, true]
  ];
  var bons = 0;
  for (var i = 0; i < casos.length; i++) {
    var t0 = Date.now(), r, certo;
    try { r = casos[i][1](); certo = r === casos[i][2]; } catch (e) { r = "erro: " + e.message; certo = false; }
    var ms = Date.now() - t0;
    if (certo) bons++;
    linha((certo ? "OK   " : "MAL  ") + casos[i][0] + "  (" + ms + " ms)", certo ? "ok" : "nao");
  }
  linha("bigint-test: " + bons + " de " + casos.length + (bons === casos.length ? " certos" : " — há falhas"), bons === casos.length ? "ok" : "nao");
}

function selftest() {
  var casos = [["", "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"],
               ["abc", "ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad"],
               ["abcdbcdecdefdefgefghfghighijhijkijkljklmklmnlmnomnopnopq", "248d6a61d20638b8e5c026930c3e6039a33ce45964ff2167f6ecedd419db06c1"]];
  var bons = 0;
  for (var i = 0; i < casos.length; i++) {
    var h = KSHA.deTexto(casos[i][0]), ok = h === casos[i][1];
    if (ok) bons++;
    linha((ok ? "OK   " : "MAL  ") + "sha256(\"" + (casos[i][0].length > 20 ? casos[i][0].slice(0, 20) + "…" : casos[i][0]) + "\")", ok ? "ok" : "nao");
  }
  var semRede = typeof self.fetch === "undefined" && typeof self.XMLHttpRequest === "undefined" && typeof self.WebSocket === "undefined";
  linha((semRede ? "OK   " : "MAL  ") + "a caixa de trabalho não tem rede (fetch, XMLHttpRequest e WebSocket desligados)", semRede ? "ok" : "nao");
  linha("selftest: " + (bons + (semRede ? 1 : 0)) + " de " + (casos.length + 1), (bons === casos.length && semRede) ? "ok" : "nao");
}

function comparar(esperado, obtido, origem) {
  if (obtido === esperado) linha("IGUAL · " + origem + " tem este SHA-256.", "ok");
  else linha("DIFERENTE · esperado " + esperado + " · calculado " + obtido + " (" + origem + ")", "nao");
}

function ficheiroSha(f, aoFim) {
  var t0 = Date.now(), ultimoPct = -1;
  linha("A ler " + f.name + " (" + f.size + " bytes), aos bocados de 1 MB…", "fraco");
  return KSHA.deBlob(f, { progresso: function (a, total) {
    var pct = total ? Math.floor(a * 100 / total) : 100;
    if (pct >= ultimoPct + 25) { ultimoPct = pct; linha("  " + pct + " %", "fraco"); }
  } }).then(function (r) {
    ultimo = { sha256: r.sha256, origem: "o ficheiro " + f.name };
    linha(r.sha256 + "  " + f.name);
    linha(r.bytes + " bytes · " + (Date.now() - t0) + " ms" + (r.confirmado ? " · conferido também com o motor do navegador" : ""), "fraco");
    if (aoFim) aoFim(r.sha256);
  });
}

function executar(m) {
  var texto = (m.linha || "").trim(), partes = texto.split(/\s+/), cmd = (partes[0] || "").toLowerCase();
  var resto = texto.slice(partes[0] ? partes[0].length : 0).replace(/^\s+/, "");
  if (cmd === "help" || cmd === "ajuda" || cmd === "?") { AJUDA.forEach(function (l) { linha(l); }); return Promise.resolve(); }
  if (cmd === "clear" || cmd === "limpar") { postMessage({ tipo: "limpar" }); return Promise.resolve(); }
  if (cmd === "versao" || cmd === "version") { linha(VERSAO); return Promise.resolve(); }
  if (cmd === "selftest") { selftest(); return Promise.resolve(); }
  if (cmd === "bigint-test" || cmd === "bigint") { bigintTest(); return Promise.resolve(); }
  if (cmd === "sha256") {
    if (m.ficheiro) return ficheiroSha(m.ficheiro);
    var r = shaTexto(resto);
    ultimo = { sha256: r.sha256, origem: "o texto" };
    linha(r.sha256 + "  (" + r.bytes + " bytes UTF-8)");
    return confirmarSubtle(resto, r.sha256).then(function (ok) { if (ok === true) linha("conferido também com o motor do navegador", "fraco"); else if (ok === false) linha("ATENÇÃO: o motor do navegador deu outro valor", "nao"); });
  }
  if (cmd === "verify") {
    var esperado = (partes[1] || "").toLowerCase();
    if (!hexValido(esperado)) { linha("verify precisa de um SHA-256 com 64 caracteres hexadecimais (0-9, a-f).", "nao"); return Promise.resolve(); }
    if (m.ficheiro) return ficheiroSha(m.ficheiro, function (h) { comparar(esperado, h, "o ficheiro " + m.ficheiro.name); });
    var depois = texto.replace(/^\S+\s+\S+\s?/, "");
    if (partes.length > 2) { var r2 = shaTexto(depois); ultimo = { sha256: r2.sha256, origem: "o texto" }; comparar(esperado, r2.sha256, "o texto"); return Promise.resolve(); }
    if (!ultimo) { linha("Ainda não calculaste nenhum SHA-256. Usa sha256 primeiro, ou verify <hash> <texto>.", "nao"); return Promise.resolve(); }
    comparar(esperado, ultimo.sha256, ultimo.origem);
    return Promise.resolve();
  }
  if (!cmd) return Promise.resolve();
  linha("Comando desconhecido: " + cmd + ". Escreve help.", "nao");
  return Promise.resolve();
}

onmessage = function (ev) {
  var m = ev.data || {};
  if (m.tipo !== "cmd") return;
  Promise.resolve().then(function () { return executar(m); })
    .catch(function (e) { linha("Erro: " + (e && e.message ? e.message : e), "nao"); })
    .then(function () { postMessage({ tipo: "fim", id: m.id }); });
};
