"""Copia para enxame_naves.html, byte a byte, o motor KSHA (de ksha_fluxo.js) e os portoes 112/criancas (do chat).
Uso: python3 injetar.py <raiz do repositorio>"""
import sys, hashlib, pathlib
raiz = pathlib.Path(sys.argv[1])
def entre(t, ini, fim_marca, incluir=True):
    a = t.index(ini); b = t.index(fim_marca, a) + len(fim_marca)
    return t[a:b]
fonte = (raiz / "ksha_fluxo.js").read_text(encoding="utf-8")
ksha = entre(fonte, "/* >>> KSHA: inicio", "/* <<< KSHA: fim */")
chat = (raiz / "konfirmu_chat_offline_v0.1.html").read_text(encoding="utf-8")
a = chat.index("/* ---------- portão de emergência")
j = chat.index("function portaoCrianca", a)
b = chat.index("return null}", j) + len("return null}")
portoes = "/* >>> PORTOES: copia exata de konfirmu_chat_offline_v0.1.html (nao editar aqui) */\n" + chat[a:b] + "\n/* <<< PORTOES: fim */"
pag = raiz / "enxame_naves.html"
t = pag.read_text(encoding="utf-8")
if "/*KSHA*/" in t: t = t.replace("/*KSHA*/", ksha, 1)
else:
    x = entre(t, "/* >>> KSHA: inicio", "/* <<< KSHA: fim */"); t = t.replace(x, ksha, 1)
if "/*PORTOES*/" in t: t = t.replace("/*PORTOES*/", portoes, 1)
else:
    x = entre(t, "/* >>> PORTOES:", "/* <<< PORTOES: fim */"); t = t.replace(x, portoes, 1)
pag.write_text(t, encoding="utf-8")
h = lambda s: hashlib.sha256(s.encode("utf-8")).hexdigest()
print("ksha", h(ksha)); print("portoes", h(portoes), len(portoes)); print("pagina", hashlib.sha256(t.encode("utf-8")).hexdigest(), len(t.encode("utf-8")))
