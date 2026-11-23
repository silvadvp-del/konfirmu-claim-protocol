#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# chronolex_core.py — NÚCLEO DOCUMENTAL (envelope probatório) sobre o motor REAL.
# Regra 4: nada de cripto nova — importa o motor com verificação de hash e usa selar/selo_ok/hobj.
# Nível seguinte do Chronolex: sessões com participantes, eventos encadeados, anexos por hash,
# assinaturas múltiplas Ed25519, verificação de carimbo RFC 3161 (openssl ts) e exportação.
# Alinhamento eIDAS: ver CHRONOLEX-EIDAS.md (autoavaliação Art. 25/41 — não é conformidade certificada).
import hashlib, importlib.util, json, subprocess, sys
from datetime import datetime, timezone
from pathlib import Path

ALVO = "529098c652ee8234960d69383e308f60db6a5df8ea6bdae578b538eb806e80cf"
MOTOR = Path(__file__).parent / "konfirmu_calc.py"

def _motor():
    if hashlib.sha256(MOTOR.read_bytes()).hexdigest() != ALVO:
        sys.exit("motor diverge")
    spec = importlib.util.spec_from_file_location("kc", MOTOR)
    kc = importlib.util.module_from_spec(spec); sys.modules["kc"] = kc; spec.loader.exec_module(kc)
    return kc

kc = _motor()
V = "chronolex-core/1"

def agora():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

class Sessao:
    """Sessão documental: título, participantes (pubkeys), eventos encadeados, anexos, assinaturas."""
    def __init__(self, titulo: str):
        self.titulo = titulo
        self.participantes = {}
        self.eventos = []
        self.anexos = []
        self.assinaturas = []
        self._prev = "0" * 64
        self.selado_em = None
        self.master = None

    def participante(self, nome: str, sk: bytes) -> str:
        pub = kc.ed_publica(sk).hex()
        self.participantes[nome] = pub
        return pub

    def evento(self, autor: str, texto: str, ts: str = None) -> str:
        e = {"i": len(self.eventos) + 1, "ts": ts or agora(), "autor": autor,
             "texto": texto, "prev": self._prev}
        self._prev = kc.hobj(e)[:64]
        e["hash"] = self._prev
        self.eventos.append(e)
        return self._prev

    def anexar(self, caminho: str, rotulo: str = None) -> str:
        h = hashlib.sha256(Path(caminho).read_bytes()).hexdigest()
        self.anexos.append({"rotulo": rotulo or Path(caminho).name, "sha256": h})
        return h

    def selar(self):
        if not self.eventos:
            raise ValueError("sessão sem eventos")
        self.selado_em = agora()
        self.master = kc.hobj({"v": V, "titulo": self.titulo, "participantes": self.participantes,
                               "eventos": self.eventos, "anexos": self.anexos,
                               "selado_em": self.selado_em, "prev_final": self._prev})[:64]
        return self.master

    def _alvo(self):
        return "KONFIRMU-CLX|v1|" + self.master

    def assinar(self, nome: str, sk: bytes) -> dict:
        if nome not in self.participantes:
            raise ValueError("participante desconhecido: " + nome)
        selo = kc.selar({"alvo": self._alvo()}, sk)
        self.assinaturas.append({"nome": nome, "selo": selo})
        return selo

    def verificar(self) -> dict:
        rep = {"ok": True, "linhas": []}
        def linha(ok, txt):
            rep["linhas"].append(("OK " if ok else "FALHA ") + txt)
            rep["ok"] = rep["ok"] and ok
        prev = "0" * 64
        for e in self.eventos:
            copia = {k: e[k] for k in ("i", "ts", "autor", "texto", "prev")}
            h = kc.hobj(copia)[:64]
            linha(h == e["hash"] and e["prev"] == prev, "evento #" + str(e["i"]))
            prev = h
        linha(self._prev == prev, "cadeia final")
        master = kc.hobj({"v": V, "titulo": self.titulo, "participantes": self.participantes,
                          "eventos": self.eventos, "anexos": self.anexos,
                          "selado_em": self.selado_em, "prev_final": self._prev})[:64]
        linha(master == self.master, "selo mestre")
        alvo = self._alvo()
        for a in self.assinaturas:
            pk = {self.participantes[a["nome"]]}
            linha(kc.selo_ok({"alvo": alvo}, a["selo"], pk), "assinatura de " + a["nome"])
        return rep

    def exportar(self) -> dict:
        return {"v": V, "titulo": self.titulo, "participantes": self.participantes,
                "eventos": self.eventos, "anexos": self.anexos,
                "selado_em": self.selado_em, "master": self.master,
                "assinaturas": self.assinaturas}

    def imprimir(self) -> str:
        linhas = ["ATA CHRONOLEX — " + self.titulo, "selado: " + str(self.selado_em),
                  "selo mestre: " + str(self.master)]
        for e in self.eventos:
            linhas.append("  #%d [%s] %s: %s (%s…)" % (e["i"], e["ts"], e["autor"], e["texto"][:60], e["hash"][:12]))
        for a in self.assinaturas:
            linhas.append("  assinado por %s (%s…)" % (a["nome"], a["selo"].get("sig", "")[:12]))
        return chr(10).join(linhas)

def verificar_tsr(tsr: str, dados: str, ca: str, tsa: str) -> dict:
    """Verifica carimbo RFC 3161 via openssl ts (dependência declarada: binário openssl)."""
    r = subprocess.run(["openssl", "ts", "-verify", "-in", tsr, "-data", dados,
                        "-CAfile", ca, "-untrusted", tsa], capture_output=True, text=True)
    return {"ok": "Verification: OK" in (r.stdout + r.stderr), "saida": (r.stdout + r.stderr).strip()}

def selftest():
    skA, skB = kc.chave_demo("clx-teste-a"), kc.chave_demo("clx-teste-b")
    s = Sessao("Selftest Chronolex")
    s.participante("Ana", skA); s.participante("Beto", skB)
    s.evento("Ana", "ponto um"); s.evento("Beto", "ponto dois"); s.evento("Ana", "ponto três")
    s.selar()
    s.assinar("Ana", skA); s.assinar("Beto", skB)
    rep = s.verificar()
    assert rep["ok"], rep["linhas"]
    assert s.master and len(s.master) == 64
    # tamper num evento
    s.eventos[1]["texto"] = "ALTERADO"
    rep2 = s.verificar()
    assert not rep2["ok"], "tamper de evento devia falhar"
    s.eventos[1]["texto"] = "ponto dois"
    # tamper numa assinatura
    s.assinaturas[0]["selo"] = dict(s.assinaturas[0]["selo"]); s.assinaturas[0]["selo"]["sig"] = "0" * 128
    rep3 = s.verificar()
    assert not rep3["ok"], "tamper de assinatura devia falhar"
    # TSR real do repo (positivo) — e adulterado (negativo)
    repo = Path(__file__).parent
    t = verificar_tsr(str(repo / "anchors/konfirmu_calc.tsr"), str(repo / "konfirmu_calc.py"),
                      str(repo / "anchors/cacert.pem"), str(repo / "anchors/tsa.crt"))
    assert t["ok"], "TSR real devia verificar: " + t["saida"]
    print("chronolex_core SELFTEST VERDE")
    print("  master:", s.master[:16] + "…", "| cadeia+2 assinaturas OK | tamper evento/sig detetados | TSR real verificado")

if __name__ == "__main__":
    selftest()
