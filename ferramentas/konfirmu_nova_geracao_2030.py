#!/usr/bin/env python3
"""Konfirmu Nova Geração 2030 — cofre local de selos, offline (v2.0.0, EUPL-1.2).

Python 3.9 ou mais recente (o python3 que vem no Mac serve), só a biblioteca padrão, sem rede.
Versão 2 do motor que chegou a 27-11-2026 (v1, de outra IA). O que mudou e porquê está no relatório
do pacote offline. Em resumo, a v2 cumpre o que a v1 prometia:
  * procura o ficheiro pelo CONTEÚDO (SHA-256), não pelo nome;
  * cada registo é assinado com Ed25519 (RFC 8032): qualquer pessoa confere um recibo só com a
    chave pública, sem segredo — e a assinatura é a mesma da tweetnacl usada nas páginas da casa;
  * confere a cadeia inteira: um registo mudado, apagado ou assinado por outra chave aparece;
  * prova de equivocação: dois recibos da mesma chave com o mesmo número e conteúdo diferente;
  * relógio: recusa uma hora anterior à última, mas deixa continuar com --aceitar-relogio,
    e esse registo fica marcado como «recuou» (não se esconde, não bloqueia para sempre);
  * auto-teste com respostas conhecidas (NIST, RFC 8032) e uma raiz final fixa.

O que NÃO garante: quem tiver acesso ao disco pode ler a chave e assinar registos NOVOS em nome
deste aparelho; não consegue apagar recibos que já estão nas mãos de outras pessoas. Apagar os
últimos registos do cofre só se vê comparando com um recibo ou um aperto de outra pessoa.
SELADO ≠ VERDADEIRO: o selo prova os bytes e a hora do aparelho, não a verdade do conteúdo.

Uso:
  python3 konfirmu_nova_geracao_2030.py --auto-teste
  python3 konfirmu_nova_geracao_2030.py selar FICHEIRO [--aceitar-relogio]
  python3 konfirmu_nova_geracao_2030.py verificar FICHEIRO [--recibo RECIBO.json]
  python3 konfirmu_nova_geracao_2030.py recibo SEQ            (recibo portátil, para dar a outra pessoa)
  python3 konfirmu_nova_geracao_2030.py conferir-cadeia
  python3 konfirmu_nova_geracao_2030.py aperto               (resumo < 1 KB para comparar com outro aparelho)
  python3 konfirmu_nova_geracao_2030.py comparar APERTO_A.json APERTO_B.json
  python3 konfirmu_nova_geracao_2030.py equivocacao RECIBO_A.json RECIBO_B.json
  python3 konfirmu_nova_geracao_2030.py chave                (chave pública deste aparelho)
  Opções: --cofre PASTA (por omissão ~/.konfirmu_2030) · --lingua pt|en
"""
from __future__ import annotations

import hashlib
import json
import os
import sqlite3
import sys
import tempfile
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

VERSAO = "2.0.0"
FORMATO = "konfirmu-2030/2"
DOMINIO = b"KONFIRMU-2030|v2|"
BLOCO_LEITURA = 64 * 1024
NUM_BALDES = 16
ZERO = "0" * 64

# Ponte de línguas: a chave é neutra (esperanto), o texto sai na língua pedida.
MENSAGENS = {
    "vera": {"pt": "VERIFICADO · os bytes são os que foram selados", "en": "VERIFIED · the bytes are the ones that were sealed"},
    "sangita": {"pt": "ALTERADO · os bytes não são os do recibo", "en": "ALTERED · the bytes are not the ones in the receipt"},
    "nekonata": {"pt": "SEM REGISTO · este conteúdo não está no cofre", "en": "NO RECORD · this content is not in the vault"},
    "sama_nomo": {"pt": "Há um ficheiro selado com este nome, mas com outro conteúdo", "en": "A file with this name was sealed, with different content"},
    "horlogo": {"pt": "RELÓGIO RECUOU · hora anterior à do último registo", "en": "CLOCK WENT BACK · time earlier than the last record"},
    "duobla": {"pt": "EQUIVOCAÇÃO · a mesma chave assinou duas versões do mesmo registo", "en": "EQUIVOCATION · the same key signed two versions of the same record"},
    "cadeno_bona": {"pt": "CADEIA CONFERE · todos os registos, elos e assinaturas", "en": "CHAIN OK · all records, links and signatures"},
    "cadeno_rompita": {"pt": "CADEIA PARTIDA", "en": "CHAIN BROKEN"},
}
LINGUA = "pt"


def msg(chave: str) -> str:
    return MENSAGENS[chave].get(LINGUA, MENSAGENS[chave]["pt"])


# ------------------------------------------------------------------ Ed25519 (RFC 8032, secção 6)
_P = 2 ** 255 - 19
_L = 2 ** 252 + 27742317777372353535851937790883648493
_D = -121665 * pow(121666, _P - 2, _P) % _P
_I = pow(2, (_P - 1) // 4, _P)


def _inv(x: int) -> int:
    return pow(x, _P - 2, _P)


def _rec_x(y: int, sinal: int) -> Optional[int]:
    if y >= _P:
        return None
    x2 = (y * y - 1) * _inv(_D * y * y + 1) % _P
    if x2 == 0:
        return None if sinal else 0
    x = pow(x2, (_P + 3) // 8, _P)
    if (x * x - x2) % _P:
        x = x * _I % _P
    if (x * x - x2) % _P:
        return None
    if (x & 1) != sinal:
        x = _P - x
    return x


_GY = 4 * _inv(5) % _P
_GX = _rec_x(_GY, 0)
_G = (_GX, _GY, 1, _GX * _GY % _P)


def _soma(p, q):
    a = (p[1] - p[0]) * (q[1] - q[0]) % _P
    b = (p[1] + p[0]) * (q[1] + q[0]) % _P
    c = 2 * p[3] * q[3] * _D % _P
    d = 2 * p[2] * q[2] % _P
    e, f, g, h = b - a, d - c, d + c, b + a
    return (e * f % _P, g * h % _P, f * g % _P, e * h % _P)


def _mult(s: int, p):
    q = (0, 1, 1, 0)
    while s > 0:
        if s & 1:
            q = _soma(q, p)
        p = _soma(p, p)
        s >>= 1
    return q


def _iguais(p, q) -> bool:
    return (p[0] * q[2] - q[0] * p[2]) % _P == 0 and (p[1] * q[2] - q[1] * p[2]) % _P == 0


def _comprimir(p) -> bytes:
    zi = _inv(p[2])
    x, y = p[0] * zi % _P, p[1] * zi % _P
    return int.to_bytes(y | ((x & 1) << 255), 32, "little")


def _descomprimir(s: bytes):
    if len(s) != 32:
        return None
    y = int.from_bytes(s, "little")
    sinal, y = y >> 255, y & ((1 << 255) - 1)
    x = _rec_x(y, sinal)
    return None if x is None else (x, y, 1, x * y % _P)


def _h512(m: bytes) -> int:
    return int.from_bytes(hashlib.sha512(m).digest(), "little")


def _expandir(semente: bytes):
    h = hashlib.sha512(semente).digest()
    a = int.from_bytes(h[:32], "little")
    a &= (1 << 254) - 8
    a |= 1 << 254
    return a, h[32:]


def chave_publica(semente: bytes) -> bytes:
    return _comprimir(_mult(_expandir(semente)[0], _G))


def assinar(semente: bytes, mensagem: bytes) -> bytes:
    a, prefixo = _expandir(semente)
    pub = _comprimir(_mult(a, _G))
    r = _h512(prefixo + mensagem) % _L
    rb = _comprimir(_mult(r, _G))
    s = (r + (_h512(rb + pub + mensagem) % _L) * a) % _L
    return rb + int.to_bytes(s, 32, "little")


def conferir_assinatura(pub: bytes, mensagem: bytes, assinatura: bytes) -> bool:
    if len(pub) != 32 or len(assinatura) != 64:
        return False
    pa, pr = _descomprimir(pub), _descomprimir(assinatura[:32])
    if pa is None or pr is None:
        return False
    s = int.from_bytes(assinatura[32:], "little")
    if s >= _L:
        return False
    h = _h512(assinatura[:32] + pub + mensagem) % _L
    return _iguais(_mult(s, _G), _soma(pr, _mult(h, pa)))


# ------------------------------------------------------------------ utilidades
def canonico(o) -> bytes:
    return json.dumps(o, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def hash_ficheiro(caminho: Path):
    h256, h512, n = hashlib.sha256(), hashlib.sha512(), 0
    with caminho.open("rb") as f:
        while True:
            b = f.read(BLOCO_LEITURA)
            if not b:
                break
            n += len(b)
            h256.update(b)
            h512.update(b)
    return h256.hexdigest(), h512.hexdigest(), n


def raiz_merkle(hashes: list) -> str:
    """Raiz Merkle pela ORDEM da cadeia (a ordem conta). Folha 0x00, nó 0x01 (sem colisões entre níveis)."""
    if not hashes:
        return hashlib.sha256(b"KONFIRMU-2030-VAZIO").hexdigest()
    nivel = [hashlib.sha256(b"\x00" + bytes.fromhex(h)).digest() for h in hashes]
    while len(nivel) > 1:
        nivel = [hashlib.sha256(b"\x01" + nivel[i] + (nivel[i + 1] if i + 1 < len(nivel) else nivel[i])).digest()
                 for i in range(0, len(nivel), 2)]
    return nivel[0].hex()


def hora_iso(ts: int) -> str:
    return datetime.fromtimestamp(ts, tz=timezone.utc).isoformat()


def conferir_recibo(recibo: dict) -> dict:
    """Confere um recibo portátil SÓ com o que vem nele (a chave pública). Não precisa do cofre."""
    try:
        bloco, hb, sig = recibo["bloco"], recibo["hash_bloco"], recibo["assinatura"]
        if recibo.get("recibo") != FORMATO or bloco.get("v") != FORMATO:
            return {"ok": False, "porque": "formato desconhecido"}
        if hashlib.sha256(canonico(bloco)).hexdigest() != hb:
            return {"ok": False, "porque": "o bloco não dá o hash_bloco do recibo"}
        if not conferir_assinatura(bytes.fromhex(bloco["pk"]), DOMINIO + bytes.fromhex(hb), bytes.fromhex(sig)):
            return {"ok": False, "porque": "assinatura inválida para esta chave pública"}
        return {"ok": True, "bloco": bloco}
    except (KeyError, ValueError, TypeError) as e:
        return {"ok": False, "porque": f"recibo mal formado ({e.__class__.__name__})"}


def equivocacao(recibo_a: dict, recibo_b: dict) -> dict:
    """Dois recibos válidos, mesma chave, mesmo número, blocos diferentes = prova de equivocação."""
    ra, rb = conferir_recibo(recibo_a), conferir_recibo(recibo_b)
    if not (ra["ok"] and rb["ok"]):
        return {"equivocacao": False, "porque": "um dos recibos não confere"}
    ba, bb = ra["bloco"], rb["bloco"]
    if ba["pk"] != bb["pk"] or ba["seq"] != bb["seq"]:
        return {"equivocacao": False, "porque": "chaves ou números diferentes"}
    if recibo_a["hash_bloco"] == recibo_b["hash_bloco"]:
        return {"equivocacao": False, "porque": "é o mesmo registo"}
    return {"equivocacao": True, "mensagem": msg("duobla"), "pk": ba["pk"], "seq": ba["seq"],
            "prova": [recibo_a, recibo_b]}


def comparar_apertos(a: dict, b: dict) -> dict:
    r = {"mesma_chave": a.get("pk") == b.get("pk"), "n": [a.get("n"), b.get("n")],
         "iguais": a.get("raiz") == b.get("raiz") and a.get("n") == b.get("n")}
    r["baldes_diferentes"] = [i for i, (x, y) in enumerate(zip(a.get("baldes", []), b.get("baldes", []))) if x != y]
    return r


# ------------------------------------------------------------------ cofre
class Cofre:
    def __init__(self, pasta: Path, semente: Optional[bytes] = None):
        self.pasta = pasta
        self.pasta.mkdir(parents=True, exist_ok=True)
        self.semente = semente if semente is not None else self._chave()
        self.pk = chave_publica(self.semente).hex()
        self.db = sqlite3.connect(str(pasta / "cofre_2030_v2.sqlite3"), isolation_level=None)
        self.db.execute("PRAGMA journal_mode=WAL")
        self.db.execute("PRAGMA synchronous=FULL")
        self.db.execute("CREATE TABLE IF NOT EXISTS cadeia (seq INTEGER PRIMARY KEY, bloco TEXT NOT NULL, hash_bloco TEXT NOT NULL,"
                        " assinatura TEXT NOT NULL, sha256 TEXT NOT NULL, nome TEXT NOT NULL)")
        self.db.execute("CREATE INDEX IF NOT EXISTS por_conteudo ON cadeia(sha256)")
        self.db.execute("PRAGMA user_version=2")

    def _chave(self) -> bytes:
        f = self.pasta / "dispositivo_ed25519.key"
        if f.is_file():
            return bytes.fromhex(f.read_text(encoding="utf-8").strip())
        semente = os.urandom(32)
        fd = os.open(str(f), os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)  # nasce já só para o dono
        with os.fdopen(fd, "w", encoding="utf-8") as fh:
            fh.write(semente.hex() + "\n")
        return semente

    def _ponta(self):
        return self.db.execute("SELECT seq, hash_bloco, bloco FROM cadeia ORDER BY seq DESC LIMIT 1").fetchone()

    def selar(self, caminho: Path, agora: Optional[int] = None, aceitar_relogio: bool = False) -> dict:
        if not caminho.is_file():
            raise FileNotFoundError(str(caminho))
        ts = int(time.time()) if agora is None else int(agora)
        s256, s512, n = hash_ficheiro(caminho)
        self.db.execute("BEGIN IMMEDIATE")
        try:
            ponta = self._ponta()
            seq, anterior = (ponta[0] + 1, ponta[1]) if ponta else (1, ZERO)
            bloco = {"v": FORMATO, "seq": seq, "ts": ts, "nome": caminho.name, "bytes": n, "sha256": s256, "sha512": s512,
                     "anterior": anterior, "pk": self.pk}
            if ponta:
                ultimo_ts = json.loads(ponta[2])["ts"]
                if ts < ultimo_ts:
                    if not aceitar_relogio:
                        raise RuntimeError(f"{msg('horlogo')} ({hora_iso(ts)} < {hora_iso(ultimo_ts)}). "
                                           "Se a hora certa é a de agora, repete com --aceitar-relogio: o registo fica marcado.")
                    bloco["relogio"] = "recuou"
                    bloco["ts_anterior"] = ultimo_ts
            hb = hashlib.sha256(canonico(bloco)).hexdigest()
            sig = assinar(self.semente, DOMINIO + bytes.fromhex(hb)).hex()
            self.db.execute("INSERT INTO cadeia VALUES (?,?,?,?,?,?)", (seq, canonico(bloco).decode("utf-8"), hb, sig, s256, caminho.name))
            self.db.execute("COMMIT")
        except BaseException:
            self.db.execute("ROLLBACK")
            raise
        return {"estado": msg("vera"), "recibo": {"recibo": FORMATO, "bloco": bloco, "hash_bloco": hb, "assinatura": sig}}

    def recibo(self, seq: int) -> dict:
        r = self.db.execute("SELECT bloco, hash_bloco, assinatura FROM cadeia WHERE seq=?", (seq,)).fetchone()
        if not r:
            raise KeyError(f"não há o registo {seq}")
        return {"recibo": FORMATO, "bloco": json.loads(r[0]), "hash_bloco": r[1], "assinatura": r[2]}

    def conferir_cadeia(self, assinaturas: bool = True) -> dict:
        anterior, esperado = ZERO, 1
        for seq, bloco_txt, hb, sig, s256, nome in self.db.execute("SELECT * FROM cadeia ORDER BY seq"):
            if seq != esperado:
                return {"ok": False, "mensagem": msg("cadeno_rompita"), "porque": f"falta o registo {esperado} (salta para {seq})"}
            try:
                bloco = json.loads(bloco_txt)
            except ValueError:
                return {"ok": False, "mensagem": msg("cadeno_rompita"), "porque": f"registo {seq} ilegível"}
            if hashlib.sha256(canonico(bloco)).hexdigest() != hb or canonico(bloco).decode("utf-8") != bloco_txt:
                return {"ok": False, "mensagem": msg("cadeno_rompita"), "porque": f"registo {seq} foi mudado"}
            if bloco.get("seq") != seq or bloco.get("anterior") != anterior or bloco.get("sha256") != s256 or bloco.get("nome") != nome:
                return {"ok": False, "mensagem": msg("cadeno_rompita"), "porque": f"registo {seq}: elo ou campos não batem"}
            if bloco.get("pk") != self.pk:
                return {"ok": False, "mensagem": msg("cadeno_rompita"), "porque": f"registo {seq} é de outra chave"}
            if assinaturas and not conferir_assinatura(bytes.fromhex(self.pk), DOMINIO + bytes.fromhex(hb), bytes.fromhex(sig)):
                return {"ok": False, "mensagem": msg("cadeno_rompita"), "porque": f"registo {seq}: assinatura inválida"}
            anterior, esperado = hb, esperado + 1
        return {"ok": True, "mensagem": msg("cadeno_bona"), "registos": esperado - 1, "ponta": anterior}

    def verificar(self, caminho: Path) -> dict:
        s256, s512, n = hash_ficheiro(caminho)
        cadeia = self.conferir_cadeia(assinaturas=False)  # elos e hashes de todos (rápido)
        if not cadeia["ok"]:
            return {"veredicto": "COFRE_PARTIDO", "mensagem": cadeia["mensagem"], "porque": cadeia["porque"], "sha256": s256}
        for seq, bloco_txt, hb, sig in self.db.execute("SELECT seq, bloco, hash_bloco, assinatura FROM cadeia WHERE sha256=? ORDER BY seq", (s256,)):
            bloco = json.loads(bloco_txt)
            if bloco["sha512"] == s512 and bloco["bytes"] == n and conferir_assinatura(bytes.fromhex(self.pk), DOMINIO + bytes.fromhex(hb), bytes.fromhex(sig)):
                return {"veredicto": "VERIFICADO", "mensagem": msg("vera"), "seq": seq, "nome_ao_selar": bloco["nome"],
                        "hora_do_aparelho": hora_iso(bloco["ts"]), "relogio": bloco.get("relogio", "normal"), "sha256": s256}
        mesmo_nome = self.db.execute("SELECT seq FROM cadeia WHERE nome=? ORDER BY seq DESC LIMIT 1", (caminho.name,)).fetchone()
        r = {"veredicto": "SEM_REGISTO", "mensagem": msg("nekonata"), "sha256": s256}
        if mesmo_nome:
            r["nota"] = f"{msg('sama_nomo')} (registo {mesmo_nome[0]})"
        return r

    def aperto(self) -> dict:
        hashes = [r[0] for r in self.db.execute("SELECT hash_bloco FROM cadeia ORDER BY seq")]
        baldes = [[] for _ in range(NUM_BALDES)]
        for h in hashes:
            baldes[int(h[:2], 16) % NUM_BALDES].append(h)
        corpo = {"v": "kcp-sync-2030/2", "pk": self.pk, "n": len(hashes), "ponta": hashes[-1] if hashes else ZERO,
                 "raiz": raiz_merkle(hashes), "baldes": [raiz_merkle(b)[:16] for b in baldes]}
        corpo["assinatura"] = assinar(self.semente, b"KONFIRMU-2030-APERTO|" + canonico(corpo)).hex()
        corpo["bytes"] = len(canonico(corpo))
        return corpo

    def fechar(self):
        self.db.close()


def conferir_aperto(a: dict) -> bool:
    corpo = {k: v for k, v in a.items() if k not in ("assinatura", "bytes")}
    try:
        return conferir_assinatura(bytes.fromhex(a["pk"]), b"KONFIRMU-2030-APERTO|" + canonico(corpo), bytes.fromhex(a["assinatura"]))
    except (KeyError, ValueError):
        return False


# ------------------------------------------------------------------ auto-teste
RAIZ_ESPERADA = "ac682ce103562045deaa686b63cee39689cb6f1659a47d1efdf7114adc32d2b7"  # raiz final do auto-teste determinista (regressão: qualquer mudança de formato falha aqui)


def auto_teste(mostrar: bool = True) -> bool:
    provas = []

    def prova(nome, ok):
        provas.append((nome, bool(ok)))
        if mostrar:
            print(("  ✓ " if ok else "  ✗ ") + nome)

    # 1. Respostas conhecidas: SHA-256/512 (NIST FIPS 180-4) e Ed25519 (RFC 8032, testes 1 a 3)
    prova("SHA-256 NIST (vazio, abc, 448 bits)",
          hashlib.sha256(b"").hexdigest() == "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855" and
          hashlib.sha256(b"abc").hexdigest() == "ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad" and
          hashlib.sha256(b"abcdbcdecdefdefgefghfghighijhijkijkljklmklmnlmnomnopnopq").hexdigest() == "248d6a61d20638b8e5c026930c3e6039a33ce45964ff2167f6ecedd419db06c1")
    rfc = [("9d61b19deffd5a60ba844af492ec2cc44449c5697b326919703bac031cae7f60", "d75a980182b10ab7d54bfed3c964073a0ee172f3daa62325af021a68f707511a", "",
            "e5564300c360ac729086e2cc806e828a84877f1eb8e5d974d873e065224901555fb8821590a33bacc61e39701cf9b46bd25bf5f0595bbe24655141438e7a100b"),
           ("4ccd089b28ff96da9db6c346ec114e0f5b8a319f35aba624da8cf6ed4fb8a6fb", "3d4017c3e843895a92b70aa74d1b7ebc9c982ccf2ec4968cc0cd55f12af4660c", "72",
            "92a009a9f0d4cab8720e820b5f642540a2b27b5416503f8fb3762223ebdb69da085ac1e43e15996e458f3613d0f11d8c387b2eaeb4302aeeb00d291612bb0c00"),
           ("c5aa8df43f9f837bedb7442f31dcb7b166d38535076f094b85ce3a2e0b4458f7", "fc51cd8e6218a1a38da47ed00230f0580816ed13ba3303ac5deb911548908025", "af82",
            "6291d657deec24024827e69c3abe01a30ce548a284743a445e3680d7db5ac3ac18ff9b538d16f290ae67f760984dc6594a7c15e9716ed28dc027beceea1ec40a")]
    ok = all(chave_publica(bytes.fromhex(sk)).hex() == pk and assinar(bytes.fromhex(sk), bytes.fromhex(m)).hex() == sg and
             conferir_assinatura(bytes.fromhex(pk), bytes.fromhex(m), bytes.fromhex(sg)) for sk, pk, m, sg in rfc)
    sg = bytearray(bytes.fromhex(rfc[1][3]))
    sg[5] ^= 1
    prova("Ed25519 RFC 8032 (testes 1-3) e assinatura com 1 bit trocado recusada",
          ok and not conferir_assinatura(bytes.fromhex(rfc[1][1]), bytes.fromhex(rfc[1][2]), bytes(sg)))

    semente = hashlib.sha256(b"konfirmu-auto-teste-2030").digest()  # chave fixa só do ensaio: tudo determinista
    def pseudo(n, s):
        out, c = bytearray(), 0
        while len(out) < n:
            out += hashlib.sha256(s + c.to_bytes(8, "big")).digest()
            c += 1
        return bytes(out[:n])
    with tempfile.TemporaryDirectory() as t:
        t = Path(t)
        (t / "a").mkdir()
        (t / "b").mkdir()
        c = Cofre(t / "cofre", semente)
        f1 = t / "a" / "relatorio_soldadura.bin"
        f1.write_bytes(pseudo(260_000, b"f1"))
        f2 = t / "a" / "contrato.pdf"
        f2.write_bytes(b"%PDF-1.4\n%\xe2\xe3\xcf\xd3\n" + pseudo(5000, b"f2"))
        f3 = t / "a" / "vazio.txt"
        f3.write_bytes(b"")
        T0 = 1795737600
        rec1 = c.selar(f1, T0)["recibo"]
        c.selar(f2, T0 + 60)
        c.selar(f3, T0 + 120)
        prova("ficheiro de 260 KB selado e VERIFICADO", c.verificar(f1)["veredicto"] == "VERIFICADO")
        f1b = t / "b" / "outro_nome.bin"
        f1b.write_bytes(f1.read_bytes())
        prova("mesmo conteúdo com outro nome, noutra pasta → VERIFICADO (procura pelo conteúdo)", c.verificar(f1b)["veredicto"] == "VERIFICADO")
        d = bytearray(f1.read_bytes())
        d[12345] ^= 1
        f1x = t / "b" / "relatorio_soldadura.bin"
        f1x.write_bytes(bytes(d))
        v = c.verificar(f1x)
        prova("1 bit trocado → não verificado, com nota de que há outro conteúdo com este nome", v["veredicto"] == "SEM_REGISTO" and "nota" in v)
        try:
            c.selar(f3, T0 + 100)
            bloqueou = False
        except RuntimeError:
            bloqueou = True
        prova("relógio a recuar → recusado", bloqueou)
        r4 = c.selar(f3, T0 + 100, aceitar_relogio=True)["recibo"]
        prova("com --aceitar-relogio continua, e o registo fica marcado «recuou»", r4["bloco"].get("relogio") == "recuou")
        prova("recibo portátil confere só com a chave pública (sem o cofre)", conferir_recibo(rec1)["ok"])
        falso = json.loads(json.dumps(rec1))
        falso["bloco"]["sha256"] = hashlib.sha256(b"outro").hexdigest()
        falso["hash_bloco"] = hashlib.sha256(canonico(falso["bloco"])).hexdigest()
        prova("recibo com o hash trocado (e recalculado) → assinatura não confere", not conferir_recibo(falso)["ok"])
        prova("cadeia inteira confere (elos, hashes e assinaturas)", c.conferir_cadeia()["ok"])
        orig = c.db.execute("SELECT bloco FROM cadeia WHERE seq=2").fetchone()[0]
        c.db.execute("UPDATE cadeia SET bloco=? WHERE seq=2", (orig.replace("contrato.pdf", "contrato2.pdf"),))
        prova("registo mudado diretamente na base de dados → cadeia partida", not c.conferir_cadeia()["ok"])
        c.db.execute("UPDATE cadeia SET bloco=? WHERE seq=2", (orig,))
        linha = c.db.execute("SELECT * FROM cadeia WHERE seq=2").fetchone()
        c.db.execute("DELETE FROM cadeia WHERE seq=2")
        prova("registo do meio apagado → cadeia partida e o verificar recusa dar VERIFICADO",
              not c.conferir_cadeia()["ok"] and c.verificar(f1)["veredicto"] == "COFRE_PARTIDO")
        c.db.execute("INSERT INTO cadeia VALUES (?,?,?,?,?,?)", linha)
        outra = hashlib.sha256(b"outra-chave").digest()
        hb2 = c.db.execute("SELECT hash_bloco FROM cadeia WHERE seq=2").fetchone()[0]
        sig_ok = c.db.execute("SELECT assinatura FROM cadeia WHERE seq=2").fetchone()[0]
        c.db.execute("UPDATE cadeia SET assinatura=? WHERE seq=2", (assinar(outra, DOMINIO + bytes.fromhex(hb2)).hex(),))
        prova("registo assinado por outra chave → cadeia partida", not c.conferir_cadeia()["ok"])
        c.db.execute("UPDATE cadeia SET assinatura=? WHERE seq=2", (sig_ok,))
        prova("cadeia volta a conferir depois de reposta", c.conferir_cadeia()["ok"])
        # Equivocação: a mesma chave reescreve a história a partir do registo 2
        c2 = Cofre(t / "cofre_clonado", semente)
        c2.selar(f1, T0)
        r2b = c2.selar(f1b, T0 + 60)["recibo"]
        e = equivocacao(c.recibo(2), r2b)
        prova("duas histórias da mesma chave no registo 2 → prova de equivocação que qualquer um confere",
              e["equivocacao"] and all(conferir_recibo(x)["ok"] for x in e["prova"]))
        prova("o mesmo recibo duas vezes não é equivocação", not equivocacao(c.recibo(2), c.recibo(2))["equivocacao"])
        a1, a2 = c.aperto(), c.aperto()
        prova(f"aperto de mão com {a1['bytes']} bytes (< 1024), assinado e igual nas 2 corridas", a1["bytes"] < 1024 and a1 == a2 and conferir_aperto(a1))
        cmp_ = comparar_apertos(a1, c2.aperto())
        prova("comparar apertos de dois aparelhos mostra que diferem e em que baldes", not cmp_["iguais"] and cmp_["mesma_chave"] and cmp_["baldes_diferentes"])
        raiz = a1["raiz"]
        c.fechar()
        c2.fechar()
    prova("raiz final igual à fixada (o formato não mudou sem se dar por isso)", raiz == RAIZ_ESPERADA)
    n_ok = sum(1 for _, ok in provas if ok)
    if mostrar:
        print(("VERDE" if n_ok == len(provas) else "VERMELHO") + f" — {n_ok}/{len(provas)} provas (respostas conhecidas, sabotagem, relógio, recibos, equivocação)")
    return n_ok == len(provas)


# ------------------------------------------------------------------ linha de comandos
def main(argv) -> int:
    global LINGUA
    args = list(argv)

    def opcao(nome, valor=True):
        if nome in args:
            i = args.index(nome)
            if valor:
                v = args[i + 1]
                del args[i:i + 2]
                return v
            del args[i]
            return True
        return None

    LINGUA = opcao("--lingua") or "pt"
    pasta = Path(opcao("--cofre") or (Path.home() / ".konfirmu_2030"))
    aceitar = bool(opcao("--aceitar-relogio", valor=False))
    recibo_f = opcao("--recibo")
    if not args or args[0] in ("--auto-teste", "auto-teste"):
        return 0 if auto_teste() else 1
    cmd = args[0]
    if cmd == "equivocacao" and len(args) == 3:
        r = equivocacao(*(json.loads(Path(x).read_text(encoding="utf-8")) for x in args[1:]))
    elif cmd == "comparar" and len(args) == 3:
        r = comparar_apertos(*(json.loads(Path(x).read_text(encoding="utf-8")) for x in args[1:]))
    elif cmd == "verificar" and len(args) == 2 and recibo_f:
        rec = json.loads(Path(recibo_f).read_text(encoding="utf-8"))
        cr = conferir_recibo(rec)
        if not cr["ok"]:
            r = {"veredicto": "RECIBO_INVALIDO", "porque": cr["porque"]}
        else:
            s256, s512, n = hash_ficheiro(Path(args[1]))
            igual = cr["bloco"]["sha256"] == s256 and cr["bloco"]["sha512"] == s512 and cr["bloco"]["bytes"] == n
            r = {"veredicto": "VERIFICADO" if igual else "ALTERADO", "mensagem": msg("vera" if igual else "sangita"),
                 "chave_publica": cr["bloco"]["pk"], "seq": cr["bloco"]["seq"], "hora_do_aparelho": hora_iso(cr["bloco"]["ts"])}
    else:
        c = Cofre(pasta)
        try:
            if cmd == "selar" and len(args) == 2:
                r = c.selar(Path(args[1]), aceitar_relogio=aceitar)
            elif cmd == "verificar" and len(args) == 2:
                r = c.verificar(Path(args[1]))
            elif cmd == "recibo" and len(args) == 2:
                r = c.recibo(int(args[1]))
            elif cmd == "conferir-cadeia":
                r = c.conferir_cadeia()
            elif cmd == "aperto":
                r = c.aperto()
            elif cmd == "chave":
                r = {"chave_publica_ed25519": c.pk}
            else:
                print(__doc__)
                return 2
        except (RuntimeError, FileNotFoundError, KeyError) as e:
            print(json.dumps({"erro": str(e)}, ensure_ascii=False, indent=2))
            return 1
        finally:
            c.fechar()
    print(json.dumps(r, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
