#!/usr/bin/env python3
"""Empacotador offline da Konfirmu -> KONFIRMU_EXECUTAVEL_OFFLINE_2030.zip  (EUPL-1.2)

Python 3.9 ou mais recente, só a biblioteca padrão, sem rede. Determinista: o mesmo
commit (e a mesma base) dá o mesmo ZIP, byte a byte.

Uso:
  python3 scripts/build_pacote_offline.py                        # só com o que está neste repositório
  python3 scripts/build_pacote_offline.py --base App-Unica-21.zip # junta a edição integrada (menu, Quiz, Tutor)
  python3 scripts/build_pacote_offline.py --verificar dist/KONFIRMU_EXECUTAVEL_OFFLINE_2030.zip

Regra de junção com --base (cada ficheiro fica registado em PACOTE.json, com a origem e o hash):
  * só existe num lado               -> entra esse
  * existe nos dois e é igual        -> entra (igual)
  * existe nos dois e é diferente    -> ganha o repositório (tem as correções aprovadas e ensaiadas),
                                        exceto app_unica.html, index.html e manifest.json, que vêm da base
                                        (são o menu e a identidade da edição integrada)
  * sw.js                            -> gerado aqui, com a lista exata do que vai no pacote

O pacote falha (não se faz) se: faltar uma página do menu ou uma dependência local, sobrar uma
chamada para fora do aparelho, ou o ZIP não conferir com o SHA256SUMS.txt depois de escrito.
"""
from __future__ import annotations

from html.parser import HTMLParser

import argparse
import hashlib
import io
import json
import os
import re
import subprocess
import sys
import time
import zipfile
from pathlib import Path, PurePosixPath

VERSAO = "1.0.0"
NOME_ZIP = "KONFIRMU_EXECUTAVEL_OFFLINE_2030.zip"
PASTA_TOPO = "KONFIRMU_OFFLINE_2030"
PAGINA_INICIAL = "app_unica.html"
# Têm de entrar sempre. Além destas, entra tudo o que o menu (app_unica.html) liga.
PAGINAS_OBRIGATORIAS = ["app_unica.html", "verificador_offline.html", "chronolex_verify.html",
                        "chronolex_photo_seal.html", "estudio_video_criancas.html"]
PREFERIR_BASE = {"app_unica.html", "index.html", "manifest.json"}
# Ficheiros de prova da casa (as linhas 1 e 4 do verificador) e a licença.
EXTRA_REPO = {"LICENSE.txt": "LICENSE.txt", "konfirmu_calc.py": "prova/konfirmu_calc.py",
              "anchors/konfirmu_calc.tsr": "prova/anchors/konfirmu_calc.tsr",
              "anchors/konfirmu_calc.tsq": "prova/anchors/konfirmu_calc.tsq"}
EXECUTAVEIS = {"ABRIR_KONFIRMU_OFFLINE.command", "abrir_konfirmu_offline.sh", "servidor_local.py"}
TEXTO = (".html", ".js", ".mjs", ".json", ".css", ".txt", ".md", ".py", ".command", ".sh", ".bat", ".webmanifest")
RTL_LINGUAS = {"ar", "he", "fa", "ur", "ps", "sd", "ug", "yi", "dv", "ckb"}
# Bloqueia no navegador qualquer ligação para fora do aparelho, mesmo implícita (ex.: modelos remotos).
CSP = ("default-src 'self'; script-src 'self' 'unsafe-inline' 'wasm-unsafe-eval'; style-src 'self' 'unsafe-inline'; "
       "img-src 'self' data: blob:; media-src 'self' data: blob: mediastream:; connect-src 'self' data: blob:; "
       "worker-src 'self' blob:; font-src 'self' data:; object-src 'none'; base-uri 'self'; form-action 'self'; frame-src 'none'")


class Falha(Exception):
    pass


def sha256(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


# ---------------------------------------------------------------- fontes
# Destinos da edição integrada de 21 atividades.
ATIVIDADES_21 = {
    "Tutor-Girafinha-offline.html",
    "carta_selada.html",
    "chronolex_ata.html",
    "chronolex_photo_seal.html",
    "chronolex_verify.html",
    "estudio_video_criancas.html",
    "executor_criancas.html",
    "ficha_campo.html",
    "girafinhas_criancas_facil.html",
    "kcp_art_music_studio.html",
    "kcp_family_quiz.html",
    "konfirmu_chat_offline.html",  # KON-608 (28-11): o chat do menu é o que tem o portão do 112; a v0.1 fica no repositório
    "neverland_family_quest.html",
    "patient_vault_offline.html",
    "radio_selo.html",
    "regua_do_planeta.html",
    "sala_natal_girafinhas.html",
    "testemunha_offline.html",
    "urna_voto_offline.html",
    "verificador_offline.html",
    "webrtc_local.html",
}


class MenuIntegrado(HTMLParser):
    def __init__(self):
        super().__init__()
        self.destinos = set()

    def handle_starttag(self, tag, attrs):
        if tag == "a":
            href = dict(attrs).get("href") or ""
            self.destinos.add(href[2:] if href.startswith("./") else href)


def conferir_menu_integrado(inicio):
    menu = MenuIntegrado()
    menu.feed(inicio.decode("utf-8"))
    menu.close()
    ausentes = sorted(ATIVIDADES_21 - menu.destinos)
    if ausentes:
        raise Falha("atividades ausentes do menu integrado: " + ", ".join(ausentes))


def ler_base(caminho: Path) -> dict:
    """Lê a edição integrada: um ZIP com site/ (como App-Unica-21.zip) ou uma pasta site."""
    ficheiros = {}
    if caminho.is_file():
        with zipfile.ZipFile(caminho) as z:
            for i in z.infolist():
                if i.is_dir():
                    continue
                p = PurePosixPath(i.filename)
                if p.parts and p.parts[0] == "site" and len(p.parts) > 1:
                    ficheiros[str(PurePosixPath(*p.parts[1:]))] = z.read(i)
        if not ficheiros:
            raise Falha(f"{caminho}: não tem a pasta site/")
    else:
        for f in sorted(caminho.rglob("*")):
            if f.is_file():
                ficheiros[f.relative_to(caminho).as_posix()] = f.read_bytes()
    return ficheiros


def ler_repo(repo: Path) -> dict:
    ficheiros = {}
    for f in sorted(repo.glob("*.html")) + sorted((repo / "assets").glob("*")) + [repo / "manifest.json"]:
        if f.is_file():
            ficheiros[f.relative_to(repo).as_posix()] = f.read_bytes()
    return ficheiros


# ---------------------------------------------------------------- referências
RE_ATTR = re.compile(r"""<(?:script|link|img|audio|video|source|iframe|embed|track|a|area|object|input|form)\b[^>]*?\s(?:src|href|data|poster|action|formaction)\s*=\s*["']([^"']+)["']""", re.I)
RE_JS = re.compile(r"""(?:\bimport\s*\(\s*|\bfrom\s+|\bimportScripts\s*\(\s*|\bfetch\s*\(\s*|\bnew\s+(?:Shared)?Worker\s*\(\s*|\.register\s*\(\s*|\bnew\s+(?:WebSocket|EventSource)\s*\(\s*|\bsendBeacon\s*\(\s*)["'`]([^"'`]+)["'`]""")
RE_CSS = re.compile(r"""url\(\s*["']?([^"')]+)["']?\s*\)""", re.I)
RE_URL_TEXTO = re.compile(r"""(?:https?:)?//[a-z0-9][a-z0-9.-]*\.[a-z]{2,}[^\s"'`)<>]*""", re.I)
RE_ICE = re.compile(r"""\b(?:stun|turns?):[^\s"'`]+""", re.I)


def externa(u: str) -> bool:
    return bool(re.match(r"^(?:[a-z][a-z0-9+.-]*:)?//", u, re.I)) or u.lower().startswith(("http:", "https:", "ws:", "wss:", "ftp:"))


def ignorar(u: str) -> bool:
    return u.startswith(("#", "data:", "blob:", "mailto:", "tel:", "javascript:", "about:")) or "${" in u


def referencias(nome: str, conteudo: str):
    """Devolve (locais, externas) que o navegador vai buscar sozinho ou ao carregar num botão."""
    achados = []
    if nome.endswith(".html"):
        achados += RE_ATTR.findall(conteudo)
        for bloco in re.findall(r"<script\b[^>]*>(.*?)</script>", conteudo, re.S | re.I):
            achados += RE_JS.findall(bloco)
        for bloco in re.findall(r"<style\b[^>]*>(.*?)</style>", conteudo, re.S | re.I):
            achados += RE_CSS.findall(bloco)
    elif nome.endswith((".js", ".mjs")):
        achados += RE_JS.findall(conteudo)
    elif nome.endswith(".css"):
        achados += RE_CSS.findall(conteudo)
    locais, fora = set(), set()
    for u in achados:
        u = u.strip()
        if not u or ignorar(u):
            continue
        if externa(u):
            fora.add(u)
        else:
            alvo = (PurePosixPath(nome).parent / u.split("#")[0].split("?")[0]).as_posix()
            alvo = os.path.normpath(alvo).replace("\\", "/")
            if alvo not in (".", ""):
                locais.add(alvo)
    fora |= set(RE_ICE.findall(conteudo))
    return locais, fora


def mencoes(conteudo: str):
    """URLs escritas em texto ou comentários (não são chamadas, ficam só no relatório)."""
    return sorted(set(m.group(0) for m in RE_URL_TEXTO.finditer(conteudo)))


# ---------------------------------------------------------------- transformações
IA_MSG = ("{pt:'A IA local (Qwen) não vem neste pacote: o modelo tem centenas de MB. O resto do chat funciona sem rede.',"
          "en:'The local AI (Qwen) is not in this package: the model is hundreds of MB. The rest of the chat works offline.',"
          "fr:'L\\'IA locale (Qwen) n\\'est pas dans ce paquet : le modèle fait des centaines de Mo. Le reste du chat fonctionne hors ligne.'}")
RE_CDN_IA = re.compile(r"""import\(\s*['"]https://cdn\.jsdelivr\.net/npm/@huggingface/transformers@[^'"]*['"]\s*\)""")
# Desde 27-11 (KON-577) o chat busca os ficheiros da IA a IA_BASE e confere-os por hash (IA_FIXOS).
RE_IA_BASE = re.compile(r"""(const\s+IA_BASE\s*=\s*)['"]https://cdn\.jsdelivr\.net/npm/@huggingface/transformers@[^'"]*['"]""")


def tratar_ia(nome: str, t: str, com_ia: bool, registo: list) -> str:
    if not (RE_CDN_IA.search(t) or RE_IA_BASE.search(t)):
        return t
    if "async function ligarIA(){" not in t:
        raise Falha(f"{nome}: chama a IA da CDN mas não encontro ligarIA() para a tratar")
    t = RE_CDN_IA.sub("import('./assets/ia/transformers.min.js')", t)
    t = RE_IA_BASE.sub(r"\1'./assets/ia/'", t)  # os mesmos ficheiros, conferidos pelo mesmo hash, mas do próprio pacote
    if com_ia:
        t = t.replace("ia=await m.pipeline(", "m.env.allowRemoteModels=false;m.env.allowLocalModels=true;m.env.localModelPath='./modelos/';"
                      "m.env.backends.onnx.wasm.wasmPaths='./assets/ia/';ia=await m.pipeline(", 1)
        registo.append(f"{nome}: IA local a partir de ./assets/ia e ./modelos (sem CDN)")
    else:
        t = t.replace("async function ligarIA(){", "async function ligarIA(){bolha('casa'," + IA_MSG + "[L]);return;", 1)
        registo.append(f"{nome}: IA da CDN retirada; o botão IA explica que o modelo não vem no pacote")
    return t


def tratar_sw(nome: str, t: str, registo: list) -> str:
    """No pacote há um só service worker (o gerado): o chat deixa de registar o seu."""
    novo, n = re.subn(r"""serviceWorker\.register\(\s*(['"])(?:\./)?konfirmu_chat_sw\.js\1""", "serviceWorker.register('./sw.js'", t)
    if n:
        registo.append(f"{nome}: regista o service worker do pacote (um só para tudo)")
    return novo


def tratar_rtl(nome: str, t: str, registo: list) -> str:
    """Só em páginas RTL: envolve números em <bdi dir="ltr"> no texto (nunca em script/style/textarea/pre/code)."""
    m = re.search(r"<html\b[^>]*>", t, re.I)
    cab = m.group(0) if m else ""
    lang = (re.search(r"""lang\s*=\s*["']?([a-zA-Z-]+)""", cab) or [None, ""])[1].split("-")[0].lower()
    if not (re.search(r"""dir\s*=\s*["']?rtl""", cab, re.I) or lang in RTL_LINGUAS):
        return t
    partes = re.split(r"(<script\b.*?</script>|<style\b.*?</style>|<textarea\b.*?</textarea>|<pre\b.*?</pre>|<code\b.*?</code>|<bdi\b.*?</bdi>|<!--.*?-->|<[^>]+>)", t, flags=re.S | re.I)
    num = re.compile(r"(?<![\w<])([+\-−]?\d+(?:[.,]\d+)*(?:\s?[×x]\s?10[⁰¹²³⁴⁵⁶⁷⁸⁹⁻]+|[eE][+\-−]?\d+)?(?:\s?%)?)")
    n = 0
    for i in range(0, len(partes), 2):
        partes[i], k = num.subn(r'<bdi dir="ltr">\1</bdi>', partes[i])
        n += k
    registo.append(f"{nome}: página RTL, {n} números envolvidos em <bdi>")
    return "".join(partes)


def por_csp(nome: str, t: str) -> str:
    if 'http-equiv="Content-Security-Policy"' in t:
        return t
    meta = f'<meta http-equiv="Content-Security-Policy" content="{CSP}">'
    m = re.search(r"<meta\s+charset[^>]*>", t, re.I)
    if m:
        return t[:m.end()] + "\n" + meta + t[m.end():]
    m = re.search(r"<head\b[^>]*>", t, re.I)
    if not m:
        raise Falha(f"{nome}: não tem <head> para a regra de rede")
    return t[:m.end()] + "\n" + meta + t[m.end():]


def gerar_sw(lista: list, chave: str) -> bytes:
    allow = json.dumps(["./" + p for p in lista], ensure_ascii=False)
    return f"""// sw.js do pacote offline — gerado por scripts/build_pacote_offline.py v{VERSAO}. Não editar à mão.
// Guarda todas as páginas do pacote na 1.ª visita; depois abre sem rede e sem servidor.
const allow = {allow}.map(p => new URL(p, self.registration.scope).href);
const prefix = 'konfirmu:' + self.registration.scope + ':';
const key = prefix + '{chave}';
self.addEventListener('install', e => e.waitUntil(caches.open(key).then(c => c.addAll(allow)).then(() => self.skipWaiting())));
self.addEventListener('activate', e => e.waitUntil(caches.keys().then(ks => Promise.all(ks.filter(k => k.startsWith(prefix) && k !== key).map(k => caches.delete(k)))).then(() => self.clients.claim())));
self.addEventListener('fetch', e => {{
  if (e.request.method !== 'GET') return;
  const u = e.request.url.split('#')[0].split('?')[0];
  if (u === self.registration.scope + 'favicon.ico') {{ e.respondWith(new Response(null, {{ status: 204 }})); return; }}
  if (u === self.registration.scope) {{ e.respondWith(caches.open(key).then(c => c.match(new URL('index.html', self.registration.scope).href)).then(r => r || fetch(e.request))); return; }}
  if (allow.includes(u)) e.respondWith(caches.open(key).then(c => c.match(u)).then(r => r || fetch(e.request)));
}});
""".encode("utf-8")


SERVIDOR = r'''#!/usr/bin/env python3
"""Konfirmu offline — servidor só deste computador (127.0.0.1). Python 3.9+, biblioteca padrão.
Não regista nada, não fala com a internet, não aceita ligações de outros aparelhos."""
import http.server, os, socket, sys, threading, urllib.request, webbrowser

PASTA = os.path.dirname(os.path.abspath(__file__))
PORTAS = range(8765, 8776)
TIPOS = {".html": "text/html; charset=utf-8", ".js": "text/javascript; charset=utf-8", ".mjs": "text/javascript; charset=utf-8",
         ".json": "application/json; charset=utf-8", ".webmanifest": "application/manifest+json", ".wasm": "application/wasm",
         ".onnx": "application/octet-stream", ".css": "text/css; charset=utf-8", ".svg": "image/svg+xml", ".png": "image/png",
         ".jpg": "image/jpeg", ".webp": "image/webp", ".txt": "text/plain; charset=utf-8", ".md": "text/plain; charset=utf-8",
         ".py": "text/plain; charset=utf-8", ".tsr": "application/timestamp-reply", ".tsq": "application/timestamp-query"}


class Pedido(http.server.SimpleHTTPRequestHandler):
    extensions_map = dict(http.server.SimpleHTTPRequestHandler.extensions_map, **TIPOS)

    def __init__(self, *a, **k):
        super().__init__(*a, directory=PASTA, **k)

    def end_headers(self):
        self.send_header("Cache-Control", "no-cache")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("Referrer-Policy", "no-referrer")
        self.send_header("Cross-Origin-Opener-Policy", "same-origin")
        super().end_headers()

    def do_GET(self):
        if self.path.split("?")[0] == "/favicon.ico":  # o navegador pede-o sozinho; a casa não tem ícone (sem 404)
            self.send_response(204)
            self.end_headers()
            return
        super().do_GET()

    def log_message(self, *a):  # zero registos
        pass


def ja_a_correr(porta):
    try:
        with urllib.request.urlopen(f"http://127.0.0.1:{porta}/PACOTE.json", timeout=1) as r:
            return b"KONFIRMU_OFFLINE_2030" in r.read(4096)
    except Exception:
        return False


def main():
    abrir = os.environ.get("KONFIRMU_SEM_NAVEGADOR") != "1"
    for porta in PORTAS:
        if ja_a_correr(porta):
            print(f"A Konfirmu já está aberta em http://127.0.0.1:{porta}/")
            if abrir:
                webbrowser.open(f"http://127.0.0.1:{porta}/")
            return
        try:
            srv = http.server.ThreadingHTTPServer(("127.0.0.1", porta), Pedido)
        except OSError:
            continue
        url = f"http://127.0.0.1:{porta}/"
        print(f"Konfirmu offline em {url}  (só neste computador). Para parar, fecha esta janela.", flush=True)
        if abrir:
            threading.Timer(0.6, lambda: webbrowser.open(url)).start()
        try:
            srv.serve_forever()
        except KeyboardInterrupt:
            pass
        return
    print("Não encontrei uma porta livre entre 8765 e 8775.")
    sys.exit(1)


if __name__ == "__main__":
    main()
'''

COMMAND = """#!/bin/bash
# Konfirmu offline — duplo clique no Mac. Abre a app no navegador, só neste computador.
cd "$(dirname "$0")" || exit 1
PY=""
for c in /opt/homebrew/bin/python3 /usr/local/bin/python3 /Library/Frameworks/Python.framework/Versions/Current/bin/python3; do
  if [ -x "$c" ]; then PY="$c"; break; fi
done
if [ -z "$PY" ] && [ -x /usr/bin/python3 ] && xcode-select -p >/dev/null 2>&1; then PY=/usr/bin/python3; fi
if [ -n "$PY" ]; then exec "$PY" servidor_local.py; fi
echo "Não encontrei Python 3. Abro a app diretamente: funciona quase tudo, menos o modo offline guardado."
open "app_unica.html"
"""

SH = """#!/bin/sh
# Konfirmu offline — Linux. Abre a app no navegador, só neste computador.
cd "$(dirname "$0")" || exit 1
if command -v python3 >/dev/null 2>&1; then exec python3 servidor_local.py; fi
xdg-open app_unica.html
"""

BAT = "\r\n".join([
    "@echo off",
    "rem Konfirmu offline - Windows. Abre a app no navegador, so neste computador.",
    'cd /d "%~dp0"',
    "where py >nul 2>nul && (py -3 servidor_local.py & goto :fim)",
    'python -c "import sys; sys.exit(0 if sys.version_info >= (3, 9) else 1)" >nul 2>nul && (python servidor_local.py & goto :fim)',
    "echo Nao encontrei Python 3. Abro a app diretamente.",
    'start "" "app_unica.html"',
    ":fim", ""])

LEIA_ME = """KONFIRMU OFFLINE 2030 — como abrir

1. Abre a pasta {topo}.
2. Mac: duplo clique em ABRIR_KONFIRMU_OFFLINE.command
   Se o Mac disser «programador não identificado»: botão direito no ficheiro, Abrir, Abrir.
   Windows: ABRIR_KONFIRMU_OFFLINE.bat · Linux: abrir_konfirmu_offline.sh
3. A app abre no navegador em http://127.0.0.1:8765/ — isto é só o teu computador.
4. Para parar, fecha a janela do Terminal.

Depois da 1.ª abertura, a app abre também sem rede e sem o Terminal (modo avião).
Todas as páginas trazem uma regra que impede o navegador de falar com outros sítios.

O que vem: {n} páginas (o menu da app única e tudo o que ele abre){extra}.
O que não vem: a IA local (Qwen) do chat — o modelo tem centenas de MB.

Conferir que nada mudou (dentro desta pasta, no Terminal):
   shasum -a 256 -c SHA256SUMS.txt
O SHA-256 do ZIP inteiro está no ficheiro .sha256 ao lado do ZIP.

O que isto NÃO garante: o SHA-256 prova que os bytes são os mesmos. Não certifica o conteúdo.
SELADO ≠ VERDADEIRO.
"""


# ---------------------------------------------------------------- construção
def commit_info(repo: Path):
    try:
        h = subprocess.run(["git", "-C", str(repo), "rev-parse", "HEAD"], capture_output=True, text=True, check=True).stdout.strip()
        ts = int(subprocess.run(["git", "-C", str(repo), "log", "-1", "--format=%ct"], capture_output=True, text=True, check=True).stdout.strip())
        sujo = bool(subprocess.run(["git", "-C", str(repo), "status", "--porcelain", "--untracked-files=no"], capture_output=True, text=True).stdout.strip())
        return h, ts, sujo
    except Exception:
        return "sem-git", 1795737600, None  # 2026-11-27T00:00:00Z


def construir(repo: Path, base: Path | None, com_ia: Path | None, edicao_21: bool = False):
    registo, origens = [], []
    repo_f = ler_repo(repo)
    base_f = ler_base(base) if base else {}
    base_sha = sha256(base.read_bytes()) if base and base.is_file() else (str(base) if base else None)

    def escolher(p):
        a, b = repo_f.get(p), base_f.get(p)
        if a is not None and b is not None:
            if a == b:
                return a, "igual nos dois"
            if p in PREFERIR_BASE:
                return b, "base (menu/identidade da edição integrada)"
            return a, "repositório (diferente da base: ganha a versão corrigida)"
        if b is not None:
            return b, "só na base"
        if a is not None:
            return a, "só no repositório"
        return None, None

    inicio, _ = escolher(PAGINA_INICIAL)
    if inicio is None:
        raise Falha(f"falta a página inicial {PAGINA_INICIAL}")
    if edicao_21:
        conferir_menu_integrado(inicio)
    # Percorre o menu e as dependências a partir da página inicial.
    a_visitar = [PAGINA_INICIAL, "index.html", "manifest.json"] + PAGINAS_OBRIGATORIAS
    pacote, falta = {}, []
    while a_visitar:
        p = a_visitar.pop(0)
        if p in pacote or p in ("sw.js", "konfirmu_chat_sw.js"):  # o pacote gera o seu próprio service worker
            continue
        conteudo, origem = escolher(p)
        if conteudo is None:
            if p in ("index.html",):
                continue
            falta.append(p)
            continue
        pacote[p] = conteudo
        origens.append({"ficheiro": p, "origem": origem, "sha256": sha256(conteudo),
                        "sha256_repositorio": sha256(repo_f[p]) if p in repo_f else None,
                        "sha256_base": sha256(base_f[p]) if p in base_f else None})
        # O menu de uma base antiga conserva as suas atividades e recebe o visualizador atual.
        if p in ("app_unica.html", "index.html") and p in base_f:
            html = pacote[p].decode("utf-8")
            if 'class="grid"' in html and 'src="./assets/imersao.js"' not in html:
                menu_atual = repo_f.get(PAGINA_INICIAL, b"").decode("utf-8")
                recursos = re.findall(r'<(?:link|script)\b[^>]*(?:href|src)="\./assets/imersao\.(?:js|css)"[^>]*>(?:</script>)?', menu_atual)
                html = html.replace("</head>", "\n".join(recursos) + "\n</head>", 1)
                conteudo = pacote[p] = html.encode("utf-8")
                registo.append(f"{p}: imersão 3D no menu da edição integrada")
        if p.endswith(TEXTO):
            locais, _ = referencias(p, conteudo.decode("utf-8"))
            a_visitar += sorted(x for x in locais if x != "sw.js" and not x.startswith("assets/ia/") and not x.startswith("modelos/"))
    if falta:
        raise Falha("faltam ficheiros referidos pelo menu ou pelas páginas: " + ", ".join(sorted(set(falta))))
    if "index.html" not in pacote:
        pacote["index.html"] = b'<!DOCTYPE html><meta charset="utf-8"><title>Konfirmu</title><meta http-equiv="refresh" content="0; url=app_unica.html"><a href="app_unica.html">Konfirmu</a>\n'
        origens.append({"ficheiro": "index.html", "origem": "gerado (abre app_unica.html)", "sha256": sha256(pacote["index.html"])})

    # Transformações (só no pacote; o repositório não muda).
    for p in sorted(pacote):
        if p.endswith(".html"):
            t = pacote[p].decode("utf-8")
            t = tratar_ia(p, t, bool(com_ia), registo)
            t = tratar_sw(p, t, registo)
            t = tratar_rtl(p, t, registo)
            t = por_csp(p, t)
            pacote[p] = t.encode("utf-8")
    paginas_rtl = sum(1 for r in registo if "página RTL" in r)

    if com_ia:
        for nome in ("transformers.min.js", "ort-wasm-simd-threaded.jsep.mjs", "ort-wasm-simd-threaded.jsep.wasm"):
            f = com_ia / nome
            if not f.is_file():
                raise Falha(f"--ia: falta {f}")
            pacote["assets/ia/" + nome] = f.read_bytes()
        mod = com_ia / "modelos"
        if not mod.is_dir():
            raise Falha(f"--ia: falta a pasta {mod}")
        for f in sorted(mod.rglob("*")):
            if f.is_file():
                pacote["modelos/" + f.relative_to(mod).as_posix()] = f.read_bytes()

    # Verificação de rede: nenhuma chamada para fora em nada que o navegador abra.
    chamadas, mencionadas = [], {}
    for p in sorted(pacote):
        if p.endswith((".html", ".js", ".mjs", ".css", ".json")) and not p.startswith("modelos/"):
            t = pacote[p].decode("utf-8", "replace")
            _, fora = referencias(p, t)
            chamadas += [f"{p} -> {u}" for u in sorted(fora)]
            m = mencoes(t)
            if m:
                mencionadas[p] = m
    if chamadas:
        raise Falha("sobram chamadas para fora do aparelho:\n  " + "\n  ".join(chamadas))

    # Ficheiros da casa, ferramentas e gerados.
    for origem, destino in EXTRA_REPO.items():
        f = repo / origem
        if f.is_file():
            pacote[destino] = f.read_bytes()
    for f in sorted((repo / "ferramentas").glob("*.py")) if (repo / "ferramentas").is_dir() else []:
        pacote["ferramentas/" + f.name] = f.read_bytes()
    web = sorted(p for p in pacote if p.endswith((".html", ".js", ".json", ".css", ".mjs")) and not p.startswith(("modelos/", "assets/ia/", "prova/", "ferramentas/")))
    # Selo de versão e data no rodapé de todas as páginas (ordem do David de 28-11-2026, 04:25): antes da chave
    # do sw.js, para um selo novo chegar a quem tinha a cache antiga; os hashes de PACOTE.json seguem as páginas seladas.
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    import selo_versao  # noqa: E402
    selo = selo_versao.ler(str(repo))
    for p in sorted(pacote):
        if p.endswith(".html"):
            pacote[p] = selo_versao.aplicar(pacote[p].decode("utf-8"), selo).encode("utf-8")
    for o in origens:
        if o.get("ficheiro", "").endswith(".html") and o["ficheiro"] in pacote:
            o["sha256"] = sha256(pacote[o["ficheiro"]])
            o["selo"] = selo_versao.texto(selo)
    registo.append("selo de versão em todas as páginas: " + selo_versao.texto(selo))
    chave = sha256("\n".join(f"{p}:{sha256(pacote[p])}" for p in web).encode())[:16]
    pacote["sw.js"] = gerar_sw(web, chave)
    pacote["servidor_local.py"] = SERVIDOR.encode("utf-8")
    pacote["ABRIR_KONFIRMU_OFFLINE.command"] = COMMAND.encode("utf-8")
    pacote["abrir_konfirmu_offline.sh"] = SH.encode("utf-8")
    pacote["ABRIR_KONFIRMU_OFFLINE.bat"] = BAT.encode("utf-8")
    paginas = sorted(p for p in pacote if p.endswith(".html"))
    extra = ", os ficheiros de prova da casa (pasta prova) e as ferramentas (pasta ferramentas)" if any(p.startswith("ferramentas/") for p in pacote) else ", e os ficheiros de prova da casa (pasta prova)"
    pacote["LEIA-ME.txt"] = LEIA_ME.format(topo=PASTA_TOPO, n=len(paginas), extra=extra).encode("utf-8")

    commit, ts, sujo = commit_info(repo)
    script_sha = sha256(Path(__file__).read_bytes())
    meta = {"nome": PASTA_TOPO, "zip": NOME_ZIP, "empacotador": f"scripts/build_pacote_offline.py v{VERSAO}", "empacotador_sha256": script_sha,
            "repositorio": "silvadvp-del/konfirmu-claim-protocol", "commit": commit, "commit_com_alteracoes_por_gravar": sujo,
            "data_do_commit_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(ts)),
            "base": str(base.name) if base else None, "base_sha256": base_sha, "pagina_inicial": PAGINA_INICIAL,
            "paginas": paginas, "chamadas_para_fora": 0, "paginas_rtl": paginas_rtl, "ia_local": bool(com_ia),
            "regra_de_rede": CSP, "transformacoes": registo, "mencoes_de_urls_em_texto": mencionadas, "origens": sorted(origens, key=lambda o: o["ficheiro"])}
    pacote["PACOTE.json"] = (json.dumps(meta, ensure_ascii=False, indent=1) + "\n").encode("utf-8")
    somas = "".join(f"{sha256(pacote[p])}  {p}\n" for p in sorted(pacote))
    pacote["SHA256SUMS.txt"] = somas.encode("utf-8")
    return pacote, meta, ts


def escrever_zip(pacote: dict, ts: int) -> bytes:
    data = time.gmtime(max(ts, 315532800))[:6]
    mem = io.BytesIO()
    with zipfile.ZipFile(mem, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as z:
        pastas = sorted({str(PurePosixPath(PASTA_TOPO, p).parent) for p in pacote} | {PASTA_TOPO})
        for d in pastas:
            zi = zipfile.ZipInfo(d.rstrip("/") + "/", data)
            zi.create_system, zi.external_attr = 3, (0o40755 << 16) | 0x10
            z.writestr(zi, b"")
        for p in sorted(pacote):
            zi = zipfile.ZipInfo(f"{PASTA_TOPO}/{p}", data)
            zi.create_system = 3
            zi.external_attr = ((0o100755 if PurePosixPath(p).name in EXECUTAVEIS else 0o100644) << 16)
            zi.compress_type = zipfile.ZIP_DEFLATED
            z.writestr(zi, pacote[p], compresslevel=9)
    return mem.getvalue()


def verificar_zip(dados: bytes) -> list:
    erros = []
    with zipfile.ZipFile(io.BytesIO(dados)) as z:
        nomes = {i.filename: i for i in z.infolist() if not i.is_dir()}
        somas = z.read(f"{PASTA_TOPO}/SHA256SUMS.txt").decode()
        vistos = set()
        for linha in somas.splitlines():
            h, p = linha.split("  ", 1)
            vistos.add(p)
            n = f"{PASTA_TOPO}/{p}"
            if n not in nomes:
                erros.append(f"falta no ZIP: {p}")
            elif sha256(z.read(n)) != h:
                erros.append(f"hash não confere: {p}")
        for n, i in nomes.items():
            p = n[len(PASTA_TOPO) + 1:]
            if p != "SHA256SUMS.txt" and p not in vistos:
                erros.append(f"ficheiro fora da lista: {p}")
            if PurePosixPath(p).name in EXECUTAVEIS and not (i.external_attr >> 16) & 0o111:
                erros.append(f"sem permissão de execução: {p}")
            if p.endswith((".html", ".js", ".css")) and not p.startswith("modelos/"):
                _, fora = referencias(p, z.read(n).decode("utf-8", "replace"))
                erros += [f"chamada para fora: {p} -> {u}" for u in fora]
            if p.endswith(".html") and b"Content-Security-Policy" not in z.read(n):
                erros.append(f"página sem regra de rede: {p}")
    return erros


def main(argv=None):
    ap = argparse.ArgumentParser(description="Empacotador offline da Konfirmu (duplo clique, modo avião).")
    ap.add_argument("--base", type=Path, help="edição integrada (ZIP com site/ ou pasta), ex.: App-Unica-21.zip")
    ap.add_argument("--saida", type=Path, default=None, help="pasta de saída (por omissão: dist/ no repositório)")
    ap.add_argument("--ia", type=Path, default=None, help="pasta com o runtime e o modelo da IA local (experimental, por ensaiar)")
    ap.add_argument("--verificar", type=Path, help="só conferir um ZIP já feito")
    ap.add_argument("--edicao-21", action="store_true", help="exige as 21 atividades no menu")
    a = ap.parse_args(argv)
    repo = Path(__file__).resolve().parent.parent
    if a.verificar:
        erros = verificar_zip(a.verificar.read_bytes())
        print("\n".join(erros) if erros else f"CONFERE: {a.verificar.name} · sha256 {sha256(a.verificar.read_bytes())}")
        return 1 if erros else 0
    try:
        pacote, meta, ts = construir(repo, a.base, a.ia, a.edicao_21)
        dados = escrever_zip(pacote, ts)
        erros = verificar_zip(dados)
        if erros:
            raise Falha("o ZIP escrito não confere:\n  " + "\n  ".join(erros))
    except Falha as e:
        print("PACOTE NÃO FEITO — " + str(e), file=sys.stderr)
        return 2
    saida = a.saida or (repo / "dist")
    saida.mkdir(parents=True, exist_ok=True)
    (saida / NOME_ZIP).write_bytes(dados)
    h = sha256(dados)
    (saida / (NOME_ZIP + ".sha256")).write_text(f"{h}  {NOME_ZIP}\n", encoding="utf-8")
    (saida / "SHA256SUMS.txt").write_bytes(pacote["SHA256SUMS.txt"])
    (saida / "PACOTE.json").write_bytes(pacote["PACOTE.json"])
    print(f"FEITO: {saida / NOME_ZIP}\n  {len(dados)} bytes · {len(pacote)} ficheiros · {len(meta['paginas'])} páginas · "
          f"chamadas para fora: 0 · páginas RTL: {meta['paginas_rtl']} · IA local: {'sim' if meta['ia_local'] else 'não'}\n  sha256 {h}")
    for r in meta["transformacoes"]:
        print("  ·", r)
    return 0


if __name__ == "__main__":
    sys.exit(main())
