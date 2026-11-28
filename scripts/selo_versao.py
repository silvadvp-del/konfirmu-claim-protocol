#!/usr/bin/env python3
"""Selo de versão e data no rodapé de todas as páginas (ordem do David de 28-11-2026, 04:25, ponto 3).

Cada página do pacote mostra, fixo no fundo do ecrã, um selo pequeno:

    Konfirmu r10 · 1a2b3c4 · 28-11-2026

  r10         a versão da casa (VERSAO, abaixo; muda à mão a cada entrega nova)
  1a2b3c4     o commit curto de onde o pacote foi construído; com um «+» se havia alterações por gravar
  28-11-2026  a data desse commit, na hora de Amesterdão

Serve para conferir no telemóvel, logo ao abrir, que versão se está a testar. Não apanha toques
(pointer-events:none), não sai para a rede, Branco Titânio sobre Azul Abissal (contraste AAA), sem emojis.
A página guarda a sua política de segurança: se a CSP só aceita estilos por hash, o hash do estilo do selo
entra na diretiva style-src. Duas construções do mesmo commit dão os mesmos bytes.

Uso como biblioteca:  selo = selo_versao.ler(repo); html = selo_versao.aplicar(html, selo)
Uso na linha de comandos:  python3 -I scripts/selo_versao.py [REPO]   (mostra o selo deste repositório)
"""
import base64
import hashlib
import os
import re
import subprocess
import sys

VERSAO = "r10"
CLASSE = "k-selo-versao"
CSS = (".%s{position:fixed;inset-inline-start:8px;bottom:calc(6px + env(safe-area-inset-bottom, 0px));"
       "z-index:2147483000;pointer-events:none;margin:0;padding:2px 8px;border:1px solid rgba(255,158,125,.35);"
       "border-radius:8px;background:rgba(11,25,44,.9);color:#F4F7FA;"
       "font:500 11px/1.4 system-ui,-apple-system,\"Segoe UI\",Roboto,sans-serif;letter-spacing:.02em;"
       "white-space:nowrap;max-width:calc(100vw - 16px);overflow:hidden;text-overflow:ellipsis}"
       "@media print{.%s{position:static;display:inline-block}}") % (CLASSE, CLASSE)
MARCA_INICIO, MARCA_FIM = "<!-- selo-versao:inicio -->", "<!-- selo-versao:fim -->"


def _git(repo, *args):
    env = dict(os.environ, TZ="Europe/Amsterdam", LC_ALL="C")
    return subprocess.run(["git", "-C", repo] + list(args), capture_output=True, text=True, env=env, check=True).stdout.strip()


def ler(repo):
    """Lê do git o commit curto e a data do commit. Sem git, usa KONFIRMU_COMMIT e KONFIRMU_DATA (ou para)."""
    try:
        commit = _git(repo, "rev-parse", "--short=7", "HEAD")
        data = _git(repo, "log", "-1", "--format=%cd", "--date=format-local:%d-%m-%Y")
        iso = _git(repo, "log", "-1", "--format=%cd", "--date=format-local:%Y-%m-%d")
        sujo = bool(_git(repo, "status", "--porcelain", "--untracked-files=no"))
    except (OSError, subprocess.CalledProcessError):
        commit, data = os.environ.get("KONFIRMU_COMMIT", ""), os.environ.get("KONFIRMU_DATA", "")
        if not re.fullmatch(r"[0-9a-f]{7}", commit) or not re.fullmatch(r"\d{2}-\d{2}-\d{4}", data):
            raise SystemExit("selo_versao: sem git e sem KONFIRMU_COMMIT/KONFIRMU_DATA válidos — não há selo honesto")
        iso, sujo = "%s-%s-%s" % (data[6:], data[3:5], data[:2]), False
    return {"versao": VERSAO, "commit": commit + ("+" if sujo else ""), "data": data, "iso": iso}


def texto(selo):
    return "Konfirmu %s · %s · %s" % (selo["versao"], selo["commit"], selo["data"])


def _hash_css():
    return "'sha256-%s'" % base64.b64encode(hashlib.sha256(CSS.encode("utf-8")).digest()).decode("ascii")


def _csp_com_selo(conteudo):
    """Acrescenta o hash do estilo do selo à CSP, só quando ela não deixa estilos em linha."""
    dirs = [d.strip() for d in conteudo.split(";") if d.strip()]
    nomes = [d.split()[0].lower() for d in dirs]
    if "style-src" in nomes:
        i = nomes.index("style-src")
        fontes = dirs[i].split()[1:]
        if "'unsafe-inline'" in fontes and not any(f.startswith(("'sha256-", "'nonce-")) for f in fontes):
            return conteudo
        if _hash_css() not in fontes:
            dirs[i] = dirs[i] + " " + _hash_css()
    elif "default-src" in nomes:
        fontes = dirs[nomes.index("default-src")].split()[1:]
        if "'unsafe-inline'" in fontes:
            return conteudo
        dirs.append("style-src " + " ".join([f for f in fontes if f != "'none'"] + [_hash_css()]))
    else:
        return conteudo
    return "; ".join(dirs)


def aplicar(html, selo):
    """Põe o selo antes do último </body> (ou no fim) e acerta a CSP. Idempotente: troca um selo anterior."""
    html = re.sub(re.escape(MARCA_INICIO) + r".*?" + re.escape(MARCA_FIM), "", html, flags=re.S)
    bloco = ('%s<style>%s</style><p class="%s" dir="ltr" translate="no" data-versao="%s" data-commit="%s" '
             'data-data="%s">Konfirmu %s · <bdi>%s</bdi> · <time datetime="%s">%s</time></p>%s'
             % (MARCA_INICIO, CSS, CLASSE, selo["versao"], selo["commit"], selo["iso"], selo["versao"],
                selo["commit"], selo["iso"], selo["data"], MARCA_FIM))
    fim = [m.start() for m in re.finditer(r"</body\s*>", html, re.I)]
    html = html[:fim[-1]] + bloco + html[fim[-1]:] if fim else html + bloco
    return re.sub(r'(<meta\s+http-equiv=["\']Content-Security-Policy["\']\s+content=")([^"]*)(")',
                  lambda m: m.group(1) + _csp_com_selo(m.group(2)) + m.group(3), html, flags=re.I)


if __name__ == "__main__":
    s = ler(sys.argv[1] if len(sys.argv) > 1 else os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    print(texto(s))
