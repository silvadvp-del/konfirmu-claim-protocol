"""Bateria das correcções de referência. O esperado (secção D de ESPERADO.txt) foi escrito antes.
Uso: provar_correcoes.py <konfirmu_calc.py> <pasta onde esta correcoes_ledger.py> <rascunho>"""
import copy
import errno
import hashlib
import importlib.util
import json
import os
import sys
import tempfile

MOTOR, PASTA, SCR = sys.argv[1], sys.argv[2], sys.argv[3]
espec = importlib.util.spec_from_file_location("corr", os.path.join(PASTA, "correcoes_ledger.py"))
C = importlib.util.module_from_spec(espec)
sys.modules["corr"] = C
espec.loader.exec_module(C)
motor = C.carregar_motor(MOTOR)
LedgerSegura = C.classe_ledger_segura(motor)
LINHAS, OK, TOTAL = [], 0, 0


def p(t):
    LINHAS.append(t)
    print(t, flush=True)


def v(cond, nome):
    global OK, TOTAL
    OK += bool(cond)
    TOTAL += 1
    p(("[OK] " if cond else "[FALHOU] ") + nome)


sk = motor.chave_demo("u51-notario")
obj = {"facto": "exemplo", "valor": 7}
p("D. CORRECCOES DE REFERENCIA (correcoes_ledger.py) sobre o motor " + C.ALVO_MOTOR[:16] + "…")
p("D1. O SELO ESTRIITO")
selo = motor.selar(obj, sk)
v(C.selo_estrito(obj, selo, motor), "D1a selo bom -> aceite")
for nome, troco in (("o valor de «alg»", lambda s: s.__setitem__("alg", "NENHUM")), ("o nome da chave «alg»", lambda s: s.__setitem__("clg", s.pop("alg"))),
                    ("maiúsculas em «pub»", lambda s: s.__setitem__("pub", s["pub"].upper())), ("maiúsculas em «sig»", lambda s: s.__setitem__("sig", s["sig"].upper())),
                    ("um campo a mais", lambda s: s.__setitem__("extra", 1)), ("um campo a menos", lambda s: s.pop("alg"))):
    x = copy.deepcopy(selo)
    troco(x)
    v(not C.selo_estrito(obj, x, motor), "D1b recusado: " + nome)
x = copy.deepcopy(selo)
v(not C.selo_estrito({"facto": "outro", "valor": 7}, x, motor), "D1c recusado: o objecto não é o selado")
texto = json.dumps(selo).encode("utf-8")
aceites = 0
for i in range(len(texto)):
    for b in range(8):
        try:
            d = json.loads((texto[:i] + bytes([texto[i] ^ (1 << b)]) + texto[i + 1:]).decode("utf-8"))
        except (ValueError, UnicodeDecodeError):
            continue
        aceites += bool(isinstance(d, dict) and C.selo_estrito(obj, d, motor))
v(aceites == 0, "D1d os %d bits trocados do texto do selo: %d aceites (o motor aceita 183)" % (len(texto) * 8, aceites))
x = copy.deepcopy(selo)
v(motor.selo_ok(obj, x, {x["pub"]}) and C.selo_estrito(obj, x, motor, {x["pub"]}) and not C.selo_estrito(obj, x, motor, {"00" * 32}),
  "D1e a lista de chaves aceites continua a contar: com a chave certa aceite; sem ela recusado")

p("D2. ENCAIXA NO LUGAR DO MOTOR")
d = tempfile.mkdtemp(prefix="u51c_", dir=SCR)
cam_a, cam_b = os.path.join(d, "motor.jsonl"), os.path.join(d, "segura.jsonl")
ref, nova = motor.LedgerPersistente(sk, cam_a), LedgerSegura(sk, cam_b)
for i in range(5):
    a, b = ref.registar(1, "EVENTO", {"i": i}), nova.registar(1, "EVENTO", {"i": i})
    assert a == b
v(ref.blocos == nova.blocos and open(cam_a, "rb").read() == open(cam_b, "rb").read() and nova.verificar_integridade_cadeia(),
  "D2 cinco registos: blocos, hashes e bytes do ficheiro iguais aos do motor")


def linhas(caminho):
    return open(caminho, "rb").read().split(b"\n")[:-1]


def tenta(f, *a, **k):
    """Corre e apanha o que rebentar: um teste nunca deve morrer por excecao."""
    try:
        return f(*a, **k)
    except Exception as e:
        return e


def ler_ficheiro(caminho):
    return open(caminho, "rb").read() if os.path.exists(caminho) else b""


def reler(caminho):
    try:
        return LedgerSegura(sk, caminho)
    except Exception as e:
        return str(e).split(":")[0] if isinstance(e, RuntimeError) else "EXCECAO:" + type(e).__name__


p("D3/D4/D10. A CAUDA RASGADA AO ARRANCAR")
c = os.path.join(d, "rasgada.jsonl")
l = LedgerSegura(sk, c)
for i in range(3):
    l.registar(1, "E", {"i": i})
completo = open(c, "rb").read()
irma = LedgerSegura(sk, os.path.join(d, "irma.jsonl"))
for i in range(4):
    irma.registar(1, "E", {"i": i})
quarto = motor.canon(irma.blocos[3])
meia = quarto[:len(quarto) // 2]
with open(c, "ab") as fh:
    fh.write(meia)
r = reler(c)
v(isinstance(r, LedgerSegura) and len(r.blocos) == 3 and r.recuperados == [{"isolado": True, "bytes": len(meia), "sha256": motor.h256(meia)}],
  "D3 cauda rasgada (%d bytes) -> arranca com os 3 registos completos; a cauda é isolada com o hash" % len(meia))
guardado = ler_ficheiro(c + ".rasgados")
v(open(c, "rb").read() == completo and guardado.endswith(meia + b"\n") and motor.h256(meia).encode() in guardado,
  "D3b o ficheiro volta a acabar em mudança de linha; os bytes rasgados estão inteiros no ficheiro ao lado, com o hash")
seguinte = tenta(r.registar, 1, "E", {"i": 3})
v(not isinstance(seguinte, Exception) and r.blocos[-1]["n"] == 3 and r.verificar_integridade_cadeia() and isinstance(reler(c), LedgerSegura), "D10 depois de recuperar, a cadeia segue com o número certo e o disco confere")
for nome, cauda, esperado in (("D4 registo completo a que só falta a mudança de linha", quarto, 4), ("D4b cauda que é JSON válido mas não segue a cadeia", motor.canon(irma.blocos[1]), 3)):
    c2 = os.path.join(d, "caixa%d.jsonl" % esperado)
    with open(c2, "wb") as fh:
        fh.write(completo + cauda)
    r2 = reler(c2)
    v(isinstance(r2, LedgerSegura) and len(r2.blocos) == esperado and open(c2, "rb").read().endswith(b"\n"),
      nome + " -> %d registos; ficheiro acaba em mudança de linha (%s)" % (len(r2.blocos) if isinstance(r2, LedgerSegura) else r2, r2.recuperados[0] if isinstance(r2, LedgerSegura) else "-"))
for nome, novo_texto, codigo in (("D5 um registo completo estragado (não é JSON)", completo.replace(b'"i":1', b'XX"i":1', 1), "LEDGER_ILEGIVEL"),
                                 ("D6 um registo completo alterado", completo.replace(b'"i":1', b'"i":9', 1), "LEDGER_CORROMPIDA")):
    c3 = os.path.join(d, "ma%d.jsonl" % len(nome))
    with open(c3, "wb") as fh:
        fh.write(novo_texto)
    r3 = reler(c3)
    v(r3 == codigo, nome + " -> %s (falha fechada, como o motor)" % r3)

p("D7/D8/D9. QUANDO O DISCO FALHA")
_escrita, _fsync = os.write, os.fsync


def ensaio(nome, patch, tipo, codigo=None):
    c4 = os.path.join(d, nome + ".jsonl")
    l4 = LedgerSegura(sk, c4)
    l4.registar(1, "E", {"i": 0})
    try:
        patch()
        try:
            l4.registar(1, "E", {"i": 1})
            deu = "devolveu"
        except Exception as e:
            deu = e
    finally:
        os.write, os.fsync = _escrita, _fsync
    certo = isinstance(deu, tipo) and (codigo is None or getattr(deu, "errno", None) == codigo)
    v(certo and len(l4.blocos) == 1 and len(linhas(c4)) == 1 and open(c4, "rb").read().endswith(b"\n"),
      nome + " -> %s; memória e disco ficam iguais (1 registo em cada)" % (type(deu).__name__ if certo else "resposta inesperada: %r" % (deu,)))
    seg = tenta(l4.registar, 1, "E", {"i": 2})
    v(not isinstance(seg, Exception) and len(l4.blocos) == 2 and isinstance(reler(c4), LedgerSegura) and reler(c4).blocos == l4.blocos, nome + " — b) o registo seguinte corre e, ao reler, está tudo certo")


def meia(fd, dados):
    return _escrita(fd, dados[:len(dados) // 2])


def cheio(fd, dados):
    raise OSError(errno.ENOSPC, "No space left on device")


_conta = [0]


def fsync_erro(fd):
    _conta[0] += 1
    if _conta[0] == 1:
        raise OSError(errno.EIO, "Input/output error")
    return _fsync(fd)


ensaio("D7 escrita curta", lambda: setattr(os, "write", meia), RuntimeError)
ensaio("D8 disco cheio", lambda: setattr(os, "write", cheio), OSError, errno.ENOSPC)
ensaio("D9 o fsync dá erro", lambda: setattr(os, "fsync", fsync_erro), OSError, errno.EIO)
p("")
p(("TUDO VERDE" if OK == TOTAL else "VERMELHO") + ": %d/%d verificações" % (OK, TOTAL))
print("sha256 desta saída (todas as linhas acima): " + hashlib.sha256("\n".join(LINHAS).encode("utf-8")).hexdigest())
sys.exit(0 if OK == TOTAL else 1)
