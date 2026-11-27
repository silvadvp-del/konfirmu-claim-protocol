// Constrói portal_familia_dual_mode.html (3D) num só ficheiro, sem rede. Sempre igual: duas corridas dão os mesmos bytes.
// Uso: node build.mjs PASTA
import { build } from "esbuild";
import fs from "node:fs";
import path from "node:path";
import crypto from "node:crypto";

const AQUI = path.dirname(new URL(import.meta.url).pathname);
const saida = path.resolve(process.argv[2] || "dist");
fs.mkdirSync(saida, { recursive: true });
const ler = (f) => fs.readFileSync(path.join(AQUI, f), "utf8");

// As 8 tigelas do portal Família (ordem e chaves do menu da outra janela, ramo claude/portal-familia-tigelas).
const ATIVIDADES = [
  { chave: "tutor", href: "Tutor-Girafinha-offline.html", expr: "pensativa", simbolo: "livro" },
  { chave: "quiz", href: "kcp_family_quiz.html", expr: "curiosa", simbolo: "pergunta" },
  { chave: "natal", href: "sala_natal_girafinhas.html", expr: "orgulhosa", simbolo: "estrela" },
  { chave: "video", href: "estudio_video_criancas.html", expr: "surpresa", simbolo: "filme" },
  { chave: "contas", href: "executor_criancas.html", expr: "sonolenta", simbolo: "contas" },
  { chave: "arte", href: "kcp_art_music_studio.html", expr: "risonha", simbolo: "musica" },
  { chave: "regua", href: "regua_do_planeta.html", expr: "feliz", simbolo: "globo" },
  { chave: "aventura", href: "neverland_family_quest.html", expr: "marota", simbolo: "bussola" },
];
const ORDEM_FILME = ["feliz", "curiosa", "risonha", "surpresa", "marota", "sonolenta", "pensativa", "orgulhosa"];

const pastaL = path.join(AQUI, "locales");
const linguas = [], menu = {};
for (const f of fs.readdirSync(pastaL).filter((x) => x.endsWith(".json")).sort()) {
  const d = JSON.parse(fs.readFileSync(path.join(pastaL, f), "utf8")), meta = d._meta;
  linguas.push({ c: meta.codigo, nome: meta.nome, dir: meta.dir, ia: meta.revisao !== "texto de origem" });
  menu[meta.codigo] = Object.fromEntries(Object.entries(d).filter(([k]) => !k.startsWith("_")).sort());
}
linguas.sort((a, b) => (a.c === "pt" ? -1 : b.c === "pt" ? 1 : a.nome.localeCompare(b.nome, "en")));
const textos = JSON.parse(ler("textos.json"));
const cenas = JSON.parse(ler("cenas.json")).map((c) => ({
  tipo: c.tipo, legenda: c.legenda, inicio: c.inicio, fim: c.fim, ate: c.ate, lema: c.lema, nota: c.nota,
  tigelas: c.tigelas.map((i) => ATIVIDADES.findIndex((a) => a.expr === ORDEM_FILME[i])),
}));
const dados = { linguas, menu, textos: { chaves: textos.chaves, linguas: Object.fromEntries(Object.entries(textos.linguas).map(([c, v]) => [c, { s: v.s }])) },
  cenas, atividades: ATIVIDADES, entrada: "girafinhas_criancas_facil.html" };
const dadosTxt = JSON.stringify(dados).replace(/</g, "\\u003c");

const r = await build({ entryPoints: [path.join(AQUI, "src/main.js")], bundle: true, minify: true, format: "iife", target: ["es2020"],
  write: false, legalComments: "none", charset: "utf8", absWorkingDir: AQUI });
const js = r.outputFiles[0].text.trim().replace(/<\/script/gi, "<\\/script");
const css = ler("src/estilo.css").trim();
const hash = (s) => "sha256-" + crypto.createHash("sha256").update(s, "utf8").digest("base64");
let html = ler("src/modelo.html");
html = html.replace("'__CSS__'", "'" + hash(css) + "'").replace("'__CSP__'", "'" + hash(js) + "'");
html = html.split("__ESTILO__").join(css).split("__DADOS__").join(dadosTxt);
const [a, b] = html.split("<script>__SCRIPT__</script>");
html = a + "<script>" + js + "</script>" + b;
const destino = path.join(saida, "portal_familia_dual_mode.html");
fs.writeFileSync(destino, html);
// Fonte completa (sem node_modules: refaz-se com «npm ci»), documentos e índice.
const FONTES = ["build.mjs", "render3d.py", "testar3d.py", "selar.py", "textos.json", "cenas.json", "package.json", "package-lock.json",
  "src/main.js", "src/modelo.html", "src/estilo.css"];
for (const f of FONTES) { fs.mkdirSync(path.dirname(path.join(saida, "fonte", f)), { recursive: true }); fs.copyFileSync(path.join(AQUI, f), path.join(saida, "fonte", f)); }
fs.mkdirSync(path.join(saida, "fonte", "locales"), { recursive: true });
for (const f of fs.readdirSync(pastaL).filter((x) => x.endsWith(".json")).sort()) fs.copyFileSync(path.join(pastaL, f), path.join(saida, "fonte", "locales", f));
const cenasOrig = JSON.parse(ler("cenas.json"));
fs.mkdirSync(path.join(saida, "filme"), { recursive: true });
fs.writeFileSync(path.join(saida, "filme", "STORYBOARD_FILME_3D.md"), ["# Filme Manifesto em 3D — storyboard (120 s)", "",
  "As mesmas 8 tigelas do portal, em 3D a sério (motor de jogo do navegador), com luz Pêssego Solar sobre Azul Abissal.",
  "Legendas do `MANIFESTO-MISSAO.md` (repositório público). A «régua aprovada» do filme não existe no OneDrive nem nos repositórios.",
  "Formato: 12 cenas de 10 s, 1280×720, 24 imagens por segundo, sem som, legendas em pt-PT.", "",
  "| Cena | Tempo | O que se vê | Legenda | Do manifesto |", "|---|---|---|---|---|",
  ...cenasOrig.map((c) => `| ${c.n} | ${c.inicio}–${c.fim} | ${c.plano} | ${c.legenda} | ${c.fonte} |`), "",
  "Ver: `filme_manifesto_3d.mp4`, ou no portal o botão «Filme» (corre ao vivo, no aparelho). Imagens: `storyboard/`, `prancha_storyboard_3d.jpg`.", "",
  "Por fazer: som (música e voz) e legendas noutras línguas.", ""].join("\n"));
fs.writeFileSync(path.join(saida, "00_INDICE.md"), ["# Modo Família 3D — tigelas, tranca de adulto e filme (27-11-2026)", "",
  "1. `portal_familia_dual_mode.html` — o ficheiro final, um só, sem rede: menu da Família com as 8 tigelas em 3D (62 línguas),",
  "   Modo Criança com tranca de adulto (PIN; impressão digital ou rosto por https) e o filme manifesto ao vivo.",
  "2. `tigelas/` — os 8 retratos 3D das tigelas (PNG 1024 px) e a prancha.",
  "3. `filme/` — o filme em vídeo (MP4), o storyboard e as imagens das 12 cenas.",
  "4. `provas/` — capturas no telemóvel (390×844) e o resultado dos testes.",
  "5. `fonte/` — o código. Refaz-se, sempre igual: `npm ci`, `node build.mjs PASTA`, `python3 render3d.py PASTA`, `python3 testar3d.py PASTA`, `python3 selar.py PASTA`.",
  "6. `LEIA-ME_FABLE52.md` — como integrar em `KONFIRMU_FINAL_NL/konfirmu/`.",
  "7. `SHA256SUMS.txt` — o hash de cada ficheiro. Verificar: `shasum -a 256 -c SHA256SUMS.txt`.", "",
  "Paleta única: Azul Abissal #0B192C, vidro rgba(15, 34, 61, 0.72), Pêssego Solar #FF9E7D, Branco Titânio #F4F7FA, Cinza Nevoeiro #9FB3C8. Zero emojis.",
  "Línguas: o menu nas 62 da outra janela; as frases da tranca em 27 (as outras 35 em inglês, até haver tradução). Traduções feitas por IA, por rever.",
  "Estado: em ensaio, ainda não validado.", ""].join("\n"));
fs.writeFileSync(path.join(saida, "LEIA-ME_FABLE52.md"), ["# Para o Fable 5.2 — integrar em KONFIRMU_FINAL_NL", "",
  "1. Copia `portal_familia_dual_mode.html` tal e qual para `KONFIRMU_FINAL_NL/konfirmu/` (raiz do pacote). Não o refaças: o hash tem de bater com `SHA256SUMS.txt`.",
  "2. As 8 tigelas e a entrada ligam a estes ficheiros, na mesma pasta: " + ATIVIDADES.map((a) => "`" + a.href + "`").join(", ") + " e `girafinhas_criancas_facil.html`. Se algum faltar no pacote, diz «não existe» no recibo; não inventes.",
  "3. No menu da Família do pacote, um cartão «Modo Criança» que abre `portal_familia_dual_mode.html` (ícone de linha 1,5 px, sem emoji).",
  "4. No `sw.js` do pacote: acrescenta `./portal_familia_dual_mode.html` à lista e muda o nome da cache (para chegar a quem já tem a versão anterior).",
  "5. Prova: abre em modo avião (100 %), mede a RAM (aqui: memória JavaScript bem abaixo de 64 MB) e corre `python3 fonte/testar3d.py` sobre a pasta.",
  "6. A tranca guarda só o hash do PIN com sal (`localStorage`, chave `konfirmu_familia_v1`). A biometria só aparece por https.",
  "7. Paleta e emojis: o ficheiro já passa a contagem (só as 5 cores; 0 emojis). A biblioteca three.js traz por dentro a tabela de nomes de cores do CSS: não é usada.", ""].join("\n"));
const licenca = fs.readFileSync(path.join(AQUI, "node_modules/three/LICENSE"), "utf8");
fs.writeFileSync(path.join(saida, "LICENCA_THREE_JS.txt"), "O motor 3D é o three.js r187 (licença MIT), embutido no ficheiro.\n\n" + licenca);
console.log("ok", destino, html.length, "bytes; script", js.length, "; dados", dadosTxt.length);
