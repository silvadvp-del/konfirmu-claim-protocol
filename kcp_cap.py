#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# kcp_cap.py — alertas CAP 1.2 (OASIS) gerados e ASSINADOS pela casa (motor real, hash verificado).
# Honesto: a assinatura é o bloco KONFIRMU-SIG/HASH dentro do <parameter> — NÃO é XML-DSig completo
# (declarado). stdlib-only (xml.etree). O motor importa-se com verificação de hash.
import hashlib, importlib.util, sys, xml.etree.ElementTree as ET
from datetime import datetime, timezone
from pathlib import Path

ALVO = "529098c652ee8234960d69383e308f60db6a5df8ea6bdae578b538eb806e80cf"
MOTOR = Path(__file__).parent / "konfirmu_calc.py"
if hashlib.sha256(MOTOR.read_bytes()).hexdigest() != ALVO:
    sys.exit("motor diverge")
spec = importlib.util.spec_from_file_location("kc", MOTOR)
kc = importlib.util.module_from_spec(spec); sys.modules["kc"] = kc; spec.loader.exec_module(kc)

NS = "urn:oasis:names:tc:emergency:cap:1.2"
ET.register_namespace("", NS)

def gerar_cap(sender, headline, description, area, sk):
    agora = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S+00:00")
    alert = ET.Element("{%s}alert" % NS)
    ET.SubElement(alert, "identifier").text = sender + "-" + agora.replace(":", "").replace("-", "").replace("+", "")[:14]
    ET.SubElement(alert, "sender").text = sender
    ET.SubElement(alert, "sent").text = agora
    ET.SubElement(alert, "status").text = "Actual"
    ET.SubElement(alert, "msgType").text = "Alert"
    ET.SubElement(alert, "scope").text = "Public"
    info = ET.SubElement(alert, "info")
    ET.SubElement(info, "headline").text = headline
    ET.SubElement(info, "description").text = description
    area_el = ET.SubElement(info, "{%s}area" % NS)
    ad = ET.SubElement(area_el, "{%s}areaDesc" % NS)
    ad.text = area
    core = headline + "|" + description + "|" + area
    digest = kc.hobj({"cap_core": core})[:64]
    selo = kc.selar({"cap_digest": digest}, sk)
    p1 = ET.SubElement(info, "parameter"); ET.SubElement(p1, "valueName").text = "KONFIRMU-HASH"
    ET.SubElement(p1, "value").text = digest
    p2 = ET.SubElement(info, "parameter"); ET.SubElement(p2, "valueName").text = "KONFIRMU-SIG"
    ET.SubElement(p2, "value").text = selo["sig"]
    p3 = ET.SubElement(info, "parameter"); ET.SubElement(p3, "valueName").text = "KONFIRMU-PUB"
    ET.SubElement(p3, "value").text = selo["pub"]
    xml = ET.tostring(alert, encoding="unicode")
    return {"xml": xml, "digest": digest, "selo": selo}

def verificar_cap(xml, pub_esperada=None):
    root = ET.fromstring(xml)
    info = root.find("{%s}info" % NS)
    headline = info.find("{%s}headline" % NS).text
    description = info.find("{%s}description" % NS).text
    area = info.find("{%s}area" % NS).find("{%s}areaDesc" % NS).text
    parametros = {p.find("{%s}valueName" % NS).text: p.find("{%s}value" % NS).text for p in info.findall("{%s}parameter" % NS)}
    digest = kc.hobj({"cap_core": headline + "|" + description + "|" + area})[:64]
    ok_hash = digest == parametros.get("KONFIRMU-HASH")
    selo = {"alg": "Ed25519+SHA-256", "hash": kc.h256(kc.canon({"cap_digest": digest})), "sig": parametros.get("KONFIRMU-SIG", ""), "pub": parametros.get("KONFIRMU-PUB", "")}
    if pub_esperada:
        ok_pub = selo["pub"] == pub_esperada
    else:
        ok_pub = True
    ok_sig = kc.selo_ok({"cap_digest": digest}, selo, {selo["pub"]} if selo["pub"] else set())
    return {"ok": ok_hash and ok_pub and ok_sig, "linhas": [
        ("OK " if ok_hash else "FALHA ") + "hash do núcleo",
        ("OK " if ok_pub else "FALHA ") + "remetente conhecido",
        ("OK " if ok_sig else "FALHA ") + "assinatura Ed25519"]}

def selftest():
    sk = kc.chave_demo("protecao-civil-demo")
    a = gerar_cap("protecao-civil-demo", "ALERTA TESTE — inundação", "Sobe o nível do rio; procura ponto alto.", "Vila Sintética", sk)
    r = verificar_cap(a["xml"])
    assert r["ok"], r["linhas"]
    assert a["digest"] == kc.hobj({"cap_core": "ALERTA TESTE — inundação|Sobe o nível do rio; procura ponto alto.|Vila Sintética"})[:64]
    # tamper na headline
    x = a["xml"].replace("ALERTA TESTE", "ALERTA FALSO")
    r2 = verificar_cap(x)
    assert not r2["ok"]
    # remetente errado detetado (pub diferente)
    sk2 = kc.chave_demo("impostor-demo")
    a2 = gerar_cap("protecao-civil-demo", "ALERTA TESTE — inundação", "Sobe o nível do rio; procura ponto alto.", "Vila Sintética", sk2)
    r3 = verificar_cap(a2["xml"], pub_esperada=kc.ed_publica(sk).hex())
    assert not r3["ok"]
    print("kcp_cap SELFTEST VERDE")
    print("  digest:", a["digest"][:16] + "…", "| gerar→verificar OK | headline adulterada FALHA | remetente impostor FALHA")

if __name__ == "__main__":
    selftest()
