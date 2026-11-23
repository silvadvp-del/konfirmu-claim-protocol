# Cartuchos oficiais (v1) — validados pelo kcp_lint

Cada cartucho é um JSON determinístico: fórmula com whitelist AST (sem eval), limites, vectores de teste e veto no pior caso direccional. Regra: os limiares citam a norma; onde falta fonte selada, está ASSUMIDO [VALIDAR] no próprio cartucho (campo o_que_nao_garante). Submeter um cartucho novo = Pull Request; o CI (kcp_cartridge_ci.yml) valida antes de aceitar.
