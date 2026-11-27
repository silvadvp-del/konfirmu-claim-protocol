"""Reproduz os 4 defeitos da auditoria no motor publico. Uso: provar_defeitos.py <konfirmu_calc.py> <rascunho>"""
import ast
import copy
import errno
import hashlib
import importlib.util
import json
import os
import re
import sys
import tempfile

MOTOR, SCR = sys.argv[1], sys.argv[2]
assert hashlib.sha256(open(MOTOR, "rb").read()).hexdigest() == "529098c652ee8234960d69383e308f60db6a5df8ea6bdae578b538eb806e80cf"
espec = importlib.util.spec_from_file_location("kc", MOTOR)
kc = importlib.util.module_from_spec(espec)
sys.modules["kc"] = kc
espec.loader.exec_module(kc)
OK = TOTAL = 0


def v(cond, nome):
    global OK, TOTAL
    OK += bool(cond)
    TOTAL += 1
    print(("[REPRODUZ] " if cond else "[NAO REPRODUZ] ") + nome, flush=True)


print("B. OS 4 DEFEITOS NO MOTOR PUBLICO v3.0.0")
sk = kc.chave_demo("u51-notario")
obj = {"facto": "exemplo", "valor": 7}
selo = kc.selar(obj, sk)
v(kc.selo_ok(obj, selo), "B0 selo intacto e aceite (controlo)")
x = copy.deepcopy(selo)
x["alg"] = "NENHUM"
v(kc.selo_ok(obj, x), "B1 muda-se o campo «alg» para «NENHUM»: o selo continua aceite")
for campo, mau in (("hash", "0" * 64), ("pub", "00" * 32), ("sig", "0" * 128)):
    x = copy.deepcopy(selo)
    x[campo] = mau
    v(not kc.selo_ok(obj, x), "B1b muda-se «%s»: o selo e recusado (e so o «alg» que fica de fora)" % campo)

texto = json.dumps(selo).encode("utf-8")
CAMPOS = {}
for campo in ("alg", "hash", "pub", "sig"):
    chave = ('"%s": "' % campo).encode()
    a = texto.index(chave)
    fim_valor = texto.index(b'"', a + len(chave))
    # a entrada «alg» conta com o nome da chave e com o valor; as outras so com o valor
    CAMPOS[campo] = (a if campo == "alg" else a + len(chave), fim_valor)
aceites = {c: [] for c in CAMPOS}
aceites["fora dos valores"] = []
ilegiveis = 0
for i in range(len(texto)):
    for b in range(8):
        y = texto[:i] + bytes([texto[i] ^ (1 << b)]) + texto[i + 1:]
        try:
            d = json.loads(y.decode("utf-8"))
        except (ValueError, UnicodeDecodeError):
            ilegiveis += 1
            continue
        if isinstance(d, dict) and kc.selo_ok(obj, d):
            sitio = next((c for c, (a, z) in CAMPOS.items() if a <= i < z), "fora dos valores")
            aceites[site if False else sitio].append((i, b, texto[i]))
total = sum(len(v) for v in aceites.values())
print("      bits trocados no texto do selo (%d bytes = %d flips): %d aceites | por entrada: %s | ilegiveis: %d" % (len(texto), len(texto) * 8, total, {c: len(v) for c, v in aceites.items()}, ilegiveis))
v(aceites["alg"] and not aceites["fora dos valores"] and not aceites["hash"], "B2' somando o nome e o valor de «alg»: %d aceites; «hash»: 0; fora das entradas: 0" % len(aceites["alg"]))
so_caixa = all(b == 5 and chr(x) in "abcdef" for c in ("pub", "sig") for (_, b, x) in aceites[c])
v(so_caixa and (aceites["pub"] or aceites["sig"]), "B2'' os aceites fora de «alg» sao so maiusculas/minusculas (bit 5) de a-f em «pub» (%d) e «sig» (%d): %s" % (len(aceites["pub"]), len(aceites["sig"]), so_caixa))
v(total != 550, "B2x a conta desta janela (%d) nao e a da auditoria (550): methods diferentes; diz-se" % total)

d = tempfile.mkdtemp(prefix="u51_", dir=SCR)
_real_write = os.write


def reler(caminho):
    try:
        kc.LedgerPersistente(sk, caminho)
        return "abriu"
    except RuntimeError as e:
        return str(e).split(":")[0]


caminho = os.path.join(d, "cheio.jsonl")
lp = kc.LedgerPersistente(sk, caminho)
lp.registar(1, "A", {"n": 0})


def write_cheio(fd, dados):
    raise OSError(errno.ENOSPC, "No space left on device")


os.write = write_cheio
excecao = None
try:
    lp.registar(1, "B", {"n": 1})
except OSError as e:
    excecao = e
finally:
    os.write = _real_write
v(excecao is not None and excecao.errno == errno.ENOSPC, "B3a com o disco cheio, «registar» levanta erro (nao e silencioso neste passo)")
v(len(lp.blocos) == 2 and open(caminho, "rb").read().count(b"\n") == 1, "B3b … mas o bloco que nao coube no disco FICA em memoria (%d blocos em memoria, 1 no ficheiro)" % len(lp.blocos))
lp.registar(1, "C", {"n": 2})
v(open(caminho, "rb").read().count(b"\n") == 2 and len(lp.blocos) == 3, "B3c a escrita seguinte corre e o ficheiro fica com um buraco (2 linhas no ficheiro, 3 blocos em memoria)")
v(reler(caminho) == "LEDGER_CORROMPIDA", "B3d ao reler: %s. Um disco cheio um instante deixa o livro encravado para sempre" % reler(caminho))

caminho2 = os.path.join(d, "curto.jsonl")
lp2 = kc.LedgerPersistente(sk, caminho2)
lp2.registar(1, "A", {"n": 0})


def write_curto(fd, dados):
    return _real_write(fd, dados[:len(dados) // 2])


os.write = write_curto
try:
    devolveu = lp2.registar(1, "B", {"n": 1})
finally:
    os.write = _real_write
v(isinstance(devolveu, str) and len(devolveu) == 64 and len(lp2.blocos) == 2, "B4a escrita curta: «registar» DEVOLVE o hash como se tivesse gravado")
linhas = open(caminho2, "rb").read().split(b"\n")
v(linhas[-1] != b"" and len(linhas) == 2, "B4b … e o ficheiro fica com a ultima linha rasgada (%d linhas inteiras e um pedaço)" % (len(linhas) - 1))
v(reler(caminho2) == "LEDGER_ILEGIVEL", "B4c ao reler: %s" % reler(caminho2))

arv = ast.parse(open(MOTOR, encoding="utf-8").read())
relogio = sorted({(n.module or "").split(".")[0] for n in ast.walk(arv) if isinstance(n, ast.ImportFrom) and (n.module or "").split(".")[0] in ("datetime", "time")}
                 | {a.name.split(".")[0] for n in ast.walk(arv) if isinstance(n, ast.Import) for a in n.names if a.name.split(".")[0] in ("datetime", "time")})
v(relogio == [], "B5 o motor publico nao importa relogio nenhum: %s. O defeito do recuo do relogio esta noutro codigo" % (relogio or "nenhum"))
print("")
print(("TUDO COMFORME O ESPERADO" if OK == TOTAL else "HÁ DIFERENCAS") + ": %d/%d" % (OK, TOTAL))
sys.exit(0 if OK == TOTAL else 1)
