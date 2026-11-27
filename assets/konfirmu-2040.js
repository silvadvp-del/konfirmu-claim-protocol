/* konfirmu-2040.js — peça comum a todas as páginas da app (EUPL-1.2).
 * Ordem do David, 27-11-2026, 14:53:
 *   - Modo Criança 100 % fechado: só as tigelas da família; nenhuma saída para fora da app;
 *   - Tranca Parental: impressão digital ou rosto (WebAuthn, neste aparelho) ou PIN de 4 algarismos;
 *   - pausa de movimento e alto contraste, à escolha da pessoa, guardados neste aparelho.
 * Não fala com a rede. Não guarda o PIN: guarda só uma derivação PBKDF2-SHA-256 com sal (150 000 voltas).
 * É uma tranca para crianças, não um cofre: quem apagar os dados do navegador apaga também a tranca. */
(function () {
  "use strict";
  var CHAVE_MODO = "konfirmu.modoCrianca", CHAVE_TRANCA = "konfirmu.tranca", CHAVE_FALHAS = "konfirmu.tranca.falhas";
  var CHAVE_MOV = "konfirmu.semMovimento", CHAVE_CONTRASTE = "konfirmu.contraste";
  var raiz = document.documentElement;
  var meta = document.querySelector('meta[name="konfirmu-portal"]');
  var portal = meta ? meta.getAttribute("content") : "menu";
  var PERMITIDOS_CRIANCA = { fam: 1, menu: 1, info: 1 };

  function ler(k) { try { return localStorage.getItem(k); } catch (e) { return null; } }
  function guardar(k, v) { try { if (v === null) localStorage.removeItem(k); else localStorage.setItem(k, v); } catch (e) {} }
  function emCrianca() { return ler(CHAVE_MODO) === "1"; }

  /* ---------- preferências: movimento e contraste ---------- */
  function aplicarPreferencias() {
    raiz.classList.toggle("k-sem-movimento", ler(CHAVE_MOV) === "1");
    raiz.classList.toggle("k-contraste", ler(CHAVE_CONTRASTE) === "1");
    raiz.classList.toggle("k-crianca", emCrianca());
  }
  aplicarPreferencias();

  /* ---------- bytes, base64 e PBKDF2 ---------- */
  function aleatorio(n) { var u = new Uint8Array(n); crypto.getRandomValues(u); return u; }
  function b64(u8) { var s = ""; for (var i = 0; i < u8.length; i++) s += String.fromCharCode(u8[i]); return btoa(s); }
  function deb64(t) { var s = atob(t), u = new Uint8Array(s.length); for (var i = 0; i < s.length; i++) u[i] = s.charCodeAt(i); return u; }
  function b64u(u8) { return b64(u8).replace(/\+/g, "-").replace(/\//g, "_").replace(/=+$/, ""); }
  function deb64u(t) { t = t.replace(/-/g, "+").replace(/_/g, "/"); while (t.length % 4) t += "="; return deb64(t); }
  function iguais(a, b) { if (a.length !== b.length) return false; var d = 0; for (var i = 0; i < a.length; i++) d |= a[i] ^ b[i]; return d === 0; }
  function derivar(pin, sal, voltas) {
    if (!window.crypto || !crypto.subtle) return Promise.reject(new Error("sem-cripto"));
    return crypto.subtle.importKey("raw", new TextEncoder().encode(pin), "PBKDF2", false, ["deriveBits"]).then(function (k) {
      return crypto.subtle.deriveBits({ name: "PBKDF2", hash: "SHA-256", salt: sal, iterations: voltas }, k, 256);
    }).then(function (b) { return new Uint8Array(b); });
  }
  function tranca() { try { return JSON.parse(ler(CHAVE_TRANCA) || "null"); } catch (e) { return null; } }

  /* ---------- impressão digital / rosto (WebAuthn, só neste aparelho) ---------- */
  function bioDisponivel() {
    if (!window.PublicKeyCredential || !window.isSecureContext || !PublicKeyCredential.isUserVerifyingPlatformAuthenticatorAvailable) return Promise.resolve(false);
    return PublicKeyCredential.isUserVerifyingPlatformAuthenticatorAvailable().catch(function () { return false; });
  }
  function bioRegistar() {
    return navigator.credentials.create({ publicKey: {
      rp: { name: "Konfirmu" }, user: { id: aleatorio(16), name: "adulto", displayName: "Adulto da família" },
      challenge: aleatorio(32), pubKeyCredParams: [{ type: "public-key", alg: -7 }, { type: "public-key", alg: -257 }],
      authenticatorSelection: { authenticatorAttachment: "platform", userVerification: "required", residentKey: "discouraged" },
      timeout: 60000, attestation: "none" } }).then(function (c) { return b64u(new Uint8Array(c.rawId)); });
  }
  function bioConferir(id) {
    return navigator.credentials.get({ publicKey: { challenge: aleatorio(32), timeout: 60000, userVerification: "required",
      allowCredentials: [{ type: "public-key", id: deb64u(id), transports: ["internal"] }] } }).then(function (a) {
      var ad = new Uint8Array(a.response.authenticatorData);
      return (ad[32] & 0x05) === 0x05; /* a pessoa esteve presente (UP) e foi verificada (UV) */
    });
  }

  /* ---------- estilos dos diálogos (vidro, pêssego) ---------- */
  var css = document.createElement("style");
  css.textContent =
    ".k-veu{position:fixed;inset:0;z-index:2147483000;display:grid;place-items:center;padding:20px;background:rgba(5,12,22,.82);-webkit-backdrop-filter:blur(10px);backdrop-filter:blur(10px)}" +
    ".k-dialogo{width:min(420px,100%);max-height:92vh;overflow:auto;padding:22px 20px 18px;border-radius:22px;background:rgba(15,34,61,.92);border:1px solid rgba(255,158,125,.45);box-shadow:0 30px 80px -30px rgba(255,158,125,.55);color:#F4F7FA;font:400 1rem/1.5 system-ui,-apple-system,'Segoe UI',Roboto,sans-serif;text-align:center}" +
    ".k-dialogo h2{margin:4px 0 6px;font-size:1.25rem;line-height:1.25;color:#F4F7FA}.k-dialogo p{margin:6px 0;color:#9FB3C8}" +
    ".k-dialogo .k-linha{display:flex;flex-wrap:wrap;gap:8px;justify-content:center;margin-top:14px}" +
    ".k-dialogo button{min-height:48px;padding:0 18px;border-radius:12px;border:1px solid rgba(244,247,250,.2);background:rgba(11,25,44,.9);color:#F4F7FA;font:650 1rem/1 system-ui,sans-serif;cursor:pointer}" +
    ".k-dialogo button.k-principal{background:#FF9E7D;border-color:#FF9E7D;color:#0B192C}" +
    ".k-pontos{display:flex;gap:12px;justify-content:center;margin:12px 0 4px}.k-pontos i{width:14px;height:14px;border-radius:50%;border:1.5px solid #FF9E7D}.k-pontos i.k-cheio{background:#FF9E7D;box-shadow:0 0 14px rgba(255,158,125,.7)}" +
    ".k-teclado{display:grid;grid-template-columns:repeat(3,1fr);gap:8px;margin:12px auto 0;max-width:270px}.k-teclado button{min-height:56px;font-size:1.35rem}" +
    ".k-msg{min-height:1.5em;color:#FFD3C2;font-weight:600}" +
    ".k-aviso-crianca{position:fixed;left:50%;bottom:18px;transform:translateX(-50%);z-index:2147483001;padding:10px 16px;border-radius:12px;background:rgba(15,34,61,.95);border:1px solid #FF9E7D;color:#F4F7FA;font:600 .9375rem/1.3 system-ui,sans-serif}" +
    "html.k-crianca [data-adulto]{display:none!important}" +
    "html.k-crianca #t-pro,html.k-crianca #t-cid,html.k-crianca #p-pro,html.k-crianca #p-cid,html.k-crianca .procura{display:none!important}";
  (document.head || raiz).appendChild(css);

  function veu(conteudo, fechavel) {
    var v = document.createElement("div");
    v.className = "k-veu";
    var d = document.createElement("div");
    d.className = "k-dialogo"; d.setAttribute("role", "dialog"); d.setAttribute("aria-modal", "true");
    d.innerHTML = conteudo;
    v.appendChild(d);
    document.body.appendChild(v);
    var antes = document.activeElement;
    function fechar() { if (v.parentNode) v.parentNode.removeChild(v); if (antes && antes.focus) try { antes.focus(); } catch (e) {} }
    if (fechavel) v.addEventListener("keydown", function (e) { if (e.key === "Escape") fechar(); });
    var primeiro = d.querySelector("button");
    if (primeiro) setTimeout(function () { primeiro.focus(); }, 30);
    return { veu: v, caixa: d, fechar: fechar };
  }

  function aviso(texto) {
    var a = document.createElement("div");
    a.className = "k-aviso-crianca"; a.setAttribute("role", "status"); a.textContent = texto;
    document.body.appendChild(a);
    setTimeout(function () { if (a.parentNode) a.parentNode.removeChild(a); }, 2600);
  }

  /* ---------- teclado do PIN (4 algarismos) ---------- */
  function teclado(titulo, texto, aoFim, extraHtml) {
    var h = '<h2>' + titulo + '</h2><p>' + texto + '</p><div class="k-pontos" aria-hidden="true"><i></i><i></i><i></i><i></i></div>' +
      '<p class="k-msg" role="status" aria-live="polite"></p>' + (extraHtml || "") + '<div class="k-teclado">';
    for (var n = 1; n <= 9; n++) h += '<button type="button" data-d="' + n + '">' + n + '</button>';
    h += '<button type="button" data-k="apagar" aria-label="Apagar">&larr;</button><button type="button" data-d="0">0</button><button type="button" data-k="cancelar">Fechar</button></div>';
    var j = veu(h, true), pin = "";
    var pontos = j.caixa.querySelectorAll(".k-pontos i"), msg = j.caixa.querySelector(".k-msg");
    function mostrar() { for (var i = 0; i < 4; i++) pontos[i].classList.toggle("k-cheio", i < pin.length); }
    function tecla(d) {
      if (pin.length >= 4) return;
      pin += d; mostrar();
      if (pin.length === 4) { var p = pin; setTimeout(function () { aoFim(p, j, msg, function () { pin = ""; mostrar(); }); }, 120); }
    }
    j.caixa.addEventListener("click", function (e) {
      var b = e.target.closest("button"); if (!b) return;
      if (b.getAttribute("data-d") !== null) tecla(b.getAttribute("data-d"));
      else if (b.getAttribute("data-k") === "apagar") { pin = pin.slice(0, -1); mostrar(); }
      else if (b.getAttribute("data-k") === "cancelar") j.fechar();
    });
    j.veu.addEventListener("keydown", function (e) { if (/^[0-9]$/.test(e.key)) tecla(e.key); else if (e.key === "Backspace") { pin = pin.slice(0, -1); mostrar(); } });
    return j;
  }

  /* ---------- configurar a tranca e entrar no Modo Criança ---------- */
  function entrarModoCrianca() {
    if (tranca()) { ligar(); return; }
    var primeiro = null;
    teclado("Criar o PIN dos adultos", "Escolhe 4 algarismos. É o que abre o Modo Adulto.", function (p, j, msg, limpar) {
      if (primeiro === null) { primeiro = p; msg.textContent = "Escreve outra vez o mesmo PIN."; limpar(); return; }
      if (p !== primeiro) { primeiro = null; msg.textContent = "Os dois PIN não são iguais. Começa outra vez."; limpar(); return; }
      var sal = aleatorio(16), voltas = 150000;
      derivar(p, sal, voltas).then(function (h) {
        var t = { v: 1, sal: b64(sal), voltas: voltas, h: b64(h), cred: null };
        guardar(CHAVE_TRANCA, JSON.stringify(t));
        j.fechar();
        return bioDisponivel().then(function (ok) {
          if (!ok) { ligar(); return; }
          var q = veu('<h2>Usar também a impressão digital?</h2><p>Fica só neste aparelho. O PIN continua a servir.</p>' +
            '<div class="k-linha"><button type="button" class="k-principal" data-k="sim">Sim, usar</button><button type="button" data-k="nao">Agora não</button></div>', true);
          q.caixa.addEventListener("click", function (e) {
            var b = e.target.closest("button"); if (!b) return;
            if (b.getAttribute("data-k") === "sim") {
              bioRegistar().then(function (id) { t.cred = id; guardar(CHAVE_TRANCA, JSON.stringify(t)); q.fechar(); ligar(); })
                .catch(function () { q.fechar(); ligar(); });
            } else { q.fechar(); ligar(); }
          });
        });
      }).catch(function () { msg.textContent = "Este navegador não deixa criar a tranca aqui (abre a app pelo endereço https)."; limpar(); });
    });
  }

  function ligar() {
    guardar(CHAVE_MODO, "1");
    aplicarPreferencias();
    if (portal === "menu") { escolherFamilia(); desenharBotoes(); }
    else location.href = "./app_unica.html#p-fam";
  }

  /* ---------- sair do Modo Criança: impressão digital ou PIN ---------- */
  function espera() {
    var f = {}; try { f = JSON.parse(ler(CHAVE_FALHAS) || "{}"); } catch (e) {}
    return { n: f.n || 0, ate: f.ate || 0 };
  }
  function falhou() {
    var f = espera(); f.n += 1;
    if (f.n >= 10) f.ate = Date.now() + 5 * 60000; else if (f.n >= 5) f.ate = Date.now() + 30000;
    guardar(CHAVE_FALHAS, JSON.stringify(f));
    return f;
  }
  function sair() {
    var t = tranca();
    if (!t) { guardar(CHAVE_MODO, null); aplicarPreferencias(); desenharBotoes(); return; }
    var bio = t.cred && window.PublicKeyCredential && window.isSecureContext;
    var extra = bio ? '<div class="k-linha"><button type="button" class="k-principal" data-k="bio">Usar impressão digital</button></div>' : "";
    var j = teclado("Modo Adulto", "Pede a um adulto: impressão digital ou o PIN de 4 algarismos.", function (p, j2, msg, limpar) {
      var e = espera();
      if (e.ate > Date.now()) { msg.textContent = "Espera " + Math.ceil((e.ate - Date.now()) / 1000) + " s e tenta outra vez."; limpar(); return; }
      derivar(p, deb64(t.sal), t.voltas).then(function (h) {
        if (iguais(h, deb64(t.h))) { guardar(CHAVE_FALHAS, null); j2.fechar(); desligar(); }
        else { var f = falhou(); msg.textContent = f.ate > Date.now() ? "PIN errado. Espera um pouco antes de tentar." : "PIN errado."; limpar(); }
      }).catch(function () { msg.textContent = "Não foi possível conferir o PIN neste navegador."; limpar(); });
    }, extra);
    var b = j.caixa.querySelector('[data-k="bio"]');
    if (b) b.addEventListener("click", function () {
      bioConferir(t.cred).then(function (ok) { if (ok) { j.fechar(); desligar(); } else j.caixa.querySelector(".k-msg").textContent = "Não confirmou."; })
        .catch(function () { j.caixa.querySelector(".k-msg").textContent = "Impressão digital não disponível agora. Usa o PIN."; });
    });
  }
  function desligar() {
    guardar(CHAVE_MODO, null);
    aplicarPreferencias();
    var v = document.querySelector(".k-veu[data-bloqueio]"); if (v) v.parentNode.removeChild(v);
    soltarConteudo();
    desenharBotoes();
  }

  /* ---------- bloqueio das páginas de adultos ---------- */
  function prenderConteudo() {
    var filhos = document.body.children;
    for (var i = 0; i < filhos.length; i++) if (!filhos[i].classList.contains("k-veu")) { filhos[i].setAttribute("inert", ""); filhos[i].setAttribute("aria-hidden", "true"); filhos[i].setAttribute("data-k-preso", ""); }
  }
  function soltarConteudo() {
    var presos = document.querySelectorAll("[data-k-preso]");
    for (var i = 0; i < presos.length; i++) { presos[i].removeAttribute("inert"); presos[i].removeAttribute("aria-hidden"); presos[i].removeAttribute("data-k-preso"); }
  }
  function bloquear() {
    prenderConteudo();
    var j = veu('<h2>Esta parte é para adultos</h2><p>Estás no Modo Criança. As tigelas da família esperam por ti.</p>' +
      '<div class="k-linha"><button type="button" class="k-principal" data-k="tigelas">Voltar às tigelas</button><button type="button" data-k="adulto">Sou adulto</button></div>', false);
    j.veu.setAttribute("data-bloqueio", "");
    j.caixa.addEventListener("click", function (e) {
      var b = e.target.closest("button"); if (!b) return;
      if (b.getAttribute("data-k") === "tigelas") location.href = "./app_unica.html#p-fam";
      else sair();
    });
  }

  /* ---------- nenhuma saída para fora da app no Modo Criança ---------- */
  document.addEventListener("click", function (e) {
    if (!emCrianca()) return;
    var a = e.target.closest && e.target.closest("a[href]");
    if (!a) return;
    var url; try { url = new URL(a.getAttribute("href"), location.href); } catch (x) { return; }
    var fora = url.origin !== location.origin || a.target === "_blank" || /^(mailto|tel|sms|intent|whatsapp):/i.test(a.getAttribute("href"));
    if (fora) { e.preventDefault(); e.stopPropagation(); aviso("No Modo Criança não se sai da app."); }
  }, true);
  var abrir = window.open;
  window.open = function () { if (emCrianca()) { aviso("No Modo Criança não se sai da app."); return null; } return abrir.apply(window, arguments); };

  /* ---------- no menu: só o portal da família ---------- */
  function escolherFamilia() {
    var t = document.getElementById("t-fam");
    if (t && t.getAttribute("aria-selected") !== "true") t.click();
  }

  /* ---------- botões do rodapé ---------- */
  function desenharBotoes() {
    var sitio = document.getElementById("k-acoes");
    if (!sitio) return;
    var velhos = sitio.querySelectorAll("[data-k2040]");
    for (var i = 0; i < velhos.length; i++) velhos[i].parentNode.removeChild(velhos[i]);
    function botao(rotulo, premido, acao) {
      var b = document.createElement("button");
      b.type = "button"; b.textContent = rotulo; b.setAttribute("data-k2040", "");
      if (premido !== null) b.setAttribute("aria-pressed", premido ? "true" : "false");
      b.addEventListener("click", acao);
      sitio.appendChild(b);
    }
    botao("Pausar movimento", ler(CHAVE_MOV) === "1", function () { guardar(CHAVE_MOV, ler(CHAVE_MOV) === "1" ? null : "1"); aplicarPreferencias(); desenharBotoes(); });
    botao("Alto contraste", ler(CHAVE_CONTRASTE) === "1", function () { guardar(CHAVE_CONTRASTE, ler(CHAVE_CONTRASTE) === "1" ? null : "1"); aplicarPreferencias(); desenharBotoes(); });
    if (emCrianca()) botao("Sair do Modo Criança", null, sair);
    else botao("Modo Criança", null, entrarModoCrianca);
  }

  function arrancar() {
    desenharBotoes();
    if (emCrianca()) {
      if (!PERMITIDOS_CRIANCA[portal]) bloquear();
      else if (portal === "menu") escolherFamilia();
    }
  }
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", arrancar); else arrancar();

  /* para os ensaios automáticos (não muda nada sozinho) */
  window.KonfirmuModo = { emCrianca: emCrianca, portal: portal, sair: sair, entrar: entrarModoCrianca };
})();
