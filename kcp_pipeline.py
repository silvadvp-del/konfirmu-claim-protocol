#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# kcp_pipeline.py — PROVA/1: cartucho + medicoes -> veredicto + recibo encadeado (stdlib-only)
# Reutiliza o kcp_lint (whitelist AST, sem eval). Incerteza propagada por derivada numerica central.
import hashlib, json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from kcp_lint import calcular_formula, veredicto, canon_tipado

KCP_VERSION = "3.0.0"
GENESIS = "0" * 64

def executar(cartridge, medicoes, prev_hash=None):
    """medicoes: {input: [valor, incerteza]} -> {'receipt': {...}, 'digest': sha256}"""
    for i in cartridge["inputs"]:
        if i not in medicoes:
            raise ValueError("medicao em falta: " + i)
    v, _nom, nota = veredicto(cartridge["formula"], medicoes, cartridge["limits"])
    def f(xs):
        return calcular_formula(cartridge["formula"], xs)
    nom = f({k: m[0] for k, m in medicoes.items()})
    unc = 0.0
    h = 1e-9
    for k, m in medicoes.items():
        if m[1] == 0:
            continue
        plus = {kk: [vv[0] + (h if kk == k else 0), 0] for kk, vv in medicoes.items()}
        minus = {kk: [vv[0] - (h if kk == k else 0), 0] for kk, vv in medicoes.items()}
        der = (f({kk: vv[0] for kk, vv in plus.items()}) - f({kk: vv[0] for kk, vv in minus.items()})) / (2 * h)
        unc += abs(der) * m[1]
    recibo = {
        "kcp_version": KCP_VERSION,
        "pillar": cartridge.get("cartridge_id"),
        "verdict": v,
        "summary": (cartridge.get("reason_code_veto") if v == "VETO" else "within limits"),
        "data": {"value": round(nom, 8), "unc": round(unc, 8)},
    }
    if prev_hash is not None:
        recibo["prev_hash"] = prev_hash
    digest = hashlib.sha256(canon_tipado(recibo).encode()).hexdigest()
    return {"receipt": recibo, "digest": digest}

def selftest():
    cart = json.loads(Path("cartridges/who_pediatric_paracetamol_v1.json").read_text(encoding="utf-8"))
    r1 = executar(cart, {"dose_mg": [180.0, 0.5], "peso_kg": [12.4, 0.1]}, prev_hash=GENESIS)
    assert r1["receipt"]["verdict"] == "OK", r1
    assert r1["receipt"]["prev_hash"] == GENESIS
    r2 = executar(cart, {"dose_mg": [350.0, 0.5], "peso_kg": [12.4, 0.1]}, prev_hash=r1["digest"])
    assert r2["receipt"]["verdict"] == "VETO", r2
    assert r2["receipt"]["prev_hash"] == r1["digest"]
    # adulteracao: muda um byte do recibo -> digest muda
    rec2 = json.loads(json.dumps(r2["receipt"]))
    rec2["data"]["value"] = rec2["data"]["value"] + 0.1
    d3 = hashlib.sha256(canon_tipado(rec2).encode()).hexdigest()
    assert d3 != r2["digest"]
    print("kcp_pipeline SELFTEST VERDE")
    print("  dig1:", r1["digest"][:16] + "...", "| dig2:", r2["digest"][:16] + "...", "| tamper muda:", d3[:16] + "...")

if __name__ == "__main__":
    selftest()
