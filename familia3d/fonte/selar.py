#!/usr/bin/env python3
"""Escreve PASTA/SHA256SUMS.txt (formato do shasum) com o hash de cada ficheiro. Verificar: shasum -a 256 -c SHA256SUMS.txt"""
import hashlib
import os
import sys


def main():
    pasta = os.path.abspath(sys.argv[1])
    linhas = []
    for raiz, dirs, fichs in os.walk(pasta):
        dirs[:] = sorted(d for d in dirs if d != "__pycache__")
        for f in fichs:
            rel = os.path.relpath(os.path.join(raiz, f), pasta).replace(os.sep, "/")
            if rel == "SHA256SUMS.txt":
                continue
            with open(os.path.join(raiz, f), "rb") as fh:
                linhas.append((rel, hashlib.sha256(fh.read()).hexdigest()))
    linhas.sort()
    with open(os.path.join(pasta, "SHA256SUMS.txt"), "w", encoding="utf-8", newline="\n") as fh:
        fh.write("".join("%s  %s\n" % (h, rel) for rel, h in linhas))
    print("selado:", len(linhas), "ficheiros")


if __name__ == "__main__":
    main()
