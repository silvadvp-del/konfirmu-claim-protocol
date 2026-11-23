#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# kcp_fhir.py — mapeamento KCP-vault -> HL7 FHIR R4 (Bundle JSON), ASSINADO pela casa.
# Honesto: é um MAPEAMENTO protótipo (estrutura FHIR R4); a conformidade oficial exige os
# validadores FHIR [VALIDAR]. stdlib-only. Motor importado com verificação de hash.
import hashlib, importlib.util, json, sys
from datetime import datetime, timezone
from pathlib import Path

ALVO = "529098c652ee8234960d69383e308f60db6a5df8ea6bdae578b538eb806e80cf"
MOTOR = Path(__file__).parent / "konfirmu_calc.py"
if hashlib.sha256(MOTOR.read_bytes()).hexdigest() != ALVO:
    sys.exit("motor diverge")
spec = importlib.util.spec_from_file_location("kc", MOTOR)
kc = importlib.util.module_from_spec(spec); sys.modules["kc"] = kc; spec.loader.exec_module(kc)

def vault_para_fhir(registos, paciente_nome, paciente_id, sk):
    agora = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    entries = [{"resource": {"resourceType": "Patient", "id": paciente_id,
                "name": [{"text": paciente_nome}], "active": True}}]
    for r in registos:
        if r["tipo"] == "alergia":
            entries.append({"resource": {"resourceType": "AllergyIntolerance", "id": "a" + str(len(entries)),
                "patient": {"reference": "Patient/" + paciente_id},
                "code": {"text": r["detalhe"]}, "recordedDate": r["data"],
                "clinicalStatus": {"text": "active"}}})
        elif r["tipo"] == "vacina":
            entries.append({"resource": {"resourceType": "Immunization", "id": "i" + str(len(entries)),
                "patient": {"reference": "Patient/" + paciente_id},
                "vaccineCode": {"text": r["detalhe"]}, "occurrenceDateTime": r["data"], "status": "completed"}})
        else:
            entries.append({"resource": {"resourceType": "Procedure", "id": "p" + str(len(entries)),
                "subject": {"reference": "Patient/" + paciente_id},
                "code": {"text": r["tipo"] + ": " + r["detalhe"]}, "performedDateTime": r["data"], "status": "completed"}})
    bundle = {"resourceType": "Bundle", "type": "collection", "timestamp": agora, "entry": entries}
    digest = kc.hobj({"bundle": bundle})[:64]
    selo = kc.selar({"fhir_digest": digest}, sk)
    bundle["extension"] = [{"url": "https://konfirmu.eu/fhir/seal",
        "valueString": digest + "|" + selo["sig"] + "|" + selo["pub"]}]
    return {"bundle": bundle, "digest": digest, "selo": selo}

def verificar_fhir(bundle, pub_esperada=None):
    dig_selo = bundle.get("extension", [{}])[0].get("valueString", "").split("|")
    if len(dig_selo) != 3:
        return {"ok": False, "linhas": ["FALHA extensão de selo"]}
    digest, sig, pub = dig_selo
    selo = {"alg": "Ed25519+SHA-256", "hash": kc.h256(kc.canon({"fhir_digest": digest})), "sig": sig, "pub": pub}
    ok_sig = kc.selo_ok({"fhir_digest": digest}, selo, {pub} if pub else set())
    sem_ext = {k: v for k, v in bundle.items() if k != "extension"}
    ok_hash = kc.hobj({"bundle": sem_ext})[:64] == digest
    ok_pub = (pub_esperada is None) or (pub == pub_esperada)
    return {"ok": ok_sig and ok_hash and ok_pub, "linhas": [
        ("OK " if ok_hash else "FALHA ") + "hash do Bundle",
        ("OK " if ok_sig else "FALHA ") + "assinatura Ed25519",
        ("OK " if ok_pub else "FALHA ") + "remetente conhecido"]}

def selftest():
    registos = [
        {"tipo": "alergia", "data": "2020-03-10", "detalhe": "penicilina (SINTÉTICO)"},
        {"tipo": "vacina", "data": "2026-11-01", "detalhe": "vacina exemplo (SINTÉTICO)"},
        {"tipo": "cirurgia", "data": "2019-05-20", "detalhe": "exemplo (SINTÉTICO)"},
    ]
    sk = kc.chave_demo("clinica-demo")
    p = vault_para_fhir(registos, "Paciente Sintético", "P-SINT-1", sk)
    r = verificar_fhir(p["bundle"])
    assert r["ok"], r["linhas"]
    b2 = json.loads(json.dumps(p["bundle"]))
    b2["entry"][1]["resource"]["code"]["text"] = "ALTERADO"
    r2 = verificar_fhir(b2)
    assert not r2["ok"]
    sk2 = kc.chave_demo("impostor-demo")
    p3 = vault_para_fhir(registos, "Paciente Sintético", "P-SINT-1", sk2)
    r3 = verificar_fhir(p3["bundle"], pub_esperada=kc.ed_publica(sk).hex())
    assert not r3["ok"]
    print("kcp_fhir SELFTEST VERDE")
    print("  digest:", p["digest"][:16] + "…", "| recursos:", len(p["bundle"]["entry"]), "| tamper/impostor FALHA")

if __name__ == "__main__":
    selftest()
