"""Sabotagem às correcções de referência. Uso: sabotar_correcoes.py <konfirmu_calc.py> <correcoes_ledger.py original> <pasta_de_trabalho>"""
import hashlib, json, os, re, shutil, subprocess, sys, time

MOTOR, ORIG, W = sys.argv[1:4]
SAIDA = os.path.join(W, "provas")
MUT = {
    "S01_sem_reler_o_disco": ('            return brutos.endswith(b"\\n") and brutos.rsplit(b"\\n", 2)[-2] == motor.canon(self.blocos[-1])', '            return True'),
    "S02_sem_desfazer_a_memoria": ('            del self.blocos[antes:]\n', ''),
    "S03_sem_cortar_o_ficheiro": ('            if self._tamanho() != tamanho:\n                self._cortar(tamanho)', '            if False:\n                self._cortar(tamanho)'),
    "S04_cauda_sem_conferir_a_cadeia": ('if ultimo is not None and motor.conferir_blocos(blocos + [ultimo], self.pub):', 'if ultimo is not None:'),
    "S05_isola_sem_cortar": ('                    self._cortar(len(corpo))\n', ''),
    "S06_sem_guardar_os_bytes_rasgados": ('                    self._guardar_rasgado(cauda)\n', ''),
    "S07_carrega_sem_conferir": ('            if not motor.conferir_blocos(blocos, self.pub):', '            if False:'),
    "S08_selo_sem_o_alg": (' or selo["alg"] != ALG', ''),
    "S09_selo_sem_minusculas": ('    if not (_HEX64.fullmatch(selo["hash"]) and _HEX64.fullmatch(selo["pub"]) and _HEX128.fullmatch(selo["sig"])):\n        return False\n', ''),
    "C0_controlo_neutro": ('Janela: ZCODE-CHAVE-V3-20261121. Não muda o motor público.', 'Janela: ZCODE-CHAVE-V3-20261121. Nao muda o motor público.'),
}
fonte = open(ORIG, encoding="utf-8").read()
h0 = hashlib.sha256(open(ORIG, "rb").read()).hexdigest()
res = []
for nome, (old, new) in MUT.items():
    assert fonte.count(old) == 1, (nome, fonte.count(old))
    destino = os.path.join(W, "mutantes", nome)
    shutil.rmtree(destino, ignore_errors=True)
    os.makedirs(destino)
    mutado = fonte.replace(old, new)
    open(os.path.join(destino, "correcoes_ledger.py"), "w", encoding="utf-8").write(mutado)
    inic = time.time()
    p = subprocess.run(["sandbox-exec", "-f", os.path.join(W, "caixa.sb"), "env", "-i", "PATH=/usr/bin:/bin", "HOME=" + os.path.join(W, "caixa", "home"), "TMPDIR=" + os.path.join(W, "caixa", "tmp"),
                        "LANG=pt_PT.UTF-8", sys.executable, "-I", "-B", os.path.join(W, "provar_correcoes.py"), MOTOR, destino, os.path.join(W, "caixa", "tmp")], capture_output=True, timeout=300)
    saida = p.stdout.decode("utf-8", "replace") + p.stderr.decode("utf-8", "replace")
    with open(os.path.join(SAIDA, "mutante_" + nome + ".log"), "w", encoding="utf-8") as f:
        f.write(saida + "\nEXIT=%d\n" % p.returncode)
    linhas = saida.splitlines()
    fim = next((l for l in reversed(linhas) if "TUDO VERDE" in l or "VERMELHO" in l), "(sem linha de resultado)")
    falhas = [l.strip() for l in linhas if re.match(r"^\[FALHOU\]", l)]
    r = {"mutante": nome, "troca_de": old, "troca_para": new, "sha256_do_mutante": hashlib.sha256(mutado.encode("utf-8")).hexdigest(), "exit": p.returncode, "resultado": fim,
         "a_vermelho": len(falhas), "primeiras": [l[:200] for l in falhas[:3]], "segundos": round(time.time() - inic, 1)}
    r["estado"] = "MORTO" if p.returncode != 0 or "TUDO VERDE" not in fim else "VIVO"
    res.append(r)
    print("%-38s %s  exit=%d  %s  a_vermelho=%d  %.0fs" % (nome, r["estado"], p.returncode, fim[:30], len(falhas), r["segundos"]), flush=True)
    shutil.rmtree(destino, ignore_errors=True)
with open(os.path.join(SAIDA, "SABOTAGEM_CORRECOES.json"), "w", encoding="utf-8") as f:
    json.dump(res, f, ensure_ascii=False, indent=1)
print("original intacto:", h0 == hashlib.sha256(open(ORIG, "rb").read()).hexdigest(), "| mortos:", sum(r["estado"] == "MORTO" for r in res if not r["mutante"].startswith("C0")), "de", len(res) - 1, "| controlo:", res[-1]["estado"])
