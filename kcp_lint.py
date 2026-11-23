#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# kcp_lint.py — auditor determinístico de cartuchos (stdlib-only, sem eval)
# Regra de ouro: nada de código arbitrário. A fórmula é avaliada por AST com whitelist
# (números, variáveis, + - * / ** ( ) e unário -). Veto no PIOR CASO direccional:
#   limite máximo -> pior caso alto; limite mínimo -> pior caso baixo.
import ast, hashlib, json, operator, sys
from pathlib import Path

VERSAO = "1.0.0"

CAMPOS = ["cartridge_id", "version", "standard_ref", "reason_code_veto",
          "inputs", "formula", "limits", "test_vectors"]

class FormulaError(ValueError):
    pass

def avaliar(node, env):
    if isinstance(node, ast.Expression):
        return avaliar(node.body, env)
    if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
        return float(node.value)
    if isinstance(node, ast.Name):
        if node.id in env:
            return float(env[node.id])
        raise FormulaError("variavel desconhecida: " + node.id)
    if isinstance(node, ast.BinOp):
        a = avaliar(node.left, env); b = avaliar(node.right, env)
        op = {ast.Add: operator.add, ast.Sub: operator.sub,
              ast.Mult: operator.mul, ast.Div: operator.truediv,
              ast.Pow: operator.pow}.get(type(node.op))
        if op is None:
            raise FormulaError("operador nao permitido")
        return op(a, b)
    if isinstance(node, ast.UnaryOp) and isinstance(node.op, ast.USub):
        return -avaliar(node.operand, env)
    raise FormulaError("construcao nao permitida na formula")

def calcular_formula(formula, env):
    try:
        return avaliar(ast.parse(formula, mode="eval"), env)
    except (ZeroDivisionError, FormulaError, SyntaxError) as e:
        raise FormulaError(str(e))

def veredicto(formula, env, limits):
    # env = {variavel: [valor, incerteza]}; pior caso direccional: alto = v0+u, baixo = v0-u
    nom = calcular_formula(formula, {k: v[0] for k, v in env.items()})
    alto = calcular_formula(formula, {k: v[0] + v[1] for k, v in env.items()})
    baixo = calcular_formula(formula, {k: v[0] - v[1] for k, v in env.items()})
    maxi = limits.get("max_allowed"); mini = limits.get("min_allowed")
    if maxi is not None and alto > maxi:
        return ("VETO", nom, "alto " + repr(round(alto, 6)) + " > max " + repr(maxi))
    if mini is not None and baixo < mini:
        return ("VETO", nom, "baixo " + repr(round(baixo, 6)) + " < min " + repr(mini))
    return ("OK", nom, "dentro dos limites")

def canon_tipado(d):
    def tag(v):
        if isinstance(v, bool): return "b:" + str(v)
        if isinstance(v, (int, float)): return "n:" + repr(v)
        if isinstance(v, str): return "s:" + v
        if isinstance(v, (list, tuple)): return "a:[" + ",".join(tag(x) for x in v) + "]"
        if isinstance(v, dict): return "o:{" + ",".join(k + "=" + tag(v[k]) for k in sorted(v)) + "}"
        raise TypeError(str(type(v)))
    return tag(d)

def lint_cartridge(spec):
    class R:
        def __init__(self):
            self.valid = False; self.errors = []; self.cartridge_id = spec.get("cartridge_id", "?")
            self.canonical_hash = ""
    r = R()
    for c in CAMPOS:
        if c not in spec:
            r.errors.append("campo em falta: " + c)
    if not isinstance(spec.get("inputs"), list) or not spec["inputs"]:
        r.errors.append("inputs vazio")
    if not isinstance(spec.get("test_vectors"), list) or not spec["test_vectors"]:
        r.errors.append("sem test_vectors")
    if r.errors:
        return r
    r.canonical_hash = hashlib.sha256(canon_tipado(spec).encode()).hexdigest()
    for tv in spec["test_vectors"]:
        env = tv.get("env", {})
        for i in spec["inputs"]:
            if i not in env or not isinstance(env[i], list) or len(env[i]) != 2:
                r.errors.append("vetor malformado para " + i + " em " + str(tv))
                continue
        try:
            v, nom, nota = veredicto(spec["formula"], env, spec["limits"])
        except FormulaError as e:
            v, nota = "ERRO", str(e)
        if v != tv.get("expected_verdict"):
            r.errors.append("vetor " + str(tv.get("env")) + ": esperado " +
                            str(tv.get("expected_verdict")) + ", obtido " + v + " (" + nota + ")")
    r.valid = not r.errors
    return r

def selftest():
    spec = {
        "cartridge_id": "TESTE_DUPLO", "version": "1.0.0", "standard_ref": "selftest",
        "reason_code_veto": "X", "inputs": ["a", "b"],
        "formula": "a / b",
        "limits": {"min_allowed": 0.0, "max_allowed": 10.0},
        "test_vectors": [
            {"env": {"a": [10.0, 0.0], "b": [2.0, 0.0]}, "expected_verdict": "OK"},
            {"env": {"a": [25.0, 0.0], "b": [2.0, 0.0]}, "expected_verdict": "VETO"},
        ],
    }
    r = lint_cartridge(spec)
    assert r.valid, r.errors
    assert r.canonical_hash == hashlib.sha256(canon_tipado(spec).encode()).hexdigest()
    # formula maliciosa recusada
    for f in ["__import__('os').system('id')", "open('/etc/passwd')", "a if b else c",
              "lambda: 1", "[x for x in range(1)]"]:
        try:
            calcular_formula(f, {"a": 1.0, "b": 2.0})
            assert False, "devia ter recusado: " + f
        except FormulaError:
            pass
    print("kcp_lint SELFTEST VERDE")

if __name__ == "__main__":
    if "--selftest" in sys.argv:
        selftest(); sys.exit(0)
    files = sorted(Path("cartridges").glob("*.json")) if Path("cartridges").is_dir() else []
    if not files:
        print("No cartridges found"); sys.exit(1)
    falhou = False
    for p in files:
        spec = json.loads(p.read_text(encoding="utf-8"))
        rep = lint_cartridge(spec)
        print(("[PASS]" if rep.valid else "[FAIL]"), p, "->", rep.cartridge_id, rep.canonical_hash[:16] + "...")
        for e in rep.errors:
            print("   ERROR:", e)
        falhou = falhou or not rep.valid
    print("ALL PASS" if not falhou else "FAILURES")
    sys.exit(1 if falhou else 0)
