#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""correcoes_ledger.py — correcções de referência para três defeitos do motor público · bancada · 27-11-2026

Janela: ZCODE-CHAVE-V3-20261121. Não muda o motor público. É uma referência: para entrar no motor é
por PR de quem tiver a fila. Construída por cima de konfirmu_calc.py v3.0.0, com o hash conferido.

OS TRÊS DEFEITOS (reproduzidos em provar_defeitos.py)
  1. O selo aceita 183 bits trocados no seu texto: a entrada «alg» (nome e valor) não é conferida, e
     as chaves e assinaturas em maiúsculas passam. Não se muda o objecto selado; muda o texto do selo.
  2. Uma escrita curta no disco devolve «gravado» sem ter gravado.
  3. Um disco cheio ou uma escrita cortada deixam o livro encravado para sempre ao reler.

O QUE ESTA REFERÊNCIA FAZ
  selo_estrito       só os quatro campos, «alg» exacto, hash/chave/assinatura em hexadecimal minúsculo.
  LedgerSegura       (a) o registo só fica em memória SE o disco o tiver inteiro, relido;
                     (b) se a escrita falhar, a memória e o disco voltam ao que eram;
                     (c) ao arrancar, uma cauda rasgada é isolada num ficheiro ao lado (com o hash) e o
                         livro arranca com os registos completos; um registo completo a que só falta a
                         mudança de linha é aceite e o ficheiro é reparado;
                     (d) o resto continua a falhar fechado, como o motor: registo estragado no meio ou
                         cadeia que não confere -> não arranca.

O QUE NÃO RESOLVE
  O recuo do relógio: não está no motor público (que não importa relógio nenhum).
  Não há reserva de espaço em disco: com o disco cheio, o registo dá erro em vez de se perder.
"""
import hashlib
import importlib.util
import json
import os
import re
import sys

ALVO_MOTOR = "529098c652ee8234960d69383e308f60db6a5df8ea6bdae578b538eb806e80cf"
CAMPOS_SELO = {"alg", "hash", "pub", "sig"}
ALG = "Ed25519+SHA-256"
_HEX64 = re.compile(r"[0-9a-f]{64}")
_HEX128 = re.compile(r"[0-9a-f]{128}")


def carregar_motor(caminho):
    """Carrega o motor público e recusa se o hash não for o da versão v3.0.0."""
    if hashlib.sha256(open(caminho, "rb").read()).hexdigest() != ALVO_MOTOR:
        sys.exit("motor diverge")
    espec = importlib.util.spec_from_file_location("kc_correcoes", caminho)
    motor = importlib.util.module_from_spec(espec)
    sys.modules["kc_correcoes"] = motor
    espec.loader.exec_module(motor)
    return motor


def selo_estrito(objeto, selo, motor, aceites=None):
    """A conferência do motor, mais três condições que fecham as 183 trocas aceites."""
    if not isinstance(selo, dict) or set(selo) != CAMPOS_SELO or selo["alg"] != ALG:
        return False
    if not (isinstance(selo["hash"], str) and isinstance(selo["pub"], str) and isinstance(selo["sig"], str)):
        return False
    if not (_HEX64.fullmatch(selo["hash"]) and _HEX64.fullmatch(selo["pub"]) and _HEX128.fullmatch(selo["sig"])):
        return False
    return motor.selo_ok(objeto, selo, aceites)


def partir(brutos):
    """Separa os registos completos (terminados por mudança de linha) do que vier depois do último."""
    i = brutos.rfind(b"\n")
    if i == len(brutos) - 1:
        return brutos, b""
    return brutos[:i + 1], brutos[i + 1:]


def _json(linha):
    try:
        b = json.loads(linha.decode("utf-8"))
    except (ValueError, UnicodeDecodeError):
        return None
    return b if isinstance(b, dict) else None


def classe_ledger_segura(motor):
    """Devolve a classe, atada ao motor já carregado."""

    class LedgerSegura(motor.LedgerPersistente):
        """O livro-razão do motor, com o disco e a memória sempre de acordo."""

        def __init__(self, sk_notario, caminho):
            motor.LedgerImutavel.__init__(self, sk_notario)
            self.caminho, self.recuperados = caminho, []
            if not os.path.exists(caminho):
                return
            with open(caminho, "rb") as fh:
                brutos = fh.read()
            corpo, cauda = partir(brutos)
            try:
                blocos = [json.loads(l.decode("utf-8")) for l in corpo.split(b"\n") if l]
            except (ValueError, UnicodeDecodeError):
                raise RuntimeError("LEDGER_ILEGIVEL: o ficheiro não é o que esta ledger escreveu")
            if not motor.conferir_blocos(blocos, self.pub):
                raise RuntimeError("LEDGER_CORROMPIDA: o ficheiro em disco não confere; não arranco por cima dele")
            if cauda:
                ultimo = _json(cauda)
                if ultimo is not None and motor.conferir_blocos(blocos + [ultimo], self.pub):
                    self._acrescentar(b"\n")
                    self.recuperados.append({"reparado": "mudanca_de_linha", "n": ultimo["n"]})
                    blocos = blocos + [ultimo]
                else:
                    self._cortar(len(corpo))
                    self._guardar_rasgado(cauda)
                    self.recuperados.append({"isolado": True, "bytes": len(cauda), "sha256": motor.h256(cauda)})
            self.blocos = blocos

        def registar(self, dia, evento, payload):
            antes, tamanho = len(self.blocos), self._tamanho()
            try:
                atual = motor.LedgerPersistente.registar(self, dia, evento, payload)
            except BaseException:
                self._recuar(antes, tamanho)
                raise
            if not self._esta_no_disco():
                self._recuar(antes, tamanho)
                raise RuntimeError("LEDGER_NAO_GRAVADA: o bloco não ficou inteiro no disco; não fica em memória. Repete o registo.")
            return atual

        def _tamanho(self):
            return os.path.getsize(self.caminho) if os.path.exists(self.caminho) else 0

        def _recuar(self, antes, tamanho):
            """A memória e o disco voltam ao que eram antes da tentativa."""
            del self.blocos[antes:]
            if self._tamanho() != tamanho:
                self._cortar(tamanho)

        def _cortar(self, n):
            fd = os.open(self.caminho, os.O_WRONLY)
            try:
                os.ftruncate(fd, n)
                os.fsync(fd)
            finally:
                os.close(fd)

        def _acrescentar(self, dados):
            fd = os.open(self.caminho, os.O_WRONLY | os.O_APPEND | os.O_CREAT, 0o600)
            try:
                os.write(fd, dados)
                os.fsync(fd)
            finally:
                os.close(fd)

        def _guardar_rasgado(self, cauda):
            """Os bytes rasgados não se perdem: ficam no ficheiro ao lado, com o tamanho e o hash."""
            nota = motor.canon({"v": "KONFIRMU-LEDGER-RASGADO/1", "bytes": len(cauda), "sha256": motor.h256(cauda)})
            fd = os.open(self.caminho + ".rasgados", os.O_WRONLY | os.O_APPEND | os.O_CREAT, 0o600)
            try:
                os.write(fd, nota + b"\n" + cauda + b"\n")
                os.fsync(fd)
            finally:
                os.close(fd)

        def _esta_no_disco(self):
            """Relê o fim do ficheiro: tem de acabar em mudança de linha e ter o último bloco inteiro."""
            with open(self.caminho, "rb") as fh:
                brutos = fh.read()
            return brutos.endswith(b"\n") and brutos.rsplit(b"\n", 2)[-2] == motor.canon(self.blocos[-1])

    return LedgerSegura
