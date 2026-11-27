// Ensaio do Enxame (enxame_naves.html) num Chrome real, sem rede externa.
// Corre com: PLAYWRIGHT=<caminho do pacote playwright> CHROME=<caminho do chrome> node tests/ensaio_enxame.mjs [pagina.html]
// Cada "contexto" do navegador faz de telemóvel diferente; cada separador de um contexto é uma nave do mesmo aparelho.
import http from "node:http";
import { readFileSync, existsSync } from "node:fs";
import { join, dirname, extname, resolve, normalize, sep, basename } from "node:path";
import { fileURLToPath } from "node:url";
import { createRequire } from "node:module";

const require = createRequire(import.meta.url);
const { chromium } = require(process.env.PLAYWRIGHT || "playwright");
const AQUI = dirname(fileURLToPath(import.meta.url));
const ALVO = resolve(process.argv[2] || join(AQUI, "..", "enxame_naves.html"));
const RAIZ = dirname(ALVO), PAGINA = basename(ALVO);
const TIPOS = { ".html": "text/html; charset=utf-8", ".js": "text/javascript; charset=utf-8", ".json": "application/json", ".txt": "text/plain; charset=utf-8" };

let ok = 0, falhas = 0;
function prova(texto, cond, extra) { if (cond) ok++; else falhas++; console.log((cond ? "PASSA " : "FALHA ") + texto + (extra !== undefined && extra !== "" ? " — " + extra : "")); }
const espera = (ms) => new Promise((r) => setTimeout(r, ms));
async function ate(f, ms = 10000) { const t0 = Date.now(); for (;;) { try { const v = await f(); if (v) return v; } catch (e) {} if (Date.now() - t0 > ms) return false; await espera(150); } }

const srv = http.createServer((q, r) => {
  const p = normalize(decodeURIComponent(new URL(q.url, "http://x").pathname)).replace(/^[/\\]+/, "");
  const f = join(RAIZ, p);
  if (!(f + sep).startsWith(RAIZ + sep) || !existsSync(f)) { r.writeHead(404); return r.end(); }
  r.writeHead(200, { "content-type": TIPOS[extname(f)] || "application/octet-stream" }); r.end(readFileSync(f));
});
await new Promise((ok) => srv.listen(0, "127.0.0.1", ok));
const URL_P = `http://127.0.0.1:${srv.address().port}/${PAGINA}`;
const navegador = await chromium.launch({ executablePath: process.env.CHROME || "/usr/bin/google-chrome", headless: true });

const erros = [], pedidos = [];
function vigiar(p, nome) {
  p.on("pageerror", (e) => erros.push(nome + ": " + e.message));
  p.on("console", (m) => { if (m.type() === "error") erros.push(nome + " (consola): " + m.text()); });
  p.on("request", (q) => { if (/^https?:/.test(q.url())) pedidos.push({ nome, url: q.url() }); });
}
async function abrir(ctx, nome) { const p = await ctx.newPage(); vigiar(p, nome); await p.goto(URL_P); await p.waitForFunction(() => !!window.KENX); return p; }
const total = (p) => p.evaluate(() => window.KENX.total());
const textoDiario = (p) => p.locator("#diario").innerText();
async function lancar(p, t) { await p.fill("#texto", t); await p.click("#bLancar"); }

try {
  // 1. duas naves no mesmo aparelho
  const tel1 = await navegador.newContext();
  const A = await abrir(tel1, "A"), B = await abrir(tel1, "B");
  const marcaA = pedidos.length;
  prova("a página abre e o motor KSHA/2 dá o vetor NIST «abc»", await A.evaluate(() => KSHA.deTexto("abc")) === "ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad");
  const pkA = await A.evaluate(() => window.KENX.PK), pkB = await B.evaluate(() => window.KENX.PK);
  prova("cada separador é uma nave com chave própria", pkA !== pkB && /^[0-9a-f]{64}$/.test(pkA), pkA.slice(0, 8) + " ≠ " + pkB.slice(0, 8));
  prova("as duas naves veem-se sozinhas («1 nave por perto»)", await ate(async () => (await A.textContent("#pPerto")) === "1 nave por perto" && (await B.textContent("#pPerto")) === "1 nave por perto"));

  // 2. sinais nos dois sentidos
  await lancar(A, "Olá do A, sem rede.");
  prova("sinal de A chega a B, conferido", await ate(async () => (await textoDiario(B)).includes("Olá do A, sem rede.") && (await textoDiario(B)).includes("veio de uma nave por perto · selo conferido")));
  await lancar(B, "Resposta do B.");
  prova("sinal de B chega a A", await ate(async () => (await textoDiario(A)).includes("Resposta do B.")));

  // 3. modo avião
  await tel1.setOffline(true);
  prova("sem rede, o estado diz «Voo autónomo · sem rede»", await ate(async () => (await A.textContent("#pRede")) === "Voo autónomo · sem rede"));
  await lancar(A, "Em voo autónomo.");
  prova("sem rede, o sinal passa na mesma de A para B", await ate(async () => (await textoDiario(B)).includes("Em voo autónomo.")));
  await tel1.setOffline(false);

  // 4. nave que chega depois recebe o que ficou guardado
  const C = await abrir(tel1, "C");
  prova("nave nova recebe sozinha os 3 sinais guardados", await ate(async () => (await total(C)) === 3), String(await total(C)));

  // 5. botão «Abrir outra nave»: chave nova mesmo herdando a sessionStorage
  const [D] = await Promise.all([tel1.waitForEvent("page"), A.click("#bOutra")]);
  vigiar(D, "D"); await D.waitForLoadState(); await D.waitForFunction(() => !!window.KENX);
  const pkD = await D.evaluate(() => window.KENX.PK);
  prova("«Abrir outra nave» dá chave nova", pkD !== pkA && pkD !== pkB, pkD.slice(0, 8));
  prova("a nave aberta pelo botão recebe os 3 sinais", await ate(async () => (await total(D)) === 3));
  await D.close();

  // 6. portões: 112 só quando alguém escreve que está em perigo; crianças
  await A.fill("#texto", "estou em perigo");
  prova("escrever «estou em perigo» mostra o 112", (await A.textContent("#sosEu")).includes("112"));
  await A.fill("#texto", "não estou em perigo, está tudo bem");
  prova("«não estou em perigo» não mostra o 112", (await A.textContent("#sosEu")) === "");
  await A.fill("#texto", "I am in danger");
  prova("«I am in danger» mostra o 112 em inglês", (await A.textContent("#sosEu")).includes("Call 112"));
  await A.fill("#texto", "Olá, chego às 9h");
  prova("frase comum não mostra nada", (await A.textContent("#sosEu")) === "");
  await A.fill("#texto", "um adulto pede-me fotos e diz para não contar");
  prova("adulto que pede fotos mostra a linha para crianças", (await A.textContent("#sosEu")).includes("116 111"));
  await lancar(A, "Socorro, estou em perigo na estrada");
  prova("o pedido de ajuda chega a B com a nota do 112, em primeiro lugar", await ate(async () => { const li = B.locator("#diario li").first(); return (await li.innerText()).includes("Socorro, estou em perigo na estrada") && (await li.locator(".socorro").count()) === 1; }));
  prova("os sinais comuns não levam nota do 112", (await B.locator("#diario .socorro").count()) === 1);

  // 7. pacote por texto para outro telemóvel
  prova("antes de pedir, não há QR nem botões escondidos à vista", !(await A.isVisible("#qr")) && !(await A.isVisible("#bSeguintes")) && !(await A.isVisible("#bParar")) && !(await A.isVisible("#cam")));
  await A.click("#bMostrar");
  const info = await A.textContent("#pacoteInfo"), mi = info.match(/QR com os sinais 1 a (\d+) de (\d+)/);
  prova("o QR aparece; «Seguintes» só aparece se faltarem sinais", (await A.isVisible("#qr")) && !!mi && ((mi[1] !== mi[2]) === (await A.isVisible("#bSeguintes"))), info);
  const pacote = await A.inputValue("#pacoteTxt");
  prova("o pacote começa por KENX1:", pacote.startsWith("KENX1:"), pacote.length + " letras");
  const tel2 = await navegador.newContext(), E = await abrir(tel2, "E");
  prova("o outro telemóvel não vê as naves do primeiro (só por pacote)", (await E.textContent("#pPerto")) === "0 naves por perto");
  await E.fill("#colar", pacote); await E.click("#bJuntar");
  prova("o outro telemóvel junta os 4 sinais", (await E.textContent("#juntado")) === "4 novos · 0 já cá estavam · 0 recusados (não conferem)", await E.textContent("#juntado"));
  await E.fill("#colar", pacote.replace(/(.{40})/g, "$1\n")); await E.click("#bJuntar");
  prova("o mesmo pacote outra vez (com quebras de linha) não duplica", (await E.textContent("#juntado")) === "0 novos · 4 já cá estavam · 0 recusados (não conferem)", await E.textContent("#juntado"));

  // 8. pacote adulterado
  const lista = JSON.parse(Buffer.from(pacote.slice(6), "base64url").toString("utf8"));
  lista[0][2] = lista[0][2] + "!";
  const s = Buffer.from(lista[1][3], "base64url"); s[5] ^= 1; lista[1][3] = s.toString("base64url");
  const mau = "KENX1:" + Buffer.from(JSON.stringify(lista), "utf8").toString("base64url");
  const tel3 = await navegador.newContext(), G = await abrir(tel3, "G");
  await G.fill("#colar", mau); await G.click("#bJuntar");
  prova("texto mudado e assinatura mudada são recusados; os outros entram", (await G.textContent("#juntado")) === "2 novos · 0 já cá estavam · 2 recusados (não conferem)", await G.textContent("#juntado"));
  await G.fill("#colar", "olá"); await G.click("#bJuntar");
  prova("texto que não é pacote é recusado", (await G.textContent("#juntado")).startsWith("Isto não é um pacote do enxame"));
  await G.fill("#colar", "KENX1:@@@"); await G.click("#bJuntar");
  prova("pacote partido é recusado", (await G.textContent("#juntado")).startsWith("O pacote está partido"));

  // 9. sinal falsificado pelo canal entre separadores
  const antes = await total(A);
  await B.evaluate(() => { const c = new BroadcastChannel("konfirmu-enxame-v1"); const s = window.KENX.selar("falso"); s.texto = "texto trocado depois de assinar"; c.postMessage({ t: "sinal", pk: "f".repeat(64), s: s }); c.close(); });
  await espera(800);
  prova("sinal falsificado entre separadores não entra", (await total(A)) === antes && !(await textoDiario(A)).includes("texto trocado depois de assinar"));

  // 10. QR numa «foto»: o QR de A, rodado e desfocado sobre fundo escuro, lido noutro telemóvel
  const png = await A.evaluate(() => new Promise((ok) => {
    const q = document.getElementById("qr"), c = document.createElement("canvas"); c.width = 1400; c.height = 1050;
    const g = c.getContext("2d"); g.fillStyle = "#3a3a44"; g.fillRect(0, 0, c.width, c.height);
    g.translate(700, 525); g.rotate(0.14); g.filter = "blur(1px)"; const lado = 760; g.drawImage(q, -lado / 2, -lado / 2, lado, lado);
    c.toBlob((b) => { const r = new FileReader(); r.onload = () => ok(r.result.split(",")[1]); r.readAsDataURL(b); }, "image/png");
  }));
  const n_qr = await A.evaluate(() => { const m = document.getElementById("pacoteInfo").textContent.match(/QR com os sinais 1 a (\d+)/); return m ? Number(m[1]) : 0; });
  const tel4 = await navegador.newContext(), F = await abrir(tel4, "F");
  await F.setInputFiles("#foto", { name: "foto-do-qr.png", mimeType: "image/png", buffer: Buffer.from(png, "base64") });
  prova("QR fotografado (rodado e desfocado) é lido e os sinais conferem", await ate(async () => (await F.textContent("#juntado")) === n_qr + (n_qr === 1 ? " novo" : " novos") + " · 0 já cá estavam · 0 recusados (não conferem)"), (await F.textContent("#juntado")) + " · QR leva " + n_qr);

  // 11. a nave guarda o diário ao recarregar
  const deA = pedidos.slice(marcaA).filter((x) => x.nome === "A");
  prova("depois de aberta, a nave A não fez nenhum pedido à rede (todo o ensaio)", deA.length === 0, deA.length + " pedidos");
  const nA = await total(A);
  await A.reload(); await A.waitForFunction(() => !!window.KENX);
  prova("recarregar a página mantém a nave e o diário", (await A.evaluate(() => window.KENX.PK)) === pkA && (await total(A)) === nA, nA + " sinais");

  // 12. limpeza
  const fora = pedidos.filter((x) => !x.url.startsWith(URL_P.split("/").slice(0, 3).join("/") + "/"));
  prova("nenhuma página pediu nada fora do servidor de ensaio", fora.length === 0, fora.slice(0, 2).map((x) => x.url).join(" "));
  prova("nenhum erro nas páginas", erros.length === 0, erros.slice(0, 3).join(" | "));
} finally {
  await navegador.close(); srv.close();
}
console.log("\n" + ok + " de " + (ok + falhas) + " passam · página " + PAGINA);
process.exit(falhas ? 1 : 0);
