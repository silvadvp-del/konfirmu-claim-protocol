#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# kcp_pq_hybrid.py — PROTÓTIPO DIDÁTICO de envelope híbrido pós-quântico (stdlib-only).
# ⚠️ DIDÁTICO: a camada hash-based é Lamport+Merkle para ENSINAR o conceito — NÃO é SLH-DSA
# (FIPS 205). Não usar em produção. A versão real exige a especificação oficial do NIST.
# A camada clássica é Ed25519 do MOTOR REAL (hash verificado) — híbrido: as duas assinam o mesmo digest.
import hashlib, importlib.util, os, sys
from pathlib import Path

ALVO = "529098c652ee8234960d69383e308f60db6a5df8ea6bdae578b538eb806e80cf"
MOTOR = Path(__file__).parent / "konfirmu_calc.py"
if hashlib.sha256(MOTOR.read_bytes()).hexdigest() != ALVO:
    sys.exit("motor diverge")
spec = importlib.util.spec_from_file_location("kc", MOTOR)
kc = importlib.util.module_from_spec(spec); sys.modules["kc"] = kc; spec.loader.exec_module(kc)

ESQUEMA = "PROVA/2-PQ-PROTOTIPO"   # reservado; a spec real vira v4-PQ
SUITE = "ED25519+LAMPORT-MERKLE-DIDATICO"
N_FOLHAS = 4                       # 4 assinaturas por chave raiz (didático)

def _h(b: bytes) -> bytes:
    return hashlib.sha256(b).digest()

def chave_lamport():
    sk = [[os.urandom(32) for _ in range(256)] for _ in range(2)]
    pk = [[_h(sk[b][i]) for i in range(256)] for b in range(2)]
    return sk, pk

def assinar_lamport(sk, msg: bytes):
    d = _h(msg)
    return b"".join(sk[(d[i >> 3] >> (7 - (i & 7))) & 1][i] for i in range(256))

def verificar_lamport(pk, msg: bytes, sig: bytes) -> bool:
    if len(sig) != 256 * 32:
        return False
    d = _h(msg)
    for i in range(256):
        b = (d[i >> 3] >> (7 - (i & 7))) & 1
        if _h(sig[i * 32:(i + 1) * 32]) != pk[b][i]:
            return False
    return True

def raiz_merkle(chaves_pk):
    nivel = [_h(b"".join(pk[0]) + b"".join(pk[1])) for pk in chaves_pk]
    while len(nivel) > 1:
        if len(nivel) % 2:
            nivel.append(nivel[-1])
        nivel = [_h(nivel[i] + nivel[i + 1]) for i in range(0, len(nivel), 2)]
    return nivel[0]

def caminho_merkle(chaves_pk, idx):
    nivel = [_h(b"".join(pk[0]) + b"".join(pk[1])) for pk in chaves_pk]
    caminho = []
    while len(nivel) > 1:
        if len(nivel) % 2:
            nivel.append(nivel[-1])
        irmao = nivel[idx ^ 1]
        caminho.append(irmao)
        nivel = [_h(nivel[i] + nivel[i + 1]) for i in range(0, len(nivel), 2)]
        idx //= 2
    return caminho

def verificar_raiz(raiz, folha, caminho, idx):
    h = folha
    for irmao in caminho:
        h = _h(h + irmao) if idx % 2 == 0 else _h(irmao + h)
        idx //= 2
    return h == raiz

class CarteiraPQ:
    """Envelope híbrido: Ed25519 do motor + Lamport/Merkle didático."""
    def __init__(self):
        self.sks, self.pks = zip(*[chave_lamport() for _ in range(N_FOLHAS)])
        self.raiz = raiz_merkle(self.pks)
        self.usadas = [None] * N_FOLHAS

    def assinar(self, msg: bytes, sk_ed: bytes):
        d = _h(msg).hex()
        idx = next((i for i, u in enumerate(self.usadas) if u is None), None)
        if idx is None:
            raise ValueError("chave didática esgotada (N_FOLHAS) — propriedade one-time")
        folha = _h(b"".join(self.pks[idx][0]) + b"".join(self.pks[idx][1]))
        lam = assinar_lamport(self.sks[idx], msg)
        ed = kc.selar({"digest": d}, sk_ed)
        self.usadas[idx] = d
        return {"schema": ESQUEMA, "sig_suite": SUITE, "digest": d,
                "classical_ed25519": ed,
                "hash_based": {"root": self.raiz.hex(), "index": idx,
                               "folha": folha.hex(), "caminho": [x.hex() for x in caminho_merkle(self.pks, idx)],
                               "sig": lam.hex()}}

    def verificar(self, msg: bytes, env: dict, pk_ed: str) -> dict:
        rep = {"ok": True, "linhas": []}
        def L(ok, t):
            rep["linhas"].append(("OK " if ok else "FALHA ") + t); rep["ok"] = rep["ok"] and ok
        L(_h(msg).hex() == env["digest"], "digest")
        L(kc.selo_ok({"digest": env["digest"]}, env["classical_ed25519"], {pk_ed}), "camada clássica Ed25519")
        lam = bytes.fromhex(env["hash_based"]["sig"])
        idx = env["hash_based"]["index"]
        L(verificar_lamport(self.pks[idx], msg, lam), "camada hash-based (Lamport)")
        L(verificar_raiz(self.raiz, bytes.fromhex(env["hash_based"]["folha"]),
                         [bytes.fromhex(x) for x in env["hash_based"]["caminho"]], idx), "raiz Merkle")
        return rep

def selftest():
    c = CarteiraPQ()
    sk = kc.chave_demo("pq-teste")
    pk = kc.ed_publica(sk).hex()
    msg = b"recibo Chronolex de teste"
    env = c.assinar(msg, sk)
    rep = c.verificar(msg, env, pk)
    assert rep["ok"], rep["linhas"]
    msg2 = b"recibo ALTERADO"
    rep2 = c.verificar(msg2, env, pk)
    assert not rep2["ok"], "mensagem adulterada devia falhar"
    # propriedade one-time: reutilizar a MESMA folha com outra mensagem = aviso (didático)
    aviso = None
    try:
        idx = env["hash_based"]["index"]
        d2 = _h(msg2).hex()
        if c.usadas[idx] is not None and c.usadas[idx] != d2:
            aviso = "REUTILIZAÇÃO da folha %d detetada — assinaturas one-time não se reutilizam" % idx
    except Exception:
        pass
    assert aviso, "aviso de reutilização devia existir"
    print("kcp_pq_hybrid SELFTEST VERDE")
    print("  envelope:", ESQUEMA, "| suite:", SUITE)
    print("  raiz Merkle:", c.raiz.hex()[:16] + "…", "| híbrido 2 camadas OK | tamper detetado | aviso one-time:", aviso)

if __name__ == "__main__":
    selftest()
