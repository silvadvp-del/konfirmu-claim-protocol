"""Versao de uma so pagina (para o link de ensaio): bibliotecas dentro da pagina, sem a ligacao para outra pagina do repositorio.
Uso: python3 build_artefacto.py <raiz do repositorio> <saida.html>"""
import sys, re, hashlib, pathlib
raiz, saida = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2])
t = (raiz / "enxame_naves.html").read_text(encoding="utf-8")
for nome in ["nacl-fast.min.js", "qrcode.js", "jsQR.js"]:
    tag = '<script src="./assets/%s"></script>' % nome
    assert t.count(tag) == 1, nome
    lib = (raiz / "assets" / nome).read_text(encoding="utf-8")
    assert "</script" not in lib.lower()
    t = t.replace(tag, "<script>/* assets/%s, sha256 %s */\n%s\n</script>" % (nome, hashlib.sha256(lib.encode("utf-8")).hexdigest(), lib), 1)
t, n = re.subn(r'<p id="ligacaoLocal"[^\n]*</p>\n', "", t)
assert n == 1
assert 'src="./' not in t and "href=\"./" not in t
saida.write_text(t, encoding="utf-8")
print(saida, len(t.encode("utf-8")), hashlib.sha256(t.encode("utf-8")).hexdigest())
